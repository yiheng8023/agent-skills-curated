# Data Analytics Runtime Equivalence Draft

Status: non-runtime adapted draft, not approved payload.

This draft is derived from reviewed MIT-licensed source
`github:phuryn/pm-skills` at pinned revision
`a0cd730d4c61e519ca8568b172334402257a74a9`. It summarizes and neutralizes the
reviewed source intent. It does not copy upstream source text as curated
payload.

## Candidate Shape

Use this future candidate when a product, business, or research workflow needs
bounded analysis guidance for:

- experiment result interpretation;
- cohort or retention analysis;
- natural-language-to-SQL planning;
- metric and denominator checks;
- reproducible analysis handoff.

This is a data-analysis runtime-equivalence candidate. It should first ask
whether a visible runtime analytics capability already owns the job. If so, the
candidate can become reference guidance, intake guardrails, or a recipe step
instead of standalone payload.

## Intake Boundary

Before analysis, bind:

- data source, owner, sensitivity, and whether the data may be read in the
  current environment;
- metric definitions, denominators, segmentation, time windows, and cohort
  grain;
- SQL dialect, schema evidence, database target, and execution permission;
- whether the output is explanation, proposed query, analysis plan, notebook,
  dashboard, or file artifact;
- whether statistical claims require confidence, power, sample-size, guardrail,
  or practical-significance assumptions.

If the data, schema, metric definition, or experiment setup is missing, ask for
it or label the result as a bounded assumption.

## Workflow

1. Classify the task as experiment analysis, cohort analysis, SQL generation,
   or mixed analytics workflow.
2. Check whether a visible runtime analytics capability should own execution.
3. Confirm allowed data access and output surface before reading files or
   proposing executable code.
4. Normalize metric definitions, cohort grain, filters, and denominators before
   interpreting results.
5. Keep SQL and Python as proposed artifacts until execution is explicitly
   authorized and safe.
6. Separate statistical result, business interpretation, and recommended action.
7. Preserve validation steps so the user can reproduce or challenge the result.

## Must Not

- Do not execute SQL or Python by default.
- Do not claim statistical significance without explicit assumptions.
- Do not infer schema, metric definitions, or denominators from a vague
  business question.
- Do not read sensitive datasets unless the data source and permission are in
  scope.
- Do not write files, notebooks, dashboards, or reports without an explicit
  target.
- Do not treat a generated query as safe for production until it has been
  reviewed against schema, permissions, cost, and mutation risk.
- Do not duplicate runtime-owned analytics Skills as curated payload without a
  separate runtime-equivalence decision.

## Likely Release Direction

This draft is most likely a reference or recipe candidate. Before release, a
separate gate must decide whether the behavior becomes:

- a runtime-equivalence note for external analytics capability selection;
- a merge into existing performance, observability, or analysis workflows;
- a recipe step for data-backed product decisions;
- or reference-only evidence if runtime coverage already satisfies the need.
