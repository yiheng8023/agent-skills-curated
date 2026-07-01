# Round 02 Candidate Review 2026-07-02

This is round-02 candidate review evidence, not release approval.

The review covers the pinned source-intake batch
`round02-source-intake-2026-07-02` from
`registry/source-intake-batches.json`:

- `github:kepano/obsidian-skills`
- `github:phuryn/pm-skills`
- `github:alchaincyf/huashu-design`

Current permissions:

- candidate review allowed: true
- approved payload allowed: false
- release manifest allowed: false
- routing projection allowed: false
- live install allowed: false
- local runtime sync allowed: false
- source text redistribution allowed: false

## Source Decisions

### github:kepano/obsidian-skills

Decision: split-adapt-candidates-not-approved.

The source has five detected Skill files at pinned revision
`a1dc48e68138490d522c04cbf5822214c6eb1202` under an MIT license. It is
useful for knowledge-work coverage, especially Obsidian-flavored Markdown,
JSON Canvas, and Bases. It is not safe to import directly.

Candidate decisions:

- `json-canvas`: adapter-or-merge-candidate. Useful open-format guidance, but
  local `.canvas` writes, ID generation, and JSON validation must stay bounded.
- `obsidian-markdown`: merge-or-adapter-candidate. Useful Obsidian-flavored
  Markdown guidance, but vault-only wikilinks, embeds, properties, and
  rendering assumptions must stay explicit.
- `obsidian-bases`: specialist-adapter-candidate. Useful `.base` YAML guidance,
  but this is Obsidian-specific and not a generic database or spreadsheet
  workflow.
- `obsidian-cli`: runtime-adapter-only-defer. It depends on a running Obsidian
  app, a selected vault, and commands that can mutate local files or inspect app
  state.
- `defuddle`: reference-or-tool-adapter-defer. It depends on a global npm CLI,
  network fetches, and optional local file writes.

### github:phuryn/pm-skills

Decision: split-into-sub-batches-not-approved.

The source has 68 detected Skill files at pinned revision
`a0cd730d4c61e519ca8568b172334402257a74a9` under an MIT license. It has broad
coverage across AI shipping, data analytics, execution, GTM, market research,
marketing growth, product discovery, product strategy, and toolkit workflows.
The size and domain spread make one-shot admission unsafe.

Sub-batch decisions:

- `pm-ai-shipping-group`: merge-or-recipe-candidate for review, launch,
  security, and shipping-artifact governance.
- `pm-data-analytics-group`: runtime-equivalence-or-reference-review because it
  overlaps with existing data-analytics capabilities and touches raw data,
  statistics, SQL, and scripts.
- `pm-execution-docs-group`: merge-into-existing-approved-skill-candidate for
  PRD, issue slicing, QA, release note, and launch workflows.
- `pm-gtm-market-strategy-group`: future-specialist-batch-candidate. It needs
  evidence boundaries, current market data handling, and commercial-advice
  caveats.
- `pm-product-discovery-group`: future-product-discovery-batch-candidate. It
  can broaden coverage, but duplicate brainstorming, interview, dashboard, and
  prioritization surfaces must be suppressed.
- `pm-toolkit-legal-privacy-group`: defer-or-reference-only. Legal/privacy and
  personal-document outputs need high-stakes boundaries before any admission.
- `pm-synthetic-data-and-script-group`: tooling-or-reference-defer. SQL,
  script, and synthetic-data generation must be separated from direct
  execution, sensitive data, and database mutation.

### github:alchaincyf/huashu-design

Decision: reference-and-adapter-candidate-not-approved.

The source has one top-level `SKILL.md` at pinned revision
`ec9ec0fff8a66a932c4049b200ea4c2b09f8d25b` under an MIT license. It contains
useful design workflow guidance, anti-slop review patterns, HTML prototype
rules, deck and animation workflow guidance, and asset discipline. It also
contains a large toolchain and media surface, so direct import is not the right
move.

Candidate decisions:

- `huashu-design-principles`: reference-or-merge-candidate for
  `design-an-interface`, `prototype`, and review workflows after
  neutralization.
- `huashu-brand-asset-protocol`: reference-candidate-with-copyright-boundary.
  The brand asset discipline is useful, but logo/image acquisition and
  redistribution must be bounded.
- `huashu-html-deck-animation-pipeline`: adapter-candidate-defer. Browser
  automation, scripts, export, and bundled assets need a separate toolchain
  review.
- `huashu-voiceover-tts-pipeline`: defer-high-boundary-toolchain because TTS,
  generated audio, environment configuration, cost, and media-rights boundaries
  need separate review.
- `huashu-bundled-assets`: do-not-vendor-before-asset-provenance-review.

## Boundary Checks

- `skills/` remains unchanged.
- `release-manifest.json` remains unchanged.
- Generated routing projections remain unchanged.
- Live Agent environments are untouched.
- Source text is not redistributed as approved curated payload.
- Local Codex/agents/cc-switch sync remains blocked.
- Candidate decisions are not approved payload.

## Next Gates

Separate approval is required for any adapted payload diff, release-manifest
update, routing projection update, consumer install, local sync, publication,
or source redistribution.

The next practical work is to split round-02 into smaller review/adaptation
sub-batches:

1. Obsidian open-format and vault adapter review.
2. PM execution and AI-shipping merge review.
3. PM analytics runtime-equivalence review.
4. PM market, strategy, and product-discovery specialist review.
5. Huashu design-guidance reference/merge review.
6. Huashu toolchain, asset, and media boundary review.
