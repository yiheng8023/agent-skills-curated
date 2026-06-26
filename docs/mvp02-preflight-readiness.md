# MVP-02 Preflight Readiness

Machine-readable record:
[`registry/mvp02-preflight-readiness.json`](../registry/mvp02-preflight-readiness.json).

This is a readiness record, not approval.

## Current state

```text
status: preflight_ready_awaiting_owner_approval
approval recorded: false
adapted output present: false
```

MVP-02 has enough non-executable evidence to ask the owner whether adapted draft
creation may begin. It does not have approval to create adapted output.

## What is ready

- A small candidate batch is selected and pinned.
- Candidate-specific pre-adaptation review exists.
- The transition gate is waiting for explicit owner approval.
- The adaptation review checklist is template-only and ready for future use.
- The approval request is bounded and still pending.
- Candidates are not approved Skills.
- Candidates are not in `release-manifest.json`.
- Candidates are not executable routing targets.
- Live Agent environments are not touched.

## Safe approval phrases

The owner may approve only the adapted-draft step with one of these phrases:

```text
批准进入 MVP-02 适配草案阶段
Approve MVP-02 adapted draft creation only
```

Any broader wording must be treated conservatively and checked against the
active transition gate.

## Still disallowed

Until a later gate explicitly approves it:

- do not edit `skills/`;
- do not update `release-manifest.json`;
- do not update generated routing projections;
- do not install or sync live Agent environments;
- do not approve, release, or publish any candidate payload;
- do not redistribute upstream source text as approved curated payload.

## Why this record exists

Without a preflight record, the MVP can appear vaguely blocked. This document
makes the state explicit: the repository is ready to request the smallest owner
decision, but the next implementation step still requires that decision.

