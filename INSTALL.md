# Agent Memory Stack Lite Demo Install

This package installs a memory-only Codex workflow for fresh-machine demos.

作者署名：蘑菇｜抖音名：OCD强迫者｜抖音号：38439195984｜QQ：327031882

It provides:

- a small global AGENTS gate;
- optional project AGENTS guidance;
- one public skill: `agent-memory-stack-lite-demo`;
- internal context-memory references and scripts inside that skill;
- starter `docs/codex/current-context.md` and `docs/codex/index.md` for a target project.

It does not require extra credentials, alternate model setup, or an external execution tool.

It also does not compete with an existing execution protocol. If the user, project rules, an actually used execution skill, or a model-native workflow already owns planning, debugging, testing, verification, deployment, or refactor flow, Lite Demo records that route instead of adding another one. If no explicit execution protocol exists, it may use adaptive lite-anchor: light first, fuller only after drift, repeated failure, forgotten correction, compression recovery failure, stable-module mistakes, or high pressure.

v0.2.17 keeps the stable v0.2.16 install, update, activation, task routing, in-flight queue, discharge, and `Progress boundary` behavior. Package v0.2.17 still uses memory schema/checkpoint `v0.2.7` as the compatible on-disk format. The old-user path now asks once on first activation after upgrade whether to `继承并升级整理旧记忆` or `全新启动`: inheritance reorganizes memory without resuming old tasks or touching business files, while fresh start keeps old memory cold and not default-recalled. If a user asks to inherit old memory but Lite Demo cannot find a root in the current project, Codex should first look for nearby or explicitly visible candidates and let the user choose; it should not ask ordinary users to locate `docs/codex/` by hand, and broader discovery is opt-in. v0.2.17 also adds Lite-native storage/retrieval separation through a derived pointer cache, stronger runtime closeout evidence, long local source slicing, and stricter layer/bloat checks. `session-log.md` remains an in-flight queue rather than a chronicle; settled entries discharge byte-preserved, and old conversations, damaged conversations, old projects, archives, and unknown old sources still require inventory and destinations before inheritance is claimed.

Official update manifest:

```text
https://159.75.127.201/agent-memory-stack/lite-demo/latest.json
```

## 1. Check PowerShell

```powershell
pwsh -NoLogo -NoProfile -Command '$PSVersionTable.PSVersion'
```

Use PowerShell 7 or newer.

## 2. Install From The Package Folder

From the extracted package root:

```powershell
pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -WriteGlobalAgents
```

This installs the bundled Lite Demo skill and appends a marker-based block to the selected Codex global `AGENTS.md`.

The global write is non-destructive. Existing content is preserved. If the marker already exists, the script skips appending another block.

## 3. One-Sentence Folder Bootstrap

If a new Codex only knows where the zip is, tell it:

```text
The folder <folder-path> contains an Agent Memory Stack Lite Demo skill zip. Install it.
```

Codex should run:

```powershell
pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\bootstrap-from-folder.ps1 -Folder "<folder-path>"
```

The bootstrap script selects the highest semantic version matching zip, including suffixes and newer releases such as `v0.2.17`, extracts it to a short temporary directory, checks the package, installs or upgrades the Lite Demo skill, refreshes the marked global gate, cleans the temporary extraction, and prints both package and installed versions.

If an older Lite Demo is already installed, this bootstrap path now upgrades it when the selected zip version differs. The official `升级lite demo` command remains the preferred online update path.

## 4. Optional Project Setup

For a real project:

```powershell
pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -ProjectRoot "C:\path\to\project" -WriteProjectAgents
```

This creates or updates:

- `AGENTS.md`
- `docs/codex/current-context.md`
- `docs/codex/index.md`
- `docs/codex/tasks/`
- `docs/codex/capsules/`

It does not overwrite existing project memory files.

Default policy is ask-before-write for memory landing. To preauthorize automatic task anchors in this project:

```powershell
pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -ProjectRoot "C:\path\to\project" -WriteProjectAgents -PreauthorizeMemoryLanding
```

Preauthorization still requires Codex to tell the user what path it wrote and why.

## 5. Verify

From the package root:

```powershell
pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\check-package.ps1
```

For global AGENTS loading, a Codex instance can run:

```powershell
pwsh -NoLogo -NoProfile -Command 'codex debug prompt-input "probe"'
```

## 6. First Demo Task

After install, use this prompt on a target project:

```text
启用外挂记忆
```

自然启动口令：

```text
启动外挂记忆
```

兼容旧口令：

```text
启动lite demo
```

The installed skill and AGENTS block contain the longer behavior: use the memory-only demo, read or create `docs/codex/`, keep task-scoped `ExecutionPolicy` only in the active task anchor, protect stable modules, and create `active-task.md` before complex work.

If no project memory exists yet, `启用外挂记忆`, `启动外挂记忆`, `本会话启用外挂记忆`, or the legacy `启动lite demo` counts as explicit demo activation and memory landing permission for the current project root. Codex should still report the created paths and that secrets are not recorded. If memory already exists and the user only provided an activation phrase, Codex must not auto-resume old work; it should ask whether to resume the active task or ask what real task to run. Codex should use Lite Demo's internal memory workflow.

For old users, upgrading can happen in any Codex conversation, but old project memory takeover happens in the target project conversation. If the user asks to inherit old memory and the current project does not expose a known memory root, Codex should search nearby project/parent paths and explicitly visible candidates first, then show a short candidate list. If nothing is found, ask whether to broaden discovery over named/common Codex project locations, return to the old project conversation and run `启用外挂记忆`, or start fresh. Do not ask the user to find an internal memory folder before this candidate flow.

If the user did not explicitly activate memory, a no-memory project may receive one plain suggestion after 2-3 meaningful rounds or clear constraints/failure/correction/pressure signals:

```text
这个任务可能会跨多轮，我建议启用外挂记忆接管项目记忆，帮我记住目标、踩坑和不要乱改的地方。要启用吗？
```

If the user refuses, Codex should not create `docs/codex/`, write AGENTS, save project memory, or store a refusal marker. It should simply stop suggesting again in the current chat. A later explicit `启用外挂记忆` or `启动外挂记忆` overrides that temporary skip.

The expected user-visible effect is not magic success. The expected effect is better route retention: Codex should remember the goal, avoid repeated failed paths, and recover faster after compression or interruption.

The new memory hygiene effect should appear only when Codex is about to write durable project memory from ambiguous language. It may say once in Chinese that a preference is being saved as a task habit rather than a hard rule. It should not become a repeated questionnaire.

The v0.2.17 effect is still intentionally quiet to ordinary users: the session log stays small through exact, byte-preserving discharge, recovery follows compact routes and owners instead of injecting a default log tail, and old roots get a visible fresh-start-vs-inherit choice before takeover. Lite Demo still installs and activates as one skill, and standalone `context-memory-index` copies are archived outside the active skills root with restore metadata and destination status. If the user asks a current conversation to inherit a damaged or old conversation, that referenced source must be inventoried before completion is claimed. The on-disk memory schema/checkpoint label remains v0.2.7 for compatibility. Current owners and live guards load first; cold history opens only on precise version/event matches. The v0.2.4 `Lite Demo 提醒：` task-routing wording is unchanged.

## 7. Later Updates

After install, users can ask Codex:

```text
升级lite demo
```

Codex should use the installed updater script under:

```powershell
<codex-home>\skills\agent-memory-stack-lite-demo\scripts\update-from-server.ps1
```
