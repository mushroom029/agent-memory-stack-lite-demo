# Layout

Use a project-local context workspace that separates active state from durable history.

## Recommended structure

```text
<project-root>/
├── AGENTS.md or CODEX_GUIDANCE.md  # optional auto-loaded operating guidance
└── docs/codex/
    ├── current-context.md
    ├── index.md
    ├── routes/                      # one-level cold version/event route pages
    ├── active-task.md   # optional, for long/risky tasks in progress
    ├── session-log.md   # sparse initialization/takeover proof plus admitted items
    ├── tasks/           # optional, parallel task anchors
    │   └── <task-id>/active-task.md
    └── capsules/
        ├── C13.md
        ├── C14.md
        └── ...
```

The project-root instruction file is not part of the memory root. Keep it short
and use it only for operating rules and a pointer to the memory index.

Memory root:

```text
docs/codex/
├── current-context.md
├── index.md
├── routes/          # optional one-level cold version/event route pages
├── active-task.md   # optional, for long/risky tasks in progress
├── session-log.md   # sparse initialization/takeover proof plus admitted items
├── tasks/           # optional, parallel task anchors
│   └── <task-id>/active-task.md
└── capsules/
    ├── C13.md
    ├── C14.md
    └── ...
```

If the project already uses a different stable docs root, keep the same substructure there.

## Project-root instruction file

Codex normally auto-loads `AGENTS.md` when present. Some projects may prefer a
more human-readable name such as `CODEX_GUIDANCE.md`; use that only after
adding the configured fallback and verifying it in the real project directory:

```toml
project_doc_fallback_filenames = ["CODEX_GUIDANCE.md"]
```

Verify with:

```powershell
pwsh -NoLogo -NoProfile -Command 'codex debug prompt-input "probe"'
```

The instruction file should contain only short operating guidance:

- shell and encoding rules;
- remote access and deployment safety;
- maintenance behavior constraints;
- a pointer such as: `For long, risky, resumed, or regression-sensitive work,
  read docs/context-memory/index.md and build an activation packet before
  acting.`

Do not put chronological history, failed-approach logs, pressure signals, or
version evidence in `AGENTS.md` or `CODEX_GUIDANCE.md`. That content belongs in
the memory root and capsules. Do not create a parallel root-level
`PROJECT_MEMORY.md` unless it is only a short pointer to the memory root.

## Path discovery

Before creating a context workspace, check for existing roots in this order:

1. `docs/context-memory/`
2. `docs/codex/`
3. `docs/context/`

Reuse the first existing root. If none exists, default to `docs/codex/`.

Do not silently create the first memory root unless the user explicitly asks for
project memory, install, or landing, or the project has `Memory landing policy:
preauthorized`. Otherwise ask first and explain that the root stores task goals,
stable-module protection, failed paths, user corrections, and next steps.

If a memory root already exists and a new task line becomes complex, keep it
inside the same root. Prefer `tasks/<task-id>/active-task.md` for parallel
anchors and add a pointer in `index.md`; do not create a second database.

In this situation Lite Demo is doing memory routing only. It binds the current
conversation to an existing or new task memory; it does not decide whether an old task is still running, schedule tasks, merge tasks, isolate code files, or
maintain workflow versions.

When an unfinished task makes the route ambiguous, ask:

```text
Lite Demo 提醒：我看到一个没做完的记录：“<一句话任务名>”。
上次进度是：<一句话进度或下一步>。
这次是接着做它，还是为当前想法单独创建一份记忆？
单独记录不会覆盖原来的进度。
```

If the user clearly asks for a new task or to use the same method again, do not
ask again. Create or reuse a task-local anchor, keep the old task memory
unchanged, and record only compact task pointers in `index.md`.

Use `Lite Demo 提醒：` only for memory routing, memory/risk boundaries, or clear
overlap warnings. Do not use it for ordinary progress reports or code
explanations, and do not replace every "我" with the skill name.

## Read order

1. `current-context.md`
2. `index.md`
3. Derive the touched module/entity/behavior/version/risk, then use `index.md`
   to resolve every matching current `owners=` and `mandatory=` pointer. If a
   matched route has `history=`, scan that one route page and open only its
   precisely matched version/event owners. Do not stop at a top-k subset.
4. `active-task.md` if present and not marked complete
5. Every matched current and historical owner, with mandatory guard owners
   opened first
