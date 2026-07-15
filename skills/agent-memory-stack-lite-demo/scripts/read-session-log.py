#!/usr/bin/env python3
"""Read a bounded recovery view from an append-only Lite Demo session log."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_TAIL_LINES = 60


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def tail_lines(lines: list[str], count: int = DEFAULT_TAIL_LINES) -> list[str]:
    if count < 1:
        raise ValueError("tail line count must be positive")
    return lines[-count:]


def search_lines(
    lines: list[str], term: str, context: int = 2, match_limit: int = 5
) -> list[str]:
    if not term:
        raise ValueError("search term must not be empty")
    if context < 0 or match_limit < 1:
        raise ValueError("context must be non-negative and match limit positive")

    hits = [i for i, line in enumerate(lines) if term.casefold() in line.casefold()]
    selected: set[int] = set()
    for index in hits[:match_limit]:
        start = index - context
        if start < 0:
            start = 0
        selected.update(range(start, min(len(lines), index + context + 1)))
    return [f"{index + 1}: {lines[index]}" for index in sorted(selected)]


def range_lines(lines: list[str], start: int, end: int) -> list[str]:
    if start < 1 or end < start:
        raise ValueError("line range must satisfy 1 <= start <= end")
    upper = min(end, len(lines))
    return [f"{index + 1}: {lines[index]}" for index in range(start - 1, upper)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path, help="Path to session-log.md")
    parser.add_argument("--tail-lines", type=int, default=DEFAULT_TAIL_LINES)
    parser.add_argument("--search", help="Literal case-insensitive targeted search")
    parser.add_argument("--context", type=int, default=2)
    parser.add_argument("--match-limit", type=int, default=5)
    parser.add_argument("--start-line", type=int)
    parser.add_argument("--end-line", type=int)
    args = parser.parse_args()

    if not args.log.is_file():
        parser.error(f"session log does not exist: {args.log}")
    if (args.start_line is None) != (args.end_line is None):
        parser.error("--start-line and --end-line must be used together")
    if args.search and args.start_line is not None:
        parser.error("choose either --search or a line range")

    lines = read_lines(args.log)
    try:
        if args.search:
            selected = search_lines(lines, args.search, args.context, args.match_limit)
        elif args.start_line is not None:
            selected = range_lines(lines, args.start_line, args.end_line)
        else:
            selected = tail_lines(lines, args.tail_lines)
    except ValueError as exc:
        parser.error(str(exc))

    if selected:
        sys.stdout.write("\n".join(selected) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
