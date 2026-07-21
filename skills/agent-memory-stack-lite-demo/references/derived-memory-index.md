# Derived Memory Index

This is the v0.2.17 development contract for Lite-native local-history recall.

The derived index is not a second memory store. Markdown owners, project files
explicitly pointed to by owners, legacy evidence, and task anchors remain the
source of truth. The cache only stores source identities, stable record
pointers, hashes, bounded derived terms, and query metadata.

## Storage And Retrieval Separation

- Truth stays in memory owners and source files.
- Derived cache lives under `.lite-demo-cache/v1/` and is disposable.
- Query returns record IDs, owner/source pointers, line ranges, scores, reasons,
  hashes, and continuation state. It does not return narrative bodies as the
  authoritative memory.
- A stale, missing, partial, or foreign cache must be rebuilt or rejected before
  action. It must not silently answer `no-memory`.

## Build Command

```bash
python scripts/compile-memory.py build <memory-root>
```

The build command:

- inventories source entries under the selected memory root;
- excludes `.lite-demo-cache/`, `.lite-demo-work/`, and `legacy/receipts/` from
  the authoritative source hash to avoid self-reference;
- extracts structural records from Markdown/text owners, routes, headings, and
  structured in-flight entries;
- records source SHA256 and span SHA256;
- writes a deterministic cache so a second unchanged build is a no-op.

## Query Command

```bash
python scripts/compile-memory.py query <memory-root> --query "<text>"
```

The query command:

- refuses stale caches before ranking;
- uses exact identity, aliases, keywords, normalized lexical terms, path terms,
  and CJK n-grams;
- is the required fallback when `route-memory.py` has no strong match or only
  weak candidates for a natural-language continuation. A miss in the handwritten
  route vocabulary is not proof that no local history exists until this pointer
  cache has been queried and any returned mandatory owner pointers have been
  opened.
- returns mandatory guard records outside the ordinary ranking window;
- pages ordinary records with a continuation token bound to query hash, page
  size, and source inventory hash;
- rejects stale continuation tokens after source changes;
- excludes live `session-log.md` body records and
  `legacy/session-log-*` archive/discharge bodies from ordinary recall. Only
  structured in-flight entries may be returned, and only when the caller asks
  for in-flight entries or queries the exact entry ID. Old log bytes stay
  evidence; route owners and legacy destinations carry recall.
- supports Lite-native filters such as `--channel`, `--memory-class`,
  `--status`, and `--source-prefix`. Filters narrow pointer selection only;
  they must not create a second memory taxonomy outside the Markdown owner
  metadata and routes.
- binds continuation tokens to query, page size, source inventory, and filters
  so a caller cannot reuse an old page token after changing the retrieval scope.

## Recall And Related Commands

```bash
python scripts/compile-memory.py recall <memory-root> --topic "<topic>" --topic "<topic>" --include-anchors
python scripts/compile-memory.py related <memory-root> --record-id "<record-id>"
```

The recall command is the Lite-native counterpart to a multi-topic startup
recall: it queries several topics, returns unique pointer records, and may add
current anchor pointers (`current-context.md`, `active-task.md`, `index.md`).
It still returns pointers, hashes, line ranges, and reasons rather than memory
bodies.

The related command is a bounded lexical neighbor helper. It can find records
that share aliases, keywords, path terms, scope terms, or CJK n-grams. It is
not vector search and must not be presented as semantic equivalence to
`agent-memory-mcp`.

## Layer Quality Command

```bash
python scripts/scan-layer-quality.py <memory-root> --require-derived-cache
```

Use this during pressure tests to verify that models actually used the five
layers correctly:

- live anchors stay compact and do not accumulate chronology;
- route files remain compact owner routers;
- durable bodies have one reachable owner and are not copied across layers;
- `session-log.md` remains a sparse in-flight queue;
- derived cache stores bounded metadata and pointers, not narrative bodies or
  legacy log text.

## Boundaries

- Do not add MCP, LanceDB, ONNX, embeddings, model downloads, daemon processes,
  random UUID truth identity, temporal decay, automatic prune/delete, or an
  external database.
- Do not copy `agent-memory-mcp` source, schema, wording, tests, or runtime.
- Do not package, install, publish, or claim v0.2.17 completion from this slice
  alone.
- Later phases still need complete legacy-source coverage, semantic destination
  decisions, crash-safe apply/discharge, activation integration, and independent
  old-root evidence before a release candidate exists.
