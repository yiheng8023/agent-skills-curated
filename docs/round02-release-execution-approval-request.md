# Round 02 Release Execution Approval Request

Machine-readable request:
[`registry/round02-release-execution-approval-request.json`](../registry/round02-release-execution-approval-request.json).

Execution template:
[`registry/round02-approved-payload-routing-proposal-template.json`](../registry/round02-approved-payload-routing-proposal-template.json).

This is an approval request, not approval.

## Current State

```text
status: awaiting_owner_approval
approval recorded: false
approved payload diff allowed: false
release manifest update allowed: false
routing projection update allowed: false
generated projection update allowed: false
publication allowed: false
live install allowed: false
local runtime sync allowed: false
source text redistribution allowed: false
source asset redistribution allowed: false
dependency install allowed: false
credential use allowed: false
external media generation allowed: false
adapter runtime work allowed: false
```

Round-02 has release/admission disposition evidence for 16 candidates. This
request narrows the next possible GitHub-stage execution to only the 7
non-runtime candidates that can plausibly enter an approved-payload or merge
proposal.

## Included Candidates

- `obsidian-open-format-knowledge-files` as a possible standalone approved
  payload diff.
- `ai-shipping-governance` as a possible bounded merge into existing approved
  Skills.
- `product-execution-documents` as a possible bounded merge into existing
  approved Skills.
- `product-discovery-research-planning` as a possible bounded merge into
  existing approved Skills.
- `personal-document-and-copyediting-boundary` as a possible bounded merge
  into existing approved Skills.
- `design-direction-and-anti-slop-reference` as a possible bounded merge into
  existing approved Skills.
- `brand-asset-provenance-protocol` as a possible bounded merge into existing
  approved Skills.

## Excluded Candidates

- Adapter-only candidates remain excluded: `obsidian-cli-runtime-adapter`,
  `defuddle-tool-adapter`, `synthetic-data-and-sql-tooling`,
  `html-deck-animation-toolchain-boundary`, and
  `voiceover-tts-media-pipeline-boundary`.
- Reference-only candidates remain excluded:
  `data-analytics-runtime-equivalence`, `market-strategy-evidence-boundary`,
  and `legal-privacy-document-boundary`.
- The rejected bundled-asset candidate remains excluded:
  `bundled-assets-redistribution-boundary`.

## Requested Approval

The smallest useful approval phrase is:

```text
批准进入 Round-02 approved-payload/routing 提案阶段
```

or:

```text
Approve Round-02 approved-payload and routing proposal only
```

If approved, the next work may create a GitHub-only proposal that mutates
approved repository surfaces only as needed: approved Skill bodies, governed
registries, `release-manifest.json`, and deterministic generated projections.
The proposal must remain source-text-neutral, agent-neutral, public-safe,
dependency-free, and validation-backed.

## Explicitly Not Requested

This request does not ask permission to:

- install or sync live Agent environments;
- write to `C:\Users\15521\.codex\skills`;
- write to `C:\Users\15521\.agents\skills`;
- write to `C:\Users\15521\.cc-switch\skills`;
- publish a release outside GitHub repository commits;
- redistribute upstream source text as approved curated payload;
- redistribute upstream source assets as approved curated payload;
- install dependencies, use credentials, call TTS providers, or generate
  external media;
- execute adapter-only candidates or add their runtime dependencies;
- promote reference-only candidates into runtime behavior;
- reconsider rejected bundled assets without asset-level provenance review.

## Evidence That Must Exist After Approval

If the owner approves this request, the next record must include:

1. owner approval event record;
2. bounded payload and merge execution record;
3. before/after inventory, manifest, routing, and generated projection diff
   summary;
4. candidate-specific rationale for each included payload or merge change;
5. explicit record that adapter-only, reference-only, rejected, live install,
   local sync, source redistribution, asset redistribution, dependency,
   credential, and media actions remain excluded;
6. verification command results.

Until the approval event exists, Round-02 remains admission-reviewed but not
release-executed: no approved payload diff, manifest update, routing update,
generated projection update, publication, live install, or local sync may
occur.
