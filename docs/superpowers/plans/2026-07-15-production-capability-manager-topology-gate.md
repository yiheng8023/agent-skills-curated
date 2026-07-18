# Production Capability Manager Topology Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Record the accepted Manager written design, produce a current MERIDIAN topology-impact package, and make the repository block Manager creation or product implementation until the package receives a separate owner decision.

**Outcome update (2026-07-15):** The owner accepted the topology-impact package. The acceptance event and source-pinned ecosystem/stack review now replace the review-pending gate with separate final-slug, stack, repository-creation, implementation-slice, and cross-repository transaction gates. The historical steps below retain the pre-acceptance execution sequence.

**Architecture:** Keep `registry/curation-program-plan.json` as program authority and `registry/program-acceptance-map.json` as traceability authority. Add one immutable owner design-decision event and one dated topology-impact package with a Markdown projection. Extend the existing Python verifier so the gate is deterministic while all cross-repository and product implementation work remains disabled.

**Tech Stack:** Python 3 standard library, JSON registries, Markdown specifications, PowerShell read-only Git/GitHub inventory, existing repository verifier and `unittest` suite.

## Global Constraints

- Work only in `C:\Projects\agent-skills-curated`.
- Treat `35ddb1e367c2f6e4dc913e6707191e2df7017f2a` as the pre-transaction repository base, not as the accepted topology package.
- Do not create or initialize a Manager repository.
- Do not choose a final repository slug, implementation language, packaging stack, or GUI framework without the topology decision and bounded prototype evidence.
- Do not write `YIYUAN-MERIDIAN`, radar, bookmark, user-config, template, CALIBRATION, ASSETS, or live runtime state.
- Do not execute or install candidate code, enable a Hook, connect an account, mutate credentials, commit, push, publish, release, or deploy.
- Keep the active Round 03 capability survey as the machine-bound current initiative; Manager topology work is an authorized design-only side initiative.
- Keep repository-facing canonical prose in English and discuss review results with the user in Chinese.

---

### Task 1: Record Written-Design Acceptance

**Files:**
- Create: `registry/production-capability-manager-design-acceptance-event-2026-07-15.json`
- Modify: `docs/superpowers/specs/2026-07-15-production-capability-manager-design.md`
- Modify: `registry/program-acceptance-map.json`
- Modify: `scripts/verify.py`
- Test: `tests/test_verify_integration.py`

**Interfaces:**
- Consumes: owner review in the current task and the revised written design.
- Produces: `production-capability-manager-design-acceptance-event-2026-07-15` and a `verified` design-contract assessment without implementation authority.

- [ ] **Step 1: Add the failing required-file assertion**

```python
def test_manager_design_acceptance_event_is_required(self) -> None:
    self.assertIn(
        "registry/production-capability-manager-design-acceptance-event-2026-07-15.json",
        verify_script.REQUIRED_FILES,
    )
```

- [ ] **Step 2: Run the focused test and verify the missing contract fails**

Run: `python -B -m unittest tests.test_verify_integration.StructuralValidationIntegrationTests.test_manager_design_acceptance_event_is_required -v`

Expected: FAIL because the acceptance event is not yet a required verifier input.

- [ ] **Step 3: Add the acceptance event and bind its authorization booleans**

Require these values in `validate_production_capability_manager_design_acceptance_event`:

```python
expected_authorization = {
    "recordDesignAcceptanceAuthorized": True,
    "currentRepositoryEvidenceWritesAuthorized": True,
    "readOnlyCrossRepositoryTopologyInventoryAuthorized": True,
    "topologyImpactPackagePreparationAuthorized": True,
    "topologyGateImplementationPlanAuthorized": True,
    "managerRepositoryCreationAuthorized": False,
    "managerProductImplementationAuthorized": False,
    "crossRepositoryWriteAuthorized": False,
    "hookEnablementOrLiveRuntimeMutationAuthorized": False,
    "thirdPartyCodeExecutionAuthorized": False,
    "commitAuthorized": False,
    "remotePushAuthorized": False,
}
```

- [ ] **Step 4: Change design evidence from pending review to owner accepted**

Set the design status to `Owner accepted; topology-impact review pending` and set `acceptance.manager-design-contract` to `verified` with both the written design and owner acceptance event as evidence.

- [ ] **Step 5: Run the focused integration suite**

Run: `python -B -m unittest tests.test_verify_integration.StructuralValidationIntegrationTests -v`

Expected: PASS.

### Task 2: Add The Dated MERIDIAN Topology-Impact Package

**Files:**
- Create: `registry/production-capability-manager-topology-impact-package-2026-07-15.json`
- Create: `docs/superpowers/specs/2026-07-15-production-capability-manager-topology-impact.md`
- Modify: `registry/program-acceptance-map.json`
- Modify: `registry/curation-program-plan.json`
- Modify: `docs/curation-program-plan.md`
- Modify: `scripts/verify.py`
- Test: `tests/test_verify_integration.py`

