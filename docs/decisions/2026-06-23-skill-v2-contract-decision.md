# Skill v2 Contract Decision

**Date:** 2026-06-23  
**Status:** Accepted for the current roadmap  
**Scope:** `agent-skills-curated` registry authority boundaries before any
manifest v2 or consumer integration work

## Decision

Decision: do not promote Skill v2 metadata into a new authoritative skills registry yet.

The current repository already has a factored governance model:

- `registry/skills.json` remains the schema-1 approved release inventory.
- `registry/routing.json` remains the authority for Skill routing metadata.
- `registry/capabilities.json` remains the authority for abstract lifecycle coverage.
- `registry/relations.json` remains the authority for topology edges.
- `registry/conflicts.json` remains the authority for conflict ownership and
  resolution.
- `registry/recipes.json` remains the authority for ordered capability
  composition.

No second Skill truth source is introduced in this batch. Rich Skill-level
metadata is governed through the existing registries rather than copied into a
parallel `skills` v2 document.

## Why

The release identity and installable payload boundary are already stable in
`registry/skills.json` schema 1 plus `release-manifest.json` schema 1. Routing,
semantic triggers, risk, permissions, validation, fallback, lifecycle mapping,
relations, conflicts, and recipes already have separate authorities.

Promoting all of that into a new `skills` v2 contract now would duplicate
facts, create migration pressure on downstream consumers, and increase the
chance that `skills`, `routing`, and `capabilities` drift apart.

## Current boundaries

- No manifest v2 publication.
- No consumer-side installer or runtime integration change.
- No new third-party Skills.
- No automatic discovery or approval.
- No copying of official, runtime-owned, built-in, or first-party Skill bodies.
- No treating external capability metadata as executable approval.

## Future promotion gate

A future Skill v2 contract may be introduced only after all of these are true:

1. A concrete consumer need cannot be met by the existing factored registries.
2. 5-8 representative Skills have complete candidate metadata fixtures.
3. The proposed fields are classified as one of:
   - release identity;
   - routing metadata;
   - lifecycle coverage;
   - topology relation;
   - conflict resolution;
   - recipe composition;
   - evidence reference;
   - consumer installation concern.
4. Fields already owned by `routing`, `capabilities`, `relations`,
   `conflicts`, or `recipes` are not copied into `skills`.
5. Any temporary `legacy-pending` state is narrowly scoped, tested, and
   prohibited for new or changed approved Skills.
6. The migration can be validated without publishing manifest v2.
7. Downstream consumer support is planned as a separate approved transaction.

## Consequence

The next safe implementation work should strengthen the current factored
contracts, projections, and simulations before changing the release or consumer
interface. A manifest v2 remains future work, not the next default step.
