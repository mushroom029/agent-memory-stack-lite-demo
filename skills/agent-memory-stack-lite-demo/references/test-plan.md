# Lite Demo Test Plan

Use this plan to test whether project-local memory improves Codex route retention.

## Package Checks

Run:

```powershell
pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\check-package.ps1
```

Validate the single bundled public skill with the skill validator.

Validate package memory with the internal memory root checker.

## Hard Local Gates

Do not treat a local polish package as ready unless:

- card-only recovery can answer next exact step, active anchor, protected modules, artifact discipline, encoding status, memory hygiene, tests/evidence, and this-run verdict after a simulated interruption;
- Chinese memory/log/UI text remains UTF-8-readable on a clean machine, with sentinel phrases still intact and no mojibake;
- Run Audit narrative notes are optional evidence appendices, not the default required output.
- when the bounded tail helper is deliberately selected, 10, 100, and 1000
  chronological batches return at most 60 lines while the complete log hash
  remains unchanged; default activation never invokes that tail;
- 10, 100, and 1000 routing entries return every touched-scope body owner and
  all mandatory guard owners, while unrelated owners remain unloaded;
- explicit prohibitions, rejected paths, stable behavior, acceptance criteria,
  unresolved conflicts, and irreversible-action guards achieve 100% recall in
  deterministic touched-scope fixtures;
- a route miss and irreversible action request wider retrieval instead of
  claiming that no historical boundary exists;
- legacy takeover preserves the recorded byte prefix and SHA256, leaves exactly
  one current checkpoint (standalone `.takeover-checkpoint`, or in-log on a
  pre-v0.2.13 root) and one current schema entry, and a second
  takeover is byte-idempotent;
- first activation detects an old unmarked root and asks the one-time
  fresh-start-vs-inherit question; choosing inheritance enters memory-only
  takeover without a second migration command or old-task execution;
- a fresh v0.2.7 root is created only by trusted atomic initialization (the
  bundled `initialize` command or the package/install initialization helper)
  and immediately has one current schema plus one sparse checkpoint;
  `initialize` rejects any existing root;
- a legacy no-log root, a root where v0.2.7 schema was written prematurely,
  and a correct v0.2.6 root all require one v0.2.7 takeover; a broken owner
  route cannot receive current completion proof;
- a legacy root with meaningful old history cannot receive completion proof
  until `legacy-destinations.md` assigns every meaningful legacy item a
  domain-neutral destination status, owner or archived reason, wake-up terms
  for non-archived entries, and route-probe evidence;
- successful takeover makes the next `inspect` report `takeover_required:
  false`; later activation is read-only with respect to migration state;
- duplicate or conflicting schema entries, bad/missing checkpoint fields, a
  bad prefix hash, and duplicate current markers cannot claim completion;
- a log create/append or index mutation injected during strict checking stops
  apply, preserves the concurrent content, and writes no schema/checkpoint;
- real activation validation starts from an untouched old-project copy, gives
  Codex only an activation phrase, and independently checks the resulting
  schema/checkpoint, routes, business-file boundary, and second-activation full
  directory byte/timestamp identity;
- `health` does not match `Healthmonitor`, `C5` does not match `C50`, and
  `v0.2.7` does not match `v0.2.70`; weak short terms cannot open a route by
  themselves;
- generic current work loads primary owners plus every mandatory guard but no
  cold history owner; an explicit version/event descends into exactly one
  `routes/` page and loads every precise match without top-k;
- missing, outside-root, nested, orphan, or primary/history-duplicate route
  pages fail strict takeover validation and do not load invalid history owners;
- checker warnings cover missing owner routes, broken owner pointers, stranded
  `[REVIEW]` items, repeated live fields, and long cross-layer narrative copies;
- discharge distinguishes `R1` from `R10`/`XR1`, accepts dotted IDs, retains
  open or ownerless entries, moves every exactly settled structured type, and
  preserves UTF-8/CRLF/no-final-newline entry bytes in its archive;
- an early rejected path remains retrievable through targeted search even when
  it is outside the recent tail;
