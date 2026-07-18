#!/usr/bin/env python3
"""Evaluate deterministic lifecycle-metabolism policy fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path


SIGNAL_CLASSES = {
    "consumer-feedback",
    "community-feedback",
    "security-finding",
    "license-or-provenance-change",
    "upstream-refresh",
    "validation-failure-or-change",
}
RELEASE_DISPOSITIONS = {"replace-or-supersede", "deprecate", "retire"}
REQUIRED_RELEASE_SAFEGUARDS = {
    "impactAnalysis",
    "relationshipAnalysis",
    "migrationPlan",
    "rollbackPlan",
    "versionedDecision",
    "releaseAuthority",
    "consumerAuthority",
    "verification",
}


def evaluate_case(case: dict[str, object]) -> dict[str, object]:
    case_id = case.get("id")
    signal_class = case.get("signalClass")
    disposition = case.get("proposedDisposition")
    safeguards = case.get("safeguards")
    if signal_class not in SIGNAL_CLASSES:
        return {"id": case_id, "decision": "reject", "reasonCode": "unknown-signal-class"}
    if not isinstance(safeguards, dict):
        return {"id": case_id, "decision": "reject", "reasonCode": "safeguards-required"}
    if case.get("feedbackAutomaticallyApprovesCandidate") is True:
        return {"id": case_id, "decision": "reject", "reasonCode": "feedback-cannot-approve"}
    if signal_class == "upstream-refresh" and case.get("automaticUpstreamReplacement") is True:
        return {"id": case_id, "decision": "reject", "reasonCode": "immutable-intake-required"}
    if disposition in RELEASE_DISPOSITIONS:
        if case.get("releaseMutationProposed") is not True:
            return {"id": case_id, "decision": "reject", "reasonCode": "release-mutation-must-be-explicit"}
        missing = sorted(
            key for key in REQUIRED_RELEASE_SAFEGUARDS
            if safeguards.get(key) is not True
        )
        if missing:
            return {
                "id": case_id,
                "decision": "reject",
                "reasonCode": "release-safeguards-incomplete",
                "missing": missing,
            }
    if disposition == "retire":
        if case.get("currentState") != "deprecated":
            return {"id": case_id, "decision": "reject", "reasonCode": "retirement-requires-deprecated-state"}
        if safeguards.get("migrationVerified") is not True or safeguards.get("rollbackVerified") is not True:
            return {"id": case_id, "decision": "reject", "reasonCode": "retirement-verification-incomplete"}
    if disposition == "rollback":
        required = {
            "validationFailed",
            "rollbackPlan",
            "rollbackVerified",
            "lastKnownGoodPreserved",
            "consumerAuthority",
        }
        if any(safeguards.get(key) is not True for key in required):
            return {"id": case_id, "decision": "reject", "reasonCode": "rollback-proof-incomplete"}
    if not case.get("affectedStableIds") or not case.get("signalDate") or not case.get("recheckTrigger"):
        return {"id": case_id, "decision": "reject", "reasonCode": "decision-record-incomplete"}
    return {"id": case_id, "decision": "accept", "reasonCode": "policy-satisfied"}


def evaluate_fixture_document(document: dict[str, object]) -> list[dict[str, object]]:
    cases = document.get("cases")
    if not isinstance(cases, list):
        raise ValueError("Lifecycle fixture cases must be a list.")
    return [evaluate_case(case) for case in cases if isinstance(case, dict)]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: evaluate_lifecycle_metabolism_fixtures.py <fixture.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    document = json.loads(path.read_text(encoding="utf-8"))
    results = evaluate_fixture_document(document)
    print(json.dumps(results, indent=2))
    expected = {
        item.get("id"): item.get("expected")
        for item in document.get("cases", [])
        if isinstance(item, dict)
    }
    return 0 if all(
        result.get("decision") == expected.get(result.get("id"), {}).get("decision")
        and result.get("reasonCode") == expected.get(result.get("id"), {}).get("reasonCode")
        for result in results
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