6. The most recent 30-60 `session-log.md` lines or a few sparse checkpoints as
   a recency probe; this is not a cap on selected relevant memory and never
   means reading a long log in full by default

If `active-task.md` exists but is marked complete, treat it as archived evidence.
Do not resume from its `Next exact step` or `Resume instruction`.

Templates define suggested fields, not a strict schema. Projects may use clearer
local headings, but the retrieval meaning must remain visible: current anchor,
active goal, evidence links, next step, and capsule pointers.

When multiple task memories exist, treat `current-context.md` as a project
router rather than one global next-step store. Each task's goal, progress,
failed paths, pressure, temporary constraints, and next exact step belong in
that task's own `active-task.md`.

## Update order

1. Update `active-task.md` before starting or resuming a long/risky task.
2. After each logical work unit in long/risky work, refresh `active-task.md`
   before switching focus, running a validation gate, requesting review, or
   entering interruption risk. For rapid edit bursts, use the batching rule in
   `SKILL.md`'s Compaction Interruption Gate.
3. Update `current-context.md` before deliberate compaction or a major phase shift.
4. Choose one body owner for each durable fact and update it once.
5. Refresh `index.md` with a compact scope/alias/keyword -> current owner,
   mandatory guard, optional one-level history route. A
   durable write is incomplete until this wake-up route exists.
6. Append to `session-log.md` only for an unresolved failure/conflict,
   rollback, unpromoted correction, `[REVIEW:<id>]` provisional body, or sparse
   recovery checkpoint. Routine green work receives no narrative entry.

## Resume order after interruption

1. Read `active-task.md` first if it exists and is not complete.
2. Read `current-context.md`.
3. Read `index.md`.
4. Resolve the touched scope through `index.md` and open every matched owner.
5. Use the recent `session-log.md` tail only as a recency probe. Search or read
   a bounded older range when an owner points to evidence, a route misses, a
   conflict appears, or information is missing.
6. Build an activation packet from the selected owners and compact routes.
7. Compare the intended next action with `active-task.md`; continue only if it
   matches or the user has given a newer instruction.

If `active-task.md` is present but complete, skip it for routing and use it only
as evidence of what was finished previously.

If `active-task.md` is absent but `session-log.md` or `current-context.md`
shows an unfinished task, reconstruct a new `active-task.md` from those files
before continuing. When the reconstructed route is uncertain or conflicts with
the newest user message, ask or revise the anchor before touching code, server
state, or generated artifacts.

The reconstruction starts from `current-context.md`, the recent log tail, and
indexed capsules. Never read a long session log in full by default. Use the
internal `scripts/read-session-log.py` helper or equivalent tail/search/range
operations for older evidence. These reads must not modify the append-only log.

## Naming

- Use short version IDs or topic IDs for capsules.
- One capsule should cover one durable question, not an entire project history.
- Keep filenames stable so old chat references still work.
- Use stable module labels in `index.md` so pressure signals and rejected
  approaches can be retrieved by task scope.
- Use module aliases in `index.md` when users and agents refer to the same area
  by different names.
- Give each durable body a stable `Memory ID`, `Memory class`, `Scope`, and
  `Wake-up route`. Other files keep pointers rather than copied prose.

## Validation helper

Run `scripts/route-memory.py <memory-root> --touch <action>` to resolve matching
current owners, mandatory guards, and precise one-level history routes. Run
`scripts/check-memory-root.py <memory-root>` to check missing
routes/owners, broken pointers, stranded review entries, repeated live fields,
cross-layer narrative duplication, and weak stabilization metadata.

For an existing root, run `scripts/takeover-memory.py inspect <memory-root>`,
then `apply`, then `verify`. The helper records the old byte length and prefix
SHA256 and appends one idempotent current-version checkpoint to the same
`session-log.md`. It
must not rename, rotate, or rewrite the old log.

## Index recovery

If `check-memory-root.py` reports missing capsules, broken capsule references,
or obvious index drift:

1. List capsule files under `capsules/`.
2. Rebuild `index.md` from existing capsules, `current-context.md`, and any
   active `active-task.md`.
3. Mark missing capsule references as `[missing]` or `[archived]` instead of
   silently deleting the negative evidence they may contain.
4. Record the discrepancy and repair in `session-log.md` when a session log is
   active.
5. Re-run the validator after repair.
