# Public / Private Boundary

`agent-skills-curated` is designed so reusable Skill governance can be public while personal runtime configuration stays private.

## Public-safe surfaces

Usually safe for a public repository:

- reviewed Skill bodies whose licenses permit redistribution;
- source pins, licenses, hashes, and provenance evidence;
- intake, security, portability, overlap, lifecycle, and release policies;
- registry schemas, topology, conflicts, recipes, and deterministic generated projections;
- release manifests for approved payloads;
- official/runtime capability baseline matrices that link or summarize without copying restricted content;
- candidate decisions that do not expose private user data.

## Private-only surfaces

Keep these out of the public repository:

- tokens, credentials, OAuth state, cookies, sessions, local caches, and account state;
- personal memory, raw private conversations, private assistant transcripts, and private user preferences;
- live Agent installation state and device-local paths unless intentionally documented as examples;
- private bookmarks or private resource overlays;
- third-party content without redistribution rights;
- leaked prompt archives or provenance-unsafe material as runtime content.

## User configuration repositories

A real user configuration repository may contain personal information,
preferences, memory snapshots, account assumptions, local restore policy,
installed-state notes, or private operational choices. It should remain
private unless deliberately sanitized. `codex-user-config` and
`claude-user-config` are current private examples, not the boundary of the
model.

The public-template pattern is generic in purpose: agent-environment migration,
cloud sync/backup, verification, restore, rollback, and runtime integration.
Concrete templates may still be agent-specific because each agent stores
different settings, memory, hooks, tools, MCPs, plugins, and account state.

If a public configuration example is useful, create a separate public template
such as `codex-user-config-template` or `claude-user-config-template` instead
of exposing the private repo. The public version should contain:

- generic directory structure;
- sample configuration with placeholder values;
- scripts or docs that explain how users create their own private config;
- explicit warnings about secrets, memory, preferences, local paths, and account state;
- guidance on why a private user-owned configuration repo is recommended.

The public template must not claim to be a live configuration, must not include the maintainer's personal settings, and must not be consumed as a source of truth by this curated Skill repository.

`open-resource-governance` may serve as the public-safe hub for explaining the
repository family, roadmap, promotion material, and public/private boundaries.
It does not own this repository's Skill bodies, intake decisions, release
manifests, or runtime installation.

## Declassification checklist

Before making the repository public, verify:

1. no secrets or personal configuration are tracked;
2. every vendored Skill has redistribution evidence;
3. source-available, proprietary, leaked, or unclear-rights material is reference-only or rejected;
4. release manifests include only approved payloads;
5. generated files are reproducible from registry truth;
6. README, CONTRIBUTING, SECURITY, funding, and sustainability documents are present;
7. the repository license has been explicitly chosen by the owner;
8. downstream consumers are described as private or separate consumers, not bundled public state.

## Relationship to resource-radar

`resource-radar` may suggest candidate sources. This repository owns Skill intake and release decisions. Radar output is advisory and cannot approve, install, release, or mutate curated content by itself.
