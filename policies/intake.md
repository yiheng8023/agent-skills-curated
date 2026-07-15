# Intake Policy

Treat every upstream Skill, prompt, Hook, script, command, adapter, and setup
document as executable supply-chain input. Pin an immutable revision, preserve
license and provenance, inspect every executable surface, record every upstream
Skill disposition, and approve only a minimal non-overlapping runtime set.

Keep the intake state separate from release state:

- Intake governs third-party Skill bodies against an abstract, product-neutral
  capability taxonomy. Official, runtime-owned, built-in, and first-party Skill
  bodies are not governed or inventoried here. They may be consulted only as
  dated overlap evidence, never as managed inventory, repository-owned content,
  or proof of current availability; their bodies must not be vendored or added
  to the manifest.
- A third-party candidate must pass source pinning, license, provenance,
  security, portability, overlap, adaptation, and validation review. Before a
  recorded approval, it must not enter an execution path.
- Only curated approved content with `status=approved` may enter `skills/` and
  the manifest. `registry/skills.json` is the schema-1 approved release
  inventory, not a candidate backlog.

Repository-authored gap-fill work is an origin inside the same non-executable
candidate state; it is not a fourth release layer, not an approved Skill, and
not the official/runtime/vendor first-party baseline class. It is eligible for
design only after a material residual gap is supported by evidence and native,
official/runtime, existing curated, external, composed, non-Skill,
project-standard, and human-authority alternatives have been compared. Before
admission it must record design provenance, license ownership, security,
portability, overlap, tests, maintenance and exit cost, and owner approval. A
self-built Skill must not receive weaker review merely because its author is
inside the project.

Official Skills, capability packages, workflow templates, and similar public
capability bundles from Agent, runtime, platform, or tool ecosystems may be
inspected as official external capability baselines for coverage comparison,
gap analysis, and routing calibration. Record the inspected revision, license
posture, capability coverage, gap, and disposition. A baseline row does not
approve import, adaptation, execution, or redistribution. Source-available,
all-rights-reserved, unclear-license, product-specific, or runtime-owned
official content remains reference-only unless a separate approved permission
and adaptation path exists.

A baseline row does not approve import.

User-starred repositories and awesome lists are discovery hints only. Classify
each source before intake as official baseline, third-party candidate, index,
agent runtime, methodology, external capability metadata, reference-only, or
rejected. Stars, popularity, or list membership do not prove license safety,
quality, portability, maintenance, or execution approval.

Stars are only discovery hints.

An upstream validator is evidence about structure, not proof of safety,
portability, semantic consistency, or runtime authorization.
