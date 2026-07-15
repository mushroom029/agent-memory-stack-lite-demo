#!/usr/bin/env python3
"""Resolve every strongly relevant Lite Demo memory owner from index.md."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


ROUTE_LINE_RE = re.compile(r"^\s*-\s*([^:]+):\s*(.+)$")
FIELD_RE = re.compile(r"(?:^|;)\s*([a-z][a-z0-9_-]*)\s*=\s*([^;]*)", re.I)
VALUE_SPLIT_RE = re.compile(r"\s*[,|，]\s*")


@dataclass(frozen=True)
class Route:
    scope: str
    aliases: tuple[str, ...]
    keywords: tuple[str, ...]
    owners: tuple[str, ...]
    mandatory: tuple[str, ...]
    reason: str
    line: int


def clean(value: str) -> str:
    return value.strip().strip("`\"'")


def values(value: str) -> tuple[str, ...]:
    return tuple(clean(item) for item in VALUE_SPLIT_RE.split(value) if clean(item))


def pointers(value: str) -> tuple[str, ...]:
    return tuple(
        item for item in values(value) if item.casefold() not in {"none", "n/a", "-"}
    )


def parse_routes(index_path: Path) -> list[Route]:
    routes: list[Route] = []
    for line_number, line in enumerate(index_path.read_text(encoding="utf-8").splitlines(), 1):
        match = ROUTE_LINE_RE.match(line)
        if not match or "owners=" not in line.casefold():
            continue
        fields = {key.casefold(): value.strip() for key, value in FIELD_RE.findall(match.group(2))}
        owners = pointers(fields.get("owners", ""))
        if not owners:
            continue
        routes.append(
            Route(
                scope=clean(match.group(1)),
                aliases=values(fields.get("aliases", "")),
                keywords=values(fields.get("keywords", "")),
                owners=owners,
                mandatory=pointers(fields.get("mandatory", "")),
                reason=fields.get("reason", "").strip(),
                line=line_number,
            )
        )
    return routes


def strong_match(candidate: str, touches: list[str]) -> bool:
    candidate_folded = clean(candidate).casefold()
    if not candidate_folded:
        return False
    for touch in touches:
        touch_folded = touch.casefold().strip()
        if candidate_folded == touch_folded:
            return True
        if len(candidate_folded) >= 2 and candidate_folded in touch_folded:
            return True
        if len(touch_folded) >= 3 and touch_folded in candidate_folded:
            return True
    return False


def owner_path(memory_root: Path, pointer: str) -> Path:
    relative = clean(pointer).split("#", 1)[0]
    return (memory_root / relative).resolve()


def route_to_dict(route: Route, memory_root: Path) -> dict[str, object]:
    pointers = list(dict.fromkeys((*route.mandatory, *route.owners)))
    return {
        "scope": route.scope,
        "aliases": list(route.aliases),
        "keywords": list(route.keywords),
        "owners": list(route.owners),
        "mandatory": list(route.mandatory),
        "reason": route.reason,
        "index_line": route.line,
        "missing_owners": [
            pointer for pointer in pointers if not owner_path(memory_root, pointer).is_file()
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("memory_root", type=Path, help="Path to docs/codex")
    parser.add_argument(
        "--touch",
        action="append",
        required=True,
        help="Touched module, entity, behavior, version, risk, or natural-language action",
    )
    parser.add_argument(
        "--risk",
        choices=("normal", "irreversible"),
        default="normal",
        help="Irreversible actions require an explicit wider-retrieval check",
    )
    parser.add_argument(
        "--first-touch",
        action="store_true",
        help="Flag first-time entity touch for wider retrieval",
    )
    args = parser.parse_args()

    memory_root = args.memory_root.resolve()
    index_path = memory_root / "index.md"
    if not index_path.is_file():
        parser.error(f"index does not exist: {index_path}")

    routes = parse_routes(index_path)
    matched = [
        route
        for route in routes
        if any(strong_match(term, args.touch) for term in (route.scope, *route.aliases, *route.keywords))
    ]

    owners = list(dict.fromkeys(pointer for route in matched for pointer in route.owners))
    mandatory = list(
        dict.fromkeys(pointer for route in matched for pointer in route.mandatory)
    )

    alias_hits: dict[str, list[str]] = {}
    for route in matched:
        for alias in route.aliases:
            if strong_match(alias, args.touch):
                alias_hits.setdefault(alias.casefold(), []).append(route.scope)
    ambiguous_aliases = {
        alias: scopes for alias, scopes in alias_hits.items() if len(set(scopes)) > 1
    }

    escalation_reasons: list[str] = []
    if not matched:
        escalation_reasons.append("no-route-match")
    if ambiguous_aliases:
        escalation_reasons.append("alias-ambiguity")
    if args.first_touch:
        escalation_reasons.append("first-entity-touch")
    if args.risk == "irreversible":
        escalation_reasons.append("irreversible-action")

    result = {
        "touches": args.touch,
        "matched_route_count": len(matched),
        "matched_routes": [route_to_dict(route, memory_root) for route in matched],
        "owners": owners,
        "mandatory_owners": mandatory,
        "unrelated_route_count": len(routes) - len(matched),
        "ambiguous_aliases": ambiguous_aliases,
        "escalation_required": bool(escalation_reasons),
        "escalation_reasons": escalation_reasons,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
