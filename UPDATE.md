# Lite Demo Update

作者署名：蘑菇｜抖音名：OCD强迫者｜抖音号：38439195984｜QQ：327031882｜skill 交流群：1094649041

官方更新源：

```text
https://159.75.127.201/agent-memory-stack/lite-demo/latest.json
```

已安装用户可以对 Codex 说：

```text
升级lite demo
```

Codex 应使用已安装 skill 内的脚本：

```powershell
pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File "<codex-home>\skills\agent-memory-stack-lite-demo\scripts\update-from-server.ps1"
```

升级流程会读取公开 manifest、下载最新 zip、校验 SHA256，然后重新安装两个 memory-only skills。它不需要任何私密凭据或外部执行工具。

## v0.1.9 升级说明

- 修复旧版看似安装成功、实际没有覆盖的问题。
- 多个安装包共存时按版本号选择最高版本，不再按文件时间误选旧包。
- 安装后核对真实版本，并刷新受管理的 AGENTS 规则。
- 执行策略收敛到单一任务锚点，减少重复记录和上下文消耗。
- `v0.1.7` 继续作为稳定回退版；`v0.1.8` 已退出公开分发。

升级完成后，在项目会话中说：

```text
启用外挂记忆
```
