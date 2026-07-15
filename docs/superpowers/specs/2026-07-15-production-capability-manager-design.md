# Production Capability Manager Design

## Status

- Access: Public-safe design direction
- State: Conversational design approved; written-spec review pending
- Date: 2026-07-15
- Current implementation authority: none
- Current repository: `agent-skills-curated`
- Proposed product boundary: a separately governed Manager application and
  repository, subject to a MERIDIAN topology-impact gate before creation

## Purpose

Build a local-first, production-grade external brain and capability manager
that lets users focus on creation and accountable decisions instead of manually
enumerating, screening, installing, updating, and reconciling large unknown
Skill inventories.

The product does not increase a model's capability ceiling. It improves the
path by which an Agent discovers, composes, applies, verifies, and retires
capabilities it can already exercise. Its core value requires real expansion
of governed human-AI collaboration coverage; wrapping the current release in a
new interface is not sufficient.

Skills are the first complete vertical slice because they are portable,
comparatively low burden, and able to carry instructions, resources, scripts,
and deterministic checks. The core artifact model remains general enough for
future instruction profiles, rule packs, recipes, adapters, and Hook policies.

## Binding Product Principles

1. **Real coverage growth:** the managed approved inventory must expand through
   evidence-backed demand, reuse-before-build comparison, external intake,
   adaptation, or repository authoring after a supported residual gap. Skill
   count is not the coverage metric.
2. **Local first:** core discovery from cached indexes, comparison, policy,
   planning, verification, and reversible local transactions work without a
   product account, GitHub login, or live GitHub Actions run.
3. **No product account system:** optional existing-service credentials remain
   under the owning service and local security mechanisms. The Manager does
   not become a credential custodian.
4. **User sovereignty:** no silent installation, upload, overwrite, permission
   expansion, forced update, telemetry, or ownership takeover.
5. **Headless core:** TUI, GUI, CLI, JSON, Agent, and CI clients share the same
   policy, transaction, and verification engine. A UI must not become a second
   business-logic implementation.
6. **Dual working modes:** ordinary-user and maintainer modes expose different
   detail and authority over the same governed state. They are modes, not
   forced permanent user identities.
7. **Single authority, controlled projections:** multiple physical
   `AGENTS.md`, `CLAUDE.md`, Skill, or adapter files may exist, but every copy
   is classified as authority, scoped extension, generated projection, live
   state, foreign-owned state, or cache.
8. **Dynamic metabolism:** discovery, updates, conflicts, drift, replacement,
   deprecation, migration, rollback, and retirement are first-class states.
9. **Production-grade delivery:** stable contracts, migrations, deterministic
   projections, supply-chain review, failure recovery, observability,
   compatibility, release discipline, and real-environment evidence are MVP
   requirements rather than later polish.
10. **Open-source reciprocity:** preserve attribution and licenses, record what
    was borrowed or changed, contribute generally useful improvements upstream
    when practical, and default to zero telemetry.

## Matrix And External Topology

`YIYUAN-MERIDIAN` remains the broader matrix and topology-control surface. The
bookmarks project, resource radar, community submissions, and public discovery
produce source signals. `agent-skills-curated` governs reviewed external Skill
content and its abstract topology. The proposed Manager consumes versioned
governance outputs and owns local user policy, experiments, projections,
transactions, observations, and rollback.

```text
bookmarks + resource radar + community and public discovery
                         |
                         v
                candidate source signals
                         |
                         v
               agent-skills-curated
 source pin -> review -> adaptation -> admission -> release graph
                         |
                         v
                independent Manager
 local policy -> experiments -> plans -> projections -> verification
                         |
                         v
       Codex / Claude / TRAE / WorkBuddy / other hosts
```

A new Manager repository changes the MERIDIAN graph. Repository creation is
therefore downstream of a topology-impact review that names:

- repository purpose and authority;
- upstream producers and downstream consumers;
- public/private status and data boundary;
- versioning and release relationship;
- GitHub Actions production and consumption edges;
- ownership of user policy, runtime observations, and transactions;
- acceptance and rollback responsibility;
- README, index, graph, and public projection updates;
- retirement or merge conditions if the new boundary proves unnecessary.

