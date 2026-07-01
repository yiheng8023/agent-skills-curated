# Round 02 PM Execution Adaptation Gate

Machine-readable record:
[`registry/round02-pm-execution-adaptation-gate.json`](../registry/round02-pm-execution-adaptation-gate.json).

This is PM AI-shipping and execution-document adaptation gate evidence, not
release approval.

## Current State

```text
status: pm_execution_adaptation_gate_recorded_not_release_approved
source: github:phuryn/pm-skills
revision: a0cd730d4c61e519ca8568b172334402257a74a9
draft root: drafts/round02-pm-execution-adaptation/
adapted draft allowed: true
approved payload allowed: false
release manifest allowed: false
routing projection allowed: false
live install allowed: false
local runtime sync allowed: false
source text redistribution allowed: false
```

This gate narrows the large PM source to two reviewed subsets:

- AI-shipping governance;
- product execution documents.

It explicitly excludes PM analytics, market/GTM strategy, product discovery,
legal/privacy toolkit, and script/tooling groups. Those require separate gates.

## Draft Decisions

| Candidate | Draft | Disposition | Reason |
| --- | --- | --- | --- |
| `ai-shipping-governance` | `drafts/round02-pm-execution-adaptation/ai-shipping-governance/DRAFT.md` | `merge-or-recipe-candidate` | The intended-state versus implementation review axis and shipping-document map can strengthen review and launch workflows without becoming a duplicate standalone Skill. |
| `product-execution-documents` | `drafts/round02-pm-execution-adaptation/product-execution-documents/DRAFT.md` | `merge-into-existing-approved-skill-candidate` | PRD, story, test scenario, and release-note guidance should strengthen `to-prd`, `to-issues`, `triage`, and `shipping-and-launch` rather than create parallel template Skills. |

## Boundary Checks

- `skills/` remains unchanged.
- `release-manifest.json` remains unchanged.
- Generated routing projections remain unchanged.
- Live Agent environments are untouched.
- Source text is not redistributed as approved curated payload.
- Local Codex/agents/cc-switch sync remains blocked.
- Adaptation drafts are not approved payload.
- Excluded PM groups remain unreviewed by this gate.

## Next Gate

Separate approval is required before any of these drafts become approved Skill
payload, release-manifest entries, routing projection changes, consumer install
plans, local sync inputs, publication artifacts, or redistributed source text.
