# Lite Demo Update

作者署名：蘑菇｜抖音名：OCD强迫者｜抖音号：38439195984｜QQ：327031882

官方更新源：

```text
https://159.75.127.201/agent-memory-stack/lite-demo/latest.json
```

已安装用户可以对 Codex 说：

```text
升级lite demo
```

如果用户最初是从 GitHub 直装，也走同一条升级路径。v0.2.1 起，GitHub 直装只应该安装这一个 skill 路径：

```text
https://github.com/mushroom029/agent-memory-stack-lite-demo/tree/main/skills/agent-memory-stack-lite-demo
```

GitHub 直装会得到同一个 skill 目录和 updater，但不会自行运行 zip 包根目录的全局 AGENTS 写入脚本。用户明确启用时仍可由 skill 工作；后续官方 updater 会校验并刷新全局 gate。不要重新猜 GitHub 仓库根目录。

## v0.2.17 升级说明

- 包版本是 v0.2.17；磁盘 memory schema/checkpoint 继续沿用 `v0.2.7` 兼容标签，不能用包版本字样判断接管完成。
- 旧用户首次启用旧记忆根时，先问 `继承并升级整理旧记忆 / 全新启动`。选继承后才整理旧记忆，且只改记忆层，不恢复旧任务、不运行服务、不碰业务文件；选全新则旧记忆冷存、不默认召回、不称已继承。
- 如果用户要继承旧记忆但当前项目没有暴露旧根，Codex 先做候选发现：检查当前目录、项目根、父目录链、已明示路径和 Lite Demo 归档元数据，列出候选让用户选择；不先要求普通用户手动找到 `docs/codex/`。更广发现仍需先说明将扫描的顶层路径并获得授权。
- 保留 Lite Demo 的记忆治理、用户边界、旧记忆接管和轻量使用方式；借鉴 agent-memory-mcp 的存储/检索分离思想，但实现为 Lite Demo 自己的本地 Markdown owner/route 与派生指针缓存，不引入 MCP、外部数据库、daemon、embedding 或额外凭据。
- `session-log.md` 继续是未决/未归位队列，不是编年史。已归位条目通过 discharge 字节保留到归档；普通 green 过程不写入 live log。
- 新增长文本源 intake、派生检索、层级质量扫描、膨胀扫描和 runtime replay closeout 检查，发布前压力测试必须证明结果文件、轨迹、轮次和验证产物都存在并可读。

## v0.2.16 升级说明

- 包版本是 v0.2.16；磁盘 memory schema/checkpoint 继续沿用 `v0.2.7` 兼容标签。v0.2.15 已验证的安装、更新、旧库接管、任务路由、在办队列、`Progress boundary`、Requirement Ledger 和旧源继承规则保持不变。
- 修复 discharge 的 ID 子串误判：`R1` 不再被 `R10`、`XR1` 或偶然正文命中；点号 ID 与 checker 保持一致。没有精确路线、仍是 open/pending/unresolved、指回日志或 `owners=none` 的条目一律保留。
- discharge 从只处理 `[REVIEW]` 扩展为处理所有结构化在办类型；非 REVIEW 路线必须写入精确 `entry=TYPE:id` 标识、真实 owner 和 helper 明确认可的已归位状态。`blocked`、未知状态和假 owner 都保留在 live log；旧 `[REVIEW]` 的裸 ID 路线继续兼容。
- discharge 与 roll 的归档都改为二进制追加，中文、CRLF 和无末尾换行的原条目字节不会被 Windows 文本换行转换改写；live log 通过同目录临时文件原子替换，并在替换前复查 log/index 是否并发变化。
- 新建记忆库的 `fresh-initialization` 检查点会明确区分“以后新增的当前记忆”和“升级前旧历史”，避免索引正常增长后被误判为旧库接管未完成；旧库和未知检查点的 `legacy-destinations.md` 门没有放宽。
- `legacy-destinations.md` 不再只检查两个关键词：字段、状态、owner、probe 和 owner 文件都要有效；任何 `pending-review` 都明确表示该范围尚未完成接管，helper 与 strict checker 都会阻断盖章。
- 压缩/恢复默认从 `active-task.md`、`current-context.md`、`index.md` 和全部命中 owner/mandatory guard 开始。session-log 只在精确未决路线、资料冲突或证据缺口要求时定向读取，不再默认注入最近尾部。
- 清除残留的 `Completed`/里程碑摘要/append-only 日志措辞；active-task 只保留一个覆盖式 `Progress boundary`，checker 同时检查其重复膨胀。
- 公共 ZIP 不再携带历史 `plans/`、审查目录或开发记忆；包内演示记忆使用 compact owner 路由、一个完成边界和空的在办日志。