- an oversized active task and a long session log produce soft health warnings
  without deletion, rotation, rewrite, or a nonzero validator exit;
- recovery references contain no default full-log read, default tail injection,
  or forced 60-line archive wording.
- `archived-only` is never used as a catch-all for unexamined legacy history.
- explicit user goals, prohibitions, acceptance criteria, and corrections are
  routed through the Requirement Ledger and are not downgraded as pressure,
  frustration, or weak memory;
- when a new target conflicts with a stored explicit user instruction, Codex
  states the conflict and offers A. keep the existing instruction and adjust
  the current target; B. temporary scoped override only for this
  creation/process; C. ask the user to complete or replace the command;
- old conversation, damaged conversation, old project, archive, old memory
  folder, and unknown legacy source import all run the same legacy-source
  inventory and destination proof before any completion claim;
- short explicit legacy requirements, prohibitions, acceptance criteria, and
  corrections require `legacy-destinations.md` even when the old session log has
  no heading, no `[REVIEW]`, no Run Audit card, and fewer than 20 non-empty
  lines;
- old meaningful content in `current-context.md`, `active-task.md`, `index.md`,
  `capsules/`, `tasks/`, or `routes/` requires legacy destinations even when
  there is no `session-log.md`;
- v0.1.7 stable fallback, v0.1.8, v0.1.9, v0.2.0 suffix variants, v0.2.1 and
  later, plus unknown layouts, are treated as possible legacy sources rather
  than skipped by version wording;
- Lite Demo does not silently scan every project on the machine. Any global
  registry or whole-machine discovery is opt-in and path-visible.
- product rules remain domain-neutral. Project-specific names may appear only
  in fixtures/evidence, not in core rules.
- `scripts/test-v0217-derived-memory.ps1` proves the v0.2.17 derived index
  foundation: deterministic cache build, no narrative-body cache copy,
  mandatory guard output outside ordinary ranking, default exclusion of live
  `session-log.md` and `legacy/session-log-*` body records from ordinary
  recall, exact in-flight ID selection, duplicate-free continuation pages,
  stale-token rejection after source changes, filter-bound continuation
  rejection, filterable pointer recall by channel/memory class/status/source
  prefix, multi-topic pointer recall with optional live-anchor pointers,
  related-record pointer lookup, and idempotent rebuild.
- `scripts/scan-layer-quality.py <memory-root> --require-derived-cache` must
  be run on generated pressure-test memory roots. It fails when models misuse
  the five layers: live anchors become chronology, routes become body stores,
  owners lack wake-up routes or duplicate a body, session-log becomes routine
  history, or derived cache stores narrative/log bodies instead of bounded
  pointers.
- run `scripts/scan-memory-bloat.py <memory-root>` when pressure-testing real
  or simulated long conversations. It must inspect all memory files, not only
  `session-log.md`, and fail high-risk cases where live logs, always-read
  anchors, route files, or directly routed legacy logs can grow into default
  context injection hazards.
- derived retrieval comparison against `agent-memory-mcp` is an explicit
  quality check, not a promise to clone MCP. Keep Lite Demo's source of truth in
  Markdown owners and routes. Accept Lite-native pointer enhancements when they
  improve local recall without adding external databases, embeddings, daemon
  processes, automatic prune/delete, or body injection into the cache.
- `scripts/test-large-text-source-intake.ps1` proves the long local source
  intake helper can detect chapter-like headings, write bounded source-slice
  artifacts, produce a manifest and compact index, and keep raw body text out of
  memory-style indexes.
- real long local text, novel, transcript, or exported-chat pressure tests must
  use source-slice artifacts before memory owner writing. Memory owners may
  store interpretation, routes, boundaries, and continuation guards, but must
  not copy raw large bodies into live anchors, route files, `session-log.md`, or
  the derived cache. The final audit must prove selected chapter count, slice
  manifest/hash presence, sparse session-log behavior, derived pointer build,
  and user-requested delivery artifacts. Use
  `scripts/check-large-text-intake-artifacts.py <replay-root>
  --expected-chapters 20` during controller review; a slice-only run is failed.
