from copy import deepcopy
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import verify as verify_script  # noqa: E402
from contracts import ContractError  # noqa: E402


SELECTION_DOCUMENT = "sources/addyosmani-agent-skills/selection.json"


class SourceSelectionIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.selection = verify_script.load(SELECTION_DOCUMENT)

    def assert_verify_rejects(self, selection: dict[str, object]) -> None:
        original_load = verify_script.load

        def load_with_mutation(path: str) -> dict[str, object]:
            if path == SELECTION_DOCUMENT:
                return deepcopy(selection)
            return original_load(path)

        with patch.object(verify_script, "load", side_effect=load_with_mutation):
            with self.assertRaises(ValueError):
                verify_script.verify()

    def test_rejects_selection_with_wrong_source(self) -> None:
        selection = {**self.selection, "source": "github:example/other"}

        self.assert_verify_rejects(selection)

    def test_rejects_selection_missing_nonadopt_candidate(self) -> None:
        selection = deepcopy(self.selection)
        decisions = selection["decisions"]
        name = next(
            name for name, disposition in decisions.items() if disposition != "adopt"
        )
        del decisions[name]

        self.assert_verify_rejects(selection)

    def test_rejects_selection_with_zero_adopts(self) -> None:
        selection = deepcopy(self.selection)
        selection["decisions"] = {
            name: "merge" if disposition == "adopt" else disposition
            for name, disposition in selection["decisions"].items()
        }

        self.assert_verify_rejects(selection)


