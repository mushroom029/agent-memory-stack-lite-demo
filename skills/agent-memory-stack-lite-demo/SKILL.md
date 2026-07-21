---
name: agent-memory-stack-lite-demo
description: Install, update, and operate a memory-only Codex demo stack with project-local current-context, layered current/history routes, capsules, sparse session logs, active-task anchors, a one-time fresh-start-vs-inherit choice on the first activation after upgrade before older project memory takeover, cross-conversation legacy-source import, explicit user-requirement preservation, and a one-time passive activation suggestion. Use when the user says "启用外挂记忆", "启动外挂记忆", "本会话启用外挂记忆", the legacy phrase "启动lite demo", asks to upgrade/update Lite Demo, opens an old Lite Demo project after upgrade, asks to inherit/reorganize old or damaged conversation memory into a current conversation, installs from a fresh-machine zip, sets up project docs/codex memory, preserves failed paths, routes parallel task memory, or proves compression/interruption recovery without external executors or extra credentials.
---

# Agent Memory Stack Lite Demo

Use this skill to install and demonstrate the memory-only workflow.

## Core promise

Help Codex keep the route of a real task visible:

- what the user wants;
- what has already been tried;
- which paths failed;
- what the next exact step is;
- how to resume after compression, restart, or thread reuse.
- how to keep legacy evidence byte-preserved while new memory uses one body
  owner, compact wake-up routes, sparse unresolved logs, and selective loading.
- how to import a user-named old conversation, old project, archive, or unknown
  legacy memory source before creating a blank current-session entry point.
- how to ask once, on first activation against an incomplete old memory root,
  whether the user wants a fresh 0.2.17 start or explicit old-memory inheritance.
- which explicit user goals, prohibitions, acceptance criteria, and corrections
  must survive as requirements instead of being softened as pressure.
- which task memory the current conversation should read/write when unfinished
  or parallel work creates ambiguity.
- whether the latest meaningful run had route, artifact, encoding, or memory-hygiene risk.

Do not present the demo as universal problem solving. The value is route retention and recovery.

Lite Demo keeps its memory layer active but does not activate its lightweight
fallback engineering protocol when the user, project rules,
another triggered skill, or a model-native workflow already defines how to
debug, plan, test, deploy, refactor, or verify. In that case, Lite Demo records
the active protocol's state and results. Only when no explicit execution
protocol exists may it use the adaptive lite-anchor fallback, starting as a
light memory mirror and becoming fuller only after drift, repeated failures,
forgotten corrections, compression recovery failure, stable-module mistakes, or
high pressure.

Before writing durable project rules, Lite Demo distinguishes explicit
requirements from ambiguous memory hygiene. Direct user goals, prohibitions,
acceptance criteria, and corrections are requirements by default. One-off
ambiguous requests, pressure phrases, local failures, and short
acknowledgements stay weak or task-local unless they become explicit
requirements.

When a no-memory project becomes nontrivial, Lite Demo may suggest activation
once in plain Chinese. If the user refuses, do not create memory or persist that
refusal; just stop suggesting again in the current chat. A later explicit
activation phrase overrides the temporary skip.

When a memory root already has an unfinished task and the current conversation
might be a new task line, Lite Demo only routes memory. It answers one question:
which task memory should this conversation use? It must not manage task
lifecycles, decide whether another conversation is still running, schedule task
order, isolate code files, merge tasks, or version workflows.

## Internal memory workflow

This package is one public skill: `$agent-memory-stack-lite-demo`.

The detailed current-context, index, active-task, capsule, session-log, and
recovery workflow is bundled as internal references under this skill:

- [references/context-memory-workflow.md](references/context-memory-workflow.md)
- [references/context-memory/layout.md](references/context-memory/layout.md)
- [references/context-memory/templates.md](references/context-memory/templates.md)
- [references/context-memory/index-template.md](references/context-memory/index-template.md)
- [references/context-memory/recovery-patterns.md](references/context-memory/recovery-patterns.md)
- [references/context-memory/project-stages-and-risk.md](references/context-memory/project-stages-and-risk.md)
- [references/context-memory/activation-packet-template.md](references/context-memory/activation-packet-template.md)
- [references/derived-memory-index.md](references/derived-memory-index.md)
- [references/large-text-source-intake.md](references/large-text-source-intake.md)
- [references/legacy-destination-manifest.md](references/legacy-destination-manifest.md)
- [references/legacy-source-import.md](references/legacy-source-import.md)
- [references/user-requirement-ledger.md](references/user-requirement-ledger.md)

Use the bundled memory workflow only through this skill.
Do not expose internal references as extra GitHub install paths, activation
targets, or fallback plans.

## Activation phrases

Primary phrase: `启用外挂记忆`.

Natural start phrase: `启动外挂记忆`.

Explicit safe phrase: `本会话启用外挂记忆`.

Legacy compatibility phrase: `启动lite demo`.

