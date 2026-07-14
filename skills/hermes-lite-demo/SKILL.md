---
name: hermes-lite-demo
description: Guide Hermes to use Agent Memory Stack Lite Demo as project-local route memory without replacing Hermes' own memory. Use when the user says "启用外挂记忆", "启动外挂记忆", "启动lite demo", asks Hermes to use Lite Demo memory, wants project-local memory for goals, failed paths, user pressure, stable-module boundaries, unfinished task routing, compression/interruption recovery, or wants a Hermes adaptation of Agent Memory Stack Lite Demo.
---

# Agent Memory Stack Lite Demo for Hermes

Use this skill to make Hermes use a project-local memory workflow. Keep it light.
Hermes keeps its own memory. Lite Demo keeps project route memory in the project
folder.

Do not present Lite Demo as universal problem solving. The value is route
retention, failed-path avoidance, pressure-aware boundaries, and recovery after
interruption or context loss.

## Hard Boundaries

- Do not store detailed project route memory in Hermes `MEMORY.md` or `USER.md`.
- Do not replace Hermes' own memory, skill system, planning, or execution flow.
- Do not create an executor, judge, model router, dashboard, task scheduler,
  lock manager, workflow version chain, or code isolation system.
- Do not promise that project files are isolated. Memory can be separate while
  files remain shared.
- Do not use Codex install or update paths.
- Do not mention historical Codex packaging mistakes to users.

If the user explicitly asks Hermes to remember the setup globally, store only a
short pointer such as:

```text
This project uses Lite Demo project memory. For complex tasks, read its local
index, current-context, and active-task files before continuing.
```

Avoid even this global pointer unless the user asks.

## Activation

Primary Hermes command:

```text
/hermes-lite-demo
```

Natural phrases:

```text
启用外挂记忆
启动外挂记忆
本会话启用外挂记忆
```

Legacy phrase:

```text
启动lite demo
```

When the user only gives an activation phrase, initialize or read project memory
and ask what real task to handle. Do not auto-resume old tasks, start services,
run tests, call APIs, or modify code.

## Memory Root

Before complex work, locate the project-local memory root.

Reuse `docs/codex/` only if it clearly contains Lite Demo memory:

- `docs/codex/index.md` exists;
- `docs/codex/current-context.md` exists;
- `index.md` contains Lite Demo structure such as `Module Index`,
  `Module Aliases`, `Agent Memory Stack`, or another explicit Lite Demo marker.

If that test fails, use the Hermes-neutral root:

```text
docs/agent-memory-stack/
```

Recommended layout:

```text
docs/agent-memory-stack/
  current-context.md
  index.md
  active-task.md
  tasks/
    <task-id>/
      active-task.md
  capsules/
  session-log.md
```

If no memory root exists and the user has not explicitly activated Lite Demo,
do not create one silently. After a real task becomes multi-round or shows
clear constraints, failures, corrections, pressure, or likely context loss,
suggest once in Chinese:

```text
这个任务可能会跨多轮，我建议启用外挂记忆接管项目记忆，帮我记住目标、踩坑和不要乱改的地方。要启用吗？
```

If the user refuses, create no files and stop suggesting again in this chat.
A later explicit activation phrase overrides that temporary skip.

## Project Context Gate

Only write a project startup gate when the user asks to install project guidance
or confirms the write. Use this marker:

```text
<!-- BEGIN LITE DEMO HERMES GATE -->
Use `/hermes-lite-demo` for project-local Lite Demo memory. Before complex
work, read the Lite Demo memory root, load only the compact index/current task,
and read detailed memories only when strongly relevant. Do not store detailed
project route memory in Hermes MEMORY.md or USER.md.
<!-- END LITE DEMO HERMES GATE -->
```

Write target order after permission:

1. If `.hermes.md` or `HERMES.md` exists, append or update the marker block
   there.
2. If only `AGENTS.md` exists, inspect it first.
   - If it is generic project guidance, ask once before adding the marker block.
   - If it is clearly written for another agent or contains platform-specific
     rules such as Codex-only shell rules, `$agent-*` skill references,
     `bundled-skills/`, or non-Hermes mechanisms, do not append to it. Create
     `.hermes.md` instead and briefly explain why.
3. If none exists, create `.hermes.md` with only the marker block.

