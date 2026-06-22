# Cross-Agent Capability Lifecycle Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a third-party-only curated Skill release plus a cross-Agent capability decision system that covers the full software-engineering lifecycle, avoids native/official duplication, reasons over visible and discoverable ecosystem options, and passes strict structured and live natural-language simulations.

**Architecture:** `agent-skills-curated` remains the authority for third-party Skill bodies, admission evidence, abstract lifecycle taxonomy, semantic routing metadata, Recipes, and deterministic projections. `codex-user-config` consumes a pinned curated revision, applies portable routing invariants, installs the reviewed payload and routing projection, and verifies the live environment. Agent semantics perform intent interpretation; deterministic contracts constrain eligibility, overlap, risk, permissions, fallback, and evidence.

**Tech Stack:** Python 3 standard library, JSON Schema draft 2020-12, JSON registries, Markdown Skills and policy documents, `unittest`, Git, Codex CLI read-only ephemeral probes.

---

## Repository Transactions

Keep repository authority and commits separate:

1. Complete and publish the curated repository release first.
2. Pin the immutable curated commit in `codex-user-config`.
3. Verify and publish the configuration repository.
4. Install into the live Agent environment only after both repositories pass.

The release manifest remains schema 1 and contains only approved third-party
Skill payload files.

## File Responsibility Map

### `agent-skills-curated`

- `registry/skills.json`: approved third-party release inventory and identity.
- `registry/admissions.json`: source, native-increment, overlap, disposition,
  and review evidence for every reviewed third-party Skill.
- `registry/capabilities.json`: abstract software-lifecycle capabilities and
  coverage states; no official product ownership records.
- `registry/routing.json`: semantic routing contract for approved third-party
  Skills.
- `registry/scenarios.json`: structured adversarial routing scenarios.
- `registry/relations.json`, `registry/conflicts.json`, `registry/recipes.json`:
  topology, conflict, and composition truth.
- `schemas/v1/admissions.schema.json`, `schemas/v2/capabilities.schema.json`,
  `schemas/v1/routing.schema.json`, `schemas/v1/scenarios.schema.json`: checked-in
  contracts.
- `scripts/contracts.py`: shape and reference validators.
- `scripts/build_topology.py`: deterministic generated projections.
- `scripts/build_release_manifest.py`: deterministic schema-1 payload manifest.
- `scripts/simulate_routing.py`: deterministic policy simulation over structured
  scenarios.
- `generated/routing-index.json`: portable derived routing projection consumed
  by configuration/runtime integration.

### `codex-user-config`

- `AGENTS.md`: compact global invariants only.
- `skills/capability-router/SKILL.md`: reusable capability decision procedure.
- `skills/capability-router/references/routing-contract.md`: field meanings and
  decision order loaded only when detailed routing is required.
- `scripts/skills.py`: pinned release and routing-index materialization,
  verification, backup, and rollback.
- `scripts/verify_capability_router.py`: repository and scenario contract gate.
- `scripts/live_routing_probe.py`: read-only ephemeral Codex scenario runner and
  result classifier.
- `tests/fixtures/live-routing-scenarios.json`: strict natural-language probe
  set independent from curated structured scenarios.

---

### Task 1: Add Third-Party Admission And Abstract Capability Contracts

**Files:**
- Create: `schemas/v1/admissions.schema.json`
- Create: `schemas/v2/capabilities.schema.json`
- Create: `schemas/v1/routing.schema.json`
- Create: `schemas/v1/scenarios.schema.json`
- Modify: `registry/capabilities.json`
- Modify: `scripts/contracts.py`
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `docs/architecture.md`
- Modify: `policies/intake.md`
- Modify: `policies/overlap-resolution.md`
- Test: `tests/test_shape_contracts.py`
- Test: `tests/test_schema_parity.py`
- Test: `tests/test_references.py`
- Test: `tests/test_verify_integration.py`

- [ ] **Step 1: Write failing shape and parity tests**

Add tests that require:

```python
EXPECTED_COVERAGE_STATES = {
    "curated", "recipe", "runtime-resolved", "native-sufficient",
    "human-authority", "gap",
}
EXPECTED_DISPOSITIONS = {
    "approve", "merge", "recipe-only", "adapter-only", "reject",
}
EXPECTED_RISK_LEVELS = {"low", "medium", "high", "critical"}
```

