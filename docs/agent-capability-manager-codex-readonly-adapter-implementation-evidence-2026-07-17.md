# Agent Capability Manager Codex Read-Only Adapter Evidence

Status: verified locally, uncommitted, disposable Agent Home fixtures only.

The Manager now exposes one Codex-specific read-only contract:

- deterministic inventory for 'codex-home' and 'shared-agent-home';
- instruction, Skill, Hook, Plugin, configuration, and other file classes;
- manager-owned versus foreign ownership observations;
- non-mutating 'create', 'update-manager-owned', 'blocked-foreign', and
  'no-change' previews;
- CLI/core parity through 'codex-inventory' and 'codex-preview'.

Forty integration tests pass on Rust 1.97.0 and the declared 1.93.1 minimum.
This includes six new adapter/CLI tests. Formatting, Clippy with warnings
denied, RustSec, cargo-deny, actionlint, and diff checks pass. Cargo.lock did
not change.

No real Agent home was read. No real Agent configuration was written. The
current Hook was neither read nor modified. Inventory and preview created no
durable transaction and changed no observed target. No commit, remote creation,
or push occurred.

This does not prove a real Codex adapter apply path or full host maturity.
