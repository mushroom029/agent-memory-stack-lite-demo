# Automatic Legacy Memory Takeover

Use this after the v0.2.17 startup choice gate authorizes inheritance, or when
the activation message already explicitly asks to inherit, reorganize, migrate,
repair, or continue from old memory inside an existing root that has not
completed the current takeover. This includes pre-v0.2.6 roots, correct
v0.2.6 roots, and partially reorganized roots. Do not require a second
migration command after the inheritance path is clear.

Package v0.2.17 keeps memory schema/checkpoint `v0.2.7` as the current
on-disk compatibility format, and adds the semantic completion requirement for
`legacy-destinations.md` when meaningful old history exists.

If the user names an old conversation, damaged conversation, old project,
archive, or legacy memory source outside the current root, use
[legacy-source-import.md](legacy-source-import.md) first. Automatic takeover of
the current root and referenced-source import share the same destination and
route proof; neither may claim completion from a schema marker alone.

## Activation Boundary

This is memory maintenance, not old-task execution. It is allowed when the user
chooses inheritance at the startup choice gate, or when the user message
contains an activation phrase plus explicit old-memory inheritance,
reorganization, migration, repair, or continuation intent.

Install-time migration of a standalone `skills/context-memory-index` is a
separate compatibility step: the old skill is moved out of active `skills/`
with hash/path/time/restore metadata and a destination status. It must not
remain active as a second public memory skill. Project memory takeover still
happens per target `docs/codex` root on activation.

During takeover, modify only the discovered memory root. Do not resume the old
task, touch business files, start services, run project tests, deploy, or scan
other projects.

## One-Time Detection

Run `scripts/takeover-memory.py inspect <memory-root>`.

- `takeover_required: false`: skip takeover silently and continue normal
  activation.
- `takeover_required: true`: perform the steps below before the normal
  activation response.

Completion has two layers:

1. `index.md` must contain exactly one memory-schema entry set to `v0.2.7`,
   and the root must hold exactly one verified v0.2.7 checkpoint — in the
   standalone `.takeover-checkpoint` file, or still inside `session-log.md`
   on a pre-v0.2.13 root (both verify; `migrate` moves the metadata without
   touching the log bytes).
2. When meaningful old history exists, `legacy-destinations.md` must prove that
   the old memory was inventoried and assigned reachable destinations under the
   current layout.

The destination proof must pass its full field/status/owner/probe validation.
Any `pending-review` entry is an honest incomplete scope and keeps takeover
required until it receives a settled destination; schema/checkpoint markers do
not override it.

For referenced old sources, completion also requires that the source itself was
inventoried. A new current root, a copied active task, or a link to the old
folder is not semantic import.

Meaningful old history is not a line-count-only concept. Short explicit
requirements, prohibitions, acceptance criteria, corrections, rejected paths,
stable behavior, regression guards, strong pressure, or do-not-resurrect
evidence are meaningful even if they are only a few lines. Detection must scan
the immutable session-log prefix and other legacy memory surfaces such as
`current-context.md`, `active-task.md`, `index.md`, `capsules/`, `tasks/`, and
`routes/`, while ignoring known empty starter templates.

A checkpoint whose kind is exactly `fresh-initialization` proves that later
current-context/index/capsule growth belongs to the new root, not to legacy
takeover input. This exemption applies only to that explicit fresh kind;
legacy, migrated, missing, malformed, or unknown checkpoint kinds keep the
full legacy-surface and destination checks.

A package version, schema alone, duplicate or conflicting schema entries, no
log, an older v0.2.6 checkpoint, or a checkpoint with no legacy destination
manifest does not prove completion. Branch only on `takeover_required`; do not
combine fields or infer completion independently.

## Automatic Takeover

1. Record the initial session-log byte length and SHA256 from `inspect` when a
   log exists. These identify the immutable legacy prefix.
2. Use a task-local takeover anchor under `tasks/` so an old active task is not
   overwritten. Record only the migration route, not old-task progress.
