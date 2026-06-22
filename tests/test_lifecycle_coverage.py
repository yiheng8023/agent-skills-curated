import json
import unittest
from pathlib import Path

from scripts.build_topology import render


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
PRODUCT_TERMS = {"openai", "codex", "claude", "github", "figma", "superpowers"}


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
        recipe_steps = {
            step["capability"]
            for recipe in self.recipes
            for step in recipe["steps"]
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
                if item["coverageState"] == "recipe":
                    self.assertIn(item["id"], recipe_steps)

    def test_runtime_resolved_capabilities_are_product_neutral(self) -> None:
        for item in self.capabilities["capabilities"]:
            if item["coverageState"] != "runtime-resolved":
                continue
            text = json.dumps(item, ensure_ascii=False).lower()
            with self.subTest(capability=item["id"]):
                self.assertFalse(any(term in text for term in PRODUCT_TERMS))
                self.assertNotIn("owner", text)

    def test_generated_lifecycle_coverage_matches_the_registry(self) -> None:
        rendered = render()["lifecycle-coverage.md"]
        committed = (ROOT / "generated/lifecycle-coverage.md").read_text(
            encoding="utf-8"
        )
        self.assertEqual(committed, rendered)
        for item in self.capabilities["capabilities"]:
            self.assertIn(f"`{item['id']}`", rendered)
            self.assertIn(f"`{item['coverageState']}`", rendered)


if __name__ == "__main__":
    unittest.main()
