# Brand Asset Provenance Protocol Draft

Status: non-runtime adapted draft, not approved payload.

This draft is derived from reviewed MIT-licensed source
`github:alchaincyf/huashu-design` at pinned revision
`ec9ec0fff8a66a932c4049b200ea4c2b09f8d25b`. It summarizes and neutralizes the
reviewed source intent. It does not copy upstream source text as curated
payload.

## Candidate Shape

Use this future candidate when a design or document references a real brand,
product, venue, person, or organization and needs disciplined asset handling:

- identify which assets are required for recognizability;
- prefer user-provided, official, or clearly licensed sources;
- record source, date, permission, and intended use;
- use honest placeholders when assets are missing;
- keep redistribution and public-use rights explicit.

This is a brand-asset provenance protocol candidate. It is not permission to
scrape, use, modify, or redistribute logos, product images, screenshots, audio,
or media assets.

## Intake Boundary

Before asset use, bind:

- brand/product/entity names that will appear in the artifact;
- whether the work is private mockup, internal review, public marketing,
  comparative analysis, or publication;
- available user-provided assets and their permission status;
- official-source candidates and licensing or terms constraints;
- whether generated, searched, downloaded, or edited assets are authorized.

If permission or source quality is unclear, use a labeled placeholder or ask
for assets instead of presenting approximations as official material.

## Workflow

1. List every recognizable brand, product, or entity in the artifact.
2. Decide the minimum assets needed for truthful recognition.
3. Prefer user-provided or official sources and record source date.
4. Check whether the intended use is private, public, comparative, or
   commercial.
5. Keep extracted colors or fonts secondary to real asset provenance.
6. Label missing assets and do not hide uncertainty behind generic visuals.
7. Re-check redistribution boundaries before any public release.

## Must Not

- Do not scrape, download, or redistribute brand assets without permission and source review.
- Do not use CSS silhouettes, hand-drawn SVGs, or generic placeholders as if they were official product assets.
- Do not imply endorsement, partnership, or official status from asset use.
- Do not copy restricted press-kit, report, screenshot, audio, or video assets
  into curated payload.
- Do not use generated lookalike product imagery as factual product material.
- Do not weaken copyright, trademark, privacy, or publicity-rights boundaries
  for cross-agent portability.

## Likely Release Direction

This draft is most likely a reference or checklist candidate. Before release, a
separate gate must decide whether the behavior becomes:

- a merge into design workflows;
- a provenance checklist for public artifacts;
- a document asset-handling note;
- or reference-only guidance because rights and redistribution risks are too
  context-dependent.