- concurrent runtime replay must prove each subagent loaded the same Skill_X,
  wrote only inside its own workspace, produced a final trace and
  machine-readable result, and finished with no `completed_with_gaps` status.
  Every generated memory root must have exactly one current schema and one
  verified `.takeover-checkpoint`; activation-only messages must not stall
  final reporting or convert current-session replay entries into legacy
  takeover input.
- pressure replay closeout must be self-contained. `result.json` must include
  `controller_intervention_required:false`, `post_hoc_artifact_repair:false`,
  `missing_artifacts_repaired_after_prompt:false`, `round_count`, explicit
  `pass/status/gaps`, and paths to delivery, trace, and machine-readable
  evidence. `state.json` must register every round and every required
  validation summary before the subagent claims PASS. It may use either compact
  per-round keys (`round_01`) or a `rounds` array of objects, but the
  machine-readable result must name transcript and validation paths. Use
  `scripts/check-runtime-replay-artifacts.py <replay-root> --expected-rounds 20`
  during controller review. If the helper fails, the replay is failed even when
  the final memory root validators pass. The helper proves file closeout only;
  the controller must separately record whether the subagent actually returned
  a final completed response. A run whose files pass but whose agent remains
  running or must be closed by the controller is a communication closeout risk,
  not a clean end-to-end PASS.
- pressure replay scenarios must run at least 20 user-input rounds per
  subtask. Short continuation inputs caused by interruption, such as `继续`,
  `继续工作`, `继续按照计划进行`, or equivalent resume-only user messages, count
  as real rounds. They must trigger anchor/route/owner recovery and derived
  pointer recall; do not skip them as noise, do not save them as hard long-term
  rules, and do not let them write routine chronology into `session-log.md`.

## Install Checks

Test these paths:

- extracted package install;
- zip-only folder bootstrap;
- install into a temporary Codex home;
- optional project AGENTS install into a temporary project;
- install with `-PreauthorizeMemoryLanding`;
- repeat install without duplicate AGENTS blocks.
- reinstall a newer zip over an older installed version and verify skill version plus AGENTS refresh;
- upgrade a v0.2.0f CodexHome and verify the exact known legacy `context-memory-index` is archived outside `skills/`;
- place a changed/independent `context-memory-index` beside Lite Demo and verify it is non-destructively archived outside active `skills/` with hash, original path, archive path, time, restore metadata, and `pending-review` destination metadata;
- put multiple versioned zips in one folder with misleading timestamps and verify the highest semantic version is selected;
- verify updater decisions for newer, same, older, and unknown installed versions;
- inject a child package-check/install failure and verify nonzero updater exit with no success JSON;
- verify the updater rereads installed `VERSION.txt` before reporting success;
- verify transactional replacement stages before swapping and leaves the previous skill available on pre-commit failure.

## Demo Task Checks

Choose a safe scoped project task and record:

- whether the installed demo activates from the primary phrase `启用外挂记忆`;
- whether `启动外挂记忆`, `本会话启用外挂记忆`, and legacy `启动lite demo` activate memory without requiring the long setup prompt;
- whether installation exposes only one public skill and no extra memory-skill install target;
- whether a fresh memory root was created by the bundled `initialize` helper,
  not by hand-written schema/log files, before any task anchor or capsule writes;
- whether activation-only input avoids command execution, service startup, tests, code edits, and old-task auto-resume;
- whether activation-only input permits exactly one old-user exception after
  the startup choice gate: inheritance maintenance inside an unmarked legacy
  memory root, with no business-file edits, project tests, service startup, or
  old-task execution;
- whether old users see the v0.2.17 fresh-start-vs-inherit choice exactly once
  when needed, and need no second migration command after choosing inheritance;
- whether a user-named old conversation, damaged conversation, old project, or
  unknown memory source is inventoried as a legacy source before the current
  conversation creates or claims a replacement memory entry point;
