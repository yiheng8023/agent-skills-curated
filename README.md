# Agent Skills Curated

[简体中文](README.zh-CN.md)

A private, cross-agent source of truth for reviewed Skill content, provenance,
overlap decisions, workflow relationships, security evidence, and deterministic
release manifests.

## Repository Role

This repository owns Skill bodies and their governance. It does not own user
configuration, authentication, runtime memory, Plugins, Apps, MCP account state,
or installation authority.

`codex-user-config` is the bootstrap authority and consumes one pinned reviewed
revision from this repository. The executable dependency is one-way:

```text
codex-user-config
  -> verify pinned curated revision and release manifest
  -> plan, back up, install, verify, or roll back managed Skill paths
agent-skills-curated
  -> own reviewed Skill content, provenance, topology, and release evidence
```

The Skills repository never writes back to the configuration repository or a
live Agent environment.

## Approved Inventory

The release contains 34 Skills and 60 files:

- 29 previously reviewed, adapted local Skills preserved with full content for
  cross-environment continuity;
- 5 cross-agent adaptations from `addyosmani/agent-skills`:
  `ci-cd-and-automation`, `deprecation-and-migration`,
  `observability-and-instrumentation`, `performance-optimization`, and
  `shipping-and-launch`.

All other upstream Skills have an explicit `merge`, `adapter-only`,
`recipe-only`, or `reject` decision. No upstream Hook, command adapter, persona,
script, CI workflow, marketplace manifest, or global router is installed.

## Overlap And Routing

Semantic overlap is allowed only when ownership is explicit. Each conflict
group has one default owner, scoped alternatives, and a written resolution in
`registry/conflicts.json`.

- `capability-router` remains the only global router.
- Curated `tdd`, `diagnose`, and `review` remain the general defaults.
- Plugin Skills are scoped to their explicit plugin workflows.
- Codex Security owns security scans; Product Design owns product-design work;
  Browser, Chrome, or Playwright own their actual runtime-control surfaces.

The repository does not install a third TDD, debugging, review, planning,
frontend, Git, security, or routing workflow.

## Dynamic Topology

Git-tracked registries are authoritative. `scripts/build_topology.py` produces:

- `generated/catalog.md`;
- `generated/topology.json`;
- `generated/topology.mmd`;
- `generated/routing-scenarios.md`.

Stable IDs survive renames. Typed relationships cover capabilities, ordering,
conditions, validation, collaboration, alternatives, fallbacks, conflicts, and
replacement. Recipes represent conditional multi-Skill DAGs. A graph database
may consume these generated projections, but it is not a second source of
truth.

## Source And Safety Boundary

Upstream content is untrusted candidate input. The Addy source is pinned to
commit `17214a29c429a19f7a9607f2c06f9d650ea87eb0`, with original/adapted hashes,
MIT notice, 24-item disposition map, security report, portability report, and
overlap report.

The initial release excludes all upstream executables. Security review found
risky optional Hook and CI surfaces; none are required by the five adopted
Skills. Cross-agent portability removes unnecessary product coupling, never
safety, permission, license, evidence, or real capability boundaries.

## Layout

- `skills/`: approved portable Skill content.
- `sources/`: immutable source locks, selection, licenses, and hashes.
- `registry/`: Skills, capabilities, relations, conflicts, and recipes.
- `policies/`: intake, portability, security, overlap, and lifecycle rules.
- `audits/`: source-specific provenance and review evidence.
- `generated/`: deterministic catalog and graph projections.
- `release-manifest.json`: exact installable files, sizes, and hashes.
- `scripts/`: validation and topology generation.

## Verify And Update

```bash
python scripts/build_topology.py --check
python scripts/verify.py
```

For an upstream update: pin a new commit, inspect the diff and executable
surfaces, rerun security/portability/overlap reviews, update every disposition,
adapt one Skill at a time, regenerate topology and hashes, and verify before
publishing a new immutable revision.

Installation and rollback are intentionally owned by `codex-user-config`.
