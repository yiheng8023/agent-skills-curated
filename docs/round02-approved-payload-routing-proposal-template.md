# Round 02 Approved Payload Routing Proposal Template

Machine-readable template:
[`registry/round02-approved-payload-routing-proposal-template.json`](../registry/round02-approved-payload-routing-proposal-template.json).

Template only, not approval.

This template defines how to run the Round-02 GitHub-only approved-payload and
routing proposal stage after the owner explicitly approves that gate. It does
not approve payload, manifest, routing, publication, local sync, source
redistribution, asset redistribution, dependency installation, credential use,
or media generation.

## When This Template May Be Used

Use this template only after one of the bounded approval phrases is recorded:

```text
批准进入 Round-02 approved-payload/routing 提案阶段
```

or:

```text
Approve Round-02 approved-payload and routing proposal only
```

Without that approval, this document remains scaffolding.

## Included Candidates

- `obsidian-open-format-knowledge-files`
- `ai-shipping-governance`
- `product-execution-documents`
- `product-discovery-research-planning`
- `personal-document-and-copyediting-boundary`
- `design-direction-and-anti-slop-reference`
- `brand-asset-provenance-protocol`

## Excluded Candidates

Adapter-only candidates, reference-only candidates, and the rejected bundled
asset candidate remain outside this execution template. They must not enter
approved payload, manifest, routing, generated projection, publication, live
install, local sync, source redistribution, asset redistribution, dependency
installation, credential use, or media generation.

## Required Execution Sections

Each future execution record must cover:

1. approval event;
2. candidate scope;
3. payload diff;
4. merge diff;
5. registry diff;
6. release manifest diff;
7. generated projection diff;
8. excluded candidate boundary;
9. source text boundary;
10. source asset boundary;
11. dependency, credential, and media boundary;
12. local runtime sync boundary;
13. validation results;
14. next gate.

## Fail-Closed Conditions

Stop the proposal if:

- owner approval for Round-02 approved-payload/routing proposal is missing;
- included or excluded candidate set differs from the approval request;
- a proposed Skill body copies upstream source text instead of using
  source-text-neutral adaptation;
- a merge diff creates conflicting triggers, duplicate workflow authority, or
  hidden runtime dependencies;
- a registry, manifest, or generated projection update is not explained by a
  bounded payload or merge diff;
- an adapter-only, reference-only, or rejected candidate enters approved
  payload, manifest, routing, generated projection, publication, live install,
  or local sync;
- source assets are copied, vendored, or redistributed;
- dependencies are installed, credentials are used, TTS providers are called,
  or external media is generated;
- local Codex, agents, or cc-switch directories are modified before a separate
  local runtime sync gate;
- validation commands are missing or fail.

## Output Contract After Approval

The future execution record must contain one entry per included candidate and
include:

- approval event id;
- candidate id;
- execution type;
- target files;
- rationale;
- diff summary;
- rejected alternatives;
- boundary assertions;
- validation results;
- next gate.

Until that record exists and passes verification, Round-02 remains
admission-reviewed but not release-executed.
