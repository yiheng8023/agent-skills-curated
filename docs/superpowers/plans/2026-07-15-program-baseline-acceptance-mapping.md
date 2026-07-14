# Program Baseline And Acceptance Mapping Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reconcile the repository's program state with Round 02 evidence, expand the existing curation program into the agreed Skills-terminal MVP mainline, and make every strategic objective traceable to acceptance criteria, verification methods, and evidence without claiming unfinished work is complete.

**Architecture:** Keep `registry/curation-program-plan.json` as the single machine-readable program authority and keep bounded execution in `registry/curation-expansion-rounds.json`. Add one distinct authority surface, `registry/program-acceptance-map.json`, for stable objective-to-acceptance-to-verification-to-evidence relationships. Human-readable Markdown remains a projection; `scripts/verify.py` validates references, evidence posture, state reconciliation, and projection coverage instead of hard-coding an obsolete active step.

**Tech Stack:** Python 3 standard library, JSON registries, Markdown documentation, `unittest`, existing deterministic repository verifier.

## Global Constraints

- Work only in `C:\Projects\agent-skills-curated` for this slice.
- Do not discover, install, enable, sync, delete, or execute external Skills, MCP servers, Apps, Plugins, or Hooks.
- Do not inspect or mutate live Codex, Claude, Trae, WorkBuddy, cc Switch, account, credential, memory, plugin-cache, or runtime state.
- Do not write to `YIYUAN-MERIDIAN`, `resource-radar`, `YIYUAN-CALIBRATION`, `YIYUAN-ASSETS`, or consumer configuration repositories in this implementation slice. This transaction boundary does not change `YIYUAN-CALIBRATION` as the intended durable custody target for later research and standard-candidate delivery.
- Preserve official, runtime-owned, built-in, plugin-owned, and first-party Skill bodies as environment-owned dated baselines only.
- Treat the existing Round 02 local sync record as execution evidence, not as proof of a completed stage closeout or current live state.
- Keep Skills as the first terminal MVP, not the boundary of the broader MERIDIAN funnel and not the only future terminal.
- Treat project hard standards as a future project-owned path: this repository may produce standard candidate packages for separately authorized delivery to `YIYUAN-CALIBRATION`, but does not admit, publish, or install ASSETS hard standards. Consumer configuration repositories are evidence and feedback surfaces, not durable standards custody.
- Use plan -> execute -> acceptance -> stage closeout; do not upgrade status without cited evidence.
- Keep repository-facing canonical prose in English and maintain the Chinese README projection.

---

### Task 1: Add Failing Contract Tests For The New Program Truth

**Files:**
- Modify: `tests/test_verify_integration.py`
- Test: `tests/test_verify_integration.py`

**Interfaces:**
- Consumes: `verify_script.REQUIRED_FILES`, `verify_script.load`, and `verify_script.verify`.
- Produces: regression tests requiring `registry/program-acceptance-map.json`, reference integrity, evidence-backed verified assessments, and non-obsolete Round 02 reconciliation.

- [ ] **Step 1: Add the acceptance-map required-input test**

```python
def test_program_acceptance_map_is_a_required_verifier_input(self) -> None:
    self.assertIn(
        "registry/program-acceptance-map.json",
        verify_script.REQUIRED_FILES,
    )
```

- [ ] **Step 2: Add a dangling objective-to-acceptance rejection test**

```python
def test_rejects_program_objective_with_unknown_acceptance_reference(self) -> None:
    path = "registry/program-acceptance-map.json"
    document = verify_script.load(path)
    document["objectives"][0]["acceptanceIds"] = ["acceptance.missing"]
    self.assert_verify_runtime_error(path, document, "unknown acceptance id")
```

- [ ] **Step 3: Add evidence sufficiency and current-state tests**

```python
def test_rejects_verified_program_acceptance_without_evidence(self) -> None:
    path = "registry/program-acceptance-map.json"
    document = verify_script.load(path)
    criterion = document["acceptanceCriteria"][0]
    criterion["assessment"] = "verified"
    criterion["evidenceIds"] = []
    self.assert_verify_runtime_error(path, document, "verified acceptance requires evidence")

def test_round02_waits_for_closeout_instead_of_claiming_active_execution(self) -> None:
    rounds = verify_script.load("registry/curation-expansion-rounds.json")
    round02 = next(item for item in rounds["rounds"] if item["id"] == "round-02-source-intake-and-filtering")
    self.assertEqual(round02["status"], "needs-closeout")
    self.assertEqual(round02["lifecycle"]["execute"], "closed")
    self.assertEqual(round02["lifecycle"]["acceptance"], "passed")
    self.assertEqual(round02["lifecycle"]["stageCloseout"], "pending")
```