`YIYUAN-CALIBRATION` is not a MERIDIAN matrix node. It is an independent but
linked, principally temporary calibration and reference repository created to
support `YIYUAN-ASSETS` reshaping. Bounded standard-candidate packages are
intended for delivery there through separately authorized transactions.
`YIYUAN-ASSETS` is the intended final carrier for accepted project standards as
built-in mechanisms or knowledge.
Public-safe reusable lessons may return to MERIDIAN only through a separate
reviewed projection; no private product truth flows back automatically.

Human-AI collaboration shortfalls are general, not ASSETS-local. A standard
can therefore have universal semantic applicability while using different
host, project, and risk-specific projections. Storage location does not limit
applicability.

## Repository Authority Boundaries

### `agent-skills-curated`

Owns reviewed third-party Skill bodies, immutable source identity, license and
provenance, security and portability review, overlap decisions, adaptations,
approved release inventory, abstract capability topology, conflicts, recipes,
and lifecycle evidence.

It does not own user configuration, live installation, credentials, native
memory, Plugin/App/MCP state, or Manager-local policy and transactions.

### Proposed Manager repository

Owns the headless application, local schema and migrations, policy engine,
dual-mode clients, experiment orchestration, host-adapter contracts, local
transaction engine, runtime observations, and offline caches.

It consumes pinned governance outputs and must not become an alternate source
of curated admission truth. Its local database is operational state, not a
replacement for versioned shared governance.

### Consumer and project repositories

Own project-scoped policy, instruction extensions, hard standards, and
integration choices. A project may contain `AGENTS.md`, `CLAUDE.md`, or another
host carrier without becoming the universal authority for the underlying rule.

### Live host environment

Is authoritative only for what is actually visible, linked, loaded, invoked,
authorized, healthy, and changed at the observed moment. Filesystem presence,
an old transaction, or a generated index is not live health proof.

## Artifact Identity And Naming

Author identity and upstream names are immutable provenance. Neutralization
must not erase them. Names are not unique identifiers.

Every governed artifact records at least:

```text
artifactId        stable namespaced identity
sourceId          source owner/repository identity
sourcePath        upstream artifact path
sourceRevision    immutable inspected revision
contentDigest     inspected content identity
upstreamName      original author name, never overwritten
displayName       human-facing label
runtimeName       host projection name
aliases           historical and compatibility names
derivedFrom       typed lineage to upstream or combined sources
```

Light adaptation may retain the original display name with an explicit curated
adaptation label. A semantic rewrite, multi-source composition, or independently
authored artifact receives a new identity and typed `derivedFrom` edges.

Collision handling is explicit:

- same name and same content: deduplicate content while retaining every source
  and projection identity;
- same name and different content: retain separate IDs, record a conflict, and
  prohibit silent overwrite;
- different names with overlapping capability: record overlap or alternative
  edges;
- rename, fork, and replacement: preserve aliases and lineage such as
  `renamed-from`, `forked-from`, `supersedes`, and `superseded-by`;
- host copies and links: model as projections, not new source artifacts.

Only one winner may occupy a host runtime name in a controlled target. The
policy must select a source explicitly or generate a controlled alias. Unknown
or foreign ownership freezes automatic replacement.

## Dynamic State Model

One overloaded status is insufficient. State is factored into:

- governance: discovered, screened, reviewing, adapted, approved, rejected,
  quarantined;
- lifecycle: active, update-available, deprecated, superseded, retired;
- release: unpublished, release-candidate, published, withdrawn;
- projection: absent, planned, projected, drifted, rollback-blocked;
- runtime: unknown, visible, loaded, invoked, healthy, failed;
- freshness: current, upstream-changed, source-missing, version-unknown;
- trust class: official-reference, unreviewed-third-party, curated,
  project-authored-experimental, user-local, project-local, foreign-managed.

The shared governance layer uses append-only reviewed events and deterministic
materialized indexes. Manager-local state stores cache, user policy, device
observations, experiment runs, and transaction journals. Derived indexes and
graphs can be rebuilt from authoritative inputs and must not silently become a
second truth source.

The lifecycle is:

```text
discover -> pin -> classify -> review -> adapt/compose/reject
-> deterministic validation -> weak-floor and bounded live evidence
-> human admission -> publish -> user policy -> host projection
-> observe -> update/drift/conflict -> re-review
-> retain/replace/deprecate/retire
```

## Coverage And Skill Expansion

The current approved release is a seed and governance proof, not sufficient
coverage of human-AI collaboration shortfalls. MVP acceptance requires at
least one real expansion round that produces approved release growth beyond
the current inventory and improves named priority coverage coordinates.

