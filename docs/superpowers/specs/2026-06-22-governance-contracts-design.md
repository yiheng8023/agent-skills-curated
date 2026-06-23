# Agent Skills Governance Contracts Design

**Date:** 2026-06-22
**Status:** Current roadmap after Batch A closeout
**Scope:** `agent-skills-curated` governance contracts and the future one-way
consumer interface with `codex-user-config`

## Current Implementation State

Batch A is complete. The checked-in repository now validates strict
frontmatter parsing, dynamic inventory counts, schema contracts, cross-registry
references, manifest payload boundaries, deterministic generated projections,
and the schema-1 release surface.

The lifecycle-routing baseline has also advanced beyond the original Batch B
sketch: `registry/capabilities.json` is schema 2, `registry/routing.json`
contains approved semantic routing metadata, and `registry/scenarios.json`
contains the 96-case normalized policy corpus. `registry/skills.json` remains
schema 1 and continues to serve as the approved release inventory for the
schema-1 manifest and current consumers.

The manifest v2 has not been published. The next bounded task is not a
manifest upgrade; it is to decide whether Skill-level v2 metadata should be
promoted into a new authoritative `skills` contract or remain factored through
the existing `skills` plus `routing`, `capabilities`, `relations`, `conflicts`,
and `recipes` registries. Any manifest v2 or consumer integration work remains
a later cross-repository transaction.

Current state markers:

- `registry/skills.json` remains schema 1.
- The manifest v2 has not been published.
- The next bounded task is not a manifest upgrade.

## 1. Goal

Evolve the first release from a fixed, verified Skill payload into a durable
governance system without breaking the already-pinned installer contract.

The design must preserve these boundaries:

```text
agent-skills-curated
  owns Skill content, source intake, governance registries, review evidence,
  deterministic projections, and immutable releases

codex-user-config
  owns source pinning, installation, runtime adapters, backup, verification,
  rollback, and live routing integration
```

The curated repository never writes to the configuration repository or a live
Agent environment. A routing projection may describe candidates and policy but
cannot grant authorization or execute actions.

## 2. Approaches Considered

### A. Big-bang v2 across both repositories

Change registries, release manifest, installer, transaction format, and runtime
routing in one release.

Rejected because it couples two repositories, makes rollback difficult, and
would temporarily publish a manifest the current consumer cannot understand.

### B. Compatibility-first staged contracts — recommended

1. Harden the current curated v1 contract without changing its external
   installation interface.
2. Design and validate registry v2 using representative metadata while the
   release manifest remains v1.
3. Add v1+v2 support to `codex-user-config` in a separate approved transaction.
4. Publish release manifest v2, governance attestation, and a versioned routing
   projection from the curated repository.
5. Pin that v2 release from the configuration repository only after integration
   tests pass.

This preserves the current release, gives every batch an independent acceptance
gate, and keeps cross-repository changes consumer-first.

### C. Parallel overlay metadata

Keep current registries unchanged and add a second metadata index for routing.

Rejected because it creates two manually maintained truth sources and makes
drift inevitable.

## 3. Contract Ownership

Each fact has one authority:

| Contract | Owns | Must not own |
|---|---|---|
| `skills` | Stable identity, lifecycle, source reference, routing profile, risk and evidence references | Topology edges, install paths, live authorization |
| `capabilities` | Capability definition, scope and canonical owner | Per-Skill duplicate trigger text |
| `relations` | Typed edges between governed nodes | Duplicated owner or fallback fields in Skills |
| `conflicts` | Machine-readable default owner, member disposition and scope rule | Free-text-only decisions |
| `recipes` | Conditional execution DAG, gates and failure policy | Permission grants or live execution |
| `sources` | Immutable origin, revision, license and provenance state | Runtime approval for selected Skill adaptations |
| release manifest | Installable payload identity and file integrity | Backup or live rollback implementation |
| governance attestation | Evidence that a manifest passed declared reviews | Installable Skill files |
| routing projection | Versioned, deterministic runtime advisory data | Secrets, absolute paths, live state or authorization decisions |

Generated files are disposable projections. A graph database, if ever added,
is also a rebuildable projection and never an authoring surface.

## 4. Batch A — Current Contract Hardening

**State:** complete.

Batch A changes only `agent-skills-curated` and keeps release manifest schema 1
compatible with the current `codex-user-config` installer.

### Deliverables

1. Add isolated tests around the public verification and generation behavior.
2. Replace the permissive line parser with a strict frontmatter parser that:
   - supports plain, quoted, folded (`>`) and literal (`|`) scalar values;
   - rejects duplicate keys, unsupported complex YAML, malformed indentation,
     tags, anchors and aliases;
   - correctly parses the full `caveman` description.
3. Remove fixed inventory assumptions (`34`, `60`, `24`, `5`). Counts become
   derived invariants; source selection closure comes from governed source and
   disposition data.
4. Add formal schema contracts for the current governed documents and stable,
   pointer-based validation errors.
5. Validate unique IDs, directories and names; internal references; capability
   owners; conflict owners/members; recipe capability references; and relation
   endpoint semantics.
6. Validate manifest path normalization, duplicate and case collisions, digest
   shape, exact payload coverage, and the absence of symlinks/reparse points.
7. Add the missing `local:reviewed-baseline` source record with explicitly
   incomplete provenance rather than inventing attribution.
8. Preserve and test that `generated/` is deterministic, read-only under
   `--check`, and derived only from governed registries.

### Dependency decision