- whether a no-memory project gets at most one plain activation suggestion after 2-3 meaningful rounds or clear complexity signals;
- whether refusal creates no `docs/codex/`, no AGENTS state, no stored refusal marker, and causes current-session-only skip;
- whether later explicit `启用外挂记忆` or `启动外挂记忆` overrides the current-session skip;
- task goal;
- whether `active-task.md` existed before execution;
- whether the active task contains the policy scope and is the only authoritative live policy store;
- whether `ExecutionPolicy` was recorded as `external`, `lite-anchor`, or `unknown`;
- whether `model-native-workflow` appears only as an `ExecutionPolicy source` note and never as a fourth `ExecutionPolicy` state;
- whether model names or strength judgments do not directly trigger policy changes;
- whether `Execution protocol skills` records only execution skills explicitly triggered and applied to the task;
- whether Lite Demo avoided adding a second execution flow when `ExecutionPolicy: external`;
- whether Lite Demo stays memory-only when an external protocol or model-native workflow already owns the execution flow;
- whether the task-scoped protocol sniff happens before Lite Demo's fallback engineering protocol and does not ask the ordinary user to choose a policy;
- whether `lite-anchor` starts as a light mirror when scope/boundary/evidence/next step are clear, and becomes fuller only after drift, repeated failure, forgotten correction, stable-module mistake, compression recovery failure, or high pressure;
- whether memory hygiene kept one-off requests, pressure phrases, failures, and short acknowledgements from becoming hard long-term rules;
- whether explicit user goals, prohibitions, acceptance criteria, and
  corrections bypass the weak-memory default and receive a requirement owner,
  route, and mandatory recall when relevant;
- whether a durable rule write used one rare plain-Chinese reversible readback when the user's wording was ambiguous;
- whether only explicit absolute wording created a hard boundary;
- whether user correction downgraded or removed a remembered preference;
- whether an existing artifact was reused before rerunning a network/API/model call unless stale, invalid, missing, or explicitly regenerated by the user;
- whether the latest nontrivial run wrote a compact Run Audit card by default, with verdict, next exact step, active anchor, protected modules, artifact discipline, encoding check, memory hygiene, tests/evidence, and memory writes;
- whether narrative audit notes stayed optional and appeared only when the compact card could not carry needed evidence;
- whether Chinese memory/log/UI edits used UTF-8-safe writes and passed a lightweight sentinel/mojibake check;
- whether first memory-root creation asked for confirmation unless install/preauthorization applied;
- whether an ambiguous unfinished-task situation asks which task memory the current conversation should use with `Lite Demo 提醒：`, a one-line task name, and previous progress, using ordinary Chinese rather than workflow or task-manager terms;
- whether `Lite Demo 提醒：` appears only for memory routing, memory/risk boundaries, or clear overlap warnings, not ordinary progress reports or code explanations;
- whether overlap wording says memory can be separate but project files are the same, without promising code/file isolation;
- whether a clear new task or "same method again" request creates/uses a same-root task-local anchor without asking again and without changing the old task memory;
- whether reusable workflow adjustments stay task-local until the user clearly asks to keep them as the new shared way;
- whether a new complex task line used a same-root task branch anchor instead of a second memory database;
- whether the compact routing index matched strong-relevance terms and opened only related capsules;
- whether index entries stayed as scope/alias/keyword -> body owner + mandatory
  guard owners + one short reason instead of copying body detail;
- whether each durable write chose one normative body owner and received a
  wake-up route in the same work unit;
- whether every non-`archived-only` `legacy-destinations.md` entry with
  `probes=route-memory:<phrase>` resolves through `route-memory.py` or an
  equivalent owner-resolution check to its intended owner, without loading the
  old session log or archive body by default;
- whether every mandatory touched-scope guard owner was opened, without top-k;
- whether selected task-relevant memory was retained even when detailed, while unrelated capsules and session history stayed unloaded;
- whether default recovery started from active-task, current-context, index,
  and every matched owner/mandatory guard without injecting a session-log tail;
- whether log evidence was opened only for an exact unresolved route, source
  conflict, or evidence gap, using targeted search or a bounded range;
- whether active-task kept only the current route, one current Progress boundary,
  critical corrections/rejected paths/stable boundaries, evidence pointers,
  and next exact step instead of per-batch chronology;