Coverage is measured against a capability and collaboration graph, not by raw
Skill count. A coordinate may be satisfied by native behavior, an official or
runtime capability, a curated Skill, a composition, a deterministic mechanism,
a project standard, accountable human judgment, or an explicitly unresolved
gap. Ten overlapping Skills do not count as ten solved gaps.

The stable funnel remains:

```text
shortfall evidence -> current capability baseline -> targeted discovery
-> source-pinned representative review -> alternative comparison
-> supported residual gap -> adopt/adapt/compose/reject/author
-> admission -> release -> live evidence -> lifecycle feedback
```

External reuse is preferred. Repository-authored Skills remain allowed only
after a supported residual gap and the same provenance, ownership, security,
portability, overlap, testing, and approval discipline applied to external
content.

## Self-Authored Skill Semantic Design

Negative boundary, semantic modeling, and event-driven routing are design
dimensions, not mandatory templates for every Skill.

The current `intent-contract`, `capability-router`, and `closure-contract`
family uses a negative-boundary-first semantic model: preserve ordinary Agent
interpretation while defining what must not be inferred, authorized,
continued, routed, externalized, or declared complete without sufficient
evidence. It defines exclusion rather than enumerating the open world of every
allowed intent.

That model is especially suitable for intake gates, routers, closure gates,
authority transfer, and state transitions. Creative, exploratory, reference,
and constructive Skills may instead need positive goals, principles, and
output contracts with only the necessary safety boundaries. Samples and
failure evidence determine which model applies.

Event-driven reevaluation belongs at phase changes, new evidence, failures,
permission changes, capability switches, side-effect boundaries, and final
verification. It must not become keyword-only routing or a full decision
ritual at every atomic step.

## Headless Core And Clients

The headless core is the product authority for application behavior. It owns:

- artifact, source, event, graph, policy, and profile models;
- offline indexing, search, classification, and recommendation inputs;
- lifecycle transition and permission decisions;
- experiment design and result capture;
- projection compilation and host-adapter contracts;
- transaction planning, backup, atomic apply, verification, and rollback;
- migrations, audit records, and structured diagnostics.

Clients are replaceable projections:

- TUI: primary planned human client;
- GUI: retained candidate, selected by usability value rather than excluded by
  MVP ideology;
- CLI: scripting, CI, and advanced operation;
- JSON: first-class Agent and automation interface;
- future API: optional local service boundary, not a mandatory cloud service.

All clients call the same core. Client parity tests prevent the TUI, GUI, CLI,
or Agent path from bypassing policy and transaction controls.

## Dual Working Modes

Ordinary mode is intent-centered:

```text
state desired outcome -> inspect current native and managed capability
-> compare candidates and alternatives -> decide only material choices
-> preview transaction -> apply -> verify -> observe -> rollback if needed
```

Maintainer mode is lifecycle-centered:

```text
candidate inbox -> source pin -> automated review evidence
-> duplicate/conflict/graph analysis -> adaptation workspace
-> test matrix -> admission decision -> release -> update and retirement
```

The same person may switch modes. Admission and use remain separate auditable
decisions even when one person holds both authorities.

## Agent Profiles And Projection Control

Profiles support Agent, workspace, project, scenario, risk, source, lifecycle,
and temporary-session scope. A Skill exposure is not a simple promise that a
model will invoke it. The Manager distinguishes:

```text
desired policy -> materialized projection -> observed runtime state
```

Managed exposure states are:

- core: persistently projected and eligible for routing;
- on-demand: temporarily projected for a bound task or workspace;
- disabled: not projected by this Manager;
- blocked: prohibited by explicit security, conflict, or organization policy.

Default operation is non-invasive. The Manager modifies only artifacts and
targets explicitly placed under its control. Official, runtime, Plugin, App,
CC Switch, user-local, and other foreign-managed capabilities are observed and
classified but not silently hidden or replaced. An optional strict profile may
apply an allowlist only to the Manager-controlled surface.

## Distribution Modes

The product supports three explicit modes inspired by proven external
ecosystem patterns while adding governance and rollback:

1. **Editable copy:** the user receives a forkable copy and owns later edits.
2. **Managed subscription:** the body is read-only and follows separately
   reviewed upstream updates.
3. **Temporary projection:** the capability is exposed for a task, session, or
   workspace and can be removed after the bounded need ends.

