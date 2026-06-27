# MVP-02 Adapted Draft: documentation-and-adrs

Status: non-runtime adapted draft, not approved payload.

Source integrity:

- Source: `github:addyosmani/agent-skills`
- Revision: `17214a29c429a19f7a9607f2c06f9d650ea87eb0`
- Upstream path: `skills/documentation-and-adrs/SKILL.md`
- Upstream SHA-256: `7fed35f9c5b95d8e3623ad24d78d209c3267ab62d7157fc03954c76a7e58adf4`
- Adapted draft derives only from the recorded source and prior review evidence.

License and attribution:

The reviewed upstream source is MIT licensed. This draft is a synthesized and
neutralized adaptation for review only. It does not copy upstream source text as
an approved curated payload and does not grant release, routing, or runtime use.

## Adapted guidance

Use documentation and ADR guidance when a decision, behavior, interface,
architecture, migration, or operational rule must remain understandable after
the current conversation ends.

Documentation should distinguish:

- current authority: the rule or decision that governs the system now;
- historical context: why the choice was made and which alternatives were
  rejected;
- generated projection: derived documentation that must not become a second
  truth source;
- archived context: useful history that is not current authority.

An ADR-like record should capture context, decision, alternatives, consequences,
status, supersession path, and verification evidence. Repository-local formats
may vary; no single filename, agent instruction file, stack, or toolchain is
universal.

## Security

This draft adds no external service dependency, no credential handling, no
automatic file mutation, and no publish action. Documentation that touches
private paths, account state, credentials, customer data, or unreleased
strategy must stay in private or repository-authorized surfaces.

## Portability and neutralization

Claude-specific instruction filenames and technology-stack examples are
neutralized into generic agent instruction files, repository-local standards,
and project-owned documentation. The guidance is agent-neutral and does not
assume a specific language, package manager, database, or platform.

## Overlap and conflict

This candidate overlaps `grill-with-docs`, `ubiquitous-language`,
`improve-codebase-architecture`, and `handoff`. Current disposition: `merge`.
The useful material should strengthen existing Skills and repository standards
rather than create a duplicate documentation Skill.

## Routing and runtime boundary

Positive trigger: durable decisions, ADR requests, architecture rationale,
handoff continuity, terminology governance, or documentation-authority cleanup.

Negative trigger: temporary notes, simple summaries, or generated docs that do
not need authority status.

Fallback: native reasoning with a small current-vs-history note.

## Validation

Future changes must verify that generated documents remain projections, not
truth sources; private information is not moved into public docs; and repository
documentation authority is not overridden. This draft itself must remain
outside `skills/`, `release-manifest.json`, generated routing projections, and
live Agent environments.

## Disposition

Decision: `merge`.

Next gate: `mvp03-release-or-routing-candidate-review`.
