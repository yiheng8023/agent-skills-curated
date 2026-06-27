# MVP-02 Adaptation Approval Request

Request record, not release approval.

Current decision: approved for adapted draft creation only.

Adapted output exists only under `drafts/mvp02-adaptation/`.

Machine-readable request:
[`registry/mvp-approval-requests.json`](../registry/mvp-approval-requests.json).

## Why this request exists

The MVP-02 transition gate and adaptation review checklist are ready, but they
intentionally do not authorize adapted-output creation.

This request narrows the next human decision to the smallest useful scope:
whether the selected candidate batch may move from pre-adaptation review into
non-runtime adapted draft creation.

Do not treat goal continuation as approval. A continuation prompt keeps the MVP
objective active; it does not by itself authorize candidate adaptation,
release, routing, installation, or source redistribution.

## Candidate batch

This request covers exactly:

- `spec-driven-development`
- `documentation-and-adrs`
- `code-review-and-quality`

It does not include any other source, repository, official/runtime capability,
or future candidate.

## Approved scope

The owner approved this request with:

```text
批准进入 MVP-02 适配草案阶段
```

The approved next phase may:

- create adapted draft output in a non-runtime review surface;
- apply the MVP-02 adaptation review checklist;
- record candidate-specific disposition evidence;
- run focused security, portability, overlap, attribution, and validation
  review on the adapted draft.

The next state is adapted-output drafting in a non-runtime review surface.

## Explicitly not approved

This request did not ask permission to:

- edit `skills/`;
- update `release-manifest.json`;
- update generated routing projections;
- install or sync live Agent environments;
- approve, release, or publish any candidate payload;
- redistribute upstream source text as approved curated payload.

Those remain separate gates.

## Safe approval phrases

These phrases define the narrow approval boundary for this step:

```text
批准进入 MVP-02 适配草案阶段
```

or:

```text
Approve MVP-02 adapted draft creation only
```

Any broader approval must explicitly name the broader action. Otherwise, the
system interprets approval as limited to non-runtime adapted draft creation
plus checklist-based review.

## Evidence recorded after approval

The next record now includes:

1. adapted draft location;
2. completed checklist sections;
3. candidate-specific disposition;
4. verification command results;
5. explicit record that manifest, routing projection, and live install remain
   unchanged.

## Current conclusion

MVP-02 remains partial. The bounded owner decision has been recorded and
adapted draft output exists, but no release, routing, runtime use, live install,
or publication has been authorized.
