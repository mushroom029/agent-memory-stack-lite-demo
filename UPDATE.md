# Lite Demo Update

作者署名：蘑菇｜抖音名：OCD强迫者｜抖音号：38439195984｜QQ：327031882｜skill 交流群：1094649041

已安装用户直接对 Codex 说：

```text
升级lite demo
```

官方更新源：

```text
https://159.75.127.201/agent-memory-stack/lite-demo/latest.json
```

## v0.2.6 升级说明

- 记忆正文只保存一份，其他层只留简短唤醒线索；相关范围命中后，全部相关正文和重要边界都会被找回。
- 最近 30-60 行只负责提示最近状态，不限制总召回；检索不确定或操作风险高时会继续向下寻找。
- 新 session log 不再记录普通顺利流水账，只保留未解决事项、回滚、待复核记忆和少量检查点。
- 升级不会扫描所有项目。回到旧项目后第一次说 `启用外挂记忆`，会自动整理一次旧记忆，旧记录不删除，也不会自动执行旧任务或修改业务文件。
- v0.1.7 继续保留为稳定回退版。

## GitHub 首次安装

只安装这一个 skill 路径：

```text
https://github.com/mushroom029/agent-memory-stack-lite-demo/tree/main/skills/agent-memory-stack-lite-demo
```

不要安装旧的 `skills/context-memory-index`。
