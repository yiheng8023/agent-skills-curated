import json
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.build_topology import markdown_cell, render
from scripts.contracts import ContractError, validate_lifecycle_coverage


ROOT = Path(__file__).resolve().parent.parent
EXPECTED_CAPABILITIES = {
    f"capability.{name}"
    for name in (
        "requirements-clarification",
        "prd-rfc",
        "problem-decomposition",
        "architecture-design",
        "interface-api-design",
        "data-modeling",
        "frontend-design",
        "backend-implementation",
        "tdd",
        "test-strategy",
        "code-review",
        "security-audit",
        "privacy-governance",
        "performance",
        "observability",
        "ci-cd",
        "release-readiness",
        "migration-deprecation",
        "rollback-recovery",
        "fault-diagnosis",
        "issue-triage",
        "documentation-governance",
        "knowledge-capture",
        "technical-debt",
        "cross-agent-handoff",
        "retrospective-evolution",
    )
}
ALLOWED_STATES = {
    "curated",
    "recipe",
    "runtime-resolved",
    "native-sufficient",
    "human-authority",
    "gap",
}


def load(path: str) -> dict[str, object]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class LifecycleCoverageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.capabilities = load("registry/capabilities.json")
        self.skills = load("registry/skills.json")["skills"]
        self.relations = load("registry/relations.json")["relations"]
        self.recipes = load("registry/recipes.json")["recipes"]

    def test_registry_is_schema2_and_covers_the_stable_lifecycle_ids(self) -> None:
        self.assertEqual(self.capabilities["schema"], 2)
        actual = {item["id"] for item in self.capabilities["capabilities"]}
        self.assertEqual(actual, EXPECTED_CAPABILITIES)

    def test_every_capability_has_actionable_coverage_evidence(self) -> None:
        approved = {
            item["id"] for item in self.skills if item["status"] == "approved"
        }
        provides = {
            (item["from"], item["to"])
            for item in self.relations
            if item["type"] == "provides"
        }
        for item in self.capabilities["capabilities"]:
            with self.subTest(capability=item["id"]):
                self.assertTrue(item["stage"])
                self.assertTrue(item["description"])
                self.assertIn(item["coverageState"], ALLOWED_STATES)
                self.assertTrue(item["validation"])
                self.assertTrue(item["fallback"])
                if item["coverageState"] == "curated":
                    self.assertTrue(item["curatedOwners"])
                    for owner in item["curatedOwners"]:
                        self.assertIn(owner, approved)
                        self.assertIn((owner, item["id"]), provides)
                else:
                    self.assertNotIn("curatedOwners", item)

    def test_recipe_coverage_requires_a_matching_composition(self) -> None:
        cases = []
        orphan = deepcopy(self.recipes)
        orphan[:] = [item for item in orphan if item["id"] != "recipe.test-strategy"]
        cases.append((orphan, "/capabilities/9/coverageState"))

        singleton = deepcopy(self.recipes)
        singleton[0]["steps"] = [
            {"capability": "capability.requirements-clarification"}
        ]
        cases.append((singleton, "/recipes/0/steps"))

        duplicate = deepcopy(self.recipes)
        duplicate[0]["steps"] = [
            {"capability": "capability.requirements-clarification"},
            {"capability": "capability.requirements-clarification"},
        ]
        cases.append((duplicate, "/recipes/0/steps/1/capability"))

        self_reference = deepcopy(self.recipes)
        self_reference[0]["steps"].insert(
            0, {"capability": "capability.test-strategy"}
        )
        cases.append((self_reference, "/recipes/0/steps/0/capability"))

        wrong_identity = deepcopy(self.recipes)
        wrong_identity[0]["id"] = "recipe.other-strategy"
        cases.append((wrong_identity, "/capabilities/9/coverageState"))

        for recipes, pointer in cases:
            with self.subTest(pointer=pointer):
                with self.assertRaises(ContractError) as raised:
                    validate_lifecycle_coverage(
                        self.capabilities,
                        {"schema": 1, "recipes": recipes},
                    )
                self.assertEqual(raised.exception.pointer, pointer)

    def test_runtime_resolved_capabilities_use_a_structural_resolution_marker(self) -> None:
        for item in self.capabilities["capabilities"]:
            if item["coverageState"] != "runtime-resolved":
                continue
            with self.subTest(capability=item["id"]):
                self.assertEqual(
                    item["runtimeResolution"], "visible-capability-inventory"
                )
                self.assertNotIn("curatedOwners", item)

    def test_generated_lifecycle_coverage_matches_the_registry(self) -> None:
        rendered = render()["lifecycle-coverage.md"]
        committed = (ROOT / "generated/lifecycle-coverage.md").read_text(
            encoding="utf-8"
        )
        self.assertEqual(committed, rendered)
        for item in self.capabilities["capabilities"]:
            self.assertIn(f"`{item['id']}`", rendered)
            self.assertIn(f"`{item['coverageState']}`", rendered)

    def test_markdown_cells_escape_table_and_line_break_syntax(self) -> None:
        self.assertEqual(
            markdown_cell("alpha|beta\ngamma\\delta\r\nomega"),
            r"alpha\|beta<br>gamma\\delta<br>omega",
        )


if __name__ == "__main__":
    unittest.main()
