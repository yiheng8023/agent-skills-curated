# Round 02 PM Market And Discovery Adaptation Gate

Machine-readable record:
[`registry/round02-pm-market-discovery-adaptation-gate.json`](../registry/round02-pm-market-discovery-adaptation-gate.json).

This is PM market and product-discovery adaptation gate evidence, not release approval.

## Current State

```text
status: pm_market_discovery_adaptation_gate_recorded_not_release_approved
source: github:phuryn/pm-skills
revision: a0cd730d4c61e519ca8568b172334402257a74a9
draft root: drafts/round02-pm-market-discovery-adaptation/
adapted draft allowed: true
approved payload allowed: false
release manifest allowed: false
routing projection allowed: false
live install allowed: false
local runtime sync allowed: false
source text redistribution allowed: false
```

This gate narrows the large PM source to two reviewed subsets:

- market, GTM, positioning, and strategy evidence boundaries;
- product discovery and research planning.

It explicitly excludes PM AI-shipping, execution documents, analytics,
script/tooling, and legal/privacy groups. Those require separate gates.

## Draft Decisions

| Candidate | Draft | Disposition | Reason |
| --- | --- | --- | --- |
| `market-strategy-evidence-boundary` | `drafts/round02-pm-market-discovery-adaptation/market-strategy-evidence-boundary/DRAFT.md` | `business-strategy-reference-or-recipe-candidate` | Competitive, positioning, market-sizing, and strategy workflows are useful, but they need dated-source, estimate, current-data, and advice boundaries before release. |
| `product-discovery-research-planning` | `drafts/round02-pm-market-discovery-adaptation/product-discovery-research-planning/DRAFT.md` | `product-discovery-merge-or-recipe-candidate` | Opportunity mapping, prioritization, dashboard design, and interview planning can broaden coverage, but they must separate hypotheses, research evidence, participant privacy, and product authority. |

## Boundary Checks

- `skills/` remains unchanged.
- `release-manifest.json` remains unchanged.
- Generated routing projections remain unchanged.
- Live Agent environments are untouched.
- Source text is not redistributed as approved curated payload.
- Local Codex/agents/cc-switch sync remains blocked.
- Adaptation drafts are not approved payload.
- Analytics, script/tooling, and legal/privacy PM groups remain outside this gate.

## Next Gate

Separate approval is required before any draft becomes approved Skill payload,
release-manifest entry, routing projection change, consumer install plan, local
sync input, publication artifact, redistributed source text, external research
workflow, participant-data handling workflow, or business-decision claim.
