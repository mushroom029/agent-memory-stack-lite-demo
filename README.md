# 外挂记忆 Lite Demo

给普通 Codex 用户使用的 memory-only skill。它不把旧记忆一股脑塞回上下文，而是把记忆留在本地，在任务真正碰到相关范围时沿简短线索找到该读的内容。

## 当前版本

- 最新版：`v0.2.18`
- 保留稳定版：`v0.1.7`
- 主启动词：`启用外挂记忆`
- 自然启动词：`启动外挂记忆`
- 兼容旧口令：`启动lite demo`
- 升级口令：`升级lite demo`

## v0.2.18 升级内容

- 保留 v0.2.17 的单一 skill、旧记忆选择、旧源继承、session-log 出院、派生指针召回、长文本切片和包体排污检查。
- 新增 pressure-boundary pre-check：恢复、纠错、高压力、稳定模块风险、否决路径风险或交付阻塞时，先在项目记忆里写一张很短的执行前自检卡。
- 自检卡记录匹配约束、安全默认、禁做动作、触发提醒、停止询问点、完成阻塞和证据 owner，帮助 Codex 不把用户压力当成噪声。
- 这不是新的工程协议，也不要求用户反复确认；只有真实冲突才用 `Lite Demo 提醒：` 简短说明。
- Run Audit 新增 `Pressure pre-check: green | yellow | red | not-triggered`，用于复盘这轮是否遵守压力边界、稳定模块、否决路径和完成阻塞。

## 下载

- [v0.2.18 最新版](./agent-memory-stack-lite-demo-v0.2.18.zip)
- [v0.1.7 稳定版](./agent-memory-stack-lite-demo-v0.1.7.zip)
- [GitHub 更新清单](./latest.json)

SHA256：

```text
v0.2.18 6A010A34F1DD2159273C0953E2E558DB8DBDC0479F704D87EF400D0D3BF9C02C
v0.1.7 94690A3C7FF6808000605A640210C3275420397AA1D00F45E2EAECBEBD788B0C
```

## GitHub 直装

对 Codex 说：

```text
请从 GitHub 安装或更新这个 Codex skill：
https://github.com/mushroom029/agent-memory-stack-lite-demo/tree/main/skills/agent-memory-stack-lite-demo
```

Lite Demo 是一个公开 skill，GitHub 安装路径只有上面这一条。

GitHub 直装不会主动运行 zip 根目录的全局 AGENTS 写入脚本，但明确说 `启用外挂记忆` 仍可工作。

## zip 安装

把 zip 放进本地文件夹，然后对 Codex 说：

```text
这个文件夹里有一个 skill 压缩包，安装它。
```

安装完成后，在真实项目会话里说：

```text
启用外挂记忆
```

## 它不会做什么

- 不承诺所有任务一次成功
- 不需要 Reasonix、Claude 或额外 API key
- 不会因为启动口令自动启动服务、跑项目测试或继续旧任务
- 不会在安装时扫描、迁移所有项目
- 不会删除旧记忆或记录密钥
- 不承诺隔离、锁定、合并或保护项目文件

## 作者和联系

- 作者署名：蘑菇
- 抖音名：OCD强迫者
- 抖音号：38439195984
- QQ：327031882
- skill 交流群：1094649041

## 许可证

当前仓库暂未声明开源许可证。未经作者确认，请不要去除作者信息后重新打包发布。
