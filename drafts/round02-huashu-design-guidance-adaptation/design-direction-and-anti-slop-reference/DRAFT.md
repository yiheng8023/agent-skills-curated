# Design Direction And Anti Slop Reference Draft

Status: non-runtime adapted draft, not approved payload.

This draft is derived from reviewed MIT-licensed source
`github:alchaincyf/huashu-design` at pinned revision
`ec9ec0fff8a66a932c4049b200ea4c2b09f8d25b`. It summarizes and neutralizes the
reviewed source intent. It does not copy upstream source text as curated
payload.

## Candidate Shape

Use this future candidate when a design, prototype, presentation, or visual
artifact needs a quality guardrail for:

- grounding visual work in supplied context;
- generating meaningfully different directions before committing;
- avoiding generic AI-looking visual defaults;
- separating placeholders from real assets;
- reviewing output against audience, medium, and purpose.

This is a design-direction and anti-slop reference candidate. It should help an
agent ask better design questions and produce more inspectable visual options
without treating one source's full toolchain as portable payload.

## Intake Boundary

Before design work, bind:

- audience, medium, output format, and review surface;
- available design system, brand material, screenshots, codebase, or reference
  examples;
- whether the task asks for exploration, implementation, critique, or final
  production assets;
- whether current product facts or brand facts require verification;
- whether external images, generated images, browser automation, or file writes
  are authorized.

If context is missing, the output should expose assumptions and produce
directional options rather than pretending to know the final answer.

## Workflow

1. Classify the artifact type before selecting visual rules.
2. Prefer supplied context and real assets over generic styling.
3. Offer differentiated directions when the brief is under-specified.
4. Keep placeholder labels honest when source assets are absent.
5. Avoid decorative density that does not support the message.
6. Review the result against the user's medium, audience, and decision goal.
7. Keep final approval with the user or product/design owner.

## Must Not

- Do not hard-code a single visual style as universal good design.
- Do not rely on a tool-specific WebSearch name or agent-specific workflow.
- Do not treat upstream examples, demos, or aesthetic preferences as product
  truth.
- Do not use fake metrics, fake screenshots, or invented customer proof as
  visual filler.
- Do not imply that a design is production-ready without the required asset,
  accessibility, browser, and stakeholder checks.
- Do not import the Huashu HTML/media toolchain into the curated release from
  this design-guidance gate.

## Likely Release Direction

This draft is most likely a merge or reference candidate for existing design,
prototype, and review workflows. Before release, a separate gate must decide
whether the behavior becomes:

- a merge into `design-an-interface`;
- a merge into `prototype`;
- a review checklist;
- or reference-only guidance because overlap is too high.
