# Lifecycle Capability Coverage

Do not edit manually.

| Capability | Stage | Coverage | Validation | Fallback |
| --- | --- | --- | --- | --- |
| `capability.architecture-design` | `design` | `curated` | Review the design against current domain language, decisions, and operational constraints. | Use the smallest reversible boundary change and document uncertainty. |
| `capability.backend-implementation` | `implement` | `native-sufficient` | Run repository-defined tests, static checks, and contract verification. | Implement a smaller reversible slice and report unavailable execution support. |
| `capability.ci-cd` | `deliver` | `curated` | Run the delivery workflow in its governed environment and inspect gate evidence. | Provide a reproducible manual gate sequence without claiming automated delivery. |
| `capability.code-review` | `verify` | `curated` | Inspect the bounded change set and verify actionable findings against repository evidence. | Narrow the review scope and state which change surfaces remain unreviewed. |
| `capability.cross-agent-handoff` | `coordinate` | `curated` | Verify that the receiver can identify scope, current truth, uncertainties, and allowed next actions. | Provide a minimal evidence-linked status summary and request receiver confirmation. |
| `capability.data-modeling` | `design` | `recipe` | Require domain and storage experts to review invariants and lifecycle assumptions. | Compose requirements and architecture modeling, then avoid irreversible schema commitments until accountable review. |
| `capability.documentation-governance` | `govern` | `curated` | Cross-check updated documentation with authoritative repository and decision records. | Mark stale or uncertain statements and retain traceable source references. |
| `capability.fault-diagnosis` | `recover` | `curated` | Confirm the causal explanation with instrumentation and a passing regression test. | Minimize the reproduction and report competing hypotheses with evidence gaps. |
| `capability.frontend-design` | `design` | `runtime-resolved` | Probe the live environment for an authorized design workflow and verify the rendered result. | Provide an implementation-neutral interaction specification and preserve design uncertainty. |
| `capability.interface-api-design` | `design` | `recipe` | Evaluate alternatives against callers, failure modes, compatibility, and testability. | Expose the narrowest reversible interface and defer unsupported flexibility. |
| `capability.issue-triage` | `operate` | `curated` | Confirm classification and ownership against the issue lifecycle policy. | Keep the issue uncommitted to a solution and request missing evidence. |
| `capability.knowledge-capture` | `evolve` | `recipe` | Review captured knowledge for provenance, sensitivity, freshness, and retrieval value. | Keep a local evidence note and defer durable publication until reviewed. |
| `capability.migration-deprecation` | `evolve` | `curated` | Verify compatibility, adoption, removal gates, and affected-subject communication. | Preserve compatibility and delay irreversible removal until evidence is sufficient. |
| `capability.observability` | `operate` | `curated` | Verify that critical behaviors and failures are visible without exposing restricted data. | Add bounded diagnostic evidence for the critical path and document blind spots. |
| `capability.open-format-knowledge-files` | `evolve` | `curated` | Check Markdown/YAML/JSON syntax, Obsidian-specific assumptions, link/embed uncertainty, and write authority before claiming a usable artifact. | Return a patch-ready proposal and mark parser, renderer, vault, or write-authority gaps explicitly. |
| `capability.performance` | `verify` | `curated` | Compare reproducible measurements with an explicit budget or baseline. | Report the measurement boundary and avoid unsupported performance claims. |
| `capability.prd-rfc` | `define` | `curated` | Review scope, outcomes, constraints, alternatives, and acceptance evidence. | Keep the document in draft and identify missing decision authority. |
| `capability.privacy-governance` | `govern` | `human-authority` | Obtain approval from the accountable privacy or legal authority before consequential processing. | Minimize collection and pause processing that lacks a valid authority decision. |
| `capability.problem-decomposition` | `plan` | `curated` | Check that each slice has inputs, outputs, dependencies, and observable completion. | Retain the larger outcome and mark decomposition gaps instead of inventing tasks. |
| `capability.release-readiness` | `deliver` | `curated` | Confirm explicit go or no-go authority, acceptance evidence, monitoring, and recovery readiness. | Hold the release and identify the smallest missing readiness evidence. |
| `capability.requirements-clarification` | `discover` | `curated` | Confirm unresolved questions and acceptance boundaries with the responsible subject. | Record assumptions and stop decisions that depend on unanswered questions. |
| `capability.retrospective-evolution` | `evolve` | `native-sufficient` | Compare intended and actual outcomes, then assign measurable follow-up changes. | Record observed outcomes and unresolved causes for later accountable review. |
| `capability.rollback-recovery` | `recover` | `recipe` | Exercise the recovery path and verify state integrity plus restored service objectives. | Stop further change, contain impact, and escalate to the accountable operator. |
| `capability.security-audit` | `verify` | `runtime-resolved` | Probe for an authorized security workflow and validate findings from source to impact. | Perform a bounded manual threat review and recommend specialist review for unresolved risk. |
| `capability.spec-driven-development` | `define` | `recipe` | Acceptance criteria, assumptions, work slices, selected capability path, and final verification are traceable. | Use native reasoning with a lightweight acceptance checklist when the task is small or already scoped. |
| `capability.tdd` | `implement` | `curated` | Capture a failing test before the minimal implementation and rerun it after refactoring. | Add the smallest reproducible regression test before changing behavior. |
| `capability.technical-debt` | `evolve` | `curated` | Tie proposed debt work to observable risk, cost, ownership, and verification. | Record the debt with impact and defer mutation until authority and capacity exist. |
| `capability.test-strategy` | `verify` | `recipe` | Trace each material risk to an executable check and an evidence owner. | Prioritize critical-path integration checks and disclose untested risks. |
