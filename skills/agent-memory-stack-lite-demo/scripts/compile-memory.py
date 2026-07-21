#!/usr/bin/env python3
"""Build and query a disposable Lite Demo derived memory index."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import stat
import unicodedata
from pathlib import Path
from typing import Any


ENGINE_VERSION = "v0.2.17-dev-derived-index-2"
CACHE_REL = ".lite-demo-cache/v1/derived-index.json"
RESERVED_ROOTS = (
    (".lite-demo-cache",),
    (".lite-demo-work",),
    ("legacy", "receipts"),
)
MAX_TERMS_PER_RECORD = 96
MAX_TERM_BYTES_PER_RECORD = 1024
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 30

ROUTE_LINE_RE = re.compile(r"^\s*-\s*([^:]+):\s*(.+)$")
FIELD_RE = re.compile(r"(?:^|;)\s*([a-z][a-z0-9_-]*)\s*=\s*([^;]*)", re.I)
VALUE_SPLIT_RE = re.compile(r"\s*[,|，]\s*")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
IN_FLIGHT_HEADING_RE = re.compile(
    r"^\s*##\s+\[(REVIEW|UNRESOLVED|CORRECTION|ROLLBACK|CONFLICT|CHECKPOINT):([A-Za-z0-9._-]+)\]",
    re.I,
)
META_RE = re.compile(r"^\s*-\s*([^:：]{2,40})[:：]\s*(.+?)\s*$")
ASCII_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9._-]{1,}", re.I)
ASCII_ALNUM_RE = re.compile(r"[A-Za-z0-9]")
CJK_RUN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]+")

MANDATORY_STATUSES = {
    "acceptance-gate",
    "correction-guard",
    "forbidden-action",
    "mandatory-guard",
    "rejected-path",
    "stable-guard",
    "irreversible-action-guard",
}
OPEN_STATUSES = {
    "pending-review",
    "unresolved",
    "blocked",
    "unknown",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def normalize(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold().strip()


def split_values(value: str) -> list[str]:
    return [item.strip().strip("`\"'") for item in VALUE_SPLIT_RE.split(value) if item.strip()]


def is_none_value(value: str) -> bool:
    return normalize(value) in {"", "none", "n/a", "-", "无"}


def rel_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def reserved_reason(parts: tuple[str, ...]) -> str | None:
    for reserved in RESERVED_ROOTS:
        if parts[: len(reserved)] == reserved:
            return "/".join(reserved)
    return None


def classify_path(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return "other"


def read_stable_bytes(path: Path) -> bytes:
    before = path.stat()
    data = path.read_bytes()
    after = path.stat()
    if (
        before.st_size != after.st_size
        or before.st_mtime_ns != after.st_mtime_ns
        or before.st_ctime_ns != after.st_ctime_ns
    ):
        raise RuntimeError(f"source changed during read: {path}")
    return data


def walk_source_universe(memory_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    entries: list[dict[str, Any]] = []
    source_files: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = [
        {"path": "/".join(parts), "reason": "/".join(parts)}
        for parts in RESERVED_ROOTS
    ]
    stack = [memory_root]
    while stack:
        directory = stack.pop()
        children = sorted(directory.iterdir(), key=lambda item: item.name.casefold())
        for child in children:
            rel = rel_posix(child, memory_root)
            parts = tuple(Path(rel).parts)
            reason = reserved_reason(parts)
            if reason:
                continue
            kind = classify_path(child)
            entry: dict[str, Any] = {"path": rel, "type": kind}
            entries.append(entry)
            if kind == "directory":
                stack.append(child)
            elif kind == "file":
                data = read_stable_bytes(child)
                file_entry = {
                    "path": rel,
                    "type": "file",
                    "bytes": len(data),
                    "sha256": sha256_bytes(data),
                }
                entry.update({"bytes": file_entry["bytes"], "sha256": file_entry["sha256"]})
                source_files.append(file_entry)
            else:
                entry["disposition"] = "unindexable"
    entries.sort(key=lambda item: item["path"])
    source_files.sort(key=lambda item: item["path"])
    return entries, source_files, excluded


def inventory_hash(entries: list[dict[str, Any]], excluded: list[dict[str, Any]]) -> str:
    rows: list[str] = []
    for item in entries:
        rows.append(
            "|".join(
                [
                    item["path"],
                    item["type"],
                    str(item.get("bytes", "")),
                    item.get("sha256", ""),
                    item.get("disposition", ""),
                ]
            )
        )
    # Excluded output roots are reported for transparency, but they are not part
    # of the authoritative source inventory hash. Otherwise writing the cache
    # would make the cache immediately stale by introducing `.lite-demo-cache/`.
    _ = excluded
    return sha256_text("\n".join(sorted(rows)))


def cjk_ngrams(text: str) -> list[str]:
    grams: list[str] = []
    for match in CJK_RUN_RE.finditer(text):
        run = match.group(0)
        if len(run) <= 6:
            grams.append(run)
        for width in (2, 3):
            if len(run) >= width:
                grams.extend(run[i : i + width] for i in range(len(run) - width + 1))
    return grams


def bounded_terms(candidates: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    total_bytes = 0
    for candidate in candidates:
        term = normalize(candidate)
        if not term or term in seen:
            continue
        encoded = term.encode("utf-8")
        if len(result) >= MAX_TERMS_PER_RECORD or total_bytes + len(encoded) > MAX_TERM_BYTES_PER_RECORD:
            break
        seen.add(term)
        result.append(term)
        total_bytes += len(encoded)
    return result


def terms_for_text(text: str) -> list[str]:
    normalized = normalize(text)
    candidates = ASCII_TOKEN_RE.findall(normalized)
    candidates.extend(cjk_ngrams(normalized))
    return bounded_terms(candidates)


def heading_anchor(title: str, line_number: int) -> str:
    compact = re.sub(r"\s+", "-", normalize(title))
    compact = re.sub(r"[^a-z0-9._\-\u3400-\u4dbf\u4e00-\u9fff]+", "", compact)
    compact = compact.strip("-._")
    if not compact:
        compact = sha256_text(title)[:10].lower()
    return f"line-{line_number}-{compact[:60]}"


def route_fields(body: str) -> dict[str, str]:
    return {key.casefold(): value.strip() for key, value in FIELD_RE.findall(body)}


def route_record(memory_root: Path, rel_path: str, line_number: int, line: str, source_sha: str) -> dict[str, Any] | None:
    match = ROUTE_LINE_RE.match(line)
    if not match or "owners=" not in line.casefold():
        return None
    scope = match.group(1).strip()
    fields = route_fields(match.group(2))
    status = normalize(fields.get("status", ""))
    mandatory_values = split_values(fields.get("mandatory", ""))
    mandatory = any(not is_none_value(value) for value in mandatory_values) or status in MANDATORY_STATUSES
    anchor = f"route-line-{line_number}"
    terms = (
        [scope]
        + split_values(fields.get("aliases", ""))
        + split_values(fields.get("keywords", ""))
        + split_values(fields.get("entry", ""))
        + terms_for_text(line)
        + terms_for_text(rel_path)
    )
    record_id = stable_record_id("route", rel_path, anchor)
    return {
        "record_id": record_id,
        "record_type": "route",
        "channel": "route",
        "source_path": rel_path,
        "anchor": anchor,
        "line_start": line_number,
        "line_end": line_number,
        "source_sha256": source_sha,
        "span_sha256": sha256_text(line),
        "scope": scope,
        "aliases": split_values(fields.get("aliases", "")),
        "keywords": split_values(fields.get("keywords", "")),
        "owners": split_values(fields.get("owners", "")),
        "mandatory": mandatory,
        "status": status,
        "memory_class": "route",
        "terms": bounded_terms(terms),
    }


def metadata_from_lines(lines: list[str]) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in lines[:24]:
        match = META_RE.match(line)
        if not match:
            continue
        key = normalize(match.group(1)).replace(" ", "-")
        metadata[key] = match.group(2).strip()
    return metadata


def channel_for(rel_path: str, heading: str) -> tuple[str, str, str]:
    in_flight = IN_FLIGHT_HEADING_RE.match(heading)
    if rel_path == "session-log.md" and in_flight:
        return "in-flight", in_flight.group(1).upper(), in_flight.group(2)
    if rel_path == "session-log.md":
        return "session-log", "", ""
    if rel_path.startswith("legacy/session-log-"):
        return "cold-log", "", ""
    if rel_path.startswith("legacy/"):
        return "legacy", "", ""
    if rel_path.startswith("routes/") or rel_path == "index.md":
        return "route", "", ""
    return "owner", "", ""


def stable_record_id(record_type: str, rel_path: str, anchor: str) -> str:
    digest = sha256_text(f"memory|{record_type}|{rel_path}|{anchor}")[:20]
    return f"mem-{digest}"


def section_records(rel_path: str, text: str, source_sha: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    headings: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            headings.append((index, len(match.group(1)), match.group(2).strip()))
    if not headings:
        if not text.strip():
            return []
        headings = [(0, 0, Path(rel_path).name)]

    records: list[dict[str, Any]] = []
    for position, (start, level, title) in enumerate(headings):
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        section_lines = lines[start:end]
        section_text = "\n".join(section_lines)
        line_start = start + 1
        line_end = max(line_start, end)
        anchor = heading_anchor(title, line_start)
        metadata = metadata_from_lines(section_lines)
        heading_line = lines[start] if lines else title
        channel, entry_type, entry_id = channel_for(rel_path, heading_line)
        status = normalize(metadata.get("status", ""))
        memory_class = metadata.get("memory-class", "")
        scope = metadata.get("scope", title)
        aliases = split_values(metadata.get("aliases/keywords", "")) + split_values(metadata.get("aliases", ""))
        keywords = split_values(metadata.get("keywords", ""))
        mandatory = status in MANDATORY_STATUSES or any(
            token in normalize(memory_class)
            for token in (
                "prohibition",
                "guard",
                "acceptance",
                "rejected",
                "requirement",
                "stable",
            )
        )
        terms = (
            [title, scope, memory_class, status, rel_path, entry_type, entry_id]
            + aliases
            + keywords
            + terms_for_text(section_text)
            + terms_for_text(rel_path)
        )
        record = {
            "record_id": stable_record_id("section", rel_path, anchor),
            "record_type": "section",
            "channel": channel,
            "source_path": rel_path,
            "anchor": anchor,
            "line_start": line_start,
            "line_end": line_end,
            "source_sha256": source_sha,
            "span_sha256": sha256_text(section_text),
            "scope": scope,
            "aliases": aliases,
            "keywords": keywords,
            "owners": [],
            "mandatory": mandatory,
            "status": status,
            "memory_class": memory_class,
            "terms": bounded_terms(terms),
        }
        if entry_type:
            record["entry"] = f"{entry_type}:{entry_id}"
        records.append(record)
    return records


def parse_text_file(memory_root: Path, source_file: dict[str, Any]) -> list[dict[str, Any]]:
    rel_path = source_file["path"]
    path = memory_root / rel_path
    suffix = path.suffix.casefold()
    if suffix not in {".md", ".txt"} and path.name not in {"AGENTS.md", "CODEX_GUIDANCE.md"}:
        return []
    if rel_path.startswith("legacy/session-log-"):
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []

    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        record = route_record(memory_root, rel_path, line_number, line, source_file["sha256"])
        if record:
            records.append(record)
    sections = section_records(rel_path, text, source_file["sha256"])
    if rel_path == "session-log.md":
        sections = [record for record in sections if record.get("channel") == "in-flight"]
    records.extend(sections)
    return records


def build_index(memory_root: Path) -> dict[str, Any]:
    entries, source_files, excluded = walk_source_universe(memory_root)
    inv_hash = inventory_hash(entries, excluded)
    records: list[dict[str, Any]] = []
    for source_file in source_files:
        records.extend(parse_text_file(memory_root, source_file))
    records.sort(key=lambda item: (item["source_path"], item["line_start"], item["record_id"]))
    record_hash = sha256_text(
        "\n".join(
            f"{item['record_id']}|{item['source_path']}|{item['anchor']}|{item['span_sha256']}"
            for item in records
        )
    )
    return {
        "schema": "lite-demo-derived-index-v1",
        "engine_version": ENGINE_VERSION,
        "source_inventory_hash": inv_hash,
        "record_set_hash": record_hash,
        "source_entries": entries,
        "excluded_entries": excluded,
        "source_files": source_files,
        "records": records,
    }


def cache_path(memory_root: Path) -> Path:
    return memory_root / CACHE_REL


def write_cache(memory_root: Path, cache: dict[str, Any]) -> tuple[bool, str]:
    path = cache_path(memory_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    old = path.read_bytes() if path.exists() else None
    if old == data:
        return False, sha256_bytes(data)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_bytes(data)
    os.replace(temp, path)
    return True, sha256_bytes(data)


def load_cache(memory_root: Path) -> dict[str, Any]:
    path = cache_path(memory_root)
    if not path.is_file():
        raise RuntimeError("derived index cache is missing; run build first")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "lite-demo-derived-index-v1":
        raise RuntimeError("derived index schema mismatch")
    return data


def current_inventory_hash(memory_root: Path) -> str:
    entries, _source_files, excluded = walk_source_universe(memory_root)
    return inventory_hash(entries, excluded)


def cache_is_fresh(memory_root: Path, cache: dict[str, Any]) -> bool:
    return cache.get("source_inventory_hash") == current_inventory_hash(memory_root)


def filters_hash(
    channels: list[str] | None,
    memory_classes: list[str] | None,
    statuses: list[str] | None,
    source_prefixes: list[str] | None,
) -> str:
    payload = {
        "channels": sorted(normalize(item) for item in (channels or [])),
        "memory_classes": sorted(normalize(item) for item in (memory_classes or [])),
        "statuses": sorted(normalize(item) for item in (statuses or [])),
        "source_prefixes": sorted(item.replace("\\", "/").strip("/") for item in (source_prefixes or [])),
    }
    return sha256_text(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False))


def token_payload(query: str, inventory: str, page_size: int, offset: int, filter_hash: str) -> str:
    payload = {
        "v": 1,
        "query_hash": sha256_text(normalize(query)),
        "inventory_hash": inventory,
        "page_size": page_size,
        "offset": offset,
        "filter_hash": filter_hash,
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def parse_token(token: str) -> dict[str, Any]:
    padded = token + "=" * (-len(token) % 4)
    return json.loads(base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8"))


def phrase_hit(query: str, value: str) -> bool:
    q = normalize(query)
    v = normalize(value)
    if not q or not v:
        return False
    if q == v:
        return True
    return bounded_phrase_contains(q, v) or bounded_phrase_contains(v, q)


def bounded_phrase_contains(needle: str, haystack: str) -> bool:
    if not needle or not haystack:
        return False
    if needle.isascii() and len(needle) < 2:
        return False
    left = r"(?<![A-Za-z0-9])" if ASCII_ALNUM_RE.match(needle[0]) else ""
    right = r"(?![A-Za-z0-9])" if ASCII_ALNUM_RE.match(needle[-1]) else ""
    if needle.isascii() or ASCII_ALNUM_RE.search(needle):
        return re.search(left + re.escape(needle) + right, haystack, re.I) is not None
    return needle in haystack


def score_record(record: dict[str, Any], query: str, query_terms: list[str]) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []
    identity_values = [
        ("record_id", record.get("record_id", "")),
        ("source_path", record.get("source_path", "")),
        ("anchor", record.get("anchor", "")),
        ("entry", record.get("entry", "")),
    ]
    if any(identity_hit(query, str(value), field_name) for field_name, value in identity_values):
        score += 80
        reasons.append("identity")
    for field_name, weight in (("scope", 30), ("aliases", 28), ("keywords", 24)):
        value = record.get(field_name, "")
        values = value if isinstance(value, list) else [value]
        if any(phrase_hit(query, str(item)) for item in values):
            score += weight
            reasons.append(field_name)
    record_terms = set(record.get("terms", []))
    overlap = [term for term in query_terms if term in record_terms]
    if overlap:
        score += min(40, 4 * len(overlap))
        reasons.append("term-overlap:" + ",".join(overlap[:6]))
    return score, reasons


def identity_hit(query: str, value: str, field_name: str) -> bool:
    q = normalize(query)
    v = normalize(value)
    if not q or not v:
        return False
    if field_name == "record_id":
        return q == v
    return phrase_hit(q, v)


def searchable_in_flight(record: dict[str, Any], query: str, include_in_flight: bool) -> bool:
    if record.get("channel") != "in-flight":
        return True
    if include_in_flight:
        return True
    entry = str(record.get("entry", ""))
    return bool(entry and phrase_hit(query, entry))


def record_passes_filters(
    record: dict[str, Any],
    channels: list[str] | None,
    memory_classes: list[str] | None,
    statuses: list[str] | None,
    source_prefixes: list[str] | None,
) -> bool:
    if channels and normalize(str(record.get("channel", ""))) not in {normalize(item) for item in channels}:
        return False
    if memory_classes:
        record_class = normalize(str(record.get("memory_class", "")))
        wanted = [normalize(item) for item in memory_classes]
        if not any(item and item in record_class for item in wanted):
            return False
    if statuses and normalize(str(record.get("status", ""))) not in {normalize(item) for item in statuses}:
        return False
    if source_prefixes:
        source = str(record.get("source_path", "")).replace("\\", "/")
        prefixes = [item.replace("\\", "/").strip("/") for item in source_prefixes if item.strip()]
        if not any(source == prefix or source.startswith(prefix + "/") for prefix in prefixes):
            return False
    return True


def result_from_record(record: dict[str, Any], score: int, reasons: list[str]) -> dict[str, Any]:
    result = {
        "record_id": record["record_id"],
        "score": score,
        "reasons": reasons,
        "record_type": record["record_type"],
        "channel": record["channel"],
        "source_path": record["source_path"],
        "anchor": record["anchor"],
        "line_start": record["line_start"],
        "line_end": record["line_end"],
        "source_sha256": record["source_sha256"],
        "span_sha256": record["span_sha256"],
        "mandatory": record["mandatory"],
        "status": record.get("status", ""),
        "scope": record.get("scope", ""),
        "memory_class": record.get("memory_class", ""),
        "owners": record.get("owners", []),
    }
    if record.get("entry"):
        result["entry"] = record["entry"]
    return result


def fresh_cache(memory_root: Path) -> tuple[dict[str, Any], str]:
    cache = load_cache(memory_root)
    current_hash = current_inventory_hash(memory_root)
    if cache.get("source_inventory_hash") != current_hash:
        raise RuntimeError("derived index is stale; rebuild before querying")
    return cache, current_hash


def query_cache(
    memory_root: Path,
    query: str,
    page_size: int,
    continuation: str | None,
    include_in_flight: bool,
    channels: list[str] | None = None,
    memory_classes: list[str] | None = None,
    statuses: list[str] | None = None,
    source_prefixes: list[str] | None = None,
) -> dict[str, Any]:
    cache, current_hash = fresh_cache(memory_root)
    page_size = max(1, min(page_size, MAX_PAGE_SIZE))
    current_filter_hash = filters_hash(channels, memory_classes, statuses, source_prefixes)
    offset = 0
    if continuation:
        payload = parse_token(continuation)
        if payload.get("v") != 1:
            raise RuntimeError("unsupported continuation token")
        if payload.get("query_hash") != sha256_text(normalize(query)):
            raise RuntimeError("continuation token query mismatch")
        if payload.get("inventory_hash") != current_hash:
            raise RuntimeError("continuation token inventory mismatch")
        if int(payload.get("page_size", page_size)) != page_size:
            raise RuntimeError("continuation token page-size mismatch")
        if payload.get("filter_hash", "") != current_filter_hash:
            raise RuntimeError("continuation token filter mismatch")
        offset = int(payload.get("offset", 0))

    query_terms = terms_for_text(query)
    ordinary_candidates: list[dict[str, Any]] = []
    mandatory_records: list[dict[str, Any]] = []
    in_flight_records: list[dict[str, Any]] = []
    for record in cache.get("records", []):
        if not record_passes_filters(record, channels, memory_classes, statuses, source_prefixes):
            continue
        if not searchable_in_flight(record, query, include_in_flight):
            continue
        score, reasons = score_record(record, query, query_terms)
        if score <= 0:
            continue
        result = result_from_record(record, score, reasons)
        if record.get("channel") == "in-flight":
            in_flight_records.append(result)
        elif record.get("mandatory"):
            mandatory_records.append(result)
        else:
            ordinary_candidates.append(result)

    sort_key = lambda item: (-int(item["score"]), item["record_id"])
    ordinary_candidates.sort(key=sort_key)
    mandatory_records.sort(key=sort_key)
    in_flight_records.sort(key=sort_key)
    page = ordinary_candidates[offset : offset + page_size]
    next_offset = offset + len(page)
    truncated = next_offset < len(ordinary_candidates)
    next_token = (
        token_payload(query, current_hash, page_size, next_offset, current_filter_hash)
        if truncated
        else None
    )
    return {
        "action": "query",
        "cache_fresh": True,
        "engine_version": cache.get("engine_version"),
        "source_inventory_hash": current_hash,
        "query_hash": sha256_text(normalize(query)),
        "page_size": page_size,
        "offset": offset,
        "mandatory_count": len(mandatory_records),
        "in_flight_count": len(in_flight_records),
        "total_candidates": len(ordinary_candidates),
        "returned": len(page),
        "truncated": truncated,
        "continuation_token": next_token,
        "mandatory_records": mandatory_records,
        "ordinary_records": page,
        "in_flight_records": in_flight_records,
        "filters": {
            "channels": channels or [],
            "memory_classes": memory_classes or [],
            "statuses": statuses or [],
            "source_prefixes": source_prefixes or [],
        },
        "no_memory": not mandatory_records and not in_flight_records and not ordinary_candidates,
    }


def anchor_records(cache: dict[str, Any]) -> list[dict[str, Any]]:
    anchors: list[dict[str, Any]] = []
    for record in cache.get("records", []):
        source = str(record.get("source_path", "")).replace("\\", "/")
        if source in {"current-context.md", "active-task.md", "index.md"} or source.endswith("/active-task.md"):
            anchors.append(result_from_record(record, 0, ["live-anchor"]))
    anchors.sort(key=lambda item: (item["source_path"], item["line_start"], item["record_id"]))
    return anchors


def unique_results(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for record in records:
        record_id = record["record_id"]
        if record_id in seen:
            continue
        seen.add(record_id)
        unique.append(record)
    return unique


def recall_cache(
    memory_root: Path,
    topics: list[str],
    limit_per_topic: int,
    include_anchors: bool,
    include_in_flight: bool,
    channels: list[str] | None,
    memory_classes: list[str] | None,
    statuses: list[str] | None,
    source_prefixes: list[str] | None,
) -> dict[str, Any]:
    cache, current_hash = fresh_cache(memory_root)
    per_topic: list[dict[str, Any]] = []
    all_mandatory: list[dict[str, Any]] = []
    all_in_flight: list[dict[str, Any]] = []
    all_ordinary: list[dict[str, Any]] = []
    for topic in topics:
        result = query_cache(
            memory_root,
            topic,
            limit_per_topic,
            None,
            include_in_flight,
            channels,
            memory_classes,
            statuses,
            source_prefixes,
        )
        per_topic.append(
            {
                "topic": topic,
                "query_hash": result["query_hash"],
                "mandatory_records": result["mandatory_records"],
                "ordinary_records": result["ordinary_records"],
                "in_flight_records": result["in_flight_records"],
                "no_memory": result["no_memory"],
            }
        )
        all_mandatory.extend(result["mandatory_records"])
        all_in_flight.extend(result["in_flight_records"])
        all_ordinary.extend(result["ordinary_records"])
    return {
        "action": "recall",
        "cache_fresh": True,
        "engine_version": cache.get("engine_version"),
        "source_inventory_hash": current_hash,
        "topics": topics,
        "limit_per_topic": limit_per_topic,
        "include_anchors": include_anchors,
        "anchor_records": anchor_records(cache) if include_anchors else [],
        "mandatory_records": unique_results(all_mandatory),
        "ordinary_records": unique_results(all_ordinary),
        "in_flight_records": unique_results(all_in_flight),
        "per_topic": per_topic,
        "filters": {
            "channels": channels or [],
            "memory_classes": memory_classes or [],
            "statuses": statuses or [],
            "source_prefixes": source_prefixes or [],
        },
        "no_memory": not all_mandatory and not all_in_flight and not all_ordinary,
    }


def related_records(memory_root: Path, record_id: str, limit: int) -> dict[str, Any]:
    cache, current_hash = fresh_cache(memory_root)
    records = cache.get("records", [])
    target = next((record for record in records if record.get("record_id") == record_id), None)
    if target is None:
        raise RuntimeError(f"record not found: {record_id}")
    target_terms = set(target.get("terms", []))
    target_source = target.get("source_path", "")
    candidates: list[dict[str, Any]] = []
    for record in records:
        if record.get("record_id") == record_id:
            continue
        if record.get("channel") in {"session-log", "cold-log"}:
            continue
        overlap = sorted(target_terms.intersection(set(record.get("terms", []))))
        score = len(overlap) * 4
        if record.get("source_path") == target_source:
            score += 8
        if normalize(str(record.get("scope", ""))) == normalize(str(target.get("scope", ""))):
            score += 12
        if score <= 0:
            continue
        reasons = ["related-term-overlap:" + ",".join(overlap[:6])] if overlap else []
        if record.get("source_path") == target_source:
            reasons.append("same-source")
        if normalize(str(record.get("scope", ""))) == normalize(str(target.get("scope", ""))):
            reasons.append("same-scope")
        candidates.append(result_from_record(record, score, reasons))
    candidates.sort(key=lambda item: (-int(item["score"]), item["record_id"]))
    return {
        "action": "related",
        "cache_fresh": True,
        "engine_version": cache.get("engine_version"),
        "source_inventory_hash": current_hash,
        "record_id": record_id,
        "target": result_from_record(target, 0, ["target"]),
        "returned": min(limit, len(candidates)),
        "related_records": candidates[:limit],
    }


def command_build(args: argparse.Namespace) -> int:
    memory_root = args.memory_root.resolve()
    if not memory_root.is_dir():
        raise RuntimeError(f"memory root does not exist: {memory_root}")
    cache = build_index(memory_root)
    changed, cache_hash = write_cache(memory_root, cache)
    print(
        json.dumps(
            {
                "action": "build",
                "changed": changed,
                "cache_path": CACHE_REL,
                "cache_sha256": cache_hash,
                "source_inventory_hash": cache["source_inventory_hash"],
                "record_set_hash": cache["record_set_hash"],
                "source_entry_count": len(cache["source_entries"]),
                "source_file_count": len(cache["source_files"]),
                "excluded_entry_count": len(cache["excluded_entries"]),
                "record_count": len(cache["records"]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def command_query(args: argparse.Namespace) -> int:
    result = query_cache(
        args.memory_root.resolve(),
        args.query,
        args.page_size,
        args.continuation,
        args.include_in_flight,
        args.channel,
        args.memory_class,
        args.status,
        args.source_prefix,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def command_recall(args: argparse.Namespace) -> int:
    result = recall_cache(
        args.memory_root.resolve(),
        args.topic,
        args.limit_per_topic,
        args.include_anchors,
        args.include_in_flight,
        args.channel,
        args.memory_class,
        args.status,
        args.source_prefix,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def command_related(args: argparse.Namespace) -> int:
    result = related_records(args.memory_root.resolve(), args.record_id, args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def command_stats(args: argparse.Namespace) -> int:
    cache = load_cache(args.memory_root.resolve())
    fresh = cache_is_fresh(args.memory_root.resolve(), cache)
    channels: dict[str, int] = {}
    for record in cache.get("records", []):
        channels[record["channel"]] = channels.get(record["channel"], 0) + 1
    print(
        json.dumps(
            {
                "action": "stats",
                "cache_fresh": fresh,
                "engine_version": cache.get("engine_version"),
                "source_inventory_hash": cache.get("source_inventory_hash"),
                "record_set_hash": cache.get("record_set_hash"),
                "source_file_count": len(cache.get("source_files", [])),
                "record_count": len(cache.get("records", [])),
                "channels": channels,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="Build the derived cache from source memory")
    build.add_argument("memory_root", type=Path, help="Path to docs/codex")
    build.set_defaults(func=command_build)

    query = subparsers.add_parser("query", help="Query the derived cache")
    query.add_argument("memory_root", type=Path, help="Path to docs/codex")
    query.add_argument("--query", required=True, help="Natural language or exact-id query")
    query.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE, help="Ordinary result page size")
    query.add_argument("--continuation", help="Continuation token returned by a previous query")
    query.add_argument("--include-in-flight", action="store_true", help="Include live session-log entries in ordinary recall")
    query.add_argument("--channel", action="append", help="Filter records by channel, repeatable")
    query.add_argument("--memory-class", action="append", help="Filter records by Memory class substring, repeatable")
    query.add_argument("--status", action="append", help="Filter records by exact status, repeatable")
    query.add_argument("--source-prefix", action="append", help="Filter records by source path prefix, repeatable")
    query.set_defaults(func=command_query)

    recall = subparsers.add_parser("recall", help="Run multi-topic pointer recall")
    recall.add_argument("memory_root", type=Path, help="Path to docs/codex")
    recall.add_argument("--topic", action="append", required=True, help="Topic to recall, repeatable")
    recall.add_argument("--limit-per-topic", type=int, default=5, help="Ordinary result page size per topic")
    recall.add_argument("--include-anchors", action="store_true", help="Return current-context, active-task, and index pointers")
    recall.add_argument("--include-in-flight", action="store_true", help="Include live session-log entries in ordinary recall")
    recall.add_argument("--channel", action="append", help="Filter records by channel, repeatable")
    recall.add_argument("--memory-class", action="append", help="Filter records by Memory class substring, repeatable")
    recall.add_argument("--status", action="append", help="Filter records by exact status, repeatable")
    recall.add_argument("--source-prefix", action="append", help="Filter records by source path prefix, repeatable")
    recall.set_defaults(func=command_recall)

    related = subparsers.add_parser("related", help="Find lexical neighbor pointers for one derived record")
    related.add_argument("memory_root", type=Path, help="Path to docs/codex")
    related.add_argument("--record-id", required=True, help="Record ID returned by query/recall")
    related.add_argument("--limit", type=int, default=5, help="Maximum related records to return")
    related.set_defaults(func=command_related)

    stats = subparsers.add_parser("stats", help="Inspect derived cache freshness and counts")
    stats.add_argument("memory_root", type=Path, help="Path to docs/codex")
    stats.set_defaults(func=command_stats)

    args = parser.parse_args()
    try:
        return args.func(args)
    except Exception as exc:
        print(
            json.dumps(
                {"action": args.command, "ok": False, "error": str(exc)},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