Using isolated validator fixtures, assert that admission records require
`skill`, `source`, `thirdParty`,
`nativeBaselineCompared`, `nativeIncrement`, `overlapReviewed`, `disposition`,
`reviewRefs`, and `validated`; `thirdParty` and `validated` must be true for an
approved payload Skill. Assert that abstract capabilities reject
`canonicalOwner`, product names, and official/runtime Skill identifiers.

- [ ] **Step 2: Run the focused tests and confirm RED**

Run:

```powershell
python -B -m unittest tests.test_shape_contracts tests.test_schema_parity tests.test_references -v
```

Expected: FAIL because the new schemas and validators do not exist.

- [ ] **Step 3: Add checked-in schemas and validators**

Define closed JSON objects with these required routing fields:

```text
skill, aliases, positiveTriggers, negativeTriggers, contextRequirements,
inputs, outputs, sideEffects, validation, riskLevel, permissionsRequired,
fallback, humanConfirmWhen, languages, agentCompatibility,
lifecycleCapabilities
```

`aliases`, triggers, requirements, inputs, outputs, validation, fallback,
confirmation conditions, languages, compatibility, and lifecycle mappings are
non-empty arrays of non-empty strings. IDs use existing stable-ID patterns.

- [ ] **Step 4: Add schema parity and portable authority wording**

Make the checked-in schemas the validator sources for enums and patterns.
Update governance documents to state that the curated repository governs only
third-party Skill bodies, abstract capability taxonomy is product-neutral, and
official/runtime observations are dated review evidence rather than managed
inventory.

- [ ] **Step 5: Run focused and full contract tests**

Run:

```powershell
python -B -m unittest tests.test_shape_contracts tests.test_schema_parity tests.test_references tests.test_verify_integration -v
python -B -m unittest discover -s tests -v
```

Expected: PASS.

- [ ] **Step 6: Commit the contract foundation**

```powershell
git add schemas registry scripts tests AGENTS.md README.md README.zh-CN.md docs policies
git commit -m "feat: add third-party lifecycle routing contracts"
```

---

### Task 2: Model Complete Software-Engineering Lifecycle Coverage

**Files:**
- Modify: `registry/capabilities.json`
- Modify: `registry/relations.json`
- Modify: `registry/recipes.json`
- Modify: `registry/conflicts.json`
- Modify: `scripts/build_topology.py`
- Modify: `generated/catalog.md`
- Modify: `generated/topology.json`
- Modify: `generated/topology.mmd`
- Modify: `generated/routing-scenarios.md`
- Create: `generated/lifecycle-coverage.md`
- Test: `tests/test_lifecycle_coverage.py`

- [ ] **Step 1: Write the failing lifecycle completeness test**

Require these 26 stable capability IDs:

```text
capability.requirements-clarification
capability.prd-rfc
capability.problem-decomposition
capability.architecture-design
capability.interface-api-design
capability.data-modeling
capability.frontend-design
capability.backend-implementation
capability.tdd
capability.test-strategy
capability.code-review
capability.security-audit
capability.privacy-governance
capability.performance
capability.observability
capability.ci-cd
capability.release-readiness
capability.migration-deprecation
capability.rollback-recovery
capability.fault-diagnosis
capability.issue-triage
capability.documentation-governance
capability.knowledge-capture
capability.technical-debt
capability.cross-agent-handoff
capability.retrospective-evolution
```

Every node must have `stage`, `description`, `coverageState`, `validation`, and
`fallback`. `curatedOwners` is allowed only for `coverageState=curated` and must
resolve to approved third-party Skills. `runtime-resolved` nodes cannot name a
vendor or product owner.

- [ ] **Step 2: Run the lifecycle test and confirm RED**

```powershell
python -B -m unittest tests.test_lifecycle_coverage -v
```

Expected: FAIL with missing lifecycle IDs and forbidden external canonical
owners.

- [ ] **Step 3: Replace product ownership with abstract coverage states**

Reclassify the current capability records. Preserve useful abstract relations,
but remove `external:*` canonical ownership. Use `runtime-resolved` where the
current environment must choose native, official, plugin, App, MCP, or another
visible capability.

