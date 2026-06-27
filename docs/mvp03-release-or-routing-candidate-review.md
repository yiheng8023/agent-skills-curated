# MVP-03 Release-Or-Routing Candidate Review

Machine-readable record:
[`registry/mvp03-release-or-routing-candidate-review.json`](../registry/mvp03-release-or-routing-candidate-review.json).

Approval event:
[`registry/mvp03-approval-events.json`](../registry/mvp03-approval-events.json).

This is candidate review evidence, not release approval.

## Current state

```text
status: candidate_review_recorded_not_release_approved
approval phrase: 批准进入 MVP-03 release/routing 候选审查阶段
candidate review allowed: true
approved payload allowed: false
release manifest allowed: false
routing projection allowed: false
live install allowed: false
source text redistribution allowed: false
```

The owner approved only the narrow MVP-03 transition from preflight to
candidate-specific release-or-routing review. The approval does not authorize
`skills/` edits, `release-manifest.json` updates, generated routing projection
updates, live Agent environment changes, candidate release, publication, or
source redistribution.

## Candidate decisions

| Candidate | Decision | Why |
| --- | --- | --- |
| `spec-driven-development` | `recipe-routing-proposal` | The useful pattern is an orchestration checkpoint chain across PRD, issue slicing, TDD, review, and launch. A recipe/routing proposal avoids duplicating existing approved Skills. |
| `documentation-and-adrs` | `merge-into-existing-approved-skill` | The useful material strengthens durable documentation authority, ADR-style records, terminology governance, and handoff continuity. |
| `code-review-and-quality` | `merge-into-existing-approved-skill` | The useful material strengthens proportional quality review across review, CI/CD, performance, observability, and security routes. |

## Rejected alternatives

- None of the three candidates is approved as a standalone release payload in
  this gate.
- `spec-driven-development` is not merged into a single approved Skill because
  its value spans multiple existing workflows.
- `documentation-and-adrs` and `code-review-and-quality` are not converted into
  recipe-only outputs because their value is mainly targeted enrichment of
  existing approved Skills and routing rules.
- No candidate is downgraded to reference-only because each provides actionable
  future work, but that future work still needs a narrower gate.

## Boundary checks

- `skills/` remains unchanged.
- `release-manifest.json` remains unchanged.
- `registry/routing.json` and `generated/routing-index.json` remain unchanged.
- Live Agent environments are not installed, restored, synced, or modified.
- Upstream source text is not redistributed as approved curated payload.
- Candidate decisions are not approved payloads and are not executable routing
  targets.

## Next gates

- `spec-driven-development` requires a separate routing projection proposal
  gate before any `registry/routing.json`, generated routing, or runtime
  behavior changes.
- `documentation-and-adrs` requires a separate approved-payload or governed
  documentation diff gate before any existing Skill or governed document is
  mutated.
- `code-review-and-quality` requires a separate approved-payload or routing
  diff gate before any existing Skill, routing registry, or generated
  projection is mutated.

MVP-03 has now produced candidate-specific disposition evidence. The MVP is
still active because release payload, private consumer installation, runtime
routing proof, feedback, and lifecycle evidence remain later gates.
