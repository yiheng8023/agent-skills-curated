# MVP-02 Adapted Draft Review

Machine-readable record:
[`registry/mvp02-adapted-drafts.json`](../registry/mvp02-adapted-drafts.json).

Approval event:
[`registry/mvp02-approval-events.json`](../registry/mvp02-approval-events.json).

This is adapted draft evidence, not release approval.

## Current state

```text
status: adapted_draft_review_recorded_not_approved
approval phrase: 批准进入 MVP-02 适配草案阶段
draft root: drafts/mvp02-adaptation/
approved payload allowed: false
release manifest allowed: false
routing projection allowed: false
live install allowed: false
source text redistribution allowed: false
```

The owner approved only the narrow MVP-02 transition from pre-adaptation review
to non-runtime adapted draft creation. The approval does not authorize
`skills/` edits, `release-manifest.json` updates, generated routing projection
updates, live Agent environment changes, candidate release, or publication.

## Candidate dispositions

| Candidate | Draft | Disposition | Reason |
| --- | --- | --- | --- |
| `spec-driven-development` | `drafts/mvp02-adaptation/spec-driven-development/DRAFT.md` | `recipe-only` | The useful pattern spans PRD, issue slicing, TDD, review, and launch flow. A recipe avoids duplicating existing Skills while preserving a spec-first checkpoint chain. |
| `documentation-and-adrs` | `drafts/mvp02-adaptation/documentation-and-adrs/DRAFT.md` | `merge` | The ADR and documentation-authority guidance can strengthen existing documentation, architecture, glossary, and handoff Skills without creating a duplicate runtime Skill. |
| `code-review-and-quality` | `drafts/mvp02-adaptation/code-review-and-quality/DRAFT.md` | `merge` | The quality review axes can strengthen existing review, CI/CD, performance, observability, and security routing without overriding repository or human merge authority. |

## Checklist summary

Each draft records:

- source integrity;
- license and attribution;
- security and prompt-injection boundary;
- portability and neutralization;
- overlap and conflict;
- routing and runtime boundary;
- validation expectations;
- final disposition and next gate.

No upstream source body is copied as an approved curated payload. Each draft is
neutralized, agent-neutral, and bounded to a non-runtime review surface.

## Boundary checks

- `skills/` remains the approved release payload surface only.
- `release-manifest.json` remains schema 1 and is not updated by MVP-02 draft
  creation.
- `generated/` remains derived projection output and is not updated as an
  executable route for these candidates.
- Live Agent environments are not installed, restored, synced, or modified.
- Candidate drafts are not executable routing targets.

## Next gate

MVP-02 now has adapted draft review evidence. The next step is a separate
release-or-routing candidate review gate. That later gate must decide whether
any draft becomes a release-manifest payload change, a recipe/routing change,
reference-only evidence, or rejection. No such next gate is approved here.
