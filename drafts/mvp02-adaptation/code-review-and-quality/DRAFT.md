# MVP-02 Adapted Draft: code-review-and-quality

Status: non-runtime adapted draft, not approved payload.

Source integrity:

- Source: `github:addyosmani/agent-skills`
- Revision: `17214a29c429a19f7a9607f2c06f9d650ea87eb0`
- Upstream path: `skills/code-review-and-quality/SKILL.md`
- Upstream SHA-256: `fe455372ce2d6ff9c2f22507fccfe7474a5f0378a7936981b286922c5a8d8a43`
- Adapted draft derives only from the recorded source and prior review evidence.

License and attribution:

The reviewed upstream source is MIT licensed. This draft is a synthesized and
neutralized adaptation for review only. It does not copy upstream source text as
an approved curated payload and does not grant release, routing, or runtime use.

## Adapted guidance

Use quality review guidance when a change may affect correctness,
maintainability, security, performance, observability, data integrity, user
trust, or long-term operability. Keep the review depth proportional to impact:
small low-risk changes may use native reasoning and targeted verification.

Review axes:

1. Correctness: behavior, edge cases, invariants, and tests match the stated
   goal.
2. Clarity: the change is understandable, minimal, and avoids unnecessary
   abstraction.
3. Architecture: boundaries, ownership, coupling, migration path, and future
   maintenance remain coherent.
4. Security: secrets, permissions, input handling, dependency risk, and data
   exposure are bounded.
5. Operability: performance, logs, metrics, rollout, rollback, and failure
   modes are considered when relevant.

Project-specific commands such as test, lint, typecheck, dependency audit, or
security scan must be discovered from the repository before use. No ecosystem
command is universal.

## Security

This draft does not authorize merge, release, deployment, dependency install,
or external service use. Security findings should route to the active security
capability or repository process. Human and repository authority remain final
for merge and release decisions.

## Portability and neutralization

Tool-specific and ecosystem-specific examples are neutralized into review
roles. The guidance applies across languages and agents, provided the active
repository supplies the actual verification commands and authority rules.

## Overlap and conflict

This candidate overlaps `review`, `ci-cd-and-automation`,
`performance-optimization`, `observability-and-instrumentation`, and security
capabilities. Current disposition: `merge`. The material should strengthen
existing review and routing rules rather than create a duplicate quality Skill.

## Routing and runtime boundary

Positive trigger: PR review, substantial diff review, quality gate design,
release readiness, or high-impact refactor review.

Negative trigger: trivial edits, purely stylistic changes, or review requests
already handled by a narrower specialized capability.

Fallback: native reasoning with a risk-proportional review checklist.

## Validation

Future changes must prove that review depth is proportional, specialized
security and performance routes remain available, and no candidate becomes an
approved payload without a separate release gate. This draft itself must remain
outside `skills/`, `release-manifest.json`, generated routing projections, and
live Agent environments.

## Disposition

Decision: `merge`.

Next gate: `mvp03-release-or-routing-candidate-review`.
