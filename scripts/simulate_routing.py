#!/usr/bin/env python3
"""Deterministically simulate routing policy from normalized structured facts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DECISIONS = {"native", "runtime", "curated", "recipe", "no-skill", "ask-user", "gap"}


def _load(root: Path, relative: str) -> dict[str, object]:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def load_model(root: Path) -> dict[str, object]:
    capabilities = _load(root, "registry/capabilities.json")["capabilities"]
    routes = _load(root, "registry/routing.json")["routes"]
    recipes = _load(root, "registry/recipes.json")["recipes"]
    return {
        "capabilities": {item["id"]: item for item in capabilities},
        "routes": routes,
        "recipes": {item["id"]: item for item in recipes},
    }


def _result(
    decision: str,
    selected: list[str],
    capabilities: list[dict[str, object]],
    reason: str = "",
) -> dict[str, object]:
    return {
        "decision": decision,
        "selectedIds": selected,
        "exclusions": [],
        "confirmationReason": reason,
        "validation": [
            statement
            for capability in capabilities
            for statement in capability.get("validation", [])
        ],
        "fallback": [
            statement
            for capability in capabilities
            for statement in capability.get("fallback", [])
        ],
    }


def resolve(facts: dict[str, object], model: dict[str, object]) -> dict[str, object]:
    requested = facts["requestedCapabilities"]
    capability_map = model["capabilities"]
    capabilities = [capability_map[item] for item in requested]

    boundary_reasons = []
    if facts.get("risk") in {"high", "critical"}:
        boundary_reasons.append("high-risk action")
    if facts.get("cost") == "meaningful":
        boundary_reasons.append("meaningful cost")
    for field, label in (
        ("permissionExpansion", "permission expansion"),
        ("unresolvedConflict", "unresolved conflict"),
        ("ambiguous", "ambiguous intent"),
    ):
        if facts.get(field):
            boundary_reasons.append(label)
    if any(item["coverageState"] == "human-authority" for item in capabilities):
        boundary_reasons.append("human authority required")
    if boundary_reasons:
        return _result("ask-user", [], capabilities, "; ".join(boundary_reasons))

    if facts.get("negativeMatch"):
        return _result("no-skill", [], capabilities)
    if not facts.get("contextSatisfied"):
        return _result("gap", [], capabilities)

    available = set(facts.get("available", []))
    if facts.get("nativeEquivalent") and "native" in available:
        return _result("native", [], capabilities)
    if facts.get("runtimeEquivalent") and "runtime" in available:
        return _result("runtime", [], capabilities)

    if len(capabilities) == 1:
        capability = capabilities[0]
        capability_id = capability["id"]
        state = capability["coverageState"]
        if state == "native-sufficient" and "native" in available:
            return _result("native", [], capabilities)
        if state == "runtime-resolved" and "runtime" in available:
            return _result("runtime", [], capabilities)
        if state == "recipe":
            recipe_id = f"recipe.{capability_id.removeprefix('capability.')}"
            if recipe_id in model["recipes"]:
                return _result("recipe", [recipe_id], capabilities)
        if state == "curated" and "curated" in available:
            return _result(
                "curated", sorted(capability.get("curatedOwners", [])), capabilities
            )
        if state == "gap":
            return _result("gap", [], capabilities)

    if all(item["coverageState"] == "native-sufficient" for item in capabilities) and "native" in available:
        return _result("native", [], capabilities)
    return _result("gap", [], capabilities)


def run_scenarios(root: Path) -> dict[str, object]:
    document = _load(root, "registry/scenarios.json")
    model = load_model(root)
    failures = []
    covered = set()
    for scenario in document["scenarios"]:
        facts = dict(scenario["routingFacts"])
        facts["requestedCapabilities"] = scenario["requestedCapabilities"]
        result = resolve(facts, model)
        covered.update(scenario["requestedCapabilities"])
        if result["decision"] != scenario["expectedDecision"] or result["selectedIds"] != scenario["expectedSkills"]:
            failures.append({
                "id": scenario["id"],
                "expectedDecision": scenario["expectedDecision"],
                "actualDecision": result["decision"],
                "expectedSkills": scenario["expectedSkills"],
                "actualSelectedIds": result["selectedIds"],
            })
    lifecycle = set(model["capabilities"])
    return {
        "schema": 1,
        "scenarioCount": len(document["scenarios"]),
        "passed": len(document["scenarios"]) - len(failures),
        "failed": len(failures),
        "unclassifiedLifecycleCapabilities": sorted(lifecycle - covered),
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--report")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    report = run_scenarios(root)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        (root / args.report).write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 1 if report["failed"] or report["unclassifiedLifecycleCapabilities"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
