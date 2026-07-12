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

如果是首次从 GitHub 直装，请不要只给仓库根目录；请安装这两个路径：

```text
https://github.com/mushroom029/agent-memory-stack-lite-demo/tree/main/skills/agent-memory-stack-lite-demo
https://github.com/mushroom029/agent-memory-stack-lite-demo/tree/main/skills/context-memory-index
```

Codex 应使用已安装 skill 内的脚本：

```powershell
pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File "<codex-home>\skills\agent-memory-stack-lite-demo\scripts\update-from-server.ps1"
```

升级流程会读取公开 manifest、下载最新 zip、校验 SHA256，然后重新安装两个 memory-only skills。它不需要任何私密凭据或外部执行工具。

## v0.2.0f 升级说明

- 保留 `v0.1.9` 的可靠升级能力：真实覆盖旧版、语义版本选包、安装结果校验、刷新受管理的 AGENTS 规则。
- 增加记忆卫生：临时要求、压力表达、短回复不会直接变成长期硬规则。
- 增加 compact Run Audit、UTF-8 中文写入纪律、`启动外挂记忆` 口令和 `context-memory-index` 兜底。
- 增加一次性轻提示：复杂任务多轮后可建议启用，拒绝后本会话不再主动打扰。
- 增加自适应退让：已有执行协议或模型原生流程负责计划/测试/验证时，Lite Demo 只做记忆层；没有明确流程时才用轻锚点兜底。
- `v0.1.7` 继续作为稳定回退版；`v0.1.8` 已退出公开分发。

升级完成后，在项目会话中说：

```text
启用外挂记忆
```
