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

    def test_round02_waits_for_closeout_instead_of_claiming_active_execution(self) -> None:
        rounds = verify_script.load("registry/curation-expansion-rounds.json")
        round02 = next(
            item
            for item in rounds["rounds"]
            if item["id"] == "round-02-source-intake-and-filtering"
        )
        self.assertEqual(round02["status"], "needs-closeout")
        self.assertEqual(round02["lifecycle"]["execute"], "closed")
        self.assertEqual(round02["lifecycle"]["acceptance"], "passed")
        self.assertEqual(round02["lifecycle"]["stageCloseout"], "pending")

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