- [ ] **Step 4: Add minimal Recipes for lifecycle gaps that are compositions**

Keep the existing telemetry safety, production launch, and contract retirement
Recipes. Add Recipes only when two or more existing capabilities form a stable
ordered workflow; do not create a Skill merely to fill a taxonomy cell.

- [ ] **Step 5: Generate lifecycle coverage projection**

`generated/lifecycle-coverage.md` must group all 26 nodes by stage, show coverage
state, curated owner or runtime resolution, validation, fallback, and gaps.

- [ ] **Step 6: Verify deterministic generation**

```powershell
python -B scripts/build_topology.py
python -B scripts/build_topology.py --check
python -B -m unittest tests.test_lifecycle_coverage -v
```

Expected: PASS and no stale generated files.

- [ ] **Step 7: Commit the lifecycle topology**

```powershell
git add registry scripts generated tests/test_lifecycle_coverage.py
git commit -m "feat: model full engineering lifecycle coverage"
```

---

### Task 3: Re-Audit All Approved Third-Party Skills For Native Increment

**Files:**
- Create: `registry/admissions.json`
- Create: `registry/routing.json`
- Modify: `registry/skills.json`
- Modify as justified: `skills/*/SKILL.md`
- Modify: `registry/relations.json`
- Modify: `registry/conflicts.json`
- Modify: `sources/lock.json`
- Create: `audits/native-overlap/2026-06-22.md`
- Create: `tests/test_admission_completeness.py`
- Modify: `tests/test_manifest_contract.py`
- Modify: `scripts/contracts.py`
- Modify: `scripts/verify.py`

- [ ] **Step 1: Write the failing admission-completeness test**

For every current approved Skill, require one disposition and evidence for:

```text
source identity
third-party status
portable native baseline comparison
distinct native increment
current visible/runtime overlap snapshot
existing curated overlap
maintainability and validation
final disposition
review references
```

The test must reject generic statements such as “helps the Agent perform the
task” as a native increment.

- [ ] **Step 2: Run the test and confirm RED**

```powershell
python -B -m unittest tests.test_admission_completeness -v
```

Expected: FAIL until all current records are adjudicated.

- [ ] **Step 3: Review all 34 Skills against one rubric**

For each Skill, choose exactly one allowed disposition. Apply these rules:

- retain only a distinct repeatable workflow with testable artifacts;
- merge duplicated increments into one canonical Skill;
- convert pure orchestration to Recipe-only;
- move runtime-specific integration to adapter-only;
- reject generic native reasoning, ordinary editing, simple prompting, or an
  equivalent official/runtime workflow.

Record dated runtime overlap observations as evidence, not permanent official
inventory.

- [ ] **Step 4: Apply each retained Skill edit with Skill TDD**

Before editing an individual `SKILL.md`, add at least one routing scenario that
fails under the old description or boundary. Edit only that Skill, rerun its
scenario, and proceed only after it passes. Do not batch-edit multiple Skill
bodies without per-Skill evidence.

- [ ] **Step 5: Wire admission and routing truth into verification**

Load and shape-check both documents before semantic access. Require every
currently approved Skill to have exactly one `approve` admission and one routing
record. Preserve non-approved audit dispositions without placing them in
`registry/skills.json` or the payload. Record intended payload removals in the
audit; Task 4 performs the removal and manifest regeneration as one transaction.

- [ ] **Step 6: Verify admission closure**

```powershell
python -B -m unittest tests.test_admission_completeness tests.test_references -v
```

Expected: every retained Skill is approved with distinct native increment;
every non-retained Skill has an explicit non-runtime disposition.

- [ ] **Step 7: Commit the completed audit and retained Skill changes**

```powershell
git add audits registry sources skills tests
git commit -m "refactor: enforce native-increment skill admission"
```

---

### Task 4: Build Deterministic Routing And Release Projections

**Files:**
- Create: `scripts/build_release_manifest.py`
- Modify: `scripts/build_topology.py`
- Create: `generated/routing-index.json`
- Modify: `release-manifest.json`
- Create: `tests/test_release_builder.py`
- Create: `tests/test_routing_projection.py`

- [ ] **Step 1: Write failing builder tests**

Require the release builder to include exactly files beneath approved retained
third-party Skill roots, sort paths deterministically, compute SHA-256 and size,
reject links/reparse points and unregistered roots, and emit schema 1.