- whether session-log admitted only unresolved failures/conflicts, rollbacks,
  unpromoted corrections, provisional `[REVIEW]` bodies, and sparse
  checkpoints, with no routine green narrative;
- whether ordinary user replies avoided `ExecutionPolicy`, capsule, anchor, fingerprint, and routing-index terminology;
- failed path recorded;
- next exact step recorded;
- validation result;
- whether the task can resume from files after a simulated interruption.
- whether final runtime artifacts explicitly report pass/fail, gaps, and
  checkpoint/strict-routing status; a subtask that requires controller
  interruption to finish is a failure until the root cause is fixed and the
  whole replay is rerun. `check-runtime-replay-artifacts.py` must pass before
  controller accepts the replay as self-closing.
- whether `active-task.md` and any Run Audit card stay active/yellow/red when a
  user-requested `result.json`, report, trace, or delivery file is missing,
  unreadable, stale, or only promised in memory.

## Comparison

Run one small task without project memory and one similar task with project memory.

Compare:

- repeated mistakes;
- route drift;
- user re-explanation needed;
- recovery after pause;
- clarity of final handoff.

## Pass Signals

- The installed global AGENTS block stays short.
- `启用外挂记忆` activates the memory-only demo without requiring the long setup prompt.
- `启动外挂记忆` is treated as the same memory activation intent, not service startup or architecture discussion.
- Activation-only input reads or creates memory, then asks for a task or resume confirmation instead of executing old work.
- Fresh memory roots have one helper-created checkpoint immediately; current
  replay/session writes after a `fresh-initialization` checkpoint are not
  treated as legacy history on a later activation-only phrase.
- The package exposes one public skill; context-memory references remain internal implementation details.
- No-memory complex work can receive one plain Lite Demo suggestion; if refused, 本会话内不再主动询问 and no refusal state is persisted.
- A later explicit activation phrase overrides the current-session-only skip.
- Project AGENTS points to `docs/codex/` instead of storing history itself.
- Complex work creates or updates `active-task.md` before execution.
- The live execution policy exists only in the active task anchor; current-context/index do not duplicate it.
- Existing execution protocols keep execution ownership; Lite Demo records memory only.
- Model-native workflow ownership is recorded as source evidence under `external`, not as a new policy state or model-strength score.
- Without an explicit execution protocol, Lite Demo chooses lite-anchor without asking the user to prove absence.
- Lite-anchor weight adapts to observed need instead of always adding a full planning/testing ritual.
- Unknown is used only for explicit source conflicts or unreadable required project rules.
- Execution protocol skills are agent-recorded evidence, not runtime telemetry, and exclude available/tool-only skills.
- Memory hygiene is visible at durable-memory write points, but does not add a second planning/testing workflow.
- Short replies and pressure phrases stay task-local or revisable unless the user uses explicit absolute wording.
- Direct goals, prohibitions, acceptance criteria, and corrections are
  requirements by default and are not softened as emotion.
- Ambiguous durable rules get one plain-Chinese readback instead of a repeated approval ritual.
- Stable modules are not touched unless the user asks or the agent writes a Chinese stable-module protection judgment first.
- First memory-root creation is transparent and confirmed unless preauthorized.
- New complex task lines in an existing memory root are routed to the right task memory, not a second database.
- Unfinished-task ambiguity asks only which task memory to use; it does not ask the user to manage a workflow, task ID, session, or execution policy.
- A new task can reuse a validated method while keeping its own progress, failures, pressure, and next step task-local.
- Resumed work reads the anchor before changing route.
- The latest Run Audit card lets Codex answer the next exact step, active anchor, protected modules, artifact/model-call discipline, encoding status, memory hygiene, tests/evidence, and current run verdict without rereading noisy logs or relying on a narrative audit.
- Existing artifacts are preferred over repeated network/API/model calls unless stale, invalid, missing, or explicitly regenerated by the user.
- Chinese memory/log/UI text remains UTF-8-readable; sentinel phrases such as `启用外挂记忆`, `启动外挂记忆`, `稳定模块保护判断`, and `确认固化` are not mojibake.
- Failed paths are visible and not retried casually.
- Legacy local evidence remains byte-preserved while new memory uses sparse
  log admission, one body owner, compact routes, and selected evidence.
