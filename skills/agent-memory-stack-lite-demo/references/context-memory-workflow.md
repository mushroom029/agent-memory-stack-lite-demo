# Lite Demo Internal Context Memory Workflow

This is an internal reference for `$agent-memory-stack-lite-demo`, not a
standalone skill. Do not ask the user to install or activate it separately.

Use this skill to keep memory on disk while loading only the owners that matter
to the current action.

## Core idea

Keep only a small live anchor and routing vocabulary in chat. Give every
durable fact one normative body owner, then keep only compact wake-up routes in
the other memory layers. Local memory may remain large; default context must
not become a copy of the whole store.

Explicit user goals, prohibitions, acceptance criteria, and corrections are
requirements by default. They are not softened by pressure wording. Use
[user-requirement-ledger.md](user-requirement-ledger.md) before applying the
weak-memory hygiene nudge.

When the user points to an old conversation, damaged conversation, old project,
archive, or unknown memory source, use
[legacy-source-import.md](legacy-source-import.md) before creating a blank
current-session entry point.

When the user points to a long local text source, such as a novel, transcript,
exported chat, or large notes file, use
[large-text-source-intake.md](large-text-source-intake.md) before reading or
summarizing long bodies. Keep source slices in artifacts and keep memory layers
limited to interpretation, routing, boundaries, and continuation notes.

When unfinished or parallel work creates ambiguity, treat it as memory routing,
not task management. The question is only: which task memory should the current
conversation read and write? Do not infer whether another conversation is still
running, schedule task order, merge tasks, isolate code files, or version
workflows.

## Minimal setup

Start lightweight. Create only what the current project needs:

For a brand-new root, do not hand-write these starter files. Run the bundled
`scripts/takeover-memory.py initialize <memory-root>` first so the root starts
with one current schema entry and one verified `fresh-initialization`
checkpoint. Then edit the initialized files and add owners/routes as needed.
This rule also applies in preauthorized test harnesses and concurrent replay
runs.

The full Lite Demo source package has top-level install helpers outside the
installed skill folder. A runtime agent that only has the skill folder must not
treat missing package-level `scripts/install.ps1` as a business-task blocker;
use the bundled `takeover-memory.py initialize` path for fresh roots instead.

1. `current-context.md` for phase, baseline, next step, and evidence links.
2. `index.md` for active version/topic, module aliases, keyword navigation, and capsule pointers.
3. Capsules as stable conclusions, rejected approaches, pressure signals, or regression guards become durable.
4. `active-task.md` only for multi-phase, risky, approved, or compaction-sensitive work.
5. `session-log.md` only for unresolved failures, conflicts, rollbacks,
   unpromoted corrections, provisional `[REVIEW:<id>]` memories, and sparse
   phase/interruption checkpoints.

## Default layout

See [context-memory/layout.md](context-memory/layout.md), [context-memory/templates.md](context-memory/templates.md), [context-memory/index-template.md](context-memory/index-template.md), [context-memory/recovery-patterns.md](context-memory/recovery-patterns.md), [context-memory/project-stages-and-risk.md](context-memory/project-stages-and-risk.md), and [context-memory/activation-packet-template.md](context-memory/activation-packet-template.md).

The context root is selected by path discovery. Reuse an existing project root
such as `docs/context-memory/`, `docs/codex/`, or `docs/context/`. If none
exists, use `docs/codex/` as the fallback. Keep the same file structure inside
the selected root.

## Memory Creation Consent

Do not silently create a first memory root. If no `docs/codex/`,
`docs/context-memory/`, or `docs/context/` exists, ask before creating it unless
the user explicitly requested project memory, install, or landing, or project
memory says `Memory landing policy: preauthorized`.

If a memory root already exists and a new task line becomes complex after 2-3
rounds, multiple constraints, user corrections, pressure signals, failure
paths, or likely compaction, route the current conversation to the right task
memory. Ask only when the route is ambiguous. Use
`docs/codex/tasks/<task-id>/active-task.md` when a separate task memory is
needed, leave other task memories unchanged, and add only a compact pointer to
`index.md`. Do not create a second memory database.

