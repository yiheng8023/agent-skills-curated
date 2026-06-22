#!/usr/bin/env python3
"""Build deterministic catalog and topology projections from governed registries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(name: str) -> dict[str, object]:
    return json.loads((ROOT / "registry" / name).read_text(encoding="utf-8"))


def render() -> dict[str, str]:
    skills = load("skills.json")["skills"]
    capabilities = load("capabilities.json")["capabilities"]
    relations = load("relations.json")["relations"]
    conflicts = load("conflicts.json")["groups"]
    recipes = load("recipes.json")["recipes"]

    catalog = ["# Generated Skill Catalog", "", "Do not edit manually.", ""]
    for skill in sorted(skills, key=lambda item: item["id"]):
        catalog.append(
            f"- `{skill['name']}` (phase: `{skill['phase']}`, "
            f"source: `{skill['source']}`)"
        )
    catalog.append("")

    topology = {
        "schema": 1,
        "skills": skills,
        "capabilities": capabilities,
        "relations": relations,
        "conflicts": conflicts,
        "recipes": recipes,
    }

    mermaid = ["flowchart LR"]
    for relation in relations:
        left = relation["from"].replace(".", "_").replace("-", "_")
        right = relation["to"].replace(".", "_").replace("-", "_")
        mermaid.append(f"  {left} -- {relation['type']} --> {right}")
    mermaid.append("")

    routes = ["# Generated Routing Scenarios", "", "Do not edit manually.", ""]
    for recipe in recipes:
        routes.append(f"## {recipe['id']}")
        routes.append("")
        routes.append(f"Trigger: {recipe['trigger']}")
        routes.append("")
        for step in recipe["steps"]:
            suffix = f" when {step['when']}" if step.get("when") else ""
            routes.append(f"- `{step['capability']}`{suffix}")
        routes.append("")

    lifecycle = [
        "# Lifecycle Capability Coverage",
        "",
        "Do not edit manually.",
        "",
        "| Capability | Stage | Coverage | Validation | Fallback |",
        "| --- | --- | --- | --- | --- |",
    ]
    for capability in sorted(capabilities, key=lambda item: item["id"]):
        lifecycle.append(
            f"| `{capability['id']}` | `{capability['stage']}` | "
            f"`{capability['coverageState']}` | "
            f"{'<br>'.join(capability['validation'])} | "
            f"{'<br>'.join(capability['fallback'])} |"
        )
    lifecycle.append("")

    return {
        "catalog.md": "\n".join(catalog),
        "topology.json": json.dumps(topology, indent=2, sort_keys=True) + "\n",
        "topology.mmd": "\n".join(mermaid),
        "routing-scenarios.md": "\n".join(routes),
        "lifecycle-coverage.md": "\n".join(lifecycle),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--emit", choices=("catalog.md", "topology.json", "topology.mmd", "routing-scenarios.md", "lifecycle-coverage.md"))
    args = parser.parse_args()
    outputs = render()
    if args.emit:
        print(outputs[args.emit], end="")
        return 0
    if args.check:
        stale = [name for name, text in outputs.items() if not (ROOT / "generated" / name).is_file() or (ROOT / "generated" / name).read_text(encoding="utf-8") != text]
        if stale:
            raise RuntimeError("Stale generated files: " + ", ".join(stale))
        print("Generated topology is current.")
        return 0
    for name, text in outputs.items():
        target = ROOT / "generated" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    print("Generated topology updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
