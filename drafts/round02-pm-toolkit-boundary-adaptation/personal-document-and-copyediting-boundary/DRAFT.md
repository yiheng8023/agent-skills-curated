# Personal Document And Copyediting Boundary Draft

Status: non-runtime adapted draft, not approved payload.

This draft is derived from reviewed MIT-licensed source
`github:phuryn/pm-skills` at pinned revision
`a0cd730d4c61e519ca8568b172334402257a74a9`. It summarizes and neutralizes the
reviewed source intent. It does not copy upstream source text as curated
payload.

## Candidate Shape

Use this future candidate when a user asks for bounded help with:

- resume or professional profile feedback;
- job-posting alignment;
- grammar, logic, and flow review;
- targeted edits that preserve the user's voice;
- document improvement notes.

This is a personal-document and copyediting boundary candidate. It can
strengthen document and article editing workflows if it keeps personal data,
employment implications, and authorship boundaries explicit.

## Intake Boundary

Before reviewing, bind:

- document type, audience, and objective;
- whether a job posting, resume, or personal profile contains sensitive data;
- whether the user wants comments, suggested edits, full rewrite, or scoring;
- whether public output, file writes, or repository storage is in scope;
- what claims must remain factual and user-owned.

If the content contains personal data, avoid repeating unnecessary identifiers
and keep outputs local to the task.

## Workflow

1. Identify the document purpose and reader.
2. Separate correctness, clarity, logic, tone, structure, and evidence issues.
3. For resumes, distinguish presentation advice from career or hiring outcome
   predictions.
4. For copyediting, provide targeted fixes rather than rewriting the whole
   document unless requested.
5. Preserve the user's authorship and require confirmation before changing
   meaning.
6. Avoid carrying private personal details into public examples, docs, or
   repository artifacts.

## Must Not

- Do not make hiring, employment, immigration, or credential claims.
- Do not expose resume or job-posting personal data in public outputs.
- Do not fabricate achievements, metrics, degrees, employers, titles, or
  qualifications.
- Do not rewrite a user's document into claims they cannot verify.
- Do not save personal documents unless the destination and authority are
  explicit.
- Do not treat grammar/style advice as proof that the document is truthful or
  appropriate for a regulated context.
- Do not duplicate existing document/editing Skills without proving distinct
  governed value.

## Likely Release Direction

This draft is most likely a merge or reference candidate for existing document
and article editing workflows. Before release, a separate gate must decide
whether the behavior becomes:

- a merge into `doc`;
- a merge into `edit-article`;
- a personal-document reference note;
- or rejected if privacy and overlap costs outweigh the benefit.
