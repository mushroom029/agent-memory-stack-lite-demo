#!/usr/bin/env python3
"""Validate Lite Demo pressure-replay closeout artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


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


def round_id_from(value) -> str | None:
    if isinstance(value, int):
        return f"{value:02d}"
    if isinstance(value, str):
        stripped = value.strip()
        return stripped.zfill(2) if stripped.isdigit() else stripped
    return None


def round_states_from(state: dict) -> dict[str, dict]:
    if not isinstance(state, dict):
        return {}
    by_id: dict[str, dict] = {}
    value = state.get("rounds")
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                round_id = (
                    round_id_from(item.get("round"))
                    or round_id_from(item.get("id"))
                    or round_id_from(item.get("round_id"))
                )
                if round_id:
                    by_id[round_id] = item
            else:
                round_id = round_id_from(item)
                if round_id:
                    by_id[round_id] = {}
    return by_id


def rounds_from(value) -> list[str]:
    if not isinstance(value, list):
        return []
    rounds: list[str] = []
    for item in value:
        if isinstance(item, dict):
            round_id = (
                round_id_from(item.get("round"))
                or round_id_from(item.get("id"))
                or round_id_from(item.get("round_id"))
            )
            if round_id:
                rounds.append(round_id)
        else:
            round_id = round_id_from(item)
            if round_id:
                rounds.append(round_id)
    return rounds


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("replay_root", help="subagent replay workspace")
    parser.add_argument("--expected-rounds", type=int, default=20)
    args = parser.parse_args()

    root = Path(args.replay_root)
    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        print(json.dumps({"ok": False, "errors": [f"not a directory: {root}"]}, ensure_ascii=False, indent=2))
        return 1

    result = load_json(root / "result.json", errors)
    state = load_json(root / "state.json", errors)
    delivery = read_text(root / "DELIVERY.md", errors)
    trace = read_text(root / "SUBAGENT-TRACE.md", errors)

    if result:
        if result.get("pass") is not True or str(result.get("status", "")).lower() != "pass":
            errors.append("result.json must explicitly report pass=true and status=pass")
        if result.get("gaps") not in ([], None):
            errors.append(f"result.json gaps is not empty: {result.get('gaps')!r}")
        if str(result.get("status", "")).lower() == "completed_with_gaps":
            errors.append("result.json reports completed_with_gaps")
        for field in (
            "controller_intervention_required",
            "post_hoc_artifact_repair",
            "missing_artifacts_repaired_after_prompt",
        ):
            if result.get(field) is not False:
                errors.append(f"result.json must set {field}=false")
        if result.get("round_count") != args.expected_rounds:
            errors.append(f"result.json round_count must be {args.expected_rounds}, got {result.get('round_count')!r}")
        final_artifacts = result.get("final_artifacts")
        required_artifacts = (
            "delivery",
            "trace",
            "result",
            "state",
            "runtime_replay_check",
        )
        if not isinstance(final_artifacts, dict):
            errors.append("result.json must include final_artifacts with delivery, trace, result, state, and runtime_replay_check paths")
        else:
            for field in required_artifacts:
                value = final_artifacts.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"result.json final_artifacts.{field} must be a non-empty path")
                    continue
                artifact_path = root / value
                if not artifact_path.is_file():
                    errors.append(f"result.json final_artifacts.{field} path does not exist: {value}")

    expected = [f"{i:02d}" for i in range(1, args.expected_rounds + 1)]
    list_round_states = round_states_from(state) if isinstance(state, dict) else {}
    state_rounds = rounds_from(state.get("rounds")) if isinstance(state, dict) else []
    if state_rounds != expected:
        errors.append(f"state.json rounds must be exactly {expected}, got {state_rounds}")

    for round_id in expected:
        round_state = state.get(f"round_{round_id}", {}) if isinstance(state, dict) else {}
        if not isinstance(round_state, dict) or not round_state:
            round_state = list_round_states.get(round_id, {})
        transcript = (
            round_state.get("round_path")
            or round_state.get("artifact")
            or f"rounds/ROUND-{round_id}.md"
            if isinstance(round_state, dict)
            else f"rounds/ROUND-{round_id}.md"
        )
        if not (root / str(transcript)).is_file():
            errors.append(f"missing round transcript: {transcript}")

        if not isinstance(round_state, dict) or not round_state:
            errors.append(f"state.json missing round_{round_id}")
            continue
        if round_state.get("pass") is False:
            errors.append(f"state.json round_{round_id} reports pass=false")

        validation = round_state.get("validation_summary") or round_state.get("summary_path")
        if round_id not in {"01", "02"}:
            if not validation:
                errors.append(f"state.json round_{round_id} missing validation_summary")
            else:
                summary = load_json(root / validation, errors)
                if summary.get("pass") is False:
                    errors.append(f"round {round_id} validation summary reports pass=false")
                if summary.get("gaps") not in ([], None):
                    errors.append(f"round {round_id} validation summary gaps is not empty: {summary.get('gaps')!r}")

    final = state.get("final_delivery", {}) if isinstance(state, dict) else {}
    if final:
        if final.get("pass") is not True or str(final.get("status", "")).lower() != "pass":
            errors.append("state.json final_delivery must report pass=true and status=pass")
        if final.get("gaps") not in ([], None):
            errors.append(f"state.json final_delivery gaps is not empty: {final.get('gaps')!r}")

    combined = "\n".join(
        [
            delivery,
            trace,
            json.dumps(result, ensure_ascii=False),
            json.dumps(state, ensure_ascii=False),
        ]
    )
    fail_markers = [
        "completed_with_gaps",
        "controller interruption",
        "controller_intervention_required\": true",
        "post_hoc_artifact_repair\": true",
        "missing_artifacts_repaired_after_prompt\": true",
        "需要裁判",
        "裁判中断",
        "裁判提醒",
    ]
    for marker in fail_markers:
        if marker in combined:
            errors.append(f"controller/self-close failure marker present: {marker}")

    if "before interruption" in combined or "中断前" in combined:
        warnings.append(
            "interruption wording is present; it must be a designed replay event, not controller intervention"
        )

    payload = {
        "ok": not errors,
        "replay_root": str(root),
        "expected_rounds": args.expected_rounds,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
