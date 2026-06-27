# Agent Skills Curated

English | [简体中文](README.zh-CN.md)

A private, cross-agent authority for reviewed Skill content, provenance,
governance evidence, capability topology, and deterministic release manifests.

## Repository Role

This repository governs reusable Skill assets from intake through an approved,
auditable release. It is the agent-neutral upstream producer for downstream
consumer configuration repositories, currently including `codex-user-config`
and `claude-user-config`.

## What This Repository Provides

- Reviewed, portable Skill bodies under `skills/`.
- Source pins, licenses, provenance, selection decisions, and adapted hashes.
- Security, portability, overlap, lifecycle, and conflict evidence.
- Authoritative registries for Skills, capabilities, relations, conflicts, and
  recipes.
- Deterministic generated projections and a schema-1 release manifest.

The current approved release contains 19 Skills and 41 files: 5 reviewed
adaptations from `addyosmani/agent-skills` and 14 from `mattpocock/skills`.
All have complete pinned Git provenance; the prior incomplete local baseline is
retained only as non-runtime historical evidence.

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

Official Skills, capability packages, workflow templates, and similar public
capability bundles from Agent, runtime, platform, or tool ecosystems may be
recorded as dated official external capability baselines. Baselines are used
for coverage comparison, gap analysis, and routing calibration; they are not
managed inventory. This repository uses baseline matrices to decide
`covered`, `reference`, `adapt-candidate`, or `skip`; it does not blindly
import official repositories and does not claim full coverage until workflow,
resources, scripts, trigger description, and output standard have been checked.
The current first baseline instance is
`docs/anthropic-official-skills-coverage.md`.

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

The paired consumer side is not a single repository: `codex-user-config` and
`claude-user-config` both consume this repository as a downstream. Each owns
its own consumer-side integration; this repository stays agent-neutral and
binds to none.

A real user configuration repository may contain personal information,
preferences, memory snapshots, account assumptions, local restore policy, or
private operational choices. It should remain private unless deliberately
sanitized. If a public configuration example is useful, create a separate
public template such as `codex-user-config-template`, with placeholders and
user-owned setup guidance, not a copy of the private repository.

The broader public-facing repository family may be explained through
`open-resource-governance`. That hub can map this repository, `resource-radar`,
configuration templates, and bookmark taxonomy repositories, but it does not
own Skill release decisions, manifests, or runtime installation.

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

Routing is not only a task-entry decision. For multi-step work, consumers
should re-evaluate at event-driven reroute checkpoints: phase boundaries, new
context, failures or blockers, before side-effecting actions, before switching
capability classes, and before final verification. The routing projection
supplies deterministic policy input for those checkpoints; it does not require
per-step routing and does not prove live capability availability.

The `capability-router` is the Codex consumer's decision mechanism, not a
universal prerequisite. The invocation chain is consumer-agent-specific: for
example, Claude Code loads its instruction file every session and surfaces
Skills and MCP tools to the model directly, with no capability-router step.
Only Codex and Claude are characterized today; other agents' chains are not yet
mapped. This repository names mechanisms structurally and stays agent-neutral,
open, and compatible — it must not hard-code any single agent's chain.

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
- `docs/decisions/`: accepted governance decisions that constrain future
  contract changes.
- `docs/official-external-capability-baselines.md`: general policy for official
  external capability baseline handling.
- `docs/anthropic-official-skills-coverage.md`: dated external baseline
  coverage matrix for the first official baseline instance.
- `docs/mvp02-preflight-readiness.md`: historical MVP-02 preflight record now
  consumed by bounded owner approval.
- `docs/mvp02-post-approval-execution-plan.md`: executed plan for the narrow
  post-approval adapted-draft step; stopped before release or runtime gates.
- `docs/mvp02-adapted-draft-review.md`: non-runtime adapted draft review
  evidence; not approved payload, not routing, and not live install.
- `docs/mvp03-release-or-routing-preflight.md`: next-gate preflight and
  approval request; not release, routing, manifest, or runtime approval.
