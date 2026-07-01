# Round 02 Release Admission Review Template

Machine-readable template:
[`registry/round02-release-admission-review-template.json`](../registry/round02-release-admission-review-template.json).

Template only, not approval.

This template defines how to run Round-02 release/admission review after the
owner explicitly approves that gate. It does not approve any candidate,
payload, manifest, routing projection, install, publication, local sync, source
redistribution, asset redistribution, dependency installation, credential use,
or external media generation.

## When this template may be used

Use this template only after one of the bounded approval phrases is recorded:

```text
批准进入 Round-02 release/admission 审查阶段
```

or:

```text
Approve Round-02 release/admission review only
```

Without that approval, this document remains scaffolding.

## Review sections

Each candidate-specific review must cover:

1. source integrity;
2. license and attribution;
3. security;
4. portability and neutralization;
5. overlap and conflict;
6. native or runtime equivalence;
7. routing semantics;
8. release manifest impact;
9. consumer install impact;
10. source text redistribution boundary;
11. source asset redistribution boundary;
12. dependency, credential, and media boundary;
13. validation plan;
14. rejected alternatives;
15. next gate.

## Allowed decisions after approval

- `proposed-approved-payload`
- `merge-into-existing-approved-skill`
- `recipe-only`
- `adapter-only`
- `reference-only`
- `reject`

These decisions are still review outcomes. A `proposed-approved-payload`,
`merge-into-existing-approved-skill`, `recipe-only`, or `adapter-only` outcome
does not by itself mutate `skills/`, `release-manifest.json`, generated
routing, publication surfaces, local sync, or live Agent environments. Those
require later, narrower gates.

## Fail-closed conditions

Stop the review or keep the candidate out of the execution path if:

- owner approval for Round-02 release/admission review is missing;
- candidate source revision or upstream hash differs from Round-02 gate
  evidence;
- license, provenance, attribution, source-text redistribution, or source-asset
  redistribution posture is unclear;
- security, portability, overlap, native/runtime equivalence, or routing review
  is incomplete;
- the candidate would override repository, runtime, user, domain, legal,
  security, privacy, or human authority;
- the candidate would enter `skills/`, `release-manifest.json`, generated
  routing, publication, local runtime sync, or a live environment before its
  later specific gate;
- the candidate would install dependencies, use credentials, call TTS
  providers, generate external media, or write files without explicit later
  authorization;
- the candidate decision is based only on enthusiasm, source popularity, broad
  usefulness, or coverage pressure without evidence.

## Output contract after approval

The future candidate review record must contain one entry per candidate and
include:

- decision;
- rationale;
- evidence;
- rejected alternatives;
- overlap handling;
- security boundary;
- portability boundary;
- source text boundary;
- source asset boundary;
- dependency, credential, and media boundary;
- boundary assertions;
- validation results;
- next gate.

Until that record exists and passes verification, Round-02 remains
readiness-only and no candidate enters approved payload, routing, manifest,
publication, live install, or local sync.
