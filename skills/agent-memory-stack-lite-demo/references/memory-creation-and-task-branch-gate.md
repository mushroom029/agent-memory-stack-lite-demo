# 记忆库创建与任务分支门

Use this gate before creating project memory for the first time, or before splitting a new task line inside an existing project memory root.

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

Suggest a new task branch when any trigger appears:

- the same new request has taken 2-3 discussion rounds and is still open;
- the user adds multiple constraints, forbidden changes, or stable-module protections;
- a failure path, user correction, or pressure signal appears;
- the new request is not the same task line as the current active anchor;
- the work is likely to compact, pause, resume, or cross sessions.

Ask in Chinese:

```text
这个需求已经独立成一个新任务。
为了避免和当前任务记忆混淆，我建议在同一个 docs/codex/ 记忆库里创建新的任务锚点。
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

Use root `docs/codex/active-task.md` only when no other active task is present or the previous root anchor is complete.

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
