# MVP-03 Release-Or-Routing Preflight

Machine-readable record:
[`registry/mvp03-release-or-routing-preflight.json`](../registry/mvp03-release-or-routing-preflight.json).

This is a preflight and approval request, not approval.

## Current state

```text
status: release_or_routing_review_preflight_ready_not_approved
gate: mvp03-release-or-routing-candidate-review
approval recorded: false
```

MVP-02 produced three non-runtime adapted drafts:

- `spec-driven-development`
- `documentation-and-adrs`
- `code-review-and-quality`

Those drafts are evidence for the next decision, not approved payloads.

## What this preflight proves

- The adapted drafts exist only under `drafts/mvp02-adaptation/`.
- Source, license, upstream paths, and upstream hashes remain pinned.
- The current dispositions are recorded:
  - `spec-driven-development`: `recipe-only`
  - `documentation-and-adrs`: `merge`
  - `code-review-and-quality`: `merge`
- Candidate IDs are not approved Skill directories.
- Candidate IDs are not in `release-manifest.json`.
- Candidate IDs are not executable routing targets in `registry/routing.json`
  or `generated/routing-index.json`.

## Requested approval scope

The smallest useful next approval is:

```text
批准进入 MVP-03 release/routing 候选审查阶段
```

or:

```text
Approve MVP-03 release-or-routing candidate review only
```

If the owner approves this scope, the next work may review each adapted draft
and record whether it should become:

- `release-payload-candidate`;
- `recipe-routing-proposal`;
- `merge-into-existing-approved-skill`;
- `reference-only`;
- `reject`.

## Still disallowed

Until a separate approval is recorded:

- do not edit `skills/`;
- do not update `release-manifest.json`;
- do not update generated routing projections;
- do not install or sync live Agent environments;
- do not approve, release, or publish any candidate payload;
- do not redistribute upstream source text as approved curated payload.

## Candidate review bias

The review should remain skeptical of unnecessary payload growth:

- `spec-driven-development` should prefer recipe/routing or reference-only
  unless a standalone payload is clearly better than existing PRD, issue, TDD,
  review, and launch guidance.
- `documentation-and-adrs` should prefer merging into existing documentation,
  architecture, handoff, and terminology guidance unless a standalone gap is
  proven.
- `code-review-and-quality` should prefer merging into existing review, CI/CD,
  performance, observability, and security routes unless a standalone gap is
  proven.

## Why this record exists

The MVP closeout standard requires progress, but progress must not collapse
human gates. This preflight makes the next gate executable by a future thread
without letting continuation language become release, routing, installation, or
publication approval.
