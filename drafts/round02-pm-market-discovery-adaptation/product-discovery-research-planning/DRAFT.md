# Product Discovery Research Planning Draft

Status: non-runtime adapted draft, not approved payload.

This draft is derived from reviewed MIT-licensed source
`github:phuryn/pm-skills` at pinned revision
`a0cd730d4c61e519ca8568b172334402257a74a9`. It summarizes and neutralizes the
reviewed source intent. It does not copy upstream source text as curated
payload.

## Candidate Shape

Use this future candidate when a product team needs bounded discovery support
for:

- opportunity-to-solution mapping;
- feature prioritization;
- metric and dashboard planning;
- customer interview scripts;
- experiment and assumption planning.

This is a product-discovery research-planning candidate. It should organize
evidence and questions without pretending that research planning, interviews,
or prioritization scores are product truth.

## Intake Boundary

Before drafting discovery work, bind:

- desired outcome, business objective, or decision the research informs;
- available customer research, analytics, feedback, tickets, survey results, or
  product strategy evidence;
- whether participant data is present and how it may be handled;
- whether the task is planning, summarizing provided evidence, writing an
  interview guide, designing metrics, or recommending priorities;
- who will validate the discovery findings and approve product direction.

If research inputs are absent, label the output as a planning scaffold rather
than validated discovery.

## Workflow

1. Start with the outcome or decision to be informed.
2. Separate opportunities, solutions, experiments, metrics, and assumptions.
3. Use scoring only when inputs and confidence are visible.
4. Design interview questions around past behavior and specific examples.
5. Define metrics with numerator, denominator, time window, source, and owner.
6. Keep recommendations traceable to evidence or explicitly marked
   assumptions.
7. Preserve the next validation step and the human decision owner.

## Must Not

- Do not treat interview opinions as validated demand.
- Do not collect or expose participant personal data without explicit scope and handling rules.
- Do not ask leading interview questions that pitch the product.
- Do not prioritize a feature backlog as final without product strategy,
  customer evidence, effort, risk, and owner review.
- Do not define dashboards without data source, metric formula, cadence, and
  alert owner.
- Do not turn customer quotes, support tickets, or analytics into public
  artifacts without privacy review.
- Do not claim product direction is approved from this draft alone.

## Likely Release Direction

This draft is most likely a merge or recipe candidate across existing approved
questioning, design, PRD, and planning workflows. Before release, a separate
gate must decide whether the behavior becomes:

- a merge into `grill-me` or another questioning workflow;
- a merge into `to-prd` or design/planning Skills;
- a recipe step for discovery-to-PRD conversion;
- or reference-only guidance if overlap is too high.