Every mode preserves source, revision, digest, local delta, policy owner,
verification, and removal or rollback behavior.

## Automation And Human Authority

Safe, already-authorized, reversible, and locally verifiable preparation may
be automated: public metadata sync, update detection, hashing, classification,
static executable-surface inspection, duplicate and conflict detection, graph
proposals, deterministic test generation, approved read-only experiments,
transaction planning, and drift observation.

New source trust, new Skill admission, ambiguous license decisions, semantic
adaptation, conflicting runtime-name selection, third-party code execution,
new account or data access, permission expansion, destructive changes, Hook
enablement, publication, and withdrawal stop at an accountable human gate.

The first release never auto-admits a new source or Skill. A user may later
approve `auto-within-policy` for low-risk updates to an already admitted,
unchanged source identity. Repeated decisions may generate an automation-policy
proposal but do not silently expand authority.

## External Benchmarks And Open-Source Reciprocity

External research is a required anti-self-confirmation step. Useful mechanisms
are borrowed with pinned evidence and stated limits rather than copied as
universal answers.

- `mattpocock/skills`: small composable Skills, user/model invocation classes,
  lifecycle buckets, setup flows, managed versus editable distribution, and
  engineering release discipline;
- `vercel-labs/skills`: discovery, cross-Agent selection, lock/update behavior,
  interactive and non-interactive clients;
- `kevintsai1202/add-skill-installer`: concise staged interaction, retained as
  historical reference rather than current implementation authority;
- CC Switch: multi-root and symbolic-link projection evidence, with foreign
  ownership and rollback limitations preserved;
- Codex native tasks: current-host evidence for fresh-session observations,
  paired experiments, and background task orchestration without proving
  cross-host parity.

The Manager records an adoption ledger: source, author, revision, license,
borrowed mechanism, code versus idea boundary, local change, rejected aspects,
upstream issue or contribution, recheck date, and supersession state. General
improvements should be contributed upstream when practical. Security findings
use responsible disclosure.

Telemetry is off by default. Diagnostic bundles are locally generated,
previewable, redactable, and explicitly submitted. Disabling telemetry cannot
degrade core functionality.

## Transaction And Failure Model

Every managed write follows:

```text
plan -> diff preview -> authority check -> target lock -> backup
-> atomic apply -> post-apply verification -> committed journal
```

Failures close safely:

- unreachable upstream: use the last verified cache and mark it stale;
- unknown license or incomplete scan: keep the artifact non-executable;
- graph build failure: retain the last verified projection;
- unsupported adapter: produce a plan only;
- unverifiable host load: record `unknown`, never `enabled`;
- user-edited or foreign-owned target: freeze overwrite and automatic rollback;
- partial transaction or crash: recover from the journal and backup;
- flaky model evidence: remain unverified and repeat a bounded matrix;
- incompatible update: retain the pinned working version and reopen review.

The Manager uses per-target locks, crash-consistent journals, atomic file
replacement where supported, explicit residue checks, and idempotent recovery.

## Host Adapter Maturity

The model is host-neutral; claims are adapter-specific.

- Codex is the first full read/plan/apply/verify/rollback evidence target.
- common Agent Skills filesystem conventions may receive a bounded portable
  adapter after contract tests;
- Claude begins with source and live read-only mapping before write support is
  claimed;
- CC Switch is a foreign owner in the current evidence and remains read-only
  until an ownership and coexistence contract is accepted;
- TRAE, WorkBuddy, and other hosts remain discovery or read-only profiles until
  their loaders, precedence, configuration, and recovery are tested.

No adapter inherits another host's proof.

## Weak-Agent Floor And Harness Testing

Weak models or Agents are tested to preserve the collaboration floor under the
same strict conditions, not to reproduce the capability ceiling of the
strongest model. The required floor is:

- no fabricated authority or facts;
- no unbound source, target, or completion claims;
- no silent side effects or conflict overwrite;
- safe fallback or human escalation when insufficient;
- repository-truth recovery after interruption;
- minimum viable task and verification closure.

Strong models may design experiments, explore alternatives, and adjudicate
evidence. Candidate-gap work uses controlled escalation: weakest supported
model and lowest reasoning first, then change one variable at a time across
reasoning, model, explicitness, context carrier, adapter, or host. A failure is
classified before it becomes a capability-gap claim.

Every result records host, version, model, reasoning level, operating system,
source revision, profile, invocation mode, permission boundary, duration and
context proxies, outcome, and unknowns.

