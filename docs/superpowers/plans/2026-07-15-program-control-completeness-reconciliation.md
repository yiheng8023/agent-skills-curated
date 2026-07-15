# Program Control Completeness Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Audit and correct the long-lived curation control plan before ordering further rounds, so evidence-backed demand, native and external alternatives, residual-gap proof, curated admission, consumer feedback, and CALIBRATION delivery form one traceable system without turning historical Round 02 execution into the permanent program architecture.

**Architecture:** Preserve `registry/curation-program-plan.json` as the single machine program authority and `registry/program-acceptance-map.json` as its acceptance projection. Separate stable operating lanes from bounded initiatives and historical rounds; retain Round 02 truth, but do not use its local runtime transaction as the universal final stage. Extend the existing verifier instead of creating a second controller.

**Tech Stack:** Python 3 standard library, JSON registries, Markdown evidence, `unittest`, existing deterministic repository verifier.

## Global Constraints

- Work only on `codex/round02-closeout-reconciliation` in the existing isolated worktree.
- Audit completeness before changing execution order or starting external candidate discovery.
- Do not inspect or mutate live Agent environments, user configuration repositories, `YIYUAN-CALIBRATION`, `YIYUAN-ASSETS`, or upstream radar repositories in this slice.
- Treat `C:\tmp\agent-skills-curated-capability-survey-handoff-20260714.md` as historical navigation evidence, not current repository authority.
- Preserve existing Round 02 execution and approval records; do not rewrite historical facts.
- Distinguish platform/runtime/vendor first-party baselines from repository-authored gap-fill candidates.
- Permit a repository-authored Skill candidate only after an evidence-backed residual gap, alternative comparison, bounded design, review, validation, and owner approval.
- Keep official, runtime-owned, built-in, plugin-owned, and platform/vendor first-party Skill bodies outside curated inventory.
- Keep broad multi-domain curation in scope; human-AI collaboration shortfalls are one demand lane, not the entire repository mission.
- Keep consumer projection optional and consumer-owned; current live parity is never inferred from dated execution evidence.
- Keep research and standard-candidate custody directed to `YIYUAN-CALIBRATION`, with project admission remaining in `YIYUAN-ASSETS`.
- Do not commit, merge, push, publish, install, or perform cross-repository writes without a separately authorized closeout action.

---

### Task 1: Record The Completeness Audit Before Redesign

**Files:**
- Create: `docs/program-control-plan-completeness-audit-2026-07-15.md`
- Reference: `registry/curation-program-plan.json`
- Reference: `registry/program-acceptance-map.json`
- Reference: `registry/curation-expansion-rounds.json`
- Reference: `docs/curation-harness-model.md`

**Interfaces:**
- Consumes: current repository authority plus the bound capability-survey handoff.
- Produces: a non-authoritative evidence audit with requirement IDs, current coverage, defects, severity, and exact authority surfaces to revise.

- [x] **Step 1: Create a requirement ledger**

Record these stable requirement families with IDs and evidence:

```text
PCR-01 terminal and matrix role
PCR-02 broad multi-domain coverage
PCR-03 evidence-backed demand and shortfall coordinates
PCR-04 native, official, runtime, and installed baseline comparison
PCR-05 broad discovery, clustering, deduplication, and stopping rule
PCR-06 native / single-Skill / composition / non-Skill comparison
PCR-07 residual-gap proof before repository-authored implementation
PCR-08 third-party and repository-authored candidate governance
PCR-09 admission, release, rollback, and consumer projection boundary
PCR-10 multi-Agent evidence and claim limits
PCR-11 feedback, refresh, deprecation, replacement, and retirement
PCR-12 standard extraction and YIYUAN-CALIBRATION delivery
PCR-13 decision-ready external-brain projection and cognitive-load reduction
PCR-14 sequence, reroute, acceptance, and closeout integrity
PCR-15 bounded initiative/result-package management
```

- [x] **Step 2: Classify each requirement**

Use only `covered`, `partial`, `missing`, `misplaced`, or `conflicting`. Cite exact repository paths and explain why green verification does or does not cover the requirement.

- [x] **Step 3: Record structural findings**

At minimum, assess:

```text
stable program architecture is conflated with historical Round 02 steps
local runtime alignment is consumer evidence, not a mandatory universal terminal
capability-survey demand, baseline, comparison, and gap-proof chain is absent
repository-authored gap-fill admission is absent
objective count is verifier-hard-coded to six
sequence prerequisites are prose rather than governed data
required survey result package is absent from program acceptance
```

- [x] **Step 4: Validate the audit against source evidence**

Run:

```powershell
rg -n "PCR-01|PCR-15|covered|partial|missing|misplaced|conflicting" docs/program-control-plan-completeness-audit-2026-07-15.md
```

Expected: all fifteen requirement IDs and all used classifications are visible.

### Task 2: Add Failing Completeness Contracts

**Files:**
- Modify: `tests/test_verify_integration.py`
- Test: `tests/test_verify_integration.py`

