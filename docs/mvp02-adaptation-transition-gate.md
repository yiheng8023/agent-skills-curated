# MVP-02 Adaptation Transition Gate

This is a gate, not approval.

Current state: awaiting explicit human approval.

Machine-readable record:
[`registry/mvp-transition-gates.json`](../registry/mvp-transition-gates.json).

## Purpose

This document defines the boundary between the completed pre-adaptation review
and any future adapted-output drafting for the first curated Skills MVP
candidate batch.

It exists so the project can continue making progress toward MVP closeout
without silently crossing the candidate-to-approved boundary.

## Scope

| Field | Value |
| --- | --- |
| Gate id | `mvp02-adaptation-transition-gate-2026-06-27` |
| Batch id | `mvp-skills-batch-2026-06-27-spec-doc-review` |
| Review id | `mvp-review-2026-06-27-spec-doc-review` |
| Current state | awaiting explicit human approval |
| Adapted output allowed | no |
| Approved payload allowed | no |
| Runtime allowed | no |
| Release manifest allowed | no |
| Routing projection allowed | no |
| Live install allowed | no |
| Source text redistribution allowed | no |

## Candidate set

The gate covers exactly the candidates already selected and reviewed:

- `spec-driven-development`
- `documentation-and-adrs`
- `code-review-and-quality`

No other candidate is included by implication.

## Required preconditions before adaptation

- The user must explicitly approve creation of adapted output for this
  candidate batch.
- The candidate source, revision, and upstream hashes must still match the
  recorded batch and review evidence.
- License, provenance, attribution, and redistribution posture must remain
  clear enough for adaptation; unclear posture must fail closed.
- Existing curated Skills, recipes, native/runtime capabilities, and conflict
  groups must remain the comparison baseline.
- Work must stay in a non-runtime review or staging surface until a separate
  release approval exists.

## Disallowed before approval

Do not create adapted output.

Do not edit `skills/`.

Do not update `release-manifest.json`.

Do not update generated routing projections.

Do not install or sync live Agent environments.

Do not redistribute upstream source text as curated payload.

Do not claim any candidate is approved, released, routable, or installable.

## What approval would allow

If explicit human approval is later recorded, the next phase may:

- create adapted draft text in a non-runtime review surface;
- record candidate-specific disposition as merge, recipe-only, adapter-only,
  reject, or approved-payload candidate;
- run focused security, portability, overlap, attribution, and validation
  review on the actual adapted output;
- prepare release-candidate evidence only after the adapted output passes
  review.

That later approval still would not automatically authorize release manifest
changes, routing projection changes, live install, or private consumer install.
Those are separate MVP gates.

## Fail closed

Fail closed if any of the following is true:

- no explicit human approval is recorded;
- source revision or upstream hash differs from recorded evidence;
- license, provenance, attribution, or redistribution posture is unclear;
- adaptation would override repository, human, or runtime authority;
- adaptation would introduce vendor-specific, agent-specific, or
  project-specific assumptions as universal rules;
- overlap with existing curated Skills, official/runtime capabilities, or
  recipes is unresolved;
- the change attempts to enter release manifest, routing projection, or live
  environment before release approval.

## Acceptance to leave this gate

This gate is not closed until all of the following are true:

1. Explicit human approval for adapted-output creation is recorded.
2. Adapted draft output exists only in an approved non-runtime review surface.
3. Candidate-specific disposition is recorded.
4. Security, portability, overlap, attribution, and validation evidence is
   recorded for the adapted output.
5. Repository verification passes without granting runtime, manifest, routing,
   or live-install status prematurely.

## Current conclusion

MVP-02 remains in progress. The project has selected a small candidate batch
and recorded candidate-specific pre-adaptation review, but it has not yet
entered adapted-output creation.
