# Legacy Destination Manifest

Use this during automatic legacy takeover or legacy-source import when an
existing or referenced memory source has meaningful old history. The goal is
not to load old logs by default. The goal is to prove that old memory still has
a reachable home after the upgrade.

Create `legacy-destinations.md` in the memory root before takeover completion
when the legacy session-log prefix, old active task, old index, or old capsules
contain meaningful history. The file must start with a schema field such as
`- Legacy destination schema: v0.2.17`.

For cross-conversation or damaged-conversation import, create the same manifest
for the current target root or a clearly named import subfile before claiming
that the referenced source was inherited.

This file is a routing and audit manifest. It is not a second memory store, not
a chronology, and not a project-type template.

A standalone `skills/context-memory-index` found during install is also legacy
memory history, but it is not a project memory root. The installer must move it
out of active `skills/` non-destructively and write archive metadata plus a
destination manifest inside the archive. Known old public copies are
`archived-only` because the current Lite Demo skill already internalizes that
workflow. Unknown or modified copies are `pending-review` because they may
contain user-custom rules that must not be silently discarded or automatically
merged into the public skill.

Known old project memory versions include recommended and published Lite Demo
roots such as v0.1.7 stable fallback, v0.1.8, v0.1.9, v0.2.0 suffix variants,
v0.2.1 and later. Unknown layouts remain legacy sources; they do not disappear
because the version cannot be identified.

## Destination Statuses

Every meaningful legacy item receives exactly one status:

- `memory-owner`: the body was promoted into a current Lite Demo owner such as
  a capsule, active task, or current context body.
- `mandatory-guard`: the body is a touched-scope guard that must wake before
  relevant work, such as an explicit prohibition, stable behavior, acceptance
  criterion, unresolved conflict, or irreversible-action guard.
- `rejected-path`: the body is negative evidence that prevents an old failed
  approach from being revived.
- `project-owner-indexed`: the body belongs to a real project owner outside the
  memory layer, such as source code, tests, reports, datasets, generated
  outputs, logs, design files, configuration, or local project documentation.
  Lite Demo stores only the route, owner pointer, and wake-up terms.
- `archived-only`: the entry has evidence value but should not wake by default.
  This status requires a reason.
- `pending-review`: the value or owner is uncertain. Do not mark takeover
  complete by silently treating it as archived.

These statuses are domain-neutral. Do not add statuses for a specific user
project type.

Direct user goals, prohibitions, acceptance criteria, and corrections should
normally become `memory-owner`, `mandatory-guard`, `rejected-path`, or
`pending-review` with a requirement owner. They should not be reduced to
pressure-only notes.

## Entry Shape

Use compact route-like entries:

```text
# Legacy Destinations

- Legacy destination schema: v0.2.17

- LD001: status=memory-owner; source=session-log.md#L10; scope=payment; aliases=checkout,billing; keywords=refund guard; owners=capsules/C01.md; mandatory=none; probes=route-memory:checkout refund; reason=live payment guard
- LD002: status=project-owner-indexed; source=active-task.md#old-step; scope=build; aliases=installer; keywords=package smoke; owners=../../scripts/test-install.ps1; mandatory=none; probes=route-memory:installer smoke; reason=real owner is the project test
- LD003: status=archived-only; source=session-log.md#L80-L94; scope=old event; aliases=none; keywords=none; owners=none; mandatory=none; probes=none; reason=obsolete duplicate evidence, preserved in immutable log only
- LD004: status=pending-review; source=session-log.md#[REVIEW:R1]; scope=ambiguous rule; aliases=ambiguous rule; keywords=review; owners=session-log.md#REVIEW:R1; mandatory=none; probes=none; reason=owner conflict needs future judgment
```

Required fields:

- `status`
- `source`
- `scope`
- `reason`

Statuses that wake memory also require:

- `aliases` or `keywords`
- `owners`
- `probes`

Wake-up terms must be semantic. Generic terms such as `legacy source`,
`legacy capsule`, `import evidence`, `capsule owner`, `legacy index`, or a
source-file scope like `capsules-C01` do not prove recall. If many old files
only contain duplicate cold evidence, group them as `archived-only` with a
reason or create one semantic entry for the meaningful function they support.
Do not create one destination per file number just to make a complete-looking
manifest.

`route-memory.py` treats non-`archived-only` destination entries as a compact
supplemental route source. This makes old-user inheritance wake from the
semantic destination proof without default-loading the old session log or
legacy archives. If a destination entry has `probes=route-memory:<phrase>`,
that phrase must resolve to the entry owner through `route-memory.py` or an
equivalent owner-resolution check.

`project-owner-indexed` is for real project owners outside the memory layer
(code, tests, reports, datasets, generated outputs, logs, design files,
configuration, or local project documentation). If the owner is a current
memory file such as `capsules/C01.md`, choose `memory-owner`,
`mandatory-guard`, or `rejected-path` instead.

`archived-only` does not require an owner or probe, but it must not be a
catch-all for unexamined old history.

A user-chosen v0.2.17 fresh start is the only exception to the catch-all rule.
In that case, write one explicit fresh-start decision entry with
`status=archived-only`, `source=<old memory root>`, semantic `scope`, and a
reason saying the user chose not to inherit old memory now. This entry means
"old memory is preserved and cold"; it must not be described as successful
inheritance. A later explicit inherit request must inventory the preserved
source with normal per-item destinations before claiming import.

## Takeover Completion Rule

Schema and checkpoint proof are not enough when old history is meaningful.
Completion requires:

1. old memory surfaces were inventoried by their prior version shape and
   current file layout;
2. every meaningful legacy item has a destination entry;
3. every non-archived destination has a current owner or project owner pointer;
4. every wakeable destination has aliases or keywords;
5. representative ordinary-language probes have been run with
   `route-memory.py` or an equivalent exact owner-resolution check;
6. unresolved ownership is recorded as `pending-review`;
7. `check-memory-root.py --strict-routing --allow-missing-schema` passes before
   `takeover-memory.py apply` writes the completion proof.

`pending-review` is not completion for the scope it affects. It is an honest
blocker or future-review owner, not a trash bin.

If the manifest cannot be completed safely, preserve the old memory and report
that takeover is incomplete. Do not write completion markers.

## What Not To Do

- Do not copy the full legacy log into a capsule.
- Do not mark a meaningful item `archived-only` merely because it is old.
- Do not treat a user-chosen fresh start as inherited old memory; it is only a
  cold preservation decision.
- Do not mechanically list every old capsule, route, or active-task file with
  generic aliases and the same catch-all owner.
- Do not make project-specific statuses or hardcoded domain rules.
- Do not treat owner existence as enough; the owner must have wake-up terms.
- Do not declare cross-conversation import complete when the referenced source
  was only linked, copied, or archived without destination entries.
- Do not treat route probes as a top-k search. All touched-scope mandatory
  guards must wake.