**Interfaces:**
- Consumes: `validate_curation_program_plan` and `validate_program_acceptance_map`.
- Produces: regression tests for extensible objectives, stable operating lanes, bounded initiatives, source-origin policy, sequence gates, and capability-survey acceptance.

- [x] **Step 1: Require the missing strategic objectives**

Add a test asserting that the program contains:

```python
required = {
    "objective.multi-domain-coverage",
    "objective.evidence-backed-demand-model",
    "objective.reuse-before-build-gap-proof",
    "objective.full-chain-capability-coverage",
    "objective.decision-ready-external-brain",
}
self.assertTrue(required <= {item["id"] for item in program["strategicObjectives"]})
```

- [x] **Step 2: Prove the objective set is extensible**

Add a test that appends a structurally valid future objective and matching acceptance-map record, then calls the two validators directly. Expected: the validators accept additions and do not require exactly six objectives.

- [x] **Step 3: Require stable operating lanes and initiative separation**

Add tests that reject:

```text
an operating model without demand-baseline, solution-comparison, residual-gap-decision, or calibration-handoff lanes
a current initiative without prerequisites, blocked actions, result package, and decision gate
consumer runtime sync represented as a mandatory stable operating lane
```

- [x] **Step 4: Require repository-authored gap-fill governance**

Add a mutation test that changes the repository-authored candidate eligibility gate from `residual-gap-supported` to `discovery-only` and expect `RuntimeError` containing `residual gap`.

- [x] **Step 5: Require capability-survey acceptance coverage**

Add a test requiring acceptance IDs for native baseline, candidate clustering, alternative comparison, residual-gap proof, result-package completeness, and claim limits.

- [x] **Step 6: Run the focused tests and confirm red**

Run:

```powershell
python -B -m unittest tests.test_verify_integration.StructuralValidationIntegrationTests -v
```

Expected: the new completeness tests fail because the program does not yet contain the required structures.

### Task 3: Separate Stable Program Architecture From Bounded Initiatives

**Files:**
- Modify: `registry/curation-program-plan.json`
- Modify: `scripts/verify.py`
- Test: `tests/test_verify_integration.py`

**Interfaces:**
- Produces: `programArchitecture`, `candidateOriginPolicy`, `sequenceGates`, and `currentInitiatives` inside the existing program authority.

- [x] **Step 1: Add stable operating lanes**

Add these ordered lane IDs under `programArchitecture.operatingLanes`:

```json
[
  "lane.demand-evidence",
  "lane.native-official-runtime-baseline",
  "lane.discovery-and-clustering",
  "lane.representative-deep-review",
  "lane.solution-alternative-comparison",
  "lane.residual-gap-decision",
  "lane.candidate-governance-and-adaptation",
  "lane.admission-verification-and-release",
  "lane.consumer-evidence-and-feedback",
  "lane.lifecycle-metabolism",
  "lane.standard-extraction-and-calibration-handoff"
]
```

Each lane must declare purpose, required inputs, allowed outputs, blocked transitions, verification surface, and reroute triggers. Consumer projection must be optional downstream evidence, not an unconditional lane exit requirement.

- [x] **Step 2: Add bounded initiative records**

Add:

```text
initiative.round02-stage-closeout-reconciliation: active, preserves historical Round 02 evidence and blocks new candidate intake
initiative.capability-survey-gap-proof: planned, permits plan and acceptance design now but blocks discovery execution until prerequisites close
```

The capability-survey result package must enumerate the ten deliverables from the bound handoff: native baseline, clustered candidates, STM/P/SG coverage, single/composed alternatives, dispositions, residual gaps, evidence limits, intent/router/closure/Hook recommendations, stop/recheck rules, and non-authorization statement.

- [x] **Step 3: Add candidate-origin policy**

Represent four distinct classes:

```text
platform-runtime-vendor-first-party-baseline
third-party-candidate
repository-authored-gap-fill-candidate
curated-approved-release
```

Require `residual-gap-supported`, alternative comparison, overlap/security/portability review, tests, and owner approval before a repository-authored candidate can enter curated admission.

- [x] **Step 4: Add machine sequence gates**

Require these prerequisites:

```text
demand evidence before capability-gap claims
native/runtime baseline before external-substitution decisions
clustering before representative deep review
alternative comparison before residual-gap support
residual-gap support before repository-authored design
admission evidence before release
release evidence before optional consumer projection
repeated evidence before standard extraction
CALIBRATION handoff before any ASSETS admission claim
stage closeout before activating the next candidate-intake round
```

- [x] **Step 5: Make strategic objectives extensible**

Replace the exact-length validator with a required-core-ID subset check, uniqueness checks, and reference closure. Add the five missing objectives without removing the six existing objectives.

- [x] **Step 6: Run focused tests**

Run:

```powershell
python -B -m unittest tests.test_verify_integration.StructuralValidationIntegrationTests -v
```

Expected: stable architecture tests pass; acceptance coverage tests remain red until Task 4.

### Task 4: Extend Acceptance To Cover The Whole Decision Chain

**Files:**
- Modify: `registry/program-acceptance-map.json`
- Modify: `scripts/verify.py`
- Test: `tests/test_verify_integration.py`

