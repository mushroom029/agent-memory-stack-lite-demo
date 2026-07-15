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

## GitHub 首次安装

只安装这一个 skill 路径：

```text
https://github.com/mushroom029/agent-memory-stack-lite-demo/tree/main/skills/agent-memory-stack-lite-demo
```

不要安装旧的 `skills/context-memory-index`。这套机制已经是 Lite Demo 内部组件。

## v0.2.5 升级说明

- 完整 session log 留在本地，正常恢复不再全文回灌，只读最近尾部。
- 旧证据按需定向检索或读取行段；明确纠正、否决路径和稳定边界同时写入必读锚点/capsule。
- active-task 只保存当前路线和下一步，不逐批堆积历史。
- 健康检查只告警，不自动删除、轮转或重写记忆。
- 保留 v0.2.4 的任务提示、一个公开 skill、已有工程协议时退让；`v0.1.7` 继续作为稳定回退版。

升级完成后，在项目会话中说：

```text
启用外挂记忆
```
