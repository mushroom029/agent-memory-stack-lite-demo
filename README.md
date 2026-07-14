# 外挂记忆 Lite Demo

给普通 Codex 用户使用的 memory-only skill。它不让 AI 瞬间变神，只让 Codex 在项目里记住目标、失败路径、用户纠正、稳定边界和上下文压缩后的下一步。

## 当前版本

- 最新版：0.2.4
- 保留稳定版：0.1.7
- 主启动词：启用外挂记忆
- 自然启动词：启动外挂记忆
- 兼容旧口令：启动lite demo
- 升级口令：升级lite demo

## v0.2.4 升级内容

- 未完成/并发任务的提示改成 Lite Demo 提醒：，并带一句话任务名和上次进度。
- Lite Demo 提醒： 只用于记忆路由、边界或明确重叠风险，不用于普通执行汇报、代码解释或每句话。
- 单独记录只隔离记忆，不承诺隔离项目文件；有明确重叠证据时才提醒“记忆可以分开记，但项目文件是同一份”。
- 仍然保持一个包、一个公开 skill；已有工程协议时只做记忆，不叠加第二套流程。

普通用户不需要理解内部机制。安装后在真实项目会话里说一句 启用外挂记忆 即可。

## 下载

- [v0.2.4 最新版](./agent-memory-stack-lite-demo-v0.2.4.zip)
- [v0.1.7 稳定版](./agent-memory-stack-lite-demo-v0.1.7.zip)
- [官方短链页面](https://159.75.127.201/lite/)
- [官方更新源](https://159.75.127.201/agent-memory-stack/lite-demo/latest.json)

SHA256：

`	ext
v0.2.4 95BB168A3BBFF3A0D399716F5379D00C7EEE306E30A56C4C7FD346C444D0C4E8
v0.1.7 94690A3C7FF6808000605A640210C3275420397AA1D00F45E2EAECBEBD788B0C
`

## GitHub 直装

Lite Demo 现在只有一个 skill。对 Codex 说：

`	ext
请从 GitHub 安装这个 Codex skill：
https://github.com/mushroom029/agent-memory-stack-lite-demo/tree/main/skills/agent-memory-stack-lite-demo
`

不要再安装旧的 skills/context-memory-index 路径。它曾是 v0.2.0f 的错误拆分，现在这套机制已经收回 Lite Demo 内部。

GitHub 直装不会主动运行 zip 根目录的全局 AGENTS 写入脚本，但明确说 启用外挂记忆 仍可正常工作。后续说 升级lite demo，官方 updater 会校验并刷新完整安装。

## zip 安装

把 zip 放进本地文件夹，然后对 Codex 说：

`	ext
这个文件夹里有一个 skill 压缩包，安装它。
`

安装完成后，在真实项目会话里说：

`	ext
启用外挂记忆
`

## 它不会做什么

- 不承诺所有任务一次成功
- 不需要 DeepSeek、Reasonix、Claude 或额外 API key
- 不会因为启动口令自动启动服务、跑测试或继续旧任务
- 不会记录密钥
- 不会把用户压力简单当成情绪噪声丢掉
- 不承诺隔离、锁定、合并或保护项目文件

## 作者和联系

- 作者署名：蘑菇
- 抖音名：OCD强迫者
- 抖音号：38439195984
- QQ：327031882
- skill 交流群：1094649041

## 许可证

当前仓库暂未声明开源许可证。未经作者确认，请不要去除作者信息后重新打包发布。
