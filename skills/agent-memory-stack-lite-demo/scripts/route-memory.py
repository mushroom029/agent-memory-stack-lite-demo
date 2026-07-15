#!/usr/bin/env python3
"""Resolve strongly relevant Lite Demo owners through one layered route level."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path


ROUTE_LINE_RE = re.compile(r"^\s*-\s*([^:]+):\s*(.+)$")
FIELD_RE = re.compile(r"(?:^|;)\s*([a-z][a-z0-9_-]*)\s*=\s*([^;]*)", re.I)
VALUE_SPLIT_RE = re.compile(r"\s*[,|，]\s*")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
ASCII_ALNUM_RE = re.compile(r"[A-Za-z0-9]")
PRIMARY_FANOUT_WARNING = 8
SELECTED_BYTES_WARNING = 64 * 1024


@dataclass(frozen=True)
class Route:
    scope: str
    aliases: tuple[str, ...]
    keywords: tuple[str, ...]
    owners: tuple[str, ...]
    mandatory: tuple[str, ...]
    history: tuple[str, ...]
    reason: str
    line: int
    source: Path


@dataclass(frozen=True)
class Match:
    route: Route
    direct_hits: tuple[str, ...]
    keyword_hits: tuple[str, ...]


def clean(value: str) -> str:
    return value.strip().strip("`\"'")


def normalize(value: str) -> str:
    return unicodedata.normalize("NFKC", clean(value)).casefold()


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
                history=pointers(fields.get("history", "")),
                reason=fields.get("reason", "").strip(),
                line=line_number,
                source=index_path,
            )
        )
    return routes


def ascii_boundary_match(term: str, touch: str) -> bool:
    left = r"(?<![A-Za-z0-9])" if term and ASCII_ALNUM_RE.match(term[0]) else ""
    right = r"(?![A-Za-z0-9])" if term and ASCII_ALNUM_RE.match(term[-1]) else ""
    return re.search(left + re.escape(term) + right, touch, re.I) is not None


def phrase_match(candidate: str, touch: str, allow_short_cjk: bool = False) -> bool:
    term = normalize(candidate)
    text = normalize(touch)
    if not term:
        return False
    if term == text:
        return True
    if term.isascii():
        return ascii_boundary_match(term, text)
    cjk_length = len(CJK_RE.findall(term))
    if cjk_length and (cjk_length >= 4 or allow_short_cjk):
        return term in text
    if ASCII_ALNUM_RE.search(term):
        return ascii_boundary_match(term, text)
    return False


def evaluate(route: Route, touches: list[str]) -> Match | None:
    direct_hits = tuple(
        term
        for term in (route.scope, *route.aliases)
        if any(phrase_match(term, touch) for touch in touches)
    )
    keyword_hits = tuple(
        term
        for term in route.keywords
        if any(phrase_match(term, touch, allow_short_cjk=True) for touch in touches)
    )
    atomic_keyword_hit = any(
        normalize(keyword) == normalize(touch)
        for keyword in route.keywords
        for touch in touches
    )
    if direct_hits or atomic_keyword_hit or len({normalize(hit) for hit in keyword_hits}) >= 2:
        return Match(route, direct_hits, keyword_hits)
    return None


def owner_path(memory_root: Path, pointer: str) -> Path:
    relative = clean(pointer).split("#", 1)[0]
    return (memory_root / relative).resolve()


def history_path(memory_root: Path, pointer: str) -> tuple[Path | None, str | None]:
    path = owner_path(memory_root, pointer)
    routes_root = (memory_root / "routes").resolve()
    try:
        path.relative_to(routes_root)
    except ValueError:
        return None, f"history route must stay under routes/: {pointer}"
    if not path.is_file():
        return None, f"history route does not exist: {pointer}"
    return path, None


def route_to_dict(match: Match, memory_root: Path, tier: str) -> dict[str, object]:
    route = match.route
    selected = list(dict.fromkeys((*route.mandatory, *route.owners)))
    return {
        "scope": route.scope,
        "tier": tier,
        "source": str(route.source.relative_to(memory_root)),
        "aliases": list(route.aliases),
        "keywords": list(route.keywords),
        "owners": list(route.owners),
        "mandatory": list(route.mandatory),
        "history": list(route.history),
        "reason": route.reason,
        "index_line": route.line,
        "direct_hits": list(match.direct_hits),
        "keyword_hits": list(match.keyword_hits),
        "missing_owners": [
            pointer for pointer in selected if not owner_path(memory_root, pointer).is_file()
        ],
    }


def unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))


def source_bytes(memory_root: Path, pointers_to_read: list[str]) -> int:
    total = 0
    seen: set[Path] = set()
    for pointer in pointers_to_read:
        path = owner_path(memory_root, pointer)
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        total += path.stat().st_size
    return total


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
    primary_matches = [match for route in routes if (match := evaluate(route, args.touch))]
    primary_owners = unique(
        [pointer for match in primary_matches for pointer in match.route.owners]
    )
    mandatory = unique(
        [pointer for match in primary_matches for pointer in match.route.mandatory]
    )

    historical_matches: list[Match] = []
    history_route_files: list[str] = []
    history_route_errors: list[str] = []
    deferred_history_route_count = 0
    weak_candidates: list[dict[str, object]] = []

    matched_scopes = {match.route.scope for match in primary_matches}
    for route in routes:
        if route.scope in matched_scopes:
            continue
        keyword_hits = [
            term
            for term in route.keywords
            if any(phrase_match(term, touch, allow_short_cjk=True) for touch in args.touch)
        ]
        if keyword_hits:
            weak_candidates.append(
                {"scope": route.scope, "source": "index.md", "keyword_hits": keyword_hits}
            )

    for match in primary_matches:
        for pointer in match.route.history:
            route_file, error = history_path(memory_root, pointer)
            if error:
                history_route_errors.append(error)
                continue
            assert route_file is not None
            relative_route_file = str(route_file.relative_to(memory_root))
            history_route_files.append(relative_route_file)
            child_routes = parse_routes(route_file)
            for child in child_routes:
                if child.history:
                    history_route_errors.append(
                        f"history route nesting exceeds one level: {relative_route_file}:{child.line}"
                    )
                    continue
                child_match = evaluate(child, args.touch)
                if child_match:
                    historical_matches.append(child_match)
                else:
                    deferred_history_route_count += 1
                    keyword_hits = [
                        term
                        for term in child.keywords
                        if any(
                            phrase_match(term, touch, allow_short_cjk=True)
                            for touch in args.touch
                        )
                    ]
                    if keyword_hits:
                        weak_candidates.append(
                            {
                                "scope": child.scope,
                                "source": relative_route_file,
                                "keyword_hits": keyword_hits,
                            }
                        )

    historical_owners = unique(
        [pointer for match in historical_matches for pointer in match.route.owners]
    )
    mandatory = unique(
        mandatory
        + [pointer for match in historical_matches for pointer in match.route.mandatory]
    )
    owners = unique(primary_owners + historical_owners)

    alias_hits: dict[str, list[str]] = {}
    for match in (*primary_matches, *historical_matches):
        for alias in match.route.aliases:
            if any(phrase_match(alias, touch) for touch in args.touch):
                alias_hits.setdefault(normalize(alias), []).append(match.route.scope)
    ambiguous_aliases = {
        alias: scopes for alias, scopes in alias_hits.items() if len(set(scopes)) > 1
    }

    escalation_reasons: list[str] = []
    if not primary_matches:
        escalation_reasons.append("no-route-match")
    if ambiguous_aliases:
        escalation_reasons.append("alias-ambiguity")
    if history_route_errors:
        escalation_reasons.append("history-route-error")
    if args.first_touch:
        escalation_reasons.append("first-entity-touch")
    if args.risk == "irreversible":
        escalation_reasons.append("irreversible-action")

    selected_bytes = source_bytes(memory_root, unique(owners + mandatory))
    health_warnings: list[str] = []
    if len(primary_owners) > PRIMARY_FANOUT_WARNING:
        health_warnings.append("primary-owner-fanout")
    if selected_bytes > SELECTED_BYTES_WARNING:
        health_warnings.append("large-selected-source")

    result = {
        "touches": args.touch,
        "matched_route_count": len(primary_matches) + len(historical_matches),
        "matched_routes": [
            *[route_to_dict(match, memory_root, "primary") for match in primary_matches],
            *[route_to_dict(match, memory_root, "history") for match in historical_matches],
        ],
        "owners": owners,
        "primary_owners": primary_owners,
        "historical_owners": historical_owners,
        "mandatory_owners": mandatory,
        "selected_source_bytes": selected_bytes,
        "history_route_files": unique(history_route_files),
        "deferred_history_route_count": deferred_history_route_count,
        "unrelated_route_count": len(routes) - len(primary_matches),
        "weak_candidates": weak_candidates,
        "health_warnings": health_warnings,
        "history_route_errors": history_route_errors,
        "ambiguous_aliases": ambiguous_aliases,
        "escalation_required": bool(escalation_reasons),
        "escalation_reasons": escalation_reasons,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
