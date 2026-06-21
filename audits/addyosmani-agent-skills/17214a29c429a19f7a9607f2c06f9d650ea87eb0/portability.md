# Portability Review

The five adopted Skills contain no Claude, MCP-server, `.claude/`, `/mnt/`, or
hard-coded agent invocation assumptions. Their descriptions are trigger-only,
and they defer environment-specific browser, database, deployment, and security
operations to available specialized capabilities.

Commit, push, merge, release, deploy, production data change, secret access,
and rollback remain explicit external state transitions. No Hook, Bash script,
persona, command adapter, or upstream AGENTS policy is included in the approved
runtime set.

The existing local baseline is stored as content for cross-environment
continuity. Historical per-file provenance is explicitly incomplete and must be
reconstructed before any public redistribution.
