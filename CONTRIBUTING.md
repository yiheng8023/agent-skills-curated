# Contributing

Thank you for helping improve `agent-skills-curated`.

This repository governs reviewed, portable, cross-agent Skill assets. It is not a raw prompt dump, a general resource radar, a user configuration repository, or a live Agent installation surface.

## Contribution types

Useful contributions include:

- candidate Skill source suggestions with license and provenance evidence;
- security, portability, overlap, lifecycle, and neutrality reviews;
- Skill adaptations that reduce agent-specific coupling without weakening safety;
- registry, topology, conflict, recipe, routing-scenario, or validation improvements;
- documentation that clarifies official/runtime capability baselines, candidate boundaries, or downstream consumption.

## Candidate Skill intake

A proposed Skill source must include:

- canonical source URL;
- pinned revision or a plan to pin before review;
- license and redistribution notes;
- provenance evidence;
- candidate Skill paths;
- executable surfaces, install scripts, network access, file writes, or account requirements;
- portability concerns and agent-specific assumptions;
- overlap with current curated Skills, official/runtime capabilities, or existing recipes;
- proposed disposition: `merge`, `adapter-only`, `recipe-only`, `reference`, or `reject`.

A candidate is not approved just because it is useful, popular, starred, official-looking, or already installed locally.

## Required gates before runtime approval

Before a Skill can enter `skills/`, release inventory, or a downstream runtime path, it must pass:

1. source pinning;
2. license and provenance review;
3. security review;
4. portability and neutralization review;
5. overlap and conflict review;
6. adaptation with preserved attribution where required;
7. validation and generated projection checks;
8. release-manifest update and verification.

## Boundaries

Please do not submit:

- secrets, tokens, private account state, local machine state, personal memory, or private user preferences;
- leaked prompts, proprietary dumps, or content with unclear redistribution rights as runtime candidates;
- official/runtime-owned Skill bodies as vendored inventory unless an explicit permission and adaptation path is approved;
- changes that install Skills, write to live Agent environments, mutate user configuration repositories, or bypass human approval;
- generated files as hand-authored truth.

## Downstream relationship

Downstream repositories such as `codex-user-config` and `claude-user-config` consume pinned reviewed releases. They do not own third-party Skill-body governance. This repository does not own their private configuration, memory, account state, or runtime installation choices.
