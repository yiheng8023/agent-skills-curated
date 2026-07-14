# Round Lifecycle Contract

This repository expands through bounded rounds, not one large import. Every
round has four explicit phases:

1. Plan.
2. Execute.
3. Acceptance.
4. Stage closeout.

The machine contract lives in `registry/round-lifecycle-contract.json`. The
active and historical round states live in
`registry/curation-expansion-rounds.json`.

## Phase Meanings

- Plan binds the round goal, scope, non-goals, authority boundary, blocked
  actions, evidence requirements, verification surface, and next gate.
- Execute records pinned sources, reviews, adaptations, and candidate
  dispositions without silently upgrading them to release or runtime state.
- Acceptance decides adopt, merge, recipe-only, adapter-only, reference-only,
  reject, or another explicitly governed outcome from the available evidence.
- Stage closeout reconciles the round goal against evidence and records a
  truthful outcome, residual risks, deferred work, and the next-round or pause
  decision.

Discovery is not approval. Acceptance is not live installation. A local
Codex, agents, and cc Switch sync requires a separately authorized consumer
gate and fresh verification. A dated execution record is evidence for that
transaction only.

## Current Application

Round 02 has recorded planning, closed execution, and passed candidate/release
acceptance evidence. Its stage closeout remains pending. The current machine
state is therefore `needs-closeout` with `needs_reconciliation`, supported by:

- `registry/round02-approved-payload-routing-proposal.json`
- `registry/round02-local-runtime-sync-execution.json`

This state deliberately rejects two inaccurate alternatives:

- `active`: source intake is no longer the latest evidenced phase;
- `closed`: no distinct requirement-by-requirement stage-closeout record exists.

Before a new candidate intake round becomes active, closeout reconciliation
must state what was covered, which checks ran, what remains partial or stale,
whether current live state was reverified, what authority remains external, and
whether the next decision is proceed, pause, or open a separately authorized
work package.

## Closeout Rule

A round is not closed because useful work happened or because a verifier is
green. Closeout must expose:

- goal and scope coverage;
- acceptance and verification evidence;
- dirty state and skipped checks;
- partial, stale, deferred, risky, or unverified items;
- external authority and side-effect boundaries;
- the next round, work package, or pause decision.

Allowed closeout outcomes remain `complete`, `partial`, `blocked`,
`needs_verification`, `needs_user_confirmation`, and `cannot_close`. The outcome
must follow the evidence rather than a requested label.
