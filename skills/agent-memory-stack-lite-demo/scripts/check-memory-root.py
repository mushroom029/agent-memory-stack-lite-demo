#!/usr/bin/env python3
"""Lightweight validator for a Lite Demo context-memory project root."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


FIELD_RE = re.compile(r"^\s*-\s*([^:\n]+):\s*(.*)$", re.MULTILINE)
CAPSULE_ID_RE = re.compile(r"\b(C[0-9][0-9A-Za-z_-]*)\b")
ROUTE_LINE_RE = re.compile(r"^\s*-\s*([^:]+):\s*(.+)$")
ROUTE_FIELD_RE = re.compile(r"(?:^|;)\s*([a-z][a-z0-9_-]*)\s*=\s*([^;]*)", re.I)
REVIEW_RE = re.compile(r"\[REVIEW:([A-Za-z0-9._-]+)\]")
MEMORY_ID_RE = re.compile(r"^\s*-\s*Memory ID:\s*([^\s]+)\s*$", re.I | re.MULTILINE)
VALUE_SPLIT_RE = re.compile(r"\s*[,|，]\s*")
SECRET_PATTERNS = (
    re.compile(r"(?i)\b(?:api[_ -]?key|secret|password|token)\s*[:=]\s*[^\s`]{8,}"),
    re.compile(r"(?i)\bbearer\s+[a-z0-9._-]{12,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)
CURRENT_CONTEXT_SOFT_CHARS = 8_000
ROUTING_INDEX_SOFT_CHARS = 12_000
ROUTING_LINE_SOFT_CHARS = 800
ACTIVE_TASK_SOFT_CHARS = 16_000
SESSION_LOG_TAIL_ONLY_LINES = 240
NARRATIVE_LINE_SOFT_CHARS = 500
NARRATIVE_DUPLICATION_SOFT_CHARS = 180
MEMORY_SCHEMA_VERSION = "v0.2.6"
STRICT_ROUTING_WARNING_PARTS = (
    "has no Memory schema",
    "has no Module aliases section",
    "has owners= but no normative body owner",
    "points to missing owner",
    "owner fragment was not found",
    "has no wake-up route",
    "has no status=pending-review owner route",
    "repeats live route fields",
    "appears to contain chronological sections",
    "has a long narrative line",
    "has multiple body owners",
)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text()


def fields(text: str) -> dict[str, str]:
    return {m.group(1).strip().lower(): m.group(2).strip() for m in FIELD_RE.finditer(text)}


def has_field_value(text: str, names: tuple[str, ...]) -> bool:
    found = fields(text)
    for name in names:
        value = found.get(name.lower(), "")
        if value and value not in {"-", "n/a", "none", "None"}:
            return True
    return False


def is_active_task(text: str) -> bool:
    status = fields(text).get("status", "").lower()
    return status != "complete"


def index_capsule_ids(index_text: str) -> set[str]:
    ids: set[str] = set()
    for line in index_text.splitlines():
        if "capsules=" in line.lower() or re.match(r"\s*-\s*C[0-9A-Za-z_-]+\s*:", line):
            ids.update(CAPSULE_ID_RE.findall(line))
    return ids


def route_entries(index_text: str) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for line_number, line in enumerate(index_text.splitlines(), 1):
        match = ROUTE_LINE_RE.match(line)
        if not match or "owners=" not in line.casefold():
            continue
        route_fields = {
            key.casefold(): value.strip() for key, value in ROUTE_FIELD_RE.findall(match.group(2))
        }
        owners = [
            item.strip().strip("`\"'")
            for item in VALUE_SPLIT_RE.split(route_fields.get("owners", ""))
            if item.strip().strip("`\"'").casefold() not in {"", "none", "n/a"}
        ]
        mandatory = [
            item.strip().strip("`\"'")
            for item in VALUE_SPLIT_RE.split(route_fields.get("mandatory", ""))
            if item.strip().strip("`\"'").casefold() not in {"", "none", "n/a"}
        ]
        entries.append(
            {
                "scope": match.group(1).strip(),
                "owners": owners,
                "mandatory": mandatory,
                "status": route_fields.get("status", ""),
                "line": line_number,
            }
        )
    return entries


def pointer_path(root: Path, pointer: str) -> Path:
    relative = pointer.split("#", 1)[0]
    return (root / relative).resolve()


def pointer_fragment(pointer: str) -> str:
    return pointer.split("#", 1)[1] if "#" in pointer else ""


def narrative_units(text: str) -> set[str]:
    units: set[str] = set()
    for line in text.splitlines():
        candidate = re.sub(r"^\s*(?:[-*#]+|\d+\.)\s*", "", line).strip()
        candidate = re.sub(r"\s+", " ", candidate)
        if len(candidate) >= NARRATIVE_DUPLICATION_SOFT_CHARS:
            units.add(candidate.casefold())
    for block in re.split(r"\n\s*\n", text):
        candidate = re.sub(r"\s+", " ", block).strip()
        if len(candidate) >= NARRATIVE_DUPLICATION_SOFT_CHARS:
            units.add(candidate.casefold())
    return units


def repeated_live_fields(text: str) -> list[str]:
    counts: dict[str, int] = defaultdict(int)
    live_names = {"status", "current step", "completed", "next exact step", "route check"}
    for match in FIELD_RE.finditer(text):
        name = match.group(1).strip().casefold()
        if name in live_names:
            counts[name] += 1
    return sorted(name for name, count in counts.items() if count > 1)


def has_secret_like_text(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not root.exists():
        return [f"memory root does not exist: {root}"], warnings
    if not root.is_dir():
        return [f"memory root is not a directory: {root}"], warnings

    current = root / "current-context.md"
    index = root / "index.md"
    session_log = root / "session-log.md"
    active_task = root / "active-task.md"
    capsules_dir = root / "capsules"

    for required in (current, index):
        if not required.exists():
            errors.append(f"missing required file: {required.name}")

    current_text = read_text(current) if current.exists() else ""
    index_text = read_text(index) if index.exists() else ""
    active_text = read_text(active_task) if active_task.exists() else ""
    session_text = read_text(session_log) if session_log.exists() else ""
    active_paths = [active_task] if active_task.exists() else []
    tasks_dir = root / "tasks"
    if tasks_dir.exists():
        active_paths.extend(sorted(tasks_dir.glob("*/active-task.md")))

    if len(current_text) > CURRENT_CONTEXT_SOFT_CHARS:
        warnings.append(
            "current-context.md is large for an always-read live anchor; move durable detail to capsules"
        )
    if len(index_text) > ROUTING_INDEX_SOFT_CHARS:
        warnings.append(
            "index.md is large for a routing layer; keep keyword/alias/topic -> pointer + one short reason, without limiting selected capsules"
        )
    if any(len(line) > ROUTING_LINE_SOFT_CHARS for line in index_text.splitlines()):
        warnings.append("index.md has a long routing entry that may contain capsule detail")

    for label, text in (("current-context.md", current_text), ("index.md", index_text)):
        if any(len(line) > NARRATIVE_LINE_SOFT_CHARS for line in text.splitlines()):
            warnings.append(
                f"{label} has a long narrative line; keep only active state or compact owner routes"
            )

    if len(active_text) > ACTIVE_TASK_SOFT_CHARS:
        warnings.append(
            "active-task.md is large and may be carrying chronology; keep the current route, critical corrections, rejected paths, stable boundaries, evidence pointers, and next exact step"
        )
    if len(session_text.splitlines()) > SESSION_LOG_TAIL_ONLY_LINES:
        warnings.append(
            "session-log.md is long; preserve the complete local log but use only a recent tail or targeted search/range for recovery"
        )

    for path in active_paths:
        task_text = read_text(path)
        task_label = str(path.relative_to(root))
        if is_active_task(task_text):
            if not has_field_value(task_text, ("next exact step",)):
                errors.append(f"{task_label} is active but has no Next exact step")
            if not has_field_value(task_text, ("mode",)):
                warnings.append(f"{task_label} has no Mode")
            if not has_field_value(task_text, ("activation packet",)):
                warnings.append(f"{task_label} has no Activation packet")
        repeated = repeated_live_fields(task_text)
        if repeated:
            warnings.append(
                f"{task_label} repeats live route fields ({', '.join(repeated)}); replace stale values instead of appending history"
            )
        if re.search(r"(?im)^##\s+(?:batch|run audit|history|timeline)\b", task_text):
            warnings.append(f"{task_label} appears to contain chronological sections")

    mode_text = "\n".join([current_text, active_text]).lower()
    in_stabilization = "testing/stabilization" in mode_text
    if in_stabilization:
        combined = "\n".join([current_text, active_text, index_text])
        combined_lower = combined.lower()
        if not (
            has_field_value(
                combined,
                ("stable behavior", "stable/protected behavior", "protected stable behavior"),
            )
            or "stable=" in combined_lower
        ):
            warnings.append("testing/stabilization mode has no stable behavior")
        if not (
            has_field_value(combined, ("regression guards", "regression guard index"))
            or "guards=" in combined_lower
        ):
            warnings.append("testing/stabilization mode has no regression guards")

    if index_text:
        schema = fields(index_text).get("memory schema", "")
        if schema.casefold() != MEMORY_SCHEMA_VERSION.casefold():
            warnings.append(
                f"index.md has no Memory schema: {MEMORY_SCHEMA_VERSION} takeover marker"
            )

        ids = index_capsule_ids(index_text)
        if ids and not capsules_dir.exists():
            errors.append("index.md references capsules but capsules/ is missing")
        for cid in sorted(ids):
            if cid.lower() == "ids":
                continue
            if not (capsules_dir / f"{cid}.md").exists():
                errors.append(f"index.md references missing capsule: capsules/{cid}.md")

        index_lower = index_text.lower()
        if "pressure signal index" in index_lower or "pressure=" in index_lower:
            if "status=" not in index_lower:
                warnings.append("Pressure signal entry has no status=active|historical|resolved entries")
            if "capsules=" not in index_lower and not session_log.exists():
                warnings.append("Pressure signal entry has no capsule link and no session-log.md evidence")

        if "module aliases" not in index_text.lower():
            warnings.append("index.md has no Module aliases section")

        routes = route_entries(index_text)
        routed_pointers = {
            pointer for route in routes for pointer in (*route["owners"], *route["mandatory"])
        }
        for route in routes:
            if not route["owners"]:
                warnings.append(
                    f"index.md route '{route['scope']}' has owners= but no normative body owner"
                )
            for pointer in (*route["owners"], *route["mandatory"]):
                target = pointer_path(root, pointer)
                if not target.is_file():
                    warnings.append(
                        f"index.md route '{route['scope']}' points to missing owner: {pointer}"
                    )
                    continue
                fragment = pointer_fragment(pointer)
                if fragment and fragment.casefold() not in read_text(target).casefold():
                    warnings.append(
                        f"index.md route '{route['scope']}' owner fragment was not found: {pointer}"
                    )

        if capsules_dir.exists():
            normalized_routed = {
                pointer_path(root, pointer) for pointer in routed_pointers if pointer
            }
            for capsule in sorted(capsules_dir.glob("*.md")):
                if capsule.resolve() not in normalized_routed:
                    warnings.append(
                        f"{capsule.relative_to(root)} has no wake-up route in index.md"
                    )

        for review_id in sorted(set(REVIEW_RE.findall(session_text))):
            expected_fragment = f"REVIEW:{review_id}".casefold()
            pending = any(
                route["status"].casefold() == "pending-review"
                and any(expected_fragment in pointer.casefold() for pointer in route["owners"])
                for route in routes
            )
            if not pending:
                warnings.append(
                    f"session-log.md [REVIEW:{review_id}] has no status=pending-review owner route"
                )

    memory_files = [current, index, active_task, session_log]
    memory_files.extend(path for path in active_paths if path != active_task)
    if capsules_dir.exists():
        memory_files.extend(sorted(capsules_dir.glob("*.md")))
    for memory_file in memory_files:
        if memory_file.exists() and has_secret_like_text(read_text(memory_file)):
            warnings.append(
                f"{memory_file.relative_to(root)} contains secret-like text; review and redact before sharing or persisting"
            )

    ids_by_file: dict[str, list[str]] = defaultdict(list)
    units_by_file: dict[Path, set[str]] = {}
    for memory_file in memory_files:
        if not memory_file.exists():
            continue
        text = read_text(memory_file)
        units_by_file[memory_file] = narrative_units(text)
        for memory_id in MEMORY_ID_RE.findall(text):
            ids_by_file[memory_id.casefold()].append(str(memory_file.relative_to(root)))
    for memory_id, owners in sorted(ids_by_file.items()):
        if len(set(owners)) > 1:
            warnings.append(
                f"Memory ID {memory_id} has multiple body owners: {', '.join(sorted(set(owners)))}"
            )

    duplicate_pairs: list[str] = []
    unit_items = list(units_by_file.items())
    for index_a, (path_a, units_a) in enumerate(unit_items):
        for path_b, units_b in unit_items[index_a + 1 :]:
            if units_a.intersection(units_b):
                duplicate_pairs.append(
                    f"{path_a.relative_to(root)} <-> {path_b.relative_to(root)}"
                )
    if duplicate_pairs:
        warnings.append(
            "long narrative appears in multiple memory layers: " + "; ".join(duplicate_pairs[:5])
        )

    return errors, warnings


def strict_routing_warnings(
    warnings: list[str], allow_missing_schema: bool = False
) -> list[str]:
    return [
        warning
        for warning in warnings
        if any(part in warning for part in STRICT_ROUTING_WARNING_PARTS)
        and not (allow_missing_schema and "has no Memory schema" in warning)
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Path to docs/codex or another context memory root")
    parser.add_argument(
        "--strict-routing",
        action="store_true",
        help="Fail when takeover-critical ownership or reachability warnings remain",
    )
    parser.add_argument(
        "--allow-missing-schema",
        action="store_true",
        help="Allow the pre-completion strict gate to run before apply writes the schema marker",
    )
    args = parser.parse_args()

    errors, warnings = validate(args.root)
    strict_warnings = (
        strict_routing_warnings(warnings, args.allow_missing_schema)
        if args.strict_routing
        else []
    )
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors or strict_warnings:
        if strict_warnings:
            print(f"STRICT: {len(strict_warnings)} takeover-critical warning(s)")
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK: 0 error(s), {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