If no memory root exists and a task becomes clearly nontrivial, Codex may make
one plain Lite Demo/project-memory suggestion. If the user refuses, do not
create files or store the refusal; simply stop suggesting again in the current
chat. Later explicit memory activation overrides that temporary skip.

When preauthorized, creating or updating an anchor is allowed, but the user must
be told which path was written, why, and how to return to ask-before-write mode.
Preauthorization does not allow hand-written schema/checkpoint substitutes:
new roots still start through `takeover-memory.py initialize`.

## Project Operating Guidance

Keep the auto-loaded project instruction file separate from project memory.
`AGENTS.md` is the usual Codex convention; a configured fallback such as
`CODEX_GUIDANCE.md` is acceptable only after `codex debug prompt-input`
verifies it loads in the real project root.

Use that file for short operating rules: shell patterns, remote-access safety,
deployment boundaries, maintenance discipline, and a pointer to the memory
index. Do not store chronological history, rejected-solution evidence, pressure
signals, or version judgments there. Those belong in the context root and
capsules.

## Skill Evolution

When real project use exposes a reusable gap in this skill, update the skill
itself with the durable operating lesson. Do not store the conversation history,
debugging narrative, or changelog-style process notes as skill instructions.

Record an evolution only when it changes future-session behavior, such as:
new trigger conditions, file responsibilities, forbidden actions, migration
rules, validation requirements, packaging requirements, or recovery rules.

After a substantial update, run skill validation and rebuild the portable
package before treating the upgrade as reusable on another computer.

## Workflow

1. Read `active-task.md` if present and not complete.
2. Read `current-context.md`.
3. Read the compact routing layer in `index.md`.
4. Derive the module, entity, behavior, version, and risk touched by the current
   action. Match them against strong-relevance keywords, aliases, topics, and
   scope routes. Follow every matching route to its current normative owners
   and all mandatory guards. Non-`archived-only` `legacy-destinations.md`
   entries are supplemental routes for old-source imports; they may wake the
   new owner chosen for an old item without loading the old log body. If the
   route points to a one-level `history=` page, scan it and open only precisely
   matched versions/events. Do not use a top-k cutoff. If explicit routing
   misses or returns only weak candidates, query the derived pointer cache
   before claiming no memory; open mandatory derived records and selected owner
   pointers, then use targeted legacy/source search only for remaining gaps or
   conflicts.
5. If the current action ingests or summarizes a long local source, first create
   `artifacts/source-slices/` with `scripts/slice-text-source.py`, then read
   `manifest.json` and `chapters-index.md` before selected slice files. Do not
   copy raw source bodies into `current-context.md`, `active-task.md`,
   `index.md`, `session-log.md`, or the derived cache.
6. Read `session-log.md` only when an exact unresolved route selects an entry,
   sources conflict, or selected owners still leave an evidence gap. Use an ID
   search or bounded range; never inject a default tail or the full log.
   For v0.2.17 local-history recall work, use
   [derived-memory-index.md](derived-memory-index.md) to build/query the
   disposable `.lite-demo-cache/v1/` derived index. It returns pointers,
   reasons, hashes, mandatory records, and continuation state; owners remain the
   truth.
7. Open only the capsules tied to the active version, module, hypothesis, pressure signal, rejected approach, or regression guard.
8. Build a short activation packet for the current turn: phase, goal, scope, stable behavior, pressure signals, rejected approaches, allowed changes, forbidden changes, test guards, and selected memories.
9. For long, risky, or multi-step tasks, create or update `active-task.md` before starting execution.
   If the user explicitly allowed project-memory/task landing and the task is
   long, multi-step, risky, approved, or compaction-sensitive, this is a hard
   gate: do not begin code edits, state-changing tests, deployment, or a long
   investigation branch until the anchor exists. If the memory root does not
   exist yet, initialize it with the helper before creating that anchor.
10. After each logical work unit in long/risky work, refresh `active-task.md` with the current step and next exact step before switching focus, running a validation gate, asking for review, or entering interruption risk.
11. Before deliberate compaction, restart, or a major phase shift, update
    `current-context.md` and `active-task.md`, then append one sparse checkpoint
    only if it adds recovery value.