3. Do not write `Memory schema: v0.2.7` manually. Read `current-context.md`,
   `index.md`, active task metadata, capsule
   filenames/headings/fields, and known domain-store maps. Do not read a long
   session log in full.
4. Use [legacy-destination-manifest.md](legacy-destination-manifest.md) to
   create `legacy-destinations.md` when meaningful old history exists. Classify
   legacy items by function and owner reachability, not by project domain:
   `memory-owner`, `mandatory-guard`, `rejected-path`,
   `project-owner-indexed`, `archived-only`, or `pending-review`.
   `archived-only` needs a reason and cannot be a catch-all for unexamined old
   history. `project-owner-indexed` means the real body is owned by project
   files, code, data, reports, logs, generated outputs, tests, configuration,
   or local documentation while Lite Demo stores only the route.
   Direct user goals, prohibitions, acceptance criteria, and corrections from
   old memory are requirements by default; classify them with
   [user-requirement-ledger.md](user-requirement-ledger.md) instead of treating
   them as pressure-only evidence.
5. Convert legacy routes into compact
   `scope/aliases/keywords -> owners + mandatory + history + reason` entries.
   `owners` contains current normative bodies; `mandatory` contains every live
   touched-scope guard. Put cold versions/events behind one precise route page
   under `routes/`, and keep that page to one level. Do not leave many old
   version capsules attached to one generic top-level route.
6. Ensure touched scopes can wake all explicit prohibitions, rejected paths,
   stable behavior, acceptance criteria, unresolved conflicts, and
   irreversible-action guards. Use bounded log tail/search/range reads only to
   repair missing guards, conflicts, or exact evidence.
7. Keep ordinary ownership uncertainty as one `[REVIEW:<id>]` body with a
   `status=pending-review` route. Ask the user only when a hard user boundary
   conflicts and choosing silently would change behavior materially.
8. Slim `current-context.md` and live task anchors to current state and owner
   pointers. Never rewrite, rotate, rename, delete, or summarize over the old
   session log.
9. Probe representative ordinary-language task phrases with
   `route-memory.py`. Fix boundary misses, false substring matches, missing live
   guards, broad primary owner fan-out, and every wakeable destination in
   `legacy-destinations.md`. Then run
   `scripts/check-memory-root.py <memory-root> --strict-routing
   --allow-missing-schema`. Do not complete takeover if it fails.
10. Run `inspect` again and pass its current index/log hashes to `apply`, plus
   the initial legacy prefix identity when one existed:

   ```text
   takeover-memory.py apply <memory-root> --routes-verified \
      --expected-index-sha256 <current-index-hash> \
      --expected-log-sha256 <current-log-hash> \
      --legacy-prefix-bytes <initial-bytes> \
      --legacy-prefix-sha256 <initial-hash>
   ```

   If no log existed at preflight, omit log/prefix arguments and pass
   `--expect-no-log`. The helper writes the schema only after the checkpoint is
   safe. An old v0.2.6 checkpoint stays inside the preserved prefix and does
   not count as the current checkpoint.
11. Run strict validation without `--allow-missing-schema`, then run
    `takeover-memory.py verify <memory-root>` and a final `inspect`. Completion
    requires `completion_verified: true`, `takeover_required: false`, and no
    strict warning about `legacy-destinations.md`.
12. Independently inspect the resulting files: the current marker must exist
    exactly once, old bytes must match the recorded prefix, and no business
    file may have changed. A second normal activation must leave the complete
    memory directory byte- and timestamp-identical.

If a relevant memory file changes after the final preflight, apply must stop.
Do not mark completion or retry over the concurrent write.

## Ordinary User Reply

After successful automatic takeover, say only the useful result in ordinary
Chinese, for example:

```text
外挂记忆已启用。旧记忆已经按新方式整理，旧记录没有删除；下一次上下文清理或压缩后，会按新的索引按需恢复。要继续上次任务吗？
```

If takeover cannot finish safely, preserve the old memory and give one concise
reason. Do not expose schemas, capsules, hashes, or routing fields unless the
user asks for technical detail.