## v0.2.15 升级说明

- 包版本是 v0.2.15；磁盘 memory schema/checkpoint 仍沿用 `v0.2.7` 兼容标签，不能用包版本字样判断接管完成。（v0.2.14 为作废版本号，跳过。）
- session-log 补上缺失的"出院"闸门：它是在办未决事项队列，不是编年史。准入只收未解决失败/冲突/回滚、未提升纠正、`[REVIEW]` 暂存体、稀疏恢复检查点；条目一旦被解决或提升到正式 owner，`scripts/takeover-memory.py discharge` 按字节保留搬入 `legacy/session-log-discharged.md`。活跃日志的大小跟随"当前未办结事项数"，不随项目长度增长。
- discharge 的归位判定是确定性的：仅当 index.md 中该 `[REVIEW:<id>]` 的路由已指向正式 owner（非 pending-review、不再锚定日志内条目）才出院；查无路由不出院。无 id 的未解决事项一律保留、只报告，判断权留给模型/用户。
- 例行 green 的 Run Audit 卡不再进入 session-log；结果由进度边界、验证脚本与产物本身承载。
- `active-task.md` 字段全部现值化：`Completed` 字段改为 `Progress boundary`（单一"做到哪"边界值，覆盖式更新），禁止区间/脚本名累积枚举；可寻址明细归 index 路由、owner 或本地产物。
- `roll` 保留为兜底保险丝：仅当日志超行数预算时按字节归档最旧条目。

## v0.2.13 升级说明

- 包版本是 v0.2.13；磁盘 memory schema/checkpoint 仍沿用 `v0.2.7` 兼容标签，不能用包版本字样判断接管完成。
- 接管 checkpoint 从 `session-log.md` 解耦到独立文件 `.takeover-checkpoint`：新库初始化和新接管直接写独立文件，日志里不再出现 checkpoint 块；legacy prefix 依旧按字节保护 `session-log.md` 头部，语义不变。
- 旧库零迁移兼容：checkpoint 还在 `session-log.md` 里的旧库照常校验通过（回退读取）；`scripts/takeover-memory.py migrate` 可把元数据搬到独立文件，且绝不改动 `session-log.md` 的任何字节，幂等可重复执行。
- `roll` 改为按记录的 prefix 字节边界定位自由区，不再依赖日志内 marker，解耦后的新库同样可滚动。

## v0.2.12 升级说明

- 包版本是 v0.2.12；磁盘 memory schema/checkpoint 仍沿用 `v0.2.7` 兼容标签，不能用包版本字样判断接管完成。
- `session-log.md` 降级为有界滚动近期缓冲：超过行数预算后，`scripts/takeover-memory.py roll` 会把最旧的整条目按字节保留搬入 `legacy/session-log-archive.md`，绝不触碰 checkpoint 或其保护的旧证据前缀，接管校验持续通过。

## v0.2.11 升级说明

- 包版本是 v0.2.11；磁盘 memory schema/checkpoint 仍沿用 `v0.2.7` 兼容标签，不能用包版本字样判断接管完成。
- 修复 v0.2.10 审核发现的两个接管缺口：短但重要的旧禁令/纠正/验收不再因为少于 20 行、无标题、无 `[REVIEW]`、无 Run Audit 而被判成“无意义”；旧记忆在 `current-context.md`、`active-task.md`、`index.md`、`capsules/`、`tasks/` 或 `routes/` 时，即使没有 `session-log.md` 也会要求归宿表。
- Lite Demo 仍不默认全机扫描所有项目；用户点名旧源、打开项目根或明确授权更广发现时才读对应路径。未来如果做全局 registry/扫描，必须显式授权并展示待读路径。
- 用户重复纠正同一行为两次，或在已记录纠正被忽略后强烈表达挫败，应立即写 `mandatory-guard` 或 `correction-guard`，不能只道歉或只记压力。
- 启动时运行 helper 脚本必须从已加载/已安装的 `$agent-memory-stack-lite-demo` skill 的 `scripts/` 目录定位，不依赖当前工作目录。

## v0.2.10 升级说明

