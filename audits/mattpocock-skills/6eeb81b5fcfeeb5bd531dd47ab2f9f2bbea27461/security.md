# Security Review

Source: `github:mattpocock/skills`

Revision: `6eeb81b5fcfeeb5bd531dd47ab2f9f2bbea27461`

The repository contains GitHub release automation, shell linking/listing
scripts, a plugin manifest, and Skill-bundled shell templates. None receives
blanket execution authority. The curated release includes only individually
reviewed payload files listed in the schema-1 release manifest.

Retained shell assets are inert templates or explicit guardrail installers;
their Skill instructions must preserve user authorization, path confinement,
review-before-execution, and post-write verification. No credential, session,
account, Hook enablement, remote write, package installation, or live Agent
mutation is inherited from the upstream repository.

Result: source is eligible for per-Skill review, not wholesale execution.
