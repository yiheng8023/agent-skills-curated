from __future__ import annotations

from typing import Any


def evaluate_transition(facts: dict[str, Any]) -> str:
    if not facts["repositoryBound"]:
        return "ask-for-repository-locator"
    if not facts["sourceFresh"]:
        return "reject-stale-carrier"
    if facts["authorityTransferRequired"] and not facts["authorityTransferConfirmed"]:
        return "require-human-confirmation"
    if facts["changeCount"] == 0 and facts["verificationPassed"]:
        return "honest-no-delta-exit"
    if facts["snapshotCurrent"] and facts["handoffEvidenceComplete"]:
        return "resume-from-repository-truth"
    return "needs-more-evidence"


def evaluate_routing(facts: dict[str, Any]) -> str:
    if not facts["liveRootStateKnown"]:
        return "fail-closed-live-state-unknown"
    if facts["highRisk"] or facts["permissionExpansion"]:
        return "require-human-confirmation"
    if facts["nativeEquivalentHealthy"]:
        return "prefer-native"
    if facts["sameName"] and facts["sameDigest"]:
        return "deduplicate-identical-body"
    if facts["sameName"] and not facts["sameDigest"]:
        return "record-explicit-conflict"
    return "route-through-canonical-router"


def evaluate_projection(facts: dict[str, Any]) -> str:
    edge = facts["edgeType"]
    if edge == "candidate-to-runtime":
        return "block-direct-execution"
    if edge == "candidate-to-curated":
        required = ["sourcePinned", "licenseReviewed", "securityReviewed", "ownerApproved"]
        return "allow-curated-admission-review" if all(facts[key] for key in required) else "block-incomplete-admission"
    if edge == "curated-to-consumer":
        return "allow-consumer-readiness-review" if facts["releasePinned"] and facts["consumerVerificationBound"] else "block-unverified-projection"
    if edge == "research-to-calibration":
        return "allow-candidate-custody-handoff" if facts["evidencePackageComplete"] else "block-incomplete-evidence-package"
    if edge == "calibration-to-assets":
        return "allow-project-admission-review" if facts["separateProjectAuthorityBound"] else "block-missing-project-authority"
    return "block-unknown-edge"


EVALUATORS = {
    "EL-01": evaluate_transition,
    "EL-02": evaluate_routing,
    "EL-04": evaluate_projection,
}


def evaluate_fixture_document(document: dict[str, Any]) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for fixture in document["fixtures"]:
        actual = EVALUATORS[fixture["lane"]](fixture["facts"])
        results.append({"id": fixture["id"], "expected": fixture["expected"], "actual": actual})
    return results
