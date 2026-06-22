from copy import deepcopy
import json
from pathlib import Path
import unittest

from scripts.contracts import (
    ContractError,
    validate_admissions_document,
    validate_capabilities_document,
    validate_conflicts_document,
    validate_recipes_document,
    validate_relations_document,
    validate_release_manifest_document,
    validate_routing_document,
    validate_scenarios_document,
    validate_selection_document,
    validate_skills_document,
    validate_sources_lock_document,
)


ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = (
    "skills",
    "capabilities",
    "relations",
    "conflicts",
    "recipes",
    "sources-lock",
    "selection",
    "release-manifest",
)


ADMISSIONS = {
    "schema": 1,
    "admissions": [{
        "skill": "skill.curated.alpha",
        "source": "upstream:reviewed",
        "thirdParty": True,
        "nativeBaselineCompared": True,
        "nativeIncrement": "A repeatable evidence-producing workflow.",
        "overlapReviewed": True,
        "disposition": "approve",
        "reviewRefs": ["audits/alpha.md"],
        "validated": True,
    }],
}

ROUTING = {
    "schema": 1,
    "routes": [{
        "skill": "skill.curated.alpha",
        "aliases": ["alpha workflow"],
        "positiveTriggers": ["Use the alpha workflow."],
        "negativeTriggers": ["Do not use it for ordinary summarization."],
        "contextRequirements": ["A reviewable repository is available."],
        "inputs": ["User goal"],
        "outputs": ["Verified artifact"],
        "sideEffects": ["Writes only within the requested repository scope."],
        "validation": ["Run the focused contract tests."],
        "riskLevel": "low",
        "permissionsRequired": ["Repository write access"],
        "fallback": ["Use native reasoning and declare the limitation."],
        "humanConfirmWhen": ["The route would expand the requested scope."],
        "languages": ["en"],
        "agentCompatibility": ["cross-agent"],
        "lifecycleCapabilities": ["capability.alpha"],
    }],
}

SCENARIOS_DOCUMENT = {
    "schema": 1,
    "scenarios": [{
        "id": "scenario.alpha-positive",
        "language": "en",
        "request": "Apply the alpha workflow.",
        "decisionClass": "curated",
        "expectedSkills": ["skill.curated.alpha"],
        "excludedSkills": ["skill.curated.beta"],
        "requestedCapabilities": ["capability.alpha"],
        "expectedCapabilities": ["capability.alpha"],
        "humanConfirmation": False,
        "validationExpectations": ["The output is independently verifiable."],
    }],
}

CAPABILITIES_V2 = {
    "schema": 2,
    "capabilities": [{
        "id": "capability.alpha",
        "stage": "verify",
        "description": "Produce independently verifiable alpha evidence.",
        "coverageState": "curated",
        "validation": ["Run the alpha verification contract."],
        "fallback": ["Declare a gap and request human direction."],
        "curatedOwners": ["skill.curated.alpha"],
    }],
}


