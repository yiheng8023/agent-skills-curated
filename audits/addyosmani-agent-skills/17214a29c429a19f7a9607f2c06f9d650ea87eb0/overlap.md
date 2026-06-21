# Overlap And Conflict Adjudication

All 24 upstream Skills were compared against the current local, built-in, and
plugin-provided Skill ecosystem. Five are independently adopted; the other 19
are merged, adapter-only, recipe-only, or rejected in `selection.json`.

Canonical defaults:

- global routing: `capability-router`; reject `using-agent-skills`;
- TDD: curated `tdd`; Superpowers only in an explicit Superpowers workflow;
- debugging: curated `diagnose`; Superpowers only when explicitly scoped;
- general change review: curated `review`; security review remains Codex
  Security-owned;
- implementation planning: Superpowers `writing-plans`; publishing work to an
  issue tracker remains `to-issues`;
- browser runtime verification uses the capability available in the active
  environment;
- product design, Figma, GitHub publication, and security scans retain their
  specialized owners.

The approved Addy set is intentionally limited to CI/CD, deprecation and
migration, observability, performance, and production launch. Relationships,
conditions, and multi-Skill recipes are recorded in `registry/` and generated
into `generated/topology.*`.
