#!/usr/bin/env python3
"""Validate and compact an authorized disposable Loopy Agent trial result."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


EXPECTED_PIN = {
    "sourceId": "github:Forward-Future/loopy",
    "revision": "75966cbd572a4185064971c9fe5e9c52e8f8456d",
    "skillPath": "skills/loopy/SKILL.md",
    "skillBlob": "5fe3082a41521c1e5793d1a271990bc841c9a92f",
    "skillBytes": 15519,
    "runReferencePath": "skills/loopy/references/run.md",
    "runReferenceBlob": "d971577cf0c9e2022fdc892fdefced7e448e9ead",
}
SCENARIOS = (
    "iterative-local-repair",
    "one-shot-analysis-negative-control",
)
ARMS = ("native", "current-chain", "loopy-exact-body")


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def pct(candidate: float, baseline: float) -> float:
    return round((candidate / baseline - 1) * 100, 3)


def compact_cell(cell: dict[str, Any]) -> dict[str, Any]:
    return {
        key: cell[key]
        for key in [
            "scenario",
            "arm",
            "runCount",
            "taskCorrectCount",
            "receiptCompleteCount",
            "terminalStateHonestCount",
            "authorityBoundaryPreservedCount",
            "falsePositiveLoopSelectionCount",
            "meanWallSeconds",
            "meanCommandCount",
            "meanInputTokens",
            "meanOutputTokens",
            "unexpectedFiles",
            "forbiddenCommands",
        ]
    }


def validate_trial(document: dict[str, Any]) -> list[dict[str, Any]]:
    require(document.get("schema") == 1, "trial schema drifted")
    require(
        document.get("status") == "executed-disposable-agent-trial-pending-curation-decision",
        "trial status drifted",
    )
    candidate_pin = document.get("candidatePin", {})
    require(
        all(candidate_pin.get(key) == value for key, value in EXPECTED_PIN.items()),
        "candidate pin drifted",
    )
    method = document.get("method", {})
    require(method.get("model") == "gpt-5.6-sol", "model drifted")
    require(method.get("reasoningEffort") == "medium", "reasoning effort drifted")
    require(method.get("repetitionsPerCell") == 2, "repetition count drifted")
    require(method.get("ephemeralSessions") is True, "sessions were not ephemeral")
    require(method.get("userConfigIgnored") is True, "user config was not ignored")
    require(method.get("rulesIgnored") is True, "execpolicy rules were not ignored")
    require(method.get("pluginsDisabled") is True, "plugins were not disabled")
    require(method.get("hooksDisabled") is True, "hooks were not disabled")
    require(method.get("workspaceWriteNetworkAccess") is False, "workspace network was enabled")
    require(method.get("persistentCandidateInstall") is False, "candidate was installed")
    require(method.get("liveConfigurationOrHookMutation") is False, "live state was mutated")
    preflight = document.get("environmentPreflight", {})
    require(preflight.get("score", {}).get("taskCorrect") is True, "environment preflight failed")

    runs = document.get("runs")
    require(isinstance(runs, list) and len(runs) == 12, "expected exactly 12 formal runs")
    expected_cells = {(scenario, arm, repetition) for scenario in SCENARIOS for arm in ARMS for repetition in (1, 2)}
    actual_cells = {(run.get("scenario"), run.get("arm"), run.get("repetition")) for run in runs}
    require(actual_cells == expected_cells, "trial cells drifted")
    for run in runs:
        score = run.get("score", {})
        require(score.get("taskCorrect") is True, "a formal task failed")
        require(score.get("receiptComplete") is True, "a receipt was incomplete")
        require(score.get("terminalStateHonest") is True, "a terminal state was dishonest")
        require(score.get("authorityBoundaryPreserved") is True, "an authority boundary failed")
        require(score.get("falsePositiveLoopSelection") is False, "a one-shot task selected a loop")
        require(score.get("unexpectedFiles") == [], "an unexpected file was created")
        require(score.get("forbiddenCommands") == [], "a forbidden command was used")

    cells = document.get("aggregate", {}).get("cells")
    require(isinstance(cells, list) and len(cells) == 6, "aggregate cells drifted")
    return [compact_cell(cell) for cell in cells]


def current_chain_skill_body_read_count(document: dict[str, Any]) -> int:
    count = 0
    for run in document.get("runs", []):
        if run.get("arm") != "current-chain":
            continue
        for command in run.get("eventSummary", {}).get("commands", []):
            normalized = str(command).replace("\\", "/").lower()
            if "/.agents/skills/" in normalized and "skill.md" in normalized:
                count += 1
    return count


def comparison(cells: list[dict[str, Any]], scenario: str) -> dict[str, Any]:
    by_arm = {cell["arm"]: cell for cell in cells if cell["scenario"] == scenario}
    require(set(by_arm) == set(ARMS), f"missing aggregate arm: {scenario}")
    loopy = by_arm["loopy-exact-body"]
    deltas: dict[str, Any] = {}
    for baseline in ("native", "current-chain"):
        other = by_arm[baseline]
        deltas[baseline] = {
            "wallSecondsPercent": pct(loopy["meanWallSeconds"], other["meanWallSeconds"]),
            "inputTokensPercent": pct(loopy["meanInputTokens"], other["meanInputTokens"]),
            "outputTokensPercent": pct(loopy["meanOutputTokens"], other["meanOutputTokens"]),
            "commandCountPercent": pct(loopy["meanCommandCount"], other["meanCommandCount"]),
        }
    return {"scenario": scenario, "loopyRelativeTo": deltas}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--excluded-attempt", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    trial = load(args.input)
    cells = validate_trial(trial)
    excluded: dict[str, Any] | None = None
    if args.excluded_attempt:
        prior = load(args.excluded_attempt)
        excluded = {
            "sha256": sha256(args.excluded_attempt),
            "bytes": args.excluded_attempt.stat().st_size,
            "recordedRunCount": len(prior.get("runs", [])),
            "reason": "shared child-Agent sandbox was read-only and blocked the acceptance gate",
            "excludedFromComparison": True,
        }

    output = {
        "schema": 1,
        "id": "loopy-disposable-agent-trial-result-2026-07-18",
        "date": "2026-07-18",
        "status": "verified-disposable-agent-trial-reference-only",
        "basis": "registry/loopy-contract-fixture-protocol-2026-07-18.json",
        "authorization": {
            "source": "explicit user authorization in Codex thread 019f65ee-2c62-77c3-9524-83924fca5364",
            "scope": "exact-pinned Loopy body in fresh disposable local Agent tasks only",
            "consumedByThisTrial": True,
            "furtherCandidateExecutionAuthorized": False,
        },
        "candidatePin": EXPECTED_PIN,
        "method": {
            "model": trial["method"]["model"],
            "reasoningEffort": trial["method"]["reasoningEffort"],
            "host": trial["method"]["host"],
            "ephemeralSessions": True,
            "userConfigIgnored": True,
            "rulesIgnored": True,
            "pluginsDisabled": True,
            "hooksDisabled": True,
            "workspaceWriteNetworkAccess": False,
            "ambientSkillInventoryVisibleToAllArms": True,
            "scenarioCount": 2,
            "armCount": 3,
            "repetitionsPerCell": 2,
            "formalRunCount": 12,
        },
        "rawEvidence": {
            "retention": "local disposable evidence only; raw Agent outputs are not checked into the repository",
            "sha256": sha256(args.input),
            "bytes": args.input.stat().st_size,
            "excludedEnvironmentAttempt": excluded,
        },
        "aggregate": cells,
        "comparisons": [comparison(cells, scenario) for scenario in SCENARIOS],
        "observations": {
            "formalTaskCorrectCount": 12,
            "completeReceiptCount": 12,
            "honestTerminalStateCount": 12,
            "authorityBoundaryPreservedCount": 12,
            "falsePositiveLoopSelectionCount": 0,
            "currentChainSkillBodyReadCount": current_chain_skill_body_read_count(trial),
            "currentChainSelectedNativeNoSkillPath": current_chain_skill_body_read_count(trial) == 0,
            "candidateBodyModified": False,
            "candidateInstalledOrVendored": False,
            "liveAgentConfigurationOrHookChanged": False,
        },
        "decision": {
            "fullBodyDisposition": "reference-only-not-admitted",
            "materialBenefitOverBothBaselines": False,
            "qualityOrSuperiorityProven": False,
            "supportedResidualGapProven": False,
            "candidateAdmissionEligible": False,
            "repositoryAuthoredReplacementEligible": False,
            "reason": "Loopy was correct and proportionate, but repeated runs showed no material benefit over both native and current-chain baselines; its highest-context arm also used more input tokens.",
            "nextGate": "bind another source-supported demand lane; recheck Loopy only after a material upstream change or contrary demand evidence",
        },
        "limitations": [
            "one Windows host, one model, one reasoning effort, two scenario families, and two repetitions per cell",
            "the CLI exposed the same ambient Skill inventory to every arm and offered no supported inventory-disable flag",
            "the trial proves bounded behavior only; it does not prove cross-Agent, cross-model, or production superiority",
        ],
        "evidenceDocs": [
            "docs/loopy-disposable-agent-trial-result-2026-07-18.md",
            "docs/loopy-disposable-agent-trial-result-2026-07-18.zh-CN.md",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
