from pathlib import Path
import unittest

from scripts.contracts import (
    ContractError,
    parse_frontmatter,
    validate_adopted_selection,
    validate_inventory_counts,
    validate_selection_closure,
    validate_source_selection,
)


ROOT = Path(__file__).resolve().parent.parent


class SourceSelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source_record = {
            "id": "example:upstream",
            "revision": "abc123",
            "candidateIds": ["alpha", "beta"],
        }
        self.selection = {
            "source": "example:upstream",
            "revision": "abc123",
            "decisions": {"alpha": "adopt", "beta": "merge"},
        }
        self.allowed = {"adopt", "merge", "reject"}

    def test_accepts_selection_matching_pinned_source_inventory(self) -> None:
        validate_source_selection(
            self.selection, self.source_record, self.allowed, "selection.json"
        )

    def test_rejects_selection_for_wrong_source(self) -> None:
        selection = {**self.selection, "source": "example:other"}

        with self.assertRaises(ContractError) as raised:
            validate_source_selection(
                selection, self.source_record, self.allowed, "selection.json"
            )

        self.assertIn("/source", raised.exception.pointer)

    def test_rejects_selection_for_wrong_revision(self) -> None:
        selection = {**self.selection, "revision": "different"}

        with self.assertRaises(ContractError) as raised:
            validate_source_selection(
                selection, self.source_record, self.allowed, "selection.json"
            )

        self.assertIn("/revision", raised.exception.pointer)

    def test_rejects_selection_missing_pinned_candidate(self) -> None:
        selection = {**self.selection, "decisions": {"alpha": "adopt"}}

        with self.assertRaises(ContractError) as raised:
            validate_source_selection(
                selection, self.source_record, self.allowed, "selection.json"
            )

        self.assertIn("/decisions/beta", raised.exception.pointer)

    def test_rejects_selection_with_unpinned_extra_candidate(self) -> None:
        selection = {
            **self.selection,
            "decisions": {**self.selection["decisions"], "gamma": "reject"},
        }

        with self.assertRaises(ContractError) as raised:
            validate_source_selection(
                selection, self.source_record, self.allowed, "selection.json"
            )

        self.assertIn("/decisions/gamma", raised.exception.pointer)

    def test_candidate_error_pointer_escapes_rfc6901_tokens(self) -> None:
        source_record = {**self.source_record, "candidateIds": ["alpha/beta~rc"]}
        selection = {**self.selection, "decisions": {}}

        with self.assertRaises(ContractError) as raised:
            validate_source_selection(
                selection, source_record, self.allowed, "selection.json"
            )

        self.assertEqual(raised.exception.pointer, "/decisions/alpha~1beta~0rc")


class InventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = [
            {
                "directory": "alpha",
                "status": "approved",
                "source": "example:upstream",
            },
            {
                "directory": "beta",
                "status": "approved",
                "source": "local:reviewed-baseline",
            },
        ]
        self.manifest = {
            "skillCount": 2,
            "fileCount": 2,
            "files": [
                {"path": "skills/alpha/SKILL.md"},
                {"path": "skills/beta/SKILL.md"},
            ],
        }
        self.directories = ["alpha", "beta"]

    def test_accepts_derived_inventory_counts(self) -> None:
        validate_inventory_counts(
            self.registry, self.manifest, self.directories, "release-manifest.json"
        )

    def test_rejects_skill_count_drift_from_registry_or_directories(self) -> None:
        for registry, directories in (
            (self.registry[:1], self.directories),
            (self.registry, self.directories[:1]),
        ):
            with self.subTest(registry=registry, directories=directories):
                with self.assertRaises(ContractError) as raised:
                    validate_inventory_counts(
                        registry, self.manifest, directories, "release-manifest.json"
                    )
                self.assertIn("/skillCount", raised.exception.pointer)

    def test_rejects_file_count_drift(self) -> None:
        manifest = {**self.manifest, "fileCount": 3}

        with self.assertRaises(ContractError) as raised:
            validate_inventory_counts(
                self.registry, manifest, self.directories, "release-manifest.json"
            )

        self.assertIn("/fileCount", raised.exception.pointer)

    def test_rejects_nonlist_manifest_files_at_files_pointer(self) -> None:
        manifest = {**self.manifest, "files": {"path": "skills/alpha/SKILL.md"}}

        with self.assertRaises(ContractError) as raised:
            validate_inventory_counts(
                self.registry, manifest, self.directories, "release-manifest.json"
            )

        self.assertIn("/files", raised.exception.pointer)

    def test_rejects_manifest_skill_roots_drift(self) -> None:
        manifest = {
            **self.manifest,
            "files": [
                {"path": "skills/alpha/SKILL.md"},
                {"path": "skills/alpha/reference.md"},
            ],
        }

        with self.assertRaises(ContractError) as raised:
            validate_inventory_counts(
                self.registry, manifest, self.directories, "release-manifest.json"
            )

        self.assertIn("/skillCount", raised.exception.pointer)

    def test_rejects_equal_count_manifest_with_wrong_skill_root(self) -> None:
        manifest = {
            **self.manifest,
            "files": [
                {"path": "skills/alpha/SKILL.md"},
                {"path": "skills/gamma/SKILL.md"},
            ],
        }

        with self.assertRaises(ContractError) as raised:
            validate_inventory_counts(
                self.registry, manifest, self.directories, "release-manifest.json"
            )

        self.assertIn("/files", raised.exception.pointer)

    def test_accepts_any_nonempty_closed_selection(self) -> None:
        validate_selection_closure(
            {"alpha": "adopt", "beta": "merge"},
            {"adopt", "merge", "reject"},
            "selection.json",
        )

    def test_rejects_empty_selection(self) -> None:
        with self.assertRaises(ContractError) as raised:
            validate_selection_closure({}, {"adopt"}, "selection.json")

        self.assertIn("/decisions", raised.exception.pointer)

    def test_rejects_empty_selection_name(self) -> None:
        with self.assertRaises(ContractError) as raised:
            validate_selection_closure({"": "adopt"}, {"adopt"}, "selection.json")

        self.assertIn("/decisions", raised.exception.pointer)

    def test_rejects_unknown_selection_disposition(self) -> None:
        with self.assertRaises(ContractError) as raised:
            validate_selection_closure(
                {"alpha": "retired"}, {"adopt", "reject"}, "selection.json"
            )

        self.assertIn("/decisions/alpha", raised.exception.pointer)

    def test_decision_error_pointer_escapes_rfc6901_tokens(self) -> None:
        with self.assertRaises(ContractError) as raised:
            validate_selection_closure(
                {"alpha/beta~rc": "retired"},
                {"adopt", "reject"},
                "selection.json",
            )

        self.assertEqual(raised.exception.pointer, "/decisions/alpha~1beta~0rc")

    def test_accepts_adopted_registry_source_alignment(self) -> None:
        validate_adopted_selection(
            {"alpha": "adopt", "upstream-merged": "merge"},
            self.registry,
            "example:upstream",
            "selection.json",
        )

    def test_rejects_adopt_without_registry_directory(self) -> None:
        with self.assertRaises(ContractError) as raised:
            validate_adopted_selection(
                {"missing": "adopt"},
                self.registry,
                "example:upstream",
                "selection.json",
            )

        self.assertIn("/decisions/missing", raised.exception.pointer)

    def test_rejects_adopt_with_wrong_registry_source(self) -> None:
        with self.assertRaises(ContractError) as raised:
            validate_adopted_selection(
                {"beta": "adopt"},
                self.registry,
                "example:upstream",
                "selection.json",
            )

        self.assertIn("/decisions/beta", raised.exception.pointer)

    def test_rejects_approved_source_registry_entry_without_adopt_closure(self) -> None:
        with self.assertRaises(ContractError) as raised:
            validate_adopted_selection(
                {"alpha": "merge"},
                self.registry,
                "example:upstream",
                "selection.json",
            )

        self.assertIn("/decisions/alpha", raised.exception.pointer)

    def test_rejects_nonapproved_source_registry_entry_without_adopt_closure(self) -> None:
        registry = self.registry + [
            {
                "directory": "candidate",
                "status": "reviewed",
                "source": "example:upstream",
            }
        ]

        with self.assertRaises(ContractError) as raised:
            validate_adopted_selection(
                {"alpha": "adopt"},
                registry,
                "example:upstream",
                "selection.json",
            )

        self.assertIn("/decisions/candidate", raised.exception.pointer)