Require `generated/routing-index.json` to contain only abstract capabilities,
approved third-party routing metadata, Recipes, conflicts, relations, and a
digest map of its authoritative registry inputs. It must not contain official
Skill bodies, account state, installed-state claims, or plugin cache paths.

- [ ] **Step 2: Run tests and confirm RED**

```powershell
python -B -m unittest tests.test_release_builder tests.test_routing_projection -v
```

Expected: FAIL because builders and projection do not exist.

- [ ] **Step 3: Implement release-manifest generation**

Reuse canonical path, link/reparse, hashing, and approved-only checks from
`scripts/contracts.py`; do not create a second validator implementation.

Before generating, remove Skill directories whose completed Task 3 admission
disposition is not `approve`; remove their approved inventory, routing,
relations, and conflict membership. Fail if a removed Skill is still referenced
by a retained Recipe or capability owner.

- [ ] **Step 4: Extend deterministic topology rendering**

Render the routing index from authoritative registries. Include registry input
digests so the configuration consumer can reject a hand-edited or stale
projection.

- [ ] **Step 5: Regenerate and verify**

```powershell
python -B scripts/build_release_manifest.py
python -B scripts/build_topology.py
python -B scripts/build_topology.py --check
python -B scripts/verify.py
```

Expected: PASS; manifest remains schema 1; counts match retained approved
third-party Skills and files.

- [ ] **Step 6: Commit deterministic release evidence**

```powershell
git add scripts generated release-manifest.json tests
git commit -m "feat: generate deterministic routing and release projections"
```

---

### Task 5: Implement Strict Structured Routing Simulation

**Files:**
- Create: `scripts/simulate_routing.py`
- Create: `registry/scenarios.json`
- Create: `tests/test_routing_simulation.py`
- Modify: `scripts/contracts.py`
- Modify: `scripts/verify.py`
- Modify: `.github/workflows/validate.yml`

- [ ] **Step 1: Write failing policy-simulation tests**

The deterministic resolver accepts structured facts, not raw-language NLP:

```python
decision = resolve({
    "requestedCapabilities": ["capability.release-readiness"],
    "available": ["native", "runtime", "curated"],
    "context": ["readiness evidence exists"],
    "risk": "high",
    "permissions": ["read"],
    "conflicts": [],
})
```

It returns one of `native`, `runtime`, `curated`, `recipe`, `no-skill`,
`ask-user`, or `gap`, plus selected IDs, exclusions, confirmation reason,
validation, and fallback.

- [ ] **Step 2: Run tests and confirm RED**

```powershell
python -B -m unittest tests.test_routing_simulation -v
```

Expected: FAIL because the resolver does not exist.

- [ ] **Step 3: Implement fail-closed eligibility and precedence**

Apply context requirements and negative triggers before scoring. Prefer an
equivalent healthy native/runtime path over curated content. Require Recipe for
ordered complementary capabilities. Return `ask-user` for high/critical risk,
permission expansion, unresolved conflict, or ambiguity. Return `gap` only
after fallbacks are exhausted.

- [ ] **Step 4: Populate at least 96 structured scenarios**

The corpus must include every lifecycle node and these minimum families:

```text
26 direct lifecycle coverage cases
12 native/no-Skill overlap cases
12 visible runtime/official preference cases
12 curated distinct-workflow cases
8 Recipe/DAG composition cases
10 negative-trigger and near-match false-positive cases
8 ambiguity/conflict/human-confirm cases
8 unavailable/fallback/gap cases
```

Across the corpus require Chinese, English, mixed language, colloquial intent,
conversation references, missing context, risk, cost, permissions, and side
effects.

- [ ] **Step 5: Run the complete simulation**

```powershell
python -B scripts/simulate_routing.py --all --report generated/routing-simulation-report.json
python -B -m unittest tests.test_routing_simulation -v
```

Expected: 96 or more scenarios PASS with no unclassified lifecycle node.

- [ ] **Step 6: Commit the simulation gate**

```powershell
git add scripts registry generated/routing-simulation-report.json tests .github/workflows/validate.yml
git commit -m "test: add adversarial lifecycle routing simulation"
```

---