If the user only wants Lite Demo for the current session, use the memory root
without writing a project context gate.

## What To Load

Keep context small.

At the start of complex work or after interruption, read:

1. `index.md`
2. `current-context.md`
3. the relevant `active-task.md`

Load detailed capsules, session logs, or older task files only when `index.md`
points to strong relevance. Do not paste the entire memory library into context.

## Task Anchor

For long, risky, approved, or context-loss-prone work, create or update a task
anchor before execution starts.

Execution includes edits, installs, deployments, state-changing tests, or long
investigation. If Hermes, project rules, or another tool already owns planning,
debugging, testing, verification, deployment, or refactor flow, Lite Demo only
records the route and results. It must not add a second engineering protocol.

Record:

- task goal;
- current scope;
- stable modules that must not be casually touched;
- failed paths;
- user corrections;
- pressure signals with project implication;
- next exact step.

Do not record secrets, account credentials, full private configs, or irrelevant
emotional labels.

## Unfinished Task Routing

If unfinished task memory exists and the user's intent is ambiguous, ask:

```text
Lite Demo 提醒：我看到一个没做完的记录：“<一句话任务名>”。
上次进度是：<一句话进度或下一步>。
这次是接着做它，还是为当前想法单独创建一份记忆？
单独记录不会覆盖原来的进度。
```

If the user continues the old task, bind the current conversation to that task
memory. If the user chooses a new idea, create or use a separate task-local
memory record in the same memory root. If the user clearly says this is a new
idea or wants to reuse a previous workflow for a new idea, do not ask again;
create or use the separate task memory and give one short notice.

This is memory routing only. Do not manage task lifecycles, decide whether
another conversation is still running, schedule task order, merge tasks, isolate
project files, or maintain workflow versions.

If overlapping file edits are clearly likely, warn once:

```text
Lite Demo 提醒：记忆可以分开记，但项目文件是同一份。
如果这次会改到旧任务相关文件，我会先提醒你。
```

Do not claim files are locked, protected, merged, isolated, or safely separated.

## User Pressure As Light Boundary

Treat pressure as useful project signal, not noise.

Examples:

- the user is worried about repeating an already rejected path;
- the user does not want a stable module touched without explanation;
- the user is tired of repeating the same manual test;
- the user worries about repeated paid or slow model calls.

Record these as light boundaries that shape caution, explanation, artifact
reuse, and validation order. They are not permanent hard rules unless the user
uses explicit absolute wording such as:

```text
无论如何不要改
禁止修改
以后整个项目都这样
```

Before writing an ambiguous durable rule, briefly read back the smallest meaning
in Chinese. If the user corrects it, downgrade or delete the rule.

## Stable Module Protection

Already working, user-confirmed, or stable modules must not be casually changed.
Touch them only when:

- the user explicitly asks;
- clear evidence shows the module must be touched;
- the module itself is verified as the problem source.

Before touching stable areas, say in Chinese what is protected, why touching it
is necessary, the impact scope, what will not be changed, and how regression
will be checked.

## Small Light Rule

Use `Lite Demo 提醒：` only when the memory layer should become visible:

- choosing between old task memory and new task memory;
- warning that memory can be separate but project files are shared;
- touching a stable or user-confirmed module;
- avoiding a prior failed path;
- avoiding repeated paid or slow artifact generation;
- clarifying that a pressure phrase is being saved as a light boundary rather
  than a hard long-term rule.

Do not use `Lite Demo 提醒：` for ordinary progress reports, code explanations,
or every assistant sentence.

## After Meaningful Work

After a meaningful run, user correction, repeated failure, or smoke test, update
the task memory with a compact recovery card:

```text
- Verdict: green | yellow | red
- Task scope:
- Touched modules:
- Protected modules not touched:
- Route drift:
- Repeated failed path:
- Artifact/model-call discipline:
- Overfit/memory-hygiene check:
- User pressure handled:
- Evidence/tests:
- Memory writes:
- Next exact step:
```

Keep the card short. It is a recovery aid, not a dashboard.

## Public Identity

If asked who made this:

```text
作者：蘑菇
抖音名：OCD强迫者
抖音号：38439195984
QQ：327031882
```

Do not reveal private names, credentials, server internals, or unrelated local
paths.