- `docs/mvp03-release-or-routing-review-template.md`: template-only candidate
  review contract to use after owner approval; not a candidate decision.
- `docs/mvp03-release-or-routing-approval-request.md`: formal owner approval
  request for MVP-03 candidate review; now consumed by a bounded approval
  event.
- `docs/mvp03-release-or-routing-candidate-review.md`: candidate-specific
  MVP-03 disposition evidence; not approved payload, not manifest, not routing,
  and not live install.
- `docs/mvp03-release-routing-execution.md`: owner-approved follow-up gate that
  merges two candidates into existing approved Skill payloads, models
  `spec-driven-development` as a recipe/routing projection, and hands runtime
  install proof to the consumer repository.
- `docs/starred-capability-source-discovery.md`: user-starred discovery surface
  triage for future candidate sources, baselines, indexes, and exclusions.
- `LICENSE`, `NOTICE`, and `THIRD_PARTY_NOTICES.md`: repository license,
  attribution, and third-party Skill notices.
- `docs/license-policy.md`: layered licensing for repo-owned code, docs,
  generated projections, third-party Skill bodies, and official baselines.
- `docs/public-private-boundary.md`: public/private release boundary and user-config template guidance.
- `docs/sustainability.md`: cost posture, funding boundaries, and free-first discipline.
- `generated/`: deterministic derived projections, never a second truth source.
- `registry/routing.json` and `registry/scenarios.json`: approved routing
  metadata and the 102-case structured policy corpus.
- `release-manifest.json`: exact approved payload paths, sizes, and hashes.
- `scripts/`: validation and deterministic projection generation only.

## Verification

```bash
python -B -m unittest discover -s tests -v
python -B scripts/build_release_manifest.py --check
python -B scripts/build_topology.py --check
python -B scripts/simulate_routing.py --all
python -B scripts/verify.py
```

Verification covers registry contracts, references, generated parity, source
evidence, the exact manifest payload, input-bound routing projection, all 26
lifecycle nodes, and 102 deterministic adversarial scenarios. Natural-language
interpretation remains an Agent responsibility; the simulator verifies the
normalized policy decision and does not pretend to be a keyword classifier.
It does not install a Skill.

## Update Rules

Treat each upstream revision as a new immutable intake: pin it, preserve its
license and provenance, review executable surfaces, assess security,
portability and overlap, adapt minimally, validate, update topology, and only
then approve a new release inventory. Candidate dispositions may be `merge`,
`adapter-only`, `recipe-only`, or `reject`; they are not runtime approval.

Official external capability baselines may be used for comparison, but the same
license, provenance, security, portability, overlap, and neutralization gates
apply before any adaptation. Source-available or all-rights-reserved official
content remains reference-only unless a separate permission path is approved.

User-starred repositories may seed discovery, but stars are not approval. A
starred source may become an official baseline, third-party candidate, discovery
index, external capability metadata, reference-only evidence, or rejection.
It must not enter `skills/`, the manifest, generated routing projections, or a
live execution path until the normal intake process closes.

`resource-radar` may suggest third-party Skill or capability sources. Those
suggestions remain advisory until this repository completes intake, review,
adaptation, validation, topology update, and release-manifest update.

## Safety Boundaries

- Generated files are derived projections of registry truth.
- Candidate content or dated overlap evidence is never treated as installed or
  executable content.
- Cross-agent portability never weakens permission, safety, evidence, license,
  or real environment constraints.
- Installation, account connection, external writes, and trust-boundary
  changes remain consumer-side actions requiring applicable authorization.

## Open-source readiness

This repository is private during development. Before making it public, the
owner must explicitly confirm repository visibility, funding links, third-party
redistribution boundaries, and private-overlay removal. Repository-owned code
and governance machinery are Apache-2.0; repository-owned documentation and
public governance text follow the layered policy in [`docs/license-policy.md`](docs/license-policy.md).
GitHub Free is sufficient for the current path; GitHub Team or Pro is only a
future option if private Actions minutes, organization governance, or team
review needs require it.
