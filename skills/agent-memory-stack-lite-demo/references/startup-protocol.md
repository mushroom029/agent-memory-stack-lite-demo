# 启用外挂记忆

Use this when the user says `启用外挂记忆`, `启动外挂记忆`, `本会话启用外挂记忆`, or the legacy phrase `启动lite demo`.

These phrases are activation commands for the installed memory-only demo. Do not ask the user to paste the longer onboarding prompt.

## Explicit Activation Overrides Skip

If Codex previously suggested Lite Demo and the user refused, that refusal is only a current-chat quieting signal. It is not project memory, not an AGENTS rule, and not a stored preference. A later `启用外挂记忆`, `启动外挂记忆`, or `本会话启用外挂记忆` immediately overrides the temporary skip and runs this startup protocol.

## Legacy Startup Choice Gate

When activation finds an existing memory root that does not have current
0.2.17-compatible completion proof, do not silently reorganize meaningful old
memory unless the user already said to inherit, reorganize, migrate, repair, or
continue from old memory. First ask one ordinary Chinese question:

```text
Lite Demo 发现这个项目已有旧版记忆：<path>

请选择：
A. 继承并升级整理旧记忆（推荐）
   保留旧文件不删除，把有价值的旧记忆整理进 0.2.17 的当前层、路线层、记忆 owner、派生检索指针；不执行旧任务。

B. 全新启动
   不接管旧记忆，只从现在开始建立新的 0.2.17 记忆；旧记忆保留为冷档，默认不参与召回，以后仍可手动继承。
```

If the user chooses A, automatically apply
[automatic-legacy-takeover.md](automatic-legacy-takeover.md) and do not ask for
a second migration command. If the user chooses B, preserve the old memory
bytes, record a short fresh-start decision, do not claim old-memory
inheritance, and do not default-recall the old root. A later explicit inherit
or migrate request reopens [legacy-source-import.md](legacy-source-import.md)
against the preserved source.

This gate is skipped only when the current user message already contains an
explicit inherit/reorganize/migrate/repair intent, or when helper verification
proves the memory root is already complete under the installed rules.

## Referenced Legacy Source Barrier

If the user names an old conversation, damaged conversation, failed
conversation, old project, archive, old memory folder, or says to inherit,
reorganize, or move old memory into the current conversation, read
[legacy-source-import.md](legacy-source-import.md) before creating a blank
current memory root.

This includes ordinary phrases such as `整理旧会话记忆到当前会话`,
`旧会话损坏，当前会话接管`, `继承旧版本记忆`, and `把旧记忆迁到现在这个会话`.
Treat the referenced old source as a legacy source first. If the source cannot
be found or multiple sources match, use Friendly Legacy Discovery before asking
the user to type a filesystem path. Do not initialize a new `docs/codex/` and claim takeover while the referenced old source was never inventoried.

## Friendly Legacy Discovery

Use this when the user wants inheritance/reorganization/repair but no current
memory root or exact referenced source is already available. The user should
not have to find `docs/codex/` by hand.

First run bounded, metadata-first candidate discovery:

- check the current directory, the resolved project root, and their parent
  chain for `docs/codex/`, `docs/context-memory/`, or `docs/context/`;
- check paths explicitly visible in the user message, open files, current
  project AGENTS guidance, or installed Lite Demo archive metadata;
- read only enough metadata to list candidates: path, root kind, nearest
  project folder, and last write time. Do not read long memory bodies, session
  logs, or project content before the user chooses a candidate.

If candidates are found, ask the user to choose from a short numbered list and
include `全新启动` as the last option. Do not expose schema, checkpoint, or
routing jargon in that question.

If no candidate is found, ask one ordinary Chinese question with simple choices:
return to the old project conversation and say `启用外挂记忆`, allow a broader
discovery pass over named/common Codex project locations, or start fresh in the
current project. A broader discovery pass is opt-in: say which top-level paths
will be scanned before scanning, list only candidates until one is selected,
and never perform silent whole-machine discovery.

## Activation-Only Barrier

If the user message is exactly or effectively only an activation phrase, activate memory only.

One memory-only exception is allowed after the Legacy Startup Choice Gate:
when the user chooses inheritance, or the activation phrase already includes
inherit/reorganize/migrate/repair intent, automatically apply
`automatic-legacy-takeover.md` before the normal activation response. This may
reorganize only memory files. It must not resume or execute the old task.

Do not:

- run general shell or business commands. The bundled memory-only
  `initialize`, `inspect`, `apply`, `verify`, route, and checker helpers are
  explicitly allowed inside the discovered memory root;
- edit business/project files; memory starter files and one-time legacy-memory
  takeover are allowed inside the discovered memory root;
- start APIs, dev servers, Electron helpers, or other services;
- run tests;
- continue an old `active-task.md` next step.