def load(path: str) -> dict[str, object]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class ShapeTests(unittest.TestCase):
    def assert_contract_error(
        self, validator: object, document: dict[str, object], pointer: str
    ) -> None:
        with self.assertRaises(ContractError) as raised:
            validator(document, "fixture.json")  # type: ignore[operator]
        self.assertEqual(raised.exception.document, "fixture.json")
        self.assertEqual(raised.exception.pointer, pointer)

    def test_checked_in_schemas_are_draft_2020_12_contracts(self) -> None:
        for name in SCHEMAS:
            with self.subTest(name=name):
                schema = load(f"schemas/v1/{name}.schema.json")
                self.assertEqual(
                    schema["$schema"], "https://json-schema.org/draft/2020-12/schema"
                )
                self.assertEqual(schema["type"], "object")
                self.assertFalse(schema["additionalProperties"])

        for version, name in ((1, "admissions"), (1, "routing"), (1, "scenarios"), (2, "capabilities")):
            with self.subTest(version=version, name=name):
                schema = load(f"schemas/v{version}/{name}.schema.json")
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertEqual(schema["type"], "object")
                self.assertFalse(schema["additionalProperties"])

    def test_new_governance_documents_accept_approved_fixtures(self) -> None:
        validate_admissions_document(ADMISSIONS, "fixture.json")
        validate_routing_document(ROUTING, "fixture.json")
        validate_scenarios_document(SCENARIOS_DOCUMENT, "fixture.json")
        validate_capabilities_document(CAPABILITIES_V2, "fixture.json")

    def test_admissions_require_all_evidence_and_approved_truths(self) -> None:
        for field in ADMISSIONS["admissions"][0]:
            with self.subTest(field=field):
                document = deepcopy(ADMISSIONS)
                del document["admissions"][0][field]
                self.assert_contract_error(validate_admissions_document, document, f"/admissions/0/{field}")
        for field in (
            "thirdParty",
            "nativeBaselineCompared",
            "overlapReviewed",
            "validated",
        ):
            with self.subTest(field=field):
                document = deepcopy(ADMISSIONS)
                document["admissions"][0][field] = False
                self.assert_contract_error(validate_admissions_document, document, f"/admissions/0/{field}")

    def test_admissions_schema_declares_all_approval_truths(self) -> None:
        schema = load("schemas/v1/admissions.schema.json")
        approved = schema["properties"]["admissions"]["items"]["then"]["properties"]
        self.assertEqual(
            approved,
            {
                field: {"const": True}
                for field in (
                    "thirdParty",
                    "nativeBaselineCompared",
                    "overlapReviewed",
                    "validated",
                )
            },
        )

    def test_new_governance_enums_are_closed(self) -> None:
        document = deepcopy(ADMISSIONS)
        document["admissions"][0]["disposition"] = "adopt"
        self.assert_contract_error(validate_admissions_document, document, "/admissions/0/disposition")
        document = deepcopy(ROUTING)
        document["routes"][0]["riskLevel"] = "urgent"
        self.assert_contract_error(validate_routing_document, document, "/routes/0/riskLevel")
        document = deepcopy(CAPABILITIES_V2)
        document["capabilities"][0]["coverageState"] = "official"
        self.assert_contract_error(validate_capabilities_document, document, "/capabilities/0/coverageState")

    def test_routing_semantic_contract_arrays_are_nonempty(self) -> None:
        fields = (
            "aliases", "positiveTriggers", "negativeTriggers", "contextRequirements",
            "inputs", "outputs", "validation", "fallback", "humanConfirmWhen",
            "languages", "agentCompatibility", "lifecycleCapabilities",
        )
        for field in fields:
            with self.subTest(field=field):
                document = deepcopy(ROUTING)
                document["routes"][0][field] = []
                self.assert_contract_error(validate_routing_document, document, f"/routes/0/{field}")

    def test_capabilities_v2_are_abstract_and_product_neutral(self) -> None:
        for field in ("canonicalOwner", "product", "official", "runtime", "runtimeIdentity"):
            with self.subTest(field=field):
                document = deepcopy(CAPABILITIES_V2)
                document["capabilities"][0][field] = "external:runtime"
                self.assert_contract_error(validate_capabilities_document, document, f"/capabilities/0/{field}")

        document = deepcopy(CAPABILITIES_V2)
        del document["capabilities"][0]["curatedOwners"]
        self.assert_contract_error(validate_capabilities_document, document, "/capabilities/0/curatedOwners")
        document["capabilities"][0]["coverageState"] = "native-sufficient"
        validate_capabilities_document(document, "fixture.json")

    def test_every_document_rejects_missing_or_wrong_schema(self) -> None:
        cases = (
            (validate_skills_document, "registry/skills.json"),
            (validate_capabilities_document, "registry/capabilities.json"),
            (validate_relations_document, "registry/relations.json"),
            (validate_conflicts_document, "registry/conflicts.json"),
            (validate_recipes_document, "registry/recipes.json"),
            (validate_sources_lock_document, "sources/lock.json"),
            (
                validate_selection_document,
                "sources/addyosmani-agent-skills/selection.json",
            ),
            (validate_release_manifest_document, "release-manifest.json"),
        )
        for validator, path in cases:
            with self.subTest(path=path, problem="missing"):
                document = load(path)
                del document["schema"]
                self.assert_contract_error(validator, document, "/schema")
            with self.subTest(path=path, problem="wrong"):
                document = load(path)
                document["schema"] = 3 if path == "registry/capabilities.json" else 2
                self.assert_contract_error(validator, document, "/schema")

    def test_skills_reject_unknown_status_enum_and_wrong_type(self) -> None:
        document = load("registry/skills.json")
        unknown = deepcopy(document)
        unknown["skills"][0]["statuz"] = "approved"  # type: ignore[index]
        self.assert_contract_error(
            validate_skills_document, unknown, "/skills/0/statuz"
        )

        invalid = deepcopy(document)
        invalid["skills"][0]["status"] = "done"  # type: ignore[index]
        self.assert_contract_error(
            validate_skills_document, invalid, "/skills/0/status"
        )

        wrong_type = deepcopy(document)
        wrong_type["skills"] = {}
        self.assert_contract_error(validate_skills_document, wrong_type, "/skills")

    def test_skills_reject_invalid_stable_id_and_directory(self) -> None:
        document = load("registry/skills.json")
        document["skills"][0]["id"] = "bad"  # type: ignore[index]
        self.assert_contract_error(validate_skills_document, document, "/skills/0/id")

        document = load("registry/skills.json")
        document["skills"][0]["directory"] = "../escape"  # type: ignore[index]
        self.assert_contract_error(
            validate_skills_document, document, "/skills/0/directory"
        )

    def test_skills_reject_empty_required_text(self) -> None:
        for field in ("name", "description", "phase", "source"):
            with self.subTest(field=field):
                document = load("registry/skills.json")
                document["skills"][0][field] = ""  # type: ignore[index]
                self.assert_contract_error(
                    validate_skills_document, document, f"/skills/0/{field}"
                )

    def test_other_registries_reject_invalid_stable_ids(self) -> None:
        cases = (
            (validate_capabilities_document, "registry/capabilities.json", "capabilities"),
            (validate_conflicts_document, "registry/conflicts.json", "groups"),
            (validate_recipes_document, "registry/recipes.json", "recipes"),
        )
        for validator, path, collection in cases:
            with self.subTest(path=path):
                document = load(path)
                document[collection][0]["id"] = "bad"  # type: ignore[index]
                self.assert_contract_error(
                    validator, document, f"/{collection}/0/id"
                )

    def test_capability_owner_must_be_a_string(self) -> None:
        document = load("registry/capabilities.json")
        document["capabilities"][0]["canonicalOwner"] = []  # type: ignore[index]
        self.assert_contract_error(
            validate_capabilities_document,
            document,
            "/capabilities/0/canonicalOwner",
        )

    def test_relations_validate_relation_types_and_edge_fields(self) -> None:
        document = load("registry/relations.json")
        document["relationTypes"][0] = 1  # type: ignore[index]
        self.assert_contract_error(
            validate_relations_document, document, "/relationTypes/0"
        )

        document = load("registry/relations.json")
        document["relations"][0]["type"] = []  # type: ignore[index]
        self.assert_contract_error(
            validate_relations_document, document, "/relations/0/type"
        )

        document = load("registry/relations.json")
        document["relations"][0]["weight"] = 1  # type: ignore[index]
        self.assert_contract_error(
            validate_relations_document, document, "/relations/0/weight"
        )

    def test_conflicts_validate_members_and_resolution(self) -> None:
        document = load("registry/conflicts.json")
        document["groups"][0]["members"] = "owner"  # type: ignore[index]
        self.assert_contract_error(
            validate_conflicts_document, document, "/groups/0/members"
        )

        document = load("registry/conflicts.json")
        document["groups"][0]["resolution"] = False  # type: ignore[index]
        self.assert_contract_error(
            validate_conflicts_document, document, "/groups/0/resolution"
        )

    def test_recipes_validate_steps_and_authorization(self) -> None:
        document = load("registry/recipes.json")
        document["recipes"][0]["steps"] = {}  # type: ignore[index]
        self.assert_contract_error(
            validate_recipes_document, document, "/recipes/0/steps"
        )

        document = load("registry/recipes.json")
        document["recipes"][1]["authorization"] = []  # type: ignore[index]
        self.assert_contract_error(
            validate_recipes_document, document, "/recipes/1/authorization"
        )

    def test_sources_validate_candidate_ids_revision_and_boolean_type(self) -> None:
        document = load("sources/lock.json")
        document["sources"][0]["candidateIds"][0] = 7  # type: ignore[index]
        self.assert_contract_error(
            validate_sources_lock_document, document, "/sources/0/candidateIds/0"
        )

        document = load("sources/lock.json")
        document["sources"][0]["revision"] = []  # type: ignore[index]
        self.assert_contract_error(
            validate_sources_lock_document, document, "/sources/0/revision"
        )

        document = load("sources/lock.json")
        document["sources"][0]["approvedForRuntime"] = 0  # type: ignore[index]
        self.assert_contract_error(
            validate_sources_lock_document,
            document,
            "/sources/0/approvedForRuntime",
        )

    def test_source_record_can_omit_remote_only_metadata(self) -> None:
        document = {
            "schema": 1,
            "sources": [
                {
                    "id": "local:reviewed-baseline",
                    "kind": "local",
                    "provenanceStatus": "incomplete",
                    "redistribution": "private-only",
                    "reviewRefs": ["THIRD_PARTY_NOTICES.md"],
                    "candidateIds": ["local-skill"],
                    "status": "reviewed-baseline",
                    "approvedForRuntime": True,
                    "notes": ["Maintained locally."],
                }
            ],
        }
        validate_sources_lock_document(document, "fixture.json")

    def test_sources_require_governance_metadata(self) -> None:
        fields = ("kind", "provenanceStatus", "redistribution", "reviewRefs")
        for field in fields:
            with self.subTest(field=field):
                document = load("sources/lock.json")
                del document["sources"][0][field]
                self.assert_contract_error(
                    validate_sources_lock_document,
                    document,
                    f"/sources/0/{field}",
                )

    def test_sources_reject_unknown_governance_values(self) -> None:
        for field in ("kind", "provenanceStatus", "redistribution"):
            with self.subTest(field=field):
                document = load("sources/lock.json")
                document["sources"][0][field] = "unknown"
                self.assert_contract_error(
                    validate_sources_lock_document,
                    document,
                    f"/sources/0/{field}",
                )

    def test_local_sources_reject_remote_metadata(self) -> None:
        for field in ("url", "revision", "license"):
            with self.subTest(field=field):
                document = load("sources/lock.json")
                document["sources"][1][field] = "not-allowed"
                self.assert_contract_error(
                    validate_sources_lock_document,
                    document,
                    f"/sources/1/{field}",
                )

    def test_local_sources_require_restricted_provenance_policy(self) -> None:
        cases = (
            ("provenanceStatus", "complete"),
            ("redistribution", "license-governed"),
        )
        for field, value in cases:
            with self.subTest(field=field):
                document = load("sources/lock.json")
                document["sources"][1][field] = value
                self.assert_contract_error(
                    validate_sources_lock_document,
                    document,
                    f"/sources/1/{field}",
                )

    def test_selection_validates_decisions_and_disposition_enum(self) -> None:
        document = load("sources/addyosmani-agent-skills/selection.json")
        document["decisions"] = []
        self.assert_contract_error(validate_selection_document, document, "/decisions")

        document = load("sources/addyosmani-agent-skills/selection.json")
        name = next(iter(document["decisions"]))  # type: ignore[arg-type]
        document["decisions"][name] = "retire"  # type: ignore[index]
        self.assert_contract_error(
            validate_selection_document, document, f"/decisions/{name}"
        )

    def test_selection_rejects_empty_decision_name(self) -> None:
        document = load("sources/addyosmani-agent-skills/selection.json")
        document["decisions"][""] = "reject"  # type: ignore[index]
        self.assert_contract_error(validate_selection_document, document, "/decisions/")

    def test_manifest_validates_files_path_hash_size_and_integer_bool_boundary(self) -> None:
        for field, value in (
            ("path", []),
            ("sha256", "bad"),
            ("size", True),
        ):
            with self.subTest(field=field):
                document = load("release-manifest.json")
                document["files"][0][field] = value  # type: ignore[index]
                self.assert_contract_error(
                    validate_release_manifest_document,
                    document,
                    f"/files/0/{field}",
                )

    def test_manifest_rejects_noncanonical_relative_path_shapes(self) -> None:
        for value in (
            "../outside",
            "/skills/x",
            "skills\\x\\SKILL.md",
            "skills/../outside",
            "skills/./outside",
        ):
            with self.subTest(value=value):
                document = load("release-manifest.json")
                document["files"][0]["path"] = value  # type: ignore[index]
                self.assert_contract_error(
                    validate_release_manifest_document, document, "/files/0/path"
                )

    def test_manifest_accepts_integral_floats_as_json_integers(self) -> None:
        document = load("release-manifest.json")
        document["skillCount"] = 1.0
        document["fileCount"] = 1.0
        document["files"][0]["size"] = 1.0  # type: ignore[index]

        validate_release_manifest_document(document, "fixture.json")

    def test_manifest_rejects_non_json_integers_at_their_exact_pointer(self) -> None:
        fields = (
            ("skillCount", "/skillCount"),
            ("fileCount", "/fileCount"),
            ("size", "/files/0/size"),
        )
        invalid_values = (1.5, float("nan"), float("inf"), True)
        for field, pointer in fields:
            for value in invalid_values:
                with self.subTest(field=field, value=value):
                    document = load("release-manifest.json")
                    if field == "size":
                        document["files"][0][field] = value  # type: ignore[index]
                    else:
                        document[field] = value
                    self.assert_contract_error(
                        validate_release_manifest_document, document, pointer
                    )

    def test_manifest_rejects_negative_integral_floats(self) -> None:
        for field, pointer in (
            ("skillCount", "/skillCount"),
            ("fileCount", "/fileCount"),
            ("size", "/files/0/size"),
        ):
            with self.subTest(field=field):
                document = load("release-manifest.json")
                if field == "size":
                    document["files"][0][field] = -1.0  # type: ignore[index]
                else:
                    document[field] = -1.0
                self.assert_contract_error(
                    validate_release_manifest_document, document, pointer
                )

    def test_manifest_rejects_negative_skill_count(self) -> None:
        document = load("release-manifest.json")
        document["skillCount"] = -1
        self.assert_contract_error(
            validate_release_manifest_document, document, "/skillCount"
        )

    def test_manifest_rejects_negative_file_count(self) -> None:
        document = load("release-manifest.json")
        document["fileCount"] = -2
        self.assert_contract_error(
            validate_release_manifest_document, document, "/fileCount"
        )


if __name__ == "__main__":
    unittest.main()
