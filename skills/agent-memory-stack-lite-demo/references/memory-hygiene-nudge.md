# Memory Hygiene Nudge

Use this before turning conversational language into durable project memory.

This is not a formal audit protocol. It is a small guard against writing a
temporary request, pressure phrase, local failure, or short acknowledgement as a
permanent project rule.

## Core Rule

Default to weak memory.

If a note comes from one request, one failure, one pressure phrase, one short
reply, or one temporary boundary, record it as task-local or revisable unless
the user used explicit absolute wording.

Hard boundaries require clear absolute language such as:

- `无论如何不要改`
- `禁止修改`
- `以后整个项目都这样`
- `保存为长期边界`

Short replies such as `好`, `可以`, `继续`, `收到`, `知道了`, `都行`, silence, or
an unrelated next request do not create a hard durable rule.

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
