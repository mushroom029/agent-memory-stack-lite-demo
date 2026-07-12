# Run Audit And Upgrade Notes

Use this after a meaningful demo run, install smoke test, user correction, repeated failure, or interrupted task recovery.

The pipeline is:

```text
observe -> audit note -> upgrade candidate -> human or maintainer judgment -> package patch only when justified
```

## Where To Record

Use `docs/codex/session-log.md` for chronological notes.

Promote only durable lessons into `docs/codex/capsules/`.

## Run Audit Card

Default output is this compact card only. Add a longer narrative appendix only
when the card cannot carry the needed evidence or a maintainer explicitly asks
for detail. The card is for Codex recovery after compression, not a user
dashboard.

`Verdict: green | yellow | red` is this run's audit conclusion only. It is
not a persistent global project state, autonomous monitor, automatic gate, or
permission to skip review.

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
- Encoding check:
- Memory hygiene:
- Tests/evidence:
- Memory writes:
- Upgrade candidate / decision:
```

## Field Guidance

- `Verdict`: summarize this run only. If the user asks `今天有没有红灯`, answer from the latest card with context.
- `Next exact step`: one concrete next action, or `None; task complete`.
- `ExecutionPolicy / active anchor`: name whether Lite Demo was memory-only or lite-anchor, and which `active-task.md` governed the run.
- `Touched modules / protected not touched`: say what changed and which stable areas were deliberately left alone.
- `Route drift / repeated failed path`: name avoided old paths or unresolved drift.
- `Artifact discipline`: reuse existing artifact before rerunning network/model calls unless the artifact is stale, invalid, missing, or the user explicitly asks to regenerate. Record the artifact path/evidence when relevant.
- `Encoding check`: if Chinese memory/log/UI text changed, note UTF-8 write method and sentinel/mojibake result. See `encoding-discipline.md`.
- `Memory hygiene`: note whether temporary requests, pressure, failures, or short replies stayed task-local/revisable instead of becoming hard rules.
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

Do not auto-edit the skill after every run. Repeated evidence should drive package upgrades.

Do not promote one ambiguous run, one pressure phrase, one failure, or one short
reply into a hard project rule. If the lesson is useful but uncertain, record it
as a revisable habit or task-local note.
