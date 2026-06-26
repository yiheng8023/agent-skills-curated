# MVP Candidate Review Draft: Spec, Docs, Review

This is pre-adaptation review evidence for the first curated Skills
terminal-consumer MVP batch.

It is not approval. It does not authorize adaptation, release, routing,
installation, or live Agent use.

Machine-readable record:
[`registry/mvp-candidate-reviews.json`](../registry/mvp-candidate-reviews.json).

## Scope

| Field | Value |
| --- | --- |
| Review id | `mvp-review-2026-06-27-spec-doc-review` |
| Batch id | `mvp-skills-batch-2026-06-27-spec-doc-review` |
| Source | `github:addyosmani/agent-skills` |
| Pinned revision | `17214a29c429a19f7a9607f2c06f9d650ea87eb0` |
| License posture | MIT in current source lock |
| Review state | pre-adaptation review, not approved |
| Runtime allowed | no |
| Release manifest allowed | no |
| Routing projection allowed | no |
| Adapted payload allowed | no |

The upstream candidate `SKILL.md` files were fetched read-only from the pinned
revision for inspection. They were not vendored into this repository.

## Candidate source hashes

| Candidate | Upstream path | SHA-256 |
| --- | --- | --- |
| `spec-driven-development` | `skills/spec-driven-development/SKILL.md` | `16041b4b6149c0e99d7323f8c1e2104ddca2819bf46f78c402a8f0458938e344` |
| `documentation-and-adrs` | `skills/documentation-and-adrs/SKILL.md` | `7fed35f9c5b95d8e3623ad24d78d209c3267ab62d7157fc03954c76a7e58adf4` |
| `code-review-and-quality` | `skills/code-review-and-quality/SKILL.md` | `fe455372ce2d6ff9c2f22507fccfe7474a5f0378a7936981b286922c5a8d8a43` |

## Review summary

All three candidates are instruction-only upstream Skill bodies in this review
slice. No embedded executable payload, Hook, command adapter, CI workflow, MCP
server, or runtime installer is approved by this record.

The batch remains useful, but it should not be directly imported. Each
candidate overlaps existing curated Skills and should be treated as merge,
recipe, adapter, or rejection material after human approval.

## `spec-driven-development`

Useful signal:

- Strong spec-first posture.
- Explicit phase gates before implementation.
- Emphasis on acceptance criteria, assumptions, verification, and human review.

Risks and adaptation constraints:

- Example commands such as build, test, lint, and dev commands are
  project-specific examples, not portable execution defaults.
- Upstream references to `incremental-implementation`,
  `test-driven-development`, and `context-engineering` must not become
  unresolved runtime dependencies.
- The phrase-level implementation flow must remain subject to the active
  repository's authority and user approval.

Preliminary disposition: merge or recipe candidate.

Likely targets:

- `skill.curated.to-prd`
- `skill.curated.to-issues`
- `skill.curated.tdd`
- `skill.curated.review`

## `documentation-and-adrs`

Useful signal:

- ADR lifecycle guidance.
- Clear distinction between historical context and current decisions.
- Helpful public/private artifact hygiene and continuity implications.

Risks and adaptation constraints:

- Claude-specific references such as `CLAUDE.md` must be neutralized to
  generic agent instruction files or repository-local guidance.
- PostgreSQL, Prisma, npm, OpenAPI, and TypeScript examples are illustrative,
  not universal defaults.
- Repository-local documentation standards must not be confused with portable
  Skill behavior.

Preliminary disposition: merge candidate.

Likely targets:

- `skill.curated.grill-with-docs`
- `skill.curated.ubiquitous-language`
- `skill.curated.improve-codebase-architecture`
- `skill.curated.handoff`

## `code-review-and-quality`

Useful signal:

- Multi-axis review posture covering correctness, readability, architecture,
  security, and performance.
- Useful framing for AI-generated code review.
- Good separation between required feedback and optional nits.

Risks and adaptation constraints:

- Approval language must not override repository merge, release, or human
  authority.
- `npm audit` is an ecosystem-specific example, not a universal check.
- References to `security-and-hardening` and performance guidance must map to
  existing curated Skills, official security capabilities, or recipes.
- The adapted route must not make review mandatory for every trivial or
  low-risk change.

Preliminary disposition: merge or recipe candidate.

Likely targets:

- `skill.curated.review`
- `skill.curated.ci-cd-and-automation`
- `skill.curated.performance-optimization`
- `skill.curated.observability-and-instrumentation`

## Not closed by this review

This document does not close MVP-02. It only records candidate-specific
pre-adaptation evidence.

Remaining MVP-02 work:

1. Human approval to proceed from selection into adaptation.
2. Candidate-specific provenance and license confirmation before copying or
   adapting text.
3. Focused security, portability, overlap, and conflict review for the actual
   adapted output.
4. A concrete disposition per candidate: merge into existing Skill,
   recipe-only, adapter-only, reject, or approve adapted payload.
5. Validation evidence after any adapted text or topology changes.

## Boundary

Do not copy upstream source text into `skills/`, do not add these candidates to
`release-manifest.json`, do not update generated routing projections, and do
not install or sync anything into live Agent environments based on this review
record.
