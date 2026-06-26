import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent


def load(path: str) -> dict[str, object]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class RadarFeedbackTests(unittest.TestCase):
    def setUp(self) -> None:
        self.feedback = load("registry/radar-feedback.json")
        self.sources = load("sources/lock.json")["sources"]
        self.admissions = load("registry/admissions.json")["admissions"]
        self.skills = load("registry/skills.json")["skills"]

    def test_feedback_shape_and_review_refs(self) -> None:
        self.assertEqual(self.feedback["schema"], 1)
        decisions = self.feedback["decisions"]
        self.assertGreaterEqual(len(decisions), 1)
        seen = set()
        for decision in decisions:
            with self.subTest(source=decision["id"]):
                self.assertRegex(decision["id"], r"^github:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
                self.assertIn(
                    decision["disposition"],
                    {"reject", "reference-only", "already-reviewed", "approved-elsewhere"},
                )
                self.assertIn("skill_candidate", decision["appliesTo"])
                self.assertIs(decision["runtimeEligible"], False)
                self.assertTrue(decision["reason"].strip())
                self.assertNotIn(decision["id"], seen)
                seen.add(decision["id"])
                for reference in decision["reviewRefs"]:
                    self.assertTrue((ROOT / reference).is_file(), reference)

    def test_rejected_radar_sources_are_not_runtime_inventory(self) -> None:
        rejected = {
            decision["id"]
            for decision in self.feedback["decisions"]
            if decision["disposition"] == "reject"
        }
        source_ids = {source["id"] for source in self.sources}
        admission_sources = {admission["source"] for admission in self.admissions}
        skill_sources = {skill["source"] for skill in self.skills}
        for source_id in rejected:
            with self.subTest(source=source_id):
                self.assertNotIn(source_id, source_ids)
                self.assertNotIn(source_id, admission_sources)
                self.assertNotIn(source_id, skill_sources)


if __name__ == "__main__":
    unittest.main()