When the user uses any activation phrase, treat it as an activation command for the installed memory-only demo. Read [references/startup-protocol.md](references/startup-protocol.md). Do not ask the user to paste the longer setup prompt. If the message contains only an activation phrase, do not auto-resume old tasks or start services.

## Workflow

1. For fresh-machine install, read [references/install-new-machine.md](references/install-new-machine.md).
2. For short activation after install, read [references/startup-protocol.md](references/startup-protocol.md). On an existing memory root, use its startup choice gate before applying [references/automatic-legacy-takeover.md](references/automatic-legacy-takeover.md): explicit inheritance proceeds with takeover; an explicit fresh start keeps old memory cold and does not claim inheritance. The installed helper owns completion checks even when an old project AGENTS file still names an earlier version.
   If meaningful old history exists, takeover also uses
   [references/legacy-destination-manifest.md](references/legacy-destination-manifest.md)
   so legacy memory receives a reachable destination instead of becoming cold
   dead history.
   If the user names an old conversation, damaged conversation, old project,
   archive, or unknown legacy memory source, read
   [references/legacy-source-import.md](references/legacy-source-import.md)
   before creating or routing the current-session memory.
3. For a target project during full package installation, use the package-root
   script `scripts/install.ps1 -ProjectRoot <path> -WriteProjectAgents`.
   That script is not bundled inside the installed skill folder. When operating
   from an already installed or directly supplied skill folder, do not look for
   a non-bundled `install.ps1`; create the memory root through
   `scripts/takeover-memory.py initialize <memory-root>` and write only the
   project guidance/memory files that the current task explicitly allows.
4. Before creating a first memory root or routing a current conversation to an
   existing or new task memory, apply [references/memory-creation-and-task-branch-gate.md](references/memory-creation-and-task-branch-gate.md).
5. Before complex or compaction-sensitive execution, silently sniff once with [references/execution-policy-compatibility.md](references/execution-policy-compatibility.md). If another engineering protocol owns execution, keep Lite Demo's fallback off and use [references/task-anchor-gate.md](references/task-anchor-gate.md) only as its memory mirror.
6. Before converting user language into durable project rules, first apply
   [references/user-requirement-ledger.md](references/user-requirement-ledger.md)
   for explicit goals, prohibitions, acceptance criteria, and corrections.
   Then apply [references/memory-hygiene-nudge.md](references/memory-hygiene-nudge.md)
   only to the remaining ambiguous or weak notes.
7. During work, use the internal memory workflow references when writing `docs/codex/`, and keep durable state there, not in global AGENTS.
8. When the user points to a long local text source such as a novel,
   transcript, exported chat, or notes file and asks Lite Demo to understand or
   convert part of it into memory, read
   [references/large-text-source-intake.md](references/large-text-source-intake.md)
   before reading long bodies. Use the bundled source-slice helper so source
   bodies stay in artifacts while memory owners store interpretation, routes,
   and continuation guards.
9. When touching Chinese text, UTF-8 files, JSON, Markdown, YAML, TOML, or logs, apply [references/encoding-discipline.md](references/encoding-discipline.md).
10. After a meaningful run, user correction, repeated failure, or smoke test, use [references/run-audit-and-upgrade.md](references/run-audit-and-upgrade.md).
11. For validation, use [references/test-plan.md](references/test-plan.md).
    For a long session log, use the internal `scripts/read-session-log.py`
    helper or equivalent bounded tail/search/range reads; never read the full
    log by default. Use `scripts/route-memory.py` for layered owner resolution
    and `scripts/takeover-memory.py` for fresh-root initialization,
    non-destructive legacy checkpoints, and discharge/roll maintenance. For a
    brand-new memory root, run `takeover-memory.py initialize <memory-root>`
    before writing current-context, index, session-log, schema, task anchors,
    or capsules by hand. A root that has current files but no verified
    `.takeover-checkpoint` is incomplete and must be repaired or reported as a
    gap before claiming runtime success.
    Keep `session-log.md` an in-flight queue of unresolved/unhomed items, not a
    chronicle: after a structured entry has an exact settled route and owner, run
    `scripts/takeover-memory.py discharge <memory-root>` so homed entries move
    byte-preserved into `legacy/session-log-discharged.md`. As a safety bound,
    if the log grows past its line budget, run
    `scripts/takeover-memory.py roll <memory-root>` to move
    the oldest whole entries byte-preserved into
    `legacy/session-log-archive.md`. Neither helper touches the checkpoint or
    the legacy prefix it protects, so takeover verification keeps passing.
12. If the user asks who made this package, how to get updates, or how to contact the maker, read [references/author-and-source.md](references/author-and-source.md).
13. If the user asks to update or upgrade Lite Demo through the official server, read [references/update-from-server.md](references/update-from-server.md) and use the bundled updater script.

## Boundary

This package is memory-only. Read [references/modes.md](references/modes.md) when deciding what the demo should and should not claim.

Do not ask the user for secret credentials. Do not install or configure external execution tools. Do not add tiered executor/judge flows to this demo.
