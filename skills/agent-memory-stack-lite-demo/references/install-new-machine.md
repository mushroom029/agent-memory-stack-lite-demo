# Fresh Machine Install

Use this when a new Codex is given a folder containing the Lite demo zip.

## One-sentence user prompt

```text
The folder <folder-path> contains an Agent Memory Stack Lite Demo skill zip. Install it.
```

## Expected steps

1. Find the newest matching zip in the folder.
2. Extract it to a short temporary bootstrap directory.
3. Run the package checker.
4. Install the bundled Lite Demo skill with global AGENTS guidance.
5. If a project path is provided, install project AGENTS guidance and starter `docs/codex` memory.
6. Print the next demo prompt: `启用外挂记忆`, and mention `启动外挂记忆` is also accepted.

## Commands

From an extracted package root:

```powershell
pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\check-package.ps1
pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -WriteGlobalAgents
```

From a folder containing only the zip:

```powershell
pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\bootstrap-from-folder.ps1 -Folder "<folder-path>"
```

For a target project:

```powershell
pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -ProjectRoot "<project-path>" -WriteProjectAgents
```

## Success criteria

- `agent-memory-stack-lite-demo` is installed as the only public skill.
- The context-memory workflow exists only as internal references/scripts inside that skill.
- Global AGENTS contains the marker block.
- After install, the primary activation phrase `启用外挂记忆` is enough to enable the demo.
- The natural start phrase `启动外挂记忆`, explicit safe phrase `本会话启用外挂记忆`, and legacy phrase `启动lite demo` are also accepted.
- Project AGENTS is written only when requested.
- Existing project memory files are not overwritten.
- Later `升级lite demo` requests can use the installed updater and official manifest.
- First memory-root creation asks for confirmation unless install/memory landing was requested or preauthorized.
- Complex new task lines use the same `docs/codex/` root and may create `docs/codex/tasks/<task-id>/active-task.md` after confirmation.
- A complex demo task creates or updates `docs/codex/active-task.md` before execution.
