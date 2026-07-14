# Curation Harness Model

`agent-skills-curated` is a continuous curation harness for portable,
agent-neutral Skills. It is the first terminal MVP in a broader resource system,
not the whole upstream ecosystem, not a one-time collection task, and not a
claim that every useful resource should become a Skill.

## Position In The Larger Funnel

One known upstream entrypoint is `github:yiheng8023/YIYUAN-MERIDIAN`.
`resource-radar` and other upstream systems may discover broad GitHub resources,
including but not limited to Skills. Their candidate signals remain advisory.
This repository does not mutate upstream systems and does not treat upstream
discovery as approval.

The first complete vertical slice is:

```text
broader resource discovery
-> Skill candidate governance
-> reviewed Skill terminal release
-> consumer-owned projection
-> usage and failure feedback
-> revise, update, deprecate, retire, or extract a standard candidate
```

Skills are a useful first terminal because they have a low integration burden,
work across many Agent environments, and may contain guidance, resources,
templates, scripts, TypeScript, JavaScript, and validators. Executable payload
raises security, dependency, permission, and supply-chain requirements; low
integration burden is not permission to skip review.

Future terminals may include other governed capability or knowledge projections.
They can reuse broader discovery and governance evidence, but their bodies,
release decisions, runtime state, and authority do not automatically belong to
this repository.

## Harness Loop

The continuous loop is:

```text
discover
-> filter
-> review
-> adapt
-> verify
-> release
-> consumer-owned projection
-> feedback
-> rediscover, revise, supersede, deprecate, or retire
```

Every step can feed back into an earlier step. A consumer issue can force an
adaptation change. A security or license finding can change eligibility. A
community report can expose overlap. An upstream refresh can restart intake
without invalidating the last known-good release. Inventory count is not the
optimization target; maintained task coverage and reliable use are.

## Layered Collaboration Reliability

Instruction text is necessary but not sufficient across Agents with different
discovery, precedence, context, and instruction-following behavior. Use the
smallest sufficient sequence:

```text
instructions and rules
-> Skills and Recipes
-> scripts, schemas, and validators
-> consumer-owned Hooks, CI, or runtime controls
-> project-owned hard standards
-> evidence and accountable human decisions
```

The layers are not all mandatory for every task. Stronger mechanisms are added
only when evidence shows a material gap. Skills optimize discovery,
orchestration, and capability realization; they do not raise a model's native
capability ceiling. When a project has admitted a hard standard, conflicting
generic Skill guidance must defer to that project-owned authority.

## Multi-Agent Consumer Boundary

Codex and Claude are currently characterized examples, not universal runtime
models. Trae, WorkBuddy, cc Switch, and future consumers may use different
instruction names, Skill roots, precedence, built-in packages, plugin surfaces,
and restore behavior. Instruction surfaces may be named `AGENTS.md`,
`CLAUDE.md`, rules, or another runtime-specific form, and may exist at global,
project, nested-directory, plugin, or runtime-injected scopes. No mapping is
accepted from file or directory names or memory alone. Each consumer requires
dated official-source review, read-only local inventory, ownership
classification, and minimal behavior verification under its own authority
boundary.

This repository owns reviewed third-party Skill content and abstract topology.
Consumer configuration layers own installation, live inventory, backup,
restore, environment-specific adapters, and current availability claims.
They may also produce dated research, usage, failure, and validation evidence,
but they are not the durable authority or sole custody location for
cross-project research and standard candidates.

## Standard Candidate Boundary

Repeated external and self-built Skill evidence may expose a stable reusable
rule. This repository may package that evidence as a non-authoritative standard
candidate with provenance, scope, counterexamples, verification, versioning,
migration, and authority metadata. The intended custody flow is:

```text
consumer-side research, runtime evidence, and feedback
-> bounded standard candidate package
-> YIYUAN-CALIBRATION durable custody and calibration
-> YIYUAN-ASSETS project hard-standard admission decision
```

This repository does not itself admit or publish a CALIBRATION or ASSETS
standard. Writing a handoff package into another repository is a distinct,
separately authorized transaction. This transaction boundary must not be
misread as permission to leave research and standards indefinitely in a user
configuration repository.

## Delivery Standard

Accepted releases are treated as commercial delivery artifacts even though the
project is open source and community-driven:

- source and license evidence is traceable;
- security and portability review is explicit;
- acceptance criteria map to verification and evidence;
- deterministic checks cover the claims they make;
- release, rollback, update, deprecation, and retirement surfaces are clear;
- stage closeout exposes residual risks and deferred work.

There is no absolute completion state. The repository reaches versioned
stage-closeout states and continues the loop.