class StructuralValidationIntegrationTests(unittest.TestCase):
    def test_admission_and_routing_contracts_are_required_verifier_inputs(self) -> None:
        for path in (
            "registry/admissions.json",
            "registry/routing.json",
            "schemas/v1/admissions.schema.json",
            "schemas/v1/routing.schema.json",
            "scripts/build_release_manifest.py",
            "generated/routing-index.json",
            "registry/scenarios.json",
            "schemas/v1/scenarios.schema.json",
            "scripts/simulate_routing.py",
            "generated/routing-simulation-report.json",
        ):
            self.assertIn(path, verify_script.REQUIRED_FILES)

    def test_schema2_capability_contract_is_a_required_verifier_input(self) -> None:
        self.assertIn(
            "schemas/v2/capabilities.schema.json", verify_script.REQUIRED_FILES
        )

    def test_program_acceptance_map_is_a_required_verifier_input(self) -> None:
        self.assertIn(
            "registry/program-acceptance-map.json",
            verify_script.REQUIRED_FILES,
        )

    def test_round03_demand_coordinate_contract_is_a_required_verifier_input(self) -> None:
        for path in (
            "registry/round03-demand-coordinate-source-contract.json",
            "registry/round03-demand-records-batch-01.json",
            "registry/round03-native-runtime-baseline-2026-07-15.json",
            "registry/round03-public-discovery-snapshot-2026-07-15.json",
            "registry/round03-representative-source-review-batch-01.json",
            "registry/round03-capability-survey-rebaseline-acceptance-event-2026-07-15.json",
        ):
            self.assertIn(path, verify_script.REQUIRED_FILES)

    def test_current_verifier_accepts_the_checked_in_schema2_capability_registry(self) -> None:
        document = verify_script.load("registry/capabilities.json")
        self.assertEqual(document["schema"], 2)
        verify_script.validate_capabilities_document(document, "registry/capabilities.json")

    def test_verifier_rejects_orphan_recipe_coverage(self) -> None:
        document = verify_script.load("registry/recipes.json")
        document["recipes"] = [
            recipe
            for recipe in document["recipes"]
            if recipe["id"] != "recipe.test-strategy"
        ]
        self.assert_verify_contract_error(
            "registry/recipes.json", document, "/scenarios/9/expectedSkills/0"
        )

    def assert_verify_contract_error(
        self, path: str, mutation: dict[str, object], pointer: str
    ) -> None:
        original_load = verify_script.load

        def load_with_mutation(candidate: str) -> dict[str, object]:
            if candidate == path:
                return deepcopy(mutation)
            return original_load(candidate)

        with patch.object(verify_script, "load", side_effect=load_with_mutation):
            with self.assertRaises(ContractError) as raised:
                verify_script.verify()
        self.assertEqual(raised.exception.pointer, pointer)

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

    def test_rejects_program_objective_with_unknown_acceptance_reference(self) -> None:
        path = "registry/program-acceptance-map.json"
        document = verify_script.load(path)
        document["objectives"][0]["acceptanceIds"] = ["acceptance.missing"]
        self.assert_verify_runtime_error(path, document, "unknown acceptance id")

    def test_rejects_verified_program_acceptance_without_evidence(self) -> None:
        path = "registry/program-acceptance-map.json"
        document = verify_script.load(path)
        criterion = document["acceptanceCriteria"][0]
        criterion["assessment"] = "verified"
        criterion["evidenceIds"] = []
        self.assert_verify_runtime_error(
            path,
            document,
            "verified acceptance requires evidence",
        )

    def test_round02_is_closed_only_after_owner_acceptance(self) -> None:
        rounds = verify_script.load("registry/curation-expansion-rounds.json")
        round02 = next(
            item
            for item in rounds["rounds"]
            if item["id"] == "round-02-source-intake-and-filtering"
        )
        self.assertEqual(round02["status"], "closed")
        self.assertEqual(round02["lifecycle"]["execute"], "closed")
        self.assertEqual(round02["lifecycle"]["acceptance"], "passed")
        self.assertEqual(round02["lifecycle"]["stageCloseout"], "closed")
        self.assertEqual(round02["closeoutOutcome"], "complete")
        self.assertIn(
            "registry/round02-stage-closeout-acceptance-event-2026-07-15.json",
            round02["evidence"],
        )

    def test_round02_closeout_review_prepares_but_does_not_apply_owner_decision(self) -> None:
        review = verify_script.load("registry/round02-stage-closeout-review.json")
        self.assertEqual(review["status"], "owner_decision_required")
        self.assertEqual(review["recommendedOutcome"], "complete")
        self.assertEqual(
            review["recommendedNextDecision"],
            "close-round-02-and-pause-for-round-03-rebaseline",
        )
        self.assertTrue(review["authorityBoundary"]["ownerDecisionRequired"])
        self.assertFalse(review["authorityBoundary"]["roundStateMutationApplied"])
        self.assertFalse(review["authorityBoundary"]["round03ActivationAuthorized"])
        self.assertFalse(review["authorityBoundary"]["remotePushAuthorized"])

    def test_round02_closeout_review_rejects_premature_state_mutation(self) -> None:
        path = "registry/round02-stage-closeout-review.json"
        review = verify_script.load(path)
        review["authorityBoundary"]["roundStateMutationApplied"] = True
        self.assert_verify_runtime_error(path, review, "authority boundary drifted")

    def test_round02_closeout_acceptance_does_not_activate_round03_or_push(self) -> None:
        event = verify_script.load(
            "registry/round02-stage-closeout-acceptance-event-2026-07-15.json"
        )
        self.assertEqual(event["authoritySource"], "owner-selected-option-1")
        self.assertTrue(event["roundStateMutationAuthorized"])
        self.assertFalse(event["round03ActivationAuthorized"])
        self.assertFalse(event["remotePushAuthorized"])
        self.assertFalse(event["globalProgramCompletionClaimed"])

    def test_round03_rebaseline_acceptance_activates_only_bounded_research(self) -> None:
        rounds = verify_script.load("registry/curation-expansion-rounds.json")
        round03 = next(
            item
            for item in rounds["rounds"]
            if item["id"] == "round-03-adaptation-and-curated-admission"
        )
        rebaseline = verify_script.load(
            "registry/round03-capability-survey-rebaseline.json"
        )
        self.assertEqual(round03["status"], "active")
        self.assertEqual(round03["lifecycle"]["execute"], "active")
        self.assertEqual(rebaseline["status"], "accepted")
        self.assertTrue(rebaseline["activationGate"]["executionActivated"])
        self.assertFalse(
            rebaseline["activationGate"]["externalDiscoveryAuthorizedByThisRecord"]
        )
        carrier = rebaseline["gapFillCarrierDecision"]
        self.assertIn("residual gap is supported", carrier["entryCondition"].lower())
        self.assertIn(
            "repository-authored Skill with a consumer-owned Hook",
            carrier["options"],
        )
        self.assertTrue(carrier["default"].lower().startswith("no hook"))

        event = verify_script.load(
            "registry/round03-capability-survey-rebaseline-acceptance-event-2026-07-15.json"
        )
        authorization = event["authorization"]
        self.assertTrue(authorization["publicReadOnlyMetadataDiscoveryAuthorized"])
        self.assertTrue(authorization["currentRepositoryEvidenceWritesAuthorized"])
        self.assertFalse(authorization["candidateExecutionAuthorized"])
        self.assertFalse(authorization["runtimeMutationAuthorized"])
        self.assertFalse(authorization["crossRepositoryWriteAuthorized"])
        self.assertFalse(authorization["remotePushAuthorized"])

    def test_round03_rebaseline_rejects_implicit_discovery_activation(self) -> None:
        path = "registry/round03-capability-survey-rebaseline.json"
        rebaseline = verify_script.load(path)
        rebaseline["activationGate"]["externalDiscoveryAuthorizedByThisRecord"] = True
        self.assert_verify_runtime_error(path, rebaseline, "activation gate drifted")

    def test_round03_demand_contract_pins_sources_without_promoting_them(self) -> None:
        contract = verify_script.load(
            "registry/round03-demand-coordinate-source-contract.json"
        )
        self.assertEqual(contract["status"], "verified-input-contract")
        self.assertEqual(
            {item["family"]: item["count"] for item in contract["coordinateFamilies"]},
            {"STM": 26, "P": 24, "SG": 12},
        )
        self.assertTrue(contract["readiness"]["sourceIdentityVerified"])
        self.assertTrue(contract["readiness"]["firstGovernedDemandBatchVerified"])
        self.assertTrue(contract["readiness"]["datedNativeRuntimeBaselineVerified"])
        self.assertFalse(contract["readiness"]["demandRecordExtractionComplete"])
        self.assertTrue(contract["readiness"]["externalDiscoveryAuthorized"])
        self.assertTrue(
            all(not item["bodyRedistributionAuthorized"] for item in contract["sources"])
        )

    def test_round03_demand_contract_rejects_source_identity_drift(self) -> None:
        path = "registry/round03-demand-coordinate-source-contract.json"
        contract = verify_script.load(path)
        contract["sources"][0]["sha256"] = "0" * 64
        self.assert_verify_runtime_error(path, contract, "source identity drifted")

    def test_round03_demand_contract_rejects_discovery_authority_drift(self) -> None:
        path = "registry/round03-demand-coordinate-source-contract.json"
        contract = verify_script.load(path)
        contract["readiness"]["externalDiscoveryAuthorized"] = False
        self.assert_verify_runtime_error(path, contract, "readiness drifted")

    def test_round03_first_demand_batch_preserves_partial_non_discovery_state(self) -> None:
        batch = verify_script.load("registry/round03-demand-records-batch-01.json")
        self.assertEqual(batch["status"], "verified-read-only-demand-batch")
        self.assertEqual(
            [record["sourceLaneId"] for record in batch["records"]],
            ["EL-01", "EL-02", "EL-03", "EL-04"],
        )
        self.assertFalse(batch["scope"]["demandExtractionComplete"])
        self.assertTrue(batch["batchDecision"]["publicCandidateDiscoveryMayStart"])
        self.assertEqual(
            [record["sourceLaneId"] for record in batch["records"] if record["candidateDiscoveryEligible"]],
            ["EL-01", "EL-02", "EL-04"],
        )

    def test_round03_first_demand_batch_rejects_premature_gap_or_discovery_claim(self) -> None:
        path = "registry/round03-demand-records-batch-01.json"
        batch = verify_script.load(path)
        batch["records"][0]["residualGapState"] = "supported"
        batch["records"][0]["candidateDiscoveryEligible"] = True
        self.assert_verify_runtime_error(path, batch, "demand record gate drifted")

    def test_round03_first_demand_batch_rejects_coordinate_mapping_drift(self) -> None:
        path = "registry/round03-demand-records-batch-01.json"
        batch = verify_script.load(path)
        batch["records"][1]["coordinateIds"]["SG"] = ["SG-01"]
        self.assert_verify_runtime_error(path, batch, "SG mapping drifted")

    def test_round03_first_demand_batch_rejects_evidence_vocabulary_drift(self) -> None:
        path = "registry/round03-demand-records-batch-01.json"
        batch = verify_script.load(path)
        batch["records"][1]["evidenceState"]["applicability"] = ["project hypothesis"]
        self.assert_verify_runtime_error(path, batch, "evidence vocabulary drifted")

    def test_round03_native_runtime_baseline_is_host_bounded_and_non_executing(self) -> None:
        baseline = verify_script.load("registry/round03-native-runtime-baseline-2026-07-15.json")
        self.assertFalse(baseline["scope"]["crossHostClaim"])
        self.assertEqual(baseline["observations"]["skillNameSurface"]["skillFileCount"], 422)
        self.assertFalse(baseline["observations"]["hookMetadata"]["filePresenceProvesActivation"])
        self.assertFalse(baseline["baselineDecision"]["candidateExecutionAuthorized"])
        self.assertFalse(baseline["baselineDecision"]["residualGapProven"])

    def test_round03_native_runtime_baseline_rejects_hook_activation_overclaim(self) -> None:
        path = "registry/round03-native-runtime-baseline-2026-07-15.json"
        baseline = verify_script.load(path)
        baseline["observations"]["hookMetadata"]["filePresenceProvesActivation"] = True
        self.assert_verify_runtime_error(path, baseline, "Hook metadata boundary drifted")

    def test_round03_native_runtime_baseline_rejects_human_authority_skill_routing(self) -> None:
        path = "registry/round03-native-runtime-baseline-2026-07-15.json"
        baseline = verify_script.load(path)
        baseline["demandBaselines"][2]["publicMetadataDiscoveryEligible"] = True
        baseline["demandBaselines"][2]["externalMetadataQuestion"] = "Find a Skill to replace domain authority."
        self.assert_verify_runtime_error(path, baseline, "demand baseline incomplete")

    def test_round03_public_discovery_is_public_pinned_and_non_approving(self) -> None:
        snapshot = verify_script.load("registry/round03-public-discovery-snapshot-2026-07-15.json")
        self.assertEqual(snapshot["dataBoundary"]["githubVisibility"], "public-only")
        self.assertTrue(
            all(
                "is:public" in query["query"]
                for query_round in snapshot["queryRounds"]
                for query in query_round["queries"]
            )
        )
        self.assertEqual(len(snapshot["representativeSources"]), 9)
        self.assertTrue(all(len(source["commit"]) == 40 for source in snapshot["representativeSources"]))
        self.assertFalse(snapshot["snapshotDecision"]["thirdPartyCandidateApproved"])
        self.assertFalse(snapshot["snapshotDecision"]["residualGapProven"])

    def test_round03_public_discovery_rejects_private_query_drift(self) -> None:
        path = "registry/round03-public-discovery-snapshot-2026-07-15.json"
        snapshot = verify_script.load(path)
        snapshot["queryRounds"][0]["queries"][0]["query"] = "agent skills"
        self.assert_verify_runtime_error(path, snapshot, "query evidence drifted")

    def test_round03_public_discovery_rejects_premature_candidate_approval(self) -> None:
        path = "registry/round03-public-discovery-snapshot-2026-07-15.json"
        snapshot = verify_script.load(path)
        snapshot["snapshotDecision"]["thirdPartyCandidateApproved"] = True
        self.assert_verify_runtime_error(path, snapshot, "non-approval decision drifted")

    def test_round03_public_discovery_rejects_unpinned_representative(self) -> None:
        path = "registry/round03-public-discovery-snapshot-2026-07-15.json"
        snapshot = verify_script.load(path)
        snapshot["representativeSources"][2]["commit"] = "main"
        self.assert_verify_runtime_error(path, snapshot, "representative source drifted")

    def test_round03_representative_review_separates_skills_tools_official_and_index(self) -> None:
        review = verify_script.load("registry/round03-representative-source-review-batch-01.json")
        decision = review["batchDecision"]
        self.assertEqual(decision["reviewedSourceCount"], 9)
        self.assertEqual(decision["skillContentComparisonCount"], 2)
        self.assertEqual(decision["nonSkillToolingAlternativeCount"], 4)
        self.assertEqual(decision["approvedCandidateCount"], 0)
        handoff = next(item for item in review["reviews"] if item["sourceId"] == "github:cskwork/handoff-skill")
        self.assertFalse(handoff["contentIdentity"]["exactDuplicate"])

    def test_round03_representative_review_rejects_license_blob_drift(self) -> None:
        path = "registry/round03-representative-source-review-batch-01.json"
        review = verify_script.load(path)
        review["reviews"][2]["licenseReview"]["evidence"][0]["gitBlob"] = "0" * 40
        self.assert_verify_runtime_error(path, review, "license review drifted")

    def test_round03_representative_review_rejects_premature_approval(self) -> None:
        path = "registry/round03-representative-source-review-batch-01.json"
        review = verify_script.load(path)
        review["batchDecision"]["approvedCandidateCount"] = 1
        self.assert_verify_runtime_error(path, review, "review decision drifted")

    def test_round03_representative_review_rejects_official_body_admission(self) -> None:
        path = "registry/round03-representative-source-review-batch-01.json"
        review = verify_script.load(path)
        review["reviews"][0]["disposition"] = "candidate"
        self.assert_verify_runtime_error(path, review, "official body exclusion drifted")

    def test_program_step_status_validation_is_not_snapshot_hardcoded(self) -> None:
        program = verify_script.load("registry/curation-program-plan.json")
        rounds = verify_script.load("registry/curation-expansion-rounds.json")
        program["steps"][0]["status"] = "evidence-recorded"
        verify_script.validate_curation_program_plan(program, rounds)

    def test_program_rejects_current_state_mismatch(self) -> None:
        program = verify_script.load("registry/curation-program-plan.json")
        rounds = verify_script.load("registry/curation-expansion-rounds.json")
        program["currentState"] = "complete"
        with self.assertRaisesRegex(
            RuntimeError,
            "currentState must match the current step status",
        ):
            verify_script.validate_curation_program_plan(program, rounds)

    def test_program_routes_standard_candidate_custody_to_calibration(self) -> None:
        program = verify_script.load("registry/curation-program-plan.json")
        delivery = program["strategicPositioning"]["standardCandidateDelivery"]
        self.assertEqual(delivery["researchAndCandidateCustody"], "YIYUAN-CALIBRATION")
        self.assertFalse(delivery["consumerConfigurationMayBeDurableAuthority"])
        self.assertEqual(delivery["projectAdmissionAuthority"], "YIYUAN-ASSETS")
        objective = next(
            item
            for item in program["strategicObjectives"]
            if item["id"] == "objective.standard-candidate-extraction"
        )
        self.assertIn("acceptance.calibration-custody-boundary", objective["acceptanceIds"])

    def test_program_rejects_user_configuration_as_standard_custody(self) -> None:
        program = verify_script.load("registry/curation-program-plan.json")
        rounds = verify_script.load("registry/curation-expansion-rounds.json")
        program["strategicPositioning"]["standardCandidateDelivery"][
            "researchAndCandidateCustody"
        ] = "codex-user-config"
        with self.assertRaisesRegex(RuntimeError, "preserve CALIBRATION custody"):
            verify_script.validate_curation_program_plan(program, rounds)

    def test_program_control_includes_missing_objectives_and_stable_lanes(self) -> None:
        program = verify_script.load("registry/curation-program-plan.json")
        objective_ids = {item["id"] for item in program["strategicObjectives"]}
        required_objectives = {
            "objective.multi-domain-coverage",
            "objective.evidence-backed-demand-model",
            "objective.reuse-before-build-gap-proof",
            "objective.full-chain-capability-coverage",
            "objective.decision-ready-external-brain",
        }
        self.assertTrue(required_objectives <= objective_ids)
        lane_ids = {
            item["id"] for item in program["programArchitecture"]["operatingLanes"]
        }
        self.assertTrue(
            {
                "lane.demand-evidence",
                "lane.native-official-runtime-baseline",
                "lane.solution-alternative-comparison",
                "lane.residual-gap-decision",
                "lane.standard-extraction-and-calibration-handoff",
            }
            <= lane_ids
        )

    def test_program_objective_set_is_extensible(self) -> None:
        program = verify_script.load("registry/curation-program-plan.json")
        rounds = verify_script.load("registry/curation-expansion-rounds.json")
        acceptance = verify_script.load("registry/program-acceptance-map.json")
        future_objective = {
            "id": "objective.future-reviewed-extension",
            "statement": "Preserve reviewed extension points without weakening current authority.",
            "authorityOwner": "agent-skills-curated",
            "nonGoals": ["bypassing governed program review"],
            "acceptanceIds": ["acceptance.future-terminal-boundary"],
        }
        program["strategicObjectives"].append(future_objective)
        acceptance["objectives"].append(
            {
                "id": future_objective["id"],
                "acceptanceIds": future_objective["acceptanceIds"],
            }
        )
        verify_script.validate_curation_program_plan(program, rounds)
        verify_script.validate_program_acceptance_map(acceptance, program)

    def test_program_rejects_runtime_sync_as_mandatory_stable_lane(self) -> None:
        program = verify_script.load("registry/curation-program-plan.json")
        rounds = verify_script.load("registry/curation-expansion-rounds.json")
        program["programArchitecture"]["operatingLanes"].append(
            {
                "id": "lane.mandatory-local-runtime-sync",
                "purpose": "Require every release to mutate a local consumer runtime.",
                "requiredInputs": ["curated release"],
                "allowedOutputs": ["local runtime mutation"],
                "blockedTransitions": ["none"],
                "verificationSurface": ["local path changed"],
                "rerouteTriggers": ["local runtime unavailable"],
            }
        )
        with self.assertRaisesRegex(RuntimeError, "consumer runtime sync"):
            verify_script.validate_curation_program_plan(program, rounds)

    def test_program_rejects_gap_fill_without_residual_gap_gate(self) -> None:
        program = verify_script.load("registry/curation-program-plan.json")
        rounds = verify_script.load("registry/curation-expansion-rounds.json")
        origin = next(
            item
            for item in program["candidateOriginPolicy"]["classes"]
            if item["id"] == "repository-authored-gap-fill-candidate"
        )
        origin["eligibilityGate"] = "discovery-only"
        with self.assertRaisesRegex(RuntimeError, "residual gap"):
            verify_script.validate_curation_program_plan(program, rounds)

    def test_capability_survey_acceptance_contract_is_complete(self) -> None:
        acceptance = verify_script.load("registry/program-acceptance-map.json")
        criterion_ids = {item["id"] for item in acceptance["acceptanceCriteria"]}
        self.assertTrue(
            {
                "acceptance.native-runtime-baseline",
                "acceptance.discovery-clustering-stop-rule",
                "acceptance.alternative-comparison",
                "acceptance.residual-gap-proof",
                "acceptance.capability-survey-result-package",
                "acceptance.cross-agent-claim-limits",
            }
            <= criterion_ids
        )

    def test_program_records_owner_acceptance_and_activates_capability_survey(self) -> None:
        program = verify_script.load("registry/curation-program-plan.json")
        self.assertEqual(
            program["currentInitiativeId"],
            "initiative.capability-survey-gap-proof",
        )
        completeness = next(
            item
            for item in program["currentInitiatives"]
            if item["id"] == "initiative.program-control-completeness-reconciliation"
        )
        current = next(
            item
            for item in program["currentInitiatives"]
            if item["id"] == program["currentInitiativeId"]
        )
        self.assertEqual(completeness["status"], "accepted")
        self.assertEqual(current["status"], "active")
        rebaseline = next(
            item
            for item in program["currentInitiatives"]
            if item["id"] == "initiative.round03-capability-survey-rebaseline"
        )
        self.assertEqual(rebaseline["status"], "accepted")
        event = verify_script.load("registry/program-control-acceptance-event-2026-07-15.json")
        self.assertEqual(
            event["acceptedBaselineCommit"],
            "7513da41e9c2950de1a6132ce9c9d65fb11a8098",
        )
        self.assertEqual(event["decision"], "accepted-and-merged-locally")
        self.assertFalse(event["remotePushAuthorized"])

    def test_program_control_acceptance_event_does_not_authorize_remote_push(self) -> None:
        path = "registry/program-control-acceptance-event-2026-07-15.json"
        event = verify_script.load(path)
        event["remotePushAuthorized"] = True
        self.assert_verify_runtime_error(path, event, "must not authorize remote push")

    def test_program_declares_dependency_graph_order_semantics(self) -> None:
        program = verify_script.load("registry/curation-program-plan.json")
        semantics = program["programArchitecture"]["executionSemantics"]
        self.assertEqual(
            semantics["model"],
            "dependency-graph-with-optional-and-cross-cutting-lanes",
        )
        self.assertEqual(
            semantics["corePath"],
            [
                "lane.demand-evidence",
                "lane.native-official-runtime-baseline",
                "lane.discovery-and-clustering",
                "lane.representative-deep-review",
                "lane.solution-alternative-comparison",
                "lane.residual-gap-decision",
                "lane.candidate-governance-and-adaptation",
                "lane.admission-verification-and-release",
            ],
        )
        self.assertEqual(
            semantics["optionalBranches"],
            ["lane.consumer-evidence-and-feedback"],
        )
        self.assertEqual(
            semantics["crossCuttingLanes"],
            ["lane.lifecycle-metabolism"],
        )
        self.assertEqual(
            semantics["conditionalBranches"],
            ["lane.standard-extraction-and-calibration-handoff"],
        )

    def test_program_rejects_lifecycle_that_requires_consumer_evidence(self) -> None:
        program = verify_script.load("registry/curation-program-plan.json")
        rounds = verify_script.load("registry/curation-expansion-rounds.json")
        lifecycle = next(
            item
            for item in program["programArchitecture"]["operatingLanes"]
            if item["id"] == "lane.lifecycle-metabolism"
        )
        lifecycle["requiredInputs"] = ["release and consumer evidence"]
        with self.assertRaisesRegex(RuntimeError, "lifecycle.*consumer"):
            verify_script.validate_curation_program_plan(program, rounds)

    def test_program_requires_source_pin_before_representative_deep_review(self) -> None:
        program = verify_script.load("registry/curation-program-plan.json")
        rounds = verify_script.load("registry/curation-expansion-rounds.json")
        review = next(
            item
            for item in program["programArchitecture"]["operatingLanes"]
            if item["id"] == "lane.representative-deep-review"
        )
        review["requiredInputs"] = [
            "clustered shortlist",
            "dated metadata",
            "review questions",
        ]
        with self.assertRaisesRegex(RuntimeError, "source pin"):
            verify_script.validate_curation_program_plan(program, rounds)

    def test_rejects_skill_unknown_field_before_semantic_access(self) -> None:
        document = verify_script.load("registry/skills.json")
        document["skills"][0]["statuz"] = "approved"
        self.assert_verify_contract_error(
            "registry/skills.json", document, "/skills/0/statuz"
        )

    def test_rejects_malformed_registry_as_contract_error(self) -> None:
        document = verify_script.load("registry/skills.json")
        document["skills"] = {"not": "an array"}
        self.assert_verify_contract_error("registry/skills.json", document, "/skills")

    def test_main_reports_contract_error_without_traceback(self) -> None:
        error = ContractError("registry/skills.json", "/skills", "must be an array")
        stderr = StringIO()
        with patch.object(verify_script, "verify", side_effect=error):
            with redirect_stderr(stderr):
                result = verify_script.main()

        self.assertEqual(result, 1)
        self.assertEqual(
            stderr.getvalue(),
            "Contract error: registry/skills.json:/skills: must be an array\n",
        )
        self.assertNotIn("Traceback", stderr.getvalue())


class ReferenceValidationIntegrationTests(unittest.TestCase):
    def test_verify_rejects_missing_curated_capability_owner(self) -> None:
        path = "registry/capabilities.json"
        document = verify_script.load(path)
        document["capabilities"][0]["canonicalOwner"] = "skill.curated.missing"
        original_load = verify_script.load

        def load_with_mutation(candidate: str) -> dict[str, object]:
            if candidate == path:
                return deepcopy(document)
            return original_load(candidate)

        with patch.object(verify_script, "load", side_effect=load_with_mutation):
            with self.assertRaises(ContractError) as raised:
                verify_script.verify()

        self.assertEqual(raised.exception.document, path)
        self.assertEqual(raised.exception.pointer, "/capabilities/0/canonicalOwner")

if __name__ == "__main__":
    unittest.main()
