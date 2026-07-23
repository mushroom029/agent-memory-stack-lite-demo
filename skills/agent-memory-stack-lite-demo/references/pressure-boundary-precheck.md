# Pressure Boundary Precheck

Use this when the current turn is risky, resumed after interruption, corrective,
pressure-heavy, likely to touch protected behavior, or likely to revive a
rejected path.

This is a memory-layer execution pre-check. It is not a lock. Its value is an
auditable execution contract: Codex must name the matched constraints, the safe
default, the stop condition, and the completion blockers before it performs a
risky action.

## Inputs

Apply this after `user-requirement-ledger.md` and before ambiguous memory is
weakened by `memory-hygiene-nudge.md`.

Gate-worthy inputs:

- explicit user goals, prohibitions, acceptance criteria, and corrections;
- stable behavior or modules the user said already work;
- rejected paths or failed approaches with no changed condition;
- pressure that clearly names a rejected action, repeated mistake, broken
  stable behavior, wasteful model/API call, or forced re-explanation;
- required delivery artifacts, validation evidence, or handoff files.

Memory-only inputs:

- vague urgency with no concrete rejected action;
- general mood, politeness, fatigue, or annoyance without an actionable
  boundary;
- model guesses about user preference;
- background project facts that do not constrain this turn.

## Pressure Boundary Extraction

Preserve the original user pressure text as evidence, but execute only against
the extracted boundary.

Write a boundary only when it can be phrased as:

- `user rejects <action/route/module touch/repeated mistake>`;
- `user fears <testable harm>`;
- `completion requires <artifact/evidence/acceptance check>`.

If extraction is unclear, store the note as task-local memory or pending review.
Do not convert it into a durable rule or a stop condition.

## Execution Pre-Check Card

For risky or corrective work, place this compact card in `active-task.md` or the
task-local owner before edits, installs, deployments, state-changing tests, or
long investigation branches:

```markdown
Execution pre-check card:
- Current task:
- Matched constraints:
- Safe default action:
- Forbidden actions this turn:
- Explain-before-action triggers:
- Stop-and-ask conflicts:
- Completion blockers:
- User prompt budget:
- Evidence owners:
```

Keep the card short. It is for Codex recovery and self-check, not a user
dashboard.

## Behavior Rules

- If a safe default action exists, take it instead of asking the user to approve
  routine caution.
- Ask only when every safe route is blocked by the user's current goal.
- When asking is unavoidable, state the old boundary, the current conflict, the
  safe default, and the narrow scope of the possible override. Do not recommend
  the risky option.
- A short reply such as `好`, `继续`, or `都行` authorizes only the narrow next
  action. It does not rewrite durable project memory.
- Use `Lite Demo 提醒：` only for memory routing, stable-touch risk, conflict
  risk, or clear overlap risk. Do not show gate jargon to ordinary users.
- If the task can be completed without touching a protected module, avoid that
  module and record the choice only when it matters for recovery.

## Violation And Fatigue Check

Before an edit or state change, compare the planned action with:

- forbidden actions this turn;
- rejected paths;
- stable-touch triggers;
- completion blockers.

After a work unit, record whether:

- any forbidden action was performed;
- a rejected path was reused without changed conditions;
- a stable module was touched without the required Chinese explanation;
- completion was claimed while an artifact or validation blocker remained;
- Codex asked for avoidable confirmation.

More than one avoidable confirmation in a short task is yellow. Any prompt that
pushes an ordinary user toward a risky override is red.

## Audit Field

When a Run Audit card is written, include one compact line:

```markdown
- Pressure pre-check: green | yellow | red | not-triggered
```

Green means task-relevant constraints were matched, the safe default was used,
and no avoidable confirmation happened. Yellow means the card existed but the
check, wording, or prompt budget was weak. Red means Codex violated a forbidden
action, revived a rejected path, touched protected behavior without the required
explanation, or claimed completion early.
