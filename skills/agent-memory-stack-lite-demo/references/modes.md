# Lite Demo Boundary

This package has one mode: memory-only demo.

Use it when the user wants to feel whether external project memory changes Codex behavior on real work.

It may help with:

- long tasks that compress;
- first-time memory setup that should ask before writing;
- new complex task lines that need same-root task branch anchors;
- coexistence with an existing execution protocol by recording its route instead of competing with it;
- interrupted tasks that need resuming;
- repeated mistakes that should become rejected paths;
- project-specific pressure signals and stability rules;
- stable-module protection when a feature is already working;
- remembering the next exact step after validation or errors.

It does not add:

- external executors;
- alternate model setup;
- account or credential onboarding;
- a separate reviewer role;
- a duplicate planning, testing, debugging, deployment, or verification protocol when one already exists;
- runtime telemetry or a log of available/tool-only skills;
- guaranteed task success.

Good demo tasks are scoped and real:

- fix a small bug;
- organize an existing project folder;
- continue a multi-step document or code task;
- repeat a task once without memory and once with memory;
- intentionally pause or resume after an anchor is created.

Bad demo tasks are vague or theatrical:

- "solve all my AI problems";
- "make every task succeed";
- "prove the model is always smarter";
- "run a giant open-ended refactor."

The demo should show a concrete behavioral change: Codex should preserve the route, avoid known failed paths, and recover from interruption with less user re-explanation.

When no explicit execution protocol exists, Lite Demo may use its adaptive lite-anchor fallback. When an explicit execution protocol or model-native workflow already owns execution, Lite Demo should stay memory-only and record that protocol's goals, failed paths, validation results, stable-module boundaries, and next step.
