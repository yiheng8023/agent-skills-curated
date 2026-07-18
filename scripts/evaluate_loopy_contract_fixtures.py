from __future__ import annotations

from typing import Any


ROUTES = {"native", "current-chain", "loopy-exact-body"}


def evaluate_route(route: str, facts: dict[str, Any]) -> str:
    if route not in ROUTES:
        return "reject-unknown-route"

    if facts["highImpact"] or facts["externalWrite"] or facts["permissionExpansion"]:
        return {
            "native": "insufficient-without-guarded-authority",
            "current-chain": "preferred-guarded-current-chain",
            "loopy-exact-body": "assist-only-cannot-grant-authority",
        }[route]

    if facts["creativeOrDivergent"]:
        return {
            "native": "preferred-open-native",
            "current-chain": "available-open-without-extra-structure",
            "loopy-exact-body": "reject-premature-loop-structure",
        }[route]

    if not facts["feedbackCanChangeNextAction"]:
        return {
            "native": "preferred-native-one-shot",
            "current-chain": "available-but-unnecessary",
            "loopy-exact-body": "reject-extra-context-for-one-shot",
        }[route]

    if not facts["observableGateAvailable"] or not facts["finiteBoundaryAvailable"]:
        return {
            "native": "stop-or-bind-missing-loop-gate",
            "current-chain": "stop-or-bind-missing-loop-gate",
            "loopy-exact-body": "stop-or-bind-missing-loop-gate",
        }[route]

    if facts["debuggingTask"] and facts["domainSpecificLoopAvailable"]:
        return {
            "native": "partial-native-debugging-baseline",
            "current-chain": "preferred-domain-diagnose-loop",
            "loopy-exact-body": "redundant-general-loop-for-debugging",
        }[route]

    return {
        "native": "eligible-low-overhead-baseline",
        "current-chain": "eligible-governed-baseline",
        "loopy-exact-body": "candidate-for-controlled-agent-trial",
    }[route]


def evaluate_fixture_document(document: dict[str, Any]) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for fixture in document["fixtures"]:
        actual = evaluate_route(fixture["route"], fixture["facts"])
        results.append(
            {
                "id": fixture["id"],
                "expected": fixture["expected"],
                "actual": actual,
            }
        )
    return results
