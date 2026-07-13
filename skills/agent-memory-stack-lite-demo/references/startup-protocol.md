# 启用外挂记忆

Use this when the user says `启用外挂记忆`, `启动外挂记忆`, `本会话启用外挂记忆`, or the legacy phrase `启动lite demo`.

These phrases are activation commands for the installed memory-only demo. Do not ask the user to paste the longer onboarding prompt.

## Explicit Activation Overrides Skip

If Codex previously suggested Lite Demo and the user refused, that refusal is only a current-chat quieting signal. It is not project memory, not an AGENTS rule, and not a stored preference. A later `启用外挂记忆`, `启动外挂记忆`, or `本会话启用外挂记忆` immediately overrides the temporary skip and runs this startup protocol.

## Activation-Only Barrier

If the user message is exactly or effectively only an activation phrase, activate memory only.

Do not:

- run shell commands;
- edit files beyond starter memory files when memory landing is allowed;
- start APIs, dev servers, Electron helpers, or other services;
- run tests;
- continue an old `active-task.md` next step.

After reading existing memory, if an active task exists, summarize it briefly and ask whether to resume it. If no active task exists, ask what real project task should run under 外挂记忆.

If the user includes a concrete task in the same message, for example `启用外挂记忆，并继续修复登录失败`, then proceed with the task after applying the normal task-anchor and stable-module gates.

## Startup Steps

1. State briefly in Chinese that 外挂记忆 is active and memory-only.
2. Use Lite Demo's internal memory workflow references for memory mechanics.
3. Identify the current writable project root. If no project root is clear, ask for the target project path in one short question.
4. If `docs/codex/` exists, read the active task and current context, then use the compact `index.md` routing terms to open only strongly relevant capsules, guards, failed paths, and pressure notes. Do not execute the active task unless the user included a task or confirms resume.
5. If `docs/codex/` does not exist and the project root is clear, treat the activation phrase as explicit memory landing permission. Create starter `docs/codex/current-context.md`, `docs/codex/index.md`, `docs/codex/tasks/`, and `docs/codex/capsules/`, then report the paths and that Lite Demo will avoid intentionally adding secrets to memory.
6. Before nontrivial execution after a concrete task or resume confirmation, silently sniff for an existing engineering protocol with `execution-policy-compatibility.md`. Keep memory active; activate Lite Demo's fallback engineering protocol only when no existing protocol owns the flow. Create or update the task anchor with the internal result.
7. Use the anchor as a memory mirror for an external protocol, including a model-native workflow source note, or as the adaptive lite-anchor when no explicit execution protocol exists. Ask only when explicit sources conflict or required project rules cannot be read.
8. Apply the stable-module protection gate before touching working modules.
9. If no concrete task was included, ask the user what real project task to run under 外挂记忆, or whether to resume the active task if one exists.

## Do Not

- Do not ask for secret credentials or external executor setup.
- Do not claim universal task success.
- Do not create a second memory database.
- Do not hide file writes; report the memory path and purpose.
- Do not treat the word `启动` inside the legacy phrase as permission to start a local service.
- Do not rescan every turn for other protocols; reuse the active task's policy until a recheck trigger appears.
- Do not ask the user to install or activate a second memory skill.
- Do not expose `ExecutionPolicy`, capsule, anchor, fingerprint, or routing-index terminology in ordinary user replies.
