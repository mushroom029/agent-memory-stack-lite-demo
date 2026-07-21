# User Requirement Ledger

Use this before classifying a user's explicit instruction as memory hygiene,
pressure, taste, or a weak preference.

## Core Rule

Explicit user goals, prohibitions, acceptance criteria, and corrections are
requirements by default. They do not become soft merely because the user is
angry, tired, terse, repetitive, or uses different wording across turns.

Memory hygiene still protects against overfitting one-off ambiguous language.
It does not override a clear instruction. If the user says not to do a thing,
do not do it. If the scope is unclear, record `pending-review` or stop for a
focused clarification instead of downgrading it to pressure.

If the user explicitly corrects the same behavior twice, or expresses strong
frustration after a previously recorded correction was ignored, create or
update a `mandatory-guard` or `correction-guard` immediately. Do not stop at
an apology or pressure note.

## Requirement Shapes

When a requirement must survive compression or future work, give it one owner
and one route:

```text
- RQ001: status=requirement-owner; source=<where user said it>; scope=<task/project/module>; instruction=<minimal exact meaning>; aliases=<wake terms>; owners=<capsule/active-task/project doc>; mandatory=<guards>; conflict=none; review=none
- RQ002: status=forbidden-action; source=<where user said it>; scope=<scope>; instruction=<what must not happen>; aliases=<wake terms>; owners=<owner>; mandatory=<owner>; conflict=none; review=none
- RQ003: status=acceptance-gate; source=<where user said it>; scope=<scope>; instruction=<what must be true before claiming done>; aliases=<wake terms>; owners=<owner>; mandatory=<owner>; conflict=none; review=none
- RQ004: status=correction-guard; source=<where user corrected Codex>; scope=<scope>; instruction=<corrected route>; aliases=<wake terms>; owners=<owner>; mandatory=<owner>; conflict=none; review=none
- RQ005: status=pending-review; source=<where ambiguity appears>; scope=<scope>; instruction=<uncertain meaning>; aliases=<wake terms if any>; owners=session-log.md#REVIEW:<id>; mandatory=none; conflict=<if any>; review=<question/blocker>
```

Use ordinary owner files; do not create a second database. The ledger entry can
live inside `active-task.md`, a capsule, `legacy-destinations.md`, or a
`[REVIEW]` session-log entry while uncertain.

## Conflict Gate

If a new target conflicts with an existing explicit user requirement or
prohibition, state the conflict before acting and offer exactly these paths in
plain language:

```text
A. Keep the existing instruction and adjust the current target.
B. Use a temporary scoped override only for this creation/process.
C. Ask the user to complete or replace the command.
```

Do not silently choose B. A scoped override must say what old instruction is
being suspended, for which current action, and when it expires.

## What Not To Do

- Do not treat repeated corrections as weaker because the wording changes.
- Do not require magic phrases such as "forever" before honoring a direct
  current-task prohibition.
- Do not convert user frustration into a reason to ignore the requested target.
- Do not mark a clear requirement `archived-only`.
- Do not claim completion while a requirement entry is `pending-review` and the
  unresolved point affects the work being claimed complete.
