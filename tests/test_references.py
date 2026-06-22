from copy import deepcopy
import unittest

from scripts.contracts import ContractError, validate_references
from tests.test_shape_contracts import ADMISSIONS, ROUTING, SCENARIOS_DOCUMENT


class ReferenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.documents = {
            "skills": {
                "schema": 1,
                "skills": [
                    {
                        "id": "skill.curated.alpha",
                        "directory": "alpha",
                        "name": "alpha",
                        "description": "Alpha skill.",
                        "status": "approved",
                        "phase": "general",
                        "source": "local:reviewed-baseline",
                    },
                    {
                        "id": "skill.curated.beta",
                        "directory": "beta",
                        "name": "beta",
                        "description": "Beta skill.",
                        "status": "approved",
                        "phase": "general",
                        "source": "upstream:reviewed",
                    },
                ],
            },
            "capabilities": {
                "schema": 1,
                "capabilities": [
                    {
                        "id": "capability.alpha",
                        "canonicalOwner": "skill.curated.alpha",
                    },
                    {
                        "id": "capability.external",
                        "canonicalOwner": "external:runtime",
                    },
                ],
            },
            "relations": {
                "schema": 1,
                "relationTypes": ["provides", "requires"],
                "relations": [
                    {
                        "from": "skill.curated.alpha",
                        "type": "provides",
                        "to": "capability.alpha",
                    },
                    {
                        "from": "capability.alpha",
                        "type": "requires",
                        "to": "external:runtime",
                        "condition": "when needed",
                    },
                ],
            },
            "conflicts": {
                "schema": 1,
                "groups": [
                    {
                        "id": "conflict.alpha",
                        "defaultOwner": "skill.curated.alpha",
                        "members": ["skill.curated.alpha", "upstream:alpha"],
                        "resolution": "Prefer alpha.",
                    }
                ],
            },
            "recipes": {
                "schema": 1,
                "recipes": [
                    {
                        "id": "recipe.alpha",
                        "trigger": "Alpha is needed.",
                        "steps": [{"capability": "capability.alpha"}],
                    }
                ],
            },
            "sources": {
                "schema": 1,
                "sources": [
                    {"id": "local:reviewed-baseline"},
                    {"id": "upstream:reviewed"},
                ],
            },
            "admissions": deepcopy(ADMISSIONS),
            "routing": deepcopy(ROUTING),
            "scenarios": deepcopy(SCENARIOS_DOCUMENT),
        }

    def assert_rejected(
        self, documents: dict[str, object], document: str, pointer: str
    ) -> None:
        with self.assertRaises(ContractError) as raised:
            validate_references(documents)
        self.assertEqual(raised.exception.document, document)
        self.assertEqual(raised.exception.pointer, pointer)

    def test_accepts_minimal_reference_closed_documents(self) -> None:
        validate_references(self.documents)

    def test_accepts_v2_capabilities_without_canonical_owner(self) -> None:
        documents = deepcopy(self.documents)
        documents["capabilities"] = {
            "schema": 2,
            "capabilities": [
                {
                    "id": "capability.alpha",
                    "stage": "verify",
                    "description": "Alpha evidence.",
                    "coverageState": "curated",
                    "validation": ["Run alpha checks."],
                    "fallback": ["Declare the gap."],
                    "curatedOwners": ["skill.curated.alpha"],
                },
                {
                    "id": "capability.external",
                    "stage": "verify",
                    "description": "Resolved by the live runtime.",
                    "coverageState": "runtime-resolved",
                    "validation": ["Probe live availability."],
                    "fallback": ["Declare the gap."],
                },
            ],
        }

        validate_references(documents)

    def test_v2_curated_owners_must_resolve_and_provide_the_capability(self) -> None:
        for owner, relation_type in (
            ("skill.curated.missing", "provides"),
            ("skill.curated.alpha", "requires"),
        ):
            with self.subTest(owner=owner, relation_type=relation_type):
                documents = deepcopy(self.documents)
                capability = {
                    "id": "capability.alpha",
                    "stage": "verify",
                    "description": "Alpha evidence.",
                    "coverageState": "curated",
                    "validation": ["Run alpha checks."],
                    "fallback": ["Declare the gap."],
                    "curatedOwners": [owner],
                }
                documents["capabilities"] = {"schema": 2, "capabilities": [capability]}
                documents["relations"]["relations"][0]["type"] = relation_type
                self.assert_rejected(
                    documents,
                    "registry/capabilities.json",
                    "/capabilities/0/curatedOwners/0",
                )

    def test_rejects_duplicate_skill_id_directory_and_name(self) -> None:
        for field in ("id", "directory", "name"):
            with self.subTest(field=field):
                documents = deepcopy(self.documents)
                documents["skills"]["skills"][1][field] = documents["skills"]["skills"][0][field]
                self.assert_rejected(
                    documents, "registry/skills.json", f"/skills/1/{field}"
                )

    def test_rejects_duplicate_capability_conflict_and_recipe_ids(self) -> None:
        cases = (
            ("capabilities", "capabilities", "registry/capabilities.json"),
            ("conflicts", "groups", "registry/conflicts.json"),
            ("recipes", "recipes", "registry/recipes.json"),
        )
        for document_key, collection, document in cases:
            with self.subTest(document=document):
                documents = deepcopy(self.documents)
                duplicate_index = len(documents[document_key][collection])
                duplicate = deepcopy(documents[document_key][collection][0])
                documents[document_key][collection].append(duplicate)
                self.assert_rejected(
                    documents, document, f"/{collection}/{duplicate_index}/id"
                )

    def test_curated_capability_owner_must_exist_and_provide_capability(self) -> None:
        documents = deepcopy(self.documents)
        documents["capabilities"]["capabilities"][0]["canonicalOwner"] = "skill.curated.missing"
        self.assert_rejected(
            documents, "registry/capabilities.json", "/capabilities/0/canonicalOwner"
        )

        documents = deepcopy(self.documents)
        documents["relations"]["relations"][0]["type"] = "requires"
        self.assert_rejected(
            documents, "registry/capabilities.json", "/capabilities/0/canonicalOwner"
        )

    def test_external_capability_owner_requires_nonempty_supported_namespace(self) -> None:
        for owner in (
            "external:",
            "upstream:",
            "other:runtime",
            "external:../escape",
            "external:   ",
            "external:a//b",
            "upstream:/x",
        ):
            with self.subTest(owner=owner):
                documents = deepcopy(self.documents)
                documents["capabilities"]["capabilities"][1]["canonicalOwner"] = owner
                self.assert_rejected(
                    documents,
                    "registry/capabilities.json",
                    "/capabilities/1/canonicalOwner",
                )

    def test_relation_endpoints_must_resolve_or_use_explicit_external_namespace(self) -> None:
        for endpoint, value in (("from", "skill.curated.missing"), ("to", "other:node"), ("to", "external:")):
            with self.subTest(endpoint=endpoint, value=value):
                documents = deepcopy(self.documents)
                documents["relations"]["relations"][1][endpoint] = value
                self.assert_rejected(
                    documents, "registry/relations.json", f"/relations/1/{endpoint}"
                )

    def test_provides_requires_skill_to_capability(self) -> None:
        documents = deepcopy(self.documents)
        documents["relations"]["relations"][0]["from"] = "capability.alpha"
        self.assert_rejected(
            documents, "registry/relations.json", "/relations/0/from"
        )

        documents = deepcopy(self.documents)
        documents["relations"]["relations"][0]["to"] = "skill.curated.beta"
        self.assert_rejected(
            documents, "registry/relations.json", "/relations/0/to"
        )

    def test_rejects_duplicate_relation_triple_and_condition(self) -> None:
        documents = deepcopy(self.documents)
        documents["relations"]["relations"].append(
            deepcopy(documents["relations"]["relations"][1])
        )
        self.assert_rejected(
            documents, "registry/relations.json", "/relations/2"
        )

    def test_conflict_owner_must_be_member_and_members_must_resolve_uniquely(self) -> None:
        documents = deepcopy(self.documents)
        documents["conflicts"]["groups"][0]["defaultOwner"] = "skill.curated.beta"
        self.assert_rejected(
            documents, "registry/conflicts.json", "/groups/0/defaultOwner"
        )

        for member in ("skill.curated.missing", "other:member", "external:"):
            with self.subTest(member=member):
                documents = deepcopy(self.documents)
                documents["conflicts"]["groups"][0]["members"][1] = member
                self.assert_rejected(
                    documents, "registry/conflicts.json", "/groups/0/members/1"
                )

        documents = deepcopy(self.documents)
        documents["conflicts"]["groups"][0]["members"].append("skill.curated.alpha")
        self.assert_rejected(
            documents, "registry/conflicts.json", "/groups/0/members/2"
        )

    def test_recipe_steps_require_known_capabilities(self) -> None:
        documents = deepcopy(self.documents)
        documents["recipes"]["recipes"][0]["steps"][0]["capability"] = "capability.missing"
        self.assert_rejected(
            documents, "registry/recipes.json", "/recipes/0/steps/0/capability"
        )

    def test_skill_sources_require_source_lock_records(self) -> None:
        documents = deepcopy(self.documents)
        documents["skills"]["skills"][1]["source"] = "local/missing~source"
        self.assert_rejected(
            documents, "registry/skills.json", "/skills/1/source"
        )

    def test_rejects_duplicate_source_ids_at_second_id(self) -> None:
        documents = deepcopy(self.documents)
        documents["sources"]["sources"][1]["id"] = "local:reviewed-baseline"
        documents["skills"]["skills"][1]["source"] = "local:reviewed-baseline"
        self.assert_rejected(
            documents, "sources/lock.json", "/sources/1/id"
        )

    def test_admission_and_routing_skill_references_must_resolve(self) -> None:
        for key, collection, document_name in (
            ("admissions", "admissions", "registry/admissions.json"),
            ("routing", "routes", "registry/routing.json"),
        ):
            with self.subTest(key=key):
                documents = deepcopy(self.documents)
                documents[key][collection][0]["skill"] = "skill.curated.missing"
                self.assert_rejected(documents, document_name, f"/{collection}/0/skill")

    def test_routing_lifecycle_capabilities_must_resolve(self) -> None:
        documents = deepcopy(self.documents)
        documents["routing"]["routes"][0]["lifecycleCapabilities"] = [
            "capability.missing"
        ]
        self.assert_rejected(
            documents,
            "registry/routing.json",
            "/routes/0/lifecycleCapabilities/0",
        )

    def test_scenario_skill_and_capability_references_must_resolve(self) -> None:
        cases = (
            ("expectedSkills", "skill.curated.missing"),
            ("excludedSkills", "skill.curated.missing"),
            ("requestedCapabilities", "capability.missing"),
            ("expectedCapabilities", "capability.missing"),
        )
        for field, value in cases:
            with self.subTest(field=field):
                documents = deepcopy(self.documents)
                documents["scenarios"]["scenarios"][0][field] = [value]
                self.assert_rejected(
                    documents,
                    "registry/scenarios.json",
                    f"/scenarios/0/{field}/0",
                )

if __name__ == "__main__":
    unittest.main()