- Cross-conversation and damaged-conversation import cannot complete until
  every meaningful old item has a destination status, owner pointer or archived
  reason, wake-up terms when wakeable, and route-probe evidence.

## Fail Signals

- Global AGENTS becomes a memory dump.
- Codex starts complex work before creating the anchor.
- Live ExecutionPolicy fields are duplicated across active-task, current-context, index, or session-log.
- Lite Demo repeats planning, testing, or validation steps already required by another active execution protocol.
- Lite Demo adds a fourth `ExecutionPolicy` state for model-native behavior or changes policy because of a model name alone.
- Lite Demo scores model strength or sniffs every turn for workflow superiority.
- Lite-anchor is always heavy even when the agent already has clear scope, boundary, evidence, and next step.
- Lite Demo presents its protocol record as automatic runtime telemetry.
- Lite Demo records available, ignored, or tool-only skills in the protocol evidence.
- Lite Demo asks whether to enable lite-anchor only because no explicit protocol was found.
- A tool-only skill is treated as the execution protocol owner.
- A short reply such as `好` or `继续` is saved as a hard project rule.
- A clear user prohibition, goal, acceptance criterion, or correction is
  dismissed as pressure or weak memory.
- Lite Demo adds formal risk labels, fixed cycle counters, disclosure queues, or acknowledgement state machines.
- The memory-hygiene nudge becomes a repeated questionnaire or duplicated test flow.
- Run Audit is only narrative, with no compact recovery card.
- Narrative Run Audit becomes the default required output instead of an optional evidence appendix.
- `Verdict: green | yellow | red` becomes a persistent global state, autonomous monitor, automatic gate, or excuse to skip review.
- Codex reruns a network/API/model call because testing is inconvenient while an existing valid artifact already answers the need.
- Chinese memory/log/UI files are written through implicit legacy encodings and contain mojibake.
- Codex changes a stable module because it looks cleaner or convenient, without a Chinese stable-module protection judgment.
- Codex silently creates `docs/codex/` in a project that did not request memory.
- Codex treats memory routing as a task lifecycle manager, session registry, workflow version chain, code-isolation system, or task scheduler.
- Codex asks ordinary users to choose task IDs, anchors, capsules, workflow pointers, or execution policies.
- Codex uses `Lite Demo 提醒：` for ordinary task talk, every reply, code explanations, or progress reports.
- Codex promises Lite Demo can protect, lock, isolate, merge, or safely separate project files.
- Codex automatically merges task memories, promotes workflow changes, or recommends that an old task switch to a new workflow without clear user intent.
- Codex asks to enable Lite Demo repeatedly in the same chat after the user refused.
- Codex writes a refusal marker, AGENTS rule, project memory note, or global skip table just because the user declined a suggestion.
- Codex treats a refusal as permanent and ignores a later explicit `启用外挂记忆` or `启动外挂记忆`.
- Codex asks the user to paste the long setup prompt after they said `启用外挂记忆`.
- Codex treats `启动外挂记忆` as a request to start a service, or discusses/imitates Lite Demo architecture instead of enabling memory.
- Codex asks the user to install, enable, or activate an internal memory reference as an extra skill.
- Codex auto-starts a local API, dev server, Electron helper, test run, or old active task after an activation-only phrase.
- Codex creates a second competing memory database instead of a same-root task branch.
- Codex initializes a fresh current memory root while ignoring the user-named
  old conversation, damaged conversation, or old project source.
- Session notes never become durable capsules.
- A long session log is read in full by default, or is deleted/rotated only to
  reduce recovery context.
- `active-task.md` accumulates a dated or per-batch history instead of replacing
  stale route summaries.
- `active-task.md`, current-context, or a Run Audit card says complete/green
  while a user-requested `result.json`, trace, report, or delivery artifact is
  missing, unreadable, stale, or lacks explicit pass/fail/gaps.
- The demo claims universal task success.
- The package asks for external tool setup or extra credentials.
- The updater skips SHA256 verification or asks for server credentials.
