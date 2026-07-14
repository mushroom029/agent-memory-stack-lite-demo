# 记忆库创建与任务分支门

Use this gate before creating project memory for the first time, or before
routing the current conversation to an existing or new task memory inside an
existing project memory root.

## No Existing Memory Root

If the project has no `docs/codex/`, do not create it silently.

If the user has not activated memory but the same real task has gone 2-3
meaningful rounds, or clear constraints, failures, corrections, pressure, or
likely compression appear, make one plain suggestion:

```text
这个任务可能会跨多轮，我建议启用外挂记忆接管项目记忆，帮我记住目标、踩坑和不要乱改的地方。要启用吗？
```

If the user says `不用`, `先别`, `算了`, `不要`, or otherwise refuses, do not
create `docs/codex/`, do not write AGENTS, do not write project memory, and do
not store a refusal marker. Treat it only as a current-chat skip: 本会话内不再主动询问.

If the user gives a new task instead of answering, do not silently enable memory.
Proceed without memory landing unless the user later explicitly activates it.

A later `启用外挂记忆`, `启动外挂记忆`, or `本会话启用外挂记忆` overrides the
current-chat skip immediately.

Create it only when:

- the user says `启用外挂记忆`, `启动外挂记忆`, `本会话启用外挂记忆`, or the legacy phrase `启动lite demo`;
- the user explicitly asks to install the demo, create memory, save project memory, or allow landing;
- project guidance was installed with a preauthorization policy;
- the user confirms after Codex asks.

Ask in Chinese:

```text
这个任务已经超过简单问答，后续可能会压缩、反复试错或产生多个约束。
我建议创建本地项目记忆库 docs/codex/。
它只记录任务目标、稳定模块保护、失败路径、用户修正和下一步，不记录密钥。
是否创建？
```

## Existing Memory Root

If `docs/codex/` already exists, Codex may be more proactive.

## Memory Routing Only

This feature only answers one question: 当前会话该使用哪份任务记忆.

It does not manage task lifecycles, decide whether another conversation is
still running, schedule task order, merge tasks, isolate project files, or
maintain workflow versions.

If an unfinished task exists and the user's intent is ambiguous, ask in plain
Chinese:

```text
Lite Demo 提醒：我看到一个没做完的记录：“<一句话任务名>”。
上次进度是：<一句话进度或下一步>。
这次是接着做它，还是为当前想法单独创建一份记忆？
单独记录不会覆盖原来的进度。
```

- If the user continues the old task, bind the current conversation to that task memory.
- If the user chooses a new task, create or use a separate task-local anchor in the same memory root and leave the old task memory unchanged.
- If the user already clearly says this is a new idea, another task, or "按上次的做法再做一次", do not ask again. Create or use the separate task memory and give one short notice.
- Do not expose task IDs, anchors, capsules, routing indices, workflow pointers, or execution-policy terms to ordinary users.
- Use `Lite Demo 提醒：` only for memory routing, memory/risk boundaries, or clear overlap warnings. Do not add it to ordinary task talk, code explanations, progress reports, or every assistant sentence. Do not replace every "我" with the skill name.

Suggest a new task memory route when any trigger appears:

- the same new request has taken 2-3 discussion rounds and is still open;
- the user adds multiple constraints, forbidden changes, or stable-module protections;
- a failure path, user correction, or pressure signal appears;
- the new request is not the same task memory line as the current active anchor;
- the work is likely to compact, pause, resume, or cross sessions.

Ask in Chinese:

```text
这个需求已经独立成一个新任务。
为了避免和当前任务记忆混淆，我建议在同一个 docs/codex/ 记忆库里单独记录。
它会记录目标、范围、稳定模块保护、失败路径和下一步。
是否允许落盘？
```

## Where To Write

Do not create a second memory database.

Use the same project memory root:

```text
docs/codex/
```

For parallel task lines, prefer:

```text
docs/codex/tasks/<task-id>/active-task.md
```

Then add a pointer in:

```text
docs/codex/index.md
```

Use root `docs/codex/active-task.md` only when no other active task is present
or the previous root anchor is complete.

Root `current-context.md` is a project router in concurrent use. Do not store
one global next step there when multiple task memories exist. Store each task's
goal, progress, failed paths, pressure, temporary constraints, and next exact
step in that task's own `active-task.md`.

## Workflow Memory

A reusable workflow is shared memory only when it is already validated or the
user clearly asks to save/reuse it. A new task may reference that shared memory,
but its run-specific progress, failures, pressure, and next step stay task-local.

If the new task adjusts the workflow, record the adjustment first as a
task-local suggestion. Promote it to the shared workflow only when the user
clearly says to keep it as the new way. Do not create a W1 -> W2 -> W3 workflow
version chain, migration plan, automatic switch recommendation, or user-facing
workflow manager.

Memory isolation is not code isolation. If a task edits real project files,
those edits happen in the shared workspace. Lite Demo may record source and
warn once only when there is clear evidence of overlapping file/module edits;
it must not promise to prevent conflicts.

Use ordinary Chinese for the warning:

```text
Lite Demo 提醒：记忆可以分开记，但项目文件是同一份。
如果这次会改到旧任务相关文件，我会先提醒你。
```

Do not claim that Lite Demo has protected, locked, isolated, merged, or safely
separated code files. It only records and routes memory.

## Preauthorization

If `current-context.md` or `index.md` says:

```text
Memory landing policy: preauthorized
```

Codex may create or update task anchors automatically after the trigger. It must still tell the user:

- why the anchor was created;
- which path was written;
- what was recorded;
- how to switch back to ask-before-write mode.

Default policy is:

```text
Memory landing policy: ask-by-default
```

## What To Record

Record only task-useful state:

- task goal;
- scope;
- stable-module protection;
- failed paths;
- user corrections;
- pressure signals with project implication;
- next exact step.

Do not record secrets, account credentials, full private configs, or irrelevant emotional labels.
