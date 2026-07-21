# Memory Hygiene Nudge

Use this before turning ambiguous conversational language into durable project
memory. For explicit user goals, prohibitions, acceptance criteria, or
corrections, use [user-requirement-ledger.md](user-requirement-ledger.md)
first.

This is not a formal audit protocol. It is a small guard against writing a
temporary request, pressure phrase, local failure, or short acknowledgement as a
permanent project rule.

## Explicit Instruction Exception

Explicit user goals, prohibitions, acceptance criteria, and corrections are
not weak memory merely because they arrive with pressure, frustration, repeated
wording, or small wording changes. Treat them as requirements by default and
give them an owner, route, and mandatory recall when they affect future work.

If the scope of an explicit instruction is unclear, record `pending-review` or
ask one focused question. Do not downgrade it to a soft preference just because
it is emotionally expressed.

## Core Rule

Default to weak memory.

If a note comes from one request, one failure, one pressure phrase, one short
reply, or one temporary boundary, record it as task-local or revisable unless
the user made an explicit goal, prohibition, acceptance criterion, or
correction.

Hard boundaries require clear absolute language such as:

- `无论如何不要改`
- `禁止修改`
- `以后整个项目都这样`
- `保存为长期边界`

Short replies such as `好`, `可以`, `继续`, `收到`, `知道了`, `都行`, silence, or
an unrelated next request do not create a hard durable rule.

Absolute wording is required for a permanent project-wide hard boundary. It is
not required to obey a direct current-task prohibition or acceptance gate.

## When To Speak

Stay silent for ordinary notes.

Use one short Chinese readback only when you are about to write a durable
project rule from ambiguous language:

```text
我先把它记成这个任务里的默认习惯，不是死规矩；后面证据变了我会再提醒你。
```

If the user corrects you, downgrade or remove the memory immediately.

If new evidence conflicts with a revisable preference, reopen it instead of
blindly following the old note.

## Where To Store

For active work, add a short `Memory hygiene` line to `active-task.md`, for
example:

```text
- Memory hygiene: Treat "这块别动" as current-task protection, not a permanent hard boundary.
```

For durable capsules, state whether the saved rule is:

- task-local;
- revisable project habit;
- hard boundary from explicit absolute wording.
- explicit requirement from a user goal, prohibition, acceptance criterion, or
  correction.

## Do Not Add

Do not add:

- formal risk labels;
- a fixed cycle counter;
- a disclosure queue;
- a state machine for short acknowledgements;
- a mandatory benefit/cost template;
- a second test, plan, or verification route;
- an external-protocol hook.

This nudge affects memory writes only. It does not take execution ownership.
