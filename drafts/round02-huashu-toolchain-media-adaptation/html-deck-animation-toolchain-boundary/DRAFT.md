# HTML Deck Animation Toolchain Boundary Draft

Status: non-runtime adapted draft, not approved payload.

This draft is derived from reviewed MIT-licensed source
`github:alchaincyf/huashu-design` at pinned revision
`ec9ec0fff8a66a932c4049b200ea4c2b09f8d25b`. It summarizes and neutralizes the
reviewed source intent. It does not copy upstream source text, scripts, or
generated media as curated payload.

## Candidate Shape

This is an HTML deck and animation toolchain boundary candidate.

Use this future candidate only when a user explicitly asks for a local
HTML-based deck, animation, PDF/PPTX export, browser-rendered review surface, or
media-export workflow and has authorized the required runtime steps.

The useful pattern is not the upstream script body itself. The portable part is
the boundary discipline around turning structured content into inspectable
slides or scenes, rendering them in a browser, and exporting artifacts only
after the user has approved dependencies, file writes, and media output.

## Intake Boundary

Before any execution path, bind:

- source content, target format, output directory, and review surface;
- whether dependency installation is allowed;
- whether Playwright or another browser runtime is authorized;
- whether generated files may be written;
- whether PDF, PPTX, video, or still image output is requested;
- whether external assets, fonts, screenshots, or generated imagery are
  authorized and licensed for the intended use.

Do not install dependencies, run Playwright, start servers, or export files without explicit authorization.

## Must Not

- Do not vendor scripts or generated media into approved payload from this gate.
- Do not assume local browser automation is available in every agent runtime.
- Do not start a dev server, run a browser, write output files, or publish media
  unless that side effect is authorized.
- Do not treat upstream demo HTML, animation defaults, fonts, or visual samples
  as product truth.
- Do not claim final client-ready quality without visual verification and
  user or stakeholder approval.

## Likely Release Direction

This draft is most likely an adapter or recipe candidate for prototype,
presentation, and browser-automation workflows. Before release, a separate gate
must decide whether it becomes:

- a local toolchain recipe;
- a merge into an existing prototype or Playwright Skill;
- external capability metadata;
- or reference-only guidance because runtime and media boundaries are too heavy.
