#!/usr/bin/env python3
"""Build the bounded Round 03 capability-survey result package."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DATE = "2026-07-18"


def load(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def coordinate_ids() -> dict[str, list[str]]:
    return {
        "STM": [f"STM-{index:02d}" for index in range(1, 27)],
        "P": [f"P{index}" for index in range(1, 25)],
        "SG": [f"SG-{index:02d}" for index in range(1, 13)],
    }


def build_matrix(demands: dict[str, Any]) -> list[dict[str, Any]]:
    by_coordinate: dict[str, list[str]] = {}
    lane_by_record: dict[str, str] = {}
    for record in demands["records"]:
        record_id = record["id"]
        lane_by_record[record_id] = record["sourceLaneId"]
        for family, ids in record["coordinateIds"].items():
            for coordinate_id in ids:
                by_coordinate.setdefault(coordinate_id, []).append(record_id)

    matrix: list[dict[str, Any]] = []
    for family, ids in coordinate_ids().items():
        for coordinate_id in ids:
            record_ids = by_coordinate.get(coordinate_id, [])
            lanes = sorted({lane_by_record[record_id] for record_id in record_ids})
            if not record_ids:
                matrix.append({
                    "family": family,
                    "coordinateId": coordinate_id,
                    "demandRecordIds": [],
                    "evidenceLaneIds": [],
                    "surveyState": "not-selected-unassessed",
                    "disposition": "retain-as-open-coordinate-not-a-gap",
                    "verificationMethod": "bind a source-supported demand record before capability comparison",
                    "limitations": "Coordinate membership alone proves neither material demand nor capability insufficiency.",
                    "recheckTrigger": "new source-supported demand evidence selects this coordinate",
                })
                continue
            if lanes == ["EL-03"]:
                disposition = "human-or-domain-authority-boundary-no-skill-substitution"
            elif "EL-04" in lanes:
                disposition = "current-governance-path-residual-gap-unproven"
            else:
                disposition = "current-native-or-composed-path-residual-gap-unproven"
            matrix.append({
                "family": family,
                "coordinateId": coordinate_id,
                "demandRecordIds": record_ids,
                "evidenceLaneIds": lanes,
                "surveyState": "selected-batch-compared-no-supported-residual-gap",
                "disposition": disposition,
                "verificationMethod": "source-bound demand, dated baseline, representative discovery, and nine-class alternative comparison",
                "limitations": "Static and local evidence does not prove cross-Agent behavior, superiority, or complete demand extraction.",
                "recheckTrigger": "paired behavior, cost, lifecycle, or contrary demand evidence changes the selected comparison",
            })
    return matrix


def main() -> int:
    demands = load("registry/round03-demand-records-batch-01.json")
    intent_binding_review = load("registry/round03-intent-binding-demand-review-2026-07-18.json")
    authority_boundary_review = load("registry/round03-authority-boundary-demand-review-2026-07-18.json")
    premise_challenge_review = load("registry/round03-premise-challenge-demand-review-2026-07-18.json")
    cognitive_monitoring_review = load("registry/round03-cognitive-offload-monitoring-demand-review-2026-07-18.json")
    demands = {
        **demands,
        "records": [
            *demands["records"],
            intent_binding_review["demandRecord"],
            authority_boundary_review["demandRecord"],
            premise_challenge_review["demandRecord"],
            cognitive_monitoring_review["demandRecord"],
        ],
    }
    alternatives = load("registry/round03-alternative-comparison-batch-01.json")
    matrix = build_matrix(demands)
    surveyed = sum(row["surveyState"].startswith("selected-batch") for row in matrix)
    unassessed = len(matrix) - surveyed

    document = {
        "schema": 1,
        "id": "round03-capability-survey-result-package-2026-07-18",
        "date": DATE,
        "status": "verified-ten-component-complete-coordinate-envelope-demand-model-open",
        "roundId": "round-03-adaptation-and-curated-admission",
        "authority": "decision-support evidence only; not adoption, execution, admission, release, runtime, Hook, cross-repository, or standards authority",
        "inputs": [
            "registry/round03-capability-survey-rebaseline.json",
            "registry/round03-demand-coordinate-source-contract.json",
            "registry/round03-demand-records-batch-01.json",
            "registry/round03-intent-binding-demand-review-2026-07-18.json",
            "registry/round03-authority-boundary-demand-review-2026-07-18.json",
            "registry/round03-premise-challenge-demand-review-2026-07-18.json",
            "registry/round03-cognitive-offload-monitoring-demand-review-2026-07-18.json",
            "registry/round03-native-runtime-baseline-2026-07-15.json",
            "registry/round03-public-discovery-snapshot-2026-07-15.json",
            "registry/round03-representative-source-review-batch-01.json",
            "registry/round03-alternative-comparison-batch-01.json",
            "registry/round03-evidence-protocol-batch-01.json",
            "registry/public-skill-source-discovery-preflight-2026-07-18.json",
            "registry/public-skill-source-static-review-batch-2026-07-18.json",
            "registry/loopy-demand-level-alternative-comparison-2026-07-18.json",
            "registry/loopy-contract-fixture-protocol-2026-07-18.json",
            "registry/loopy-disposable-agent-trial-result-2026-07-18.json",
            "registry/user-starred-skill-source-list-intake-2026-07-18.json",
            "registry/user-starred-index-child-source-extraction-2026-07-18.json",
            "registry/user-starred-index-child-source-preflight-2026-07-18.json",
            "registry/user-starred-index-stale-source-resolution-2026-07-18.json",
            "registry/pm-skills-current-revision-delta-review-2026-07-18.json"
        ],
        "scopeSummary": {
            "selectedDemandRecordCount": len(demands["records"]),
            "coordinateRowCount": len(matrix),
            "selectedBatchCoordinateCount": surveyed,
            "notSelectedUnassessedCoordinateCount": unassessed,
            "coordinateEnvelopeSelectionComplete": unassessed == 0,
            "demandExtractionComplete": False,
            "surveyClosureClaimed": False,
            "tenRequiredComponentsPresent": True
        },
        "components": [
            {
                "id": "component.01-dated-native-runtime-baseline",
                "state": "verified-dated-host-bound-baseline",
                "evidence": ["registry/round03-native-runtime-baseline-2026-07-15.json"],
                "result": "Native reasoning, visible runtime capabilities, the current three-contract chain, and host-specific surfaces are separated by date and evidence class.",
                "limitations": "Inventory and explicit-load evidence do not prove implicit activation, live health, cross-host parity, or future availability."
            },
            {
                "id": "component.02-clustered-deduplicated-candidates",
                "state": "verified-bounded-discovery-with-stale-source-handling",
                "evidence": [
                    "registry/round03-public-discovery-snapshot-2026-07-15.json",
                    "registry/public-skill-source-discovery-preflight-2026-07-18.json",
                    "registry/user-starred-index-child-source-extraction-2026-07-18.json",
                    "registry/user-starred-index-child-source-preflight-2026-07-18.json",
                    "registry/user-starred-index-stale-source-resolution-2026-07-18.json"
                ],
                "result": "Broad discovery, balanced preflight, user-starred expansion, overlap detection, suite decomposition, and stale-coordinate resolution are preserved without treating popularity or install syntax as approval.",
                "limitations": "Metadata and trees do not establish body quality, safety, license completeness, portability, or demand fit."
            },
            {
                "id": "component.03-stm-p-sg-coverage-matrix",
                "state": "complete-coordinate-envelope-selected-demand-model-open",
                "evidence": [
                    "registry/round03-demand-coordinate-source-contract.json",
                    "registry/round03-demand-records-batch-01.json",
                    "registry/round03-intent-binding-demand-review-2026-07-18.json",
                    "registry/round03-authority-boundary-demand-review-2026-07-18.json",
                    "registry/round03-premise-challenge-demand-review-2026-07-18.json",
                    "registry/round03-cognitive-offload-monitoring-demand-review-2026-07-18.json",
                    "registry/round03-alternative-comparison-batch-01.json"
                ],
                "result": f"All 62 coordinate IDs are represented and selected through eight source-supported evidence lanes; {unassessed} remain unassessed. Coordinate selection is complete, while demand-model and longitudinal evidence closure are not claimed.",
                "limitations": "The bounded coordinate envelope is structurally complete and disposition-ready, but demand extraction and future capability comparison are not exhaustive."
            },
            {
                "id": "component.04-single-composed-and-non-skill-alternatives",
                "state": "verified-for-selected-demand-batch",
                "evidence": [
                    "registry/round03-alternative-comparison-batch-01.json",
                    "registry/loopy-demand-level-alternative-comparison-2026-07-18.json",
                    "registry/loopy-contract-fixture-protocol-2026-07-18.json",
                    "registry/loopy-disposable-agent-trial-result-2026-07-18.json",
                    "registry/round03-intent-binding-demand-review-2026-07-18.json",
                    "registry/round03-authority-boundary-demand-review-2026-07-18.json",
                    "registry/round03-premise-challenge-demand-review-2026-07-18.json",
                    "registry/round03-cognitive-offload-monitoring-demand-review-2026-07-18.json"
                ],
                "result": "Nine alternative classes per initial demand, the completed three-route Loopy trial, and the bounded intent, authority, and premise reviews retain native-first, proportional composition, open divergence, runtime-enforcement, and accountable-authority boundaries.",
                "limitations": "The completed behavior and deterministic routing evidence remains host-, model-, scenario-, and source-bound."
            },
            {
                "id": "component.05-candidate-dispositions",
                "state": "verified-no-admission",
                "evidence": [
                    "registry/round03-representative-source-review-batch-01.json",
                    "registry/public-skill-source-static-review-batch-2026-07-18.json",
                    "registry/pm-skills-current-revision-delta-review-2026-07-18.json",
                    "registry/loopy-disposable-agent-trial-result-2026-07-18.json"
                ],
                "result": "Sources are split into bounded candidate-with-limits, reference, host-specific or external-tooling baseline, per-component review, stale, and hold dispositions; none is approved.",
                "limitations": "A suite disposition cannot be inherited by an unreviewed component or a newer revision."
            },
            {
                "id": "component.06-supported-and-unproven-residual-gaps",
                "state": "verified-no-supported-residual-gap-in-selected-batch",
                "evidence": ["registry/round03-alternative-comparison-batch-01.json", "registry/loopy-disposable-agent-trial-result-2026-07-18.json", "registry/round03-intent-binding-demand-review-2026-07-18.json", "registry/round03-authority-boundary-demand-review-2026-07-18.json", "registry/round03-premise-challenge-demand-review-2026-07-18.json", "registry/round03-cognitive-offload-monitoring-demand-review-2026-07-18.json"],
                "result": f"Supported residual gaps: {alternatives['batchDecision']['supportedResidualGapCount']}; unproven residual gaps: {alternatives['batchDecision']['unprovenResidualGapCount']}; EL-03 remains a human or domain-authority boundary.",
                "limitations": "Universal no-gap proof is not claimed; missing behavioral, longitudinal, production, cross-host, and future-demand evidence remains open."
            },
            {
                "id": "component.07-host-and-evidence-limitations",
                "state": "verified-claim-limits-present",
                "evidence": [
                    "registry/round03-evidence-protocol-batch-01.json",
                    "registry/round03-native-runtime-baseline-2026-07-15.json",
                    "registry/round03-authority-boundary-demand-review-2026-07-18.json"
                ],
                "result": "Host, model, reasoning, loader, activation, permission, workspace, evidence-class, date, and cross-Agent limits stay attached to behavioral claims; advisory guidance never masquerades as host enforcement or accountable authority.",
                "limitations": "Current local success cannot be generalized to other Agents, models, roots, permissions, or future versions."
            },
            {
                "id": "component.08-contract-chain-and-hook-recommendations",
                "state": "verified-proportional-chain-default-no-hook",
                "evidence": [
                    "registry/round03-alternative-comparison-batch-01.json",
                    "registry/loopy-contract-fixture-protocol-2026-07-18.json",
                    "registry/round03-authority-boundary-demand-review-2026-07-18.json"
                ],
                "result": "Use native reasoning for open or one-shot work; add intent-contract, capability-router, and closure-contract only at matching boundaries; retain human authority for consequential decisions; default to no Hook until repeated host-specific recall failure and net benefit are proven.",
                "limitations": "This is a bounded routing recommendation, not a universal mandatory chain or Hook policy."
            },
            {
                "id": "component.09-stop-recheck-update-and-next-round",
                "state": "verified-current-pass-stopped-with-bounded-next-gates",
                "evidence": [
                    "registry/public-skill-source-discovery-preflight-2026-07-18.json",
                    "registry/user-starred-index-child-source-preflight-2026-07-18.json",
                    "registry/user-starred-index-stale-source-resolution-2026-07-18.json"
                ],
                "result": "Current broad collection stops because new sources mostly enlarge known suites or domain clusters without changing the bounded Harness decision. The operating mode becomes evidence-triggered monitoring and recheck on source, license, host, demand, failure, cost, or authority drift.",
                "limitations": "The stop is marginal-yield control, not ecosystem completeness."
            },
            {
                "id": "component.10-explicit-non-authorization",
                "state": "verified-fail-closed",
                "evidence": ["registry/round03-capability-survey-rebaseline.json"],
                "result": "This package does not authorize candidate execution, download beyond reviewed read-only evidence, installation, adaptation, admission, vendoring, release, Skill or Hook authoring, runtime mutation, cross-repository write, standard promotion, commit, or push.",
                "limitations": "Any later state transition requires its own bound task, authority, verification surface, and evidence."
            }
        ],
        "coordinateMatrix": matrix,
        "followupEvidence": [
            {
                "id": "loopy-disposable-agent-trial-result-2026-07-18",
                "path": "registry/loopy-disposable-agent-trial-result-2026-07-18.json",
                "state": "verified-reference-only-not-admitted",
                "effect": "The one-time exact-body trial closed the Loopy behavior gate without proving superiority, a residual gap, or admission eligibility."
            },
            {
                "id": "round03-intent-binding-demand-review-2026-07-18",
                "path": "registry/round03-intent-binding-demand-review-2026-07-18.json",
                "state": "verified-current-path-sufficient-no-residual-gap",
                "effect": "A source-supported four-coordinate lane is now selected without requiring new external discovery or authoring."
            },
            {
                "id": "round03-authority-boundary-demand-review-2026-07-18",
                "path": "registry/round03-authority-boundary-demand-review-2026-07-18.json",
                "state": "verified-layered-current-path-sufficient-no-residual-gap",
                "effect": "A source-supported three-coordinate lane now separates advisory guidance, host runtime enforcement, and accountable authority without inferring a new Skill or Hook gap."
            },
            {
                "id": "round03-premise-challenge-demand-review-2026-07-18",
                "path": "registry/round03-premise-challenge-demand-review-2026-07-18.json",
                "state": "verified-proportional-current-path-sufficient-no-residual-gap",
                "effect": "A source-supported balanced premise lane now preserves native and open-divergent fast paths while keeping document grilling narrow and opt-in."
            },
            {
                "id": "round03-cognitive-offload-monitoring-demand-review-2026-07-18",
                "path": "registry/round03-cognitive-offload-monitoring-demand-review-2026-07-18.json",
                "state": "verified-current-classes-sufficient-longitudinal-evidence-open",
                "effect": "The final coordinate lane separates immediate assistance, longitudinal cognition, production monitoring, maintainer learning, and anti-accretion without inferring a new Skill gap."
            }
        ],
        "nextRoundCandidates": [
            {
                "candidate": "exact-pinned-loopy-controlled-agent-trial",
                "state": "executed-reference-only-not-admitted",
                "reason": "The separately authorized 12-run disposable Agent trial was correct and boundary-preserving but showed no material benefit over both native and current-chain baselines.",
                "boundary": "authorization consumed; no further candidate execution, install, persistence, publication, live configuration, Hook, or external action"
            },
            {
                "candidate": "emilkowalski/skill versus jakubkrehel/make-interfaces-feel-better",
                "state": "hold-until-design-quality-demand-is-bound",
                "reason": "Both are permissively licensed and have no detected executable or Hook surface, but the selected Harness demand batch does not currently justify a design-domain review."
            },
            {
                "candidate": "large-multi-skill-suites",
                "state": "hold-for-component-specific-demand",
                "reason": "Suite breadth, stars, and installability do not justify whole-suite review or admission; executable, license, overlap, and dependency costs vary per component."
            }
        ],
        "decision": {
            "tenComponentPackageAssembled": True,
            "selectedDemandBatchDecisionReady": True,
            "wholeCoordinateCorpusDecisionReady": True,
            "wholeDemandModelClosureClaimed": False,
            "longitudinalProductionCrossHostEvidenceOpen": True,
            "supportedResidualGapCount": 0,
            "candidateApprovedCount": 0,
            "candidateTrialAuthorizationConsumed": True,
            "loopyTrialDisposition": "reference-only-not-admitted",
            "candidateExecutionAuthorized": False,
            "repositoryAuthoredSkillOrHookEligible": False,
            "hookEligible": False,
            "hardStandardEligible": False,
            "operatingMode": "evidence-triggered-monitoring-and-recheck",
            "nextGate": "keep demand-model, longitudinal, production, and cross-host evidence limits open; require a new bound demand, repeated failure, source drift, or host change before further discovery, authoring, Hook, phase-close, or standard decisions"
        },
        "evidenceDocs": [
            "docs/round03-capability-survey-result-package-2026-07-18.md",
            "docs/round03-capability-survey-result-package-2026-07-18.zh-CN.md"
        ]
    }
    output = ROOT / "registry/round03-capability-survey-result-package-2026-07-18.json"
    output.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
