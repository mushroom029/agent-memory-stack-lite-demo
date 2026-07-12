# Task Anchor Gate

Use this gate when the user explicitly allows project-memory/task landing and the task is long, multi-step, risky, approved, or likely to compact.

Apply `execution-policy-compatibility.md` first.

If `ExecutionPolicy: external`, the anchor is a memory mirror of the chosen execution protocol. This includes `ExecutionPolicy source: model-native-workflow`. 不新增第二套执行流程, plan, test route, or validation route.

If `ExecutionPolicy: lite-anchor`, the anchor is Lite Demo's adaptive fallback against compression loss. Use a light mirror when scope, boundary, evidence, and next step are already clear. Use a fuller anchor only after route drift, repeated failed paths, forgotten correction, stable-module mistakes, compression recovery failure, or high pressure.

If `ExecutionPolicy: unknown`, explicit sources conflict or required project rules are unreadable. Keep Lite Demo memory-only and ask one focused question before complex execution.

Before execution starts, create or update:

```text
docs/codex/active-task.md
```

Execution includes:

- code edits;
- file moves;
- installs;
- deployments;
- state-changing tests;
- long investigation branches.

The anchor must include:

- user goal;
- scope;
- policy scope, ExecutionPolicy, source, execution protocol skills, and Lite Demo role;
- Memory hygiene: whether user language is task-local, a revisable habit, or a hard boundary from explicit absolute wording;
- 稳定模块保护判断;
- current step;
- completed steps;
- next exact step;
- allowed changes;
- forbidden changes;
- validation gates;
- rejected paths or failed approaches that should not be retried.

Before rerunning a network call, paid model call, crawl, or expensive generator,
check whether an existing artifact already answers the need. Prefer the existing
artifact unless it is stale, invalid, missing, or the user explicitly asks to
regenerate it. Do not turn this into a visible pre-call ritual for ordinary
API/model use. If the decision matters for recovery, record the artifact path
and reason in the next Run Audit card.

Refresh the anchor:

- after each logical work unit;
- before validation gates;
- before switching modules;
- before pausing;
- after any error that changes the route.

## 稳定模块保护门

已经稳定、已经能用、或用户确认正常的功能/模块，默认不允许模型自行修改。

只有在用户明确要求、当前任务存在必须触碰它的清晰证据链、或它本身是已验证问题来源时，才可以触碰稳定模块。

触碰前必须用中文显式说明：

- 保护的稳定行为是什么；
- 为什么非改不可；
- 证据链是什么；
- 影响范围是什么；
- 明确不改什么；
- 用什么回归检查证明没有改坏。

如果无法用中文说清楚，就把该模块写入 `forbidden changes` 或 `Do not touch`，并选择更窄的方案。

After compression, restart, model switch, or thread reuse, read the anchor before acting. If the newest user instruction conflicts with it, update the anchor first.

Tiny one-shot tasks do not need an anchor unless the user asks to preserve them.

## 自然语言记忆卫生

Before saving a user request, pressure phrase, short acknowledgement, local
failure, or temporary boundary as a long-term project rule, apply
`memory-hygiene-nudge.md`.

Default to task-local or revisable memory. Hard boundaries require explicit
absolute wording. User correction downgrades or removes the memory immediately.
