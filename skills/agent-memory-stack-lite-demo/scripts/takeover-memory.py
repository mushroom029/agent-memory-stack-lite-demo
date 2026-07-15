#!/usr/bin/env python3
"""Initialize, inspect, checkpoint, and verify Lite Demo v0.2.7 memory."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


MARKER = "<!-- LITE-DEMO-V0.2.7-CHECKPOINT -->"
PREVIOUS_MARKER = "<!-- LITE-DEMO-V0.2.6-TAKEOVER -->"
SCHEMA_VERSION = "v0.2.7"
SCHEMA_RE = re.compile(
    r"^[ \t]*-[ \t]*Memory schema:[ \t]*(\S+)[ \t]*\r?$", re.I | re.MULTILINE
)
LENGTH_RE = re.compile(r"^- Legacy prefix bytes:\s*(\d+)\s*$", re.MULTILINE)
HASH_RE = re.compile(r"^- Legacy prefix SHA256:\s*([0-9A-Fa-f]{64})\s*$", re.MULTILINE)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def memory_schemas(index_path: Path) -> tuple[str, ...]:
    if not index_path.is_file():
        return ()
    return tuple(SCHEMA_RE.findall(index_path.read_text(encoding="utf-8")))


def write_memory_schema(index_path: Path, expected_sha256: str | None = None) -> bool:
    if not index_path.is_file():
        raise ValueError("index.md is required before takeover completion")
    data = index_path.read_bytes()
    require_expected_hash("index.md", sha256(data), expected_sha256)
    text = data.decode("utf-8")
    schema_line = f"- Memory schema: {SCHEMA_VERSION}"
    matches = list(SCHEMA_RE.finditer(text))
    if (
        len(matches) == 1
        and matches[0].group(1).casefold() == SCHEMA_VERSION.casefold()
    ):
        return False
    if matches:
        kept_schema = False
        updated_lines: list[str] = []
        for line in text.splitlines(keepends=True):
            bare = line.rstrip("\r\n")
            if SCHEMA_RE.fullmatch(bare):
                if kept_schema:
                    continue
                ending = line[len(bare) :]
                updated_lines.append(schema_line + ending)
                kept_schema = True
            else:
                updated_lines.append(line)
        updated = "".join(updated_lines)
    else:
        newline = "\r\n" if "\r\n" in text else "\n"
        lines = text.splitlines(keepends=True)
        insert_at = 1 if lines else 0
        if len(lines) > 1 and not lines[1].strip():
            insert_at = 2
        if insert_at and not lines[insert_at - 1].endswith(("\n", "\r")):
            lines[insert_at - 1] += newline
        lines.insert(insert_at, schema_line + newline)
        updated = "".join(lines)
    if updated == text:
        return False
    index_path.write_bytes(updated.encode("utf-8"))
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
    checkpoint_kind: str = "legacy-takeover",
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
        "## Lite Demo v0.2.7 Memory Checkpoint\n\n"
        f"- Checkpoint kind: {checkpoint_kind}\n"
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
    schemas = memory_schemas(index_path)
    schema = schemas[0] if len(schemas) == 1 else ""
    index_data = index_path.read_bytes() if index_path.is_file() else b""
    result: dict[str, object] = {
        "memory_schema": schema or None,
        "memory_schema_values": list(schemas),
        "schema_count": len(schemas),
        "schema_verified": len(schemas) == 1
        and schema.casefold() == SCHEMA_VERSION.casefold(),
        "index_present": index_path.is_file(),
        "index_sha256": sha256(index_data) if index_path.is_file() else None,
        "session_log_present": log_path.is_file(),
    }
    if log_path.is_file():
        log_data = log_path.read_bytes()
        result.update(verification(log_data))
        result["session_log_sha256"] = sha256(log_data)
        result["previous_checkpoint_count"] = log_data.count(
            PREVIOUS_MARKER.encode("ascii")
        )
    else:
        result.update(
            {
                "checkpoint_present": False,
                "checkpoint_required": True,
                "verified": False,
                "current_bytes": 0,
                "session_log_sha256": None,
                "previous_checkpoint_count": 0,
            }
        )
    result["checkpoint_required"] = True
    current_checkpoint_verified = bool(result["verified"])
    result["current_checkpoint_verified"] = current_checkpoint_verified
    result["completion_verified"] = bool(
        result["schema_verified"] and current_checkpoint_verified
    )
    result["verified"] = result["completion_verified"]
    reasons: list[str] = []
    if len(schemas) != 1:
        reasons.append("schema-count-invalid")
    if not result["schema_verified"]:
        reasons.append("schema-not-current")
    if not result["checkpoint_present"]:
        reasons.append("current-checkpoint-missing")
    elif not current_checkpoint_verified:
        reasons.append("current-checkpoint-invalid")
    result["incomplete_reasons"] = reasons
    result["takeover_required"] = not result["completion_verified"]
    return result


def require_expected_hash(label: str, actual: str | None, expected: str | None) -> None:
    if expected and (actual or "").casefold() != expected.casefold():
        raise ValueError(f"{label} changed after takeover preflight")


def starter_current_context(project_name: str, memory_landing_policy: str) -> str:
    today = datetime.now(timezone.utc).date().isoformat()
    return f"""# Current Context

