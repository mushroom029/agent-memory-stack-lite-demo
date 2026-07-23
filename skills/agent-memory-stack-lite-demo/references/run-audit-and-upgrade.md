# Run Audit And Upgrade Notes

Use this after a meaningful demo run, install smoke test, user correction, repeated failure, or interrupted task recovery.

The pipeline is:

```text
observe -> audit note -> upgrade candidate -> human or maintainer judgment -> package patch only when justified
```

## Where To Record

Keep current run state in the active task. Put durable conclusions in one
capsule or domain owner and add a compact owner route in `index.md`.

Append to `docs/codex/session-log.md` only for unresolved failures/conflicts,
rollbacks, unpromoted corrections, provisional `[REVIEW:<id>]` bodies, or a
sparse phase/interruption checkpoint. Routine green runs with no durable delta
never enter the log — their outcome already lives in the progress boundary,
the validators, and the artifacts. Entries that later resolve or get promoted
leave the live log via `takeover-memory.py discharge`. Preserve old log bytes
as provenance.

## Run Audit Card

When an audit summary is needed, use this compact card. Store it in the active
task or relevant owner. A green card never goes to `session-log.md`; a yellow
or red card may enter only as the unresolved item it documents, and it leaves
via discharge once resolved. Add a longer narrative appendix only when the
card cannot carry
the needed evidence or a maintainer explicitly asks for detail. The card is for
Codex recovery after compression, not a user dashboard or an automatic entry
after every run.

`Verdict: green | yellow | red` is this run's audit conclusion only. It is
not a persistent global project state, autonomous monitor, automatic gate, or
permission to skip review.

A green verdict is not allowed while required delivery artifacts are missing,
unreadable, stale, or only described in memory. When the user requested a
machine-readable result, trace, report, or handoff file, the card must list its
path and existence/readability evidence under `Artifact discipline` or
`Tests/evidence`. If those artifacts are missing, use yellow/red, keep a next
exact step, and do not mark the active task complete.

```markdown
## Run Audit - <date> - <task>

- Verdict: green | yellow | red
- Verdict reason:
- Next exact step:
- ExecutionPolicy / active anchor:
- Task scope:
- Touched modules / protected not touched:
- Route drift / repeated failed path:
- Artifact discipline:
- Pressure pre-check:
- Encoding check:
- Memory hygiene:
- Tests/evidence:
- Memory writes:
- Owner route:
- Upgrade candidate / decision:
```

## Field Guidance

- `Verdict`: summarize this run only. If the user asks `今天有没有红灯`, answer from the latest card with context.
- `Next exact step`: one concrete next action, or `None; task complete` only
  after required delivery artifacts and validators have been verified.
- `ExecutionPolicy / active anchor`: name whether Lite Demo was memory-only or lite-anchor, and which `active-task.md` governed the run.
- `Touched modules / protected not touched`: say what changed and which stable areas were deliberately left alone.
- `Route drift / repeated failed path`: name avoided old paths or unresolved drift.
- `Artifact discipline`: reuse existing artifact before rerunning network/model calls unless the artifact is stale, invalid, missing, or the user explicitly asks to regenerate. Record the artifact path/evidence when relevant. For user-requested local deliverables, name every required file and whether it exists and is readable; missing files are completion blockers, not optional notes.
- `Pressure pre-check`: use `green`, `yellow`, `red`, or `not-triggered`.
  Green means task-relevant constraints were matched, the safe default was used,
  and no avoidable confirmation happened. Yellow means the card existed but the
  check, wording, or prompt budget was weak. Red means Codex violated a
  forbidden action, revived a rejected path, touched protected behavior without
  the required explanation, or claimed completion early.
- `Encoding check`: if Chinese memory/log/UI text changed, note UTF-8 write method and sentinel/mojibake result. See `encoding-discipline.md`.
- `Memory hygiene`: note whether temporary requests, pressure, failures, or short replies stayed task-local/revisable instead of becoming hard rules.
- `Owner route`: name the one body owner and its compact `index.md` wake-up route;
  use `none` when the run produced no durable memory.
- `Upgrade candidate / decision`: use `none`, `project-memory`, `skill-upgrade-candidate`, or `rejected`.

## Optional Longer Audit Appendix

Do not write this appendix by default. Use it only when the compact card would
hide evidence that the next Codex needs for recovery or upgrade judgment.

```markdown
## Run Audit - <date>

- Task:
- Environment:
- Memory files used:
- Policy scope:
- ExecutionPolicy:
- Execution protocol skills:
- Did Lite Demo stay memory-only when an external protocol existed:
- Was active-task.md created before complex execution:
- Did compression/interruption happen:
- Route drift observed:
- Repeated failed path avoided:
- Artifact discipline:
- Pressure pre-check:
- Encoding check:
- User correction:
- Memory hygiene note:
- Blocker:
- Upgrade candidate:
- Evidence path:
- Decision: candidate-only | accepted-for-project-memory | rejected
```

## Promotion Rules

Accept a lesson into durable memory only when it is:

- evidence-backed;
- useful for future sessions;
- specific enough to guide behavior;
- not just a temporary log;
- free of unnecessary private details.

Reject or keep as candidate-only when it is:

- a one-off accident;
- vague;
- contradicted by later evidence;
- too broad for the demo boundary;
- likely to create a worse habit.

Do not auto-edit the skill or append a log narrative after every run. Repeated
evidence should drive package upgrades.

Do not promote one ambiguous run, one pressure phrase, one failure, or one short
reply into a hard project rule. If the lesson is useful but uncertain, record it
as a revisable habit or task-local note.
