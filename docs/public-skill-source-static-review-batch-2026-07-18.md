# Public Skill Source Static Review — 2026-07-18 Batch

This source-pinned, non-executing review covers five public sources selected by
the balanced discovery preflight. Temporary clones were used only to read
fixed commits and Git blob identities; no source body was vendored, installed,
connected, executed, enabled, or admitted.

- `loopy` remains the only candidate-with-limits: compare the `loopy` body,
  exclude the redundant `loop-library` alias, and keep its catalog and publish
  infrastructure behind a separate external-service boundary.
- `governed-skill-tree` is a dense 17-Skill reference with high overlap and a
  material over-structuring risk; the whole suite is held.
- `ai-skills` is a 24-component account and service integration suite. Review
  only a component selected by a concrete gap; never infer whole-suite value.
- `claude-code-infrastructure-showcase` has five distinct Skill bodies, 39 Hook
  files, and host-specific blocking and state-tracking behavior. Skills and
  Hooks require separate review.
- `context-mode` is an MCP, Hook, storage, and adapter system under Elastic
  License 2.0, not a direct Skill admission candidate. Its context-saving
  hypothesis must be separated from privacy, persistence, update, license, and
  over-control evaluation.

No source or component is approved. Quality, superiority, residual gaps,
repository self-authoring, and hard-standard eligibility remain unproven. These
are correctable working conclusions, not hard standards.
