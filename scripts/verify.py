#!/usr/bin/env python3
"""Verify inventory, provenance, overlap decisions, graph, and portability."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADDY_APPROVED = {
    "ci-cd-and-automation",
    "deprecation-and-migration",
    "observability-and-instrumentation",
    "performance-optimization",
    "shipping-and-launch",
}
FORBIDDEN_APPROVED_TEXT = (
    "using-agent-skills",
    "Chrome DevTools MCP",
    "git reset --hard",
    "Agent fixes → pushes",
    "/mnt/skills/",
    ".claude/",
)


def load(path: str) -> dict[str, object]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise RuntimeError("Missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise RuntimeError("Unclosed YAML frontmatter")
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if re.match(r"^[A-Za-z][A-Za-z0-9_-]*:\s*", line):
            key, value = line.split(":", 1)
            values[key] = value.strip()
    return values


def verify() -> None:
    required = (
        "AGENTS.md", "README.md", "README.zh-CN.md", "THIRD_PARTY_NOTICES.md",
        "sources/lock.json", "sources/addyosmani-agent-skills/selection.json",
        "sources/addyosmani-agent-skills/LICENSE",
        "sources/addyosmani-agent-skills/files.sha256", "registry/skills.json",
        "registry/capabilities.json", "registry/relations.json",
        "registry/conflicts.json", "registry/recipes.json",
        "policies/intake.md", "policies/portability.md", "policies/security.md",
        "policies/overlap-resolution.md", "policies/lifecycle.md",
        "scripts/build_topology.py", "scripts/verify.py", "release-manifest.json",
        "audits/addyosmani-agent-skills/17214a29c429a19f7a9607f2c06f9d650ea87eb0/security.md",
        "audits/addyosmani-agent-skills/17214a29c429a19f7a9607f2c06f9d650ea87eb0/overlap.md",
        "audits/addyosmani-agent-skills/17214a29c429a19f7a9607f2c06f9d650ea87eb0/portability.md",
    )
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        raise RuntimeError("Missing required files: " + ", ".join(missing))

    registry = load("registry/skills.json")["skills"]
    directories = sorted(path.name for path in (ROOT / "skills").iterdir() if path.is_dir())
    registered = sorted(item["directory"] for item in registry)
    if directories != registered:
        raise RuntimeError("Skill registry does not match installed directories.")
    if len(directories) != 34:
        raise RuntimeError(f"Expected 34 curated Skills, found {len(directories)}.")

    manifest = load("release-manifest.json")
    if manifest.get("skillCount") != 34 or manifest.get("fileCount") != 60:
        raise RuntimeError("Unexpected release manifest inventory.")
    manifest_paths = {item["path"] for item in manifest["files"]}
    actual_paths = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "skills").rglob("*")
        if path.is_file()
    }
    if manifest_paths != actual_paths:
        raise RuntimeError("Release manifest does not match Skill files.")
    for item in manifest["files"]:
        data = (ROOT / item["path"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != item["sha256"] or len(data) != item["size"]:
            raise RuntimeError(f"Release manifest hash mismatch: {item['path']}")

    ids = [item["id"] for item in registry]
    if len(ids) != len(set(ids)):
        raise RuntimeError("Skill IDs are not unique.")
    for item in registry:
        path = ROOT / "skills" / item["directory"] / "SKILL.md"
        if not path.is_file():
            raise RuntimeError(f"Missing {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        meta = frontmatter(text)
        if meta.get("name") != item["name"] or meta.get("description") != item["description"]:
            raise RuntimeError(f"Registry/frontmatter drift: {item['directory']}")
        if item["directory"] in ADDY_APPROVED:
            if not meta["description"].startswith("Use when"):
                raise RuntimeError(f"Non-trigger description: {item['directory']}")
            for forbidden in FORBIDDEN_APPROVED_TEXT:
                if forbidden.lower() in text.lower():
                    raise RuntimeError(f"Agent-specific or unsafe text in {item['directory']}: {forbidden}")
            for reference in re.findall(r"`(references/[^`]+)`", text):
                if not (path.parent / reference).is_file():
                    raise RuntimeError(f"Dead adopted-Skill reference in {item['directory']}: {reference}")

    selection = load("sources/addyosmani-agent-skills/selection.json")["decisions"]
    if len(selection) != 24 or {name for name, decision in selection.items() if decision == "adopt"} != ADDY_APPROVED:
        raise RuntimeError("Upstream selection must close all 24 Skills and adopt exactly five.")

    capabilities = load("registry/capabilities.json")["capabilities"]
    capability_ids = {item["id"] for item in capabilities}
    skill_ids = set(ids)
    relations_doc = load("registry/relations.json")
    allowed = set(relations_doc["relationTypes"])
    nodes = capability_ids | skill_ids
    for relation in relations_doc["relations"]:
        if relation["type"] not in allowed or relation["from"] not in nodes or relation["to"] not in nodes:
            raise RuntimeError(f"Invalid relationship: {relation}")

    conflicts = load("registry/conflicts.json")["groups"]
    if not conflicts or any(not group.get("defaultOwner") or not group.get("resolution") for group in conflicts):
        raise RuntimeError("Every conflict group needs a default owner and resolution.")

    subprocess.run([sys.executable, str(ROOT / "scripts/build_topology.py"), "--check"], check=True)


def main() -> int:
    verify()
    print("Agent Skills Curated validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
