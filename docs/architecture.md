# Architecture

## Two Repository Model

`codex-user-config` owns portable user configuration, the canonical capability
router, authorization boundaries, and restoration order. This repository owns
the reviewed Skill supply chain and its semantic relationships.

The runtime sequence is:

1. restore and verify the user-configuration baseline;
2. resolve the pinned Skills repository revision;
3. verify provenance, policy, hashes, and approval state;
4. materialize agent-neutral Skill cores into the supported Skill directory;
5. apply only the adapter required by the active agent environment;
6. rebuild the capability index and topology from governed registry data;
7. verify discovery, routing, conflicts, and representative workflows.

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
