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

1. Fetch the public manifest.
2. Download the zip listed by the manifest.
3. Verify SHA256 before install.
4. Extract to a temporary folder.
5. Run the downloaded package checker.
6. Run the downloaded installer with `-WriteGlobalAgents -UpdateExistingAgentsBlock -Force`.
7. Report installed version, SHA256, author identity, and the next prompt: `启用外挂记忆`; also mention `启动外挂记忆` is accepted.

## Boundaries

- Do not ask for server credentials, account passwords, or service keys.
- Do not expose SSH aliases, server filesystem paths, object storage credentials, or deployment methods.
- Do not skip SHA256 verification.
- Do not install external executors or alternate model setup as part of Lite Demo updates.
