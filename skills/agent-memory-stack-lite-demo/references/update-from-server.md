# Update From Official Server

Use this when the user asks to update, upgrade, reinstall, or get the latest Lite Demo through the official server.

Chinese shortcut:

```text
升级lite demo
```

## Public Source

- Manifest: `https://159.75.127.201/agent-memory-stack/lite-demo/latest.json`
- Channel: stable
- Author: 蘑菇

## GitHub Direct Install Compatibility

If Lite Demo was first installed from GitHub with these exact skill paths, use the same update flow:

```text
https://github.com/mushroom029/agent-memory-stack-lite-demo/tree/main/skills/agent-memory-stack-lite-demo
```

Do not add extra memory-skill installation steps. In v0.2.1 and later, the memory workflow is internal to `agent-memory-stack-lite-demo`.

GitHub direct install is only an initial install source. It installs the same
skill directory and updater, but it does not itself execute the zip package's
global AGENTS writer. Explicit activation still works through the skill; a later
official update validates and refreshes the managed global gate. When the user
says `升级lite demo`, use the official manifest instead of guessing the repo
root or reinstalling from an arbitrary GitHub path.

## Command

Run the installed updater script from the user's Codex home:

```powershell
pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File "<codex-home>\skills\agent-memory-stack-lite-demo\scripts\update-from-server.ps1"
```

If the user also wants to refresh project guidance for a target project, pass:

```powershell
-ProjectRoot "<project-path>" -WriteProjectAgents
```

## Required Behavior

1. Fetch the public manifest and compare installed/manifest versions.
2. For the same version, report no change. If installed is newer, keep it and do not download or downgrade.
3. Only when installation is needed, download the manifest zip and verify SHA256.
4. Extract to a temporary folder and run the package checker through a checked child process.
5. Run the installer through a checked child process. A nonzero child exit is an update failure.
6. Reread installed `VERSION.txt`; report success only when it equals the manifest version.
7. Report installed version, SHA256, author identity, and the next prompt: `启用外挂记忆`; also mention `启动外挂记忆` is accepted.

## Boundaries

- Do not ask for server credentials, account passwords, or service keys.
- Do not expose SSH aliases, server filesystem paths, object storage credentials, or deployment methods.
- Do not skip SHA256 verification.
- Do not silently downgrade or reinstall the same version.
- Do not emit success JSON after a failed checker, installer, or version reread.
- Do not install external executors or alternate model setup as part of Lite Demo updates.