class FrontmatterTests(unittest.TestCase):
    def test_parses_adopted_skill_metadata_mapping(self) -> None:
        document = "skills/ci-cd-and-automation/SKILL.md"
        text = (ROOT / document).read_text(encoding="utf-8")

        metadata = parse_frontmatter(text, document)

        self.assertEqual(
            metadata["metadata"],
            {
                "source": "https://github.com/addyosmani/agent-skills/tree/17214a29c429a19f7a9607f2c06f9d650ea87eb0/skills/ci-cd-and-automation",
                "license": "MIT",
                "adapted-for": "cross-agent",
            },
        )

    def test_parses_caveman_folded_description(self) -> None:
        text = """---
name: folded-example
description: >
  First line of a folded
  description remains readable.
---
"""

        metadata = parse_frontmatter(text, "folded-example.md")

        self.assertEqual(
            metadata["description"],
            "First line of a folded description remains readable.",
        )

    def test_rejects_duplicate_keys(self) -> None:
        text = "---\nname: first\nname: second\n---\n"

        with self.assertRaisesRegex(ContractError, "duplicate key"):
            parse_frontmatter(text, "duplicate.md")

    def test_rejects_yaml_tags_anchors_and_aliases(self) -> None:
        for value in ("!!str value", "&anchor value", "*anchor"):
            with self.subTest(value=value):
                text = f"---\nname: {value}\n---\n"
                with self.assertRaises(ContractError):
                    parse_frontmatter(text, "unsafe.md")

    def test_rejects_ambiguous_plain_scalars(self) -> None:
        for value in ("value: nested", "value # comment"):
            with self.subTest(value=value):
                text = f"---\nname: {value}\n---\n"
                with self.assertRaises(ContractError):
                    parse_frontmatter(text, "ambiguous.md")

    def test_rejects_plain_scalars_starting_with_yaml_indicators(self) -> None:
        for value in ("@bad", "`bad", "#bad", ",bad", "[bad"):
            with self.subTest(value=value):
                text = f"---\nname: {value}\n---\n"
                with self.assertRaises(ContractError):
                    parse_frontmatter(text, "indicator.md")

    def test_parses_quoted_and_literal_scalars(self) -> None:
        text = (
            "---\n"
            "single: 'safe: value # text'\n"
            'double: "safe: value # text"\n'
            "literal: |\n"
            "  first line\n"
            "  second line\n"
            "---\n"
        )

        metadata = parse_frontmatter(text, "scalars.md")

        self.assertEqual(metadata["single"], "safe: value # text")
        self.assertEqual(metadata["double"], "safe: value # text")
        self.assertEqual(metadata["literal"], "first line\nsecond line")

    def test_rejects_folded_blocks_with_blank_or_deep_lines(self) -> None:
        cases = (
            "---\ndescription: >\n  first\n\n  second\n---\n",
            "---\ndescription: >\n  first\n    deeper\n---\n",
        )
        for text in cases:
            with self.subTest(text=text):
                with self.assertRaises(ContractError):
                    parse_frontmatter(text, "folded.md")

    def test_rejects_duplicate_or_misindented_mapping_entries(self) -> None:
        cases = (
            "---\nmetadata:\n  source: first\n  source: second\n---\n",
            "---\nmetadata:\n   source: value\n---\n",
        )
        for text in cases:
            with self.subTest(text=text):
                with self.assertRaises(ContractError):
                    parse_frontmatter(text, "metadata.md")


if __name__ == "__main__":
    unittest.main()
