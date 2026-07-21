# Large Text Source Intake

Use this when the user points Lite Demo at a long local text source, such as a
novel, transcript, exported chat, or large notes file, and asks Codex to turn
part of that source into local memory.

The source text remains evidence. Lite Demo memory stores interpretation,
routes, boundaries, and continuation notes. Do not paste large source bodies
into `current-context.md`, `active-task.md`, `index.md`, or `session-log.md`.

## Required Pattern

1. Create or reuse the task memory root through the normal Lite Demo gate.
2. Put raw source slices under a local artifact folder outside `docs/codex/`,
   for example `artifacts/source-slices/`.
3. Use `scripts/slice-text-source.py` for chapter-like text before reading or
   summarizing long bodies:

   ```powershell
   python -X utf8 <skill-root>\scripts\slice-text-source.py <source.txt> `
     --out-dir <project-root>\artifacts\source-slices `
     --start-chapter 1 --max-chapters 20 --min-found 20
   ```

   The default heading detector is conservative: after `第X章`, `Chapter N`, or
   `CHN`, it expects line end, whitespace, or a title separator. If a source uses
   no separator between the chapter number and title, pass an explicit
   `--heading-regex` and keep the chosen pattern in the manifest.

4. Read the generated `manifest.json` and `chapters-index.md` first. Then read
   only the selected chapter slice files needed for the current work.
5. Write durable understanding to one or more capsules, such as:
   chapter synopsis, character state, plot logic, world/scene rules, style, and
   continuation guardrails.
6. Add compact routes in `index.md` to those capsules. The route may point to
   the source-slice manifest as evidence, but it must not copy raw chapter
   bodies.
7. Build/query the derived pointer cache with `compile-memory.py` after memory
   files are written.
8. Before completion, verify required delivery artifacts exist and are readable.
   If the user asked for `result.json`, a trace, or a report, missing files are
   blockers: keep the active task open and write the next exact step.

Slicing is not completion. After `slice-text-source.py` succeeds, the task is
still open until interpretation owners, routes, derived pointer recall evidence,
and requested delivery artifacts exist. For replay or pressure-test work, run:

```powershell
python -X utf8 <skill-root>\scripts\check-large-text-intake-artifacts.py <replay-root> `
  --expected-chapters 20 --required-topic 主线冲突 `
  --required-topic 人物关系 --required-topic 写法特点
```

If this helper fails, report the run as failed even when source slices were
created successfully.

## Source Slice Contract

`slice-text-source.py` writes:

- `manifest.json`: source path, source hash, heading regex, selected chapter
  count, per-chapter line/char ranges, slice file path, and slice hash.
- `chapters-index.md`: a compact human-readable slice index.
- `chapters/chapter-NNN.txt`: one raw source slice per selected chapter.

These files are artifacts, not memory owners. They can be referenced by
capsules as evidence and reread when precise source inspection is needed.

## Failure Rules

- If chapter headings are not detected or fewer chapters are found than the user
  requested, report the gap instead of inventing boundaries.
- If selected slices are too large to read in one pass, process them in smaller
  batches but keep chapter-level source files as the evidence boundary.
- If memory owners are written but delivery artifacts are missing, the run is
  not complete.
- If `session-log.md` starts receiving routine chapter summaries, stop and move
  settled content into capsules, then discharge or leave only unresolved items.

## Boundaries

- Do not treat this as OCR, semantic search, or a vector database.
- Do not rewrite the source text.
- Do not store copyrighted or private source bodies in the derived cache.
- Do not claim the source was understood if only the headings or manifest were
  read.
- Do not stop after creating `artifacts/source-slices/`; that is only the
  intake boundary. The memory value comes from the selected interpretation
  owners and their recall routes.