- [ ] **Step 4: Add the mutation helper used by the new tests**

```python
def assert_verify_runtime_error(
    self,
    path: str,
    mutation: dict[str, object],
    message: str,
) -> None:
    original_load = verify_script.load

    def load_with_mutation(candidate: str) -> dict[str, object]:
        if candidate == path:
            return deepcopy(mutation)
        return original_load(candidate)

    with patch.object(verify_script, "load", side_effect=load_with_mutation):
        with self.assertRaisesRegex(RuntimeError, message):
            verify_script.verify()
```

- [ ] **Step 5: Run the focused tests and confirm they fail for the missing contract**

Run: `python -B -m unittest tests.test_verify_integration.StructuralValidationIntegrationTests -v`

Expected: FAIL because `registry/program-acceptance-map.json` and its validation do not exist, and Round 02 still claims active execution.

- [ ] **Step 6: Commit the failing test boundary**

```bash
git add tests/test_verify_integration.py
git commit -m "test: define program acceptance mapping contract"
```

### Task 2: Reconcile Program And Round State Without False Closeout

**Files:**
- Modify: `registry/curation-program-plan.json`
- Modify: `registry/curation-expansion-rounds.json`
- Modify: `registry/round-lifecycle-contract.json`
- Modify: `scripts/verify.py`
- Test: `tests/test_verify_integration.py`

**Interfaces:**
- Consumes: `registry/round02-approved-payload-routing-proposal.json` and `registry/round02-local-runtime-sync-execution.json` as bounded historical evidence.
- Produces: a truthful current program position and a reusable lifecycle state model that permits `needs-closeout` without claiming `complete`.

- [ ] **Step 1: Change Round 02 to evidence-recorded closeout pending**

Use this state in `registry/curation-expansion-rounds.json`:

```json
{
  "currentRound": "round-02-source-intake-and-filtering",
  "status": "needs-closeout",
  "lifecycle": {
    "plan": "recorded",
    "execute": "closed",
    "acceptance": "passed",
    "stageCloseout": "pending"
  },
  "evidence": [
    "registry/round02-release-admission-candidate-review.json",
    "registry/round02-approved-payload-routing-proposal.json",
    "registry/round02-local-runtime-sync-execution.json"
  ],
  "nextGate": "round-02-stage-closeout-reconciliation"
}
```

Keep Round 03 planned. Replace the obsolete sync deferral with a consumer boundary that states local integration is consumer-owned and the dated Round 02 record is not current live-state proof.

- [ ] **Step 2: Reconcile the reusable lifecycle application**

Set `registry/round-lifecycle-contract.json#currentApplication` to:

```json
{
  "roundRegistry": "registry/curation-expansion-rounds.json",
  "currentRound": "round-02-source-intake-and-filtering",
  "phaseState": "stage_closeout_pending",
  "stageCloseout": "needs_reconciliation",
  "evidence": [
    "registry/round02-approved-payload-routing-proposal.json",
    "registry/round02-local-runtime-sync-execution.json"
  ],
  "deferredActions": [
    "claiming Round 02 stage closeout",
    "claiming current live runtime parity",
    "starting a new candidate intake round before closeout reconciliation"
  ],
  "nextRequiredEvidence": [
    "Round 02 requirement-by-requirement closeout reconciliation",
    "explicit residual-risk and deferred-work record",
    "next-round or pause decision"
  ]
}
```

- [ ] **Step 3: Move the program current position to closeout reconciliation**

Keep the six delivery stages, but use these statuses in `registry/curation-program-plan.json`:

```json
{
  "currentStep": "program-06-local-runtime-alignment-closeout",
  "currentState": "needs-reconciliation",
  "stepStatuses": {
    "program-01-discovery-and-coverage": "complete",
    "program-02-source-intake-and-filtering": "evidence-recorded",
    "program-03-review-and-adaptation": "evidence-recorded",
    "program-04-curated-admission-and-release": "evidence-recorded",
    "program-05-consumer-projection-readiness": "evidence-recorded",
    "program-06-local-runtime-alignment-closeout": "needs-reconciliation"
  }
}
```

Do not use `complete` for steps 02-06 until the closeout record proves every mapped acceptance item.

- [ ] **Step 4: Replace hard-coded obsolete status validation**

Update `validate_curation_expansion_rounds`, `validate_curation_program_plan`, and `validate_round_lifecycle_contract` so they validate allowed state transitions and evidence requirements. Required statuses are:

```python
ROUND_STATUSES = {"planned", "active", "needs-closeout", "closed"}
PROGRAM_STEP_STATUSES = {
    "planned",
    "active",
    "evidence-recorded",
    "needs-reconciliation",
    "complete",
}
```

