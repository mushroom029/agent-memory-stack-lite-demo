# Activation Packet Template

Use this short packet after resume, compaction, model switch, or before a risky
task. It is the context that should enter the live thread, not the whole history.

```md
# Activation Packet

- Updated:
- Project:
- Phase/mode:
- Current task:
- Touched modules:
- Memory landing policy:
- Task branch:
- Selected index entries:
- Selected body owners:
- Mandatory guard owners:
- Targeted unresolved/evidence read:
- Surprise non-matches:
- Wider-retrieval reason:
- Stable behavior:
- 稳定模块保护判断:
- Pressure signals:
- Historical pressure still blocking resurrection:
- Rejected approaches:
- Allowed changes:
- Forbidden opportunistic changes:
- Regression guards:
- Conflict priority check:
- Next exact step:
```

Rules:

- Read `active-task.md`, `current-context.md`, and `index.md` before selecting memories.
- If a touched scope or alias appears in `index.md`, open every matching owner
  and every mandatory guard owner before claiming no relevant memory exists.
- A route miss, alias ambiguity, source conflict, first-time entity touch, or
  irreversible action requires wider retrieval. Record the reason rather than
  treating the first miss as proof of absence.
- Read `session-log.md` only for an exact unresolved route, source conflict, or
  remaining evidence gap; record the selected ID/range, not a default tail.
- Keep the packet short. Link capsules and logs instead of copying them.
- Include `Surprise non-matches` only when an index entry matched a touched
  module or alias but was judged irrelevant after inspection. Do not enumerate
  every capsule or memory that was skipped.
