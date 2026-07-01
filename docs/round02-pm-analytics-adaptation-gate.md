# Round 02 PM Analytics Adaptation Gate

Machine-readable record:
[`registry/round02-pm-analytics-adaptation-gate.json`](../registry/round02-pm-analytics-adaptation-gate.json).

This is PM analytics and data-safety adaptation gate evidence, not release approval.

## Current State

```text
status: pm_analytics_adaptation_gate_recorded_not_release_approved
source: github:phuryn/pm-skills
revision: a0cd730d4c61e519ca8568b172334402257a74a9
draft root: drafts/round02-pm-analytics-adaptation/
adapted draft allowed: true
approved payload allowed: false
release manifest allowed: false
routing projection allowed: false
live install allowed: false
local runtime sync allowed: false
source text redistribution allowed: false
```

This gate narrows the large PM source to two reviewed subsets:

- analytics runtime equivalence;
- synthetic data and SQL tooling.

It explicitly excludes PM AI-shipping, execution documents, market/GTM
strategy, product discovery, and legal/privacy groups. Those require separate
gates.

## Draft Decisions

| Candidate | Draft | Disposition | Reason |
| --- | --- | --- | --- |
| `data-analytics-runtime-equivalence` | `drafts/round02-pm-analytics-adaptation/data-analytics-runtime-equivalence/DRAFT.md` | `runtime-equivalence-or-reference-candidate` | A/B testing, cohort analysis, and SQL query guidance may be useful, but it overlaps runtime analytics capabilities and needs explicit data, metric, denominator, SQL, and statistical-assumption boundaries. |
| `synthetic-data-and-sql-tooling` | `drafts/round02-pm-analytics-adaptation/synthetic-data-and-sql-tooling/DRAFT.md` | `tooling-or-reference-defer` | Synthetic data and generated SQL/script workflows are useful only when separated from real personal data, live databases, automatic execution, and unbounded file writes. |

## Boundary Checks

- `skills/` remains unchanged.
- `release-manifest.json` remains unchanged.
- Generated routing projections remain unchanged.
- Live Agent environments are untouched.
- Source text is not redistributed as approved curated payload.
- Local Codex/agents/cc-switch sync remains blocked.
- Adaptation drafts are not approved payload.
- Non-analytics PM groups remain outside this gate.

## Next Gate

Separate approval is required before any draft becomes approved Skill payload,
release-manifest entry, routing projection change, consumer install plan, local
sync input, publication artifact, redistributed source text, SQL execution,
script execution, or live database access.