12. Keep `current-context.md` short: phase, goal, active constraint, evidence pointers, active-task pointer, and next step. Move durable detail into capsules.
13. Apply the session-log admission AND discharge gates. Admission: admit only
    unresolved failures/conflicts, rollbacks, unpromoted corrections,
    `[REVIEW:<id>]` bodies whose owner is uncertain, and sparse recovery
    checkpoints. Routine green work with no new durable delta never enters the
    log. Content summaries, progress enumerations, and per-batch results belong
    to their owners (capsules, active task boundary, index routes, local
    artifacts), never to the log. Discharge: every admitted entry is in-flight,
    not permanent. Use structured in-flight `TYPE:id` headings: canonical
    `REVIEW`, `UNRESOLVED`, and `CHECKPOINT`; compatibility headings
    `CORRECTION`, `ROLLBACK`, and `CONFLICT` obey the same rule. After an entry
    settles, update a route with exact `entry=TYPE:id` identity (legacy bare
    review IDs remain accepted), a real owner, and a helper-recognized settled
    owner/guard/resolved/promoted/superseded status, then run
    `scripts/takeover-memory.py discharge <memory-root>` so homed entries move
    byte-preserved to `legacy/session-log-discharged.md`. Resolved failures and
    promoted corrections leave the same way once their outcome lives with an
    owner. The live log holds only what is still unresolved or unhomed. As a
    safety bound, `scripts/takeover-memory.py roll <memory-root>` still archives
    the oldest free-region entries to `legacy/session-log-archive.md` if the
    log grows past its line budget. Never delete, rotate by hand, rename, or
    rewrite entries yourself; only the discharge and roll helpers may move
    them, and they never touch the checkpoint or the legacy prefix it protects.
14. At durable-memory write time, choose exactly one normative body owner and
    add a wake-up route in `index.md` with scope, aliases/keywords, owner path,
    and one short routing reason. Other layers may keep a short ID, provenance,
    and pointer, but must not mirror the narrative body.
15. Before writing user instructions as memory, classify explicit goals,
    prohibitions, acceptance criteria, and corrections through
    `user-requirement-ledger.md`. If a new target conflicts with an existing
    explicit instruction, run the A/B/C conflict gate before acting.
16. Before promoting one request, pressure phrase, short acknowledgement, local
    failure, or temporary boundary into a durable rule, keep it weak by default:
    task-local or revisable unless it is an explicit requirement or the user
    used explicit absolute wording for a permanent hard boundary.
17. Keep reusable workflow memory compact. Run-specific progress, failed paths,
    pressure, and next steps stay in task anchors. Workflow adjustments stay
    task-local until the user clearly asks to keep them as the new shared way;
    do not maintain a workflow version chain.
18. Store raw logs separately and link them from the log or capsules instead of pasting them wholesale.
19. After a restart or model switch, rebuild the live anchor from
    `active-task.md`, `current-context.md`, `index.md`, and every matched owner
    and mandatory guard. Read targeted evidence from `session-log.md` only for
    an exact unresolved route, source conflict, or remaining evidence gap. A
    miss, alias ambiguity, first-time entity touch, or irreversible action
    requires wider owner/route retrieval before claiming no boundary exists.

## Ownership And Reachability Contract

- One durable fact has one normative body owner.
- `index.md` is the compact owner router; do not create a second owner manifest.
- Use route entries shaped as `scope: aliases=...; keywords=...; owners=...;
  mandatory=...; history=...; reason=...`. `owners` means current normative
  bodies. `mandatory` points to touched-scope guard owners
  that must all be opened.
- Put cold versions/events behind one route page under `routes/`. The page uses
  the same grammar, has precise version/event aliases, and cannot point to a
  second route page. Keep every still-live prohibition or stable boundary in a
  top-level mandatory owner.
- Explicit prohibitions, rejected paths, stable behavior, acceptance criteria,
  unresolved conflicts, and irreversible-action guards are mandatory recall.
