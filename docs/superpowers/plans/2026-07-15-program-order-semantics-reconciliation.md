# Program Order Semantics Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the master control plan express prerequisite order, safe parallelism, optional branches, cross-cutting feedback, and the actual current initiative without turning the recurring program into a false linear conveyor.

**Architecture:** Keep `registry/curation-program-plan.json` as the single machine authority. Add explicit execution semantics and per-lane dependency modes around the existing lanes, strengthen source pinning before deep review, and bind the current completeness reconciliation separately from the historical Round 02 step. Extend the existing acceptance map and verifier rather than introducing another scheduler.

**Tech Stack:** Python 3 standard library, JSON registries, Markdown evidence, `unittest`, existing deterministic repository verifier.

## Global Constraints

- Work only in the existing isolated worktree on `codex/round02-closeout-reconciliation`.
- Do not start Round 02 closeout, capability discovery, candidate execution, Skill authoring, runtime mutation, or cross-repository delivery.
- Preserve all historical Round 01 and Round 02 records as dated evidence.
- Treat upstream resource-radar discovery as an independent producer; this repository governs candidate intake and decisions only after its own demand, authority, and evidence gates are satisfied.
- Consumer projection is optional, lifecycle metabolism is cross-cutting, and standard extraction is a conditional evidence branch.
- Third-party representative deep review requires an exact source pin and license/provenance boundary before executable surfaces are inspected; inspection is not execution.
- Do not commit, merge, push, publish, install, or mutate another repository without separate authorization.

---

### Task 1: Record The Order-Semantics Audit

**Files:**
- Create: `docs/program-order-semantics-audit-2026-07-15.md`
- Reference: `registry/curation-program-plan.json`
- Reference: `registry/program-acceptance-map.json`

**Interfaces:**
- Consumes: the verified completeness correction and current repository truth.
- Produces: ordered findings `POS-01` through `POS-08` and exact correction requirements.

- [x] **Step 1: Record the dependency questions**

Cover core prerequisites, parallel work, optional branches, cross-cutting loops, source-trust timing, current initiative truth, closeout boundaries, and upstream radar separation.

- [x] **Step 2: Classify the current ordering**

Use `correct`, `ambiguous`, `misordered`, or `missing`; distinguish an array display order from executable dependency semantics.

- [x] **Step 3: Record the bounded conclusion**

State that the audit does not authorize Git closeout, Round 02 execution, external discovery, runtime mutation, or cross-repository work.

---

### Task 2: Add Failing Order-Semantics Tests

**Files:**
- Modify: `tests/test_verify_integration.py`
- Modify later: `scripts/verify.py`

**Interfaces:**
- Consumes: `validate_curation_program_plan` through the existing integration-test fixture.
- Produces: mutation tests that fail when current initiative, lane modes, dependencies, source pinning, or non-linear branches drift.

- [x] **Step 1: Require the actual current initiative**

Add a test requiring `currentInitiativeId == "initiative.program-control-completeness-reconciliation"` and a matching initiative whose status is `needs-user-confirmation`.

- [x] **Step 2: Require dependency-graph semantics**

Add a test requiring `executionSemantics.model == "dependency-graph-with-optional-and-cross-cutting-lanes"`, the eight-lane core path, the optional consumer branch, cross-cutting lifecycle lane, and conditional standard-extraction branch.

- [x] **Step 3: Reject false consumer prerequisites**

Mutate lifecycle inputs to require both release and consumer evidence and assert a `RuntimeError` containing `lifecycle` and `consumer`.

- [x] **Step 4: Require source pinning before deep review**

Remove the exact-pin requirement from representative deep review and assert a `RuntimeError` containing `source pin`.

- [x] **Step 5: Run the focused tests and confirm red**

Run: `python -B -m unittest tests.test_verify_integration.StructuralValidationIntegrationTests -v`

Expected: only the new order-semantics tests fail before implementation.

---

### Task 3: Implement Machine Order Semantics

