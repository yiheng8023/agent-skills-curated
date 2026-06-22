# Agent Skills Curated Repository Guidance

This repository is the authority for reviewed cross-agent Skill content,
provenance, adapters, recipes, audits, and generated capability topology.

Keep three governance layers distinct:

- An official, runtime-owned, or built-in Skill is represented only as
  external capability metadata when topology or conflict decisions need it. Its
  body must not be vendored and it must not enter this repository's release
  manifest by default.
- A third-party candidate must be source-pinned and pass license, provenance,
  security, portability, overlap, adaptation, and validation review. Until it
  is approved, it must not enter an execution path.
- A curated approved Skill is the only kind allowed in `skills/` and the
  release manifest. In schema 1, `registry/skills.json` is the approved release
  inventory: each payload Skill must have `status=approved`.

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
graph projections are derived projections, not independent truth.

The canonical router belongs to the consuming configuration/runtime layer. It
is a capability decision router, not a mandate to select a Skill. Its choices
may include native reasoning, an official or runtime-owned capability, a
curated Skill, external capability metadata, a recipe or DAG, human
confirmation, or no skill needed. Third-party candidates are never executable.
High-risk, ambiguous, conflicting, permission-changing, write, install,
delete, migration, publish, release, or rollback paths require the applicable
human confirmation.

This repository does not own user configuration, credentials, native memory,
runtime caches, Apps, Plugins, MCP account state, or installation authority.
`codex-user-config` may consume a pinned reviewed revision; this repository
does not install, does not write to `codex-user-config`, and does not write to a
live Agent environment.

Prefer small, reviewable intake batches. Verification must pass before any
content is marked approved. Installation, account connection, external writes,
or trust-boundary changes require the applicable user authorization.
