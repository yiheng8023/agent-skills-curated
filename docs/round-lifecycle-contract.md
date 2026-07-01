# Round Lifecycle Contract

This repository expands through bounded rounds, not through one large import.
Every round must have four explicit phases:

1. Plan.
2. Execute.
3. Acceptance.
4. Stage closeout.

The machine-readable contract lives in
`registry/round-lifecycle-contract.json`. The active round list lives in
`registry/curation-expansion-rounds.json`.

## Why This Exists

The repository is a curated authority, not a dump of useful Skill folders. Good
source discovery is only the first step. A candidate still needs license,
provenance, security, portability, overlap, adaptation, validation, and release
review before it can become approved payload.

This contract keeps the work iterative:

- Plan decides the round goal, scope, non-goals, blocked actions, and
  verification surface.
- Execute records source pins, review evidence, adaptation drafts, and
  candidate disposition proposals.
- Acceptance decides whether each candidate is adopted, merged, modeled as a
  recipe, kept as an adapter, retained as reference, or rejected.
- Stage closeout records whether the round is complete, partial, blocked,
  needs verification, needs user confirmation, or cannot close.

## Current Application

The current round is `round-02-source-intake-and-filtering`. It is in the
execution phase. The pinned source batch is evidence for review, not approval.

The current deferred actions are:

- approved payload admission;
- release manifest changes;
- source text redistribution;
- runtime installation;
- local Codex, agents, and cc Switch sync.

Those actions require later acceptance and release gates. Local runtime
alignment remains deferred until curated release coverage is broad and stable
enough to justify consumer-side projection.

## Stage Closeout Rule

A round is not closed just because useful work happened. Closeout must state:

- what was covered;
- what verification ran;
- what remains deferred, risky, or unverified;
- whether the round outcome is complete, partial, blocked, needs verification,
  needs user confirmation, or cannot close;
- what the next gate is.

If the next action changes release inventory, approved payload, local runtime
state, external publication, or source redistribution, it needs its own
explicit gate.
