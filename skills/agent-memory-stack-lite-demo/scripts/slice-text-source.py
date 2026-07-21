#!/usr/bin/env python3
"""Slice a long local text source into bounded chapter artifacts and a manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_HEADING_RE = (
    r"(?m)^[ \t\u3000]*(?P<title>"
    r"(?:第[零〇一二两三四五六七八九十百千万0-9０-９]+章|"
    r"Chapter[ \t]+[0-9]+|CH[0-9]+)"
    r"(?:[ \t\u3000:：\-—.．][^\r\n]*)?)[ \t\u3000]*\r?$"
)
AUTO_ENCODINGS = ("utf-8-sig", "utf-8", "gb18030")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def read_source(path: Path, encoding: str) -> tuple[str, bytes, str]:
    raw = path.read_bytes()
    if encoding != "auto":
        return raw.decode(encoding), raw, encoding
    errors: list[str] = []
    for candidate in AUTO_ENCODINGS:
        try:
            return raw.decode(candidate), raw, candidate
        except UnicodeDecodeError as exc:
            errors.append(f"{candidate}: {exc}")
    raise UnicodeDecodeError("auto", raw, 0, 1, "; ".join(errors))


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def write_text_exact(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def find_chapters(text: str, heading_regex: str) -> list[dict[str, Any]]:
    pattern = re.compile(heading_regex)
    matches = list(pattern.finditer(text))
    chapters: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        title = (match.groupdict().get("title") or match.group(0)).strip()
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end]
        chapters.append(
            {
                "ordinal": index + 1,
                "heading": title,
                "char_start": start,
                "char_end": end,
                "line_start": line_number(text, start),
                "line_end": line_number(text, max(start, end - 1)),
                "text": body,
            }
        )
    return chapters


def select_chapters(chapters: list[dict[str, Any]], start_chapter: int, max_chapters: int) -> list[dict[str, Any]]:
    if start_chapter < 1:
        raise ValueError("--start-chapter must be >= 1")
    if max_chapters < 1:
        raise ValueError("--max-chapters must be >= 1")
    start_index = start_chapter - 1
    return chapters[start_index : start_index + max_chapters]


def make_index_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Text Source Slice Index",
        "",
        f"- Source: `{manifest['source_path']}`",
        f"- Source SHA256: `{manifest['source_sha256']}`",
        f"- Encoding: `{manifest['encoding']}`",
        f"- Total chapters found: {manifest['total_chapters_found']}",
        f"- Selected chapters: {manifest['selected_count']}",
        "",
        "## Chapters",
        "",
    ]
    for chapter in manifest["chapters"]:
        lines.append(
            "- {ordinal:03d}: {heading}; lines={line_start}-{line_end}; "
            "chars={chars}; sha256={sha}; file={path}".format(
                ordinal=chapter["ordinal"],
                heading=chapter["heading"],
                line_start=chapter["line_start"],
                line_end=chapter["line_end"],
                chars=chapter["chars"],
                sha=chapter["sha256"],
                path=chapter["relative_path"],
            )
        )
    lines.append("")
    return "\n".join(lines)


def build_manifest(
    source: Path,
    out_dir: Path,
    encoding: str,
    raw: bytes,
    heading_regex: str,
    chapters: list[dict[str, Any]],
    selected: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tool": "slice-text-source.py",
        "source_path": str(source),
        "source_sha256": sha256_bytes(raw),
        "source_size_bytes": len(raw),
        "encoding": encoding,
        "heading_regex": heading_regex,
        "total_chapters_found": len(chapters),
        "selected_count": len(selected),
        "output_dir": str(out_dir),
        "chapters": [],
        "warnings": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Long local text source to slice")
    parser.add_argument("--out-dir", type=Path, required=True, help="Directory for slice artifacts")
    parser.add_argument("--start-chapter", type=int, default=1, help="1-based chapter ordinal to start from")
    parser.add_argument("--max-chapters", type=int, default=20, help="Maximum number of chapters to write")
    parser.add_argument("--encoding", default="auto", help="Input encoding, or auto")
    parser.add_argument("--heading-regex", default=DEFAULT_HEADING_RE, help="Python regex for chapter headings")
    parser.add_argument("--manifest-name", default="manifest.json")
    parser.add_argument("--index-name", default="chapters-index.md")
    parser.add_argument("--min-found", type=int, default=1, help="Minimum detected chapter headings required")
    args = parser.parse_args()

    source = args.source.resolve()
    out_dir = args.out_dir.resolve()
    if not source.is_file():
        parser.error(f"source file does not exist: {source}")
    if args.manifest_name in {"", ".", ".."} or Path(args.manifest_name).name != args.manifest_name:
        parser.error("--manifest-name must be a simple file name")
    if args.index_name in {"", ".", ".."} or Path(args.index_name).name != args.index_name:
        parser.error("--index-name must be a simple file name")

    try:
        text, raw, used_encoding = read_source(source, args.encoding)
        chapters = find_chapters(text, args.heading_regex)
        selected = select_chapters(chapters, args.start_chapter, args.max_chapters)
    except (UnicodeDecodeError, re.error, ValueError) as exc:
        parser.error(str(exc))

    if len(chapters) < args.min_found:
        parser.error(f"found {len(chapters)} chapter headings, below --min-found {args.min_found}")
    if not selected:
        parser.error("selected chapter range is empty")

    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest(source, out_dir, used_encoding, raw, args.heading_regex, chapters, selected)
    if len(selected) < args.max_chapters:
        manifest["warnings"].append(
            f"selected only {len(selected)} chapters; requested {args.max_chapters}"
        )

    chapter_dir = out_dir / "chapters"
    chapter_dir.mkdir(parents=True, exist_ok=True)
    for chapter in selected:
        file_name = f"chapter-{chapter['ordinal']:03d}.txt"
        rel_path = str(Path("chapters") / file_name).replace("\\", "/")
        body = chapter["text"]
        target = chapter_dir / file_name
        write_text_exact(target, body)
        encoded = body.encode("utf-8")
        manifest["chapters"].append(
            {
                "ordinal": chapter["ordinal"],
                "heading": chapter["heading"],
                "relative_path": rel_path,
                "line_start": chapter["line_start"],
                "line_end": chapter["line_end"],
                "char_start": chapter["char_start"],
                "char_end": chapter["char_end"],
                "chars": len(body),
                "bytes_utf8": len(encoded),
                "sha256": sha256_bytes(encoded),
            }
        )

    manifest_path = out_dir / args.manifest_name
    index_path = out_dir / args.index_name
    write_text_exact(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    write_text_exact(index_path, make_index_markdown(manifest))

    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not manifest["warnings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
