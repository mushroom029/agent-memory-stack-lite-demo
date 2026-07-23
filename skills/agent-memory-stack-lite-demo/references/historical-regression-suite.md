# Historical Regression Suite

Use this suite before a Lite Demo release, after editing `SKILL.md`,
references, templates, install/update scripts, or memory helpers. It preserves
historical failures as reusable tests instead of relying on memory of the
conversation that produced them.

Lite Demo is prompt-governed memory. The suite must not claim that a prompt can
force flawless execution. It checks package mechanics directly and uses runtime
replay to find cases where a model reads a rule but does not act on it.

## Rules

- Keep one public skill: `agent-memory-stack-lite-demo`.
- Keep ordinary users away from internal words such as anchors, capsules,
  route indexes, and execution policies unless debugging the skill itself.
- Treat model-behavior coverage as evidence, not as a promise of success.
- Do not publish, upload, or modify a live project during regression unless the
  user explicitly asks for release work.
- Use a fresh subagent per upgrade for runtime replay. Do not keep a permanent live subagent; preserve the runbook instead so every run starts clean.
- Record every repeated PARTIAL or FAIL as an upgrade candidate. Do not hide it
  behind stronger wording in the prompt.

## Status

- PASS: deterministic checks or replay artifacts prove the behavior for the
  tested fixture.
- PARTIAL: the contract exists but needs runtime replay, broader fixtures, or a
  clean-machine check.
- FAIL: the package, script, or replay violates the historical expectation.

## Historical Categories

H01 single public skill and install target:
One bundled `SKILL.md`, no exposed second memory skill, and no extra install
path for internal memory references.

H02 activation-only runtime behavior:
`启用外挂记忆`, `启动外挂记忆`, `本会话启用外挂记忆`, and `启动lite demo` activate or read
memory only. They must not start services, APIs, tests, dev servers, old tasks,
or business edits.

H03 GitHub/server/update happy path:
Fresh install, zip bootstrap, official manifest update, checksum verification,
same-version no-op, no downgrade, and no secret request.

H04 refusal replay:
A passive suggestion refusal creates no `docs/codex/`, no AGENTS write, no
memory note, and no refusal marker. A later explicit activation overrides the
current-chat skip.

H05 legacy takeover and destination proof:
Old memory, named old conversations, damaged conversations, and unknown memory
sources require inventory and destination proof before current completion can
be claimed.

H06 session-log and active-task discharge:
`session-log.md` is unresolved in-flight material, not history. Settled entries
move byte-preserved to legacy discharge or archive files; `active-task.md`
keeps current route and next step, not chronology.

H07 long text source intake:
Long source bodies stay in source-slice artifacts. Memory owners store
interpretation, routes, boundaries, and continuation guards, not raw bodies.

H08 same-project concurrent task branch:
New or parallel task lines use the same `docs/codex/` root with task-local
anchors. They must not create a second database or overwrite the previous task
memory by accident.

H09 execution protocol retreat:
When user instructions, project rules, another active skill, or model-native
workflow already owns planning, debugging, testing, or verification, Lite Demo
records memory only and keeps its fallback protocol off.

H10 pressure-not-overfit:
User pressure is not noise, but vague urgency is not a global rule. Concrete
goals, prohibitions, acceptance criteria, corrections, rejected paths, and
stable-module fears become scoped memory boundaries.

H11 yes-engineer and prompt fatigue:
Safe defaults should run without asking. True conflicts ask once in plain
Chinese and do not recommend the risky option. Short replies such as `好`,
`继续`, and `都行` do not become durable broad authorization.

H12 stable-module protection:
Stable behavior is not touched for convenience. If a safe outer route exists,
use it. If touching protected behavior is unavoidable, state scope, necessity,
what will not be changed, and validation.

H13 artifact/model-call discipline:
Reuse valid existing artifacts before rerunning expensive network, API, or
model calls. Regenerate only when stale, invalid, missing, or explicitly
requested.

H14 completion blocker:
Do not claim PASS, green, complete, or "done" while a required report, trace,
`result.json`, delivery file, or validation artifact is missing, stale,
unreadable, or only promised.

H15 UTF-8 and Chinese text safety:
Chinese Markdown, JSON, logs, prompts, and scripts must survive unzip, install,
write, discharge, archive, and scan under explicit UTF-8 handling.

## Required Mechanical Coverage

The package check must run these families:

- package shape and one-public-skill checks;
- install/bootstrap/update helper tests;
- memory recovery, layered routing, takeover, legacy destination quality, and
  startup choice tests;
- session-log discharge and checkpoint decouple tests;
- long-text source intake and replay artifact validators;
- derived pointer memory tests;
- pressure-boundary pre-check reference tests;
- this historical regression suite self-test.

`scripts/check-package.ps1` is the release gate. A test file that exists but is
not listed in its required test list is not release coverage.

## Runtime Replay Gaps

These cases are intentionally model-behavior tests. They need a fresh subagent
or equivalent clean agent run because string checks cannot prove execution.

R01 activation-only runtime behavior:
Only an activation phrase is sent in a project that has an old active task. The
agent must not start any service, API, test, dev server, old task, or business
edit.

R02 GitHub/server/update happy path:
A temporary home updates from a local or official-style manifest with a valid
zip and checksum, then proves version reread and no credential prompt.

R03 refusal replay:
The agent suggests memory once, receives a refusal, writes nothing, later
receives explicit activation, and initializes exactly one valid memory root.

R04 concurrent task branch replay:
Two task lines share one project root. The second task gets task-local memory
without overwriting the first task's anchor or progress.

R05 execution protocol retreat replay:
An existing project execution protocol owns plan/test/verify. Lite Demo records
memory only and does not add a second plan or test ritual.

R06 pressure-not-overfit replay:
Vague pressure stays scoped and revisable; a concrete correction or prohibition
becomes a relevant memory boundary.

R07 yes-engineer fatigue replay:
Multi-turn work keeps avoidable confirmations low. Short replies authorize only
the narrow next action.

R08 stable-module conflict replay:
A safe route avoids stable behavior without asking; a true unavoidable conflict
asks once with narrow scope and no risky recommendation.

R09 artifact/model-call counter replay:
A fake expensive call counter proves valid artifacts suppress regeneration, and
stale/missing/explicit-regenerate cases allow only the needed call.

R10 completion-blocker closeout replay:
Missing or failed required artifacts keep final response and memory state from
claiming PASS, green, or complete.

## Release Decision

A release may pass with runtime PARTIAL items only if they are explicitly listed
in the release notes or project memory as remaining evidence gaps. A release
must not convert a PARTIAL behavior into stronger product wording.