### Task 6: Fill Only Verified Lifecycle Gaps From Reviewed Third-Party Sources

**Files:**
- Modify as evidence requires: `sources/lock.json`
- Create per source: `sources/<source-id>/selection.json`
- Create per source: `audits/<source-id>/<revision>/security.md`
- Create per source: `audits/<source-id>/<revision>/portability.md`
- Create per source: `audits/<source-id>/<revision>/overlap.md`
- Create per approved Skill: `skills/<neutral-name>/SKILL.md`
- Modify: `registry/admissions.json`
- Modify: `registry/skills.json`
- Modify: `registry/routing.json`
- Modify: `registry/capabilities.json`
- Modify: `registry/relations.json`
- Modify as composition requires: `registry/recipes.json`
- Modify: `registry/scenarios.json`
- Test: `tests/test_gap_intake.py`

- [ ] **Step 1: Write the failing gap-intake test**

Fail when a lifecycle node remains `gap` without a dated search decision, or
when an approved newly sourced Skill lacks source pin, license, provenance,
security, sensitive-data review, neutralization, portability, native/runtime
overlap, existing-curated overlap, naming, Skill TDD, and routing scenarios.

- [ ] **Step 2: Confirm whether discovery is necessary**

Run the complete lifecycle and routing simulation. For every `gap`, evaluate in
order: native-sufficient, visible runtime-resolved, existing curated mapping,
and Recipe composition. Search externally only when all four fail.

- [ ] **Step 3: Perform targeted GitHub discovery for each remaining gap**

Use capability-specific searches and trusted source evidence. Record candidate
repository, immutable commit, license, maintenance posture, and the exact gap
it may fill. Do not clone or install a candidate into the live Agent
environment during discovery.

- [ ] **Step 4: Apply the complete third-party intake gate**

Inspect every executable surface and instruction boundary. Remove credentials,
personal data, author-specific paths, organization assumptions, vendor lock-in,
and Agent-specific commands that are not essential. Preserve license,
provenance, safety, permission, and real environment constraints. Rename using
a neutral verb-first or capability-specific name and record the upstream name
as provenance, not runtime identity.

- [ ] **Step 5: Choose one disposition per candidate**

Use only `approve`, `merge`, `recipe-only`, `adapter-only`, or `reject`.
Approval requires a distinct native increment and full validation. Prefer merge
or Recipe when a new Skill body would duplicate an existing workflow.

- [ ] **Step 6: Test each approved Skill independently**

For each approved candidate, run baseline routing scenarios before adding the
Skill, observe the expected gap, add the minimal neutralized Skill, rerun the
same scenarios, add negative and overlap scenarios, then run the full suite.

- [ ] **Step 7: Iterate until coverage closes or human authority is explicit**

Repeat Tasks 2-6 when new conflicts or gaps appear. A node may finish as
`human-authority`, `native-sufficient`, or `runtime-resolved`; a Skill is not
required merely to eliminate the word `gap`.

- [ ] **Step 8: Commit each independently reviewed source batch**

```powershell
git add sources audits skills registry tests
git commit -m "feat: fill reviewed lifecycle capability gap"
```

---

### Task 7: Make `codex-user-config` Consume The Routing Projection

**Files:**
- Modify: `AGENTS.md`
- Modify: `skills/capability-router/SKILL.md`
- Create: `skills/capability-router/references/routing-contract.md`
- Modify: `scripts/skills.py`
- Modify: `scripts/install.py`
- Modify: `scripts/verify_capability_router.py`
- Modify: `scripts/verify_skills_install.py`
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Test: `tests/test_routing_index_install.py`

- [ ] **Step 1: Write failing installation and Router contract tests**

Require `scripts/skills.py` to verify curated routing-index input digests at the
pinned commit, back up and install it to
`~/.agents/capability-routing-index.json`, include it in the rollback
transaction, and verify it after writing.

Require Router wording for the exact decision sequence and the distinction
between visible-callable, visible-unavailable, discoverable-uninstalled,
historical, and unknown capabilities.

- [ ] **Step 2: Run focused tests and confirm RED**

```powershell
python -B -m unittest tests.test_routing_index_install -v
python -B scripts/verify_capability_router.py
```

Expected: FAIL because the projection is not consumed and detailed Router
reference does not exist.

