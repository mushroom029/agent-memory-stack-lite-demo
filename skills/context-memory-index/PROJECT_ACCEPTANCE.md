# Context Memory Index Acceptance Map

## User Goal

Reduce live conversation load during long-running, versioned work while preserving recoverable state across `/compact`, session reuse, and model switches.

## Functional Nodes

### CMI-01 Trigger Coverage

Goal: Long-running or repeatedly compacted work should route into this skill.

Success:
- Skill description covers long sessions, repeated compaction, versioned test loops, and cross-session recovery.
- The skill is easy to trigger for "preserve context", "recover prior judgment", and "version index" requests.

### CMI-02 Live Anchor

Goal: The active thread stays small.

Success:
- `current-context.md` holds only the active baseline, hypothesis, known failures, next step, and links.
- The live anchor is intentionally short and fast to re-read.

### CMI-03 Capsule Index

Goal: Durable version judgments are searchable outside the chat thread.

Success:
- `index.md` points to version/topic capsules.
- Each capsule records one version or one durable topic shift.

### CMI-04 Recovery After Compaction

Goal: `/compact`, model switches, or thread restarts do not lose the active line of reasoning.

Success:
- Codex re-anchors from `current-context.md` first.
- Relevant capsules are reopened before continuing.

### CMI-05 Raw Evidence Separation

Goal: Raw logs stay external and are linked, not copied wholesale into the live thread.

Success:
- Capsules link to source logs or files.
- Summaries do not replace source evidence when facts conflict.

### CMI-06 Session Log Recovery

Goal: Active investigations have a lightweight chronological log that can be rebuilt after compaction.

Success:
- `session-log.md` captures recent actions, decisions, errors, and tests when the work is noisy or long-running.
- Stable conclusions are promoted into capsules instead of living only in the session log.
- `current-context.md` points at the active log when one exists.

### CMI-07 Reboot Check

Goal: After compaction or a session switch, the agent can re-anchor quickly from files.

Success:
- The skill includes a short reboot check.
- The live anchor can be reconstructed from `current-context.md`, `session-log.md`, and relevant capsules.

### CMI-08 Project Phase Discipline

Goal: The skill distinguishes early construction from user testing and stabilization.

Success:
- The memory files can record `exploration`, `testing/stabilization`, and `scoped-build` modes.
- Mature working behavior is protected during testing unless the user asks, a logic conflict requires change, or a verified bug requires change.
- Mode can be module-specific rather than freezing the whole project.

### CMI-09 Pressure Signal Memory

Goal: Strong user pressure survives compaction as risk-weighted project memory.

Success:
- Pressure is recorded as affected module, rejected behavior, inferred constraint, recurrence, and required agent behavior.
- Pressure lowers speed and tightens scope without blocking necessary fixes.
- Repeated pressure becomes durable capsule memory and updates `index.md`.

### CMI-10 Activation Packet Retrieval

Goal: Each resumed work burst loads only the needed memory while still respecting indexed risks.

Success:
- The skill requires reading the full `index.md` keyword map before selecting capsules.
- Activation packets include phase, scope, stable behavior, pressure signals, rejected approaches, and regression guards.
- A module named in `index.md` cannot be treated as memory-free until its indexed pressure, stable behavior, rejected approach, and guard entries are checked.
- Activation packets explain only surprise non-matches, not every skipped memory.
- Low-risk reversible tasks can use lightweight activation after checking whether the touched module or alias appears in `index.md`.

### CMI-11 Practical Update Cadence

Goal: Memory updates are frequent enough to survive compaction without making normal work unusable.

Success:
- `active-task.md` is refreshed after logical work units, not after every tiny edit.
- Rapid edit bursts have a batching rule and must flush before module switches, tests, review, user feedback, deployment, rollback, or errors.
- Unexpected compaction has a stale-memory exception when compacted summaries contain newer explicit user instructions.

### CMI-12 Memory Root Health Check

Goal: Project memory roots can be checked for common structural drift.

Success:
- A script reports missing `current-context.md` or `index.md`.
- Active `active-task.md` files without a next exact step are errors.
- Missing indexed capsule files are errors.
- Weak stabilization metadata, missing module aliases, and pressure entries without status are warnings.

### CMI-13 Operating Guidance Separation

Goal: Auto-loaded project instructions stay short and do not become a second memory store.

Success:
- The skill distinguishes `AGENTS.md` or configured fallback names such as `CODEX_GUIDANCE.md` from the context memory root.
- The auto-loaded guidance file is limited to operating rules and a pointer to `docs/context-memory/index.md` or the discovered memory root.
- Durable project memory remains in `current-context.md`, `index.md`, `session-log.md`, and capsules.
- Any fallback rename is verified with `codex debug prompt-input` before being treated as complete.

### CMI-14 Skill Evolution Discipline

Goal: Improvements discovered through real use become reusable without turning the skill into a history log.

Success:
- The skill records durable operating lessons, not conversation history or debugging narrative.
- Evolution entries are limited to future-session behavior: triggers, file responsibilities, forbidden actions, migration rules, validation, packaging, or recovery.
- Substantial skill updates are followed by validation and a rebuilt portable package.

## Validation

- Confirm `SKILL.md` triggers on long-running, versioned, or compaction-heavy work.
- Confirm the templates define the minimal file set plus the optional session log.
- Confirm the layout keeps the live anchor short.
- Confirm the reboot check can be answered from files alone.
- Confirm pressure signals and rejected approaches have fields in current context, active task, capsule, and index templates.
- Confirm the activation packet protocol prevents all-history loading while guarding against accidental "no memory needed" shortcuts.
- Confirm active-task updates are batched by logical work units and the batching rule is present in `SKILL.md`.
- Confirm core field names are consistent: `Stable behavior`, `Pressure signals`, `Rejected approaches`, and `Regression guards`.
- Confirm auto-loaded project guidance is documented as operating guidance, not project memory.
- Confirm skill evolution guidance records reusable rules without turning the skill into a changelog.
- Confirm `scripts/check-memory-root.py` catches missing files and passes a minimal valid root.

## Change Log

### 2026-07-06

Added project phase discipline, pressure-signal memory, negative-evidence preservation, stable-behavior protection, and activation-packet retrieval rules. This update treats user pressure during testing as risk-weighted project memory instead of noise, while avoiding a full freeze on necessary fixes.

Later on 2026-07-06, added conflict priority, mode transition criteria, pressure severity/status, module aliases, an activation packet template, and a lightweight memory-root health-check script.

Later on 2026-07-06, added practical batching for `active-task.md`, lightweight activation for low-risk tasks, surprise non-match reporting, stale-memory handling after unexpected compaction, canonical field names, and index recovery guidance.

Later on 2026-07-06, added project-root operating guidance separation: `AGENTS.md` or a verified fallback such as `CODEX_GUIDANCE.md` should stay short, point at the memory index, and not become a parallel project memory store.

Later on 2026-07-06, added skill evolution discipline: real-use upgrades should preserve durable future-session rules, avoid conversation-history bloat, and be validated plus repackaged before reuse.

### 2026-06-30

Initial creation of the context-index skill after repeated long-thread compaction made conversation state too fragile. The skill formalizes a small live anchor plus durable version capsules.