- Explicit user goals, prohibitions, acceptance criteria, and corrections must
  have a requirement owner or a `pending-review` owner; do not hide them as
  pressure-only evidence.
- A durable write is incomplete until its route exists. When ownership is
  uncertain, write one `[REVIEW:<id>]` body in `session-log.md` and immediately
  add a `status=pending-review` route to that exact entry. Once the owner
  settles, move the body to that owner, update the route (drop
  `pending-review` and the in-log anchor), and run
  `scripts/takeover-memory.py discharge <memory-root>` — the log entry has done
  its job and leaves the live log byte-preserved.
- A legacy takeover with meaningful old history is incomplete until
  `legacy-destinations.md` assigns every meaningful old item one destination:
  `memory-owner`, `mandatory-guard`, `rejected-path`,
  `project-owner-indexed`, `archived-only`, or `pending-review`. This manifest
  is domain-neutral. It proves old memory is reachable or deliberately cold; it
  must not become another narrative store.
- A cross-conversation or damaged-conversation import is incomplete until every
  meaningful item from the referenced legacy source has the same destination
  proof. Initializing the current root alone is not import completion.
- Use `scripts/route-memory.py` to resolve every matching owner. Use
  `scripts/check-memory-root.py` to find missing routes, broken pointers,
  duplicate bodies, or stranded review items.

## First Activation After Upgrade

On the first v0.2.17 activation in an existing memory root that lacks current
dual completion proof, ask once whether to `继承并升级整理旧记忆` or `全新启动`
before changing migration state. If the user chooses inheritance, apply
`automatic-legacy-takeover.md` as memory maintenance, not old-task execution.
Successful takeover changes what future recovery injects, so the next context
cleanup or compaction can discard old live text and rebuild from compact routes
without a second migration command. If meaningful old history exists,
successful takeover also requires the legacy destination manifest described in
`legacy-destination-manifest.md`; preserving old log bytes without reachable
destinations is not a semantic takeover. If the user chooses fresh start, keep
old memory cold, do not default-recall it, and do not claim inheritance.
Package v0.2.17 keeps the memory schema/checkpoint label `v0.2.7` as the
current compatible on-disk format.

If the user names a legacy source outside the current root, first use
`legacy-source-import.md`. That path follows the same destination-proof rule as
inheritance takeover, not a project-specific exception.

## Conflict Priority

When sources disagree, follow this order:

1. Newest explicit user instruction.
2. Active `active-task.md` route.
3. `current-context.md`.
4. Relevant capsules and `index.md`.
5. `session-log.md`.
6. Compacted chat summary.
7. Codex engineering taste or inferred aesthetics.

Exception: if memory file `Updated:` timestamps are older than an unexpected
compaction and the compacted summary contains newer explicit user instructions
that are not reflected in memory files, treat those specific instructions as
priority 2 until the memory files are reconciled.

If the newest user instruction conflicts with the anchor, update the anchor before acting.

If a new target conflicts with any explicit stored user requirement or
prohibition, state the conflict and offer: A. keep the existing instruction and
adjust the current target; B. temporary scoped override only for this
creation/process; C. ask the user to complete or replace the command.

## Project Phase And Risk

Use [context-memory/project-stages-and-risk.md](context-memory/project-stages-and-risk.md) when the user starts testing, reports regressions, expresses strong frustration, or asks for bug fixes on a partly working project.

Core rules:

- Treat user pressure as a project risk signal and requirement tendency, not as noise.
- Treat pressure as a weighted constraint, not an absolute freeze.
- In early exploration/build mode, Codex may infer, design, and reshape the product.
- In testing/stabilization mode, protect mature working behavior unless the user asks, a logic conflict requires change, or a verified bug requires change.
- For stable or user-confirmed working behavior, require a Chinese explicit judgment before touching it: protected behavior, necessity, evidence chain, scope, non-goals, and regression check.
- If pressure targets a module, narrow discipline to that module; do not freeze unrelated project work.
- If the user explicitly requests expansion or refactor, enter scoped build mode and declare scope and protected areas.
- Record repeated pressure, rejected behavior, and "do not resurrect" decisions as durable memory so compaction cannot revive a previously disproven solution.

