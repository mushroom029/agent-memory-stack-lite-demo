#!/usr/bin/env python3
"""Initialize, inspect, checkpoint, and verify Lite Demo v0.2.7 memory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


MARKER = "<!-- LITE-DEMO-V0.2.7-CHECKPOINT -->"
PREVIOUS_MARKER = "<!-- LITE-DEMO-V0.2.6-TAKEOVER -->"
SCHEMA_VERSION = "v0.2.7"
LEGACY_DESTINATIONS_FILE = "legacy-destinations.md"
# v0.2.13: the takeover checkpoint lives in its own file so session-log.md can
# later become a bounded ring without invalidating the legacy-prefix proof.
# The checkpoint block (MARKER + fields) is IDENTICAL in shape whether it sits
# in this standalone file or, for pre-v0.2.13 roots, still appended inside
# session-log.md. Readers prefer the standalone file and fall back to the
# in-log marker, so every existing v0.2.7 root keeps verifying untouched.
# The legacy-prefix SHA256 still measures session-log.md's head bytes
# [0:prefix_length]; only the metadata's storage location moved.
CHECKPOINT_FILE = ".takeover-checkpoint"
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
SCHEMA_RE = re.compile(
    r"^[ \t]*-[ \t]*Memory schema:[ \t]*(\S+)[ \t]*\r?$", re.I | re.MULTILINE
)
LENGTH_RE = re.compile(r"^- Legacy prefix bytes:\s*(\d+)\s*$", re.MULTILINE)
HASH_RE = re.compile(r"^- Legacy prefix SHA256:\s*([0-9A-Fa-f]{64})\s*$", re.MULTILINE)
CHECKPOINT_KIND_RE = re.compile(r"^- Checkpoint kind:\s*(\S+)\s*$", re.MULTILINE)

# v0.2.13: session-log is a bounded rolling recency buffer, not an unbounded
# archive. Only the free region after the checkpoint marker rolls; the
# hash-protected legacy prefix and the checkpoint block are never touched.
# When the free region grows past this line budget, the oldest whole entries
# roll out to legacy/session-log-archive.md (byte-preserved, never deleted).
DEFAULT_SESSION_LOG_LINE_LIMIT = 200
SESSION_LOG_ARCHIVE_REL = "legacy/session-log-archive.md"
# v0.2.16 extends v0.2.15's REVIEW discharge to every structured in-flight
# type. Exact route identity, a non-open status, and a real owner are positive
# evidence; absence or ambiguity keeps the entry live.
SESSION_LOG_DISCHARGE_REL = "legacy/session-log-discharged.md"
ENTRY_ID_CHARS = r"A-Za-z0-9._-"
IN_FLIGHT_ENTRY_TYPES = (
    "REVIEW",
    "UNRESOLVED",
    "CORRECTION",
    "ROLLBACK",
    "CONFLICT",
    "CHECKPOINT",
)
IN_FLIGHT_HEADING_RE = re.compile(
    rf"^\s*##\s+\[({'|'.join(IN_FLIGHT_ENTRY_TYPES)}):([{ENTRY_ID_CHARS}]+)\]",
    re.I,
)
INDEX_ROUTE_LINE_RE = re.compile(r"^\s*-\s*([^:]+?):\s*(.+)$")
ROUTE_FIELD_RE = re.compile(
    r"(?:^|;)\s*([a-z][a-z0-9_-]*)\s*=\s*([^;]*)", re.I
)
VALUE_SPLIT_RE = re.compile(r"\s*[,|，]\s*")
SETTLED_ROUTE_STATUSES = frozenset(
    {
        "acceptance-gate",
        "archived-only",
        "complete",
        "correction-guard",
        "forbidden-action",
        "mandatory-guard",
        "memory-owner",
        "project-owner-indexed",
        "promoted",
        "rejected-path",
        "requirement-owner",
        "resolved",
        "settled",
        "stable-behavior",
        "superseded",
    }
)
LEGACY_DESTINATION_ALLOWED_STATUSES = frozenset(
    {
        "memory-owner",
        "mandatory-guard",
        "rejected-path",
        "project-owner-indexed",
        "archived-only",
        "pending-review",
    }
)
LEGACY_DESTINATION_OWNER_STATUSES = frozenset(
    {"memory-owner", "mandatory-guard", "rejected-path", "project-owner-indexed"}
)
ENTRY_HEADING_RE = re.compile(r"^\s*##\s+")
CHECKPOINT_HEADING_RE = re.compile(r"^\s*##\s+Lite Demo v0\.2\.[0-9]+ Memory Checkpoint\b")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def route_fields(body: str) -> dict[str, str]:
    return {
        key.casefold(): value.strip()
        for key, value in ROUTE_FIELD_RE.findall(body)
    }


def route_values(value: str) -> tuple[str, ...]:
    return tuple(
        item.strip()
        for item in VALUE_SPLIT_RE.split(value)
        if item.strip().casefold() not in {"", "none", "unknown", "pending", "n/a", "-"}
    )


def make_writable_if_exists(path: Path) -> None:
    if not path.exists():
        return
    try:
        path.chmod(path.stat().st_mode | stat.S_IWRITE)
    except OSError:
        # Let the following write/replace raise the original platform error.
        return


def atomic_write_bytes(path: Path, data: bytes) -> None:
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as stream:
            temporary_path = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        make_writable_if_exists(path)
        temporary_path.replace(path)
        temporary_path = None
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


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
    atomic_write_bytes(index_path, updated.encode("utf-8"))
    return True


def parse_checkpoint_fields(text: str) -> tuple[int, str] | None:
    """Parse (prefix_length, prefix_hash) from a checkpoint block's text.

    Works identically for the standalone .takeover-checkpoint file and for a
    legacy in-log checkpoint tail, because the block shape is the same.
    """
    length_match = LENGTH_RE.search(text)
    hash_match = HASH_RE.search(text)
    if not length_match or not hash_match:
        return None
    return int(length_match.group(1)), hash_match.group(1).upper()


def standalone_checkpoint_fields(memory_root: Path) -> tuple[int, str] | None:
    """Read checkpoint metadata from the standalone .takeover-checkpoint file."""
    path = memory_root / CHECKPOINT_FILE
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    marker_count = text.count(MARKER)
    if marker_count == 0:
        raise ValueError(f"{CHECKPOINT_FILE} is missing the checkpoint marker")
    if marker_count != 1:
        raise ValueError(f"expected one takeover checkpoint, found {marker_count}")
    fields = parse_checkpoint_fields(text)
    if fields is None:
        raise ValueError(f"{CHECKPOINT_FILE} is missing prefix length or SHA256")
    return fields


def in_log_checkpoint_fields(data: bytes) -> tuple[int, str] | None:
    """Parse a legacy in-log checkpoint (pre-v0.2.13 roots)."""
    marker = MARKER.encode("ascii")
    count = data.count(marker)
    if count == 0:
        return None
    if count != 1:
        raise ValueError(f"expected one takeover checkpoint, found {count}")
    tail = data[data.index(marker) :].decode("utf-8")
    fields = parse_checkpoint_fields(tail)
    if fields is None:
        raise ValueError("takeover checkpoint is missing prefix length or SHA256")
    return fields


def resolve_checkpoint(memory_root: Path, data: bytes) -> tuple[tuple[int, str] | None, str]:
    """Prefer the standalone checkpoint file; fall back to an in-log marker.

    Returns (fields, source) where source is 'standalone', 'in-log', or 'none'.
    A vestigial in-log marker left behind after migration is ignored once the
    standalone file exists, so a migrated root is never miscounted as two
    checkpoints.
    """
    standalone = standalone_checkpoint_fields(memory_root)
    if standalone is not None:
        return standalone, "standalone"
    in_log = in_log_checkpoint_fields(data)
    if in_log is not None:
        return in_log, "in-log"
    return None, "none"


def current_checkpoint_kind(memory_root: Path, data: bytes) -> str | None:
    checkpoint_path = memory_root / CHECKPOINT_FILE
    if checkpoint_path.is_file():
        text = checkpoint_path.read_text(encoding="utf-8")
    else:
        marker = MARKER.encode("ascii")
        marker_index = data.find(marker)
        if marker_index < 0:
            return None
        text = data[marker_index:].decode("utf-8")
    match = CHECKPOINT_KIND_RE.search(text)
    return match.group(1) if match else None


def verification(data: bytes, memory_root: Path | None = None) -> dict[str, object]:
    if memory_root is not None:
        fields, source = resolve_checkpoint(memory_root, data)
    else:
        fields = in_log_checkpoint_fields(data)
        source = "in-log" if fields is not None else "none"
    if fields is None:
        return {
            "checkpoint_present": False,
            "verified": False,
            "current_bytes": len(data),
            "current_sha256": sha256(data),
            "checkpoint_source": source,
        }
    prefix_length, expected_hash = fields
    if prefix_length > len(data):
        actual_hash = ""
        verified = False
    else:
        actual_hash = sha256(data[:prefix_length])
        verified = actual_hash == expected_hash
    checkpoint_count = 1 if source == "standalone" else data.count(MARKER.encode("ascii"))
    return {
        "checkpoint_present": True,
        "verified": verified,
        "legacy_prefix_bytes": prefix_length,
        "legacy_prefix_sha256": expected_hash,
        "actual_prefix_sha256": actual_hash,
        "current_bytes": len(data),
        "checkpoint_count": checkpoint_count,
        "checkpoint_source": source,
    }


def legacy_prefix_text(data: bytes, prefix_length: int | None = None) -> str:
    # After decoupling there is no in-log marker to split on, so the recorded
    # prefix_length is the authoritative boundary. Falling back to the marker
    # keeps pre-v0.2.13 roots working before migration.
    if prefix_length is not None:
        return data[:prefix_length].decode("utf-8", errors="replace")
    marker = MARKER.encode("ascii")
    marker_index = data.find(marker)
    prefix = data[:marker_index] if marker_index >= 0 else data
    return prefix.decode("utf-8", errors="replace")


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


def has_meaningful_legacy_history(data: bytes) -> bool:
    return has_meaningful_legacy_text(legacy_prefix_text(data))


def iter_legacy_surface_paths(memory_root: Path) -> tuple[Path, ...]:
    paths: list[Path] = []
    for name in LEGACY_SURFACE_NAMES:
        candidate = memory_root / name
        if candidate.is_file():
            paths.append(candidate)
    for directory_name in LEGACY_SURFACE_DIRS:
        directory = memory_root / directory_name
        if directory.is_dir():
            paths.extend(sorted(path for path in directory.rglob("*.md") if path.is_file()))
    return tuple(dict.fromkeys(paths))


def has_meaningful_legacy_surfaces(memory_root: Path) -> bool:
    for path in iter_legacy_surface_paths(memory_root):
        if path.name == LEGACY_DESTINATIONS_FILE:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return True
        if has_meaningful_legacy_text(text):
            return True
    return False


def legacy_destinations_verified(memory_root: Path) -> bool:
    destination_path = memory_root / LEGACY_DESTINATIONS_FILE
    if not destination_path.is_file():
        return False
    try:
        text = destination_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    if "legacy destination schema" not in text.casefold():
        return False

    entries: list[tuple[str, dict[str, str]]] = []
    for line in text.splitlines():
        match = INDEX_ROUTE_LINE_RE.match(line)
        if not match or "status=" not in line.casefold():
            continue
        entries.append((match.group(1).strip(), route_fields(match.group(2))))
    if not entries:
        return False

    seen_ids: set[str] = set()
    for entry_id, fields in entries:
        normalized_id = entry_id.casefold()
        if normalized_id in seen_ids:
            return False
        seen_ids.add(normalized_id)

        status = fields.get("status", "").casefold()
        if status not in LEGACY_DESTINATION_ALLOWED_STATUSES:
            return False
        if status == "pending-review":
            return False
        if any(not fields.get(required, "").strip() for required in ("source", "scope", "reason")):
            return False

        wake_terms = route_values(fields.get("aliases", "")) + route_values(
            fields.get("keywords", "")
        )
        owners = route_values(fields.get("owners", ""))
        probes = route_values(fields.get("probes", ""))
        if status != "archived-only" and not wake_terms:
            return False
        if status in LEGACY_DESTINATION_OWNER_STATUSES:
            if not owners or not probes:
                return False
            for pointer in owners:
                owner_path = (memory_root / pointer.split("#", 1)[0]).resolve()
                if not owner_path.is_file():
                    return False
    return True


def roll_free_region(
    log_path: Path,
    memory_root: Path,
    max_lines: int = DEFAULT_SESSION_LOG_LINE_LIMIT,
) -> dict[str, object]:
    """Archive the oldest recency-buffer entries that sit AFTER the checkpoint.

    Only the free-growth region (bytes after the checkpoint block) is touched.
    The hash-protected legacy prefix and the checkpoint block are copied
    verbatim, so takeover verification keeps passing. Whole `##` entries move
    to ``legacy/session-log-archive.md`` for byte preservation; entries are
    never cut mid-way. Rolling keeps the newest entries and stops archiving as
    soon as the buffer fits the line budget.
    """
    if max_lines < 1:
        raise ValueError("line budget must be positive")
    if not log_path.is_file():
        return {"action": "roll", "changed": False, "reason": "no-session-log"}
    data = log_path.read_bytes()
    # v0.2.13: the checkpoint may live in the standalone file (no in-log marker)
    # or, on an un-migrated legacy root, still inside the log. Either way the
    # protected boundary is the recorded legacy prefix length, not a marker
    # position. Everything at/after prefix_length is the free recency region.
    fields, source = resolve_checkpoint(memory_root, data)
    if fields is None:
        # Pre-takeover log: every byte is unprotected legacy prefix evidence.
        # Never roll before a checkpoint boundary exists.
        return {"action": "roll", "changed": False, "reason": "no-checkpoint"}
    prefix_length, _ = fields
    if prefix_length > len(data):
        return {"action": "roll", "changed": False, "reason": "prefix-out-of-range"}
    text = data.decode("utf-8")
    lines = text.splitlines(keepends=True)
    if len(lines) <= max_lines:
        return {
            "action": "roll",
            "changed": False,
            "reason": "within-bound",
            "line_count": len(lines),
        }

    # Convert the protected byte boundary (prefix_length) into a line index:
    # the free region begins at the first line whose byte offset is >= prefix_length.
    protected_bytes = 0
    free_start = len(lines)
    for index, line in enumerate(lines):
        if protected_bytes >= prefix_length:
            free_start = index
            break
        protected_bytes += len(line.encode("utf-8"))
    else:
        free_start = len(lines)
    # An un-migrated legacy root still has the checkpoint block sitting in the
    # free region; skip past its heading/field lines so it is never archived.
    while free_start < len(lines) and (
        lines[free_start].startswith(("#", "-")) or not lines[free_start].strip()
    ):
        if ENTRY_HEADING_RE.match(lines[free_start]) and not CHECKPOINT_HEADING_RE.match(
            lines[free_start]
        ):
            break
        free_start += 1

    # Entry boundaries inside the free region only.
    entry_starts = [
        index
        for index in range(free_start, len(lines))
        if ENTRY_HEADING_RE.match(lines[index])
        and not CHECKPOINT_HEADING_RE.match(lines[index])
    ]
    if not entry_starts:
        return {
            "action": "roll",
            "changed": False,
            "reason": "no-free-entries",
            "line_count": len(lines),
        }

    # Archive oldest whole entries until the remaining file fits the budget.
    protected_line_count = entry_starts[0]
    cut_index = 0
    while cut_index < len(entry_starts) - 1:
        next_boundary = entry_starts[cut_index + 1]
        remaining = protected_line_count + (len(lines) - next_boundary)
        if remaining <= max_lines:
            cut_index += 1
            break
        cut_index += 1
    boundary = entry_starts[cut_index]
    if cut_index == 0:
        return {
            "action": "roll",
            "changed": False,
            "reason": "single-entry-exceeds-budget",
            "line_count": len(lines),
        }

    preserved = "".join(lines[: entry_starts[0]])
    archived = "".join(lines[entry_starts[0] : boundary])
    kept = "".join(lines[boundary:])

    if log_path.read_bytes() != data:
        raise ValueError("session-log.md changed during roll; retry from a fresh read")

    archive_path = memory_root / SESSION_LOG_ARCHIVE_REL
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    if not archive_path.exists():
        archive_path.write_bytes(
            (
                "# Session Log Archive\n\n"
                "<!-- Byte-preserved recency entries rolled out of session-log.md. "
                "Read-only evidence; reach via targeted search, not default recall. -->\n\n"
            ).encode("utf-8")
        )
    with archive_path.open("ab") as stream:
        stamp = datetime.now(timezone.utc).isoformat()
        stream.write(f"<!-- rolled {stamp} -->\n".encode("utf-8"))
        archived_bytes = archived.encode("utf-8")
        stream.write(archived_bytes)
        if not archived_bytes.endswith((b"\n", b"\r")):
            stream.write(b"\n")

    if log_path.read_bytes() != data:
        raise ValueError("session-log.md changed during roll; live log was not replaced")
    atomic_write_bytes(log_path, (preserved + kept).encode("utf-8"))

    verified = verification(log_path.read_bytes(), memory_root)
    return {
        "action": "roll",
        "changed": True,
        "reason": "rolled",
        "archived_entries": cut_index,
        "line_count": len((preserved + kept).splitlines()),
        "archive_path": str(archive_path),
        "checkpoint_verified": bool(verified.get("verified")),
    }


def contains_exact_entry_token(text: str, token: str) -> bool:
    return bool(
        re.search(
            rf"(?<![{ENTRY_ID_CHARS}]){re.escape(token)}(?![{ENTRY_ID_CHARS}])",
            text,
            re.I,
        )
    )


def entry_is_homed(entry_type: str, entry_id: str, index_text: str) -> bool:
    """Deterministic settlement check for one structured in-flight entry.

    Positive evidence only: a legacy REVIEW route may use the exact id as its
    key; every structured route may use an exact ``entry=TYPE:id`` field. Every
    referencing route must have a known settled status (legacy REVIEW routes
    may omit status), must not point at the in-log anchor, and must name a real
    owner. Missing or ambiguous evidence keeps the entry admitted.
    """
    normalized_type = entry_type.upper()
    typed_id = f"{normalized_type}:{entry_id}"
    in_log_anchor = f"session-log.md#{typed_id}"
    referencing: list[dict[str, str]] = []
    for line in index_text.splitlines():
        match = INDEX_ROUTE_LINE_RE.match(line)
        if not match:
            continue
        key, body = match.group(1).strip(), match.group(2)
        fields = route_fields(body)
        legacy_review_key = (
            normalized_type == "REVIEW" and key.casefold() == entry_id.casefold()
        )
        exact_entry_field = fields.get("entry", "").casefold() == typed_id.casefold()
        if legacy_review_key or exact_entry_field:
            referencing.append(fields)
    if not referencing:
        return False
    has_settled_owner = False
    for fields in referencing:
        status = fields.get("status", "").casefold()
        if status and status not in SETTLED_ROUTE_STATUSES:
            return False
        if normalized_type != "REVIEW" and not status:
            return False
        owners = route_values(fields.get("owners", ""))
        if any(contains_exact_entry_token(owner, in_log_anchor) for owner in owners):
            return False
        if owners:
            has_settled_owner = True
    return has_settled_owner


def review_id_is_homed(review_id: str, index_text: str) -> bool:
    """Backward-compatible v0.2.15 review settlement helper."""
    return entry_is_homed("REVIEW", review_id, index_text)


def discharge_homed_entries(log_path: Path, memory_root: Path) -> dict[str, object]:
    """Move settled structured entries out of the live session log.

    The discharge half of the admission/discharge gate: an admitted structured
    entry whose exact id shows positive settlement evidence in index.md leaves
    the live log as a whole entry, byte-preserved, into
    legacy/session-log-discharged.md. Unstructured or unhomed entries stay
    admitted. The hash-protected legacy prefix and checkpoint are never
    touched.
    """
    if not log_path.is_file():
        return {"action": "discharge", "changed": False, "reason": "no-session-log"}
    data = log_path.read_bytes()
    fields, _source = resolve_checkpoint(memory_root, data)
    if fields is None:
        return {"action": "discharge", "changed": False, "reason": "no-checkpoint"}
    prefix_length, _ = fields
    if prefix_length > len(data):
        return {"action": "discharge", "changed": False, "reason": "prefix-out-of-range"}
    index_path = memory_root / "index.md"
    index_data = index_path.read_bytes() if index_path.is_file() else b""
    index_text = index_data.decode("utf-8")

    lines = data.decode("utf-8").splitlines(keepends=True)
    protected_bytes = 0
    free_start = len(lines)
    for index, line in enumerate(lines):
        if protected_bytes >= prefix_length:
            free_start = index
            break
        protected_bytes += len(line.encode("utf-8"))
    while free_start < len(lines) and (
        lines[free_start].startswith(("#", "-")) or not lines[free_start].strip()
    ):
        if ENTRY_HEADING_RE.match(lines[free_start]) and not CHECKPOINT_HEADING_RE.match(
            lines[free_start]
        ):
            break
        free_start += 1
    entry_starts = [
        index
        for index in range(free_start, len(lines))
        if ENTRY_HEADING_RE.match(lines[index])
        and not CHECKPOINT_HEADING_RE.match(lines[index])
    ]
    if not entry_starts:
        return {
            "action": "discharge",
            "changed": False,
            "reason": "nothing-to-discharge",
            "discharged": [],
            "discharged_entries": [],
            "retained_reviews": [],
            "retained_structured_entries": [],
            "retained_entries": 0,
        }

    kept_lines = lines[: entry_starts[0]]
    discharged: list[tuple[str, str, str]] = []
    retained_reviews: list[str] = []
    retained_structured_entries: list[str] = []
    retained_entries = 0
    for position, start in enumerate(entry_starts):
        end = entry_starts[position + 1] if position + 1 < len(entry_starts) else len(lines)
        entry_match = IN_FLIGHT_HEADING_RE.match(lines[start])
        if entry_match:
            entry_type, entry_id = entry_match.group(1).upper(), entry_match.group(2)
        else:
            entry_type, entry_id = "", ""
        if entry_match and entry_is_homed(entry_type, entry_id, index_text):
            discharged.append((entry_type, entry_id, "".join(lines[start:end])))
            continue
        if entry_match:
            retained_structured_entries.append(f"{entry_type}:{entry_id}")
            if entry_type == "REVIEW":
                retained_reviews.append(entry_id)
        retained_entries += 1
        kept_lines.extend(lines[start:end])

    if not discharged:
        return {
            "action": "discharge",
            "changed": False,
            "reason": "nothing-to-discharge",
            "discharged": [],
            "discharged_entries": [],
            "retained_reviews": retained_reviews,
            "retained_structured_entries": retained_structured_entries,
            "retained_entries": retained_entries,
        }

    current_index_data = index_path.read_bytes() if index_path.is_file() else b""
    if log_path.read_bytes() != data or current_index_data != index_data:
        raise ValueError("session-log.md or index.md changed during discharge; retry")

    discharge_path = memory_root / SESSION_LOG_DISCHARGE_REL
    discharge_path.parent.mkdir(parents=True, exist_ok=True)
    if not discharge_path.exists():
        discharge_path.write_bytes(
            (
                "# Session Log Discharged Entries\n\n"
                "<!-- Byte-preserved entries whose owner settled in index.md; the live\n"
                "owner is authoritative. Read-only evidence, reach via targeted search. -->\n\n"
            ).encode("utf-8")
        )
    with discharge_path.open("ab") as stream:
        stamp = datetime.now(timezone.utc).isoformat()
        for entry_type, entry_id, entry_text in discharged:
            archive_id = entry_id if entry_type == "REVIEW" else f"{entry_type}:{entry_id}"
            stream.write(f"<!-- discharged {archive_id} {stamp} -->\n".encode("utf-8"))
            entry_bytes = entry_text.encode("utf-8")
            stream.write(entry_bytes)
            if not entry_bytes.endswith((b"\n", b"\r")):
                stream.write(b"\n")

    current_index_data = index_path.read_bytes() if index_path.is_file() else b""
    if log_path.read_bytes() != data or current_index_data != index_data:
        raise ValueError(
            "session-log.md or index.md changed during discharge; live log was not replaced"
        )
    atomic_write_bytes(log_path, "".join(kept_lines).encode("utf-8"))

    verified = verification(log_path.read_bytes(), memory_root)
    return {
        "action": "discharge",
        "changed": True,
        "reason": "discharged",
        "discharged": [entry_id for _, entry_id, _ in discharged],
        "discharged_entries": [
            f"{entry_type}:{entry_id}" for entry_type, entry_id, _ in discharged
        ],
        "retained_reviews": retained_reviews,
        "retained_structured_entries": retained_structured_entries,
        "retained_entries": retained_entries,
        "archive_path": str(discharge_path),
        "checkpoint_verified": bool(verified.get("verified")),
    }


def discharge_homed_reviews(log_path: Path, memory_root: Path) -> dict[str, object]:
    """Backward-compatible v0.2.15 entry point for the generalized discharge."""
    return discharge_homed_entries(log_path, memory_root)


def checkpoint_block_text(
    prefix_length: int, prefix_hash: str, checkpoint_kind: str
) -> str:
    return (
        f"{MARKER}\n"
        "## Lite Demo v0.2.7 Memory Checkpoint\n\n"
        f"- Checkpoint kind: {checkpoint_kind}\n"
        f"- Recorded UTC: {datetime.now(timezone.utc).isoformat()}\n"
        f"- Legacy prefix bytes: {prefix_length}\n"
        f"- Legacy prefix SHA256: {prefix_hash}\n"
        "- Owner router: index.md\n"
        "- Rule: preserve the legacy prefix; repair owner routes without rewriting old evidence.\n"
    )


def append_checkpoint(
    log_path: Path,
    data: bytes,
    legacy_prefix_bytes: int | None = None,
    legacy_prefix_sha256: str | None = None,
    checkpoint_kind: str = "legacy-takeover",
) -> dict[str, object]:
    # v0.2.13: the checkpoint block lives in the standalone .takeover-checkpoint
    # file, not appended to session-log.md. The legacy prefix is still measured
    # against session-log.md bytes ([0:prefix_length]); only the metadata's home
    # moved. session-log.md bytes are never touched by this write.
    memory_root = log_path.parent
    existing = verification(data, memory_root)
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
    checkpoint = checkpoint_block_text(prefix_length, prefix_hash, checkpoint_kind)
    checkpoint_path = memory_root / CHECKPOINT_FILE
    atomic_write_bytes(checkpoint_path, checkpoint.encode("utf-8"))

    result = verification(log_path.read_bytes(), memory_root)
    result["changed"] = True
    result["action"] = "checkpoint-written"
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
    legacy_destinations_required = False
    if log_path.is_file():
        log_data = log_path.read_bytes()
        log_verification = verification(log_data, memory_root)
        checkpoint_kind = current_checkpoint_kind(memory_root, log_data)
        # Measure "meaningful legacy history" against the recorded prefix, not
        # the in-log marker: after decoupling there is no marker, and the free
        # recency region past the prefix must not be miscounted as old history.
        prefix_length = log_verification.get("legacy_prefix_bytes")
        legacy_destinations_required = has_meaningful_legacy_text(
            legacy_prefix_text(
                log_data,
                prefix_length if isinstance(prefix_length, int) else None,
            )
        )
        result.update(log_verification)
        result["checkpoint_kind"] = checkpoint_kind
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
                "checkpoint_kind": None,
                "session_log_sha256": None,
                "previous_checkpoint_count": 0,
            }
        )
    # A fresh initialization has no legacy surfaces: index/current-context
    # written after that checkpoint are current memory, not takeover input.
    # Every legacy/unknown checkpoint kind keeps the full destination gate.
    if (
        not legacy_destinations_required
        and result.get("checkpoint_kind") != "fresh-initialization"
    ):
        legacy_destinations_required = has_meaningful_legacy_surfaces(memory_root)
    result["checkpoint_required"] = True
    current_checkpoint_verified = bool(result["verified"])
    legacy_destinations_present = (memory_root / LEGACY_DESTINATIONS_FILE).is_file()
    legacy_destinations_ok = (
        not legacy_destinations_required or legacy_destinations_verified(memory_root)
    )
    result["legacy_destinations_required"] = legacy_destinations_required
    result["legacy_destinations_present"] = legacy_destinations_present
    result["legacy_destinations_verified"] = legacy_destinations_ok
    result["current_checkpoint_verified"] = current_checkpoint_verified
    result["completion_verified"] = bool(
        result["schema_verified"] and current_checkpoint_verified and legacy_destinations_ok
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
    if legacy_destinations_required and not legacy_destinations_present:
        reasons.append("legacy-destinations-missing")
    elif legacy_destinations_required and not legacy_destinations_ok:
        reasons.append("legacy-destinations-invalid")
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
- recovery: active task, routed owner, exact unresolved item, targeted evidence
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


def migrate_checkpoint(memory_root: Path) -> dict[str, object]:
    """Move a pre-v0.2.13 in-log checkpoint into the standalone file.

    Non-destructive: session-log.md bytes are never touched. The vestigial
    in-log marker is left in place and ignored by readers once the standalone
    file exists. Idempotent: a root that is already standalone is a no-op.
    """
    log_path = memory_root / "session-log.md"
    checkpoint_path = memory_root / CHECKPOINT_FILE
    if checkpoint_path.is_file():
        return {"action": "migrate", "changed": False, "reason": "already-standalone"}
    if not log_path.is_file():
        return {"action": "migrate", "changed": False, "reason": "no-session-log"}
    data = log_path.read_bytes()
    fields = in_log_checkpoint_fields(data)
    if fields is None:
        return {"action": "migrate", "changed": False, "reason": "no-checkpoint"}
    prefix_length, prefix_hash = fields
    if prefix_length > len(data) or sha256(data[:prefix_length]) != prefix_hash:
        raise ValueError("in-log checkpoint prefix does not match session-log bytes")
    checkpoint_path.write_text(
        checkpoint_block_text(prefix_length, prefix_hash, "migrated-from-in-log"),
        encoding="utf-8",
    )
    result = verification(log_path.read_bytes(), memory_root)
    result["changed"] = True
    result["action"] = "migrate"
    result["reason"] = "migrated"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=("initialize", "inspect", "apply", "verify", "roll", "migrate", "discharge"),
    )
    parser.add_argument("memory_root", type=Path, help="Path to docs/codex")
    parser.add_argument(
        "--line-budget",
        type=int,
        default=DEFAULT_SESSION_LOG_LINE_LIMIT,
        help="roll: keep session-log.md within this many lines by archiving the oldest free-region entries",
    )
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
        elif args.command == "roll":
            before = root_verification(memory_root)
            if before["takeover_required"]:
                raise ValueError(
                    "roll requires a completed takeover; run inspect/apply first"
                )
            result = roll_free_region(log_path, memory_root, args.line_budget)
            after = root_verification(memory_root)
            if after["takeover_required"]:
                raise ValueError(
                    "roll broke takeover verification; restore session-log.md from "
                    + SESSION_LOG_ARCHIVE_REL
                )
            result["completion_verified"] = after["completion_verified"]
            result["takeover_required"] = after["takeover_required"]
        elif args.command == "migrate":
            result = migrate_checkpoint(memory_root)
        elif args.command == "discharge":
            before = root_verification(memory_root)
            if before["takeover_required"]:
                raise ValueError(
                    "discharge requires a completed takeover; run inspect/apply first"
                )
            result = discharge_homed_reviews(log_path, memory_root)
            after = root_verification(memory_root)
            if after["takeover_required"]:
                raise ValueError(
                    "discharge broke takeover verification; restore session-log.md from "
                    + SESSION_LOG_DISCHARGE_REL
                )
            result["completion_verified"] = after["completion_verified"]
            result["takeover_required"] = after["takeover_required"]
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
