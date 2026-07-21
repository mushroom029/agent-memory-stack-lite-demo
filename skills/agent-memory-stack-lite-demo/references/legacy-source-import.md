# Legacy Source Import

Use this whenever the user points to old Lite Demo memory from a previous
conversation, project, archive, or memory layout and asks the current
conversation to inherit, reorganize, continue from, or repair it.

This is domain-neutral. Product rules must stay domain-neutral. Specific
projects, local paths, app types, reports, or conversation names may appear in
tests or evidence, never as product conditions.

## Trigger Phrases

Apply this before creating a blank current memory root when the user says or
clearly means:

- old conversation memory should be organized into the current conversation;
- damaged conversation, failed conversation, or unusable conversation should be
  taken over here;
- inherit old version memory;
- migrate old memory to the current session;
- continue work from a referenced old project or memory source;
- "整理旧会话记忆到当前会话", "旧会话损坏，当前会话接管",
  "继承旧版本记忆", or "把旧记忆迁到现在这个会话".

If the referenced source is ambiguous or not found, do not ask the user to find
an internal memory path first. Use the user-friendly discovery flow below. Do
not silently create an empty `docs/codex/` and call that takeover.

## Universal Legacy Sources

Treat these as possible legacy sources, regardless of version wording:

- current or referenced project roots containing `docs/codex/`,
  `docs/context-memory/`, or `docs/context/`;
- old standalone `context-memory-index` skill folders or their non-destructive
  archives;
- memory roots produced by recommended or published Lite Demo versions,
  including v0.1.7 stable fallback, v0.1.8, v0.1.9, v0.2.0 suffix variants,
  v0.2.1 and later;
- unknown or user-modified memory layouts that look like local project memory.

Unknown structure is not ignored. Preserve it and classify unresolved value or
ownership as `pending-review`.

Do not perform a silent whole-machine or all-project scan by default. Lite Demo
is project-local unless the user names a source, opens a project root, or
explicitly authorizes a broader discovery pass. A future global project
registry or machine-wide scan must be opt-in and must report what paths it will
read before scanning.

## User-Friendly Missing Source Flow

When inheritance is requested but the exact source is missing, Codex should
find candidates for the user instead of asking for `docs/codex/`:

1. Search the current directory, resolved project root, and parent chain for
   `docs/codex/`, `docs/context-memory/`, and `docs/context/`.
2. Check explicit paths already visible in the conversation, open-file context,
   current/project AGENTS guidance, and Lite Demo archive metadata.
3. Present only a short candidate list with project names, root kind, paths,
   and last write times. Include `全新启动` as an option.
4. If no candidate is found, ask whether Codex may broaden discovery over
   named/common Codex project locations, or whether the user wants to return to
   the old project conversation and say `启用外挂记忆`, or start fresh.
5. Before a broader discovery pass, state the top-level paths to be scanned.
   During discovery, read metadata only until the user selects a source. Do not
   read long logs, memory bodies, or unrelated project content merely to build
   the list.

Only ask for a typed path after candidate discovery fails and the user chooses
to provide one manually.

## Import Flow

1. Identify two sides: the current target memory root and every referenced
   legacy source. If there are multiple plausible sources and choosing changes
   behavior, ask one focused question.
2. Inspect each legacy source before writing the current-session entry point.
   Prefer bundled helpers when the source is a Lite Demo memory root. Use
   bounded reads: current context, index/routes, active task, capsule headings
   and fields, manifest files, and targeted session-log search/ranges.
   Short explicit requirements or corrections count even without headings,
   `[REVIEW]`, Run Audit cards, or long line counts.
3. Inventory meaningful old items by function, not domain: explicit
   requirements, prohibitions, acceptance gates, corrections, stable behavior,
   rejected paths, unresolved conflicts, project-owner bodies, and cold
   evidence.
   Do not inventory by file number or storage role alone. A manifest that lists
   `capsules/C01.md`, `capsules/C02.md`, etc. with aliases such as
   `legacy capsule`, keywords such as `capsule owner`, generic reason
   `import route`, or many entries pointing to the same catch-all owner is not
   an import. It is only a file listing and must fail validation.
4. For every meaningful item, create or update a destination entry using
   [legacy-destination-manifest.md](legacy-destination-manifest.md):
   `memory-owner`, `mandatory-guard`, `rejected-path`,
   `project-owner-indexed`, `archived-only`, or `pending-review`.
5. For every wakeable destination, add aliases or keywords, an owner or project
   owner pointer, and route probes. Mandatory guards must wake for touched
   scopes without top-k truncation. Non-`archived-only` destination entries are
   supplemental routes: their route probes must resolve through
   `route-memory.py` or equivalent owner-resolution, while `archived-only`
   entries remain cold and do not wake by default.
6. Only after the legacy source has destinations may the current conversation
   create or refresh its own active task/current context to continue work. This
   is memory import, not permission to run the old task.
7. Validate with `route-memory.py` probes and `check-memory-root.py
   --strict-routing` when operating inside a Lite Demo root.

## Completion Blockers

Do not claim import or takeover complete when:

- a meaningful old item has no destination status;
- `archived-only` is used for unexamined old history;
- `pending-review` affects the work being claimed complete;
- a wakeable item lacks aliases/keywords, owner pointer, or route probe;
- a wakeable item has only generic wake terms such as `legacy source`,
  `legacy capsule`, `import evidence`, or a source filename scope such as
  `capsules-C01`;
- many non-archived legacy entries collapse onto one generic memory owner
  instead of being merged into a small number of semantic owners or marked
  `archived-only` with reasons;
- `project-owner-indexed` points to a memory-layer file such as
  `capsules/C01.md` instead of a real project owner outside the memory layer;
- an explicit old user requirement conflicts with the current target and the
  conflict gate in [user-requirement-ledger.md](user-requirement-ledger.md) has
  not run;
- the current root was initialized but the referenced old source was never
  inventoried.
