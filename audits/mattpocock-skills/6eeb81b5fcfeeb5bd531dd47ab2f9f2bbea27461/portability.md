# Portability Review

Source: `github:mattpocock/skills`

Revision: `6eeb81b5fcfeeb5bd531dd47ab2f9f2bbea27461`

Upstream content includes Claude-specific paths, plugin conventions, author
identity, sub-agent assumptions, and GitHub-oriented workflows. Curated
approval requires neutral Skill names, agent-neutral instructions, optional
capability fallbacks, explicit issue-tracker/runtime context, and no assumption
that a named Agent feature exists.

Product-specific adapters may be retained only when essential to the workflow
and must be scoped by context and permission. Personal productivity Skills and
ordinary reasoning/editing instructions do not become portable merely by
renaming them.

Result: only individually adapted Skills with explicit compatibility and
fallback metadata are portable.
