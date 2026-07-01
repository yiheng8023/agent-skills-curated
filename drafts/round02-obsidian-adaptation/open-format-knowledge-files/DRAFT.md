# Obsidian Open-Format Knowledge Files Draft

Status: non-runtime adapted draft, not approved payload.

This draft is derived from reviewed MIT-licensed source
`github:kepano/obsidian-skills` at pinned revision
`a1dc48e68138490d522c04cbf5822214c6eb1202`. It summarizes and neutralizes the
reviewed source intent. It does not copy upstream source text as curated
payload.

## Candidate Shape

Use this future candidate when the task is about reading, creating, editing, or
reviewing Obsidian-compatible open-format knowledge files:

- Obsidian-flavored Markdown notes;
- JSON Canvas `.canvas` files;
- Obsidian Bases `.base` files.

This is a file-format and knowledge-workflow candidate. It must not imply that
Obsidian, an Obsidian CLI, a vault, or a plugin is installed.

## Intake Boundary

Before writing or editing files, bind:

- the target path or workspace;
- whether the user wants read-only review, proposed content, or an actual file
  write;
- the target format: Markdown, JSON Canvas, or Bases YAML;
- whether Obsidian-specific rendering assumptions are acceptable;
- whether any links, embeds, files, URLs, or formulas refer to private or
  external material.

If the target or write authority is unclear, ask before changing files.

## Workflow

1. Classify the format.
2. Read existing files when present and allowed.
3. Preserve standard Markdown/JSON/YAML semantics before Obsidian-specific
   extensions.
4. For Markdown, keep vault-only wikilinks, embeds, callouts, comments, tags,
   and frontmatter explicit.
5. For JSON Canvas, maintain valid JSON, unique node and edge ids, resolvable
   edges, required node fields, and escaped text.
6. For Bases, maintain valid YAML, quoted expressions, defined formulas, and
   view references.
7. Validate with parser-level checks when feasible.
8. Treat Obsidian visual rendering as optional verification, not guaranteed
   runtime availability.

## Must Not

- Do not invoke an Obsidian CLI or assume a focused vault.
- Do not install plugins, CLIs, or packages.
- Do not fetch web pages or external assets as part of this draft.
- Do not mutate a local vault without explicit write authority.
- Do not claim an Obsidian-specific file will render correctly unless that
  rendering has been verified in the user's environment.
- Do not treat file-format guidance as a live knowledge-base sync mechanism.

## Likely Release Direction

This draft is a candidate for a future new curated Skill or recipe component,
not a merge into an existing approved Obsidian Skill. The current repository release inventory has no approved `obsidian-vault` Skill.

Before release, a separate gate must decide:

- final name and stable id;
- whether it is standalone Skill payload, recipe-only, or reference-only;
- exact trigger wording and negative triggers;
- JSON/YAML validation requirements;
- overlap with documentation, knowledge-capture, prototype, and handoff
  workflows;
- attribution and third-party notice updates.
