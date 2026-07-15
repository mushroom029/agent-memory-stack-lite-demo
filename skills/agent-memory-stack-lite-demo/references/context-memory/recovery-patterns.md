# Recovery Patterns

Use these patterns when the work is active and the live thread is starting to feel crowded.

## When to use session-log.md

Create or update the project session log, such as `docs/codex/session-log.md`
or the discovered project memory root's `session-log.md`, only when:

- An unresolved failure, conflict, or rollback must survive interruption.
- A user correction is not yet promoted to its final body owner.
- Ownership is uncertain and one provisional `[REVIEW:<id>]` body plus a
  pending index route is required.
- A phase boundary or interruption needs one sparse recovery checkpoint.

## Update cadence

- Do not write by tool-call count, elapsed work burst, or successful test count.
- Routine green work with no new durable delta gets no session-log narrative.
- During testing or bug-fix work, log strong user pressure as a pressure signal:
  affected module, rejected behavior, inferred constraint, recurrence, and
  required agent behavior.
- After each logical work unit in long/risky work, refresh `active-task.md`
  `Current step`, `Completed`, and `Next exact step` before switching focus,
  running tests, requesting review, or entering interruption risk.
- For rapid edit bursts in one module, batch `active-task.md` refreshes until
  the burst ends. End the burst and refresh after errors, test failures, user
  feedback, module switches, deployment, or rollback.
- After a phase shift or deliberate compaction warning, sync `current-context.md`
  and `active-task.md`, then append one sparse checkpoint only if those pointers
  do not already make recovery clear.
- Keep `session-log.md` append-only. A long log is cold local memory, not a
  default recovery payload. Do not delete, rotate, or rewrite older entries
  merely because the file grew.

## Recovery read policy

- Start with roughly the most recent 30-60 lines or a few sparse checkpoints as
  a recency probe, never as the total recall budget.
- Never read a long `session-log.md` in full by default.
- Read older content only through a targeted keyword search or a bounded line
  range when `active-task.md` points to evidence, sources conflict, or required
  information is missing.
- A search miss, alias ambiguity, source conflict, first-time entity touch, or
  irreversible action is a reason to widen retrieval, not proof that no
  historical boundary exists.
- Give explicit corrections, rejected approaches, and stable boundaries one
  body owner plus a compact index route when written. Do not mirror their full
  narrative into every layer.
- The internal `scripts/read-session-log.py` helper provides a 60-line default
  tail plus explicit search/range modes without modifying the source log.

## Mid-task compaction guard

For long approved tasks, write `active-task.md` before execution begins. This is
the recovery anchor if the thread compacts mid-run.

The file should say the last approved route, exact next step, validation gates,
critical user corrections, rejected paths, stable boundaries, evidence
pointers, and non-goals. Keep it small. It is not a log; replace stale progress
summaries instead of appending one history block per batch.

Because system compaction can happen without warning, do not rely on a final
"before compaction" save. Keep the route marker current during execution. Any
logical state-changing unit, such as an edit burst, server change, generated
artifact, test result, or confirmed decision, should be followed by an
`active-task.md` refresh before the route can change.

After compaction or resume, read `active-task.md` before acting. If the compacted
summary suggests a different route, treat the summary as secondary and reconcile
against `active-task.md`, `current-context.md`, and project files.

If an unexpected compaction happened after the latest memory-file `Updated:`
timestamps and the compacted summary contains newer explicit user instructions,
temporarily treat those specific instructions as newer user input. Reconcile
them into memory files before making state-changing edits.

Before touching code, server state, or generated artifacts after resume, perform
a route check:

- Does the next action match `active-task.md`?
- Does the activation packet include relevant project phase, stable behavior,
  pressure signals, rejected approaches, and regression guards for the touched
  module?
- Did the conflict priority order change the route? Newest explicit user
  instruction wins over the active anchor, which wins over compacted summaries
  and engineering taste, except for the stale-memory exception above.
- Did the user give a newer instruction after the anchor was written? Scan
  visible user messages after `active-task.md`'s `Updated:` value when timestamps
  are available. If timestamps are unavailable, treat the first visible user
  message after resume as authoritative; if it contradicts `active-task.md`,
  update the anchor before continuing.
- Are validation gates and "do not touch" boundaries still intact?
- After completing this check, update `Route check:` in `active-task.md` with a
  one-line outcome such as `Passed 2026-07-02: next action matches anchor.` or
  `Mismatch recorded in session-log.md.`
- If not, update `session-log.md` with the mismatch and ask or revise the anchor
  before continuing.

Mark `active-task.md` complete when finished, then promote durable results into a
capsule.

## Promote to a capsule

- Move stable conclusions, rejected hypotheses, and durable version judgments into capsules.
- Move repeated pressure signals, disproven approaches, and do-not-resurrect
  decisions into capsules.
- Keep all old session-log bytes as cold evidence. New entries still obey the
  admission gate, and default recovery uses only the recency probe.
- Leave raw logs, screenshots, and traces in separate files and link to them.

## Reboot check

Answer these from files before making new judgments:

1. Where am I?
2. Where am I going next?
3. What is the current goal?
4. What have I learned?
5. What have I already done?
6. If `active-task.md` exists, what exact step was interrupted?
7. Does my next action still match the last approved route?
8. What phase/mode am I in, and what stable behavior must not be changed?
9. Which rejected approaches must not be resurrected?
10. Did I check module aliases in `index.md` before deciding memory relevance?
