# Agent Skills Curated

English | [简体中文](README.zh-CN.md)

A private, cross-agent authority for reviewed Skill content, provenance,
governance evidence, capability topology, and deterministic release manifests.

## Repository Role

This repository governs reusable Skill assets from intake through an approved,
auditable release. It is the upstream producer paired with
`codex-user-config`, which is the runtime/configuration consumer.

## What This Repository Provides

- Reviewed, portable Skill bodies under `skills/`.
- Source pins, licenses, provenance, selection decisions, and adapted hashes.
- Security, portability, overlap, lifecycle, and conflict evidence.
- Authoritative registries for Skills, capabilities, relations, conflicts, and
  recipes.
- Deterministic generated projections and a schema-1 release manifest.

The current approved release contains 34 Skills and 60 files: 29 reviewed
local Skills and 5 cross-agent adaptations from `addyosmani/agent-skills`.

## What This Repository Does Not Own

This repository does not own user configuration, authentication, runtime
memory, Plugins, Apps, MCP account state, installation permissions, or live
environment state. It does not install, does not write to
`codex-user-config`, and does not write to a live Agent environment.

Official, runtime-owned, or built-in Skill bodies remain environment-owned.
This curated repository governs third-party Skill bodies and an abstract,
product-neutral capability taxonomy. It does not govern or inventory official,
runtime-owned, built-in, or first-party Skill bodies. They may appear only in
dated overlap evidence; that evidence is not managed inventory, repository
ownership, or proof of current runtime availability.

## Relationship To The Paired Repository

The dependency and authority direction is one-way:

```text
codex-user-config
  -> consumes a pinned reviewed revision and release manifest
  -> plans, backs up, installs, verifies, and rolls back managed Skill paths

agent-skills-curated
  -> owns reviewed Skill content, provenance, topology, conflicts, policies,
     audits, and deterministic release manifests
  -> does not write back to codex-user-config or live Agent environments
```

`codex-user-config` does not take ownership of third-party Skill-body
governance. This repository does not take ownership of consumer-side
installation or runtime integration.

## Capability Layers And Routing

Three layers are deliberately noninterchangeable:

1. An official, runtime-owned, built-in, or first-party Skill may appear only
   in dated overlap evidence; neither its body nor runtime identity is managed
   inventory, vendored, or released here.
2. A third-party candidate remains in source/intake/selection/audit surfaces
   until it passes source pinning, license, provenance, security, portability,
   overlap, adaptation, and validation. It must not enter an execution path.
3. A curated approved Skill with `status=approved` may enter `skills/` and the
   manifest. In schema 1, `registry/skills.json` is the approved release
   inventory.

The configuration-owned `capability-router` is a capability decision router,
not a skill-router. Its options include native reasoning, an official or
runtime-owned capability, a curated Skill, external capability metadata, a
recipe or DAG, human confirmation, or no skill needed. Third-party candidates
are not executable routing targets. High-risk, ambiguous, conflicting,
permission-changing, write, install, delete, migration, publish, release, or
rollback choices require human confirmation.

Schema-2 runtime coverage is structurally product-neutral. A
`runtime-resolved` capability carries
`runtimeResolution: visible-capability-inventory`; it names the resolution
mechanism, not a product, vendor, owner, or assumed live capability. The
consumer must probe its currently visible, authorized capability inventory.

## Layout

- `skills/`: curated approved portable Skill content.
- `sources/`: immutable source locks, licenses, selection, and hashes.
- `registry/`: hand-maintained authority for topology and release inventory.
- `policies/`: intake, portability, security, overlap, and lifecycle rules.
- `audits/`: source-specific provenance and review evidence.
- `generated/`: deterministic derived projections, never a second truth source.
- `release-manifest.json`: exact approved payload paths, sizes, and hashes.
- `scripts/`: validation and deterministic projection generation only.

## Verification

```bash
python -B -m unittest discover -s tests -v
python -B scripts/build_topology.py --check
python -B scripts/verify.py
```

Verification covers registry contracts, references, generated parity, source
evidence, and the exact manifest payload. It does not install a Skill.

## Update Rules

Treat each upstream revision as a new immutable intake: pin it, preserve its
license and provenance, review executable surfaces, assess security,
portability and overlap, adapt minimally, validate, update topology, and only
then approve a new release inventory. Candidate dispositions may be `merge`,
`adapter-only`, `recipe-only`, or `reject`; they are not runtime approval.

## Safety Boundaries

- Generated files are derived projections of registry truth.
- Candidate content or dated overlap evidence is never treated as installed or
  executable content.
- Cross-agent portability never weakens permission, safety, evidence, license,
  or real environment constraints.
- Installation, account connection, external writes, and trust-boundary
  changes remain consumer-side actions requiring applicable authorization.