**Files:**
- Modify: `registry/curation-program-plan.json`
- Modify: `scripts/verify.py`

**Interfaces:**
- Consumes: the audit and failing tests.
- Produces: `currentInitiativeId`, `executionSemantics`, lane dependency metadata, a source-pin gate, and deterministic validation.

- [x] **Step 1: Bind the current initiative separately from historical steps**

Add `currentInitiativeId` and a first current-initiative record for completeness reconciliation. Preserve `currentStep` as historical Round 02 execution posture rather than treating it as the active control initiative.

- [x] **Step 2: Add dependency-graph semantics**

Define the core path as demand, baseline, discovery, representative review, alternative comparison, residual-gap decision, candidate governance, and admission/release. Define consumer projection as optional, lifecycle as cross-cutting, and standards extraction as conditional on repeated evidence.

- [x] **Step 3: Add lane modes and dependencies**

For every lane add `executionMode` and `dependsOn`. For lifecycle and standards extraction add `triggerInputsAnyOf`; do not require consumer evidence for lifecycle or a release for standards extraction.

- [x] **Step 4: Strengthen pre-review trust ordering**

Require an exact source pin plus license/provenance boundary for third-party deep review and add `gate.source-pin-before-deep-review` between clustering and alternatives.

- [x] **Step 5: Validate the new structure**

Extend `validate_curation_program_plan` to check initiative identity, dependency closure, lane modes, branch semantics, source pinning, and the eleven sequence gates without hard-coding historical steps as the stable path.

- [x] **Step 6: Run focused tests**

Run: `python -B -m unittest tests.test_verify_integration.StructuralValidationIntegrationTests -v`

Expected: all focused tests pass.

---

### Task 4: Reconcile Acceptance And Human Projections

**Files:**
- Modify: `registry/program-acceptance-map.json`
- Modify: `docs/curation-program-plan.md`
- Modify: `docs/curation-harness-model.md`
- Modify: `docs/coverage-and-curation-expansion.md`
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `scripts/verify.py`

**Interfaces:**
- Consumes: verified machine semantics.
- Produces: honest acceptance status and matching bilingual explanations.

- [x] **Step 1: Add the current-control acceptance gate**

Add `acceptance.program-control-completeness` with assessment `partial`: technical correction and verification exist, while owner review and Git closeout remain pending. Reference it from the full-chain objective and current initiative.

- [x] **Step 2: Document graph semantics**

Explain the eight-lane core path, safe parallel work within bounded stages, optional consumer projection, cross-cutting lifecycle metabolism, conditional standards extraction, and initiative closeout before the next intake round.

- [x] **Step 3: Document upstream radar separation**

State that broad radar discovery may continue upstream, but this repository does not turn a radar signal into a candidate decision before demand, baseline, source-trust, and review gates.

- [x] **Step 4: Extend projection verification**

Require the stable concepts `dependency graph`, `optional branch`, `cross-cutting`, `source pin`, and `current initiative` in the relevant projections without forcing identical bilingual prose.

---

### Task 5: Verify And Pause At The Human Gate

**Files:**
- Verify: all changed files

**Interfaces:**
- Consumes: Tasks 1 through 4.
- Produces: a technically verified order-semantics correction ready for owner review, not an approved or merged baseline.

- [x] **Step 1: Run deterministic verification**

Run:

```text
python -B scripts/verify.py
python -B scripts/build_release_manifest.py --check
python -B scripts/build_topology.py --check
python -B scripts/simulate_routing.py --all
python -B -m unittest discover -s tests -v
git diff --check
```

Expected: all commands pass; generated and release artifacts remain current.

- [x] **Step 2: Audit changed surfaces**

Confirm no changes under `skills/`, no release-manifest or generated-topology change, no external discovery execution, no runtime write, and no cross-repository write.

- [x] **Step 3: Stop before Git closeout**

Report findings, evidence, dirty branch state, deferred work, and the exact owner decision required before commit and merge.
