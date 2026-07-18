# Agent Capability Manager Foundation Slice

## Status

- Repository slug: `agent-capability-manager` — owner accepted
- Selected stack: Rust — owner accepted
- Repository creation: authorized for `C:/Projects/agent-capability-manager`
- Product implementation: authorized only for this disposable-root slice
- First slice: disposable-root transaction closure

## Why Rust Is Recommended

This product's hardest risk is not drawing a screen. It is changing local Agent
configuration without losing user state, stealing ownership, or leaving a
half-applied transaction. Rust makes invalid ownership and transaction states
harder to represent, avoids a garbage-collected runtime in the headless core,
and gives the later Tauri client a direct in-process path.

The practical cost is slower early coding and a steeper language curve. That
cost is acceptable here because the user values production-grade coverage over
the easiest implementation, the local machine already has a current Rust
toolchain, and the reviewed adjacent-manager ecosystem provides direct
Rust/Tauri precedent.

Go would make the first CLI faster to write and simpler for more contributors.
Its Wails and Bubble Tea path is credible. But Go is not installed on the
current machine, its desktop permission boundary would be more application-
defined, and building both prototypes would duplicate the very transaction
logic that needs one authoritative implementation. Go remains a fallback if
real delivery evidence later proves Rust friction unacceptable.

## First Vertical Slice

The first slice is not an empty scaffold or GUI mock. It proves one complete
transaction loop inside a generated disposable root:

```text
inspect -> classify ownership -> plan -> lock -> backup -> apply
        -> verify -> receipt -> rollback or recover
```

It defines artifact identities and digests, host targets, ownership states,
plans and preconditions, backup receipts, an append-only journal, verification
receipts, and rollback outcomes. The CLI emits canonical JSON so future TUI,
GUI, Agent, and CI clients cannot invent another policy path.

The implemented CLI always emits JSON; it does not require a separate
`--json` switch. Its commands bind the disposable root explicitly and use the
persisted transaction identifier for apply, verify, rollback, and recovery.

## Safety Boundary

The slice refuses any root without a generated disposable-test marker and any
root resolving into real user or project configuration. Foreign or unknown
ownership freezes writes. Apply requires an unchanged persisted plan, target
lock, backup, and journal. Verification failure attempts bounded rollback and
records both the original and rollback outcomes.

There is no network, account, telemetry, package installation, Hook mutation,
real Agent-home write, external candidate execution, cross-repository write,
commit, push, publication, or deployment in this slice.

## Acceptance

Tests must prove byte-for-byte rollback, drift rejection, foreign-owner
preservation, concurrency exclusion, idempotent recovery, core/CLI parity, and
failure recovery at every transaction boundary. Windows path, reparse-point,
case-folding, and locked-file fixtures fail closed.

Real Codex and other host adapters, Skill operations, the broader capability
graph, TUI, GUI, signing, updating, and cross-repository integrations are later
slices. Passing this foundation proves the transaction authority boundary; it
does not by itself prove the production MVP.

## Next Gate

The Rust route, necessary dependencies, new local repository, and this
disposable-root-only implementation slice are authorized. The next gate is
passing the complete foundation acceptance suite. Real Agent adapters and
configuration writes remain separately gated.

The dated local implementation and verification result is recorded in
`registry/agent-capability-manager-foundation-slice-implementation-evidence-2026-07-16.json`.
That evidence closes only this disposable-root foundation gate.
