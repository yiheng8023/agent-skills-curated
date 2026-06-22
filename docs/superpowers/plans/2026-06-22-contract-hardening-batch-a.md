# Contract Hardening Batch A Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Harden the current schema-1 curated release with deterministic,
fail-closed contracts without changing the manifest interface consumed by
`codex-user-config`.

**Architecture:** Add a zero-network contract module used by the existing
verifier, exercise it with standard-library `unittest` fixtures, and keep
`release-manifest.json` schema 1 compatible. Checked-in schemas document the
current governed formats; explicit Python validators enforce them and add
cross-document semantic checks.

**Tech Stack:** Python 3 standard library, JSON, `unittest`, GitHub Actions.

---

## File Map

- Create `scripts/contracts.py`: strict frontmatter parsing, diagnostics,
  structural helpers, reference checks, inventory checks, and manifest safety.
- Create `tests/test_contracts.py`: isolated unit and fixture tests.
- Create `tests/test_repository_contract.py`: repository-level read-only and
  deterministic behavior tests.
- Create `schemas/v1/*.schema.json`: current contract documents for Skills,
  capabilities, relations, conflicts, recipes, source locks, selections, and
  the release manifest.
- Modify `scripts/verify.py`: delegate contract behavior and remove frozen
  inventory/source counts.
- Modify `registry/skills.json`: repair the `caveman` folded description.
- Modify `sources/lock.json`: register the legacy local baseline explicitly.
- Modify `.github/workflows/validate.yml`: run tests before repository verify.
- Modify governance documentation only where the implemented contract changes
  an existing claim.

## Task 1: Strict Frontmatter Tracer Bullet

**Files:**
- Create: `tests/test_contracts.py`
- Create: `scripts/contracts.py`
- Modify: `scripts/verify.py`
- Modify: `registry/skills.json`

- [ ] **Step 1: Write the failing folded-scalar test**

```python
from pathlib import Path
import unittest

from scripts.contracts import ContractError, parse_frontmatter


ROOT = Path(__file__).resolve().parents[1]


class FrontmatterTests(unittest.TestCase):
    def test_caveman_folded_description_is_semantically_parsed(self) -> None:
        text = (ROOT / "skills/caveman/SKILL.md").read_text(encoding="utf-8")
        metadata = parse_frontmatter(text, "skills/caveman/SKILL.md")
        self.assertTrue(metadata["description"].startswith("Ultra-compressed communication mode."))
        self.assertIn('Use when user says "caveman mode"', metadata["description"])
        self.assertNotEqual(metadata["description"], ">")

    def test_frontmatter_rejects_duplicate_keys(self) -> None:
        with self.assertRaisesRegex(ContractError, "duplicate key"):
            parse_frontmatter("---\nname: one\nname: two\n---\n", "fixture.md")

    def test_frontmatter_rejects_yaml_tags_anchors_and_aliases(self) -> None:
        for value in ("!!python/object:x", "&anchor value", "*anchor"):
            with self.subTest(value=value), self.assertRaises(ContractError):
                parse_frontmatter(f"---\nname: {value}\n---\n", "fixture.md")
```

- [ ] **Step 2: Run the test and confirm RED**

Run:

```bash
python -m unittest tests.test_contracts.FrontmatterTests -v
```

Expected: import failure because `scripts/contracts.py` does not exist.

- [ ] **Step 3: Implement the strict scalar-only parser**

Create `scripts/contracts.py` with:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
import re
from typing import Any


@dataclass(frozen=True)
class ContractError(ValueError):
    document: str
    pointer: str
    message: str

    def __str__(self) -> str:
        return f"{self.document}{self.pointer}: {self.message}"


_KEY = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
_FORBIDDEN_YAML = ("!!", "&", "*")


def _decode_inline(value: str, document: str, pointer: str) -> str:
    if value.startswith(_FORBIDDEN_YAML):
        raise ContractError(document, pointer, "YAML tags, anchors, and aliases are unsupported")
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('\"', "'"):
        return value[1:-1]
    return value