- Updated: {today}
- Project: {project_name}
- Project phase: new
- Memory landing policy: {memory_landing_policy}
- Lite demo activation phrase: 启用外挂记忆
- Natural start phrase: 启动外挂记忆
- Explicit safe phrase: 本会话启用外挂记忆
- Legacy compatibility phrase: 启动lite demo
- Active goal: Not set yet.
- Active task pointer: none.
- Selected owner routes: none; derive the touched scope before opening owners.
- Stable/protected behavior: Not set yet; record only when relevant.
- Memory hygiene: one-off requests, pressure, failures, and short replies stay task-local or revisable unless the user uses explicit absolute wording.
- Next step: Ask for the real task and create a task anchor before complex execution.
"""


def starter_index(project_name: str, memory_landing_policy: str) -> str:
    today = datetime.now(timezone.utc).date().isoformat()
    return f"""# Context Index

- Updated: {today}
- Project: {project_name}
- Current anchor: docs/codex/current-context.md
- Memory landing policy: {memory_landing_policy}
- Task branches: none yet
- Active topic: new project

## Module Aliases

- task: goal, next step, resume
- branch: unfinished task, current idea, separate record
- route: failure, rejected path, correction
- recovery: session log, recent probe, evidence search, active task
- owner: body owner, wake-up route, mandatory guard
- boundary: stable behavior, do not touch, pressure

## Module Index