**Interfaces:**
- Consumes: read-only local Git posture, authenticated GitHub repository metadata, current MERIDIAN README, radar consumer contract, bookmark boundary, and the accepted Manager design.
- Produces: a dated node/edge/authority/version/Actions/rollback/retirement package whose `status` is `owner-review-pending` and whose implementation booleans remain false.

- [ ] **Step 1: Add a failing topology-package required-file assertion**

```python
def test_manager_topology_impact_package_is_required(self) -> None:
    self.assertIn(
        "registry/production-capability-manager-topology-impact-package-2026-07-15.json",
        verify_script.REQUIRED_FILES,
    )
```

- [ ] **Step 2: Run the new test and verify it fails**

Run: `python -B -m unittest tests.test_verify_integration.StructuralValidationIntegrationTests.test_manager_topology_impact_package_is_required -v`

Expected: FAIL because the topology package is not yet a required verifier input.

- [ ] **Step 3: Add the machine package and human projection**

The machine package must include `snapshot`, `proposedAuthority`, `proposedEdges`, `publicPrivateBoundary`, `versionAndRelease`, `githubActionsBoundary`, `acceptanceResponsibility`, `rollbackAndRetirement`, `requiredFutureCrossRepositoryUpdates`, `observedDrift`, `ownerDecisionRequired`, and `verification`.

- [ ] **Step 4: Validate fail-closed topology state**

Require:

```python
if document.get("status") != "owner-review-pending":
    raise RuntimeError("Manager topology package must remain owner-review-pending.")
if document.get("repositoryCreationAuthorized") is not False:
    raise RuntimeError("Manager repository creation must remain unauthorized.")
if document.get("productImplementationAuthorized") is not False:
    raise RuntimeError("Manager product implementation must remain unauthorized.")
```

Also require at least the MERIDIAN, radar, bookmarks, curated, Codex consumer,
Claude consumer, CALIBRATION, and ASSETS node classes; reject an executable
candidate or observation edge; require rollback, retirement, Actions, version,
public/private, acceptance, and unresolved owner-decision sections.

- [ ] **Step 5: Run the focused integration suite**

Run: `python -B -m unittest tests.test_verify_integration.StructuralValidationIntegrationTests -v`

Expected: PASS.

### Task 3: Reconcile Program And Acceptance Projections

**Files:**
- Modify: `registry/curation-program-plan.json`
- Modify: `registry/program-acceptance-map.json`
- Modify: `docs/curation-program-plan.md`
- Modify: `docs/superpowers/specs/2026-07-15-production-capability-manager-design.md`
- Modify: `scripts/verify.py`

**Interfaces:**
- Consumes: the design acceptance event and topology-impact package.
- Produces: a planned Manager initiative that records design acceptance and topology-package review pending while preserving `initiative.capability-survey-gap-proof` as active.

- [ ] **Step 1: Bind the Manager initiative decision evidence**

Add:

```json
{
  "designDecisionEvidence": "registry/production-capability-manager-design-acceptance-event-2026-07-15.json",
  "topologyImpactPackage": "registry/production-capability-manager-topology-impact-package-2026-07-15.json",
  "topologyDecisionState": "owner-review-pending"
}
```

Keep the initiative `status` as `planned` and retain every blocked action.

- [ ] **Step 2: Add topology evidence to the acceptance map**

Add `evidence.production-capability-manager-design-acceptance` and
`evidence.production-capability-manager-topology-impact`. The design criterion
becomes `verified`; the topology gate remains verified as an enforced gate,
while the topology evidence kind explicitly says `owner-review-pending`.

- [ ] **Step 3: Update the human program projection**

State that the written design is accepted, the topology package is prepared,
the package awaits separate review, and repository creation and implementation
remain blocked.

- [ ] **Step 4: Run deterministic repository verification**

Run: `python -B scripts/verify.py`

Expected: `Agent Skills Curated validation passed.`

### Task 4: Verify And Stop At The Owner Gate

**Files:**
- Verify: all files changed by Tasks 1-3.
- Do not modify another repository.

**Interfaces:**
- Consumes: updated design, decision event, topology package, plan, acceptance map, and verifier.
- Produces: review-ready evidence only; no Manager implementation.

- [ ] **Step 1: Check generated release surfaces remain current**

Run: `python -B scripts/build_release_manifest.py --check`

Expected: `Release manifest is current.`

Run: `python -B scripts/build_topology.py --check`

Expected: `Generated topology is current.`

- [ ] **Step 2: Run routing and all tests**

Run: `python -B scripts/simulate_routing.py --all`

Expected: all checked-in scenarios pass.

Run: `python -B -m unittest discover -s tests -v`

Expected: PASS with no failures or errors.

- [ ] **Step 3: Check diff quality and scope**

Run: `git diff --check`

Expected: no output.

Run: `git status --short`

Expected: only the accepted design transaction, topology package, plan,
program/acceptance projections, verifier, and focused tests are changed.

- [ ] **Step 4: Stop before product implementation**

Report `needs owner confirmation` for the topology package. Do not create a
repository, select the final stack, edit another repository, commit, or push.
