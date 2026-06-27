# MVP-03 Release-Or-Routing Approval Request

Machine-readable request:
[`registry/mvp03-release-or-routing-approval-request.json`](../registry/mvp03-release-or-routing-approval-request.json).

This is an approval request, not approval.

## Current state

```text
status: awaiting_owner_approval
approval recorded: false
candidate review allowed: false
```

The selected candidates have MVP-02 non-runtime adapted drafts, MVP-03
preflight evidence, and a template-only MVP-03 review contract. They do not have
approval to enter candidate review, release, routing, manifest, install,
publication, or source redistribution.

## Requested approval

The smallest useful approval phrase is:

```text
批准进入 MVP-03 release/routing 候选审查阶段
```

or:

```text
Approve MVP-03 release-or-routing candidate review only
```

If approved, the next work may apply the MVP-03 review template to exactly:

- `spec-driven-development`
- `documentation-and-adrs`
- `code-review-and-quality`

The review may decide whether each candidate should become:

- `release-payload-candidate`;
- `recipe-routing-proposal`;
- `merge-into-existing-approved-skill`;
- `reference-only`;
- `reject`.

## Explicitly not requested

This request does not ask permission to:

- edit `skills/`;
- update `release-manifest.json`;
- update generated routing projections;
- install or sync live Agent environments;
- approve, release, or publish any candidate payload;
- redistribute upstream source text as approved curated payload.

## Evidence that must exist after approval

If the owner approves this request, the next record must include:

1. owner approval event record;
2. candidate-specific release/routing disposition record;
3. rationale for release payload, recipe/routing proposal, merge,
   reference-only, or reject;
4. verification command results;
5. explicit record that live install, publication, and source redistribution
   remain unchanged unless separately approved.

Until the approval event exists, MVP-03 remains preflight-only and the MVP
remains active in progress.
