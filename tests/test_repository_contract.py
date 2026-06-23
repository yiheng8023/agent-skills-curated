import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def snapshot(root: Path) -> dict[str, tuple[str, int]]:
    result: dict[str, tuple[str, int]] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if ".git" in relative.parts or "__pycache__" in relative.parts:
            continue
        if path.suffix == ".pyc":
            continue
        result[relative.as_posix()] = (
            hashlib.sha256(path.read_bytes()).hexdigest(),
            path.stat().st_mtime_ns,
        )
    return result


def run_python(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-B", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )


def copy_repo(target: Path) -> None:
    shutil.copytree(
        ROOT,
        target,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
    )


class RepositoryContractTests(unittest.TestCase):
    def test_build_check_is_read_only(self) -> None:
        before = snapshot(ROOT)
        run_python(ROOT, "scripts/build_topology.py", "--check")
        self.assertEqual(before, snapshot(ROOT))

    def test_emit_is_byte_deterministic(self) -> None:
        command = ("scripts/build_topology.py", "--emit", "topology.json")
        first = run_python(ROOT, *command).stdout
        second = run_python(ROOT, *command).stdout
        self.assertEqual(first, second)

    def test_registry_change_makes_check_fail_in_temporary_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / "repo"
            copy_repo(copy)
            path = copy / "registry/capabilities.json"
            document = json.loads(path.read_text(encoding="utf-8"))
            document["capabilities"].append({
                "id": "capability.fixture",
                "stage": "verify",
                "description": "Fixture capability used only to prove generated drift.",
                "coverageState": "native-sufficient",
                "validation": ["Check that generated topology detects drift."],
                "fallback": ["Remove the fixture after the temporary check."],
            })
            path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, "-B", "scripts/build_topology.py", "--check"],
                cwd=copy,
                capture_output=True,
                text=True,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Stale generated files", result.stderr + result.stdout)

    def test_generated_file_change_makes_check_fail_in_temporary_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / "repo"
            copy_repo(copy)
            with (copy / "generated/catalog.md").open("a", encoding="utf-8") as handle:
                handle.write("manual drift\n")

            result = subprocess.run(
                [sys.executable, "-B", "scripts/build_topology.py", "--check"],
                cwd=copy,
                capture_output=True,
                text=True,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Stale generated files", result.stderr + result.stdout)

    def test_topology_projection_contains_only_governed_inputs(self) -> None:
        topology = json.loads((ROOT / "generated/topology.json").read_text(encoding="utf-8"))
        self.assertEqual(
            set(topology),
            {"schema", "skills", "capabilities", "relations", "conflicts", "recipes"},
        )


if __name__ == "__main__":
    unittest.main()
