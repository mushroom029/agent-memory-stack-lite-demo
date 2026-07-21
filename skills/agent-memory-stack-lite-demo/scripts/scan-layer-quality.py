#!/usr/bin/env python3
"""Inspect whether a Lite Demo memory root is using the five layers correctly."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


CACHE_REL = ".lite-demo-cache/v1/derived-index.json"
EXCLUDED_DIRS = {".lite-demo-cache", ".lite-demo-work", "__pycache__"}
FIELD_RE = re.compile(r"(?:^|;)\s*([a-z][a-z0-9_-]*)\s*=\s*([^;]*)", re.I)
ROUTE_RE = re.compile(r"^\s*-\s*([^:]+):\s*(.+)$")
MEMORY_ID_RE = re.compile(r"(?im)^\s*-\s*Memory ID:\s*(.+?)\s*$")
HEADING_RE = re.compile(r"(?m)^(#{1,6})\s+(.+?)\s*$")
IN_FLIGHT_HEADING_RE = re.compile(
    r"^\s*\[(REVIEW|UNRESOLVED|CORRECTION|ROLLBACK|CONFLICT|CHECKPOINT):[A-Za-z0-9._-]+\]",
    re.I,
)

ANCHOR_LIMITS = {
    "current-context.md": 6000,
    "active-task.md": 14000,
}
ROUTE_LINE_LIMIT = 1200
SESSION_LOG_LINE_LIMIT = 80
SESSION_LOG_BYTE_LIMIT = 12000
NARRATIVE_DUPLICATION_CHARS = 120

LIVE_FIELD_NAMES = {
    "status",
    "current step",
    "progress boundary",
    "next exact step",
    "route check",
}
CHRONOLOGY_HEADINGS = re.compile(r"(?im)^##\s+(batch|timeline|history|run audit|round|轮次)\b")
ROUTINE_LOG_WORDS = re.compile(r"(?i)\b(round|batch|green|completed normally|routine)\b|常规|完成了|流水账|逐轮")
BODY_FIELD_NAMES = {"body", "text", "content", "narrative", "summary"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def split_values(value: str) -> list[str]:
    return [
        item.strip().strip("`\"'")
        for item in re.split(r"\s*[,|，]\s*", value)
        if item.strip().strip("`\"'")
    ]


def pointer_path(root: Path, pointer: str) -> Path:
    return (root / pointer.split("#", 1)[0]).resolve()


def route_entries(text: str, source: str) -> list[dict[str, Any]]:
    routes: list[dict[str, Any]] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        match = ROUTE_RE.match(line)
        if not match or "owners=" not in line.casefold():
            continue
        fields = {key.casefold(): value.strip() for key, value in FIELD_RE.findall(match.group(2))}
        routes.append(
            {
                "source": source,
                "line": line_no,
                "scope": match.group(1).strip(),
                "owners": split_values(fields.get("owners", "")),
                "mandatory": split_values(fields.get("mandatory", "")),
                "history": split_values(fields.get("history", "")),
                "status": fields.get("status", "").strip(),
                "raw": line,
            }
        )
    return routes


def iter_memory_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if set(path.relative_to(root).parts).intersection(EXCLUDED_DIRS):
            continue
        if path.suffix.casefold() not in {".md", ".txt"} and path.name not in {"AGENTS.md", "CODEX_GUIDANCE.md"}:
            continue
        files.append(path)
    return files


def narrative_units(text: str) -> set[str]:
    units: set[str] = set()
    for line in text.splitlines():
        candidate = re.sub(r"^\s*(?:[-*#]+|\d+\.)\s*", "", line).strip()
        candidate = re.sub(r"\s+", " ", candidate)
        if len(candidate) >= NARRATIVE_DUPLICATION_CHARS:
            units.add(candidate.casefold())
    return units


def add(layer: dict[str, Any], severity: str, message: str) -> None:
    layer[severity].append(message)


def inspect_anchor(root: Path) -> dict[str, Any]:
    layer = {"ok": True, "failures": [], "warnings": [], "files": []}
    current = root / "current-context.md"
    if not current.is_file():
        add(layer, "failures", "missing current-context.md")
    anchors = [current] if current.is_file() else []
    active = root / "active-task.md"
    if active.is_file():
        anchors.append(active)
    tasks = root / "tasks"
    if tasks.is_dir():
        anchors.extend(sorted(tasks.glob("*/active-task.md")))
    for path in anchors:
        text = read_text(path)
        relative = rel(path, root)
        limit = ANCHOR_LIMITS.get(path.name, ANCHOR_LIMITS.get(relative, 14000))
        layer["files"].append({"path": relative, "bytes": path.stat().st_size, "lines": len(text.splitlines())})
        if path.stat().st_size > limit:
            add(layer, "failures", f"{relative} exceeds compact anchor limit {limit}")
        if CHRONOLOGY_HEADINGS.search(text):
            add(layer, "failures", f"{relative} contains chronology-style sections")
        if path.name == "active-task.md":
            fields = defaultdict(int)
            for match in re.finditer(r"(?im)^\s*-\s*([^:：]{2,40})[:：]", text):
                name = match.group(1).strip().casefold()
                if name in LIVE_FIELD_NAMES:
                    fields[name] += 1
            repeated = sorted(name for name, count in fields.items() if count > 1)
            if repeated:
                add(layer, "failures", f"{relative} repeats live route fields: {', '.join(repeated)}")
            if "next exact step" not in text.casefold():
                add(layer, "warnings", f"{relative} has no Next exact step")
    layer["ok"] = not layer["failures"]
    return layer


def inspect_routes(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    layer = {"ok": True, "failures": [], "warnings": [], "route_count": 0}
    index = root / "index.md"
    routes: list[dict[str, Any]] = []
    if not index.is_file():
        add(layer, "failures", "missing index.md")
    else:
        index_text = read_text(index)
        routes.extend(route_entries(index_text, "index.md"))
        if len(index_text) > 16000:
            add(layer, "failures", "index.md is too large for a compact route layer")
        for line_no, line in enumerate(index_text.splitlines(), 1):
            if len(line) > ROUTE_LINE_LIMIT:
                add(layer, "failures", f"index.md:{line_no} route line is too long")
    routes_dir = root / "routes"
    if routes_dir.is_dir():
        for route_file in sorted(routes_dir.glob("*.md")):
            routes.extend(route_entries(read_text(route_file), rel(route_file, root)))
    layer["route_count"] = len(routes)
    if not routes:
        add(layer, "failures", "no owner routes found")
    for route in routes:
        if not route["owners"]:
            add(layer, "failures", f"{route['source']}:{route['line']} has owners= but no owner")
        for pointer in [*route["owners"], *route["mandatory"]]:
            if pointer.casefold() in {"none", "n/a", "-"}:
                continue
            clean = pointer.split("#", 1)[0].replace("\\", "/")
            if clean.startswith("legacy/session-log-"):
                add(layer, "failures", f"{route['source']}:{route['line']} directly routes legacy session-log bytes")
            if clean == "session-log.md" and route.get("status", "").casefold() != "pending-review":
                add(layer, "failures", f"{route['source']}:{route['line']} routes live session-log outside pending-review")
            target = pointer_path(root, pointer)
            if not target.is_file():
                add(layer, "failures", f"{route['source']}:{route['line']} points to missing owner {pointer}")
    layer["ok"] = not layer["failures"]
    return layer, routes


def inspect_owners(root: Path, routes: list[dict[str, Any]]) -> dict[str, Any]:
    layer = {"ok": True, "failures": [], "warnings": [], "owner_files": []}
    routed_paths = {
        pointer_path(root, pointer)
        for route in routes
        for pointer in [*route["owners"], *route["mandatory"]]
        if pointer and pointer.casefold() not in {"none", "n/a", "-"}
    }
    capsule_dir = root / "capsules"
    if capsule_dir.is_dir():
        for capsule in sorted(capsule_dir.glob("*.md")):
            layer["owner_files"].append(rel(capsule, root))
            if capsule.resolve() not in routed_paths:
                add(layer, "failures", f"{rel(capsule, root)} has no wake-up route")
    ids: dict[str, list[str]] = defaultdict(list)
    units: dict[str, set[str]] = {}
    for path in iter_memory_files(root):
        relative = rel(path, root)
        text = read_text(path)
        units[relative] = narrative_units(text)
        for memory_id in MEMORY_ID_RE.findall(text):
            ids[memory_id.casefold()].append(relative)
    for memory_id, owners in sorted(ids.items()):
        unique = sorted(set(owners))
        if len(unique) > 1:
            add(layer, "failures", f"Memory ID {memory_id} appears in multiple owners: {', '.join(unique)}")
    duplicate_pairs: list[str] = []
    items = list(units.items())
    for idx, (path_a, units_a) in enumerate(items):
        for path_b, units_b in items[idx + 1 :]:
            if units_a.intersection(units_b):
                duplicate_pairs.append(f"{path_a} <-> {path_b}")
    if duplicate_pairs:
        add(layer, "failures", "long narrative duplicated across layers: " + "; ".join(duplicate_pairs[:5]))
    layer["ok"] = not layer["failures"]
    return layer


def inspect_session_log(root: Path) -> dict[str, Any]:
    layer = {"ok": True, "failures": [], "warnings": [], "files": []}
    log = root / "session-log.md"
    if not log.is_file():
        add(layer, "failures", "missing session-log.md")
        layer["ok"] = False
        return layer
    text = read_text(log)
    lines = text.splitlines()
    layer["files"].append({"path": "session-log.md", "bytes": log.stat().st_size, "lines": len(lines)})
    if len(lines) > SESSION_LOG_LINE_LIMIT or log.stat().st_size > SESSION_LOG_BYTE_LIMIT:
        add(layer, "failures", "session-log.md is too large for a sparse in-flight layer")
    for heading in HEADING_RE.findall(text):
        level, title = heading
        if level == "#" and title.strip().casefold() in {"session log", "session-log"}:
            continue
        if level == "##" and IN_FLIGHT_HEADING_RE.match(title.strip()):
            continue
        add(layer, "warnings", f"session-log heading is not a structured in-flight entry: {title.strip()}")
    if ROUTINE_LOG_WORDS.search(text) and len(lines) > 12:
        add(layer, "failures", "session-log.md appears to contain routine chronology")
    layer["ok"] = not layer["failures"]
    return layer


def inspect_derived(root: Path, require_cache: bool) -> dict[str, Any]:
    layer = {"ok": True, "failures": [], "warnings": [], "record_count": 0}
    cache_path = root / CACHE_REL
    if not cache_path.is_file():
        if require_cache:
            add(layer, "failures", "derived cache is missing")
        else:
            add(layer, "warnings", "derived cache is missing")
        layer["ok"] = not layer["failures"]
        return layer
    try:
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add(layer, "failures", f"derived cache is invalid JSON: {exc}")
        layer["ok"] = False
        return layer
    if cache.get("schema") != "lite-demo-derived-index-v1":
        add(layer, "failures", "derived cache schema mismatch")
    records = cache.get("records", [])
    layer["record_count"] = len(records)
    for record in records:
        body_keys = sorted(BODY_FIELD_NAMES.intersection(record.keys()))
        if body_keys:
            add(layer, "failures", f"{record.get('record_id')} stores body-like keys: {', '.join(body_keys)}")
        source = str(record.get("source_path", "")).replace("\\", "/")
        channel = str(record.get("channel", ""))
        if source == "session-log.md" and channel != "in-flight":
            add(layer, "failures", f"{record.get('record_id')} indexes live session-log as {channel}")
        if source.startswith("legacy/session-log-"):
            add(layer, "failures", f"{record.get('record_id')} indexes legacy session-log body")
    layer["ok"] = not layer["failures"]
    return layer


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("memory_root", type=Path, help="Path to docs/codex")
    parser.add_argument("--require-derived-cache", action="store_true")
    args = parser.parse_args()

    root = args.memory_root.resolve()
    if not root.is_dir():
        print(json.dumps({"ok": False, "error": f"memory root not found: {root}"}, ensure_ascii=False, indent=2))
        return 2

    anchor = inspect_anchor(root)
    route, routes = inspect_routes(root)
    owner = inspect_owners(root, routes)
    session_log = inspect_session_log(root)
    derived = inspect_derived(root, args.require_derived_cache)
    layers = {
        "anchor": anchor,
        "route": route,
        "owner": owner,
        "session_log": session_log,
        "derived_retrieval": derived,
    }
    failures = [
        {"layer": name, "message": message}
        for name, layer in layers.items()
        for message in layer["failures"]
    ]
    result = {
        "ok": not failures,
        "memory_root": str(root),
        "layers": layers,
        "failures": failures,
        "warnings": [
            {"layer": name, "message": message}
            for name, layer in layers.items()
            for message in layer["warnings"]
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
