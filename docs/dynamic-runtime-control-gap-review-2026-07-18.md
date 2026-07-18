# Dynamic Runtime-Control Gap Review — 2026-07-18

## Current judgment

The observed MCP load problem is real enough to investigate, but it does not yet prove that a new Skill or Hook is required. Codex 0.144.5 exposes 13 currently enabled MCP entries in this task. Its CLI can list, get, add, remove, log in, and log out, but it has no dedicated enable/disable command and sampled plugin/runtime-visible names could not be addressed by `mcp get`.

Current OpenAI source at revision `2895d82b5e449407712439ba4f89954f3fa0c7e3` confirms useful startup controls: standalone and plugin-provided MCP servers have an `enabled` field, `enabled=false` skips initialization, and tool allow/deny lists can reduce the advertised surface. Plugins themselves also have an enable flag. The same source does not place MCP or plugin maps inside `ConfigProfile`, and this review found no proof of safe mid-session hot switching or unloading an already-running server.

The smallest current route is therefore native startup filtering first. A future Skill may decide which capability set a task needs; a future Hook may observe events or prepare an invocation. Neither should claim process-lifecycle control until Codex exposes a supported actuation and verification surface.

## Instruction-carrier versions

The portable version belongs here and stays product-neutral. It defines collaboration invariants, dynamic checkpoint contracts, `off`/`auto`/`on` Hook modes, verification, rollback, and safe degradation.

The private `codex-user-config` version may carry the owner's personal Codex paths, proactive branch/worktree and context preferences, real Hook wiring, and rollback procedures. The public consumer configuration should not become a third manually maintained authority. If public reuse later justifies it, publish a sanitized generated template with explicit provenance and non-authority wording.

## Research before authoring

The next evidence should compare disposable launches with baseline, MCP disabled, plugin MCP disabled, and tool-filtered configurations. Context management needs a separate runtime check for token, compaction, or handoff events; an `AGENTS.md` instruction alone cannot manufacture telemetry. No persistent configuration, Hook, or consumer repository was changed in this review.

Machine evidence: `registry/dynamic-runtime-control-gap-review-2026-07-18.json`.
