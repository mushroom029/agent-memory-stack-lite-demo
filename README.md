# 外挂记忆 Lite Demo

给普通 Codex 用户使用的 memory-only skill。它不把旧记忆一股脑塞回上下文，而是把记忆留在本地，在任务真正碰到相关范围时沿简短线索找到该读的内容。

## 当前版本

- 最新版：`v0.2.17`
- 保留稳定版：`v0.1.7`
- 主启动词：`启用外挂记忆`
- 自然启动词：`启动外挂记忆`
- 兼容旧口令：`启动lite demo`
- 升级口令：`升级lite demo`

## v0.2.17 升级内容

- 保留 Lite Demo 的记忆治理、用户边界、旧记忆接管和轻量本地 Markdown 使用方式；补齐 Lite Demo 自己的存储/检索分离、owner route 和派生指针缓存能力。
- 升级安装只替换 Skill 程序文件，不删除、不自动迁移用户项目里的旧记忆。
- 老用户回到旧项目说 `启用外挂记忆` 后，先选择 `继承并升级整理旧记忆` 或 `全新启动`。继承只改记忆层，不恢复旧任务、不运行服务、不碰业务文件。
- 如果用户要继承旧记忆但当前项目没找到旧根，Codex 先只读查找附近候选并列出来，不先让普通用户手动找 `docs/codex/`；更广范围查找需要用户授权。
- `session-log.md` 继续是未决/未归位队列，不是编年史；已归位条目字节保留到归档，后续恢复从精简路线和 owner 按需召回。
- 长文本源会先切片成 artifact，记忆层只保存理解、路线和续接保护，避免把正文塞进日志或上下文。
- 旧的独立 `context-memory-index` 会被非破坏性归档出 active skills；公开使用仍只有一个 `agent-memory-stack-lite-demo` skill。

## 下载

- [v0.2.17 最新版](./agent-memory-stack-lite-demo-v0.2.17.zip)
- [v0.1.7 稳定版](./agent-memory-stack-lite-demo-v0.1.7.zip)
- [官方短链页面](https://159.75.127.201/lite/)
- [官方更新源](https://159.75.127.201/agent-memory-stack/lite-demo/latest.json)

SHA256：

```text
v0.2.17 3ADC0DE49AA895214018EA813152B577BD067C12989250403AB71753C7E77D45
v0.1.7 94690A3C7FF6808000605A640210C3275420397AA1D00F45E2EAECBEBD788B0C
```

## 推荐升级方式

在任意 Codex 会话里说：

```text
升级lite demo
```

升级完成后，回到真实项目会话里说：

```text
启用外挂记忆
```

如果项目已有旧版记忆，新版 Lite Demo 会询问继承旧记忆还是全新启动。

## GitHub 直装

对 Codex 说：

```text
请从 GitHub 安装这个 Codex skill：
https://github.com/mushroom029/agent-memory-stack-lite-demo/tree/main/skills/agent-memory-stack-lite-demo
```

Lite Demo 只有一个公开 skill。不要安装旧的 `skills/context-memory-index` 路径。

GitHub 直装不会主动运行 zip 根目录的全局 AGENTS 写入脚本，但明确说 `启用外挂记忆` 仍可工作。后续说 `升级lite demo`，官方 updater 会校验并刷新完整安装。

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
