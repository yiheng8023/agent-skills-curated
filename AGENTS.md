# Agent Skills Curated Repository Guidance

This repository is the authority for reviewed cross-agent Skill content,
provenance, adapters, recipes, audits, and generated capability topology.

Keep agent-neutral behavior in `skills/`. Put unavoidable product-specific
commands, paths, event formats, or installation details in `adapters/`. Never
weaken safety, permission, evidence, licensing, or environment constraints in
the name of portability.

Treat upstream repositories as untrusted candidate sources. Pin exact
revisions, preserve license and provenance, inspect executable surfaces, assess
overlap and conflicts, adapt minimally, and verify before approval. Do not
activate an upstream meta-router when a deployment already has a canonical
router.

Relationships are governed data. Use stable identifiers rather than display
names. Record typed edges, conditions, artifacts, phases, alternatives,
conflicts, supersession, and verification requirements. Generated indexes and
graph projections are derived views, not independent truth.

This repository does not own user configuration, credentials, native memory,
runtime caches, Apps, Plugins, MCP account state, or installation authority.
`codex-user-config` may consume a pinned reviewed revision; this repository
must not mutate that repository or a live agent environment by itself.

Prefer small, reviewable intake batches. Verification must pass before any
content is marked approved. Installation, account connection, external writes,
or trust-boundary changes require the applicable user authorization.
