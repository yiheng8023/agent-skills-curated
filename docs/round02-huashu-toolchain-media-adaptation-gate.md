# Round 02 Huashu Toolchain Media Adaptation Gate

Machine-readable record:
[`registry/round02-huashu-toolchain-media-adaptation-gate.json`](../registry/round02-huashu-toolchain-media-adaptation-gate.json).

This is Huashu toolchain and media adaptation gate evidence, not release approval.

## Current State

```text
status: huashu_toolchain_media_adaptation_gate_recorded_not_release_approved
source: github:alchaincyf/huashu-design
revision: ec9ec0fff8a66a932c4049b200ea4c2b09f8d25b
draft root: drafts/round02-huashu-toolchain-media-adaptation/
adapted draft allowed: true
approved payload allowed: false
release manifest allowed: false
routing projection allowed: false
live install allowed: false
local runtime sync allowed: false
source text redistribution allowed: false
source asset redistribution allowed: false
dependency install allowed: false
credential use allowed: false
external media generation allowed: false
```

This gate narrows the Huashu source to three reviewed boundary subsets:

- HTML deck, animation, PDF/PPTX, and video export toolchain;
- voiceover, TTS, narration, and media generation pipeline;
- bundled assets redistribution boundary.

It explicitly excludes design-guidance candidates already handled by the separate design guidance gate.

## Draft Decisions

| Candidate | Draft | Disposition | Reason |
| --- | --- | --- | --- |
| `html-deck-animation-toolchain-boundary` | `drafts/round02-huashu-toolchain-media-adaptation/html-deck-animation-toolchain-boundary/DRAFT.md` | `toolchain-adapter-defer` | HTML deck, animation, browser export, and media rendering may be useful as a local adapter, but dependency install, Playwright execution, file export, and generated media boundaries require separate approval. |
| `voiceover-tts-media-pipeline-boundary` | `drafts/round02-huashu-toolchain-media-adaptation/voiceover-tts-media-pipeline-boundary/DRAFT.md` | `credential-cost-media-defer` | TTS and narration work touches provider credentials, cost, audio/video rights, and external service calls, so it stays outside approved payload. |
| `bundled-assets-redistribution-boundary` | `drafts/round02-huashu-toolchain-media-adaptation/bundled-assets-redistribution-boundary/DRAFT.md` | `do-not-vendor-before-asset-provenance-review` | The source assets tree is substantial. Repository-level MIT evidence does not automatically prove every bundled media file can be redistributed as curated payload. |

## Boundary Checks

- `skills/` remains unchanged.
- `release-manifest.json` remains unchanged.
- Generated routing projections remain unchanged.
- Live Agent environments are untouched.
- Source text is not redistributed as approved curated payload.
- Source assets are not redistributed as approved curated payload.
- Local Codex/agents/cc-switch sync remains blocked.
- Adaptation drafts are not approved payload.
- Huashu design guidance remains outside this gate.

## Next Gate

Separate approval is required before any draft becomes approved Skill payload,
release-manifest entry, routing projection change, consumer install plan, local
sync input, publication artifact, redistributed source text, redistributed
assets, installed toolchain, TTS request, credential use, dependency install,
or external media generation workflow.
