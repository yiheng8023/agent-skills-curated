import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def load(path: str) -> dict[str, object]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class Round02LocalRuntimeSyncRequestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.request = load("registry/round02-local-runtime-sync-approval-request.json")
        self.proposal = load("registry/round02-approved-payload-routing-proposal.json")
        self.manifest = load("release-manifest.json")

    def test_request_is_not_approval_and_binds_validated_source(self) -> None:
        self.assertEqual(self.request["schema_version"], 1)
        self.assertEqual(
            self.request["id"],
            "round02-local-runtime-sync-approval-request-2026-07-02",
        )
        self.assertEqual(self.request["status"], "awaiting_owner_approval")
        self.assertTrue(self.request["not_approval"])
        self.assertFalse(self.request["approval_recorded"])
        self.assertEqual(
            self.request["source_execution_record"],
            "registry/round02-approved-payload-routing-proposal.json",
        )
        self.assertEqual(
            self.proposal["status"],
            "approved_payload_routing_proposal_validated_github_only",
        )
        self.assertEqual(self.manifest["skillCount"], 20)
        self.assertEqual(self.manifest["fileCount"], 42)
        self.assertEqual(
            self.request["release_inventory"],
            {"skill_count": 20, "file_count": 42, "routing_scenario_count": 105},
        )

    def test_preflight_records_only_the_expected_local_drift(self) -> None:
        snapshot = self.request["preflight_snapshot"]
        self.assertEqual(snapshot["mode"], "read_only")
        self.assertEqual(
            snapshot["canonical_local_source"],
            r"C:\Users\15521\.cc-switch\skills",
        )
        self.assertEqual(
            snapshot["cc_switch_manifest_file_status"],
            {"match": 34, "drift": 7, "missing": 1},
        )
        self.assertEqual(
            snapshot["drift_files"],
            [
                "skills/grill-with-docs/SKILL.md",
                "skills/prototype/SKILL.md",
                "skills/review/SKILL.md",
                "skills/shipping-and-launch/SKILL.md",
                "skills/to-issues/SKILL.md",
                "skills/to-prd/SKILL.md",
                "skills/triage/SKILL.md",
            ],
        )
        self.assertEqual(
            snapshot["missing_files"],
            ["skills/obsidian-open-format-knowledge-files/SKILL.md"],
        )
        for missing in snapshot["missing_release_roots_by_directory"].values():
            self.assertEqual(missing, ["obsidian-open-format-knowledge-files"])

    def test_permissions_fail_closed_until_owner_approval(self) -> None:
        permissions = self.request["current_permissions"]
        self.assertTrue(permissions["approval_request_allowed"])
        for key, value in permissions.items():
            if key != "approval_request_allowed" and key != "network_access_required":
                self.assertFalse(value, key)
        self.assertFalse(permissions["network_access_required"])
        self.assertEqual(
            self.request["safe_approval_phrases"],
            [
                "批准执行 Round-02 local runtime sync",
                "Approve Round-02 local runtime sync only",
            ],
        )
        disallowed = set(self.request["still_disallowed"])
        self.assertIn("local runtime sync without owner approval", disallowed)
        self.assertIn(
            "modifying Codex-owned .system, codex-primary-runtime, plugin, or cache Skills",
            disallowed,
        )
        self.assertIn("promoting adapter-only, reference-only, or rejected candidates", disallowed)

    def test_doc_and_readmes_link_the_request(self) -> None:
        doc_path = self.request["evidence_doc"]
        doc = (ROOT / doc_path).read_text(encoding="utf-8")
        for phrase in [
            "This is an approval request, not approval.",
            "Read-Only Preflight",
            "批准执行 Round-02 local runtime sync",
            "Explicitly Not Requested",
            "Until the approval event exists, local runtime sync remains blocked",
        ]:
            self.assertIn(phrase, doc)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn(doc_path, readme)
        self.assertIn(doc_path, readme_zh)


if __name__ == "__main__":
    unittest.main()
