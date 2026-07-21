#!/usr/bin/env python3
"""Scan Lite Demo memory roots for bloat and default-recall injection risk."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


EXCLUDED_DIRS = {".lite-demo-cache", ".lite-demo-work", "__pycache__"}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".toml"}
FIELD_RE = re.compile(r"(^|;)\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*([^;]+)")
VALUE_SPLIT_RE = re.compile(r"\s*,\s*")


ROLE_LIMITS = {
    "current-context": 6000,
    "index": 16000,
    "active-task": 14000,
    "session-log-live": 12000,
    "route": 10000,
    "capsule": 50000,
    "legacy-log": 0,
    "other": 30000,
}

LIVE_LOG_LINE_LIMIT = 80
LONG_LINE_LIMIT = 1200
RISK_WORDS = ("session-log", "session log", "日志", "上下文", "history", "全量", "chronology")


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def role_for(rel_path: str) -> str:
    name = Path(rel_path).name
    if rel_path == "current-context.md":
        return "current-context"
    if rel_path == "index.md":
        return "index"
    if rel_path == "active-task.md" or rel_path.endswith("/active-task.md"):
        return "active-task"
    if rel_path == "session-log.md":
        return "session-log-live"
    if rel_path.startswith("legacy/session-log-"):
        return "legacy-log"
    if rel_path.startswith("routes/"):
        return "route"
    if rel_path.startswith("capsules/") or "/capsules/" in rel_path:
        return "capsule"
    if name in {"AGENTS.md", "CODEX_GUIDANCE.md"}:
        return "other"
    return "other"


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        parts = set(path.relative_to(root).parts)
        if parts.intersection(EXCLUDED_DIRS):
            continue
        if path.suffix.casefold() not in TEXT_SUFFIXES and path.name not in {
            "AGENTS.md",
            "CODEX_GUIDANCE.md",
        }:
            continue
        files.append(path)
    return files


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="replace")


def route_pointers(index_text: str) -> set[str]:
    pointers: set[str] = set()
    for line in index_text.splitlines():
        if "owners=" not in line and "mandatory=" not in line and "history=" not in line:
            continue
        fields = {m.group(2).casefold(): m.group(3).strip() for m in FIELD_RE.finditer(line)}
        for key in ("owners", "mandatory", "history"):
            for value in VALUE_SPLIT_RE.split(fields.get(key, "")):
                value = value.strip()
                if value and value.casefold() != "none":
                    pointers.add(value.split("#", 1)[0])
    return pointers


def file_record(root: Path, path: Path, routed: set[str]) -> dict[str, Any]:
    rel_path = rel(path, root)
    data = path.read_bytes()
    text = read_text(path)
    lines = text.splitlines()
    role = role_for(rel_path)
    limit = ROLE_LIMITS[role]
    long_lines = [idx for idx, line in enumerate(lines, 1) if len(line) > LONG_LINE_LIMIT]
    routed_here = rel_path in routed
    risk_terms = [
        word
        for word in RISK_WORDS
        if word.casefold() in rel_path.casefold() or word.casefold() in text.casefold()
    ]
    record = {
        "path": rel_path,
        "role": role,
        "bytes": len(data),
        "lines": len(lines),
        "routed": routed_here,
        "limit": limit,
        "over_limit": bool(limit and len(data) > limit),
        "long_line_count": len(long_lines),
        "first_long_lines": long_lines[:5],
        "risk_terms": risk_terms[:8],
    }
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("memory_root", type=Path, help="Path to docs/codex")
    parser.add_argument("--max-live-log-lines", type=int, default=LIVE_LOG_LINE_LIMIT)
    parser.add_argument("--max-report-files", type=int, default=20)
    args = parser.parse_args()

    root = args.memory_root.expanduser().resolve()
    if not root.is_dir():
        print(json.dumps({"ok": False, "error": f"memory root not found: {root}"}, ensure_ascii=False, indent=2))
        return 2

    index_text = read_text(root / "index.md") if (root / "index.md").is_file() else ""
    routed = route_pointers(index_text)
    records = [file_record(root, path, routed) for path in iter_files(root)]
    records.sort(key=lambda item: (-item["bytes"], item["path"]))

    high: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    for item in records:
        path = item["path"]
        role = item["role"]
        if role == "session-log-live" and item["lines"] > args.max_live_log_lines:
            high.append(
                {
                    "path": path,
                    "risk": "live-session-log-too-large",
                    "bytes": item["bytes"],
                    "lines": item["lines"],
                    "reason": "live session-log must be an unresolved queue, not a chronology",
                }
            )
        if role == "legacy-log" and item["routed"]:
            high.append(
                {
                    "path": path,
                    "risk": "legacy-log-routed-directly",
                    "bytes": item["bytes"],
                    "reason": "legacy log bytes should be cold evidence behind destinations, not a direct owner route",
                }
            )
        if role in {"current-context", "index", "active-task", "route"} and item["over_limit"]:
            high.append(
                {
                    "path": path,
                    "risk": f"{role}-oversized",
                    "bytes": item["bytes"],
                    "limit": item["limit"],
                    "reason": "always-read or routing files must stay compact",
                }
            )
        if item["long_line_count"]:
            warnings.append(
                {
                    "path": path,
                    "risk": "long-lines",
                    "count": item["long_line_count"],
                    "first": item["first_long_lines"],
                }
            )
        if item["over_limit"] and role in {"capsule", "other"}:
            warnings.append(
                {
                    "path": path,
                    "risk": f"{role}-large",
                    "bytes": item["bytes"],
                    "limit": item["limit"],
                    "routed": item["routed"],
                }
            )

    session_log_records = [
        item for item in records if item["role"] in {"session-log-live", "legacy-log"}
    ]
    routed_large = [
        item
        for item in records
        if item["routed"] and item["bytes"] > item["limit"] and item["limit"]
    ]
    result = {
        "ok": not high,
        "memory_root": str(root),
        "file_count": len(records),
        "total_bytes": sum(item["bytes"] for item in records),
        "largest_files": records[: args.max_report_files],
        "session_log_files": session_log_records,
        "routed_large_files": routed_large,
        "high_risks": high,
        "warnings": warnings[: args.max_report_files],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
