# Context Index

Use this as the navigation file for durable context.

```md
# Context Index

- Updated:
- Project:
- Memory schema: v0.2.7
- Current anchor:
- Memory landing policy: ask-by-default | preauthorized
- Task branches:
- Active version:
- Active topic:
- Project phase:
- Module aliases:
  - <canonical-module>: <alias>, <alias>, <alias>
- Module index:
  - <scope>: aliases=<user and code terms>; keywords=<strong terms>; owners=<current body paths>; mandatory=<current guard paths or none>; history=routes/<scope>-history.md or none; reason=<one short routing reason>
- Pending review:
  - <review-id>: aliases=<terms>; keywords=<terms>; owners=session-log.md#REVIEW:<review-id>; mandatory=none; history=none; status=pending-review; reason=owner not settled yet
- Capsules:
  - C13: <short label>
  - C14: <short label>
- Session log:
- Evidence store:
```

Keep this file narrow. It is the owner router, not a second memory store or an
independent owner manifest. Use canonical scope names, strong-relevance
keywords, aliases, owner pointers, mandatory guard pointers, and one short
reason. Keep current normative owners and all live guards at the top level. If
older versions or events would make one route fan out broadly, point `history=`
to one route page under `routes/`; that page uses the same grammar with precise
version/event aliases. Follow every actually matched owner; do not apply a
top-k cutoff.

One durable fact has one normative body owner. Other layers may keep its short
ID, provenance, owner pointer, and one routing reason, but not another copy of
the body. A durable write is incomplete until its owner route exists.

Use these canonical concepts across memory files:

- `Stable behavior`
- `Pressure signals`
- `Rejected approaches`
- `Regression guards`

Move explanations and evidence into capsules or domain-owned files. Admit only
unresolved failures/conflicts/rollbacks, unpromoted corrections, provisional
`[REVIEW]` bodies, and sparse checkpoints to `session-log.md`. Size warnings
are maintenance signals, not hard limits on task-relevant owners.