## Native Task And Agent Orchestration

The Manager reuses a host's native independent-task, background-Agent, or
delegation capability when available instead of rebuilding a proprietary
multi-Agent runtime. Native tasks may execute:

- fresh-context repository recovery observations;
- paired handoff and no-handoff experiments;
- implicit and explicit Skill-routing comparisons;
- independent source, security, portability, and overlap reviews;
- weak-model floor probes and stronger-model evidence adjudication;
- parallel read-only research that joins at an explicit reconciliation gate.

The parent task owns experiment design, variable isolation, evidence
reconciliation, and the final claim boundary. A child task result is an
observation, not automatic truth, acceptance, or completion evidence.

Host-native orchestration remains adapter-specific. The current Codex Desktop
observation proves that separately delegated project tasks can run against the
same local checkout; it does not prove another host has the same feature or
semantics. Shared `local` checkout tasks are read-only by default. Concurrent
write tasks require isolated worktrees or another verified workspace-isolation
mechanism, plus explicit branch and cleanup ownership. Model cost, context,
latency, cancellation, task residue, and user visibility are recorded as
experiment costs.

## Testing And Production Acceptance

The production baseline includes:

- schema, migration, property, and reference-closure tests;
- deterministic index, graph, manifest, and documentation projections;
- license, source, digest, collision, lineage, and lifecycle fixtures;
- disposable-home install, update, removal, and rollback tests;
- permission denial, file lock, partial write, crash, and residue injection;
- explicit/implicit, positive/negative/near-match semantic cases;
- fresh-task, handoff, interruption, and cross-review experiments;
- native child-task orchestration, result reconciliation, isolation, and
  residue tests;
- weak-floor and strong-adjudication behavior evidence;
- adapter contract suites without cross-host inference;
- reproducible build, dependency, release, and supply-chain checks;
- TUI/GUI/CLI/JSON client parity around the same core decisions.

Passing deterministic tests never proves live host behavior. A live pass is
scoped to its recorded environment and does not prove future or cross-host
parity.

## Standards, Historical Debt, And Restart Baselines

Repeated, counterexample-aware evidence may produce a versioned standard
candidate. When an accountable owner accepts a standard, it serves two roles:

1. settle affected historical debt;
2. define the verified starting point for later evolution.

Adoption triggers a graph-scoped revalidation cascade rather than a universal
big-bang rewrite:

```text
accepted standard -> affected-source and projection query
-> migration and revalidation set -> bounded remediation batches
-> verification -> new baseline -> old projection deprecation
```

The current project and necessary MERIDIAN links must be reshaped when an
accepted standard applies. Unaffected surfaces are not rewritten for ceremony.
Cross-repository mutation and ASSETS admission remain separately authorized.

## MVP Acceptance Boundary

The MVP is usable and production-grade, not a mock catalog. It requires:

- a production headless core with CLI and JSON interfaces;
- ordinary and maintainer workflows through a primary human client;
- TUI as the current planned client and a GUI decision based on bounded
  usability prototypes rather than a permanent exclusion;
- import of current real governance and approved release state;
- at least one complete new intake and admission round that expands the
  approved release and improves named priority shortfall coverage;
- a visible capability/shortfall graph with unresolved gaps preserved;
- source identity, classification, event history, graph, collision, update,
  supersession, and retirement behavior;
- non-invasive and strict managed profiles;
- editable, managed-subscription, and temporary distribution modes;
- Codex as the first fully verified adapter and honest maturity for others;
- local-first offline operation, no product accounts, and zero telemetry by
  default;
- transaction, recovery, rollback, and failure-injection evidence;
- weak-Agent floor evidence without relaxed safety conditions;
- native task orchestration for bounded experiments where a host supports it,
  with read-only sharing and isolated-write contracts;
- a topology-impact package before any new Manager repository is created;
- a standard-driven revalidation contract for later debt settlement.

The MVP does not require universal shortfall coverage, every host adapter, a
cloud service, automatic new-source admission, automatic Hook enablement, or a
final GUI decision.

## Explicit Non-Authorization

This design does not authorize creation of the proposed repository, third-party
code execution, installation, live environment mutation, Hook enablement,
cross-repository writes, standard promotion, GUI implementation, release,
remote push, or implementation work. Those actions require the approved
written spec, a topology-impact decision where applicable, an implementation
plan, and the relevant bounded authority.
