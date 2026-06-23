import json
from pathlib import Path
import unittest

from scripts.simulate_routing import load_model, resolve, run_scenarios


ROOT = Path(__file__).resolve().parent.parent


class RoutingResolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_model(ROOT)

    def facts(self, capability: str, **overrides: object) -> dict[str, object]:
        facts: dict[str, object] = {
            "requestedCapabilities": [capability],
            "available": ["native", "runtime", "curated"],
            "contextSatisfied": True,
            "negativeMatch": False,
            "nativeEquivalent": False,
            "runtimeEquivalent": False,
            "risk": "low",
            "permissionExpansion": False,
            "unresolvedConflict": False,
            "ambiguous": False,
        }
        facts.update(overrides)
        return facts

    def test_native_and_runtime_equivalence_precede_curated(self) -> None:
        native = resolve(
            self.facts("capability.code-review", nativeEquivalent=True), self.model
        )
        runtime = resolve(
            self.facts("capability.code-review", runtimeEquivalent=True), self.model
        )
        self.assertEqual(native["decision"], "native")
        self.assertEqual(runtime["decision"], "runtime")

    def test_curated_and_recipe_routes_are_selected_only_when_eligible(self) -> None:
        curated = resolve(self.facts("capability.code-review"), self.model)
        recipe = resolve(self.facts("capability.test-strategy"), self.model)
        self.assertEqual(curated["decision"], "curated")
        self.assertEqual(curated["selectedIds"], ["skill.curated.review"])
        self.assertEqual(recipe["decision"], "recipe")
        self.assertEqual(recipe["selectedIds"], ["recipe.test-strategy"])

    def test_negative_context_and_authority_boundaries_fail_closed(self) -> None:
        no_skill = resolve(
            self.facts("capability.code-review", negativeMatch=True), self.model
        )
        missing = resolve(
            self.facts("capability.code-review", contextSatisfied=False), self.model
        )
        high_risk = resolve(
            self.facts("capability.code-review", risk="high"), self.model
        )
        self.assertEqual(no_skill["decision"], "no-skill")
        self.assertEqual(missing["decision"], "gap")
        self.assertEqual(high_risk["decision"], "ask-user")

    def test_permission_conflict_and_ambiguity_require_confirmation(self) -> None:
        for field in ("permissionExpansion", "unresolvedConflict", "ambiguous"):
            with self.subTest(field=field):
                decision = resolve(
                    self.facts("capability.code-review", **{field: True}), self.model
                )
                self.assertEqual(decision["decision"], "ask-user")
                self.assertTrue(decision["confirmationReason"])


class RoutingCorpusTests(unittest.TestCase):
    def test_corpus_has_all_required_families_and_at_least_96_cases(self) -> None:
        document = json.loads((ROOT / "registry/scenarios.json").read_text(encoding="utf-8"))
        scenarios = document["scenarios"]
        self.assertGreaterEqual(len(scenarios), 96)
        minimums = {
            "lifecycle": 26,
            "native-no-skill": 12,
            "runtime-preference": 12,
            "curated-workflow": 12,
            "recipe-dag": 8,
            "negative-near-match": 10,
            "authority-ambiguity": 8,
            "fallback-gap": 8,
            "execution-reroute": 6,
        }
        for family, minimum in minimums.items():
            with self.subTest(family=family):
                self.assertGreaterEqual(
                    sum(item["family"] == family for item in scenarios), minimum
                )

    def test_every_scenario_matches_the_deterministic_resolver(self) -> None:
        report = run_scenarios(ROOT)
        self.assertGreaterEqual(report["scenarioCount"], 96)
        self.assertEqual(report["failed"], 0)
        self.assertEqual(report["unclassifiedLifecycleCapabilities"], [])


if __name__ == "__main__":
    unittest.main()