- [ ] **Step 3: Extend pinned source verification and transaction rollback**

The Git commit pin proves source identity; input digests prove generated
projection parity. Installation remains explicit, backup-first, hash-verified,
and reversible. Release payload installation and routing-index installation are
recorded in one transaction without adding generated files to the schema-1
payload manifest.

- [ ] **Step 4: Refine AGENTS and Router responsibilities**

Keep global instructions compact. Put field definitions and detailed decision
order in the Router reference. State that Agent semantics interpret language;
keywords are retrieval aids; unavailable options are recommendations only; and
official/runtime content is never governed by the curated repository.

- [ ] **Step 5: Run configuration verification**

```powershell
python -B scripts/verify_capability_router.py
python -B scripts/verify_skills_install.py
python -B scripts/verify.py
```

Expected: PASS.

- [ ] **Step 6: Commit configuration-side consumption**

```powershell
git add AGENTS.md README.md README.zh-CN.md skills scripts tests
git commit -m "feat: consume curated capability routing projection"
```

---

### Task 8: Publish Curated Release And Pin Configuration

**Files:**
- Modify: `C:/Projects/codex-user-config/config/skills-source.json`
- Modify: `C:/Projects/codex-user-config/README.md`
- Modify: `C:/Projects/codex-user-config/README.zh-CN.md`

- [ ] **Step 1: Run the full curated verification gate**

```powershell
python -B -m unittest discover -s tests -v
python -B scripts/build_topology.py --check
python -B scripts/verify.py
git diff --check
```

Expected: PASS and only intended commits on the feature branch.

- [ ] **Step 2: Merge the curated feature branch to `main`**

Fetch origin, verify `main` has not diverged unexpectedly, fast-forward local
`main` to the reviewed feature branch, rerun the full gate, and push
`origin/main`. Do not force-push.

- [ ] **Step 3: Pin the exact curated `main` commit in configuration**

Update `config/skills-source.json.revision` to the pushed immutable commit.
Update documented Skill counts only from the generated schema-1 manifest.

- [ ] **Step 4: Run a local-source install plan before remote verification**

```powershell
python -B scripts/skills.py --source C:\tmp\agent-skills-curated-work plan
```

Expected: deterministic add/replace/unchanged classification with no writes.

- [ ] **Step 5: Verify the remote pinned source**

```powershell
python -B scripts/skills.py plan
python -B scripts/verify_skills_install.py
python -B scripts/verify.py
```

Expected: remote checkout resolves exactly to the new pin and passes manifest
and routing-index verification.

- [ ] **Step 6: Commit and push the configuration pin**

```powershell
git add config/skills-source.json README.md README.zh-CN.md
git commit -m "chore: pin lifecycle-routed curated skills release"
git push origin main
```

---

### Task 9: Install Live Configuration With Backup And Rollback Evidence

**Files affected outside repositories:**
- `~/.codex/AGENTS.md`
- `~/.agents/skills/capability-router/`
- `~/.agents/skills/<retained-curated-skill>/`
- `~/.agents/capability-routing-index.json`
- `~/.agents/curated-skills-transaction.json`
- `~/.agents/curated-skills-backups/<timestamp>/`

- [ ] **Step 1: Record pre-install hashes and inventory**

Capture SHA-256 for live AGENTS, Router, managed Skill files, routing index if
present, and current managed transaction. Store the report under a temporary
local verification directory; do not commit device paths.

- [ ] **Step 2: Install global AGENTS and Router without enabling the Hook**

```powershell
python -B scripts/install.py
```

Expected: AGENTS and Router installed; Hook remains disabled.

- [ ] **Step 3: Apply the pinned curated release**

```powershell
python -B scripts/skills.py install --apply
python -B scripts/skills.py verify
```

Expected: backup-first transaction, exact retained Skill count, routing index
installed, and post-write hashes verified.

- [ ] **Step 4: Verify live hashes and rollback plan**

```powershell
python -B scripts/skills.py rollback
```

Expected: dry-run rollback plan succeeds without modifying live files.

- [ ] **Step 5: Restart the Agent surface**

Fully exit and reopen Codex so instruction discovery and Skill inventory are
rebuilt. This is the only required user-controlled transition; resume the same
closure workflow after restart.

---

