# Architecture

## Two Repository Model

`codex-user-config` owns portable user configuration, the canonical capability
router, authorization boundaries, and restoration order. This repository owns
the reviewed Skill supply chain and its semantic relationships.

The repositories have a one-way producer-consumer relationship. This
repository produces reviewed content and deterministic release evidence; it
does not install, does not write to `codex-user-config`, and does not write to a
live Agent environment. The configuration repository pins a reviewed revision,
then plans, backs up, installs, verifies, and rolls back managed Skill paths.

The consumer-owned runtime sequence is:

1. restore and verify the user-configuration baseline;
2. resolve the pinned Skills repository revision;
3. verify provenance, policy, hashes, and approval state;
4. materialize agent-neutral Skill cores into the supported Skill directory;
5. apply only the adapter required by the active agent environment;
6. rebuild the capability index and topology from governed registry data;
7. verify discovery, routing, conflicts, and representative workflows.

Steps 1-7 describe consumer behavior, not executable responsibilities of this
repository.

## Capability Layers And Decisions

The curated authority governs third-party Skill bodies and an abstract,
product-neutral capability taxonomy. Official, runtime-owned, built-in, and
first-party Skill bodies remain outside its governed and managed inventory.
They may be consulted only as dated overlap evidence; such evidence does not
transfer ownership, assert canonical identity, or prove current runtime
availability. Their bodies must not be vendored or enter the release manifest.

A third-party candidate remains in source, intake, selection, and audit
surfaces until it has passed source pinning, license, provenance, security,
portability, overlap, adaptation, and validation review. Before approval it
must not enter an execution path. Only a curated approved Skill with
`status=approved` may enter `skills/` and the schema-1 manifest;
`registry/skills.json` is the approved release inventory.

The configuration-owned `capability-router` is a capability decision router.
It may select native reasoning, an official or runtime-owned capability, a
curated Skill, external capability metadata, a recipe or DAG, human
confirmation, or no skill needed. Candidate content is not a routing target.
High-risk, ambiguous, conflicting, permission-changing, write, install,
delete, migration, publish, release, or rollback decisions require human
confirmation.

## Dynamic Capability Topology

Git-tracked JSON is the initial authority. A graph database or visualization
may consume generated projections later, but must not become a second manual
source of truth.

Nodes may represent Skills, capabilities, artifacts, lifecycle phases,
conditions, tools, adapters, policies, risks, and evidence. Typed edges express
ordering, data flow, collaboration, alternatives, fallbacks, conflicts, and
replacement. Recipes represent multi-node conditional workflows where a simple
pairwise edge is insufficient.

Stable IDs survive renames. Every inventory change must regenerate derived
indexes and report impacted routes, unresolved references, cycles where cycles
are forbidden, and newly introduced conflicts.

## Portability Boundary

The portable core describes goals, inputs, outputs, invariants, decisions, and
verification. Adapters translate only unavoidable environment details such as
tool names, hook event shapes, filesystem conventions, and agent-specific
invocation syntax.

Portability does not erase legitimate capability differences. Unsupported
operations must degrade explicitly instead of being simulated or silently
claimed.
