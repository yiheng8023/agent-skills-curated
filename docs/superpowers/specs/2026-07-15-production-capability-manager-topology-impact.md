# Production Capability Manager MERIDIAN Topology Impact Package

## Status

- Date: 2026-07-15
- State: owner accepted
- Design decision: revised written design accepted
- Repository creation authority: none
- Product implementation authority: none
- Cross-repository write authority: none
- Machine record: `registry/production-capability-manager-topology-impact-package-2026-07-15.json`
- Acceptance event: `registry/production-capability-manager-topology-acceptance-event-2026-07-15.json`
- Accepted repository slug: `agent-capability-manager`
- Slug decision: `registry/production-capability-manager-repository-slug-acceptance-event-2026-07-16.json`

## Accepted Decision

The owner accepted the proposed Manager as a separately released node in the
`YIYUAN-MERIDIAN` graph under the boundaries below. This acceptance settles
topology placement; it does not by itself authorize
repository creation, product implementation, Hook enablement, cross-repository
writes, commit, push, publication, or deployment.

## Current Truth Snapshot

The snapshot combines read-only local Git posture with authenticated GitHub
metadata. Local absence is not treated as remote absence, and a local checkout
is not treated as current merely because it exists.

| Node | Visibility | Current evidence | Role |
| --- | --- | --- | --- |
| `YIYUAN-MERIDIAN` | public | GitHub `main` `d0f3d57...`; no local checkout | public topology hub |
| `resource-radar` | private | GitHub `main` `11a9ae4...`; local `c54ba53...` without tracking | discovery and candidate projections |
| `resource-radar-public` | public | GitHub `main` `4dca7c5...`; no local checkout | public-safe radar pattern |
| `research-bookmarks` | private | GitHub `main` `461f28e...`; no local checkout | private bookmark source |
| `research-bookmarks-public` | public | GitHub `main` `a157128...`; no local checkout | public bookmark projection |
| `agent-skills-curated` | public | GitHub `main` `d0955bf...`; local `35ddb1e...`, ahead 12 before this transaction | reviewed Skill supply and abstract topology |
| `codex-user-config` | private | GitHub `main` `4dffc1c...`; local `addbe80...`, ahead 27 with unrelated `.tmp/` | private Codex consumer state |
| public config templates | public | current GitHub and local evidence recorded in machine package | public-safe consumer patterns |
| private user configs | private | current GitHub and local evidence recorded in machine package | live policy, backup, restore, and runtime integration |
| `YIYUAN-CALIBRATION` | private, outside MERIDIAN | local `6909081...` | temporary non-authoritative calibration |
| `YIYUAN-ASSETS` | private, outside MERIDIAN | local `f4f8df2...` | final carrier for separately admitted project standards |

## Proposed Node Boundary

The Manager should be a local-first operational control plane, not another
curation authority. It owns the headless application, local schemas and
migrations, user policy, profiles, experiments, runtime observations, adapter
contracts, transaction journals, backups, verification receipts, rollback,
and replaceable clients.

It does not own curated admission, provenance, release topology, radar truth,
bookmark truth, MERIDIAN topology authority, credentials, product accounts,
native memory, external accounts, or project hard-standard admission. Visible
official, runtime, Plugin, App, MCP, Agent, project, or user-installed
capabilities remain foreign-managed until explicit reversible opt-in.

## Proposed Graph Edges

```text
private bookmarks -> filtered seeds -> resource-radar
resource-radar -> non-executable candidate proposals -> agent-skills-curated
agent-skills-curated -> pinned reviewed release -> Manager
Manager -> preview/apply/verify/rollback -> opted-in local host targets
local hosts -> read-only observations and drift -> Manager
Manager -> separately reviewed public-safe feedback package -> curated/radar
YIYUAN-MERIDIAN -> public navigation and topology description -> Manager
```

The Manager may display radar or bookmark metadata, but those edges are never
execution eligibility. Only an exact curated revision and manifest digest,
compatible adapter, local user policy, explicit target authority, backup, and
verification can enter an apply path.

There is no direct runtime edge from `YIYUAN-CALIBRATION`. Any later ASSETS
relationship is project-owned and requires separate ASSETS admission plus a
separate Manager integration decision.

## Public And Private Boundary

The accepted shape is public code and public-safe contracts in the future
`agent-capability-manager` repository. User policy,
runtime inventories, account metadata, device paths, transaction journals,
backups, private experiments, credentials, and tokens remain local or private.
Telemetry stays off and the product has no account system.

## Actions, Versioning, And Release

The future Manager repository would own its build, schema migration tests,
unit/property/adapter tests, supply-chain checks, packaging, and release. It
would not receive a token that can write curated, radar, hub, or private user
configuration repositories during the first release.

`agent-skills-curated` continues to own curated manifests, topology,
provenance, and admission checks. Radar and bookmark repositories continue to
own their projections and privacy gates. `YIYUAN-MERIDIAN` continues to own
public navigation and topology validation.

The Manager application uses independent semantic versions. Local state has
explicit schema versions and tested migrations. Curated consumption pins an
exact commit and manifest digest rather than floating `main`. Adapter support
is declared and evidenced per host; no host inherits another host's proof.

## Acceptance, Rollback, And Retirement

Topology acceptance belongs to the MERIDIAN owner. Curated supply acceptance
belongs to `agent-skills-curated`. Local mutation belongs to the user who owns
the bound target. Host behavior claims belong to adapter-specific evidence.
Project standards belong to the project that admits them.

Local rollback requires locks, backups, crash-consistent journals,
post-rollback verification, and residue checks. Release rollback retains the
last compatible Manager and pinned curated release. Topology rollback removes
active navigation and consumption edges while retaining dated lineage.

If the headless application does not justify independent release, security,
migration, and maintenance ownership, the repository should be retired or
merged. Reusable governance returns to its owning repositories, user-owned
local state remains exportable, and no managed projection may be stranded.

## Required Future Topology Updates

After acceptance and separate write authorization, likely updates are:

- `YIYUAN-MERIDIAN`: repository map, system topology, roadmap, decision point,
  and verifier;
- `agent-skills-curated`: consumer/interface documentation only for accepted
  pinned-release and feedback edges;
- `resource-radar`: consumer contract only if direct non-executable Manager
  metadata is accepted;
- public templates: only after a generic public-safe integration exists;
- private consumer repositories: only through separate local transaction plans.

## Actual Drift And Limits

- The public hub still describes the older selected-Skills-MVP
  pause-and-observe snapshot and has no Manager node.
- Local and remote `resource-radar` revisions differ, with no local tracking
  relationship; neither is silently chosen as permanent topology truth.
- This repository is ahead of GitHub and contains this uncommitted design
  transaction.
- `codex-user-config` is ahead of GitHub and contains unrelated `.tmp/` state;
  it remains untouched.
- Several nodes have no local checkout; their current GitHub metadata and
  selected repository contracts are the available evidence.
- Implementation stack and exact cross-repository write batches remain
  undecided. The selected slug was collision-checked on 2026-07-16, but the
  search is not a namespace reservation and must be refreshed before creation.

## Remaining Owner Decisions

1. Accept the recommended Rust/Ratatui/later-Tauri stack or authorize a bounded
   Rust-versus-Go transaction-core prototype.
2. Separately authorize repository creation, the first implementation slice,
   and any cross-repository documentation transaction.