## Activation Packet

Before acting after resume, compaction, model switch, or a risky new request, synthesize a short activation packet from the memory files. Use [context-memory/activation-packet-template.md](context-memory/activation-packet-template.md).

If no memory is selected for the current task, say why. If the task touches a module named in `index.md`, first check that module's pressure signals, stable behavior, rejected approaches, and guard entries.

For simple, reversible, low-risk tasks, use a lightweight activation:

1. Check whether the touched file, module, or alias appears in `index.md`.
2. If it does not, state that no indexed constraints were found and proceed.
3. If it does, inspect only that module's pressure signals, stable behavior,
   rejected approaches, and regression guards.
4. Build a minimal packet only when those indexed constraints affect the task.

## Active Task Anchor

Use `active-task.md` to prevent mid-task compaction from changing the route.

When the user explicitly allows project-memory/task landing and the task is
long, risky, multi-step, approved, or likely to compact, `active-task.md` is a
pre-execution gate rather than an optional later note.

Create or update it before starting work when:

- the task has more than one phase;
- the task will touch production, deployment, release, or user-facing behavior;
- the user has approved a plan and expects that plan to continue;
- a previous run drifted after compaction;
- the work includes a rollback point, validation gate, or "do not touch" boundary.

Keep it short and directive:

- goal;
- scope;
- mode and touched modules;
- activation packet;
- allowed and forbidden changes;
- current step;
- one overwrite-only `Progress boundary` value and evidence pointers;
- next exact step;
- validation gates;
- rollback/backup path if any;
- explicit non-goals and "do not touch" items.

The anchor is the current route, not a chronological audit trail. Replace stale
`Current step`, `Progress boundary`, and `Next exact step` values as the route moves;
do not append one section or bullet set per batch. Durable corrections,
rejected paths, and stable boundaries get one body owner plus compact route and
evidence pointers. Only admitted unresolved events or sparse checkpoints go to
the helper-managed in-flight session log.

After compaction, do not continue from the compacted chat alone. Read
`active-task.md` first. If it conflicts with the compacted summary, prefer
`active-task.md` and the project files, then reconcile in `session-log.md`.

When a task is complete, mark `active-task.md` as `Status: complete`, set
`Next exact step` to `None; task complete`, and move durable conclusions into a
capsule. Keep the completed anchor as an archive. Future resumes must not follow
a completed anchor's `Next exact step` or `Resume instruction`.

## Compaction Interruption Gate

Use [context-memory/recovery-patterns.md](context-memory/recovery-patterns.md) whenever compaction, restart, model switch, or a tool/session handoff happens during an unfinished task.

Minimum gate:

1. Read active `active-task.md`, then `current-context.md`, `index.md`, and relevant capsules.
2. Build an activation packet.
3. Compare the intended next action with `active-task.md`.
4. Continue only if the action matches the anchor or the user gave a newer instruction.
5. If the user gave a newer instruction, update the anchor before acting.

Do not start a new fix, refactor, investigation branch, or deployment during
resume until this gate has passed.

Batching rule for rapid edits: when making 3+ state-changing edits inside one
logical work unit, refresh `active-task.md` once after the burst instead of
after every edit. End the burst and refresh before switching modules, running
tests, requesting review, acting on user feedback, deployment, rollback, or
any error/test failure. A burst that spans multiple modules should refresh
after each module group.

## Decision rules

- Use `current-context.md` for the active thread state.
- Use `index.md` only as a compact router across versions and topics: keyword/alias/topic -> pointer + one short routing reason.
- Keep old `session-log.md` bytes as immutable local evidence. New writes obey
  the admission gate. Read only targeted evidence selected by an exact
  unresolved route, source conflict, or evidence gap.
- Use one capsule per version or one durable topic shift.
- Split capsules when evidence or hypotheses diverge.
- Prefer source logs over summaries when facts conflict.
- If a provisional note becomes durable, establish one capsule/domain owner and
  replace its pending route with the final owner route. Preserve the old log
  entry only as provenance; do not copy its full body into another live layer.
