# Synthetic Data And SQL Tooling Draft

Status: non-runtime adapted draft, not approved payload.

This draft is derived from reviewed MIT-licensed source
`github:phuryn/pm-skills` at pinned revision
`a0cd730d4c61e519ca8568b172334402257a74a9`. It summarizes and neutralizes the
reviewed source intent. It does not copy upstream source text as curated
payload.

## Candidate Shape

Use this future candidate when a user needs bounded support for:

- sample datasets for demos, tests, or documentation;
- SQL query drafts or insert statements;
- local analysis scripts;
- reproducible examples that avoid sensitive production data.

This is a synthetic-data and SQL tooling candidate. It is not permission to run
generated code, mutate databases, create files, or manufacture real-looking
personal records from actual people.

## Intake Boundary

Before generating anything, bind:

- purpose: demo, test fixture, documentation example, local analysis, or
  database seed proposal;
- target schema, output format, row count, constraints, and destination;
- whether any file write, script execution, or database execution is requested;
- whether generated data must be synthetic, anonymized, pseudonymous, or
  derived from already-provided safe examples;
- privacy, domain, jurisdiction, and retention constraints when relevant.

If the user provides real records, treat them as sensitive unless the task and
policy clearly say otherwise.

## Workflow

1. Confirm the output is a proposal, file artifact, script, SQL statement, or
   execution request.
2. Prefer small, deterministic, schema-valid examples for review.
3. Keep generated identifiers, names, emails, phone numbers, and addresses
   synthetic and clearly fictional.
4. For SQL, separate read-only queries from insert, update, delete, DDL, or
   migration behavior.
5. For scripts, state dependencies and expected output before execution is
   considered.
6. Validate shape, constraints, and edge cases before presenting the result as
   usable.
7. Escalate to explicit approval before writes, execution, database access, or
   larger data generation.

## Must Not

- Do not run generated SQL against a live database.
- Do not generate realistic personal data from real people.
- Do not treat anonymization as complete without a separate privacy review.
- Do not create files unless the destination and write authority are explicit.
- Do not install packages, connect to databases, or execute scripts from this
  draft alone.
- Do not create seed data that implies production realism, legal compliance, or
  statistical representativeness.
- Do not mix real customer, employee, student, patient, payment, or account data
  into public examples.

## Likely Release Direction

This draft is most likely a deferred tool adapter or reference candidate.
Before release, a separate gate must decide whether the behavior becomes:

- a recipe step inside an approved analytics or testing workflow;
- a merge into an existing execution or data-quality workflow;
- a runtime adapter for a local analysis tool;
- or reference-only guidance because the execution boundary is too high.
