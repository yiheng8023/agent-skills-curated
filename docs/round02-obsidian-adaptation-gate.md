# Round 02 Obsidian Adaptation Gate

Machine-readable record:
[`registry/round02-obsidian-adaptation-gate.json`](../registry/round02-obsidian-adaptation-gate.json).

This is Obsidian sub-batch adaptation gate evidence, not release approval.

## Current State

```text
status: obsidian_adaptation_gate_recorded_not_release_approved
source: github:kepano/obsidian-skills
revision: a1dc48e68138490d522c04cbf5822214c6eb1202
draft root: drafts/round02-obsidian-adaptation/
adapted draft allowed: true
approved payload allowed: false
release manifest allowed: false
routing projection allowed: false
live install allowed: false
local runtime sync allowed: false
source text redistribution allowed: false
```

The current approved release inventory has no Obsidian-specific curated Skill.
Local runtime Skills such as a local `obsidian-vault` directory are not
repository release truth. This means the Obsidian open-format material cannot
be described as a merge into an existing approved Obsidian Skill.

## Draft Decisions

| Candidate | Draft | Disposition | Reason |
| --- | --- | --- | --- |
| `obsidian-open-format-knowledge-files` | `drafts/round02-obsidian-adaptation/open-format-knowledge-files/DRAFT.md` | `new-skill-draft-candidate` | Markdown, JSON Canvas, and Bases can form one bounded knowledge-file workflow, but it needs a separate release-or-routing review before any payload, recipe, routing, or manifest change. |
| `obsidian-cli-runtime-adapter` | `drafts/round02-obsidian-adaptation/obsidian-cli-runtime-adapter/DRAFT.md` | `external-runtime-adapter-defer` | CLI behavior depends on local Obsidian app state, installed CLI health, vault targeting, and mutation authority. |
| `defuddle-tool-adapter` | `drafts/round02-obsidian-adaptation/defuddle-tool-adapter/DRAFT.md` | `external-tool-adapter-defer` | Web extraction depends on an external CLI, outbound network access, and optional local file writes. |

## Boundary Checks

- `skills/` remains unchanged.
- `release-manifest.json` remains unchanged.
- Generated routing projections remain unchanged.
- Live Agent environments are untouched.
- Source text is not redistributed as approved curated payload.
- Local Codex/agents/cc-switch sync remains blocked.
- Adaptation drafts are not approved payload.

## Next Gate

Separate approval is required before any of these drafts become approved Skill
payload, release-manifest entries, routing projection changes, consumer install
plans, local sync inputs, publication artifacts, or redistributed source text.

The next useful Obsidian step is a release-or-routing review that decides
whether `obsidian-open-format-knowledge-files` becomes:

- a standalone curated Skill;
- a recipe component under knowledge capture;
- reference-only evidence;
- or a rejection if overlap and maintenance cost outweigh the value.