- Record compact run-audit fields in the active task or relevant domain owner.
  Append a session-log card only for an admitted unresolved item or sparse
  recovery checkpoint.
- Use pressure signals to lower speed, restate the target, and tighten scope; do not interpret pressure as permission to stop necessary fixes.
- Treat pressure, short approval, and one-off instructions as memory evidence, not automatic hard law. If the note becomes durable, mark it task-local, revisable, or an explicit hard boundary.
- Treat direct goals, prohibitions, acceptance criteria, and corrections as
  requirements first; only ambiguous leftovers use the weak-memory default.
- Keep negative evidence visible: rejected approaches, old-solution resurrection risks, and regression guards must survive compaction.
- For a project memory health check, run `scripts/check-memory-root.py <memory-root>`.

## Index Purity

The initial context should pay only for the routing layer and active state. The
context cost of memories selected for the current task is necessary; do not cap
or discard relevant capsules merely because they are detailed.

Do not let `index.md` become a second memory store. Move explanations, evidence,
decision history, long guards, and narrative status into capsules. Treat size
warnings from `check-memory-root.py` as silent maintenance signals for Codex,
not as user-facing approval gates or hard limits on selected memory.

## Reboot check

When you resume after compaction, restart, or model switch, answer these from files before making new judgments:

1. Where am I?
2. Where am I going next?
3. What is the current goal?
4. What have I learned?
5. What have I already done?

If `active-task.md` exists and is not marked complete, answer one more question:

6. What exact step was in progress before interruption?
7. What phase/mode is the project or touched module in?
8. Which pressure signals, rejected approaches, and stable behaviors constrain this turn?

## What not to do

- Do not treat compacted chat as the source of truth except for the narrow stale-memory exception in Conflict Priority.
- Do not bury history only in the conversation thread.
- Do not expand the live anchor beyond what can be re-read quickly.
- Do not let the session log become a second capsule store.
- Do not log routine green actions merely because tools were called or a work
  burst ended.
- Do not copy one durable narrative into current-context, active-task, index,
  capsule, and session-log. Keep one body and compact pointers.
- Do not read a long session log in full merely because the current task is
  active, noisy, or interrupted.
- Do not delete, summarize away, or irreversibly rewrite the local session log
  as a context-control shortcut. The only sanctioned bounds are
  `takeover-memory.py discharge`, which moves settled structured in-flight entries
  byte-preserved to `legacy/session-log-discharged.md`, and
  `takeover-memory.py roll`, which moves whole old entries byte-preserved to
  `legacy/session-log-archive.md`; neither touches the checkpoint or the
  protected legacy prefix.
- Do not use a session-log tail as a default activation or recovery payload.
- Do not let `active-task.md` accumulate per-batch chronology, interval
  enumerations, or per-batch validator lists; keep only the live route, the
  current progress boundary, critical corrections, rejected paths, stable
  boundaries, evidence pointers, and next exact step. Addressable details
  (which batch lives where) belong to index routes, owners, or local
  artifacts.
- Do not let `AGENTS.md` or `CODEX_GUIDANCE.md` become a second project memory
  store; keep it as short operating guidance that points to the memory index.
- Do not turn skill upgrade history into another memory log; keep only durable
  future-session rules in the skill itself.
- Do not start a long approved task without an `active-task.md` anchor.
- Do not continue an interrupted task without reading `active-task.md` first.
- Do not treat a compacted summary as permission to change route when
  `active-task.md` says a different exact next step.
- Do not discard strong user pressure as emotional noise during testing or bug fixing.
- Do not convert ordinary pressure, short acknowledgements, or one-off requests into hard durable rules without explicit absolute wording.
- Do not downgrade explicit user goals, prohibitions, acceptance criteria, or
  corrections into soft pressure.
- Do not claim old source import complete after only creating the current
  memory root or linking the old source.
- Do not revive a previously rejected approach because it looks simpler after compaction.
- Do not opportunistically refactor mature working behavior during stabilization work.
