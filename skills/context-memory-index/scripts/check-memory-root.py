#!/usr/bin/env python3
"""Lightweight validator for a context-memory-index project root."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FIELD_RE = re.compile(r"^\s*-\s*([^:\n]+):\s*(.*)$", re.MULTILINE)
CAPSULE_ID_RE = re.compile(r"\b(C[0-9][0-9A-Za-z_-]*)\b")


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

    if active_task.exists() and is_active_task(active_text):
        if not has_field_value(active_text, ("next exact step",)):
            errors.append("active-task.md is active but has no Next exact step")
        if not has_field_value(active_text, ("mode",)):
            warnings.append("active-task.md has no Mode")
        if not has_field_value(active_text, ("activation packet",)):
            warnings.append("active-task.md has no Activation packet")

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

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Path to docs/codex or another context memory root")
    args = parser.parse_args()

    errors, warnings = validate(args.root)
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK: 0 error(s), {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
