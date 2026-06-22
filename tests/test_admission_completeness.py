import json
from pathlib import Path
import unittest

from scripts.contracts import (
    validate_admissions_document,
    validate_routing_document,
)


ROOT = Path(__file__).resolve().parent.parent
GENERIC_INCREMENT_PHRASES = {
    "helps the agent perform the task",
    "provides guidance",
    "improves results",
    "makes the agent better",
}
NON_NEUTRAL_NAME_PARTS = {"claude", "matt", "pocock"}


def load(path: str) -> dict[str, object]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class AdmissionCompletenessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.skills = load("registry/skills.json")["skills"]
        self.admissions = load("registry/admissions.json")["admissions"]
        self.routing = load("registry/routing.json")["routes"]
        self.sources = load("sources/lock.json")["sources"]

    def test_documents_pass_shape_contracts(self) -> None:
        validate_admissions_document(
            {"schema": 1, "admissions": self.admissions},
            "registry/admissions.json",
        )
        validate_routing_document(
            {"schema": 1, "routes": self.routing},
            "registry/routing.json",
        )

    def test_approved_inventory_equals_approved_admissions_and_routes(self) -> None:
        approved = {item["id"] for item in self.skills}
        admitted = {
            item["skill"]
            for item in self.admissions
            if item["disposition"] == "approve"
        }
        routed = {item["skill"] for item in self.routing}
        self.assertEqual(approved, admitted)
        self.assertEqual(approved, routed)

    def test_approved_sources_have_complete_pinned_provenance(self) -> None:
        source_by_id = {item["id"]: item for item in self.sources}
        for admission in self.admissions:
            if admission["disposition"] != "approve":
                continue
            source = source_by_id[admission["source"]]
            with self.subTest(skill=admission["skill"]):
                self.assertEqual("git", source["kind"])
                self.assertEqual("complete", source["provenanceStatus"])
                self.assertEqual("license-governed", source["redistribution"])
                self.assertTrue(source.get("url"))
                self.assertRegex(source.get("revision", ""), r"^[0-9a-f]{40}$")
                self.assertTrue(source.get("license"))

    def test_every_approved_skill_has_a_specific_native_increment(self) -> None:
        for admission in self.admissions:
            if admission["disposition"] != "approve":
                continue
            increment = admission["nativeIncrement"].strip().lower()
            with self.subTest(skill=admission["skill"]):
                self.assertGreaterEqual(len(increment), 40)
                self.assertNotIn(increment, GENERIC_INCREMENT_PHRASES)
                self.assertTrue(admission["reviewRefs"])
                for reference in admission["reviewRefs"]:
                    self.assertTrue((ROOT / reference).is_file(), reference)

    def test_incomplete_sources_are_never_runtime_approved(self) -> None:
        for source in self.sources:
            if source["provenanceStatus"] == "incomplete":
                self.assertFalse(source["approvedForRuntime"])

    def test_approved_runtime_names_are_agent_and_author_neutral(self) -> None:
        for skill in self.skills:
            identity = " ".join(
                str(skill[field]).lower() for field in ("id", "directory", "name")
            )
            for forbidden in NON_NEUTRAL_NAME_PARTS:
                with self.subTest(skill=skill["id"], forbidden=forbidden):
                    self.assertNotIn(forbidden, identity)

    def test_nonapproved_admissions_do_not_remain_in_release_inventory(self) -> None:
        approved = {item["id"] for item in self.skills}
        for admission in self.admissions:
            if admission["disposition"] == "approve":
                continue
            with self.subTest(skill=admission["skill"]):
                self.assertNotIn(admission["skill"], approved)


if __name__ == "__main__":
    unittest.main()