### Task 10: Run Strict Fresh-Agent Natural-Language Simulation

**Files:**
- Create: `C:/Projects/codex-user-config/tests/fixtures/live-routing-scenarios.json`
- Create: `C:/Projects/codex-user-config/scripts/live_routing_probe.py`
- Create locally: `C:/tmp/capability-routing-live-report.json`
- Test: `C:/Projects/codex-user-config/tests/test_live_routing_probe.py`

- [ ] **Step 1: Write failing probe-runner tests**

The runner must invoke:

```text
codex exec --ephemeral --sandbox read-only --ask-for-approval never
```

with a JSON output schema that permits only:

```text
decisionClass, capabilities, selectedSkills, excludedSkills,
confirmationRequired, confirmationReason, validation, fallback, rationale
```

It must reject tool execution, filesystem mutation, network action, fabricated
availability, and outputs that treat candidates or uninstalled options as
active.

- [ ] **Step 2: Run tests and confirm RED**

```powershell
python -B -m unittest tests.test_live_routing_probe -v
```

Expected: FAIL because the runner and fixture do not exist.

- [ ] **Step 3: Create at least 32 adversarial fresh-session prompts**

Include:

```text
4 Chinese colloquial or implicit requests
4 English technical requests
4 mixed-language and project-term requests
4 negative/near-match false positives
4 native-versus-Skill overlap decisions
4 visible-versus-uninstalled ecosystem decisions
4 ambiguity/conflict/permission/high-risk decisions
4 Recipe/fallback/gap decisions
```

Each fixture declares allowed decision classes, required exclusions,
confirmation expectation, and forbidden claims.

- [ ] **Step 4: Run every prompt in an independent ephemeral session**

```powershell
python -B scripts/live_routing_probe.py --all --report C:\tmp\capability-routing-live-report.json
```

Expected: all 32 or more sessions PASS; no external actions; every failure
contains the exact prompt, observed output, and contract mismatch.

- [ ] **Step 5: Perform variance runs**

Repeat the eight highest-risk or most ambiguous prompts three times each.
Require the same decision class and confirmation posture in all three runs;
allow different prose and equivalent capability ordering.

- [ ] **Step 6: Diagnose and fix any failure at the owning layer**

Fix taxonomy errors in curated registries, eligibility errors in routing
metadata, decision-order errors in Router instructions, and availability errors
in live integration. Add the failing prompt as a permanent regression fixture,
then rerun structured and live suites.

- [ ] **Step 7: Commit only portable fixtures and runner**

Do not commit model transcripts, account state, device paths, tokens, or raw
session logs.

```powershell
git add scripts/live_routing_probe.py tests
git commit -m "test: add strict live capability routing probes"
git push origin main
```

---

### Task 11: Final Cross-Repository Closure

**Files:**
- Update as generated: repository verification reports only

- [ ] **Step 1: Run all curated gates from a clean `main`**

```powershell
python -B -m unittest discover -s tests -v
python -B scripts/build_topology.py --check
python -B scripts/verify.py
git diff --check
git status --short --branch
```

Expected: all PASS and clean synchronized `main`.

- [ ] **Step 2: Run all configuration gates**

```powershell
python -B scripts/verify_capability_router.py
python -B scripts/verify.py
python -B scripts/verify_skills_install.py
python -B scripts/memory.py verify
python -B -m unittest discover -s tests -v
git diff --check
git status --short --branch
```

Expected: all PASS and clean synchronized `main`.

- [ ] **Step 3: Verify live state**

Confirm repository/live hashes match for AGENTS and Router, every managed Skill
matches the pinned manifest, routing index input digests match the pinned
registries, Hook remains disabled unless separately authorized, and the live
inventory contains no candidate or rejected Skill.

- [ ] **Step 4: Verify remote state**

Fetch both repositories and confirm local `HEAD` equals the configured remote
branch. Confirm the configuration pin equals curated `main` HEAD.

- [ ] **Step 5: Publish the closure report**

Report final retained Skill count, lifecycle coverage states, structured
simulation count, live fresh-session count and variance results, commits,
branches, remote parity, live hashes, rollback evidence, known runtime-owned
limitations, and any human-authority nodes. Do not claim universal future
auto-routing; claim only the tested versions and environment.
