---
name: obsidian-open-format-knowledge-files
description: Use when reading, creating, editing, or reviewing Obsidian-compatible Markdown notes, JSON Canvas files, or Bases files as portable open-format knowledge artifacts without assuming a live Obsidian app, CLI, plugin, or vault.
metadata:
  source: https://github.com/kepano/obsidian-skills/tree/a1dc48e68138490d522c04cbf5822214c6eb1202
  license: MIT
  adapted-for: cross-agent
---

# Obsidian Open-Format Knowledge Files

Use this Skill for Obsidian-compatible files when the useful part is the open
file format, not control of a live Obsidian app or a local vault.

This Skill covers:

- Obsidian-flavored Markdown notes.
- JSON Canvas `.canvas` files.
- Obsidian Bases-style `.base` files.

It does not prove that Obsidian, an Obsidian CLI, plugins, a focused vault, or
the user's desktop app are installed or authorized. Treat app control, CLI
commands, plugin installation, vault sync, webpage extraction, and generated
assets as separate runtime or tool-adapter work.

## Intake

Before changing files, bind the smallest safe contract:

- Target format: Markdown, JSON Canvas, or Bases.
- Target path or workspace.
- Mode: read-only review, proposed content, or actual file write.
- Whether Obsidian-only rendering features are acceptable.
- Whether links, embeds, file paths, URLs, formulas, or properties expose
  private, external, copyrighted, or sensitive material.

If the target path or write authority is unclear, stop and ask. If the user
only wants advice, return a patch-ready proposal instead of writing files.

## Format Rules

### Markdown Notes

- Preserve ordinary Markdown validity first.
- Keep Obsidian-only syntax explicit: wikilinks, embeds, tags, callouts,
  comments, block identifiers, and YAML properties.
- Do not assume a link resolves unless the target exists or the user supplied
  the vault context.
- Keep frontmatter parseable YAML when present.
- Avoid moving private paths, attachments, or embeds into published text.

### JSON Canvas

- Keep the file valid JSON.
- Preserve unique node and edge identifiers.
- Ensure edges refer to existing nodes.
- Preserve required node fields for text, file, link, group, and other node
  types that are already present.
- Escape multiline text and URLs through JSON semantics, not manual string
  splicing.
- Treat visual placement as format data; do not claim the canvas is visually
  correct unless it is rendered or otherwise inspected.

### Bases Files

- Keep the file valid YAML.
- Preserve property, formula, filter, sort, and view names as data contracts.
- Quote expressions or strings when YAML parsing would be ambiguous.
- Do not invent formulas from business meaning alone; mark uncertain formulas
  for user confirmation.
- Treat Bases behavior as Obsidian-specific. Generic Markdown consumers may
  ignore it.

## Workflow

1. Identify the format and mode.
2. Read existing files when they exist and access is authorized.
3. Use a structured parser or format-aware validation when practical.
4. Make the smallest change that preserves existing semantics.
5. Separate generic Markdown/JSON/YAML validity from Obsidian rendering
   assumptions.
6. Record any unresolved link, formula, embed, or rendering uncertainty.
7. Verify the file parses or provide the exact check that could verify it.

## Boundaries

- Do not invoke an Obsidian CLI, local app, plugin, browser automation, or
  webpage extraction tool from this Skill.
- Do not install packages, plugins, CLIs, or dependencies.
- Do not mutate a vault, sync target, or local knowledge base without explicit
  write authority for that exact path.
- Do not fetch external links or assets as part of open-format editing.
- Do not claim rendering success without rendering evidence from the user's
  environment.
- Do not treat this Skill as a live knowledge-base sync, search, import, or
  automation system.

## Verification

For meaningful changes, report which checks actually ran:

- Markdown: frontmatter parses when present, links/embeds are listed, and
  Obsidian-only syntax is intentional.
- JSON Canvas: JSON parses, ids are unique, and edges resolve.
- Bases: YAML parses, formulas and views are named, and ambiguous expressions
  are marked.

If a parser or renderer is unavailable, state that clearly and keep the output
as a reviewable proposal rather than a rendering claim.
