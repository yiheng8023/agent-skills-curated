# Round 02 Huashu Design Guidance Adaptation Gate

Machine-readable record:
[`registry/round02-huashu-design-guidance-adaptation-gate.json`](../registry/round02-huashu-design-guidance-adaptation-gate.json).

This is Huashu design-guidance adaptation gate evidence, not release approval.

## Current State

```text
status: huashu_design_guidance_adaptation_gate_recorded_not_release_approved
source: github:alchaincyf/huashu-design
revision: ec9ec0fff8a66a932c4049b200ea4c2b09f8d25b
draft root: drafts/round02-huashu-design-guidance-adaptation/
adapted draft allowed: true
approved payload allowed: false
release manifest allowed: false
routing projection allowed: false
live install allowed: false
local runtime sync allowed: false
source text redistribution allowed: false
```

This gate narrows the Huashu source to two reviewed subsets:

- design direction and anti-generic-output guidance;
- brand asset provenance and permission discipline.

It explicitly excludes HTML deck, voiceover, and bundled asset toolchain candidates.
Those require separate gates.

## Draft Decisions

| Candidate | Draft | Disposition | Reason |
| --- | --- | --- | --- |
| `design-direction-and-anti-slop-reference` | `drafts/round02-huashu-design-guidance-adaptation/design-direction-and-anti-slop-reference/DRAFT.md` | `design-guidance-reference-or-merge-candidate` | Design-direction, variation, anti-generic-output, and review guidance is useful if made agent-neutral and separated from the heavy HTML/media pipeline. |
| `brand-asset-provenance-protocol` | `drafts/round02-huashu-design-guidance-adaptation/brand-asset-provenance-protocol/DRAFT.md` | `asset-provenance-reference-candidate` | Brand asset discipline is valuable only when framed around provenance, permission, official sources, placeholder honesty, and redistribution limits. |

## Boundary Checks

- `skills/` remains unchanged.
- `release-manifest.json` remains unchanged.
- Generated routing projections remain unchanged.
- Live Agent environments are untouched.
- Source text is not redistributed as approved curated payload.
- Local Codex/agents/cc-switch sync remains blocked.
- Adaptation drafts are not approved payload.
- Huashu toolchain and bundled assets remain outside this gate.

## Next Gate

Separate approval is required before any draft becomes approved Skill payload,
release-manifest entry, routing projection change, consumer install plan, local
sync input, publication artifact, redistributed source text, redistributed
assets, enabled toolchain, or external media generation workflow.
