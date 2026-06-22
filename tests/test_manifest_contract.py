from copy import deepcopy
import hashlib
from pathlib import Path, PurePosixPath
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from scripts.contracts import (
    ContractError,
    canonical_payload_path,
    is_link_or_reparse,
    validate_manifest_entries,
    validate_manifest_payload,
)


DOCUMENT = "release-manifest.json"


def entry(path: str, data: bytes = b"content") -> dict[str, object]:
    return {
        "path": path,
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": len(data),
    }


class CanonicalPayloadPathTests(unittest.TestCase):
    def test_accepts_nested_posix_skill_path(self) -> None:
        self.assertEqual(
            canonical_payload_path(
                "skills/alpha/references/guide.md", DOCUMENT, "/files/0/path"
            ),
            PurePosixPath("skills/alpha/references/guide.md"),
        )

    def test_rejects_noncanonical_or_out_of_root_paths(self) -> None:
        invalid = (
            "",
            "/skills/alpha/SKILL.md",
            "C:/skills/alpha/SKILL.md",
            "skills\\alpha\\SKILL.md",
            "skills/alpha/../beta/SKILL.md",
            "skills/./alpha/SKILL.md",
            "registry/alpha/SKILL.md",
            "skills//alpha/SKILL.md",
            "skills/alpha//SKILL.md",
            "skills/alpha/SKILL.md/",
        )
        for raw in invalid:
            with self.subTest(raw=raw):
                with self.assertRaises(ContractError) as raised:
                    canonical_payload_path(raw, DOCUMENT, "/files/0/path")
                self.assertEqual(raised.exception.pointer, "/files/0/path")

    def test_rejects_repository_metadata_as_payload(self) -> None:
        invalid = (
            "generated/topology.json",
            "registry/skills.json",
            "policies/security.md",
        )
        for raw in invalid:
            with self.subTest(raw=raw):
                with self.assertRaises(ContractError) as raised:
                    canonical_payload_path(raw, DOCUMENT, "/files/0/path")
                self.assertEqual(raised.exception.pointer, "/files/0/path")


class ReparseDetectionTests(unittest.TestCase):
    def test_detects_windows_reparse_file_attribute(self) -> None:
        path = Mock(spec=Path)
        path.is_symlink.return_value = False
        path.lstat.return_value = SimpleNamespace(st_file_attributes=0x400)

        self.assertTrue(is_link_or_reparse(path))


class ManifestEntryTests(unittest.TestCase):
    def manifest(self, entries: list[dict[str, object]]) -> dict[str, object]:
        return {
            "schema": 1,
            "skillCount": 1,
            "fileCount": len(entries),
            "files": entries,
        }

    def test_rejects_duplicate_raw_path(self) -> None:
        item = entry("skills/one/SKILL.md")
        with self.assertRaises(ContractError) as raised:
            validate_manifest_entries(self.manifest([item, deepcopy(item)]), DOCUMENT)
        self.assertEqual(raised.exception.pointer, "/files/1/path")

    def test_rejects_casefold_path_collision(self) -> None:
        with self.assertRaises(ContractError) as raised:
            validate_manifest_entries(
                self.manifest(
                    [
                        entry("skills/one/SKILL.md"),
                        entry("skills/ONE/SKILL.md"),
                    ]
                ),
                DOCUMENT,
            )
        self.assertEqual(raised.exception.pointer, "/files/1/path")

    def test_rejects_invalid_digest_and_size(self) -> None:
        cases = (
            ("sha256", "A" * 64),
            ("sha256", "f" * 63),
            ("size", -1),
            ("size", True),
            ("size", 1.5),
        )
        for field, value in cases:
            with self.subTest(field=field, value=value):
                item = entry("skills/one/SKILL.md")
                item[field] = value
                with self.assertRaises(ContractError) as raised:
                    validate_manifest_entries(self.manifest([item]), DOCUMENT)
                self.assertEqual(raised.exception.pointer, f"/files/0/{field}")


class ManifestPayloadTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.registry = [
            {"directory": "alpha", "status": "approved"},
            {"directory": "beta", "status": "approved"},
        ]
        self.files = {
            "skills/alpha/SKILL.md": b"alpha skill",
            "skills/alpha/references/guide.md": b"alpha guide",
            "skills/beta/SKILL.md": b"beta skill",
        }
        for relative, data in self.files.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        self.manifest = {
            "schema": 1,
            "skillCount": 2,
            "fileCount": len(self.files),
            "files": [entry(path, data) for path, data in self.files.items()],
        }

    def assert_rejected(self, manifest: dict[str, object]) -> ContractError:
        with self.assertRaises(ContractError) as raised:
            validate_manifest_payload(self.root, manifest, self.registry)
        return raised.exception

    def test_accepts_exact_payload_coverage(self) -> None:
        validate_manifest_payload(self.root, self.manifest, self.registry)

    def test_rejects_file_omitted_from_manifest(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["files"].pop()
        self.assertEqual(self.assert_rejected(manifest).pointer, "/files")

    def test_rejects_extra_manifest_entry_for_nonexistent_file(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["files"].append(entry("skills/alpha/missing.md"))
        self.assertEqual(self.assert_rejected(manifest).pointer, "/files/3/path")

    def test_rejects_extra_payload_file(self) -> None:
        extra = self.root / "skills" / "beta" / "extra.md"
        extra.write_bytes(b"extra")
        self.assertEqual(self.assert_rejected(self.manifest).pointer, "/files")

    def test_rejects_hash_mismatch(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["files"][0]["sha256"] = "0" * 64
        self.assertEqual(self.assert_rejected(manifest).pointer, "/files/0/sha256")

    def test_rejects_size_mismatch(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["files"][0]["size"] += 1
        self.assertEqual(self.assert_rejected(manifest).pointer, "/files/0/size")

    def test_rejects_duplicate_registry_roots(self) -> None:
        for registry in (
            [
                {"directory": "alpha", "status": "approved"},
                {"directory": "alpha", "status": "approved"},
            ],
            [
                {"directory": "alpha", "status": "approved"},
                {"directory": "ALPHA", "status": "approved"},
            ],
        ):
            with self.subTest(registry=registry):
                with self.assertRaises(ContractError) as raised:
                    validate_manifest_payload(self.root, self.manifest, registry)
                self.assertEqual(raised.exception.document, "registry/skills.json")

    def test_rejects_registered_root_without_skill_file(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["files"] = [
            item
            for item in manifest["files"]
            if item["path"] != "skills/beta/SKILL.md"
        ]
        (self.root / "skills" / "beta" / "SKILL.md").unlink()
        error = self.assert_rejected(manifest)
        self.assertEqual(error.pointer, "/files")

    def test_rejects_unregistered_skill_root(self) -> None:
        registry = [{"directory": "alpha", "status": "approved"}]
        with self.assertRaises(ContractError) as raised:
            validate_manifest_payload(self.root, self.manifest, registry)
        self.assertEqual(raised.exception.pointer, "/files/2/path")

    def test_rejects_nonapproved_registry_skill(self) -> None:
        registry = deepcopy(self.registry)
        registry[1]["status"] = "candidate"
        with self.assertRaises(ContractError) as raised:
            validate_manifest_payload(self.root, self.manifest, registry)
        self.assertEqual(raised.exception.document, "registry/skills.json")
        self.assertEqual(raised.exception.pointer, "/skills/1/status")

    def test_rejects_unregistered_empty_payload_root(self) -> None:
        (self.root / "skills" / "unregistered").mkdir()
        error = self.assert_rejected(self.manifest)
        self.assertEqual(error.pointer, "/files")

    def test_rejects_reparse_reported_by_platform_probe(self) -> None:
        suspect = self.root / "skills" / "alpha" / "references"

        def is_link(path: Path) -> bool:
            return path == suspect

        with patch("scripts.contracts.is_link_or_reparse", side_effect=is_link):
            error = self.assert_rejected(self.manifest)
        self.assertIn("reparse", error.message)

    def test_rejects_payload_walk_enumeration_failure(self) -> None:
        def failing_walk(*args: object, **kwargs: object):
            onerror = kwargs.get("onerror")
            if onerror is not None:
                onerror(PermissionError("access denied"))  # type: ignore[operator]
            return iter(())

        with patch("scripts.contracts.os.walk", side_effect=failing_walk):
            error = self.assert_rejected(self.manifest)
        self.assertEqual(error.pointer, "/files")
        self.assertIn("enumerate", error.message)

    def test_rejects_real_file_symlink_when_supported(self) -> None:
        target = self.root / "outside.txt"
        target.write_bytes(b"outside")
        link = self.root / "skills" / "alpha" / "linked.md"
        try:
            link.symlink_to(target)
        except OSError as exc:
            self.skipTest(f"symlink creation unavailable: {exc}")

        with self.assertRaises(ContractError) as raised:
            validate_manifest_payload(self.root, self.manifest, self.registry)
        self.assertIn("reparse", raised.exception.message)

    def test_rejects_real_directory_symlink_when_supported(self) -> None:
        target = self.root / "outside"
        target.mkdir()
        (target / "file.md").write_bytes(b"outside")
        link = self.root / "skills" / "alpha" / "linked"
        try:
            link.symlink_to(target, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"directory symlink creation unavailable: {exc}")

        with self.assertRaises(ContractError) as raised:
            validate_manifest_payload(self.root, self.manifest, self.registry)
        self.assertIn("reparse", raised.exception.message)


if __name__ == "__main__":
    unittest.main()
