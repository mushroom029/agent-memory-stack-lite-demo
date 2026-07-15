# Automatic Legacy Memory Takeover

Use this automatically on the first Lite Demo v0.2.7 activation inside any
existing memory root that has not completed the current takeover. This includes
pre-v0.2.6 roots, correct v0.2.6 roots, and partially reorganized roots. Do not
require a second user command.

## Activation Boundary

This is memory maintenance, not old-task execution. It is allowed when the user
message contains only `启用外挂记忆`, `启动外挂记忆`,
`本会话启用外挂记忆`, or `启动lite demo`.

During takeover, modify only the discovered memory root. Do not resume the old
task, touch business files, start services, run project tests, deploy, or scan
other projects.

## One-Time Detection

Run `scripts/takeover-memory.py inspect <memory-root>`.

- `takeover_required: false`: skip takeover silently and continue normal
  activation.
- `takeover_required: true`: perform the steps below before the normal
  activation response.

Completion has one rule with no exception: `index.md` must contain exactly one
memory-schema entry set to `v0.2.7`, and `session-log.md` must contain exactly
one verified v0.2.7 checkpoint. A package version, schema alone, duplicate or
conflicting schema entries, no log, or an older v0.2.6 checkpoint does not prove
completion. Branch only on `takeover_required`; do not combine fields or infer
completion independently.

## Automatic Takeover

1. Record the initial session-log byte length and SHA256 from `inspect` when a
   log exists. These identify the immutable legacy prefix.
2. Use a task-local takeover anchor under `tasks/` so an old active task is not
   overwritten. Record only the migration route, not old-task progress.
3. Do not write `Memory schema: v0.2.7` manually. Read `current-context.md`,
   `index.md`, active task metadata, capsule
   filenames/headings/fields, and known domain-store maps. Do not read a long
   session log in full.
4. Convert legacy routes into compact
   `scope/aliases/keywords -> owners + mandatory + history + reason` entries.
   `owners` contains current normative bodies; `mandatory` contains every live
   touched-scope guard. Put cold versions/events behind one precise route page
   under `routes/`, and keep that page to one level. Do not leave many old
   version capsules attached to one generic top-level route.
5. Ensure touched scopes can wake all explicit prohibitions, rejected paths,
   stable behavior, acceptance criteria, unresolved conflicts, and
   irreversible-action guards. Use bounded log tail/search/range reads only to
   repair missing guards, conflicts, or exact evidence.
6. Keep ordinary ownership uncertainty as one `[REVIEW:<id>]` body with a
   `status=pending-review` route. Ask the user only when a hard user boundary
   conflicts and choosing silently would change behavior materially.
7. Slim `current-context.md` and live task anchors to current state and owner
   pointers. Never rewrite, rotate, rename, delete, or summarize over the old
   session log.
8. Probe representative ordinary-language task phrases with
   `route-memory.py`. Fix boundary misses, false substring matches, missing live
   guards, and broad primary owner fan-out. Then run
   `scripts/check-memory-root.py <memory-root> --strict-routing
   --allow-missing-schema`. Do not complete takeover if it fails.
9. Run `inspect` again and pass its current index/log hashes to `apply`, plus
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
10. Run strict validation without `--allow-missing-schema`, then run
    `takeover-memory.py verify <memory-root>` and a final `inspect`. Completion
    requires `completion_verified: true` and `takeover_required: false`.
11. Independently inspect the resulting files: the current marker must exist
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