Batch A uses a deliberately strict repository frontmatter subset rather than a
general YAML execution surface. It supports every scalar form used by the
curated inventory and fails closed on unsupported YAML features. This avoids
adding an unreviewed parser dependency merely to read three metadata fields.

Governed JSON validation uses explicit repository validators plus checked-in
schema documents. Adding a general JSON Schema engine remains a separate
supply-chain decision; the contracts must not silently depend on packages that
CI has not pinned and reviewed.

### Acceptance

- The `caveman` regression test first fails with `>` and then passes with its
  complete folded description.
- A valid fixture with a different Skill/file/source selection count passes.
- Invalid types, enums and unknown fields fail with a file and JSON pointer.
- Internal references resolve; external/upstream references use an allowed
  namespace.
- Recipe dependencies are valid and acyclic when DAG fields are introduced.
- Manifest traversal, duplicate, case-collision, malformed digest and link
  fixtures fail closed.
- `--check` changes no repository bytes or mtimes.
- The existing schema-1 release remains installable by the current consumer.

## 5. Batch B — Registry v2 and Routing Samples

**State:** partially absorbed by the current lifecycle-routing baseline.

After Batch A is green, define registry schema version 2. Do not require
legacy Skills to claim evidence they do not yet have. The current repository
has already adopted schema 2 for abstract capabilities and keeps Skill release
identity in `registry/skills.json` schema 1. Rich routing metadata currently
lives in `registry/routing.json` to avoid creating a second Skill truth source.

### Minimum Skill v2 metadata

- stable identity: `id`, `directory`, `entrypoint`, `name`;
- localized aliases;
- lifecycle object and optional lifecycle stages;
- immutable `sourceRef`;
- routing profile with positive examples, negative examples and context
  requirements;
- risk profile with level, permission classes, side-effect classes and
  conditional confirmation rules;
- compatibility profile references;
- validation and evidence references.

Inputs/outputs, numeric confidence thresholds, embeddings, filesystem mappings,
cost models and exhaustive Agent matrices are deferred.

If a future Skill v2 contract is introduced, select 5-8 representative Skills
for full metadata first. Legacy entries must use an explicit, narrowly scoped
`legacy-pending` assessment state; new or changed approved Skills cannot use
that exception.

Relations remain the only topology-edge authority. Fallbacks, capability maps
and conflict membership are not copied into each Skill.

## 6. Batch C — Capability Graph and Lifecycle Recipes

**State:** partially implemented for lifecycle coverage and routing policy.

Extend capabilities with scope and ownership, relations with stable IDs and
conditions, conflicts with machine-readable dispositions, and recipes with
step IDs, `dependsOn`, optional branches, evidence gates, authorization gates,
failure policy and terminal criteria.

The global capability graph may contain feedback loops. A concrete recipe run
must resolve to a DAG.

Build a lifecycle capability map, not one mandatory mega-pipeline. Initial
priority gaps are requirements/RFC, data modeling, test strategy, documentation
governance and post-incident learning. Security, privacy, live deployment and
rollback execution remain external authorities.

The current baseline classifies all 26 software-engineering lifecycle
capabilities and leaves no unclassified lifecycle gap. Some capabilities are
intentionally `recipe`, `runtime-resolved`, `native-sufficient`, or
`human-authority` rather than curated Skill bodies.

## 7. Batch D — Cross-Repository Release v2

**State:** future work requiring separate approval.

This batch requires a separate user approval because it changes
`codex-user-config`.

Order is mandatory:

```text
config consumer supports manifest v1 + v2 while still pinned to v1
→ curated publishes manifest v2 + attestation + routing projection
→ config pins exact commit and manifest/attestation digests
→ cross-platform install, reinstall, failure and rollback tests pass
```

Manifest v2 contains release identity, stable Skill IDs, entrypoints, exact
allowlisted files, executable semantics and projection digests. It does not
implement rollback.

The governance attestation binds the manifest digest to source locks,
registries, policies, audits, checks and human approval. A plain
`state: approved` field is not sufficient evidence.

The routing projection is static advisory data. `capability-router` remains in
`codex-user-config`; it decides whether and how to consume the projection.

## 8. Error and Safety Model

- Unknown schema or feature fails closed.
- Validation errors identify document, JSON pointer and violated rule.
- Upstream and generated data never authorize external effects.
- New source, executable, dependency, trust boundary or license uncertainty
  requires explicit review.
- Curated scripts may validate or generate repository artifacts only; they may
  not install, fetch, authenticate or mutate live state.
- Every cross-repository interface change is a separate bounded transaction.

## 9. Test Strategy

Use vertical TDD slices:

1. folded frontmatter regression;
2. dynamic inventory and selection counts;
3. schema and diagnostic foundation;
4. cross-reference and graph semantics;
5. manifest supply-chain boundary;
6. deterministic generated projections.

Tests create malformed or expanded repositories only in temporary directories.
They must not mutate the working repository or access the network.

## 10. Explicit Non-Goals

- No new third-party Skills.
- No live installation or Router integration.
- No manifest v2 publication before consumer support.
- No automatic source discovery or approval.
- No vector database, graph database or embeddings.
- No numeric routing thresholds without a labeled scenario corpus.
- No signature/SLSA framework in the first batches.
- No claim that the release manifest alone can restore replaced local content.

## 11. Completion Criteria

The design is complete when each batch has a bounded contract, a failing test
before implementation, deterministic outputs, no unresolved internal
references, and no violation of the two-repository authority boundary.
