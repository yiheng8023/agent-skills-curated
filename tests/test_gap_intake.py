import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent


class GapIntakeTests(unittest.TestCase):
    def test_no_lifecycle_capability_remains_unclassified_as_gap(self) -> None:
        capabilities = json.loads(
            (ROOT / "registry/capabilities.json").read_text(encoding="utf-8")
        )["capabilities"]
        self.assertEqual(
            [item["id"] for item in capabilities if item["coverageState"] == "gap"],
            [],
        )

    def test_data_modeling_uses_composition_instead_of_an_overlapping_skill(self) -> None:
        recipes = json.loads(
            (ROOT / "registry/recipes.json").read_text(encoding="utf-8")
        )["recipes"]
        recipe = next(item for item in recipes if item["id"] == "recipe.data-modeling")
        self.assertGreaterEqual(len({step["capability"] for step in recipe["steps"]}), 2)
        inventory = json.loads(
            (ROOT / "registry/skills.json").read_text(encoding="utf-8")
        )["skills"]
        self.assertNotIn("domain-modeling", {item["directory"] for item in inventory})


if __name__ == "__main__":
    unittest.main()
