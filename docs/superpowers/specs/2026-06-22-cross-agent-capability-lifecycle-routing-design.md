# Cross-Agent Capability Lifecycle Routing Design

## Status

- Access: Internal
- State: Approved direction, implementation pending
- Scope: `agent-skills-curated`, `codex-user-config`, and their live Agent integration
- Manifest compatibility: release manifest schema 1 remains unchanged

## Purpose

Build a complete software-engineering lifecycle capability system without
turning Skills into a duplicate implementation of Agent reasoning or official
runtime capabilities.

The system optimizes for complete capability coverage, not maximum Skill
count. A lifecycle capability may be satisfied by native Agent behavior, a
visible runtime or official capability, a reviewed third-party Skill, a
Recipe/DAG, an explicit human decision, or a declared gap. A Skill is admitted
only when it contributes a distinct, reusable, testable workflow beyond the
target Agent's native baseline.

## Binding Principles

1. Skills are instructions for Agents. They define goals, decision boundaries,
   workflow, artifacts, and validation; they do not replace Agent judgment.
2. Reviewed Skills must not duplicate native Agent capability. Generic advice,
   ordinary reasoning, basic file editing, and capabilities already supplied
   equivalently by the target Agent are not sufficient reasons for admission.
3. `agent-skills-curated` governs third-party Skill content only. Official,
   runtime-owned, built-in, or first-party Skill bodies and update authority
   remain outside the repository.
4. Capability routing considers the full materially relevant ecosystem:
   native capabilities, visible installed capabilities, connected tools,
   official/runtime surfaces, reviewed third-party Skills, and targeted
   discoverable-but-uninstalled options.
5. Uninstalled or disconnected capability is never represented as available.
   Discovery may recommend it, but installation, connection, broader access,
   cost, or trust-boundary changes remain separately authorized.
6. Unknown, ambiguous, conflicting, high-risk, or state-changing routes fail
   safely to native/no-Skill handling, a verified fallback, or human
   confirmation.

## Repository Authority Model

### `agent-skills-curated`

The curated repository owns:

- reviewed third-party Skill bodies;
- immutable source pins, license and provenance evidence;
- security, portability, overlap, native-increment, and validation evidence;
- abstract software-lifecycle capability taxonomy;
- mappings from approved third-party Skills to abstract capabilities;
- third-party conflict decisions and portable Recipes/DAGs;
- deterministic release evidence and generated projections.

It does not own or inventory official Skill bodies, runtime installations,
account state, plugin caches, user configuration, or live routing state.
Official/runtime capabilities may appear in dated overlap-review evidence, but
not as governed Skill records or canonical content owned by this repository.

### `codex-user-config`

The configuration repository owns:

- portable global routing invariants;
- capability decision policy;
- pinned consumption of curated third-party releases;
- installation planning, backup, verification, rollback, and live integration;
- platform-specific adapters and runtime probes;
- targeted discovery policy for visible and discoverable ecosystem options.

It consumes curated release evidence without taking ownership of third-party
Skill-body governance.

### Live Agent environment

The runtime is authoritative for what is actually visible, enabled, connected,
authorized, healthy, and callable in the current session. Repository state is
not proof of live availability.

## Two-Layer Non-Overlap Decision

### Admission-time portable baseline

Every third-party candidate is compared with a portable native baseline:

- general reasoning and synthesis;
- ordinary code, text, and file editing;
- following explicit instructions;
- basic planning, explanation, and summarization;
- normal tool use already exposed by the target Agent.

A candidate must document a concrete native increment. Acceptable increments
include a specialized repeatable procedure, a non-obvious safety discipline,
a stable artifact contract, a cross-step validation loop, or a portable
workflow that materially reduces failure across supported Agents.

Disposition rules:

- `approve`: distinct procedure with testable outputs and no unresolved owner
  conflict;
- `merge`: useful increments belong in an existing approved Skill;
- `recipe-only`: value comes from composing existing capabilities, not a new
  Skill body;
- `adapter-only`: value is limited to one runtime integration surface;
- `reject`: duplicates native behavior, official/runtime capability, or an
  existing reviewed workflow, or lacks maintainable evidence.

### Runtime environment arbitration

Even an approved third-party Skill is not automatically the best current path.
The Router compares it with the live environment. A native or official/runtime
capability wins when it provides equivalent or better correctness,
reliability, authority, safety, cost, and verifiability. The third-party Skill
is selected only when its distinct workflow remains materially useful.

## Lifecycle Capability Model

The topology models abstract capabilities rather than products. Initial
software-engineering lifecycle groups are:

1. discover and clarify: requirements clarification, ubiquitous language,
   stakeholder constraints, PRD/RFC;
2. plan and design: decomposition, architecture, interface/API design, data
   modeling, UX/product design, threat and privacy design;
3. implement: frontend, backend, data changes, dependency management, coding
   discipline;
4. verify: TDD, test strategy, functional and integration testing, code review,
   security, privacy, accessibility, performance;
5. deliver: CI/CD, release readiness, migration, rollout, rollback;
6. operate: observability, incident diagnosis and response, recovery,
   reliability and operational verification;
7. evolve: issue triage, documentation, knowledge capture, technical debt,
   deprecation, cross-Agent handoff, retrospective and long-term evolution.

Every lifecycle node records a coverage state:

- `curated`: an approved third-party Skill provides a distinct workflow;
- `recipe`: reviewed composition of capabilities provides coverage;
- `runtime-resolved`: the Router must select a visible native or runtime
  capability without the curated repository owning it;
