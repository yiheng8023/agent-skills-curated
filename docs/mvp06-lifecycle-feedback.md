# MVP-06 Lifecycle Feedback

Machine-readable record:
[`registry/mvp06-lifecycle-feedback.json`](../registry/mvp06-lifecycle-feedback.json).

This record supports MVP-06 for the curated Skills terminal-consumer MVP. It is
not a completion claim for all future Skills, not a new source intake approval,
and not a public promotion decision.

## Runtime evidence summarized

The selected MVP batch was consumed by `codex-user-config` at:

```text
a89b61737f066118b13264510cb4dbe5566e2269
```

Public-safe runtime proof:

- install plan: 0 adds, 17 unchanged, 2 replacements, 0 retires;
- replaced curated Skills: `grill-with-docs`, `review`;
- routing index replaced and verified;
- 19 curated Skills verified;
- private transaction: `~/.agents/curated-skills-transaction.json`;
- private runtime details remain private.

## Lifecycle decisions

| Candidate | Runtime surface | Lifecycle state | Decision |
| --- | --- | --- | --- |
| `spec-driven-development` | `recipe.spec-driven-development` | accepted as recipe projection | keep active |
| `documentation-and-adrs` | `skill.curated.grill-with-docs` | accepted as merge into existing Skill | keep active |
| `code-review-and-quality` | `skill.curated.review` | accepted as merge into existing Skill | keep active |

No candidate in this batch is deprecated or retired in this lifecycle record.
No upstream repository is globally rejected by this record. The outcome only
deduplicates exact candidate reproposals for this selected batch.

## Resource radar feedback

The safe feedback for discovery is:

```text
source: github:addyosmani/agent-skills@17214a29c429a19f7a9607f2c06f9d650ea87eb0
dedupe action: suppress exact candidate reproposal for this batch
new source approval: false
official/runtime Skill vendoring: false
```

This lets discovery avoid resurfacing the same three candidates as if they were
unprocessed, without turning the entire upstream repository into approved
runtime payload.

## Generalizable lessons

- A useful upstream Skill does not always need to become a standalone curated
  Skill.
- Workflow-scale guidance can be safer as a Recipe that composes existing
  capabilities.
- Overlapping guidance should merge into existing approved Skills when that
  preserves trigger quality and avoids duplicate routing surfaces.
- Runtime install proof belongs in the private consumer repository; public
  records should summarize without exposing private runtime state.
- Future candidate batches need fresh source pin, review, approval, manifest,
  install, routing, and lifecycle evidence.

## Next step decision

The current decision is:

```text
pause and observe before the next batch
```

Reason: the selected small batch is installed and verified; more runtime
observation is preferable before expanding source intake or adding another
terminal consumer.

This does not block future work. It means:

- another curated Skills batch requires a new intake/review/approval gate;
- another terminal consumer requires a separate graduation gate;
- broad public promotion remains governed by the global closeout record.
