# Execution Policy Compatibility Gate

Use this before complex execution, task-anchor creation, or recovery from compression.

Lite Demo does not decide how to do engineering work when another explicit protocol already does. It records how the chosen protocol is going.

## Single Source Of Truth

Write the live policy only in the active task anchor:

```text
Policy scope: <task-id or short task goal>
ExecutionPolicy: external | lite-anchor | unknown
ExecutionPolicy source: user instruction | project AGENTS | triggered execution skill | model-native-workflow | none | conflict
Execution protocol skills: none | <skill names explicitly applied to this task>
Lite Demo role: memory-only | memory-anchor
```

`active-task.md` is authoritative for the active task. `current-context.md` may point to that anchor but must not duplicate the live fields. `index.md` stores task pointers, not live policy. `session-log.md` records only policy changes or conflicts.

Fields left by v0.1.8 in current-context, index, or session-log are migration hints only. Re-evaluate them when a new complex task starts; do not route a new task from stale copies.

`Execution protocol skills` is agent-recorded evidence, not runtime telemetry. Record only skills explicitly triggered, read, and applied to the current task. Do not record available skills, tool-only skills, ignored skills, or skill contents.

## Decision

Inspect only these current-task sources:

- the newest user instruction;
- project-root `AGENTS.md` or equivalent operating rules;
- execution skills explicitly triggered and applied to this task;
- an obvious model-native workflow already being followed in this task.

Set `ExecutionPolicy: external` when one of those sources explicitly owns a debugging, planning, testing, verification, deployment, maintenance, or refactor workflow.

Lite Demo does not judge model strength or score workflow quality. `model-native-workflow` is only an `ExecutionPolicy source` note, not a fourth policy state. Do not use a model name as a direct trigger, and do not add `ExecutionPolicy: model-native`.

In `external` mode:

- do not add a second execution flow;
- do not add plan, test, verification, or deployment steps only because Lite Demo is active;
- record the chosen protocol's goal, route summary, failed paths, validation result, stable-module boundary, pressure signal, and next step.

Set `ExecutionPolicy: lite-anchor` when none of the allowed sources explicitly owns the execution workflow. Absence of an explicit protocol is enough; do not ask the user to prove that no other protocol exists.

`lite-anchor` is adaptive. Start as a light mirror when the agent already has clear scope, boundary, evidence, and next step. Use a fuller anchor only after route drift, repeated failed paths, forgotten user correction, stable-module mistakes, compression recovery failure, or high pressure.

Set `ExecutionPolicy: unknown` only when explicit sources conflict or required project rules cannot be read. Stay memory-only and ask one focused question before complex execution.

## Recheck Triggers

Do not sniff every turn. Re-evaluate and replace the task-scoped fields when:

- a new complex task line starts;
- the user changes or names an execution protocol;
- project operating rules visibly change;
- a new execution skill is explicitly triggered for the task;
- explicit sources conflict with the cached policy.

Do not run broad project scans for protocols.
