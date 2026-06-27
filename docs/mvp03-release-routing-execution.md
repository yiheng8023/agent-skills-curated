# MVP-03 Release/Routing Execution

Machine-readable record:
[`registry/mvp03-release-routing-execution.json`](../registry/mvp03-release-routing-execution.json).

Source candidate review:
[`registry/mvp03-release-or-routing-candidate-review.json`](../registry/mvp03-release-or-routing-candidate-review.json).

This document records the owner-approved follow-up gate after MVP-03 candidate
review. It is not a new source intake, not public promotion, and not permission
to vendor official/runtime-owned Skills.

## Approval

```text
approval phrase: routing projection proposal、merge proposal、approved payload diff、manifest change 或 runtime install proof全部批准。
routing projection proposal allowed: true
merge proposal allowed: true
approved payload diff allowed: true
release manifest allowed: true
runtime install proof allowed: true
new source discovery allowed: false
official Skill vendoring allowed: false
public promotion allowed: false
source redistribution allowed: false
```

## Execution decisions

| Candidate | Review decision | Execution decision | Why |
| --- | --- | --- | --- |
| `spec-driven-development` | `recipe-routing-proposal` | routing projection approved | The useful pattern is lifecycle orchestration, not a standalone Skill body. It is modeled as `capability.spec-driven-development` plus `recipe.spec-driven-development` and scenarios. |
| `documentation-and-adrs` | `merge-into-existing-approved-skill` | approved payload merge | The useful material strengthens existing documentation authority and ADR boundary behavior in `grill-with-docs`. |
| `code-review-and-quality` | `merge-into-existing-approved-skill` | approved payload merge | The useful material strengthens risk-proportionate quality review behavior in `review`. |

## Boundary checks

- No candidate is added as a standalone approved Skill directory.
- Only existing approved Skill payloads are changed under `skills/`.
- `release-manifest.json` remains schema 1 and is regenerated from approved
  payload files only.
- Generated projections remain derived from registry sources.
- Runtime install proof belongs to the consumer repository after it pins the
  resulting curated revision.
- This gate does not discover new GitHub sources, import third-party source
  text, vendor official/runtime-owned Skills, publish a release, or promote
  public materials.

## Expected generated updates

- `generated/catalog.md`
- `generated/lifecycle-coverage.md`
- `generated/routing-index.json`
- `generated/routing-scenarios.md`
- `generated/routing-simulation-report.json`
- `generated/topology.json`
- `generated/topology.mmd`
- `release-manifest.json`

## Runtime install proof handoff

After this curated repository is committed and pushed, `codex-user-config`
should pin the exact curated revision, run its skills install and verification
workflow, and record the runtime install proof there. The dependency direction
remains one-way: `codex-user-config` consumes this curated revision; this
repository does not write back to live Agent environments.
