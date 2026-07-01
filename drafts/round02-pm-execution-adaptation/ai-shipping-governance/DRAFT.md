# AI Shipping Governance Draft

Status: non-runtime adapted draft, not approved payload.

This draft is derived from reviewed MIT-licensed source
`github:phuryn/pm-skills` at pinned revision
`a0cd730d4c61e519ca8568b172334402257a74a9`. It summarizes and neutralizes the
reviewed source intent. It does not copy upstream source text as curated
payload.

## Candidate Shape

Use this future candidate when a software product, especially an AI-assisted or
agent-built app, needs a pre-ship reviewability package:

- intended-state documentation;
- permission and trust-boundary flow mapping;
- secret/configuration surface mapping;
- test coverage mapped back to documented claims;
- comparison between documented intent and implementation evidence.

This is a governance and review workflow candidate. It does not replace a security scanner, performance audit, legal review, or human release authority.

## Intake Boundary

Before producing or changing documents, bind:

- repository or artifact scope;
- whether the task is read-only review, proposed documentation, or actual file
  writes;
- authoritative intent sources such as PRDs, architecture docs, policies,
  permission matrices, tickets, or prior decisions;
- implementation evidence surfaces such as code paths, tests, configuration,
  jobs, external providers, and automation paths;
- the target release or handoff decision.

If intended-state evidence is missing, record that absence as a gap instead of
inventing intent.

## Workflow

1. Inventory intended-state claims and their authority level.
2. Inventory implementation evidence with cited files, tests, configuration, or
   operational records.
3. Compare claims and implementation one boundary at a time.
4. Classify mismatches by trust, tenant, data, money, cost, infrastructure, or
   safety impact.
5. Separate findings from questions when evidence is missing.
6. Propose the minimum documentation, test, or implementation follow-up needed
   to make the system reviewable.
7. Keep launch or merge authority with the owner and active repository process.

## Must Not

- Do not fabricate product intent from code behavior.
- Do not treat documentation as proof that implementation is correct.
- Do not turn every cosmetic doc/code mismatch into a release blocker.
- Do not write repository documentation unless that write is explicitly in
  scope.
- Do not claim security approval, compliance approval, or production readiness
  from this draft alone.
- Do not route unapproved third-party source text into live execution.

## Likely Release Direction

This draft is most likely a merge or recipe candidate across existing approved
review and shipping workflows. Before release, a separate gate must decide
whether the behavior becomes:

- a merge into `review`;
- a merge into `shipping-and-launch`;
- a recipe step in a launch-readiness or spec-to-release workflow;
- or reference-only evidence if overlap is too high.
