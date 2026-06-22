# Generated Routing Scenarios

Do not edit manually.

## recipe.interface-api-design

Trigger: A component boundary or API needs alternatives evaluated without a dedicated duplicate Skill

- `capability.requirements-clarification`
- `capability.architecture-design`
- `capability.code-review` when a candidate contract or implementation exists

## recipe.data-modeling

Trigger: A system needs explicit entities, invariants, ownership, retention, and change semantics without adding an overlapping dedicated Skill

- `capability.requirements-clarification`
- `capability.architecture-design`
- `capability.privacy-governance` when personal, confidential, regulated, or retention-sensitive data is involved
- `capability.code-review` when a schema, contract, or migration candidate exists

## recipe.test-strategy

Trigger: A change needs risk-proportionate verification across test layers and delivery gates

- `capability.requirements-clarification`
- `capability.tdd` when behavior is being added or corrected
- `capability.performance` when a performance objective or regression risk exists
- `capability.security-audit` when a trust boundary or material threat changes
- `capability.ci-cd` when repeatable automated gates are required

## recipe.telemetry-safety

Trigger: Operational evidence may contain personal, confidential, regulated, or secret data

- `capability.privacy-governance`
- `capability.observability` when purpose, minimization, redaction, retention, and access are defined
- `capability.security-audit` when telemetry crosses a new trust boundary

## recipe.release

Trigger: A change is approaching a governed release boundary

- `capability.test-strategy`
- `capability.observability`
- `capability.performance` when a performance objective applies
- `capability.ci-cd`
- `capability.rollback-recovery`
- `capability.release-readiness`

## recipe.migration

Trigger: An interface, dependency, feature, data contract, or system is replaced or retired

- `capability.migration-deprecation`
- `capability.test-strategy`
- `capability.observability`
- `capability.rollback-recovery`
- `capability.release-readiness`

## recipe.rollback-recovery

Trigger: A failed change or incident requires controlled restoration of a known-safe state

- `capability.observability`
- `capability.fault-diagnosis` when safe restoration does not explain the cause
- `capability.test-strategy` when recovery behavior needs regression evidence

## recipe.knowledge-capture

Trigger: A completed decision, delivery, incident, or experiment produced reusable learning

- `capability.retrospective-evolution`
- `capability.documentation-governance` when learning changes an authoritative standard or operating path
- `capability.cross-agent-handoff` when another subject will continue the work