Require `needs-closeout` rounds to have closed execution, passed acceptance, pending stage closeout, non-empty evidence, and an explicit next gate. Require `evidence-recorded` and `needs-reconciliation` program steps to cite closeout evidence or the current reconciliation surface.

- [ ] **Step 5: Run the focused tests**

Run: `python -B -m unittest tests.test_verify_integration.StructuralValidationIntegrationTests -v`

Expected: the Round 02 state test passes; acceptance-map tests still fail until Task 3.

- [ ] **Step 6: Commit the state reconciliation**

```bash
git add registry/curation-program-plan.json registry/curation-expansion-rounds.json registry/round-lifecycle-contract.json scripts/verify.py tests/test_verify_integration.py
git commit -m "fix: reconcile curation program state with round 02 evidence"
```

### Task 3: Add The Strategic Objective And Acceptance Mapping Authority

**Files:**
- Create: `registry/program-acceptance-map.json`
- Modify: `registry/curation-program-plan.json`
- Modify: `scripts/verify.py`
- Test: `tests/test_verify_integration.py`

**Interfaces:**
- Consumes: stable objective IDs declared in `registry/curation-program-plan.json`.
- Produces: `validate_program_acceptance_map(document, program_doc)` and a machine-readable trace from objectives to acceptance, verification, and evidence.

- [ ] **Step 1: Add the agreed strategic positioning to the existing program authority**

Add these objective IDs to `registry/curation-program-plan.json`:

```json
[
  "objective.skills-terminal-mvp",
  "objective.reviewed-third-party-governance",
  "objective.multi-agent-consumer-mapping",
  "objective.layered-collaboration-reliability",
  "objective.standard-candidate-extraction",
  "objective.lifecycle-metabolism"
]
```

For each objective record `statement`, `authorityOwner`, `nonGoals`, and `acceptanceIds`. State explicitly that broad discovery is upstream-owned, live installation is consumer-owned, project hard-standard admission is project-owned, and future non-Skill terminals are outside this repository's current release authority.

- [ ] **Step 2: Create `registry/program-acceptance-map.json`**

Use this exact top-level contract:

```json
{
  "schema": 1,
  "id": "curation-program-acceptance-map-v1",
  "programPlan": "registry/curation-program-plan.json",
  "assessmentVocabulary": [
    "planned",
    "partial",
    "verified",
    "stale",
    "blocked",
    "not-applicable"
  ],
  "objectives": [],
  "acceptanceCriteria": [],
  "verifications": [],
  "evidence": []
}
```

Populate all six objectives. Every objective must reference at least one acceptance criterion; every criterion must reference at least one verification; every verification must declare `method`, `expectedResult`, and `evidenceRequirement`. Evidence records must contain `id`, `path`, `kind`, `asOf`, and `supports`.

Use `partial` for multi-Agent consumer mapping, layered reliability, standards candidate extraction, and lifecycle metabolism until future implementation evidence exists. Use `verified` only for repository-role and third-party-governance criteria supported by current checked-in files and deterministic checks.

- [ ] **Step 3: Implement reference and evidence validation**

Add:

```python
def validate_program_acceptance_map(
    document: dict[str, object],
    program_doc: dict[str, object],
) -> None:
    """Validate objective -> acceptance -> verification -> evidence traceability."""
```

The function must reject duplicate IDs, unknown references, objectives with no acceptance IDs, criteria with no verification IDs, unknown assessment values, missing evidence files, future `asOf` dates, and `verified` criteria with no evidence IDs. It must also require the objective ID set to equal the strategic objective ID set in the program plan.

- [ ] **Step 4: Load and validate the map from `verify()`**

Add `registry/program-acceptance-map.json` to `REQUIRED_FILES`, load it immediately after the program plan, and call:

```python
validate_program_acceptance_map(
    program_acceptance_map_doc,
    curation_program_plan_doc,
)
```

- [ ] **Step 5: Run the focused contract tests**

Run: `python -B -m unittest tests.test_verify_integration.StructuralValidationIntegrationTests -v`

Expected: PASS.

- [ ] **Step 6: Commit the acceptance authority**

```bash
git add registry/program-acceptance-map.json registry/curation-program-plan.json scripts/verify.py tests/test_verify_integration.py
git commit -m "feat: map program objectives to acceptance evidence"
```

### Task 4: Update Human Projections And Public Positioning

**Files:**
- Modify: `docs/curation-program-plan.md`
- Modify: `docs/curation-harness-model.md`
- Modify: `docs/round-lifecycle-contract.md`
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `scripts/verify.py`

**Interfaces:**
- Consumes: the machine-readable program and acceptance map.
- Produces: public-safe human projections that explain the funnel position, first-terminal MVP, multi-Agent boundary, layered reliability, and standards-candidate handoff without claiming external repositories are modified.

