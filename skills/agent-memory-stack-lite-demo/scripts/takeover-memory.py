#!/usr/bin/env python3
"""Inspect, checkpoint, and verify a non-destructive Lite Demo v0.2.6 takeover."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


MARKER = "<!-- LITE-DEMO-V0.2.6-TAKEOVER -->"
SCHEMA_VERSION = "v0.2.6"
SCHEMA_RE = re.compile(
    r"^[ \t]*-[ \t]*Memory schema:[ \t]*(\S+)[ \t]*$", re.I | re.MULTILINE
)
LENGTH_RE = re.compile(r"^- Legacy prefix bytes:\s*(\d+)\s*$", re.MULTILINE)
HASH_RE = re.compile(r"^- Legacy prefix SHA256:\s*([0-9A-Fa-f]{64})\s*$", re.MULTILINE)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def memory_schema(index_path: Path) -> str:
    if not index_path.is_file():
        return ""
    match = SCHEMA_RE.search(index_path.read_text(encoding="utf-8"))
    return match.group(1) if match else ""


def write_memory_schema(index_path: Path) -> bool:
    if not index_path.is_file():
        raise ValueError("index.md is required before takeover completion")
    text = index_path.read_text(encoding="utf-8")
    schema_line = f"- Memory schema: {SCHEMA_VERSION}"
    match = SCHEMA_RE.search(text)
    if match and match.group(1).casefold() == SCHEMA_VERSION.casefold():
        return False
    if match:
        updated = SCHEMA_RE.sub(schema_line, text, count=1)
    else:
        lines = text.splitlines()
        insert_at = 1 if lines else 0
        if len(lines) > 1 and not lines[1].strip():
            insert_at = 2
        lines.insert(insert_at, schema_line)
        updated = "\n".join(lines) + ("\n" if text.endswith(("\n", "\r")) else "")
    if updated == text:
        return False
    index_path.write_text(updated, encoding="utf-8")
    return True


def checkpoint_fields(data: bytes) -> tuple[int, str] | None:
    marker = MARKER.encode("ascii")
    count = data.count(marker)
    if count == 0:
        return None
    if count != 1:
        raise ValueError(f"expected one takeover checkpoint, found {count}")
    tail = data[data.index(marker) :].decode("utf-8")
    length_match = LENGTH_RE.search(tail)
    hash_match = HASH_RE.search(tail)
    if not length_match or not hash_match:
        raise ValueError("takeover checkpoint is missing prefix length or SHA256")
    return int(length_match.group(1)), hash_match.group(1).upper()


def verification(data: bytes) -> dict[str, object]:
    fields = checkpoint_fields(data)
    if fields is None:
        return {
            "checkpoint_present": False,
            "verified": False,
            "current_bytes": len(data),
            "current_sha256": sha256(data),
        }
    prefix_length, expected_hash = fields
    if prefix_length > len(data):
        actual_hash = ""
        verified = False
    else:
        actual_hash = sha256(data[:prefix_length])
        verified = actual_hash == expected_hash
    return {
        "checkpoint_present": True,
        "verified": verified,
        "legacy_prefix_bytes": prefix_length,
        "legacy_prefix_sha256": expected_hash,
        "actual_prefix_sha256": actual_hash,
        "current_bytes": len(data),
        "checkpoint_count": data.count(MARKER.encode("ascii")),
    }


def append_checkpoint(
    log_path: Path,
    data: bytes,
    legacy_prefix_bytes: int | None = None,
    legacy_prefix_sha256: str | None = None,
) -> dict[str, object]:
    existing = verification(data)
    if existing["checkpoint_present"]:
        existing["changed"] = False
        existing["action"] = "already-taken-over"
        return existing

    prefix_length = legacy_prefix_bytes if legacy_prefix_bytes is not None else len(data)
    prefix_hash = (legacy_prefix_sha256 or sha256(data)).upper()
    if prefix_length < 0 or prefix_length > len(data):
        raise ValueError("legacy prefix length is outside the current session log")
    if sha256(data[:prefix_length]) != prefix_hash:
        raise ValueError("legacy session-log prefix changed during takeover")
    separator = b"" if data.endswith(b"\n\n") else (b"\n" if data.endswith(b"\n") else b"\n\n")
    checkpoint = (
        f"{MARKER}\n"
        "## Lite Demo v0.2.6 Legacy Takeover Checkpoint\n\n"
        f"- Recorded UTC: {datetime.now(timezone.utc).isoformat()}\n"
        f"- Legacy prefix bytes: {prefix_length}\n"
        f"- Legacy prefix SHA256: {prefix_hash}\n"
        "- Owner router: index.md\n"
        "- Rule: preserve the legacy prefix; repair owner routes without rewriting old evidence.\n"
    ).encode("utf-8")
    with log_path.open("ab") as stream:
        stream.write(separator)
        stream.write(checkpoint)

    result = verification(log_path.read_bytes())
    result["changed"] = True
    result["action"] = "checkpoint-appended"
    return result


def root_verification(memory_root: Path) -> dict[str, object]:
    index_path = memory_root / "index.md"
    log_path = memory_root / "session-log.md"
    schema = memory_schema(index_path)
    index_data = index_path.read_bytes() if index_path.is_file() else b""
    result: dict[str, object] = {
        "memory_schema": schema or None,
        "schema_verified": schema.casefold() == SCHEMA_VERSION.casefold(),
        "index_present": index_path.is_file(),
        "index_sha256": sha256(index_data) if index_data else None,
        "session_log_present": log_path.is_file(),
    }
    if log_path.is_file():
        log_data = log_path.read_bytes()
        result.update(verification(log_data))
        result["session_log_sha256"] = sha256(log_data)
    else:
        result.update(
            {
                "checkpoint_present": False,
                "checkpoint_required": False,
                "verified": schema.casefold() == SCHEMA_VERSION.casefold(),
                "current_bytes": 0,
                "session_log_sha256": None,
            }
        )
    result["checkpoint_required"] = log_path.is_file()
    result["takeover_required"] = not result["schema_verified"] or (
        log_path.is_file() and not result["verified"]
    )
    return result


def require_expected_hash(label: str, actual: str | None, expected: str | None) -> None:
    if expected and (actual or "").casefold() != expected.casefold():
        raise ValueError(f"{label} changed after takeover preflight")


def require_strict_routes(memory_root: Path) -> None:
    checker = Path(__file__).with_name("check-memory-root.py")
    completed = subprocess.run(
        [
            sys.executable,
            str(checker),
            str(memory_root),
            "--strict-routing",
            "--allow-missing-schema",
        ],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        detail = (completed.stdout or completed.stderr).strip().splitlines()
        summary = detail[-1] if detail else "unknown strict-routing failure"
        raise ValueError(f"strict routing validation failed: {summary}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("inspect", "apply", "verify"))
    parser.add_argument("memory_root", type=Path, help="Path to docs/codex")
    parser.add_argument("--expected-index-sha256")
    parser.add_argument("--expected-log-sha256")
    parser.add_argument("--legacy-prefix-bytes", type=int)
    parser.add_argument("--legacy-prefix-sha256")
    parser.add_argument(
        "--routes-verified",
        action="store_true",
        help="Confirm strict routing validation passed before writing completion markers",
    )
    args = parser.parse_args()

    memory_root = args.memory_root.resolve()
    if not memory_root.is_dir():
        parser.error(f"memory root does not exist: {memory_root}")
    index_path = memory_root / "index.md"
    log_path = memory_root / "session-log.md"

    try:
        if args.command == "apply":
            if (args.legacy_prefix_bytes is None) != (args.legacy_prefix_sha256 is None):
                raise ValueError(
                    "--legacy-prefix-bytes and --legacy-prefix-sha256 must be used together"
                )
            before = root_verification(memory_root)
            if not args.routes_verified:
                raise ValueError("apply requires --routes-verified")
            if not before["index_present"]:
                raise ValueError("index.md is required before takeover completion")
            require_strict_routes(memory_root)
            require_expected_hash(
                "index.md", before.get("index_sha256"), args.expected_index_sha256
            )
            require_expected_hash(
                "session-log.md",
                before.get("session_log_sha256"),
                args.expected_log_sha256,
            )
            if not log_path.is_file():
                log_path.write_bytes(b"# Session Log\n")
            checkpoint = append_checkpoint(
                log_path,
                log_path.read_bytes(),
                args.legacy_prefix_bytes,
                args.legacy_prefix_sha256,
            )
            schema_changed = write_memory_schema(index_path)
            result = root_verification(memory_root)
            result["changed"] = checkpoint["changed"] or schema_changed
            result["action"] = checkpoint["action"]
        else:
            result = root_verification(memory_root)
            result["action"] = args.command
    except (UnicodeDecodeError, ValueError) as exc:
        print(json.dumps({"action": args.command, "verified": False, "error": str(exc)}, indent=2))
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.command == "verify" and result["takeover_required"]:
        return 1
    if args.command == "apply" and result["takeover_required"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