- `native-sufficient`: explicit Agent instructions are sufficient and a Skill
  would duplicate native behavior;
- `human-authority`: the decision cannot be delegated safely;
- `gap`: no verified path currently exists.

Coverage completeness means every node has an explicit state, validation path,
and fallback. It does not mean every node has a Skill.

## Skill Routing Metadata

Registry metadata is a semantic contract for Agents, not a deterministic NLP
engine. Approved third-party Skill metadata should support:

- stable identifier, aliases, supported languages, and lifecycle mappings;
- positive triggers and negative/exclusion triggers;
- required context and preconditions;
- inputs, outputs, artifacts, side effects, and validation;
- risk and permission boundaries;
- native increment and overlap disposition;
- compatible Agent classes and environment requirements;
- conflicts, alternatives, fallback, and human-confirm conditions;
- provenance and review-evidence references.

Keywords and aliases improve retrieval but never decide alone. Numeric
confidence thresholds are avoided because model calibration differs across
Agents. Routing uses qualitative evidence:

- clear match plus satisfied context and low risk: select the minimal path;
- multiple complementary capabilities: select a Recipe/DAG;
- equivalent native/runtime path: prefer it and skip the Skill;
- negative trigger or missing context: exclude the Skill;
- ambiguous, conflicting, permission-changing, or high-risk path: ask for the
  smallest required human decision;
- unavailable preferred path: use a verified fallback or declare the gap.

## Capability Decision Router

The Router follows this decision sequence:

```text
goal and conversation context
-> abstract lifecycle capability classification
-> visible capability inventory and health
-> targeted ecosystem discovery only when materially needed
-> context, exclusion, overlap, risk, permission, and cost filtering
-> native | runtime/official | curated | Recipe/DAG | no Skill | ask user
-> execute within authorization
-> validate result and record material evidence
-> fallback or declare a gap
```

The Router must not require exact wording. It interprets Chinese, English,
mixed-language, colloquial, implicit, project-specific, and conversation-
referential expressions using Agent semantics plus explicit metadata. Metaphor,
irony, missing context, and unresolved references are treated as ambiguity, not
as permission to guess.

The global `AGENTS.md` remains a compact invariant layer. Detailed lifecycle
metadata belongs in registries and generated projections; detailed reusable
decision procedure belongs in `capability-router`; optional Hooks remain recall
aids and never become authority or a substitute semantic engine.

## Dynamic Ecosystem Awareness

At runtime, capability states are classified as:

- visible and callable;
- visible but disconnected, unauthorized, disabled, or unhealthy;
- discoverable but uninstalled;
- referenced historically but not currently discoverable;
- unknown.

The Router uses the platform-provided inventory first. It performs targeted
catalog or official-source discovery only for a material gap, a materially
weaker current path, likely ecosystem drift, or an explicit best-current-path
request. It never treats plugin caches, repository pins, or remembered state as
proof of availability.

## Verification Strategy

### Static contract verification

- registry and schema parity;
- lifecycle nodes all have a valid coverage state;
- approved Skills have native-increment and overlap evidence;
- candidate/external/official content cannot enter the release payload;
- relations, conflicts, Recipes, validation, and fallback references close;
- generated projections are deterministic.

### Scenario corpus

Portable routing scenarios cover:

- Chinese, English, and mixed-language requests;
- aliases, colloquial language, implicit intent, and long-context references;
- negative triggers and near-match false positives;
- native-versus-Skill overlap;
- visible versus discoverable-but-uninstalled capability;
- multiple complementary Skills and Recipe/DAG selection;
- ambiguous, conflicting, high-risk, permission, cost, and side-effect cases;
- missing context, unavailable preferred path, fallback, and declared gaps.

Tests assert decision class, exclusions, required confirmation, and validation
expectations. They do not require identical prose from different Agents.

### Live closure

Final closure requires:

1. merge the curated governance release to its authoritative branch;
2. pin that immutable reviewed revision in `codex-user-config`;
3. verify manifest and installer planning;
4. install updated global instructions, Router, and approved third-party Skills
   with backup and rollback evidence;
5. restart Codex or the target Agent surface;
6. confirm live file hashes and visible inventory;
7. run fresh-thread explicit and implicit routing probes;
8. run representative lifecycle, ambiguity, overlap, and authorization
   scenarios;
9. verify both repositories and remote state are clean and synchronized.

Repository tests alone cannot claim live closure.

## Migration And Compatibility

- Release manifest schema 1 remains stable.
- Registry evolution may introduce a new schema version, but existing approved
  payload paths and hashes change only through an explicit reviewed release.
- Generated files remain derived projections.
- The current 34 third-party approved Skills are reclassified against the
  native-increment rule before the next release; approval is not grandfathered.
- Official/runtime Skill bodies are not copied into the curated repository.
- Runtime discovery and installation remain configuration-side concerns.

## Completion Criteria

The work is complete only when:

- every lifecycle node has an explicit, justified coverage state;
- every approved third-party Skill passes native-increment, overlap, safety,
  portability, provenance, validation, and lifecycle mapping checks;
- no official/runtime Skill body is governed or released by the curated repo;
- Router policy considers all materially relevant visible and discoverable
  capability types without representing unavailable options as active;
- multilingual and ambiguity scenario contracts pass;
- curated release, configuration pin, live installation, hashes, restart, and
  routing probes are verified;
- both repositories are committed, pushed, clean, and synchronized.