- [ ] **Step 1: Rewrite the program current-position section**

State that Round 02 has execution and acceptance evidence but awaits explicit stage-closeout reconciliation. Link the three evidence records and `registry/program-acceptance-map.json`. Remove the obsolete claim that source intake is the active execution step.

- [ ] **Step 2: Expand the harness without expanding repository authority**

Add this model to `docs/curation-harness-model.md`:

```text
broader resource discovery
-> Skill candidate governance
-> reviewed Skill terminal release
-> consumer-owned projection
-> usage and failure feedback
-> revise, update, deprecate, retire, or extract a standard candidate
```

Explain that Skills are the first low-burden terminal MVP; future terminals may reuse upstream governance but are not released by this repository. Explain that standard candidates may be exported as evidence packages for durable custody and calibration in `YIYUAN-CALIBRATION`, while `YIYUAN-ASSETS` project admission remains a separate authority decision. Consumer configuration repositories must not become their long-term home.

- [ ] **Step 3: Document the layered collaboration reliability model**

Record this authority order:

```text
instructions and rules
-> Skills and Recipes
-> scripts, schemas, and validators
-> consumer hooks, CI, or runtime controls
-> project-owned hard standards
-> evidence and accountable human decisions
```

State that a project-owned hard standard overrides conflicting generic Skill guidance, and that this repository does not own runtime instruction discovery or project standard admission.

- [ ] **Step 4: Update both README projections**

Add concise repository-role language covering the first-terminal MVP, internal-and-external Skill audience, multi-Agent evidence requirement, the non-custodial consumer-configuration role, and the `YIYUAN-CALIBRATION` standard-candidate delivery boundary. Do not add ASSETS-private standard bodies or private environment details.

- [ ] **Step 5: Update verifier phrase coverage**

Replace obsolete phrase assertions with checks for stable concepts:

```python
required_program_concepts = [
    "first terminal MVP",
    "program-acceptance-map.json",
    "stage-closeout reconciliation",
]
required_harness_concepts = [
    "broader resource discovery",
    "standard candidate",
    "project-owned hard standards",
    "future terminals",
]
```

- [ ] **Step 6: Run focused and repository verification**

Run: `python -B -m unittest tests.test_verify_integration -v`

Expected: PASS.

Run: `python -B scripts/verify.py`

Expected: `Agent Skills Curated validation passed.`

- [ ] **Step 7: Commit the projections**

```bash
git add README.md README.zh-CN.md docs/curation-program-plan.md docs/curation-harness-model.md docs/round-lifecycle-contract.md scripts/verify.py
git commit -m "docs: align curation mainline with the skills terminal MVP"
```

### Task 5: Full Verification And Planning-Slice Closeout

**Files:**
- Modify only if verification exposes an in-scope defect.
- Verify: all files changed by Tasks 1-4.

**Interfaces:**
- Consumes: updated program authority, round state, acceptance map, verifier, and projections.
- Produces: evidence that this planning slice is internally consistent; it does not prove multi-Agent local inventory, external discovery, standards extraction, or future implementation complete.

- [ ] **Step 1: Run deterministic repository verification**

Run: `python -B scripts/verify.py`

Expected: `Agent Skills Curated validation passed.`

- [ ] **Step 2: Check generated topology and release manifest remain unchanged and current**

Run: `python -B scripts/build_topology.py --check`

Expected: `Generated topology is current.`

Run: `python -B scripts/build_release_manifest.py --check`

Expected: `Release manifest is current.`

- [ ] **Step 3: Run routing and all unit tests**

Run: `python -B scripts/simulate_routing.py --all`

Expected: all checked-in scenarios pass.

Run: `python -B -m unittest discover -s tests -v`

Expected: PASS with no failures or errors.

- [ ] **Step 4: Check repository diff quality**

Run: `git diff --check`

Expected: no output.

Run: `git status --short`

Expected: only the intended program-baseline, acceptance-map, verifier, test, documentation, and plan files are changed.

- [ ] **Step 5: Perform requirement-by-requirement closeout**

Confirm all of the following from current files and command output:

```text
single program authority preserved
Round 02 not falsely marked complete
obsolete active-execution claim removed
six strategic objectives represented
every objective maps to acceptance and verification
verified assessments cite existing evidence
unfinished implementation remains partial or planned
live Agent and external repository state remains untouched
release payload, manifest, topology, and routing behavior remain unchanged
```

- [ ] **Step 6: Commit any final in-scope correction**

```bash
git add README.md README.zh-CN.md docs registry scripts tests
git commit -m "chore: close program baseline acceptance mapping slice"
```

Only create this final commit if Step 5 required an additional correction; otherwise leave the prior task commits as the complete review series.
