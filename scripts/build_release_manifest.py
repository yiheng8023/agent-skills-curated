#!/usr/bin/env python3
"""Build the deterministic schema-1 release manifest from approved Skill payloads."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from contracts import validate_manifest_payload
except ModuleNotFoundError:  # Imported as scripts.build_release_manifest in tests.
    from scripts.contracts import validate_manifest_payload


ROOT = Path(__file__).resolve().parent.parent


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(
    root: Path, registry: list[dict[str, object]]
) -> dict[str, object]:
    files: list[dict[str, object]] = []
    for item in sorted(registry, key=lambda value: str(value.get("directory", ""))):
        directory = item.get("directory")
        if not isinstance(directory, str):
            continue
        skill_root = root / "skills" / directory
        if skill_root.is_dir():
            for path in sorted(
                (candidate for candidate in skill_root.rglob("*") if candidate.is_file()),
                key=lambda candidate: candidate.relative_to(root).as_posix(),
            ):
                files.append(
                    {
                        "path": path.relative_to(root).as_posix(),
                        "sha256": _sha256(path),
                        "size": path.stat().st_size,
                    }
                )

    manifest: dict[str, object] = {
        "schema": 1,
        "skillCount": len(registry),
        "fileCount": len(files),
        "files": files,
    }
    validate_manifest_payload(root, manifest, registry)
    return manifest


def render_manifest(manifest: dict[str, object]) -> str:
    return json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    registry = json.loads(
        (ROOT / "registry" / "skills.json").read_text(encoding="utf-8")
    )["skills"]
    rendered = render_manifest(build_manifest(ROOT, registry))
    target = ROOT / "release-manifest.json"
    if args.check:
        if not target.is_file() or target.read_text(encoding="utf-8") != rendered:
            raise RuntimeError("release-manifest.json is stale")
        print("Release manifest is current.")
        return 0
    target.write_text(rendered, encoding="utf-8", newline="\n")
    print("Release manifest updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
