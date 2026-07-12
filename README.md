# 外挂记忆 Lite Demo

给普通 Codex 用户用的 memory-only skill 包。

它不是让 AI 瞬间变神，而是让 Codex 在项目里留下可恢复的记忆：

- 这次任务目标是什么
- 哪些路已经失败过
- 用户已经纠正过什么
- 哪些稳定模块不能乱改
- 上下文压缩或中断以后下一步该接着做什么

普通人用 AI，最难受的不是失败一次，而是它失败以后不记得为什么失败。外挂记忆 Lite Demo 解决的就是这个问题。

## 当前版本

- 最新升级版：`v0.2.0f`
- 保留稳定版：`v0.1.7`
- `v0.1.8`：已从公开分发中清理
- 主启动词：`启用外挂记忆`
- 明确启动词：`本会话启用外挂记忆`
- 兼容旧口令：`启动lite demo`
- 升级口令：`升级lite demo`

## v0.2.0f 升级内容

`v0.2.0f` 在 `v0.1.9` 的可靠升级基础上，补上了更适合普通用户长期使用的记忆层能力：

- 保留 `v0.1.9` 的真实覆盖旧版、语义版本选包、安装结果校验。
- 增加记忆卫生：临时要求、压力表达、短回复不直接变成长期死规矩。
- 增加 compact Run Audit：重要运行后留下更容易恢复的一屏审计卡。
- 增加 UTF-8/中文写入纪律，减少中文记忆和日志乱码。
- 增加 `启动外挂记忆` 口令和 `context-memory-index` 兜底。
- 增加一次性轻提示：复杂任务多轮后可建议启用，拒绝后本会话不再打扰。
- 增加自适应退让：如果已有执行协议或模型原生流程在负责计划/测试/验证，Lite Demo 只做记忆层；没有明确流程时才用轻锚点兜底，只有漂移、重复失败、忘记纠正、压缩恢复失败或高压时才加重。

版本建议：想体验最新记忆层能力，选择 `v0.2.0f`；想保留更早、已经长期使用的行为，选择 `v0.1.7` 稳定版。

## 下载

最新升级版：

```text
agent-memory-stack-lite-demo-v0.2.0f.zip
```

保留稳定版：

```text
agent-memory-stack-lite-demo-v0.1.7.zip
```

官方短链页面：

```text
https://159.75.127.201/lite/
```

官方更新源：

```text
https://159.75.127.201/agent-memory-stack/lite-demo/latest.json
```

SHA256：

```text
v0.2.0f 0D89663F4D07579C274D89C586DA70A4F8A7FCE5969E4EDBDE7A2F12368BDE0A
v0.1.7  94690A3C7FF6808000605A640210C3275420397AA1D00F45E2EAECBEBD788B0C
```

## 怎么安装

### 方法一：Codex GitHub 直装

如果你想让 Codex 直接从 GitHub 安装，不要只给仓库根目录。请让 Codex 安装下面两个 skill 路径：

```text
https://github.com/mushroom029/agent-memory-stack-lite-demo/tree/main/skills/agent-memory-stack-lite-demo
https://github.com/mushroom029/agent-memory-stack-lite-demo/tree/main/skills/context-memory-index
```

可以直接对 Codex 说：

```text
请从 GitHub 安装这两个 Codex skills：
https://github.com/mushroom029/agent-memory-stack-lite-demo/tree/main/skills/agent-memory-stack-lite-demo
https://github.com/mushroom029/agent-memory-stack-lite-demo/tree/main/skills/context-memory-index
```

如果安装器说仓库是 private 或无法访问，通常不是本仓库私有，而是它拿到了仓库根目录或错误路径。请改用上面的 `skills/...` 精确路径。

### 方法二：下载 zip 安装

把 zip 下载到本地，然后在 Codex 里对它说：

```text
这个文件夹里有一个 skill 压缩包，安装它。
```

安装完成后，到你的真实项目会话里说：

```text
启用外挂记忆
```

已经安装 Lite Demo 的用户可以直接说：

```text
升级lite demo
```

## 它会做什么

它会让 Codex 在项目内建立 `docs/codex/` 记忆区，用来保存当前任务目标、阶段、下一步、失败路径、用户纠正、压力信号、稳定模块保护和上下文压缩后的恢复锚点。

## 它不会做什么

- 不承诺所有任务一次成功
- 不需要 DeepSeek、Reasonix、Claude 或额外 API key
- 不会自动启动服务、测试接口或继续旧任务
- 不会记录你的密钥
- 不会把情绪压力当作无意义噪声直接丢掉

## 作者和联系

- 作者署名：蘑菇
- 抖音名：OCD强迫者
- 抖音号：38439195984
- QQ：327031882
- skill 交流群：1094649041

## 许可证

当前仓库暂未声明开源许可证。未经作者确认，请不要去除作者信息后重新打包发布。
