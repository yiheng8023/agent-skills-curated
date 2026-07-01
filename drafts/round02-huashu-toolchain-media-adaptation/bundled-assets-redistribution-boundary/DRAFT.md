# Bundled Assets Redistribution Boundary Draft

Status: non-runtime adapted draft, not approved payload.

This draft is derived from reviewed MIT-licensed source
`github:alchaincyf/huashu-design` at pinned revision
`ec9ec0fff8a66a932c4049b200ea4c2b09f8d25b`. It records the redistribution
boundary for the upstream `assets/` tree. It does not copy upstream assets as
curated payload.

## Candidate Shape

This is a bundled-assets redistribution boundary candidate.

Use this future candidate when evaluating whether a Skill source includes demo,
audio, image, video, showcase, font, or other media assets that are useful for
understanding the source but should not be redistributed without asset-level
provenance.

The useful pattern is a safety rule: source code or repository text license
evidence does not automatically clear every bundled media asset for reuse,
especially when assets may embed third-party brands, voices, screenshots,
generated media, or unknown upstream rights.

## Intake Boundary

Before any asset reuse, bind:

- exact asset path, size, hash, and intended reuse;
- repository license and asset-specific license evidence;
- whether the asset contains third-party marks, real people, voices, product
  screenshots, music, photos, or generated media;
- whether redistribution, modification, publication, or commercial use is
  permitted;
- whether a placeholder, regenerated asset, or user-supplied asset is safer.

Do not redistribute bundled audio, image, demo, or showcase assets before asset-level provenance review.

## Must Not

- Do not assume MIT repository license automatically clears every bundled media asset for reuse.
- Do not vendor upstream media into `skills/`, release manifests, generated
  projections, docs, examples, or consumer installs from this gate.
- Do not publish screenshots, generated videos, voices, or product-like assets
  without path-level rights evidence.
- Do not let a useful toolchain source smuggle unreviewed media into curated
  payload.

## Likely Release Direction

This draft is most likely a standing exclusion and review checklist rather than
an installable Skill. Before any asset reuse, a separate gate must produce
asset-level provenance, permission, hash, intended-use, and redistribution
evidence.