**Interfaces:**
- Consumes: the eleven strategic objectives and two current initiatives.
- Produces: acceptance and verification coverage for PCR-01 through PCR-15 without falsely upgrading future work.

- [x] **Step 1: Add missing acceptance criteria**

Add stable IDs for:

```text
acceptance.multi-domain-coverage
acceptance.demand-coordinate-contract
acceptance.native-runtime-baseline
acceptance.discovery-clustering-stop-rule
acceptance.alternative-comparison
acceptance.residual-gap-proof
acceptance.repository-authored-gap-fill-gate
acceptance.full-chain-coverage-matrix
acceptance.decision-ready-consumer-projection
acceptance.capability-survey-result-package
acceptance.cross-agent-claim-limits
acceptance.sequence-integrity
```

- [x] **Step 2: Preserve honest assessments**

Use `verified` only for multi-domain registry evidence and newly machine-validated sequence structure. Use `partial` for discovery infrastructure and decision-ready projection. Use `planned` for demand coordinates, native baselines, alternative comparison, residual-gap proof, repository-authored gap-fill execution, survey result package, and cross-Agent behavioral proof.

- [x] **Step 3: Add verification methods and evidence requirements**

Every new criterion must map to a verification record. Behavioral claims must require dated host, model, reasoning, loader, permission, workspace, and comparison evidence; metadata similarity must never count as behavioral coverage.

- [x] **Step 4: Validate objective and initiative coverage**

Extend `validate_program_acceptance_map` so all strategic objectives remain reference-closed and every current initiative declares acceptance IDs that resolve to criteria.

- [x] **Step 5: Run focused tests**

Run:

```powershell
python -B -m unittest tests.test_verify_integration.StructuralValidationIntegrationTests -v
```

Expected: PASS.

### Task 5: Reconcile Human Projections Without Starting The Survey

**Files:**
- Modify: `docs/curation-program-plan.md`
- Modify: `docs/curation-harness-model.md`
- Modify: `docs/coverage-and-curation-expansion.md`
- Modify: `policies/intake.md`
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `scripts/verify.py`

**Interfaces:**
- Consumes: corrected machine program and acceptance map.
- Produces: public-safe projections of the stable architecture, current initiative portfolio, reuse-before-build decision chain, and sequencing boundary.

- [x] **Step 1: Replace the misleading universal delivery sequence**

Show the stable loop as demand evidence through CALIBRATION handoff. Explain that Round 02 local runtime alignment is historical consumer-side evidence, not the permanent last program stage.

- [x] **Step 2: Document the reuse-before-build decision chain**

Use:

```text
evidenced demand or shortfall
-> native / official / runtime baseline
-> external discovery and clustering
-> representative deep review
-> native / single / composition / non-Skill comparison
-> residual-gap decision
-> adopt, adapt, compose, reference, reject, hold, or repository-author
```

- [x] **Step 3: Document current initiative ordering**

State that completeness reconciliation is current, Round 02 closeout remains the next execution gate, and capability-survey discovery execution cannot begin until those prerequisites close. Planning and acceptance design may proceed without external discovery.

- [x] **Step 4: Add bilingual public positioning**

Explain broad multi-domain scope, decision-ready external-brain output, reduced enumeration burden, repository-authored gap-fill boundary, cross-Agent claim limits, and CALIBRATION custody without promising universal Agent equality or model-ceiling improvement.

Clarify in `policies/intake.md` that a repository-authored gap-fill is a candidate origin inside the same non-executable candidate state, not a new release layer and not the platform/runtime/vendor first-party baseline class.

- [x] **Step 5: Extend projection verification**

Require stable concepts rather than exact prose, including `reuse before build`, `residual gap`, `repository-authored`, `capability survey`, `optional consumer projection`, and `YIYUAN-CALIBRATION`.

### Task 6: Full Verification And Decision-Gate Package

**Files:**
- Modify only if verification exposes an in-scope defect.
- Verify all files changed in Tasks 1-5.

**Interfaces:**
- Produces: a reviewed master-plan correction ready for user authorization to commit and merge; does not start candidate discovery or close Round 02.

- [x] **Step 1: Run deterministic verification**

```powershell
python -B scripts/verify.py
python -B scripts/build_topology.py --check
python -B scripts/build_release_manifest.py --check
python -B scripts/simulate_routing.py --all
python -B -m unittest discover -s tests -v
git diff --check
```

Expected: all commands pass, topology and release manifest remain current, and routing behavior remains unchanged.

- [x] **Step 2: Audit changed surfaces**

Confirm no changes under `skills/`, no release-manifest change, no generated topology change, no live runtime write, no external discovery execution, and no cross-repository write.

- [x] **Step 3: Produce the next decision gate**

Report:

```text
master-plan defects found and corrected
remaining planned or partial acceptance
why Round 02 closeout is or is not still the next gate
what capability-survey planning may proceed in parallel
which actions still need explicit authorization
```

- [x] **Step 4: Pause before Git closeout**

Do not commit, merge, push, or delete the worktree until the user reviews the corrected master-plan package and separately authorizes the Git action.
