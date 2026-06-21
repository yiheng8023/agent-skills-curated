# Generated Routing Scenarios

Do not edit manually.

## recipe.telemetry-safety

Trigger: Logs, metrics, traces, alerts, or launch monitoring may contain sensitive data

- `capability.privacy-governance`
- `capability.observability` when collection purpose, minimization, redaction, retention, and access are defined
- `capability.security-scan` when telemetry crosses a new trust or external-service boundary

## recipe.production-launch

Trigger: A product or service change is approaching production

- `capability.observability` when production behavior needs evidence
- `capability.performance` when a performance target or regression risk exists
- `capability.ci-cd` when automated delivery gates are required
- `capability.security-scan` when the change crosses a security boundary
- `capability.production-launch` when readiness evidence is available

## recipe.contract-retirement

Trigger: An API, dependency, feature, or data contract is replaced or retired

- `capability.lifecycle-migration`
- `capability.tdd`
- `capability.observability`
- `capability.ci-cd`
- `capability.production-launch`
