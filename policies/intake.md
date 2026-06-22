# Intake Policy

Treat every upstream Skill, prompt, Hook, script, command, adapter, and setup
document as executable supply-chain input. Pin an immutable revision, preserve
license and provenance, inspect every executable surface, record every upstream
Skill disposition, and approve only a minimal non-overlapping runtime set.

Keep the intake state separate from release state:

- An official, runtime-owned, or built-in capability may be recorded as
  external capability metadata, but its body must not be vendored or added to
  the manifest by default.
- A third-party candidate must pass source pinning, license, provenance,
  security, portability, overlap, adaptation, and validation review. Before a
  recorded approval, it must not enter an execution path.
- Only curated approved content with `status=approved` may enter `skills/` and
  the manifest. `registry/skills.json` is the schema-1 approved release
  inventory, not a candidate backlog.

An upstream validator is evidence about structure, not proof of safety,
portability, semantic consistency, or runtime authorization.
