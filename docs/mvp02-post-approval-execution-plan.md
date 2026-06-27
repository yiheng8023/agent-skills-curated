# MVP-02 Post-Approval Execution Plan

Machine-readable plan:
[`registry/mvp02-post-approval-execution-plan.json`](../registry/mvp02-post-approval-execution-plan.json).

This is an executed plan record, not release approval.

## Current state

```text
status: executed_after_owner_approval_stopped_before_release_gate
approval recorded: true
adapted output present: true
planned output root: drafts/mvp02-adaptation/
```

The planned output root exists only because owner approval was recorded. The
plan has been executed through adapted draft creation and then stopped before
release, routing, or live-install gates.

## When this plan may be used

This plan may be used only after the owner explicitly approves one of the
active safe approval phrases:

```text
批准进入 MVP-02 适配草案阶段
Approve MVP-02 adapted draft creation only
```

Goal continuation is not approval. The recorded approval phrase authorized only
non-runtime adapted draft creation.

## Covered candidate batch

This plan covers exactly:

- `spec-driven-development`
- `documentation-and-adrs`
- `code-review-and-quality`

It does not cover any other source, official/runtime capability, future
candidate, release payload, routing projection, or live Agent environment.

## Execution sequence after approval

1. Record the approval event.
   - Confirm the approval phrase matches the active safe approval phrase list.
   - Confirm the scope is limited to non-runtime adapted draft creation plus
     checklist-based review.
2. Create the non-runtime review surface.
   - Use only `drafts/mvp02-adaptation/`.
   - Do not write under `skills/`.
   - Do not update `release-manifest.json`.
   - Do not update generated routing projections.
   - Do not touch live Agent environments.
3. Draft candidate adaptations.
   - Remove or bound private assumptions.
   - Preserve source attribution and license boundaries.
   - Do not redistribute upstream source text as approved curated payload.
   - Record overlap with existing curated Skills and native/runtime capability.
4. Complete the MVP-02 adaptation review checklist.
   - Source integrity.
   - License and attribution.
   - Security and prompt-injection.
   - Portability and neutrality.
   - Overlap and conflict.
   - Runtime boundary.
   - Validation evidence.
   - Final disposition.
5. Run verification.
   - `python -B scripts/verify.py`
   - `python -B scripts/build_topology.py --check`
   - `python -B -m unittest discover -s tests -v`
6. Stop before the next gate.
   - No release manifest update.
   - No generated routing projection update.
   - No live install or sync.
   - No approved curated payload.
   - Record the next required gate explicitly.

## Still disallowed until the next gate

- Do not edit `skills/`.
- Do not update `release-manifest.json`.
- Do not update generated routing projections.
- Do not install or sync live Agent environments.
- Do not approve, release, or publish any candidate payload.
- Do not redistribute upstream source text as approved curated payload.

## Why this plan exists

The repository consumed the owner decision and produced non-runtime adapted
drafts. The next state is deliberately fail-closed: no candidate may become a
release payload, generated route, approved Skill, live install, or publication
without a separate next gate.
