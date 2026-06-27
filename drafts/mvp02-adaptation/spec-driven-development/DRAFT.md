# MVP-02 Adapted Draft: spec-driven-development

Status: non-runtime adapted draft, not approved payload.

Source integrity:

- Source: `github:addyosmani/agent-skills`
- Revision: `17214a29c429a19f7a9607f2c06f9d650ea87eb0`
- Upstream path: `skills/spec-driven-development/SKILL.md`
- Upstream SHA-256: `16041b4b6149c0e99d7323f8c1e2104ddca2819bf46f78c402a8f0458938e344`
- Adapted draft derives only from the recorded source and prior review evidence.

License and attribution:

The reviewed upstream source is MIT licensed. This draft is a synthesized and
neutralized adaptation for review only. It does not copy upstream source text as
an approved curated payload and does not grant release, routing, or runtime use.

## Adapted guidance

Use a spec-first route when the task is ambiguous, multi-step, multi-file,
architectural, product-facing, or likely to create long-lived behavior. Skip
this route for small, low-risk edits where native reasoning and ordinary
verification are sufficient.

Recommended recipe shape:

1. Clarify the target outcome, non-goals, owner, affected users, and risk.
2. Record assumptions separately from facts and mark unknowns that need
   verification.
3. Define acceptance criteria before implementation work begins.
4. Split work into small units that can be verified independently.
5. Select the implementation path: native execution, existing curated Skill,
   recipe/DAG, or human confirmation.
6. Verify against the acceptance criteria and record what remains unresolved.

Repository commands are never universal defaults. Build, test, lint, migration,
or launch commands must be discovered from the active repository and checked
against its authority surface before use.

## Security

The draft contains no executable hooks, no install instructions, no credential
requirements, and no external service assumptions. Any side-effecting step such
as schema migration, dependency installation, deployment, commit, push, or
release requires an explicit later authorization boundary.

## Portability and neutralization

Agent-specific skill names and upstream skill-path references are neutralized
into structural roles: PRD, issue slicing, TDD, review, launch, and native
reasoning. The route is language-neutral and repository-neutral.

## Overlap and conflict

This candidate overlaps existing `to-prd`, `to-issues`, `tdd`, `review`, and
launch workflows. It should not become a duplicate Skill unless later evidence
proves a separate runtime body is materially better. Current disposition:
`recipe-only`.

## Routing and runtime boundary

Positive trigger: ambiguous or consequential work needing a spec, acceptance
criteria, and traceable implementation plan.

Negative trigger: trivial edits, one-off explanations, or already-scoped tasks
where the cost of a spec loop exceeds the risk.

Fallback: native reasoning plus lightweight acceptance checklist.

## Validation

Validation requires repository verification after any future recipe or routing
change. This draft itself must remain outside `skills/`, `release-manifest.json`,
generated routing projections, and live Agent environments.

## Disposition

Decision: `recipe-only`.

Next gate: `mvp03-release-or-routing-candidate-review`.
