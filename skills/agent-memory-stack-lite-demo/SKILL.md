---
name: agent-memory-stack-lite-demo
description: Install, update, and operate a memory-only Codex demo stack with project-local current-context, index, capsules, session logs, active-task anchors, automatic one-time takeover of pre-v0.2.6 project memory on first activation after upgrade, task-memory routing for unfinished or parallel conversations, execution-protocol compatibility, adaptive lite-anchor fallback, one-time passive activation suggestion, and memory-hygiene guards. Use when the user says "启用外挂记忆", "启动外挂记忆", "本会话启用外挂记忆", the legacy phrase "启动lite demo", asks to upgrade/update Lite Demo, opens an old Lite Demo project after upgrade, installs from a fresh-machine zip, sets up project docs/codex memory, preserves failed paths, routes parallel task memory, or proves compression/interruption recovery without external executors or extra credentials.
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

Before writing durable project rules, Lite Demo applies a memory-hygiene nudge:
one-off requests, pressure phrases, local failures, and short acknowledgements
stay weak or task-local by default unless the user uses explicit absolute
wording.

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
2. For short activation after install, read [references/startup-protocol.md](references/startup-protocol.md). On an existing memory root, also apply [references/automatic-legacy-takeover.md](references/automatic-legacy-takeover.md) once when v0.2.6 completion markers are absent.
3. For a target project, install project guidance with `scripts/install.ps1 -ProjectRoot <path> -WriteProjectAgents`.
4. Before creating a first memory root or routing a current conversation to an
   existing or new task memory, apply [references/memory-creation-and-task-branch-gate.md](references/memory-creation-and-task-branch-gate.md).
5. Before complex or compaction-sensitive execution, silently sniff once with [references/execution-policy-compatibility.md](references/execution-policy-compatibility.md). If another engineering protocol owns execution, keep Lite Demo's fallback off and use [references/task-anchor-gate.md](references/task-anchor-gate.md) only as its memory mirror.
6. Before converting ambiguous user language into durable project rules, apply [references/memory-hygiene-nudge.md](references/memory-hygiene-nudge.md).
7. During work, use the internal memory workflow references when writing `docs/codex/`, and keep durable state there, not in global AGENTS.
8. When touching Chinese text, UTF-8 files, JSON, Markdown, YAML, TOML, or logs, apply [references/encoding-discipline.md](references/encoding-discipline.md).
9. After a meaningful run, user correction, repeated failure, or smoke test, use [references/run-audit-and-upgrade.md](references/run-audit-and-upgrade.md).
10. For validation, use [references/test-plan.md](references/test-plan.md).
    For a long session log, use the internal `scripts/read-session-log.py`
    helper or equivalent bounded tail/search/range reads; never read the full
    log by default. Use `scripts/route-memory.py` for layered owner resolution
    and `scripts/takeover-memory.py` for a non-destructive legacy checkpoint.
11. If the user asks who made this package, how to get updates, or how to contact the maker, read [references/author-and-source.md](references/author-and-source.md).
12. If the user asks to update or upgrade Lite Demo through the official server, read [references/update-from-server.md](references/update-from-server.md) and use the bundled updater script.

## Boundary

This package is memory-only. Read [references/modes.md](references/modes.md) when deciding what the demo should and should not claim.

Do not ask the user for secret credentials. Do not install or configure external execution tools. Do not add tiered executor/judge flows to this demo.
