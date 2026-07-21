#!/usr/bin/env python3
"""Validate large local text intake artifacts and Lite Demo memory landing."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


MEMORY_FILE_SUFFIXES = {".md", ".txt", ".json"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def load_json(path: Path, errors: list[str]) -> dict:
    if not path.is_file():
        errors.append(f"missing JSON artifact: {path}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        errors.append(f"unreadable JSON artifact: {path}: {exc}")
        return {}


def read_text(path: Path, errors: list[str]) -> str:
    if not path.is_file():
        errors.append(f"missing artifact: {path}")
        return ""
    try:
        return path.read_text(encoding="utf-8-sig")
    except Exception as exc:
        errors.append(f"unreadable artifact: {path}: {exc}")
        return ""


def line_count(text: str) -> int:
    if not text:
        return 0
    return len(text.splitlines())


def memory_files(memory_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in memory_root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(memory_root).as_posix()
        if rel.startswith(".lite-demo-cache/"):
            continue
        if path.suffix.lower() in MEMORY_FILE_SUFFIXES or path.name.startswith(".takeover"):
            files.append(path)
    return files


def collect_source_fragments(chapter_paths: list[Path], max_fragments: int = 120) -> list[str]:
    fragments: list[str] = []
    for chapter_path in chapter_paths:
        try:
            text = chapter_path.read_text(encoding="utf-8-sig")
        except Exception:
            continue
        for line in text.splitlines():
            stripped = line.strip()
            if len(stripped) < 40:
                continue
            if stripped.startswith("第") and "章" in stripped[:12]:
                continue
            fragments.append(stripped[:180])
            if len(fragments) >= max_fragments:
                return fragments
    return fragments


def check_manifest(replay_root: Path, expected_chapters: int, errors: list[str]) -> tuple[dict, list[Path]]:
    slices_root = replay_root / "artifacts" / "source-slices"
    manifest = load_json(slices_root / "manifest.json", errors)
    read_text(slices_root / "chapters-index.md", errors)
    chapter_paths: list[Path] = []
    if not manifest:
        return manifest, chapter_paths
    if manifest.get("selected_count", 0) < expected_chapters:
        errors.append(
            f"manifest selected_count must be >= {expected_chapters}, got {manifest.get('selected_count')!r}"
        )
    if not manifest.get("source_sha256"):
        errors.append("manifest missing source_sha256")
    chapters = manifest.get("chapters")
    if not isinstance(chapters, list) or len(chapters) < expected_chapters:
        errors.append(f"manifest chapters must contain at least {expected_chapters} entries")
        chapters = chapters if isinstance(chapters, list) else []
    for chapter in chapters[:expected_chapters]:
        rel = chapter.get("relative_path")
        if not rel:
            errors.append("chapter manifest entry missing relative_path")
            continue
        chapter_path = slices_root / rel
        chapter_paths.append(chapter_path)
        if not chapter_path.is_file():
            errors.append(f"missing chapter slice: {chapter_path}")
            continue
        data = chapter_path.read_bytes()
        if chapter.get("sha256") and sha256_bytes(data) != chapter.get("sha256"):
            errors.append(f"chapter slice hash mismatch: {rel}")
    return manifest, chapter_paths


def check_memory_landing(
    replay_root: Path,
    expected_chapters: int,
    required_topics: list[str],
    chapter_paths: list[Path],
    errors: list[str],
    warnings: list[str],
) -> None:
    memory_root = replay_root / "docs" / "codex"
    if not memory_root.is_dir():
        errors.append(f"missing memory root: {memory_root}")
        return

    current_context = read_text(memory_root / "current-context.md", errors)
    index_text = read_text(memory_root / "index.md", errors)
    session_log = read_text(memory_root / "session-log.md", errors)
    active_task = read_text(memory_root / "active-task.md", errors)

    if not active_task:
        errors.append("large text intake must create active-task.md; slicing alone is not completion")
    if len(current_context) > 6000:
        errors.append(f"current-context.md too large: {len(current_context)} bytes/chars")
    if len(index_text) > 18000:
        errors.append(f"index.md too large: {len(index_text)} bytes/chars")
    if len(active_task) > 16000:
        errors.append(f"active-task.md too large: {len(active_task)} bytes/chars")
    if len(session_log.encode("utf-8")) > 12000 or line_count(session_log) > 80:
        errors.append("session-log.md is not sparse after large text intake")

    capsules_dir = memory_root / "capsules"
    capsule_files = sorted(capsules_dir.glob("*.md")) if capsules_dir.is_dir() else []
    if not capsule_files:
        errors.append("no capsule owner was written for large text understanding")

    owner_text = "\n".join(read_text(path, errors) for path in capsule_files)
    combined_routes = index_text + "\n" + owner_text + "\n" + active_task

    if "source-slices" not in combined_routes and "manifest.json" not in combined_routes:
        errors.append("memory owners/routes do not point to source-slice evidence")
    if str(expected_chapters) not in combined_routes and "20" not in combined_routes:
        warnings.append("chapter count is not visibly recorded in memory owners/routes")
    for topic in required_topics:
        if topic and topic not in combined_routes:
            errors.append(f"required topic is not routed or owned: {topic}")

    fragments = collect_source_fragments(chapter_paths)
    if not fragments:
        warnings.append("no long source fragments were available for leak detection")
    memory_texts = []
    for path in memory_files(memory_root):
        try:
            rel = path.relative_to(memory_root).as_posix()
            memory_texts.append((rel, path.read_text(encoding="utf-8-sig")))
        except Exception as exc:
            errors.append(f"unreadable memory file for leak scan: {path}: {exc}")
    for fragment in fragments:
        for rel, text in memory_texts:
            if fragment in text:
                errors.append(f"raw source body fragment leaked into memory file: {rel}")
                return


def check_derived_cache(replay_root: Path, errors: list[str]) -> None:
    cache = load_json(replay_root / "docs" / "codex" / ".lite-demo-cache" / "v1" / "derived-index.json", errors)
    if not cache:
        return
    records = cache.get("records")
    if not isinstance(records, list) or not records:
        errors.append("derived cache has no pointer records")
        return
    forbidden_keys = {"body", "text", "content", "full_text", "raw_body", "source_body"}
    found = sorted({key for rec in records if isinstance(rec, dict) for key in rec if key in forbidden_keys})
    if found:
        errors.append(f"derived cache stores body-like fields: {found}")


def check_delivery(replay_root: Path, expected_chapters: int, errors: list[str]) -> None:
    result = load_json(replay_root / "result.json", errors)
    read_text(replay_root / "DELIVERY.md", errors)
    read_text(replay_root / "SUBAGENT-TRACE.md", errors)
    if not result:
        return
    if result.get("pass") is not True or str(result.get("status", "")).lower() != "pass":
        errors.append("result.json must report pass=true and status=pass")
    if result.get("gaps") not in ([], None):
        errors.append(f"result.json gaps is not empty: {result.get('gaps')!r}")
    if result.get("selected_chapter_count", 0) < expected_chapters:
        errors.append(
            f"result.json selected_chapter_count must be >= {expected_chapters}, got {result.get('selected_chapter_count')!r}"
        )
    for field in (
        "controller_intervention_required",
        "post_hoc_artifact_repair",
        "missing_artifacts_repaired_after_prompt",
    ):
        if result.get(field) is not False:
            errors.append(f"result.json must set {field}=false")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("replay_root")
    parser.add_argument("--expected-chapters", type=int, default=20)
    parser.add_argument("--required-topic", action="append", default=[])
    args = parser.parse_args()

    replay_root = Path(args.replay_root)
    errors: list[str] = []
    warnings: list[str] = []
    if not replay_root.is_dir():
        print(json.dumps({"ok": False, "errors": [f"not a directory: {replay_root}"]}, ensure_ascii=False, indent=2))
        return 1

    manifest, chapter_paths = check_manifest(replay_root, args.expected_chapters, errors)
    check_memory_landing(replay_root, args.expected_chapters, args.required_topic, chapter_paths, errors, warnings)
    check_derived_cache(replay_root, errors)
    check_delivery(replay_root, args.expected_chapters, errors)

    payload = {
        "ok": not errors,
        "replay_root": str(replay_root),
        "expected_chapters": args.expected_chapters,
        "selected_count": manifest.get("selected_count") if manifest else None,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
