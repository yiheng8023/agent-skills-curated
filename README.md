# Agent Skills Curated

English | [简体中文](README.zh-CN.md)

A public-safe, cross-agent authority for reviewed Skill content, provenance,
governance evidence, capability topology, and deterministic release manifests.

## Repository Role

This repository governs reusable Skill assets from intake through an approved,
auditable release. It is an agent-neutral producer for downstream consumer
configuration lanes. Codex and Claude are the currently characterized consumer
examples because they are the maintainer's active environments; they are not
the boundary of the model. Public readers should start from the public-safe
templates `codex-user-config-template` and `claude-user-config-template`,
which demonstrate a broader pattern for agent-environment migration, cloud
sync/backup, verification, and restore.

## What This Repository Provides

- Reviewed, portable Skill bodies under `skills/`.
- Source pins, licenses, provenance, selection decisions, and adapted hashes.
- Security, portability, overlap, lifecycle, and conflict evidence.
- Authoritative registries for Skills, capabilities, relations, conflicts, and
  recipes.
- Deterministic generated projections and a schema-1 release manifest.

The current approved release contains 20 Skills and 42 files: 5 reviewed
adaptations from `addyosmani/agent-skills`, 14 from `mattpocock/skills`, and
1 from `kepano/obsidian-skills`.
All have complete pinned Git provenance; the prior incomplete local baseline is
retained only as non-runtime historical evidence.

## Strategic Positioning

Reviewed Skills are the first terminal MVP in the broader `YIYUAN-MERIDIAN`
resource-governance funnel. They are a low-burden, cross-Agent entry point that
can carry guidance, resources, scripts, and deterministic checks for internal
and external consumers. They are not the only possible terminal and do not
constrain upstream discovery to Skills.

The repository is multi-domain. Human-AI collaboration shortfalls are one
evidence-backed demand lane, not the repository's whole mission. Its stable
operating rule is reuse before build: establish the demand, compare native,
official, runtime, single-Skill, composed-Skill, and other Harness alternatives,
then prove a residual gap before adapting or authoring anything. Discovery
volume, popularity, or an old draft is not gap evidence.

The intended external-brain outcome is decision-ready rather than inventory
heavy. Consumers should receive a small, governed set of routes, alternatives,
conflicts, evidence limits, and recheck signals instead of repeatedly
enumerating unknown Skills. This reduces selection, routing, context, and
maintenance burden so the human can concentrate on creation and decisions; it
does not claim to raise a model ceiling or prove identical behavior across
Agents.

The stable process is a dependency graph, not a mandatory linear conveyor:
consumer projection is an optional branch, lifecycle metabolism is
cross-cutting, and standards extraction is conditional on repeated evidence.
Upstream radar may discover broadly, while this repository requires bounded
demand, baseline, an exact source pin, review, and acceptance before a signal
can affect a curated decision. The current initiative remains pending owner
confirmation rather than being inferred from the historical Round 02 step.

Reliability is layered rather than text-only: instructions and rules may route
to Skills and Recipes; deterministic scripts, schemas, and validators cover
machine-checkable behavior; consumer-owned controls and project-owned hard
standards remain higher-authority integration surfaces. This repository may
extract traceable standard candidates from repeated governance evidence, but it
does not admit, publish, or install project hard standards. Consumer
configuration repositories are temporary consumption, validation, and feedback
surfaces for this purpose, not durable research or standards custody. Bounded
research and standard-candidate packages are intended for delivery to
`YIYUAN-CALIBRATION`; `YIYUAN-ASSETS` separately decides project hard-standard
admission.

The strategic objective-to-acceptance-to-verification-to-evidence mapping is
`registry/program-acceptance-map.json`. Partial or dated evidence remains
partial or stale; a green repository verifier does not prove current live Agent
state.

## What This Repository Does Not Own

This repository does not own user configuration, authentication, runtime
memory, Plugins, Apps, MCP account state, installation permissions, or live
environment state. It does not install, does not write to
private consumer configuration repositories such as `codex-user-config` or
`claude-user-config`, and does not write to a live Agent environment.
Cross-repository delivery to `YIYUAN-CALIBRATION` is therefore a separate,
explicitly authorized transaction rather than an implicit side effect of this
repository's verification or release workflow.

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
Current public reader entry points
  codex-user-config-template
  claude-user-config-template
    -> show public-safe structure, placeholders, and user-owned setup guidance

