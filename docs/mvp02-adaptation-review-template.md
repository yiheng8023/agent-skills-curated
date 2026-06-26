# MVP-02 Adaptation Review Template

Template only, not adapted output.

Do not use this template as approval. It defines the evidence structure for a
future adapted-output review after the MVP-02 transition gate has explicit
human approval.

Machine-readable checklist:
[`registry/mvp-adaptation-review-checklist.json`](../registry/mvp-adaptation-review-checklist.json).

## Boundary

This template does not:

- create adapted Skill text;
- approve any candidate;
- edit `skills/`;
- update `release-manifest.json`;
- update generated routing projections;
- install or sync a live Agent environment;
- authorize upstream source text redistribution.

Fail closed if any required section is missing, if source integrity changes, if
license/provenance posture is unclear, or if the adapted draft attempts to
skip release, routing, runtime, or human-approval gates.

## Review record header

| Field | Value |
| --- | --- |
| Candidate id | |
| Source id | |
| Source revision | |
| Upstream path | |
| Upstream SHA-256 | |
| Adapted draft location | |
| Reviewer | |
| Review date | |
| Approval state | |

## Source integrity

Record:

- source id;
- source revision;
- candidate upstream path;
- candidate upstream SHA-256;
- whether the adapted draft derives only from recorded source evidence.

Fail closed if source revision, upstream hash, or source path differs from the
recorded pre-adaptation review without a new review record.

## License and attribution

Record:

- license posture;
- attribution text;
- redistribution posture;
- whether upstream text was copied, paraphrased, summarized, or rejected.

Fail closed if attribution, license, provenance, or redistribution posture is
unclear.

## Security

Record whether the draft removes or bounds:

- side-effecting instructions;
- dangerous command guidance;
- secrets, credentials, private paths, and account assumptions;
- external service assumptions;
- installation, deployment, release, rollback, or deletion authority.

Fail closed if the draft can mutate state beyond the active user-approved
scope.

## Portability and neutralization

Record:

- agent-specific names neutralized;
- vendor-specific paths neutralized;
- project-specific command examples bounded as examples only;
- language, operating-system, package-manager, and runtime assumptions made
  conditional;
- no limitation to Codex, Claude, or any single runtime unless explicitly
  scoped.

Fail closed if the draft turns a tool-specific habit into a universal rule.

## Overlap and conflict

Compare against:

- existing curated Skills;
- existing recipes;
- official or runtime-owned capabilities as external baselines;
- conflict groups;
- native or no-skill routes.

Record why the chosen outcome is better than alternatives.

Fail closed if overlap with an existing Skill, recipe, native path, or
runtime-owned capability remains unresolved.

## Routing and runtime boundary

Record whether the candidate should become:

- a merge into an existing Skill;
- a recipe-only update;
- an adapter-only record;
- a routing scenario;
- an approved-payload candidate;
- a rejection record;
- no runtime artifact.

Also record:

- positive trigger implications;
- negative trigger implications;
- human-confirmation requirements;
- fallback or native path.

Fail closed if the draft would make Skills mandatory for simple, low-risk, or
native-sufficient tasks.

## Validation

Record:

- focused checks run;
- repository verification command results;
- whether manifest, routing, and live install remain unchanged unless
  separately approved;
- known limitations.

Fail closed if validation cannot distinguish candidate material from approved
runtime material.

## Disposition

Choose exactly one candidate-specific disposition:

- merge into existing curated Skill;
- recipe-only;
- adapter-only;
- reject;
- approved-payload candidate for a later release gate.

Record:

- decision rationale;
- next gate;
- reviewer role;
- public-safe summary.

Fail closed if the disposition implies release, routing, or runtime use without
the later MVP gates.

## Candidate-specific prompts

### `spec-driven-development`

- Should useful content merge into PRD, issue, TDD, and review guidance, or
  become a recipe only?
- Which upstream Skill references must be replaced by existing curated Skills,
  recipes, or native reasoning?
- Which command examples must remain repository-local examples rather than
  defaults?

Forbidden shortcuts:

- do not create a duplicate spec Skill without proving non-overlap;
- do not make implementation proceed without active repository authority;
- do not treat upstream references as runtime dependencies.

### `documentation-and-adrs`

- Which ADR lifecycle rules are portable enough for curated guidance?
- Which documentation rules belong in repository-local standards instead of a
  Skill?
- How should historical context, current authority, and archived notes remain
  distinct?

Forbidden shortcuts:

- do not preserve Claude-specific file names as universal rules;
- do not turn stack-specific examples into defaults;
- do not make generated documentation a second truth source.

### `code-review-and-quality`

- Should the quality guidance merge into review, CI/CD, performance, and
  observability Skills, or become a recipe?
- Which review dimensions are already covered by native reasoning or
  official/runtime capabilities?
- What validation evidence is required before claiming quality improvement?

Forbidden shortcuts:

- do not override human or repository merge authority;
- do not make heavy review mandatory for trivial low-risk changes;
- do not universalize ecosystem-specific audit commands.
