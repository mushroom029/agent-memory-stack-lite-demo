# Encoding Discipline

Use this when Lite Demo or project memory touches Chinese text, UTF-8 files, JSON, Markdown, YAML, TOML, logs, or run-audit records.

This is a write-time guard. Do not treat console mojibake as proof that a file is corrupt until rereading with an explicit UTF-8 tool.

## Windows Rules

- Prefer PowerShell 7+ with `pwsh`.
- Avoid Windows PowerShell 5.1 for Chinese/UTF-8/JSON/Markdown/log writes.
- If Windows PowerShell 5.1 is unavoidable, pass explicit UTF-8 encoding on file reads and writes.
- Prefer `apply_patch` for Chinese memory/reference edits when practical.
- Write logs and generated memory files with explicit UTF-8.
- If Python touches Chinese text, use `python -X utf8` or set `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8`; still pass explicit `encoding="utf-8"` for file IO.

## Lightweight Check

After touching Chinese memory/log/UI text, run a small sentinel or mojibake scan instead of a broad audit.

Suggested sentinel terms:

```text
启用外挂记忆 / 启动外挂记忆 / 稳定模块保护判断 / 确认固化 / 角色识别 / 物品库
```

Pass signal: the touched file still reads as UTF-8 and key Chinese phrases are not replaced by mojibake such as `Ã`, `Â`, `�`, or long runs of `?`.

Fail signal: the next Codex would need to guess whether the memory says one thing or the text was damaged by encoding.