- 包版本是 v0.2.10；磁盘 memory schema/checkpoint 仍沿用 `v0.2.7` 兼容标签，不能用包版本字样判断接管完成。
- 用户明确表达的目标、禁令、验收条件、纠正，默认是 requirement，不因愤怒、压力、短语变化或重复表达降级成软边界。
- 新目标如果和旧的显式用户指令冲突，Codex 必须先指出冲突，并让用户选择：A 保留旧指令并微调当前目标；B 仅本次创建/流程临时覆盖；C 补全或替换命令。
- 用户点名旧会话、损坏会话、旧项目、旧记忆源或要求迁移旧记忆时，先按 legacy-source import 盘点旧源并写归宿；不能只创建当前 `docs/codex/` 或复制 active-task 就宣布接管。
- v0.1.7 稳定版、v0.1.8、v0.1.9、v0.2.0 后缀版本、v0.2.1 以后版本和未知布局，都按可能的旧源保守处理；未知价值进入 `pending-review`，不是静默忽略。

## v0.2.7 升级说明

- 用户升级后回到旧会话，只需输入 `启用外挂记忆`；不需要第二条迁移命令。
- 接管完成必须同时具有 v0.2.7 schema 和可验证的 v0.2.7 检查点。提前写版本号、没有日志或只有旧检查点都不会被误判为完成。
- 正确 v0.2.6 记忆也会一次性升级到 v0.2.7 路由；旧检查点和旧日志全部保留为新前缀。
- 顶层路由只挂当前正文与仍然有效的必须保护项；冷版本和旧事件进入一层 `routes/` 页面，明确命中才继续读取。
- 英文、编号和版本按边界匹配，`health` 不再误命中 `Healthmonitor`；短中文弱词不能单独展开整条历史路线。
- 第一次真实启用后必须独立只读核对检查点、路由和业务文件边界；第二次启用必须让完整记忆目录保持不变。
- 本地 v0.2.7 包不会自行发布、修改服务器或覆盖本机已安装版本；公开 updater 在正式发布前仍以公开 manifest 为准。

## v0.2.6 升级说明

- 一条长期记忆只保留一份正文，`index.md` 只保存作用范围、别名/关键词、正文位置和一句唤醒原因。
- 当前动作碰到的禁令、否决方案、稳定行为、验收条件、未解决冲突和不可逆操作保护必须全部召回，不设 top-k 截断。
- 最近 30-60 行只用于了解刚才发生了什么，不是总召回上限；没命中、别名冲突、资料矛盾、第一次碰某对象或不可逆操作会扩大查找。
- 新 `session-log.md` 只记录未解决事项、回滚、尚未归位的纠正、`[REVIEW]` 暂存和少量检查点，普通顺利过程不再写流水账。
- 老日志不删除、不轮转、不换文件；接管时记录旧长度和前缀 SHA256，在同一文件只追加一次可验证检查点，重复接管不再写入。
- 升级时不扫描所有项目。老用户回到以前运行过 Lite Demo 的项目或会话后，第一次输入 `启用外挂记忆`（或其他兼容启动口令）会先问一次：`继承并升级整理旧记忆` 还是 `全新启动`。选继承后整理一次旧记忆，不需要再输入迁移命令，也不会执行旧任务或修改业务文件；选全新则旧记忆冷存、不默认召回、不声称已继承。
- 整理成功后，下一次上下文清理或压缩会从新的精简索引和按需正文恢复；已经进入当前上下文的旧内容由这次清理/压缩移走。
- 本地 v0.2.6 包不会自行发布、修改服务器或覆盖本机已安装版本；公开 updater 在正式发布前仍以公开 manifest 为准。

## v0.2.5 升级说明

- 完整 `session-log.md` 继续保存在本地，不强制删除、轮转或改写；正常恢复只读最近 30-60 行或几张审计卡。
- 旧证据按锚点指针、冲突或信息缺口做关键词/行段定向读取，不默认把长日志全文打入上下文。
- `active-task.md` 只保留当前目标、步骤、关键纠正/否决、稳定边界、证据指针和下一步，不逐批累计时间线。
- 健康检查只对锚点职责漂移和长日志给软警告，不做不可逆自动处理。
- 保留 v0.2.4 的任务记忆提示文案、一个公开 skill、memory-only 和工程协议退让。

Codex 应使用已安装 skill 内的脚本：

```powershell
pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File "<codex-home>\skills\agent-memory-stack-lite-demo\scripts\update-from-server.ps1"
```

升级流程先比较版本：同版本不重复安装，本机版本更新时不自动降级；确需安装时才下载并校验 SHA256。包检查和安装失败会直接报错，成功前会重新读取真实安装版本。它不需要服务器密码、账号密钥或外部执行工具。

升级完成后，在项目会话中说：

```text
启用外挂记忆
```
