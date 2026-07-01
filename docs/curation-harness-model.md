# Curation Harness Model

`agent-skills-curated` is a continuous curation harness for portable,
agent-neutral Skills. It is not the whole upstream resource ecosystem and it is
not a one-time collection task.

## Position In The Larger System

This repository is downstream of broader resource-governance inputs. One known
upstream entrypoint is:

- `github:yiheng8023/YIYUAN-MERIDIAN`

That upstream entrypoint is recorded here only as a boundary. This repository
does not own `YIYUAN-MERIDIAN`, does not mutate it, and does not treat upstream discovery as approval. Upstream systems may provide candidates, but candidates
still enter this repository through the normal Skill curation gates.

This repository then becomes an upstream release source for downstream
consumers such as local Codex, agents, cc Switch, and future agent runtimes.

## Harness Loop

The loop is continuous:

```text
discover
-> filter
-> review
-> adapt
-> verify
-> release
-> consume-sync
-> feedback
-> rediscover-or-revise
```

Every step can feed back into earlier steps. A local runtime alignment issue can
force an adaptation change. A security finding can change review rules. A
community issue or pull request can add a new candidate, expose overlap, or
strengthen acceptance criteria. An upstream refresh can restart candidate
intake without invalidating the last released version.

## Delivery Standard

Although the repository is open source and community-cooperative, accepted
releases should be treated like commercial delivery artifacts:

- source and license evidence must be traceable;
- security and portability review must be explicit;
- acceptance criteria must map to the plan;
- repository verification must be deterministic;
- release and rollback surfaces must be clear;
- stage closeout must record residual risks and deferred work.

There is no absolute completion state. The repository reaches versioned
stage-closeout states, then continues the loop.
