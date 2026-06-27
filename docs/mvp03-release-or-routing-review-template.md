# MVP-03 Release-Or-Routing Review Template

Machine-readable template:
[`registry/mvp03-release-or-routing-review-template.json`](../registry/mvp03-release-or-routing-review-template.json).

Template only, not approval.

This template defines how to run MVP-03 release-or-routing candidate review
after the owner explicitly approves that gate. It does not approve any
candidate, payload, manifest, routing projection, install, publication, or
source redistribution.

## When this template may be used

Use this template only after one of the bounded approval phrases is recorded:

```text
批准进入 MVP-03 release/routing 候选审查阶段
```

or:

```text
Approve MVP-03 release-or-routing candidate review only
```

Without that approval, this document remains scaffolding.

## Review sections

Each candidate-specific review must cover:

1. source integrity;
2. license and attribution;
3. security;
4. portability and neutralization;
5. overlap and conflict;
6. native or runtime equivalence;
7. routing semantics;
8. release manifest impact;
9. consumer install impact;
10. validation plan;
11. rejected alternatives;
12. next gate.

## Allowed decisions after approval

- `release-payload-candidate`
- `recipe-routing-proposal`
- `merge-into-existing-approved-skill`
- `reference-only`
- `reject`

These decisions are still review outcomes. A `release-payload-candidate`,
`recipe-routing-proposal`, or `merge-into-existing-approved-skill` outcome
does not by itself mutate `skills/`, `release-manifest.json`, generated
routing, or live Agent environments. Those require later, narrower gates.

## Fail-closed conditions

Stop the review or keep the candidate out of the execution path if:

- owner approval for MVP-03 review is missing;
- candidate source revision or upstream hash differs from MVP-02 evidence;
- license, provenance, attribution, or redistribution posture is unclear;
- security, portability, overlap, or native/runtime equivalence review is
  incomplete;
- the candidate would override repository, runtime, or human authority;
- the candidate would enter `skills/`, `release-manifest.json`, generated
  routing, or a live environment before its later specific gate;
- the candidate decision is based only on enthusiasm, source popularity, or
  broad usefulness without evidence.

## Output contract after approval

The future candidate review record must contain one entry per candidate and
include:

- decision;
- rationale;
- evidence;
- rejected alternatives;
- boundary assertions;
- validation results;
- next gate.

Until that record exists and passes verification, MVP-03 remains preflight-only
and the MVP remains active in progress.
