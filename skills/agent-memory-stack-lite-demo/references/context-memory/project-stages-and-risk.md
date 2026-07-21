# Project Stages And Risk

Use this reference when the project has moved beyond initial construction, the
user is testing real behavior, regressions are repeating, or user pressure is
high.

## Core rule

User pressure is a risk signal and requirement tendency, not noise. It is also a
weighted constraint, not an absolute command to stop acting.

## Modes

- `exploration`: Early project shaping. Codex may infer missing requirements,
  propose design, and reshape implementation to help the user discover what they
  want.
- `testing/stabilization`: The user is testing, reporting bugs, or reacting to
  regressions. Protect mature working behavior. Make minimal scoped changes
  unless the user requests expansion, a logic conflict requires change, or a
  verified bug requires change.
- `scoped-build`: The user explicitly requests expansion or refactor after some
  behavior is already stable. State the build scope and protected areas before
  editing.

Modes can be project-wide or module-specific. A stabilized module can coexist
with an exploratory module.

## Mode transitions

- Enter `testing/stabilization` when the user starts hands-on testing, reports
  bugs, runs acceptance checks, complains about repeated regressions, or asks
  for follow-up fixes on partly working behavior.
- Enter `scoped-build` when the user explicitly asks for expansion, redesign, or
  refactor after some behavior is already stable.
- Mark a module stable when it has passed user-visible testing or has worked
  normally across multiple related fixes.
- Repeated same-category pressure twice or more moves the affected module into
  `testing/stabilization` until resolved.
- A module can leave strict stabilization when regression guards pass and the
  related pressure signals are marked `historical` or `resolved`.

`Same-category pressure` means the same affected module plus the same rejected
behavior type, such as repeated route drift, repeated resurrection of a rejected
approach, repeated breakage of a stable workflow, or repeated unrequested
refactor. `Regression guards pass` means the user explicitly confirms the
regression is fixed, the associated automated test/check passes, or the module
works normally across later related fixes.

## Pressure escalation

- One strong pressure signal: slow down, restate the target, list allowed scope
  and do-not-touch items, then proceed with a narrow fix.
- Repeated same-category pressure: treat it as an agent behavior problem and
  enter testing/stabilization discipline for the affected module.
- Module-specific pressure: constrain that module's changes; do not freeze the
  whole project.
- Explicit user request for expansion or refactor: enter `scoped-build`, state
  the scope, and preserve unrelated stable behavior.

## Pressure severity

- `low`: Preference, mild concern, or a one-off clarification that does not yet
  constrain implementation.
- `medium`: A testing conclusion, explicit "do not do this again" feedback, or
  a pressure signal tied to a module or workflow.
- `high`: Repeated regression, broken user trust, real-use workflow damage, or
  strong pressure that identifies an agent behavior pattern.

If the user explicitly corrects the same behavior twice, or expresses strong
frustration after a recorded correction was ignored, immediately create or
update a `mandatory-guard` or `correction-guard` owner with wake-up terms. Do
not leave it as apology-only chat or pressure-only evidence.

Only record pressure when it points to project behavior, user-facing pain,
testing conclusions, repeated regressions, or required agent discipline. Do not
record free-floating emotion with no project implication.

Before turning pressure, one local failure, a temporary request, or a short
acknowledgement into durable memory, mark the conclusion as task-local or
revisable unless the user used explicit absolute wording such as `禁止修改` or
`以后整个项目都这样`.

Record examples:

- "This broke X again" as regression evidence.
- "Do not change Y; it works" as stable behavior protection.
- "I asked for A, you built B" as requirement drift or route drift.
- Strong frustration tied to a module, repeated failure, or agent behavior
  pattern as a pressure signal.

Do not record examples:

- General frustration with no project implication.
- Clarification requests.
- Thanks, acknowledgments, or casual tone.

## What to record

Record pressure as project memory, not as a character judgment about the user.

```md
- Pressure signal:
  - Date:
  - Affected module:
  - User-facing pain:
  - Rejected behavior:
  - Inferred design constraint:
  - Required agent behavior:
  - Severity: low | medium | high
  - Status: active | historical | resolved
  - Recurrence:
  - Evidence links:
```

## Stable behavior protection

In `testing/stabilization`, mature working behavior must not be changed unless:

- the user asks for that change;
- the current fix has a clear logic conflict with that behavior;
- the behavior is a verified bug.

If touching a stable module, write the stable behavior and regression guard
before editing.

## 稳定模块保护门

已经稳定、已经能用、或用户确认正常的功能、模块、流程、样式和数据结构，默认受保护。不要因为顺手优化、审美偏好、架构洁癖或无关重构去改它。

只有三种情况可以触碰稳定区域：

- 用户明确要求修改它；
- 当前任务无法完成，并且有清晰证据链表明必须触碰它；
- 它本身是已验证的问题来源。

触碰稳定区域前，必须用中文显式说明。不要输出隐藏推理，只输出可审查判断：

- 保护的稳定行为是什么；
- 为什么这次非触碰不可；
- 证据链是什么；
- 本次只改哪些文件、模块或行为；
- 明确不改哪些稳定区域；
- 用什么回归检查证明没有改坏。

如果无法用中文说清楚以上内容，就把该稳定区域写入 `forbidden changes`、`Do not touch` 或回归保护项，并选择更窄的方案。

## Negative evidence

Rejected approaches are durable evidence. Record:

- what was tried or proposed;
- why the user or tests rejected it;
- what regression it caused;
- what guard prevents resurrection.

Do not resurrect an old approach after compaction because it looks simpler in
isolation.

## Pressure aging

- `active`: Must shape the current activation packet when the touched module is
  involved.
- `historical`: No longer narrows ordinary fixes, but still prevents resurrecting
  rejected approaches.
- `resolved`: Kept as evidence; only reactivate if the same pattern returns.

Downgrade pressure only when the user accepts the replacement behavior, related
regression guards pass, or the module works normally across later fixes.

## Activation packet protocol

Before acting after resume, compaction, model switch, or a risky request:

1. Read `active-task.md` if present and active.
2. Read `current-context.md`.
3. Read the full keyword/tag map in `index.md`.
4. Identify touched modules and related phase, stable behavior, pressure,
   rejected approach, and guard entries.
5. Open every matched owner and mandatory guard. Read `session-log.md` only for
   an exact unresolved route, source conflict, or remaining evidence gap; use
   an ID search or bounded range, never a tail chosen only by recency.
6. Produce a short activation packet using [activation-packet-template.md](activation-packet-template.md):

```md
# Activation Packet

- Phase/mode:
- Current task:
- Touched modules:
- Selected memories:
- Surprise non-matches:
- Stable behavior:
- Pressure signals:
- Rejected approaches:
- Allowed changes:
- Forbidden opportunistic changes:
- Regression guards:
- Next exact step:
```

If no memories are selected, explain why. If the task touches a module named in
`index.md`, do not claim no relevant memory until its pressure signals, stable
behavior, rejected approaches, and guard entries have been checked. Only list
`Surprise non-matches` when an index entry matched a touched module or alias but
was judged irrelevant after inspection.
