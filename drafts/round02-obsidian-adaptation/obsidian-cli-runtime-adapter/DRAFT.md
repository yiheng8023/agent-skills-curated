# Obsidian CLI Runtime Adapter Draft

Status: non-runtime adapter draft, not approved payload.

This draft is derived from reviewed MIT-licensed source
`github:kepano/obsidian-skills` at pinned revision
`a1dc48e68138490d522c04cbf5822214c6eb1202`. It summarizes and neutralizes the
reviewed source intent. It does not copy upstream source text as curated
payload.

## Candidate Shape

Use this future adapter only when the user explicitly asks to operate a local
Obsidian vault through an Obsidian CLI or to debug an Obsidian plugin/theme
through a running Obsidian app.

This is not portable Skill payload by itself. It depends on local runtime
state:

- Obsidian installed and open;
- the Obsidian CLI installed and healthy;
- a known target vault or active vault;
- local file write authority when mutations are requested.

## Intake Boundary

Before running any CLI command, bind:

- the vault name or path;
- the target file, note, plugin, theme, or command class;
- whether the action is read-only or mutating;
- expected output;
- whether screenshots, DOM inspection, console access, or app-context
  evaluation is in scope.

Mutating commands, developer commands, screenshots, DOM inspection, console
inspection, and app-context evaluation require explicit confirmation at the
current task boundary.
Any elevated local-app control requires explicit confirmation before it runs.

## Safe Direction

- Prefer read-only list, read, search, tags, backlinks, and status-style
  commands before mutation.
- Show the intended command and target before writes when the command can
  create, append, overwrite, reload, or inspect app internals.
- Treat plugin reload, CSS inspection, DOM inspection, screenshots, console
  inspection, and app-context evaluation as elevated local-app control.
- Record failure as a runtime capability gap rather than installing or
  enabling anything automatically.

## Must Not

- Do not install the CLI from this adapter.
- Do not assume the most recently focused vault is correct for a user request.
- Do not write notes, daily logs, properties, or tasks without explicit write
  authorization.
- Do not run app-context evaluation, plugin reload, screenshots, or DOM
  inspection as a background convenience.
- Do not present adapter availability as proof that Obsidian or a vault exists.

## Likely Release Direction

This draft should remain an external runtime adapter unless a future consumer
repository supplies verified install, permission, backup, rollback, and
capability-health checks. It is not eligible for direct release-manifest
payload without that separate runtime gate.
