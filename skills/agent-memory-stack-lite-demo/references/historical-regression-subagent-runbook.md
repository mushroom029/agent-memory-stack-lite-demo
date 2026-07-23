# Historical Regression Subagent Runbook

Use this runbook when a Lite Demo upgrade needs model-behavior evidence. It is
not a permanent live agent. Start a fresh subagent for each package version,
give it clean inputs, collect artifacts, then close it.

## Controller Setup

Inputs:

- `PACKAGE_ROOT`: unpacked Lite Demo package root.
- `SKILL_ROOT`: `PACKAGE_ROOT/bundled-skills/agent-memory-stack-lite-demo`.
- `OUTPUT_ROOT`: throwaway regression output folder.
- `PACKAGE_VERSION`: expected version such as `v0.2.18`.
- `SCENARIOS`: `all` or a comma-separated list such as `R01,R04,R10`.

Rules:

- Do not pass the intended answer, diagnosis, or previous report to the
  subagent. Pass the package and scenario prompts.
- Do not ask for hidden chain of thought. No hidden chain of thought is required. Require concise visible traces,
  command summaries, file paths, and machine-readable results.
- Use throwaway projects and temporary homes. Never use a user's live project
  unless the user explicitly asks.
- If a replay modifies files, it must modify only its own `OUTPUT_ROOT`.
- The controller, not the subagent, makes the final release decision.

## Fresh Subagent Prompt

```text
You are running a Lite Demo historical regression replay.

Package root:
<PACKAGE_ROOT>

Skill root:
<SKILL_ROOT>

Output root:
<OUTPUT_ROOT>

Expected package version:
<PACKAGE_VERSION>

Scenario set:
<SCENARIOS>

Use the supplied Lite Demo package as a user-facing Codex skill package. First
run the deterministic package checks that are safe in this throwaway workspace.
Then run the requested runtime replay scenarios from
references/historical-regression-suite.md.

Do not publish, upload, or touch any live project. Do not request secrets. Do
not expose hidden chain of thought. Write visible traces and artifacts only.

For every scenario, create:
- scenario-results/<ID>/trace.md
- scenario-results/<ID>/result.json
- scenario-results/<ID>/memory-root-check.json when a memory root is created

Create:
- matrix.json
- controller-notes.md

Use statuses PASS, PARTIAL, or FAIL. If a behavior cannot be proved because a
real agent/user loop is missing, mark PARTIAL and state the exact missing
evidence. A final "looks good" without artifacts is FAIL.
```

## Required Output Shape

`matrix.json`:

```json
{
  "package_version": "v0.2.18",
  "package_root": "<PACKAGE_ROOT>",
  "started_at": "<ISO-8601>",
  "finished_at": "<ISO-8601>",
  "summary": {
    "pass": 0,
    "partial": 0,
    "fail": 0
  },
  "scenarios": [
    {
      "id": "R01",
      "status": "PASS",
      "evidence": [
        "scenario-results/R01/trace.md",
        "scenario-results/R01/result.json"
      ],
      "gaps": []
    }
  ]
}
```

Each `result.json`:

```json
{
  "id": "R01",
  "status": "PASS",
  "pass": true,
  "summary": "one sentence",
  "commands_run": [],
  "files_created_or_changed": [],
  "forbidden_side_effects_observed": false,
  "memory_root": null,
  "validation": {
    "package_check": "PASS",
    "memory_check": "not-applicable"
  },
  "gaps": []
}
```

## Controller Acceptance

Accept a replay only when:

- every requested scenario has `trace.md` and `result.json`;
- `matrix.json` summarizes every scenario exactly once;
- PASS entries include concrete artifacts or command evidence;
- PARTIAL entries name missing evidence without pretending success;
- FAIL entries identify the violated historical category;
- the subagent finishes with a final answer and does not require controller
  interruption to close the run.

If the package was changed after replay, discard the old replay and run a fresh
subagent again. Do not reuse a dirty subagent as release evidence.