def parse_frontmatter(text: str, document: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ContractError(document, "", "missing frontmatter opening delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ContractError(document, "", "missing frontmatter closing delimiter") from exc

    result: dict[str, str] = {}
    index = 1
    while index < end:
        line = lines[index]
        if not line or line.startswith((" ", "\t")) or ":" not in line:
            raise ContractError(document, f"/line/{index + 1}", "expected a top-level scalar key")
        key, raw = line.split(":", 1)
        if not _KEY.fullmatch(key):
            raise ContractError(document, f"/line/{index + 1}", "invalid key")
        if key in result:
            raise ContractError(document, f"/{key}", "duplicate key")
        raw = raw.strip()
        if raw in (">", "|"):
            block: list[str] = []
            index += 1
            while index < end and (not lines[index] or lines[index].startswith("  ")):
                block.append(lines[index][2:] if lines[index].startswith("  ") else "")
                index += 1
            if not block:
                raise ContractError(document, f"/{key}", "empty block scalar")
            result[key] = (" ".join(part.strip() for part in block).strip()
                           if raw == ">" else "\n".join(block).rstrip())
            continue
        result[key] = _decode_inline(raw, document, f"/{key}")
        index += 1
    return result
```

Replace the local `frontmatter()` function in `scripts/verify.py` with an import
from `scripts.contracts`.

- [ ] **Step 4: Repair the registry value and verify GREEN**

Set `skill.curated.caveman.description` to the complete folded description
returned by `parse_frontmatter()`, then run:

```bash
python -m unittest tests.test_contracts.FrontmatterTests -v
python scripts/verify.py
```

Expected: all frontmatter tests pass and repository verification passes.

- [ ] **Step 5: Review checkpoint**

Run `git diff --check` and inspect only the four Task 1 files. Do not commit or
push without explicit user authorization.

## Task 2: Dynamic Inventory and Source Selection

**Files:**
- Modify: `tests/test_contracts.py`
- Modify: `scripts/contracts.py`
- Modify: `scripts/verify.py`

- [ ] **Step 1: Write failing dynamic-count tests**

```python
class InventoryTests(unittest.TestCase):
    def test_counts_are_derived_from_current_documents(self) -> None:
        registry = [{"id": "skill.one", "directory": "one"},
                    {"id": "skill.two", "directory": "two"}]
        manifest = {
            "skillCount": 2,
            "fileCount": 2,
            "files": [
                {"path": "skills/one/SKILL.md"},
                {"path": "skills/two/SKILL.md"},
            ],
        }
        validate_inventory_counts(registry, manifest, {"one", "two"})

    def test_manifest_count_mismatch_has_pointer(self) -> None:
        with self.assertRaisesRegex(ContractError, "/fileCount"):
            validate_inventory_counts(
                [{"id": "skill.one", "directory": "one"}],
                {"skillCount": 1, "fileCount": 7,
                 "files": [{"path": "skills/one/SKILL.md"}]},
                {"one"},
            )

    def test_selection_closure_does_not_require_addy_magic_counts(self) -> None:
        validate_selection_closure(
            {"alpha": "adopt", "beta": "reject"},
            {"adopt", "merge", "adapter-only", "recipe-only", "reject"},
            "fixture-selection.json",
        )
```

Import `validate_inventory_counts` and `validate_selection_closure` from
`scripts.contracts`.

- [ ] **Step 2: Confirm RED**

Run `python -m unittest tests.test_contracts.InventoryTests -v`.

Expected: import failure for the new functions.

- [ ] **Step 3: Implement derived invariants**

Add functions that:

```python
def validate_inventory_counts(registry, manifest, directories):
    expected_skills = {item["directory"] for item in registry}
    if expected_skills != set(directories):
        raise ContractError("registry/skills.json", "/skills", "directories do not match skills/")
    if manifest.get("skillCount") != len(expected_skills):
        raise ContractError("release-manifest.json", "/skillCount", "must equal registered Skill count")
    files = manifest.get("files")
    if not isinstance(files, list):
        raise ContractError("release-manifest.json", "/files", "must be an array")
    if manifest.get("fileCount") != len(files):
        raise ContractError("release-manifest.json", "/fileCount", "must equal files length")


def validate_selection_closure(decisions, dispositions, document):
    if not decisions:
        raise ContractError(document, "/decisions", "must not be empty")
    for name, decision in decisions.items():
        if not name or decision not in dispositions:
            raise ContractError(document, f"/decisions/{name}", "invalid disposition")
```

Replace the `34`, `60`, `24`, `5`, and `ADDY_APPROVED` count assumptions in
`scripts/verify.py`. Derive adopted directories from the selection document and
verify that each adopted directory has the source recorded in its registry
entry.

- [ ] **Step 4: Verify GREEN**

Run:

```bash
python -m unittest tests.test_contracts.InventoryTests -v
python scripts/verify.py
```

Expected: tests and repository verification pass.

- [ ] **Step 5: Review checkpoint**

Run `git diff --check`; do not commit or push without user authorization.

## Task 3: Structural Contract Schemas and Stable Diagnostics

**Files:**
- Create: `schemas/v1/skills.schema.json`
- Create: `schemas/v1/capabilities.schema.json`
- Create: `schemas/v1/relations.schema.json`
- Create: `schemas/v1/conflicts.schema.json`
- Create: `schemas/v1/recipes.schema.json`
- Create: `schemas/v1/sources-lock.schema.json`
- Create: `schemas/v1/selection.schema.json`
- Create: `schemas/v1/release-manifest.schema.json`
- Modify: `tests/test_contracts.py`
- Modify: `scripts/contracts.py`
- Modify: `scripts/verify.py`

- [ ] **Step 1: Write failing diagnostic tests**

```python
class ShapeTests(unittest.TestCase):
    def test_unknown_skill_field_is_rejected_with_pointer(self) -> None:
        item = {
            "id": "skill.curated.example", "directory": "example",
            "name": "example", "description": "Use when testing.",
            "status": "approved", "phase": "general",
            "source": "local:reviewed-baseline", "statuz": "approved",
        }
        with self.assertRaisesRegex(ContractError, "/skills/0/statuz"):
            validate_skill_registry({"schema": 1, "skills": [item]})

    def test_invalid_status_is_rejected(self) -> None:
        item = {
            "id": "skill.curated.example", "directory": "example",
            "name": "example", "description": "Use when testing.",
            "status": "banana", "phase": "general",
            "source": "local:reviewed-baseline",
        }
        with self.assertRaisesRegex(ContractError, "/skills/0/status"):
            validate_skill_registry({"schema": 1, "skills": [item]})
```

- [ ] **Step 2: Confirm RED**

Run `python -m unittest tests.test_shape_contracts.ShapeTests -v`.

Expected: missing validator import.

- [ ] **Step 3: Add checked-in schema documents**

Each schema uses Draft 2020-12 vocabulary, `additionalProperties: false`, a
constant schema version of 1, required current fields, controlled lifecycle and
disposition enums, stable ID patterns, canonical relative path patterns, and
the exact optional fields currently supported. No v2 field is added in Batch A.

Example Skill item contract:

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["id", "directory", "name", "description", "status", "phase", "source"],
  "properties": {
    "id": {"type": "string", "pattern": "^skill\\.curated\\.[a-z0-9][a-z0-9-]*$"},
    "directory": {"type": "string", "pattern": "^[a-z0-9][a-z0-9-]*$"},
    "name": {"type": "string", "minLength": 1},
    "description": {"type": "string", "minLength": 1},
    "status": {"enum": ["candidate", "adapted", "reviewed", "approved", "deprecated", "retired"]},
    "phase": {"type": "string", "minLength": 1},
    "source": {"type": "string", "minLength": 1}
  }
}
```

- [ ] **Step 4: Implement explicit structural validators**

Add small helpers `require_object`, `require_array`, `require_string`,
`require_keys`, `reject_unknown`, and per-document validators. Every failure
raises `ContractError(document, pointer, message)`. Validators accept only the
fields and enums declared by the checked-in schema documents.

Do not implement a partial general-purpose JSON Schema interpreter. The schema
documents are portable contracts; repository validators are the dependency-free
enforcement implementation.

- [ ] **Step 5: Integrate and verify GREEN**

Call all document validators before semantic checks in `scripts/verify.py`.

Run:

```bash
python -m unittest tests.test_shape_contracts.ShapeTests -v
python scripts/verify.py
```

Expected: all tests and repository verification pass with no traceback.

## Task 4: Cross-Document Reference and Recipe Integrity

**Files:**
- Modify: `tests/test_contracts.py`
- Modify: `scripts/contracts.py`
- Modify: `scripts/verify.py`

- [ ] **Step 1: Write failing semantic tests**

Add a minimal fixture and concrete tests:

```python
from copy import deepcopy


def reference_fixture() -> dict[str, object]:
    return {
        "skills": [{
            "id": "skill.curated.one", "directory": "one", "name": "one",
            "description": "Use when testing one.", "status": "approved",
            "phase": "general", "source": "local:reviewed-baseline",
        }],
        "capabilities": [{
            "id": "capability.one", "canonicalOwner": "skill.curated.one",
        }],
        "relations": [{
            "from": "skill.curated.one", "type": "provides",
            "to": "capability.one",
        }],
        "conflicts": [{
            "id": "conflict.one", "defaultOwner": "skill.curated.one",
            "members": ["skill.curated.one", "external:alternative"],
            "resolution": "Use the curated owner unless the external scope is explicit.",
        }],
        "recipes": [{
            "id": "recipe.one", "trigger": "A governed test is requested",
            "steps": [{"capability": "capability.one"}],
        }],
        "sources": [{"id": "local:reviewed-baseline"}],
    }


class ReferenceTests(unittest.TestCase):
    def test_missing_curated_capability_owner_is_rejected(self) -> None:
        documents = reference_fixture()
        documents["capabilities"][0]["canonicalOwner"] = "skill.curated.missing"
        with self.assertRaisesRegex(ContractError, "canonicalOwner"):
            validate_references(documents)

    def test_conflict_default_owner_must_be_a_member(self) -> None:
        documents = reference_fixture()
        documents["conflicts"][0]["defaultOwner"] = "external:not-a-member"
        with self.assertRaisesRegex(ContractError, "defaultOwner"):
            validate_references(documents)

    def test_recipe_capability_ref_must_resolve(self) -> None:
        documents = reference_fixture()
        documents["recipes"][0]["steps"][0]["capability"] = "capability.missing"
        with self.assertRaisesRegex(ContractError, "capability"):
            validate_references(documents)

    def test_duplicate_recipe_ids_are_rejected(self) -> None:
        documents = reference_fixture()
        documents["recipes"].append(deepcopy(documents["recipes"][0]))
        with self.assertRaisesRegex(ContractError, "duplicate recipe id"):
            validate_references(documents)

    def test_provides_must_be_skill_to_capability(self) -> None:
        documents = reference_fixture()
        documents["relations"][0]["from"] = "capability.one"
        with self.assertRaisesRegex(ContractError, "provides"):
            validate_references(documents)

    def test_internal_skill_source_ref_must_resolve(self) -> None:
        documents = reference_fixture()
        documents["skills"][0]["source"] = "local:missing"
        with self.assertRaisesRegex(ContractError, "source"):
            validate_references(documents)
```

Each fixture must assert the exact document and pointer in `ContractError`.

- [ ] **Step 2: Confirm RED**

Run `python -m unittest tests.test_contracts.ReferenceTests -v`.

Expected: missing semantic validator or a fixture incorrectly passes.

- [ ] **Step 3: Implement semantic validation**

Create `validate_references(documents)` that:

- builds unique Skill, capability, recipe, conflict, and source ID sets;
- rejects duplicate Skill ID, directory or canonical name;
- resolves internal `skill.*` and `capability.*` references;
- permits `external:*` and `upstream:*` only as explicit external namespaces;
- verifies curated capability owners exist;
- verifies conflict default owners are members;
- verifies recipe steps resolve to capabilities;
- verifies `provides` edges are Skill → capability;
- rejects duplicate relation triples including condition;
- verifies every Skill source resolves in `sources/lock.json`.

- [ ] **Step 4: Add the missing local source record**

Add `local:reviewed-baseline` to `sources/lock.json` with local kind, incomplete
provenance, private-only redistribution posture, and a review note pointing to
`THIRD_PARTY_NOTICES.md`. Do not invent a Git revision or license.

- [ ] **Step 5: Verify GREEN**

Run all unit tests and `python scripts/verify.py`.

Expected: all pass.

## Task 5: Manifest Supply-Chain Boundary

**Files:**
- Modify: `tests/test_contracts.py`
- Modify: `scripts/contracts.py`
- Modify: `scripts/verify.py`

- [ ] **Step 1: Write failing path and digest tests**

Use one valid entry and mutate one property per test:

```python
import hashlib
import tempfile


VALID_HASH = "a" * 64


def manifest_entry(path: str = "skills/one/SKILL.md") -> dict[str, object]:
    return {"path": path, "sha256": VALID_HASH, "size": 1}


class ManifestTests(unittest.TestCase):
    def test_manifest_rejects_parent_traversal(self) -> None:
        with self.assertRaisesRegex(ContractError, "unsafe path segment"):
            validate_manifest_entries([manifest_entry("skills/one/../two/SKILL.md")])

    def test_manifest_rejects_absolute_and_backslash_paths(self) -> None:
        for path in ("/skills/one/SKILL.md", "skills\\one\\SKILL.md"):
            with self.subTest(path=path), self.assertRaises(ContractError):
                validate_manifest_entries([manifest_entry(path)])

    def test_manifest_rejects_duplicate_and_case_colliding_paths(self) -> None:
        for paths in (
            ["skills/one/SKILL.md", "skills/one/SKILL.md"],
            ["skills/one/SKILL.md", "skills/ONE/SKILL.md"],
        ):
            with self.subTest(paths=paths), self.assertRaises(ContractError):
                validate_manifest_entries([manifest_entry(path) for path in paths])

    def test_manifest_rejects_non_lowercase_or_short_sha256(self) -> None:
        for digest in ("A" * 64, "a" * 63):
            entry = manifest_entry()
            entry["sha256"] = digest
            with self.subTest(digest=digest), self.assertRaisesRegex(ContractError, "sha256"):
                validate_manifest_entries([entry])

    def test_manifest_rejects_negative_or_boolean_size(self) -> None:
        for size in (-1, True):
            entry = manifest_entry()
            entry["size"] = size
            with self.subTest(size=size), self.assertRaisesRegex(ContractError, "size"):
                validate_manifest_entries([entry])

    def test_manifest_rejects_symlink_payload(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "skills/one").mkdir(parents=True)
            outside = root / "outside.md"
            outside.write_text("x", encoding="utf-8")
            try:
                (root / "skills/one/SKILL.md").symlink_to(outside)
            except OSError:
                self.skipTest("symlink creation is unavailable")
            with self.assertRaisesRegex(ContractError, "link"):
                validate_manifest_payload(root, [manifest_entry()])

    def test_manifest_exactly_covers_registered_skill_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "skills/one/SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text("x", encoding="utf-8")
            entry = {"path": "skills/one/SKILL.md",
                     "sha256": hashlib.sha256(b"x").hexdigest(), "size": 1}
            validate_manifest_payload(root, [entry])
```

- [ ] **Step 2: Confirm RED**

Run `python -m unittest tests.test_contracts.ManifestTests -v`.

Expected: unsafe fixtures pass or required functions are missing.

- [ ] **Step 3: Implement fail-closed manifest checks**

Use `PurePosixPath` and explicit checks:

```python
def canonical_payload_path(raw: str, document: str, pointer: str) -> PurePosixPath:
    if "\\" in raw:
        raise ContractError(document, pointer, "must use POSIX separators")
    path = PurePosixPath(raw)
    if path.is_absolute() or not path.parts or path.parts[0] != "skills":
        raise ContractError(document, pointer, "must be relative under skills/")
    if any(part in ("", ".", "..") for part in path.parts):
        raise ContractError(document, pointer, "contains an unsafe path segment")
    return path
```

Reject links/reparse points along every payload path, enforce lower-case 64-hex
SHA-256, integer non-negative sizes, exact file coverage, unique normalized
paths, and casefold uniqueness.

- [ ] **Step 4: Verify GREEN**

Run all tests and `python scripts/verify.py`.

Expected: all pass and the schema-1 manifest remains byte-compatible for the
configuration consumer.

## Task 6: Deterministic and Read-Only Generated Projections

**Files:**
- Create: `tests/test_repository_contract.py`
- Modify: `scripts/build_topology.py` only if a failing test exposes drift

- [ ] **Step 1: Write repository behavior tests**

Tests must hash all non-`.git` files and capture mtimes before and after:

```python
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def snapshot(root: Path) -> dict[str, tuple[str, int]]:
    result = {}
    for path in root.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            result[path.relative_to(root).as_posix()] = (
                hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns
            )
    return result


class RepositoryContractTests(unittest.TestCase):
    def test_build_check_is_read_only(self) -> None:
        before = snapshot(ROOT)
        subprocess.run([sys.executable, "scripts/build_topology.py", "--check"],
                       cwd=ROOT, check=True, capture_output=True, text=True)
        self.assertEqual(before, snapshot(ROOT))

    def test_emit_is_byte_deterministic(self) -> None:
        command = [sys.executable, "scripts/build_topology.py", "--emit", "topology.json"]
        first = subprocess.check_output(command, cwd=ROOT)
        second = subprocess.check_output(command, cwd=ROOT)
        self.assertEqual(first, second)

    def test_registry_change_makes_check_fail_in_temporary_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git"))
            path = copy / "registry/capabilities.json"
            document = json.loads(path.read_text(encoding="utf-8"))
            document["capabilities"].append({"id": "capability.fixture",
                                               "canonicalOwner": "external:fixture"})
            path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
            result = subprocess.run([sys.executable, "scripts/build_topology.py", "--check"],
                                    cwd=copy, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)

    def test_generated_file_change_makes_check_fail_in_temporary_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git"))
            with (copy / "generated/catalog.md").open("a", encoding="utf-8") as handle:
                handle.write("manual drift\n")
            result = subprocess.run([sys.executable, "scripts/build_topology.py", "--check"],
                                    cwd=copy, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)

    def test_topology_projection_contains_only_governed_inputs(self) -> None:
        topology = json.loads((ROOT / "generated/topology.json").read_text(encoding="utf-8"))
        self.assertEqual(set(topology), {"schema", "skills", "capabilities",
                                         "relations", "conflicts", "recipes"})
```

Use `tempfile.TemporaryDirectory` and `shutil.copytree` for mutation fixtures.
Never mutate the working repository.

- [ ] **Step 2: Run and classify RED/GREEN**

Run:

```bash
python -m unittest tests.test_repository_contract -v
```

Expected: existing deterministic behavior may already pass; any missing
read-only or input-boundary behavior must fail for the asserted reason.

- [ ] **Step 3: Make only evidence-driven generator changes**

If all behavior is already green, keep `build_topology.py` unchanged. If a test
fails, make the smallest change that restores deterministic, registry-only
generation.

- [ ] **Step 4: Verify GREEN**

Run the repository tests twice. Expected: identical clean output both times.

## Task 7: CI and Documentation Closure

**Files:**
- Modify: `.github/workflows/validate.yml`
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `docs/architecture.md`
- Modify: policies only where necessary to reflect enforced behavior

- [ ] **Step 1: Add the CI test command before repository verify**

```yaml
- name: Test governance contracts
  run: python -m unittest discover -s tests -v
- name: Verify curated Skills
  run: python scripts/verify.py
```

- [ ] **Step 2: Clarify actor boundaries and current version posture**

Document that:

- Batch A hardens schema 1 and does not publish manifest v2;
- installation and rollback remain configuration-repository responsibilities;
- curated verification has no network or live-environment effects;
- the architecture runtime sequence labels the consumer/runtime actor;
- formal v2/attestation/routing-projection work follows consumer-first ordering.

- [ ] **Step 3: Run the full acceptance suite**

```bash
python -m unittest discover -s tests -v
python scripts/build_topology.py --check
python scripts/verify.py
git diff --check
git status --short --branch
```

Expected: tests pass, generated topology is current, verification passes,
whitespace check is clean, and only intended Batch A/spec/plan files are
modified or untracked.

- [ ] **Step 4: Review and authorization checkpoint**

Present the diff, test evidence, unresolved limitations, and next-batch proposal
to the user. Do not install, commit, push, modify `codex-user-config`, or touch a
live Agent environment without a new explicit authorization covering that
action.
