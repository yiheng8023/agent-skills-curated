# CC Switch Source-Preserving Skill Pool Strategy

Date: 2026-07-17
State: Owner accepted; current strategy
Machine decision:
`registry/cc-switch-source-preserving-skill-pool-strategy-acceptance-event-2026-07-17.json`

## Decision

Use CC Switch as the operational Skill manager and stop building a separate
production capability manager. The custom Manager design, topology package,
foundation, and disposable Codex preview remain historical experiment evidence;
they are not an active product roadmap.

The repository name and one shared directory are not the product boundary.
Every supported Agent may expose user-added Skills through its own paths and
loader behavior. Directory mapping belongs to consumer adaptation and
verification, not to the core curation strategy.

## Current Division Of Responsibility

- CC Switch owns operational source registration, installation, update
  detection, distribution, backup, and restore for supported Agents.
- This repository owns source intake evidence, safety and license review,
  quality and superiority comparison, overlap and redundancy decisions,
  shortfall coverage mapping, and the residual-gap decision.
- Each Agent or consumer configuration owns its instruction, Skill, Hook, and
  runtime paths plus live visibility verification.
- This repository remains the Agent-neutral, cross-Agent authority for shared
  Skills and portable chain contracts. It must not be consolidated wholesale
  into the Codex-specific `codex-user-config` consumer repository.
- `codex-user-config` owns only the Codex consumer adapter: user instructions,
  installation, runtime paths, Hook deployment, verification, and rollback.

## Source-Preserving Workflow

```text
broad discovery
-> metadata, license, provenance, and executable-surface preflight
-> exact upstream download into a non-active candidate pool
-> safety, quality, superiority, overlap, and redundancy review
-> unchanged admission through CC Switch after separate install authority
-> per-Agent visibility and chain verification
-> human-AI collaboration shortfall coverage mapping
-> repository authoring only for a reproducible residual gap
```

Third-party payloads remain byte-for-byte upstream content by default. A poor
or incompatible candidate is rejected or replaced instead of silently patched.
An adapted derivative is an exception that requires a proven residual need and
an explicit decision to accept a separate update lineage.

## Live Migration Reality — 2026-07-18

The strategy is a target contract, not proof that the pre-existing live pool
already satisfies it. A later read-only reconciliation found 43 shared-root
targets resolving into CC Switch: 42 have local database rows, zero have
source-backed rows, and one has no database row. The 19 legacy curated targets
exactly match this repository's current adapted release and do not yet have
CC Switch Git-source lineage.

Accordingly, strategy acceptance and operational reuse remain valid, while
live source-preserving completion is partial. Each existing target needs a
reviewed replace, explicit-derivative-retain, or retire disposition before any
separately authorized CC Switch migration.

Downloading is not execution, admission, installation, or trust. Candidate
content must remain outside active Agent Skill roots until preflight and review
have passed and installation is separately authorized.

## Chain And Path Contract

The portable narrow chain remains:

```text
Agent native capability
-> scoped instructions or rules
-> Skills
-> optional Hook
-> verification, feedback, and rollback
```

Every consumer adapter, including `codex-user-config`, must document for its
Agent:

- the `AGENTS.md` or equivalent instruction path and precedence;
- the Skill source, distribution, and runtime discovery paths;
- the Hook path, event, `off / auto / on` mode, authority, failure behavior,
  verification, and rollback.

The portable Hook policy and host-profile contract belong here; executable
installation and live state belong to the applicable consumer configuration.
No consumer configuration may silently replace the portable core authority.

## Manager Retirement

The local `agent-capability-manager` repository has no commits and no remote.
Its non-build source and documentation surface contained 18 untracked files
totalling 119,386 bytes. The much larger local footprint was disposable Rust
build output. After the governance rebaseline passed the full repository
verification set, the authorized exact path
`C:/Projects/agent-capability-manager` was deleted on 2026-07-17. A post-delete
path check returned absent; the pre-delete audit still recorded zero commits,
zero remotes, and zero tracked files.

Historical Manager artifacts keep their original names and evidence semantics.
They prove what was designed and tested at the time; they do not authorize or
require continued Manager development.

## Current Transaction Boundary

This strategy decision does not authorize Skill download or installation, CC
Switch configuration changes, Agent Home or Hook mutation, writes to
`codex-user-config`, commit, or push.