After reading existing memory, if an active task exists, summarize it briefly and ask whether to resume it. If no active task exists, ask what real project task should run under 外挂记忆.

If the user includes a concrete task in the same message, for example `启用外挂记忆，并继续修复登录失败`, then proceed with the task after applying the normal task-anchor and stable-module gates.

## Startup Steps

1. State briefly in Chinese that 外挂记忆 is active and memory-only.
2. Use Lite Demo's internal memory workflow references for memory mechanics.
   Locate helper scripts from the installed/bundled skill directory, not from
   the current working directory. If the cwd is not the skill folder, resolve
   `takeover-memory.py`, `route-memory.py`, `read-session-log.py`, and
   `check-memory-root.py` under the loaded `$agent-memory-stack-lite-demo`
   skill's `scripts/` directory before running them.
3. If the message references an old conversation, damaged conversation, old
   project, archive, or legacy memory source, apply the Referenced Legacy
   Source Barrier before normal root creation or task routing.
4. Identify the current writable project root. If no project root is clear, ask
   the user to open or choose the target project, not to locate an internal
   memory folder.
5. Discover the project memory root. Reuse the first existing root among
   `docs/codex/`, `docs/context-memory/`, and `docs/context/`. These older
   layouts are valid legacy roots, including projects that were originally
   run with the standalone `context-memory-index` skill. If the current
   directory appears to be a project subdirectory, check the parent chain before
   deciding that no project memory exists. Create only `docs/codex/` for a
   brand-new root.
6. If a memory root exists, read
   [automatic-legacy-takeover.md](automatic-legacy-takeover.md) and run its
   one-time detection. If takeover is required, apply the Legacy Startup Choice
   Gate before modifying memory unless the current message already explicitly
   asks for inheritance/reorganization/migration/repair. Complete required
   legacy takeover only after that inheritance path is authorized. Then read the
   active task and current context and follow the compact owner routes. Do not
   execute the old task unless the user included a task or confirms resume.
   If the root was created during the current conversation or test replay by
   the bundled `initialize` helper and `inspect` reports a verified
   `fresh-initialization` checkpoint with `takeover_required: false`, treat
   entries written after that checkpoint as current-session memory, not legacy
   history. Do not create `legacy-destinations.md` merely because an
   activation-only phrase arrives after earlier replay messages.
7. If no memory root exists and the project root is clear, branch on intent.
   For an activation-only fresh start, treat the activation phrase as explicit
   memory landing permission. Run bundled `takeover-memory.py initialize
   <memory-root>` so one tool atomically creates the starter context, index,
   directories, sparse initialization checkpoint, and schema. Do not hand-write
   the schema before this command. Then report the path and that Lite Demo will
   avoid intentionally adding secrets to memory. If the user asked to inherit,
   reorganize, migrate, repair, or continue from old memory, run Friendly
   Legacy Discovery first and do not create a blank root unless the user chooses
   fresh start.
8. Before nontrivial execution after a concrete task or resume confirmation, silently sniff for an existing engineering protocol with `execution-policy-compatibility.md`. Keep memory active; activate Lite Demo's fallback engineering protocol only when no existing protocol owns the flow. Create or update the task anchor with the internal result.
9. Use the anchor as a memory mirror for an external protocol, including a model-native workflow source note, or as the adaptive lite-anchor when no explicit execution protocol exists. Ask only when explicit sources conflict or required project rules cannot be read.
10. Apply the stable-module protection gate before touching working modules.
11. If no concrete task was included, ask the user what real project task to run under 外挂记忆, or whether to resume the active task if one exists.

## Do Not

- Do not ask for secret credentials or external executor setup.
- Do not claim universal task success.
- Do not create a second memory database.
- Do not hide file writes; report the memory path and purpose.
- Do not ask an old user for a second migration command after they have chosen
  inheritance, or after they explicitly asked to inherit/reorganize/migrate old
  memory in the activation message.
- Do not treat a user-named old conversation or damaged conversation as a
  current-session blank-start request.
- Do not infer completion from a package or schema version. Branch only on the
  helper's `takeover_required` result and verify after apply.
- Do not hand-write a new root's schema, checkpoint, or starter log during
  activation. Missing `.takeover-checkpoint` after activation is a failed
  runtime state, not an acceptable partial success.
- Do not let a stale version-specific sentence in an old project `AGENTS.md`
  override the installed helper's current completion check.
- Do not treat the word `启动` inside the legacy phrase as permission to start a local service.
- Do not rescan every turn for other protocols; reuse the active task's policy until a recheck trigger appears.
- Use Lite Demo's internal memory workflow; do not add extra install or activation steps.
- Do not expose `ExecutionPolicy`, capsule, anchor, fingerprint, or routing-index terminology in ordinary user replies.
