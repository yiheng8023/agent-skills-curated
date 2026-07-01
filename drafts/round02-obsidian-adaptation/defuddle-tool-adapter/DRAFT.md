# Defuddle Tool Adapter Draft

Status: non-runtime adapter draft, not approved payload.

This draft is derived from reviewed MIT-licensed source
`github:kepano/obsidian-skills` at pinned revision
`a1dc48e68138490d522c04cbf5822214c6eb1202`. It summarizes and neutralizes the
reviewed source intent. It does not copy upstream source text as curated
payload.

## Candidate Shape

Use this future adapter only when the task is to extract readable markdown-like
content from ordinary web pages and the Defuddle CLI is already installed,
healthy, and explicitly suitable.

This is an external tool adapter, not a general web-reading Skill.

## Intake Boundary

Before using the tool, bind:

- the URL and whether it is public, private, authenticated, or sensitive;
- whether native browser/fetch/doc tools are sufficient;
- whether the output is transient analysis input or should be written to a
  file;
- whether the URL is already markdown or another structured document format;
- whether outbound network access is allowed in the current task.

If the URL ends in a direct markdown file or the current environment has a
better official/runtime reader, prefer that route.

## Safe Direction

- Treat web fetching as an external network action.
- Treat local output files as explicit writes.
- Preserve source URL provenance in any generated note.
- Do not treat cleaned extraction as authoritative when layout, images,
  tables, scripts, login state, or dynamic content matter.
- If the tool is missing, record a capability gap; do not install it from this
  adapter.

## Must Not

- Do not install npm packages.
- Do not fetch private, authenticated, or sensitive URLs without explicit
  authorization.
- Do not overwrite local files without explicit target-path confirmation.
- Do not claim extracted content preserves full page meaning, legal terms,
  tables, or visual layout.
- Do not use this adapter as a bypass around web, copyright, robots, or account
  boundaries.

## Likely Release Direction

This draft should remain an external tool adapter unless a future gate proves a
stable, agent-neutral dependency contract. It may become reference-only if
native or runtime web-reading capabilities are sufficient.
