# Context Index

Use this as the navigation file for durable context.

```md
# Context Index

- Updated:
- Project:
- Current anchor:
- Memory landing policy: ask-by-default | preauthorized
- Task branches:
- Active version:
- Active topic:
- Project phase:
- Module aliases:
  - <canonical-module>: <alias>, <alias>, <alias>
- Module index:
  - <module>: phase=<mode>; stable=<Stable behavior>; pressure=status=<active|historical|resolved>, severity=<low|medium|high>, signal=<Pressure signals>; rejected=<Rejected approaches>; guards=<Regression guards>; capsules=<ids>
- Capsules:
  - C13: <short label>
  - C14: <short label>
- Session log:
- Evidence store:
```

Keep this file narrow. It should expose enough keywords for activation-packet
selection without mirroring full history. Use canonical module names plus aliases
so related pressure signals are not missed. If a task touches a named module or
alias, scan that module's phase, stable behavior, pressure, rejected approach,
and guard entries before deciding which capsules to open.

Use these canonical concepts across memory files:

- `Stable behavior`
- `Pressure signals`
- `Rejected approaches`
- `Regression guards`

If a project already has separate focused views such as `Stable behavior index`
or `Pressure signal index`, keep them only as compatibility views. The module
line remains the primary navigation record and should not contradict them.
