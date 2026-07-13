# Layout

Use a project-local context workspace that separates active state from durable history.

## Recommended structure

```text
<project-root>/
├── AGENTS.md or CODEX_GUIDANCE.md  # optional auto-loaded operating guidance
└── docs/codex/
    ├── current-context.md
    ├── index.md
    ├── active-task.md   # optional, for long/risky tasks in progress
    ├── session-log.md   # optional, for active investigations
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
├── active-task.md   # optional, for long/risky tasks in progress
├── session-log.md   # optional, for active investigations
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

## Read order

1. `current-context.md`
2. `index.md`
3. Use `index.md` to identify relevant module, pressure, stable-behavior,
   rejected-approach, and regression-guard keywords.
4. `active-task.md` if present and not marked complete
5. `session-log.md` if the current work is active, noisy, or has many tool calls
6. Only the capsules relevant to the current version, module, hypothesis,
   pressure signal, rejected approach, or failure

If `active-task.md` exists but is marked complete, treat it as archived evidence.
Do not resume from its `Next exact step` or `Resume instruction`.

Templates define suggested fields, not a strict schema. Projects may use clearer
local headings, but the retrieval meaning must remain visible: current anchor,
active goal, evidence links, next step, and capsule pointers.

## Update order

1. Update `active-task.md` before starting or resuming a long/risky task.
2. After each logical work unit in long/risky work, refresh `active-task.md`
   before switching focus, running a validation gate, requesting review, or
   entering interruption risk. For rapid edit bursts, use the batching rule in
   `SKILL.md`'s Compaction Interruption Gate.
3. Update `current-context.md` before deliberate compaction or a major phase shift.
4. Update `session-log.md` with the latest actions, pressure signals, errors,
   and tests if the work is still active.
5. Add or update the relevant capsule, including rejected approaches and
   regression guards when they become durable.
6. Refresh `index.md` if navigation, project phase, module protection,
   pressure signals, rejected approaches, or guards changed.

## Resume order after interruption

1. Read `active-task.md` first if it exists and is not complete.
2. Read `current-context.md`.
3. Read `index.md`.
4. Read `session-log.md` and relevant capsules.
5. Build an activation packet from selected index entries and capsules.
6. Compare the intended next action with `active-task.md`; continue only if it
   matches or the user has given a newer instruction.

If `active-task.md` is present but complete, skip it for routing and use it only
as evidence of what was finished previously.

If `active-task.md` is absent but `session-log.md` or `current-context.md`
shows an unfinished task, reconstruct a new `active-task.md` from those files
before continuing. When the reconstructed route is uncertain or conflicts with
the newest user message, ask or revise the anchor before touching code, server
state, or generated artifacts.

## Naming

- Use short version IDs or topic IDs for capsules.
- One capsule should cover one durable question, not an entire project history.
- Keep filenames stable so old chat references still work.
- Use stable module labels in `index.md` so pressure signals and rejected
  approaches can be retrieved by task scope.
- Use module aliases in `index.md` when users and agents refer to the same area
  by different names.

## Validation helper

Run `scripts/check-memory-root.py <memory-root>` to check for missing required
files, missing active next steps, broken capsule references, and weak
stabilization metadata.

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
