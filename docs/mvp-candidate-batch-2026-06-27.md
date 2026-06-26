# MVP Candidate Batch: Spec, Docs, Review

This is the first small candidate batch for the curated Skills
terminal-consumer MVP.

It is a selection record, not approval. Nothing in this batch is executable,
installed, included in `skills/`, included in `release-manifest.json`, or added
to generated routing projections.

Machine-readable record:
[`registry/mvp-candidate-batches.json`](../registry/mvp-candidate-batches.json).

## Batch

| Field | Value |
| --- | --- |
| Batch id | `mvp-skills-batch-2026-06-27-spec-doc-review` |
| Source | `github:addyosmani/agent-skills` |
| Pinned revision | `17214a29c429a19f7a9607f2c06f9d650ea87eb0` |
| License posture | MIT in current source lock |
| Approval state | selected for review, not approved |
| Runtime allowed | no |
| Release manifest allowed | no |
| Routing projection allowed | no |

## Why this batch

The MVP needs a small, high-value Skill candidate batch that can prove the
review, adaptation, manifest, consumer, routing, feedback, and closeout loop.

This batch is intentionally small:

- `spec-driven-development`
- `documentation-and-adrs`
- `code-review-and-quality`

The three candidates form one coherent software-engineering slice:

```text
specification discipline
-> decision and documentation discipline
-> review and quality discipline
```

They are useful because the current curated release already has adjacent
capabilities such as `to-prd`, `to-issues`, `tdd`, `review`,
`grill-with-docs`, `ubiquitous-language`, `ci-cd-and-automation`,
`performance-optimization`, and `observability-and-instrumentation`.

That adjacency is deliberate. These are not direct imports. They are merge
candidates: the review should decide whether useful pieces become merged
guidance, a recipe, adapter-only metadata, rejection evidence, or a future
adapted payload.

## Candidate notes

### `spec-driven-development`

Target gap: sharper spec-first acceptance and implementation discipline across
PRD, issue slicing, TDD, review, and launch workflows.

Likely merge targets:

- `skill.curated.to-prd`
- `skill.curated.to-issues`
- `skill.curated.tdd`
- `skill.curated.review`

Review questions:

- Which spec-driven steps are already covered by existing curated Skills or
  native capability?
- Which acceptance and traceability rules should become a recipe instead of a
  new Skill body?
- Does any wording assume a specific Agent, IDE, or upstream command?

### `documentation-and-adrs`

Target gap: explicit documentation and ADR lifecycle rules for decisions,
context drift, and long-term maintainability.

Likely merge targets:

- `skill.curated.grill-with-docs`
- `skill.curated.ubiquitous-language`
- `skill.curated.improve-codebase-architecture`
- `skill.curated.handoff`

Review questions:

- Which ADR/documentation steps are general enough for portable curated
  guidance?
- Which parts belong in repository-local standards rather than a Skill?
- How should generated documentation, hand-written authority, and archived
  context be distinguished?

### `code-review-and-quality`

Target gap: quality-oriented review posture that complements existing review,
security, CI/CD, and performance workflows without duplicating them.

Likely merge targets:

- `skill.curated.review`
- `skill.curated.ci-cd-and-automation`
- `skill.curated.performance-optimization`
- `skill.curated.observability-and-instrumentation`

Review questions:

- Which quality checks are already covered by review, CI/CD, security,
  performance, or native reasoning?
- Which quality dimensions should be represented as routing scenarios or
  recipes?
- What evidence is required before claiming a quality improvement?

## Boundaries

- Do not copy upstream Skill bodies into `skills/` during this selection step.
- Do not add these candidates to `release-manifest.json`.
- Do not add these candidates to generated routing projections as executable
  targets.
- Do not install or sync candidates into live Agent environments.
- Do not treat `merge` disposition as approval.

## Next review path

```text
candidate selection
-> candidate-specific provenance check
-> focused security review
-> focused portability and agent-neutrality review
-> focused overlap review
-> disposition decision
-> adaptation or rejection
-> validation
-> topology and manifest update only if approved
```

This document closes MVP-01 selection evidence only. It does not close review,
adaptation, release, runtime consumption, feedback, or global closeout.