Current private consumer repositories
  codex-user-config
  claude-user-config
    -> may consume a pinned reviewed revision and release manifest
    -> plan, back up, install, verify, and roll back managed Skill paths

agent-skills-curated
  -> owns reviewed Skill content, provenance, topology, conflicts, policies,
     audits, and deterministic release manifests
  -> does not write back to private consumer configuration repositories or
     live Agent environments
```

The public templates do not contain the maintainer's private configuration,
memory, account assumptions, preferences, or local machine state. They are the
public way to understand the consumer-side pattern. The private Codex and
Claude configuration repositories are real downstream consumers, but ordinary
public users should not need access to them.

The consumer-side pattern is generic even when a concrete implementation is
agent-specific. Future agents or toolchains can add their own public template
and private overlay once their runtime files, settings, memory, hooks, tools,
permissions, and restore behavior have been mapped.

Consumer repositories do not take ownership of third-party Skill-body
governance. This repository does not take ownership of consumer-side
installation or runtime integration. Each consumer owns its own integration;
this repository stays agent-neutral and binds to none.

A real user configuration repository may contain personal information,
preferences, memory snapshots, account assumptions, local restore policy, or
private operational choices. It should remain private unless deliberately
sanitized. If a public configuration example is useful, create a separate
public template such as `codex-user-config-template` or
`claude-user-config-template`, with placeholders and user-owned setup guidance,
not a copy of the private repository.

The broader public-facing repository family is mapped through
`YIYUAN-MERIDIAN`. That hub can map this repository, `resource-radar`,
configuration templates, bookmark taxonomy repositories, and future terminal
lanes, but it does not own Skill release decisions, manifests, or runtime
installation.

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

A repository-authored gap-fill is a candidate origin, not a fourth release
layer and not a platform/runtime/vendor first-party baseline. It remains
non-executable until a material residual gap, alternative comparison, design
provenance and licensing, security, portability, overlap, validation, and owner
approval have all passed the same curated-admission boundary.

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
Codex and Claude are the first characterized consumer lanes, not the complete
set of possible consumers. Other agents' chains must be mapped as evidence
before this repository describes their install, routing, or restore behavior.
This repository names mechanisms structurally and stays agent-neutral, open,
and compatible — it must not hard-code any single agent's chain.

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
- `docs/mvp06-lifecycle-feedback.md`: lifecycle feedback from the verified
  consumer install, including radar dedupe metadata and the pause/observe
  decision before the next batch.
- `registry/program-acceptance-map.json`: stable strategic objective,
  acceptance, verification, and evidence relationships with honest current
  assessments.
- `docs/curation-program-plan.md`: machine-plan projection, strategic baseline,
  delivery lifecycle, and current stage-closeout reconciliation state.
- `docs/curation-harness-model.md`: continuous curation loop, first-terminal MVP,
  layered reliability, multi-Agent consumer, and standard-candidate boundaries.
- `docs/round-lifecycle-contract.md`: reusable plan, execution, acceptance,
  and stage-closeout contract for iterative curation rounds.
- `docs/round02-candidate-review-2026-07-02.md`: round-02 candidate-specific
  source disposition evidence; not approved payload, not manifest, not
  routing, and not local runtime sync.
- `docs/round02-obsidian-adaptation-gate.md`: Obsidian sub-batch adapted draft
  gate; records open-format, CLI, and Defuddle dispositions without approving
  payload, routing, manifest, or local sync.
- `docs/round02-pm-execution-adaptation-gate.md`: PM AI-shipping and
  execution-document adapted draft gate; excludes analytics, market/GTM,
  discovery, legal/privacy, and script/tooling groups for separate review.
- `docs/round02-pm-analytics-adaptation-gate.md`: PM analytics and data-safety
  adapted draft gate; records analytics runtime-equivalence and synthetic
  data/SQL tooling dispositions without approving payload, routing, manifest,
  execution, or local sync.
- `docs/round02-pm-market-discovery-adaptation-gate.md`: PM market and
  product-discovery adapted draft gate; records strategy evidence and discovery
  research dispositions without approving payload, routing, manifest, external
  research, participant-data handling, or local sync.
- `docs/round02-pm-toolkit-boundary-adaptation-gate.md`: PM toolkit
  high-boundary adapted draft gate; records legal/privacy reference and
  personal-document/copyediting dispositions without approving payload,
  routing, manifest, legal/compliance claims, resume data handling, or local
  sync.
- `docs/round02-huashu-design-guidance-adaptation-gate.md`: Huashu design
  guidance adapted draft gate; records design-direction and brand-asset
  provenance dispositions without approving payload, routing, manifest,
  toolchains, bundled assets, external media generation, or local sync.
- `docs/round02-huashu-toolchain-media-adaptation-gate.md`: Huashu toolchain
  and media adapted draft gate; records HTML deck/export, voiceover/TTS, and
  bundled asset redistribution boundaries without approving payload, routing,
  manifest, dependency install, generated media, asset reuse, or local sync.
- `docs/round02-release-readiness-review.md`: Round-02 GitHub-stage readiness
  review; summarizes all 3 reviewed sources and 7 sub-gates without approving
  release payload, routing, manifest changes, publication, or local sync.
- `docs/round02-release-admission-review-template.md`: template-only contract
  for a future Round-02 release/admission review after owner approval; not a
  candidate decision and not approval for payload, routing, manifest, install,
  publication, or local sync.
- `docs/round02-release-admission-approval-request.md`: formal request for the
  smallest approval needed to enter Round-02 release/admission review; now
  consumed by a bounded approval event and still blocks payload, manifest,
  routing, live install, publication, and local sync.
- `docs/round02-release-admission-candidate-review.md`: candidate-specific
  Round-02 release/admission disposition evidence; not approved payload, not
  manifest, not routing, not publication, and not local sync.
- `docs/round02-release-execution-approval-request.md`: formal request for the
  next GitHub-only approved-payload and routing proposal gate; excludes
  adapter runtime work, reference-only promotion, rejected assets, publication,
  live install, and local sync.
- `docs/round02-approved-payload-routing-proposal-template.md`: template-only
  execution contract for the future Round-02 approved-payload/routing proposal
  after owner approval; not release execution and not local sync.
- `docs/round02-approved-payload-routing-proposal.md`: owner-approved
  GitHub-only execution record that admits open-format Obsidian payload, merges
  bounded Round-02 improvements, updates routing/manifest/generated
  projections, and still blocks local sync.
- `docs/round02-local-runtime-sync-approval-request.md`: formal request for
  the smallest bounded approval needed to sync the validated Round-02 release
  payload into local cc-switch, agents, and Codex Skill directories; not sync
  approval and not a local write.
- `docs/round02-local-runtime-sync-execution.md`: recorded local runtime sync
  execution; aligns cc-switch hashes to the Round-02 manifest and records
  Junction fallback links for agents and Codex.
- `docs/starred-capability-source-discovery.md`: user-starred discovery surface
  triage for future candidate sources, baselines, indexes, and exclusions.
- `LICENSE`, `NOTICE`, and `THIRD_PARTY_NOTICES.md`: repository license,
  attribution, and third-party Skill notices.
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md`: public
  contribution, community, and vulnerability-reporting boundaries.
- `docs/license-policy.md`: layered licensing for repo-owned code, docs,
  generated projections, third-party Skill bodies, and official baselines.
- `docs/public-private-boundary.md`: public/private release boundary and user-config template guidance.
- `docs/sustainability.md`: cost posture, funding boundaries, and free-first discipline.
- `generated/`: deterministic derived projections, never a second truth source.
- `registry/routing.json` and `registry/scenarios.json`: approved routing
  metadata and the 105-case structured policy corpus.
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
evidence, the exact manifest payload, input-bound routing projection, all 27
lifecycle nodes, and 105 deterministic adversarial scenarios. Natural-language
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

## Public release posture

This repository is designed to be public-safe, but public visibility does not
weaken the release gates. Third-party redistribution boundaries, provenance,
private-overlay exclusion, and funding links remain owner-controlled release
decisions. Repository-owned code and governance machinery are Apache-2.0;
repository-owned documentation and public governance text follow the layered
policy in [`docs/license-policy.md`](docs/license-policy.md). GitHub Free is
sufficient for the current path; GitHub Team or Pro is only a future option if
private Actions minutes, organization governance, or team review needs require
it.