- Notes: Add a compact `scope/aliases/keywords -> owners + mandatory + history + reason` route when the first durable body is saved.
"""


def initialize_memory_root(
    memory_root: Path, project_name: str | None, memory_landing_policy: str
) -> dict[str, object]:
    if memory_root.exists():
        raise ValueError("initialize requires a memory root that does not exist")
    parent = memory_root.parent
    parent.mkdir(parents=True, exist_ok=True)
    resolved_project_name = project_name or memory_root.parent.parent.name or "project"
    temporary = Path(tempfile.mkdtemp(prefix=".lite-demo-init-", dir=parent))
    try:
        (temporary / "capsules").mkdir()
        (temporary / "tasks").mkdir()
        (temporary / "current-context.md").write_text(
            starter_current_context(resolved_project_name, memory_landing_policy),
            encoding="utf-8",
        )
        index_path = temporary / "index.md"
        index_path.write_text(
            starter_index(resolved_project_name, memory_landing_policy), encoding="utf-8"
        )
        require_strict_routes(temporary)
        log_path = temporary / "session-log.md"
        log_path.write_bytes(b"# Session Log\n")
        append_checkpoint(
            log_path, log_path.read_bytes(), checkpoint_kind="fresh-initialization"
        )
        write_memory_schema(index_path)
        result = root_verification(temporary)
        if result["takeover_required"]:
            raise ValueError("fresh memory initialization did not produce completion proof")
        temporary.replace(memory_root)
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise
    result = root_verification(memory_root)
    result["changed"] = True
    result["action"] = "initialized"
    return result


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
    parser.add_argument("command", choices=("initialize", "inspect", "apply", "verify"))
    parser.add_argument("memory_root", type=Path, help="Path to docs/codex")
    parser.add_argument("--expected-index-sha256")
    parser.add_argument("--expected-log-sha256")
    parser.add_argument("--legacy-prefix-bytes", type=int)
    parser.add_argument("--legacy-prefix-sha256")
    parser.add_argument(
        "--expect-no-log",
        action="store_true",
        help="Fail if session-log.md appears after a no-log preflight",
    )
    parser.add_argument("--project-name")
    parser.add_argument(
        "--memory-landing-policy",
        choices=("ask-by-default", "preauthorized"),
        default="ask-by-default",
    )
    parser.add_argument(
        "--routes-verified",
        action="store_true",
        help="Confirm strict routing validation passed before writing completion markers",
    )
    args = parser.parse_args()

    memory_root = args.memory_root.expanduser().resolve()
    if args.command != "initialize" and not memory_root.is_dir():
        parser.error(f"memory root does not exist: {memory_root}")
    index_path = memory_root / "index.md"
    log_path = memory_root / "session-log.md"

    try:
        if args.command == "initialize":
            result = initialize_memory_root(
                memory_root, args.project_name, args.memory_landing_policy
            )
        elif args.command == "apply":
            if (args.legacy_prefix_bytes is None) != (args.legacy_prefix_sha256 is None):
                raise ValueError(
                    "--legacy-prefix-bytes and --legacy-prefix-sha256 must be used together"
                )
            before = root_verification(memory_root)
            if not args.routes_verified:
                raise ValueError("apply requires --routes-verified")
            if not before["index_present"]:
                raise ValueError("index.md is required before takeover completion")
            if args.expect_no_log and args.expected_log_sha256:
                raise ValueError("use either --expect-no-log or --expected-log-sha256")
            if args.expect_no_log and args.legacy_prefix_bytes is not None:
                raise ValueError("--expect-no-log cannot use legacy prefix arguments")
            if before["takeover_required"]:
                if not args.expected_index_sha256:
                    raise ValueError("incomplete takeover requires --expected-index-sha256")
                if before["session_log_present"]:
                    if not args.expected_log_sha256:
                        raise ValueError(
                            "existing session log requires --expected-log-sha256"
                        )
                    if args.legacy_prefix_bytes is None:
                        raise ValueError(
                            "existing session log requires its initial legacy prefix identity"
                        )
                elif not args.expect_no_log:
                    raise ValueError("no-log preflight requires --expect-no-log")
            require_strict_routes(memory_root)
            current = root_verification(memory_root)
            if not before["takeover_required"] and current["takeover_required"]:
                raise ValueError("memory completion state changed after takeover preflight")
            require_expected_hash(
                "index.md", current.get("index_sha256"), args.expected_index_sha256
            )
            require_expected_hash(
                "session-log.md",
                current.get("session_log_sha256"),
                args.expected_log_sha256,
            )
            if args.expect_no_log and current["session_log_present"]:
                raise ValueError("session-log.md appeared after a no-log preflight")
            if not log_path.is_file():
                try:
                    with log_path.open("xb") as stream:
                        stream.write(b"# Session Log\n")
                except FileExistsError as exc:
                    raise ValueError(
                        "session-log.md appeared after a no-log preflight"
                    ) from exc
            log_data = log_path.read_bytes()
            if args.expect_no_log and log_data != b"# Session Log\n":
                raise ValueError("session-log.md changed during no-log initialization")
            require_expected_hash(
                "session-log.md", sha256(log_data), args.expected_log_sha256
            )
            checkpoint = append_checkpoint(
                log_path,
                log_data,
                args.legacy_prefix_bytes,
                args.legacy_prefix_sha256,
                checkpoint_kind="legacy-takeover",
            )
            schema_changed = write_memory_schema(index_path, args.expected_index_sha256)
            result = root_verification(memory_root)
            result["changed"] = checkpoint["changed"] or schema_changed
            result["action"] = checkpoint["action"]
        else:
            result = root_verification(memory_root)
            result["action"] = args.command
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(json.dumps({"action": args.command, "verified": False, "error": str(exc)}, indent=2))
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.command == "verify" and result["takeover_required"]:
        return 1
    if args.command == "apply" and result["takeover_required"]:
        return 1
    if args.command == "initialize" and result["takeover_required"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
