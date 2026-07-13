# 外挂记忆 Lite Demo

给普通 Codex 用户使用的 memory-only skill。它不让 AI 瞬间变神，只让 Codex 在项目里记住目标、失败路径、用户纠正、稳定边界和上下文压缩后的下一步。

## 当前版本

- 最新版：`v0.2.2`
- 保留稳定版：`v0.1.7`
- 主启动词：`启用外挂记忆`
- 自然启动词：`启动外挂记忆`
- 兼容旧口令：`启动lite demo`
- 升级口令：`升级lite demo`

## v0.2.2 升级内容

- 回归一个包、一个公开 skill；context-memory 索引和记忆机制全部作为内部组件。
- 升级 v0.2.0f 时，只归档内容完全匹配的旧版遗留 skill；用户修改过或独立安装的同名 skill 会保留。
- 已有工程流程负责计划、调试、测试或验证时，Lite Demo 只做记忆，不再叠加第二套流程。
- 没有其他工程流程时，才使用自己的轻量兜底。
- 初始上下文只保留精准索引，按当前任务加载强相关记忆。
- 安装与升级增加事务替换、失败回滚、禁止静默降级、失败如实返回和安装后版本复读。

普通用户不需要理解这些内部机制。安装后在真实项目会话里说一句 `启用外挂记忆` 即可。

## 下载

- [v0.2.2 最新版](./agent-memory-stack-lite-demo-v0.2.2.zip)
- [v0.1.7 稳定版](./agent-memory-stack-lite-demo-v0.1.7.zip)
- [官方短链页面](https://159.75.127.201/lite/)
- [官方更新源](https://159.75.127.201/agent-memory-stack/lite-demo/latest.json)

SHA256：

```text
v0.2.2 A7B736FBD593625A0CBA9A5B6F7FACC46DD1FCAEB61F8B3A47F99A6E60CF090F
v0.1.7 94690A3C7FF6808000605A640210C3275420397AA1D00F45E2EAECBEBD788B0C
```

## GitHub 直装

Lite Demo 现在只有一个 skill。对 Codex 说：

```text
请从 GitHub 安装这个 Codex skill：
https://github.com/mushroom029/agent-memory-stack-lite-demo/tree/main/skills/agent-memory-stack-lite-demo
```

不要再安装旧的 `skills/context-memory-index` 路径。它曾是 v0.2.0f 的错误拆分，v0.2.2 已把这套机制收回 Lite Demo 内部。

GitHub 直装不会主动运行 zip 根目录的全局 AGENTS 写入脚本，但明确说 `启用外挂记忆` 仍可正常工作。后续说 `升级lite demo`，官方 updater 会校验并刷新完整安装。

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
- 不需要 DeepSeek、Reasonix、Claude 或额外 API key
- 不会因为启动口令自动启动服务、跑测试或继续旧任务
- 不会记录密钥
- 不会把用户压力简单当成情绪噪声丢掉

## 作者和联系

- 作者署名：蘑菇
- 抖音名：OCD强迫者
- 抖音号：38439195984
- QQ：327031882
- skill 交流群：1094649041

## 许可证

当前仓库暂未声明开源许可证。未经作者确认，请不要去除作者信息后重新打包发布。
