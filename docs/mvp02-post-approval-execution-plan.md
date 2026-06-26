# MVP-02 Post-Approval Execution Plan

Machine-readable plan:
[`registry/mvp02-post-approval-execution-plan.json`](../registry/mvp02-post-approval-execution-plan.json).

This is a plan, not approval.

## Current state

```text
status: post_approval_plan_ready_not_executable_without_owner_approval
approval recorded: false
adapted output present: false
planned output root: drafts/mvp02-adaptation/
```

The planned output root must not exist before owner approval. The plan only
defines the future execution sequence so the next approved step does not depend
on chat memory.

## When this plan may be used

Use this plan only after the owner explicitly approves one of the active safe
approval phrases:

```text
批准进入 MVP-02 适配草案阶段
Approve MVP-02 adapted draft creation only
```

Goal continuation is not approval. A continuation prompt keeps the MVP active,
but it does not authorize adapted output.

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

## Still disallowed until approval

- Do not create adapted candidate output.
- Do not create `drafts/mvp02-adaptation/`.
- Do not edit `skills/`.
- Do not update `release-manifest.json`.
- Do not update generated routing projections.
- Do not install or sync live Agent environments.
- Do not approve, release, or publish any candidate payload.
- Do not redistribute upstream source text as approved curated payload.

## Why this plan exists

The repository is ready for an owner decision, but not ready to adapt without
that decision. This execution plan makes the future authorized path
deterministic while keeping the current state fail-closed.
