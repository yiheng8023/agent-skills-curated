# Agent Capability Manager Codex Read-Only Adapter Slice

## Goal

Add the first host-specific contract without crossing into a real Agent home:
inventory a marked disposable Codex fixture and preview a projection decision
without mutating the target or creating a durable transaction.

## Contract

The adapter is explicitly scoped to two fixture roots inside one
'DisposableRoot': 'codex-home' and 'shared-agent-home'. It reports stable host,
root, path, artifact class, digest, and ownership observations. A preview
returns only 'create', 'update-manager-owned', 'blocked-foreign', or
'no-change'.

Foreign or unknown ownership is observe-only. Preview cannot imply takeover,
persist a transaction, write an artifact, inspect the live user home, or touch
the current Hook.

## Test-First Tasks

1. Add failing core tests for deterministic inventory, ownership preservation,
   preview decisions, no mutation, and path escape rejection.
2. Implement the minimal Codex adapter contract on the existing headless core.
3. Add failing CLI tests for JSON output and direct-core parity.
4. Implement 'codex-inventory' and 'codex-preview' on the same adapter path.
5. Run the full locked test, format, Clippy, audit, deny, and governance gates.

## Stop Boundary

Stop after disposable-fixture evidence. Real Codex home reads, any adapter
apply/verify/rollback path, Hook inspection or mutation, TUI, GUI, commit, and
push remain separately gated.
