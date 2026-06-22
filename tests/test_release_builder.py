import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.build_release_manifest import build_manifest, render_manifest
from scripts.contracts import ContractError


class ReleaseBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.registry = [
            {"directory": "beta", "status": "approved"},
            {"directory": "alpha", "status": "approved"},
        ]
        for relative, data in (
            ("skills/beta/SKILL.md", b"beta"),
            ("skills/alpha/z.md", b"z"),
            ("skills/alpha/SKILL.md", b"alpha"),
        ):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)

    def test_builds_schema1_manifest_in_deterministic_path_order(self) -> None:
        manifest = build_manifest(self.root, self.registry)
        self.assertEqual(manifest["schema"], 1)
        self.assertEqual(manifest["skillCount"], 2)
        self.assertEqual(manifest["fileCount"], 3)
        self.assertEqual(
            [entry["path"] for entry in manifest["files"]],
            [
                "skills/alpha/SKILL.md",
                "skills/alpha/z.md",
                "skills/beta/SKILL.md",
            ],
        )
        first = manifest["files"][0]
        self.assertEqual(first["size"], 5)
        self.assertEqual(first["sha256"], hashlib.sha256(b"alpha").hexdigest())
        self.assertEqual(render_manifest(manifest), render_manifest(build_manifest(self.root, self.registry)))

    def test_rejects_nonapproved_inventory(self) -> None:
        registry = [{"directory": "alpha", "status": "candidate"}]
        with self.assertRaises(ContractError):
            build_manifest(self.root, registry)

    def test_render_is_canonical_json_with_final_newline(self) -> None:
        rendered = render_manifest(build_manifest(self.root, self.registry))
        self.assertTrue(rendered.endswith("\n"))
        self.assertEqual(json.loads(rendered)["schema"], 1)


if __name__ == "__main__":
    unittest.main()
