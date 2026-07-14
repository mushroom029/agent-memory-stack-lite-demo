# Agent Memory Stack Lite Demo for Hermes

Version: `hermes-lite-demo v0.1.0`

作者署名：蘑菇｜抖音名：OCD强迫者｜抖音号：38439195984｜QQ：327031882

This branch is the Hermes adaptation track for Agent Memory Stack Lite Demo.
It is separate from the Codex release track.

## What It Does

Hermes keeps its own memory. Lite Demo keeps project-local route memory.

Use this skill when you want Hermes to remember, inside the project folder:

- current task goal;
- failed paths and user corrections;
- user pressure as a light boundary;
- stable modules that should not be touched casually;
- unfinished task routing;
- the next exact step after interruption or context loss.

It does not replace Hermes memory, does not add an executor, and does not
promise that every task succeeds.

## Install

Preferred GitHub branch install text must be verified on a real Hermes profile
before public release.

Expected branch path:

```text
mushroom029/agent-memory-stack-lite-demo/skills/hermes-lite-demo
```

Expected branch name:

```text
hermes-lite-demo
```

If Hermes supports raw `SKILL.md` URL installs, the branch raw URL should be:

```text
https://raw.githubusercontent.com/mushroom029/agent-memory-stack-lite-demo/hermes-lite-demo/skills/hermes-lite-demo/SKILL.md
```

## Activate

In a project conversation:

```text
/hermes-lite-demo 启用外挂记忆
```

Natural follow-up phrase:

```text
启用外挂记忆
```

Legacy compatibility phrase:

```text
启动lite demo
```

## Update

Use Hermes' native skill update flow after install. Do not use the Codex zip
updater for this Hermes branch.

The exact public update wording must be verified with Hermes CLI before release.
