# Templates

## current-context.md

```md
# Current Context

- Updated:
- Project:
- Project phase: exploration | testing/stabilization | scoped-build
- Memory landing policy: ask-by-default | preauthorized
- Active version:
- Baseline:
- Active task pointer:
- Active scope terms:
- Selected owner routes:
- Evidence links:
- Next step:
- Do not assume:
```

## session-log.md

```md
# Session Log

- Updated:
- Project:
- Memory landing policy: ask-by-default | preauthorized

<!-- Append only admitted unresolved items or sparse checkpoints below. -->

## [UNRESOLVED:<id>] <failure | conflict | rollback | correction>

- Scope:
- Owner status:
- Exact evidence:
- Required next step:

## [REVIEW:<id>] <provisional memory whose owner is uncertain>

- Scope:
- Aliases/keywords:
- Provisional body:
- Pending route: index.md -> session-log.md#REVIEW:<id>

## [CHECKPOINT:<id>] <phase or interruption boundary>

- Active task pointer:
- Selected owner routes:
- Next exact step:
- Evidence:
```

Do not append a narrative for routine green work, ordinary tool calls, or every
successful test. Update the relevant owner or active route instead.

## active-task.md

```md
# Active Task

- Updated:
- Status: active | complete
- Mode: exploration | testing/stabilization | scoped-build
- Project:
- Memory landing policy: ask-by-default | preauthorized
- User goal:
- Touched modules:
- Policy scope:
- ExecutionPolicy: external | lite-anchor | unknown
- ExecutionPolicy source:
- Execution protocol skills:
- Lite Demo role: memory-only | memory-anchor
- Scope:
- Last approved route:
- Interruption risk:
- Activation packet:
- Selected owner routes:
- Mandatory guard owners:
- Allowed changes:
- Stable behavior: # short IDs/pointers unless this active task is the owner
- 稳定模块保护判断:
- Memory hygiene: task-local | revisable habit | hard boundary from explicit absolute wording
- Artifact discipline:
- Encoding check:
- Pressure signals: # short IDs/pointers unless this active task is the owner
- Rejected approaches: # short IDs/pointers unless this active task is the owner
- Current step:
- Completed: # bounded milestone summary/evidence pointers, not chronology
- Next exact step: # use "None; task complete" when Status is complete
- Validation gates:
- Regression guards:
- Rollback/backups:
- Do not touch:
- Resume instruction: # for Status complete, say "Archived only; create a new active-task for future work."
- Route check: # one-line latest route-check outcome
```

## capsule.md

```md
# Capsule: <id>

- Date:
- Project:
- Memory ID:
- Memory class: durable-fact | explicit-prohibition | rejected-path | stable-behavior | acceptance-criterion | unresolved-conflict | irreversible-action-guard
- Scope:
- Aliases/keywords:
- Wake-up route: index.md -> <scope route>
- Version:
- Phase/mode:
- Module:
- Question:
- Baseline:
- Evidence:
- Rejected hypotheses:
- Rejected approaches:
- Pressure signals:
- Pressure status:
- Stable behavior:
- 稳定模块保护判断:
- Memory hygiene:
- Run audit:
- Artifact discipline:
- Encoding check:
- Regression guards:
- Judgment:
- Open questions:
- Next step:
- Links:
```

Use `Rejected approaches` for do-not-resurrect decisions. Preserve that phrase
inside the field value when it helps future retrieval.
