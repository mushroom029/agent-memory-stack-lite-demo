#!/usr/bin/env python3
"""Lightweight validator for a Lite Demo context-memory project root."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path


FIELD_RE = re.compile(r"^\s*-\s*([^:\n]+):\s*(.*)$", re.MULTILINE)
CAPSULE_POINTER_RE = re.compile(r"^capsules/([^/#]+)\.md(?:#.*)?$", re.I)
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
MEMORY_SCHEMA_VERSION = "v0.2.7"
CURRENT_CHECKPOINT_MARKER = "<!-- LITE-DEMO-V0.2.7-CHECKPOINT -->"
CHECKPOINT_FILE = ".takeover-checkpoint"
MEMORY_SCHEMA_RE = re.compile(
    r"^[ \t]*-[ \t]*Memory schema:[ \t]*(\S+)[ \t]*\r?$", re.I | re.MULTILINE
)
CHECKPOINT_LENGTH_RE = re.compile(r"^- Legacy prefix bytes:\s*(\d+)\s*$", re.MULTILINE)
CHECKPOINT_HASH_RE = re.compile(
    r"^- Legacy prefix SHA256:\s*([0-9A-Fa-f]{64})\s*$", re.MULTILINE
)
CHECKPOINT_KIND_RE = re.compile(r"^- Checkpoint kind:\s*(\S+)\s*$", re.MULTILINE)
LEGACY_DESTINATIONS_FILE = "legacy-destinations.md"
LEGACY_DESTINATION_ALLOWED_STATUSES = {
    "memory-owner",
    "mandatory-guard",
    "rejected-path",
    "project-owner-indexed",
    "archived-only",
    "pending-review",
}
LEGACY_DESTINATION_OWNER_STATUSES = {
    "memory-owner",
    "mandatory-guard",
    "rejected-path",
    "project-owner-indexed",
}
LEGACY_DESTINATION_PROBE_STATUSES = {
    "memory-owner",
    "mandatory-guard",
    "rejected-path",
    "project-owner-indexed",
}
GENERIC_LEGACY_WAKE_TERMS = {
    "legacy",
    "legacy source",
    "legacy active task",
    "legacy context",
    "legacy index",
    "legacy destination",
    "legacy capsule",
    "capsule",
    "capsule owner",
    "current context",
    "active task",
    "session log",
    "import",
    "import evidence",
    "owner",
    "route",
    "source",
    "evidence",
}
GENERIC_LEGACY_REASONS = {
    "import route",
    "preserved cold evidence",
    "legacy source",
    "legacy evidence",
}
LEGACY_FILE_ROLE_SCOPE_RE = re.compile(
    r"^(?:"
    r"c[0-9][0-9a-z_-]*|"
    r"capsules[-_/\\]c[0-9][0-9a-z_-]*|"
    r"capsules[-_/\\][^\\/]+|"
    r"active-task|current-context|index|session-log|legacy-destinations|"
    r"\.takeover-checkpoint"
    r")$",
    re.I,
)
LEGACY_CAPSULE_SOURCE_RE = re.compile(r"(?:^|[\\/])capsules[\\/][^\\/]+\.md$", re.I)
MEMORY_LAYER_OWNER_RE = re.compile(
    r"^(?:"
    r"capsules/|tasks/|routes/|current-context\.md|active-task\.md|"
    r"index\.md|session-log\.md|legacy-destinations\.md"
    r")",
    re.I,
)
LEGACY_REQUIREMENT_SIGNAL_RE = re.compile(
    r"\[REVIEW:|Run Audit|Memory ID:|Requirement Ledger|forbidden-action|"
    r"acceptance[- ]?(?:gate|criterion)|correction[- ]?guard|rejected[- ]?path|"
    r"regression[- ]?guard|stable behavior|explicit prohibition|"
    r"\bdo not\b|\bdon't\b|\bmust\b|\bnever\b|\bforbidden\b|\bprohibit|\brequir|"
    r"禁止|不要|不得|不能|不允许|必须|务必|验收|纠正|否决|驳回|拒绝|"
    r"不要再|边界|保护|稳定|回滚|压力|骂|生气|愤怒|崩溃",
    re.I,
)
LEGACY_TEMPLATE_LINE_RE = re.compile(
    r"^\s*(?:"
    r"#\s*(?:Current Context|Context Index|Session Log|Active Task)|"
    r"##\s*(?:Module Aliases|Module Index|Lite Demo v0\.2\.7 Memory Checkpoint)|"
    r"-\s*(?:Updated|Project|Project phase|Memory landing policy|Lite demo activation phrase|"
    r"Natural start phrase|Explicit safe phrase|Legacy compatibility phrase|Current anchor|"
    r"Task branches|Active topic|Owner router|Checkpoint kind|Recorded UTC|"
    r"Legacy prefix bytes|Legacy prefix SHA256|Rule):|"
    r"-\s*Active goal:\s*Not set yet\.|"
    r"-\s*Active task pointer:\s*none\.|"
    r"-\s*Selected owner routes:\s*none\b|"
    r"-\s*Stable/protected behavior:\s*Not set yet\b|"
    r"-\s*Next step:\s*Ask for the real task\b|"
    r"-\s*Memory hygiene:\s*(?:one-off requests|ambiguous one-off requests)\b|"
    r"-\s*Legacy source import:\s*if the user names\b|"
    r"-\s*Old-user takeover:\s*package v[0-9.]+\b|"
    r"-\s*Execution route:\s*sniff once\b|"
    r"-\s*(?:task|branch|route|recovery|owner|boundary):\s|"
    r"-\s*Notes:\s*Add a compact\b|"
    r"<!--\s*LITE-DEMO-|"
    r"-\s*Memory schema:\s*v0\.2\.7"
    r")",
    re.I,
)
LEGACY_SURFACE_NAMES = ("current-context.md", "index.md", "active-task.md")
LEGACY_SURFACE_DIRS = ("capsules", "tasks", "routes")
PRIMARY_OWNER_FANOUT_SOFT_COUNT = 8
STRICT_ROUTING_WARNING_PARTS = (
    "has no Memory schema",
    "has no Module aliases section",
    "has owners= but no normative body owner",
    "points to missing owner",
    "references missing capsule",
    "owner fragment was not found",
    "has no wake-up route",
    "has no status=pending-review owner route",
    "repeats live route fields",
    "appears to contain chronological sections",
    "has a long narrative line",
    "has multiple body owners",
    "points outside routes/ for history",
    "points to missing history route",
    "history route nesting exceeds one level",
    "history route page has no top-level pointer",
    "appears in both primary and history routes",
    "has current schema but no v0.2.7 checkpoint",
    "Memory schema entries; exactly one required",
    "must contain exactly one v0.2.7 checkpoint",
    "v0.2.7 checkpoint is invalid",
    "legacy-destinations.md",
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
    for route in route_entries(index_text):
        for pointer in (*route["owners"], *route["mandatory"]):
            normalized = pointer.strip().replace("\\", "/")
            match = CAPSULE_POINTER_RE.match(normalized)
            if match:
                ids.add(match.group(1))
    return ids


def route_entries(index_text: str, source: str = "index.md") -> list[dict[str, object]]:
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
        history = [
            item.strip().strip("`\"'")
            for item in VALUE_SPLIT_RE.split(route_fields.get("history", ""))
            if item.strip().strip("`\"'").casefold() not in {"", "none", "n/a"}
        ]
        entries.append(
            {
                "scope": match.group(1).strip(),
                "owners": owners,
                "mandatory": mandatory,
                "history": history,
                "status": route_fields.get("status", ""),
                "line": line_number,
                "source": source,
            }
        )
    return entries


def route_values(value: str) -> list[str]:
    return [
        item.strip().strip("`\"'")
        for item in VALUE_SPLIT_RE.split(value or "")
        if item.strip().strip("`\"'").casefold() not in {"", "none", "n/a"}
    ]


def semantic_legacy_terms(values: list[str]) -> list[str]:
    semantic: list[str] = []
    for value in values:
        normalized = re.sub(r"\s+", " ", value.strip().casefold())
        if not normalized:
            continue
        if normalized in GENERIC_LEGACY_WAKE_TERMS:
            continue
        if LEGACY_FILE_ROLE_SCOPE_RE.match(normalized):
            continue
        semantic.append(value)
    return semantic


def is_memory_layer_owner(pointer: str) -> bool:
    return MEMORY_LAYER_OWNER_RE.match(pointer.strip().replace("\\", "/")) is not None


def legacy_prefix_text(session_text: str) -> str:
    marker_index = session_text.find(CURRENT_CHECKPOINT_MARKER)
    return session_text[:marker_index] if marker_index >= 0 else session_text


def meaningful_legacy_lines(text: str) -> list[str]:
    return [
        line.strip()
        for line in text.splitlines()
        if line.strip()
        and line.strip() != "# Session Log"
        and not LEGACY_TEMPLATE_LINE_RE.match(line.strip())
    ]


def has_meaningful_legacy_text(text: str) -> bool:
    if not text.strip():
        return False
    meaningful_lines = meaningful_legacy_lines(text)
    if not meaningful_lines:
        return False
    meaningful_text = "\n".join(meaningful_lines)
    if LEGACY_REQUIREMENT_SIGNAL_RE.search(meaningful_text):
        return True
    if re.search(
        r"(?im)^##\s+(?!Lite Demo v0\.2\.[0-9]+ .*Checkpoint)",
        meaningful_text,
    ):
        return True
    return len(meaningful_lines) >= 20


def has_meaningful_legacy_history(prefix_text: str) -> bool:
    return has_meaningful_legacy_text(prefix_text)


def iter_legacy_surface_paths(root: Path) -> tuple[Path, ...]:
    paths: list[Path] = []
    for name in LEGACY_SURFACE_NAMES:
        candidate = root / name
        if candidate.is_file():
            paths.append(candidate)
    for directory_name in LEGACY_SURFACE_DIRS:
        directory = root / directory_name
        if directory.is_dir():
            paths.extend(sorted(path for path in directory.rglob("*.md") if path.is_file()))
    return tuple(dict.fromkeys(paths))


def has_meaningful_legacy_surfaces(root: Path) -> bool:
    for path in iter_legacy_surface_paths(root):
        if path.name == LEGACY_DESTINATIONS_FILE:
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            return True
        if has_meaningful_legacy_text(text):
            return True
    return False


def legacy_destination_entries(text: str) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        match = ROUTE_LINE_RE.match(line)
        if not match or "status=" not in line.casefold():
            continue
        route_fields = {
            key.casefold(): value.strip()
            for key, value in ROUTE_FIELD_RE.findall(match.group(2))
        }
        entries.append(
            {
                "id": match.group(1).strip(),
                "fields": route_fields,
                "line": line_number,
            }
        )
    return entries


def validate_legacy_destinations(
    root: Path, destination_path: Path, warnings: list[str]
) -> None:
    text = read_text(destination_path)
    if "legacy destination schema" not in text.casefold():
        warnings.append(
            "legacy-destinations.md has no Legacy destination schema field"
        )
    entries = legacy_destination_entries(text)
    if not entries:
        warnings.append("legacy-destinations.md has no destination entries")
        return

    seen_ids: set[str] = set()
    non_archived_count = 0
    generic_destination_ids: list[str] = []
    owner_counts: dict[str, int] = defaultdict(int)
    for entry in entries:
        entry_id = str(entry["id"])
        fields_by_name = entry["fields"]
        assert isinstance(fields_by_name, dict)
        normalized_id = entry_id.casefold()
        if normalized_id in seen_ids:
            warnings.append(
                f"legacy-destinations.md entry '{entry_id}' is duplicated"
            )
        seen_ids.add(normalized_id)

        status = fields_by_name.get("status", "").casefold()
        if not status:
            warnings.append(
                f"legacy-destinations.md entry '{entry_id}' has no status"
            )
            continue
        if status != "archived-only":
            non_archived_count += 1
        if status not in LEGACY_DESTINATION_ALLOWED_STATUSES:
            warnings.append(
                f"legacy-destinations.md entry '{entry_id}' has invalid status: {status}"
            )
        for required in ("source", "scope", "reason"):
            if not fields_by_name.get(required, "").strip():
                warnings.append(
                    f"legacy-destinations.md entry '{entry_id}' has no {required}"
                )

        wake_terms = route_values(fields_by_name.get("aliases", "")) + route_values(
            fields_by_name.get("keywords", "")
        )
        owners = route_values(fields_by_name.get("owners", ""))
        probes = route_values(fields_by_name.get("probes", ""))
        source = fields_by_name.get("source", "").strip()
        scope = fields_by_name.get("scope", "").strip()
        reason = fields_by_name.get("reason", "").strip()

        if status != "archived-only" and not wake_terms:
            warnings.append(
                f"legacy-destinations.md entry '{entry_id}' has no aliases or keywords"
            )
        elif status != "archived-only" and not semantic_legacy_terms(wake_terms):
            generic_destination_ids.append(entry_id)
            warnings.append(
                f"legacy-destinations.md entry '{entry_id}' has only generic wake terms; classify the legacy item by semantic function, not by file role"
            )
        if (
            status != "archived-only"
            and LEGACY_FILE_ROLE_SCOPE_RE.match(scope)
            and (LEGACY_CAPSULE_SOURCE_RE.search(source) or not semantic_legacy_terms(wake_terms))
        ):
            warnings.append(
                f"legacy-destinations.md entry '{entry_id}' uses a file-role scope instead of a semantic legacy scope: {scope}"
            )
        if status != "archived-only" and reason.strip().casefold() in GENERIC_LEGACY_REASONS:
            warnings.append(
                f"legacy-destinations.md entry '{entry_id}' has a generic reason; explain the preserved requirement, guard, rejected path, owner, or archival reason"
            )
        if status in LEGACY_DESTINATION_OWNER_STATUSES and not owners:
            warnings.append(
                f"legacy-destinations.md entry '{entry_id}' has status={status} but no owners"
            )
        if status == "project-owner-indexed" and any(is_memory_layer_owner(pointer) for pointer in owners):
            warnings.append(
                f"legacy-destinations.md entry '{entry_id}' has status=project-owner-indexed but points to a memory-layer owner; use memory-owner/mandatory-guard/rejected-path or point to a real project owner"
            )
        if status in LEGACY_DESTINATION_PROBE_STATUSES and not probes:
            warnings.append(
                f"legacy-destinations.md entry '{entry_id}' has status={status} but no route probes"
            )
        if status == "pending-review" and not (
            owners or "[REVIEW:" in fields_by_name.get("source", "")
        ):
            warnings.append(
                f"legacy-destinations.md entry '{entry_id}' is pending-review but has no review owner/source"
            )
        if status == "pending-review":
            warnings.append(
                f"legacy-destinations.md entry '{entry_id}' is pending-review; pending-review is not takeover completion"
            )
        for pointer in owners:
            owner_counts[pointer.strip().replace("\\", "/")] += 1
            target = pointer_path(root, pointer)
            if not target.is_file():
                warnings.append(
                    f"legacy-destinations.md entry '{entry_id}' points to missing owner: {pointer}"
                )
    if non_archived_count >= 10 and generic_destination_ids:
        warnings.append(
            f"legacy-destinations.md has {len(generic_destination_ids)} generic non-archived destination entries; a takeover manifest must be a semantic inventory, not a file listing"
        )
    if non_archived_count >= 10:
        for pointer, count in sorted(owner_counts.items(), key=lambda item: (-item[1], item[0])):
            if count >= 10 and count / max(1, non_archived_count) >= 0.6:
                warnings.append(
                    f"legacy-destinations.md collapses {count} non-archived entries onto one owner ({pointer}); split by meaningful owner or mark cold evidence archived-only with reasons"
                )
                break


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
    live_names = {
        "status",
        "current step",
        "completed",
        "progress boundary",
        "next exact step",
        "route check",
    }
    for match in FIELD_RE.finditer(text):
        name = match.group(1).strip().casefold()
        if name in live_names:
            counts[name] += 1
    return sorted(name for name, count in counts.items() if count > 1)


def has_secret_like_text(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def checkpoint_fields_from_text(text: str) -> tuple[int, str] | None:
    length_match = CHECKPOINT_LENGTH_RE.search(text)
    hash_match = CHECKPOINT_HASH_RE.search(text)
    if not length_match or not hash_match:
        return None
    return int(length_match.group(1)), hash_match.group(1).upper()


def checkpoint_kind_from_text(text: str) -> str | None:
    match = CHECKPOINT_KIND_RE.search(text)
    return match.group(1) if match else None


def standalone_checkpoint_text(root: Path) -> str | None:
    """v0.2.13: checkpoint metadata lives in the standalone .takeover-checkpoint."""
    path = root / CHECKPOINT_FILE
    if not path.is_file():
        return None
    try:
        text = read_text(path)
    except UnicodeDecodeError:
        return ""
    return text


def prefix_hash_ok(data: bytes, fields: tuple[int, str]) -> bool:
    prefix_length, expected = fields
    if prefix_length > len(data):
        return False
    actual = hashlib.sha256(data[:prefix_length]).hexdigest().upper()
    return actual == expected


def checkpoint_is_valid(data: bytes, root: Path | None = None) -> bool:
    """Validate the current checkpoint against the session-log prefix.

    Prefers the standalone .takeover-checkpoint file (v0.2.13); falls back to a
    legacy in-log marker for un-migrated roots. The legacy prefix is always the
    session-log bytes [0:prefix_length], regardless of where the metadata lives.
    """
    if root is not None:
        standalone = standalone_checkpoint_text(root)
        if standalone is not None:
            if not standalone or CURRENT_CHECKPOINT_MARKER not in standalone:
                return False
            fields = checkpoint_fields_from_text(standalone)
            if fields is None:
                return False
            return prefix_hash_ok(data, fields)
    marker = CURRENT_CHECKPOINT_MARKER.encode("ascii")
    if data.count(marker) != 1:
        return False
    try:
        tail = data[data.index(marker) :].decode("utf-8")
    except UnicodeDecodeError:
        return False
    fields = checkpoint_fields_from_text(tail)
    if fields is None:
        return False
    return prefix_hash_ok(data, fields)


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
    session_data = session_log.read_bytes() if session_log.exists() else b""
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
            "session-log.md is long; run takeover-memory.py discharge for settled structured entries, then roll only as a safety bound; read the log through an exact unresolved route or targeted search/range, never as a default recovery payload"
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
        schemas = MEMORY_SCHEMA_RE.findall(index_text)
        schema_is_current = len(schemas) == 1 and (
            schemas[0].casefold() == MEMORY_SCHEMA_VERSION.casefold()
        )
        if not schemas:
            warnings.append(
                f"index.md has no Memory schema: {MEMORY_SCHEMA_VERSION} takeover marker"
            )
        elif len(schemas) != 1:
            warnings.append(
                f"index.md has {len(schemas)} Memory schema entries; exactly one required"
            )
        elif not schema_is_current:
            warnings.append(
                f"index.md has no Memory schema: {MEMORY_SCHEMA_VERSION} takeover marker"
            )

        # v0.2.13: prefer the standalone checkpoint file; fall back to an in-log
        # marker for un-migrated roots. A vestigial in-log marker left behind
        # after migration is ignored once the standalone file exists.
        standalone_text = standalone_checkpoint_text(root)
        in_log_count = session_data.count(CURRENT_CHECKPOINT_MARKER.encode("ascii"))
        if standalone_text is not None:
            if not standalone_text or CURRENT_CHECKPOINT_MARKER not in standalone_text:
                warnings.append(f"{CHECKPOINT_FILE} is present but has no valid checkpoint")
            elif not checkpoint_is_valid(session_data, root):
                warnings.append("session-log.md v0.2.7 checkpoint is invalid")
        else:
            if in_log_count == 0 and schema_is_current:
                warnings.append(
                    "index.md has current schema but no v0.2.7 checkpoint; takeover is incomplete"
                )
            elif in_log_count > 1:
                warnings.append(
                    f"session-log.md must contain exactly one v0.2.7 checkpoint; found {in_log_count}"
                )
            elif in_log_count == 1 and not checkpoint_is_valid(session_data, root):
                warnings.append("session-log.md v0.2.7 checkpoint is invalid")

        legacy_destinations = root / LEGACY_DESTINATIONS_FILE
        checkpoint_fields = None
        checkpoint_text = ""
        if standalone_text:
            checkpoint_text = standalone_text
            checkpoint_fields = checkpoint_fields_from_text(checkpoint_text)
        if checkpoint_fields is None:
            checkpoint_text = (
                session_text[session_text.find(CURRENT_CHECKPOINT_MARKER):]
                if CURRENT_CHECKPOINT_MARKER in session_text
                else ""
            )
            checkpoint_fields = checkpoint_fields_from_text(checkpoint_text)
        if checkpoint_fields is not None:
            legacy_prefix = session_text.encode("utf-8", "surrogatepass")[: checkpoint_fields[0]].decode("utf-8", "replace")
        else:
            legacy_prefix = legacy_prefix_text(session_text)
        legacy_destination_required = has_meaningful_legacy_history(legacy_prefix)
        if (
            not legacy_destination_required
            and checkpoint_kind_from_text(checkpoint_text) != "fresh-initialization"
        ):
            legacy_destination_required = has_meaningful_legacy_surfaces(root)
        if legacy_destination_required:
            if not legacy_destinations.is_file():
                warnings.append(
                    "legacy-destinations.md is required when takeover sees meaningful legacy history"
                )
            else:
                validate_legacy_destinations(root, legacy_destinations, warnings)
        elif legacy_destinations.exists():
            validate_legacy_destinations(root, legacy_destinations, warnings)

        ids = index_capsule_ids(index_text)
        if ids and not capsules_dir.exists():
            errors.append("index.md references capsules but capsules/ is missing")
        for cid in sorted(ids):
            if cid.lower() == "ids":
                continue
            if not (capsules_dir / f"{cid}.md").exists():
                warnings.append(f"index.md references missing capsule: capsules/{cid}.md")

        index_lower = index_text.lower()
        if "pressure signal index" in index_lower or "pressure=" in index_lower:
            if "status=" not in index_lower:
                warnings.append("Pressure signal entry has no status=active|historical|resolved entries")
            if "capsules=" not in index_lower and not session_log.exists():
                warnings.append("Pressure signal entry has no capsule link and no session-log.md evidence")

        if "module aliases" not in index_text.lower():
            warnings.append("index.md has no Module aliases section")

        top_routes = route_entries(index_text)
        routes = list(top_routes)
        history_routes: list[dict[str, object]] = []
        history_route_paths: set[Path] = set()
        routes_root = (root / "routes").resolve()
        for route in top_routes:
            if len(route["owners"]) > PRIMARY_OWNER_FANOUT_SOFT_COUNT:
                warnings.append(
                    f"index.md route '{route['scope']}' has broad primary owner fan-out; keep current owners here and move cold version/event routes under routes/"
                )
            for pointer in route["history"]:
                target = pointer_path(root, pointer)
                try:
                    target.relative_to(routes_root)
                except ValueError:
                    warnings.append(
                        f"index.md route '{route['scope']}' points outside routes/ for history: {pointer}"
                    )
                    continue
                if not target.is_file():
                    warnings.append(
                        f"index.md route '{route['scope']}' points to missing history route: {pointer}"
                    )
                    continue
                if target in history_route_paths:
                    continue
                history_route_paths.add(target)
                child_source = str(target.relative_to(root))
                child_entries = route_entries(read_text(target), child_source)
                for child in child_entries:
                    if child["history"]:
                        warnings.append(
                            f"{child_source} route '{child['scope']}' history route nesting exceeds one level"
                        )
                history_routes.extend(child_entries)
        routes.extend(history_routes)

        if routes_root.is_dir():
            for route_page in sorted(routes_root.rglob("*.md")):
                if route_page.resolve() not in history_route_paths:
                    warnings.append(
                        f"{route_page.relative_to(root)} history route page has no top-level pointer"
                    )

        routed_pointers = {
            pointer for route in routes for pointer in (*route["owners"], *route["mandatory"])
        }
        primary_owners = {
            pointer_path(root, pointer)
            for route in top_routes
            for pointer in route["owners"]
        }
        historical_owners = {
            pointer_path(root, pointer)
            for route in history_routes
            for pointer in route["owners"]
        }
        duplicated_tiers = sorted(primary_owners.intersection(historical_owners))
        for duplicated in duplicated_tiers:
            warnings.append(
                f"{duplicated} appears in both primary and history routes"
            )
        for route in routes:
            if not route["owners"]:
                warnings.append(
                    f"{route['source']} route '{route['scope']}' has owners= but no normative body owner"
                )
            for pointer in (*route["owners"], *route["mandatory"]):
                target = pointer_path(root, pointer)
                if not target.is_file():
                    warnings.append(
                        f"{route['source']} route '{route['scope']}' points to missing owner: {pointer}"
                    )
                    continue
                fragment = pointer_fragment(pointer)
                if fragment and fragment.casefold() not in read_text(target).casefold():
                    warnings.append(
                        f"{route['source']} route '{route['scope']}' owner fragment was not found: {pointer}"
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

    memory_files = [current, index, active_task, session_log, root / LEGACY_DESTINATIONS_FILE]
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
        and not (
            allow_missing_schema
            and (
                "has no Memory schema" in warning
                or "has current schema but no v0.2.7 checkpoint" in warning
                or "Memory schema entries; exactly one required" in warning
            )
        )
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

    errors, warnings = validate(args.root.expanduser().resolve())
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
