# Product Execution Documents Draft

Status: non-runtime adapted draft, not approved payload.

This draft is derived from reviewed MIT-licensed source
`github:phuryn/pm-skills` at pinned revision
`a0cd730d4c61e519ca8568b172334402257a74a9`. It summarizes and neutralizes the
reviewed source intent. It does not copy upstream source text as curated
payload.

## Candidate Shape

Use this future candidate when a product idea, feature, or release needs a
bounded documentation chain:

- PRD or product requirements;
- user stories or job stories;
- acceptance criteria;
- test scenarios;
- user-facing release notes.

This is an execution-document workflow candidate. It should strengthen the
existing `to-prd`, `to-issues`, `triage`, and `shipping-and-launch` surfaces
instead of creating parallel template Skills for every document type.

## Intake Boundary

Before drafting, bind:

- product or feature scope;
- source materials: user notes, tickets, design links, customer evidence,
  analytics, interviews, changelogs, or repository history;
- whether web research is requested and allowed;
- whether the output is draft-only, repository documentation, issue text, or a
  saved file;
- the target audience and decision authority.

If source materials are absent, ask for the missing input or label assumptions
as assumptions. Do not turn a guessed PRD into product authority.

## Workflow

1. Start from the user goal and source evidence.
2. Decide the needed document level: PRD, story, test scenario, release note, or
   a chain across them.
3. Preserve traceability from each requirement to user value, acceptance
   evidence, and release communication.
4. Convert requirements into issue-ready slices only when ownership, scope, and
   acceptance evidence are clear.
5. Convert stories into test scenarios only when roles, preconditions, steps,
   and expected outcomes can be stated.
6. Convert shipped work into release notes only from tickets, changelogs,
   commits, PRDs, or other authoritative shipped evidence.
7. Keep output draft-labeled until the owner accepts it.

## Must Not

- Do not save files by default; file writes require explicit target and
  authority.
- Do not use web research unless the task asks for current public context or
  the repository policy requires it.
- Do not treat design links, tickets, or changelogs as accessible unless they
  are actually provided or connected.
- Do not claim a release note describes shipped behavior without shipped evidence.
- Do not duplicate existing approved Skills as standalone template payload
  without proving distinct value.
- Do not embed private customer, analytics, or ticket data into public outputs
  without review.

## Likely Release Direction

This draft is most likely a merge candidate into existing approved execution
Skills and launch workflows. Before release, a separate gate must decide the
exact merge target, routing behavior, attribution notice, and whether any part
should remain recipe-only or reference-only.
