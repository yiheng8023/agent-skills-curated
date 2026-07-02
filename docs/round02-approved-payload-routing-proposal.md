# Round-02 Approved Payload And Routing Proposal

Registry record:
[`registry/round02-approved-payload-routing-proposal.json`](../registry/round02-approved-payload-routing-proposal.json).

Approval event:
[`registry/round02-approved-payload-routing-approval-events.json`](../registry/round02-approved-payload-routing-approval-events.json).

Owner approval phrase: `批准进入 Round-02 approved-payload/routing 提案阶段`.

## Scope

This is a GitHub-only approved-payload and routing proposal stage. It admits
one new approved portable Skill and merges bounded improvements into existing
approved Skill bodies. It does not install, sync, publish outside GitHub
commits, call external tools, install dependencies, use credentials, generate
media, or write local live Agent directories.

The admitted payload is the open-format Obsidian payload for portable
Markdown, JSON Canvas, and Bases files only.

## Payload Diff

- Added `skills/obsidian-open-format-knowledge-files/SKILL.md`.
- Added `github:kepano/obsidian-skills` to `sources/lock.json`.
- Added `sources/kepano-obsidian-skills/LICENSE`.
- Added the Skill to `registry/skills.json`, `registry/admissions.json`,
  `registry/capabilities.json`, `registry/relations.json`, `registry/routing.json`,
  and `registry/scenarios.json`.

The Skill is a source-text-neutral adaptation for Obsidian-compatible
Markdown, JSON Canvas, and Bases files. It excludes live Obsidian app control,
CLI invocation, plugin install, vault sync, webpage extraction, dependency
installation, and asset fetching.

## Merge Diff

Merged bounded improvements into existing approved Skills:

- `review`: intent fidelity, design-quality, and asset-provenance review axes.
- `shipping-and-launch`: intended-vs-implemented-vs-ready launch evidence and
  release/support-note checks.
- `to-prd`: product-discovery evidence state, job/scenario stories, and
  unresolved-question boundaries.
- `to-issues`: scenario-backed acceptance and release/support impact.
- `triage`: readiness checks for product-execution documents.
- `prototype`: design-direction and brand-asset provenance boundaries.
- `grill-with-docs`: product-discovery and personal-document sensitivity
  boundaries.

Deferred merge targets because they are not approved release inventory:
`design-an-interface`, `doc`, `edit-article`, `grill-me`,
`security-ownership-map`, and `writing-shape`.

## Exclusions

Still excluded:

- adapter-only candidates;
- reference-only candidates;
- rejected bundled assets;
- source text redistribution;
- source asset redistribution;
- dependency installation;
- credential use;
- external media generation;
- local runtime sync to Codex, agents, or cc-switch directories.

## Validation

Validation passed after rebuilding generated projections and the release
manifest, then running the repository command set recorded in the registry
execution record:

- `python -B scripts/build_topology.py`
- `python -B scripts/build_release_manifest.py`
- `python -B scripts/simulate_routing.py --report generated/routing-simulation-report.json`
- `python -B scripts/verify.py`
- `python -B scripts/build_topology.py --check`
- `python -B scripts/build_release_manifest.py --check`
- `python -B scripts/simulate_routing.py --all`
- `python -B -m unittest discover -s tests -v`

## Next Gate

After the GitHub repository state is committed and pushed, local runtime sync
requires a separate approval gate.
