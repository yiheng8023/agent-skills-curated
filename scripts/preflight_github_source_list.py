#!/usr/bin/env python3
"""Pin and structurally preflight GitHub sources from a reviewed source list."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
EXECUTABLE_SUFFIXES = {
    ".bat", ".cmd", ".go", ".js", ".mjs", ".cjs", ".ps1", ".py",
    ".rb", ".rs", ".sh", ".ts", ".tsx",
}
ROOT_LICENSE_RE = re.compile(r"^(LICENSE|LICENCE|COPYING)(\.|$)", re.IGNORECASE)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def gh_json(path: str) -> dict[str, Any]:
    completed = subprocess.run(
        ["gh", "api", path],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(completed.stdout)


def is_agent_hook(path: str) -> bool:
    lowered = path.lower()
    return (
        lowered.startswith((
            ".agents/hooks/", ".claude/hooks/", ".codex/hooks/",
            ".continue/hooks/", ".cursor/hooks/", "hooks/",
        ))
        or "/.agents/hooks/" in f"/{lowered}"
        or "/.claude/hooks/" in f"/{lowered}"
        or "/.codex/hooks/" in f"/{lowered}"
        or "/.continue/hooks/" in f"/{lowered}"
        or "/.cursor/hooks/" in f"/{lowered}"
        or Path(path).name.lower() == "hooks.json"
    )


def preflight(source_id: str) -> dict[str, Any]:
    if not source_id.startswith("github:") or source_id.count("/") != 1:
        raise ValueError(f"invalid GitHub source id: {source_id}")
    full_name = source_id.removeprefix("github:")
    repo = gh_json(f"repos/{full_name}")
    branch = repo["default_branch"]
    commit = gh_json(f"repos/{full_name}/commits/{branch}")
    revision = commit["sha"]
    tree_sha = commit["commit"]["tree"]["sha"]
    tree_doc = gh_json(f"repos/{full_name}/git/trees/{tree_sha}?recursive=1")
    if tree_doc.get("truncated"):
        return {
            "sourceId": source_id,
            "revision": revision,
            "treeSha": tree_sha,
            "treeStatus": "truncated",
            "defaultBranch": branch,
        }
    paths = [
        item["path"]
        for item in tree_doc.get("tree", [])
        if item.get("type") == "blob" and isinstance(item.get("path"), str)
    ]
    skill_paths = [path for path in paths if path.lower().endswith("skill.md")]
    hook_paths = [path for path in paths if is_agent_hook(path)]
    executable_paths = [
        path for path in paths if Path(path).suffix.lower() in EXECUTABLE_SUFFIXES
    ]
    root_license_paths = [path for path in paths if "/" not in path and ROOT_LICENSE_RE.match(path)]
    license_info = repo.get("license") or {}
    license_key = license_info.get("spdx_id") or license_info.get("key")
    if license_key and root_license_paths:
        license_state = "metadata-and-root-artifact-present"
    elif license_key:
        license_state = "metadata-only"
    elif root_license_paths:
        license_state = "root-artifact-needs-content-review"
    else:
        license_state = "missing-at-preflight"
    if len(skill_paths) > 1:
        source_shape = "multi-skill-suite"
    elif skill_paths:
        source_shape = "single-skill-source"
    else:
        source_shape = "no-skill-md-detected"
    return {
        "sourceId": source_id,
        "url": repo["html_url"],
        "description": repo.get("description"),
        "defaultBranch": branch,
        "revision": revision,
        "revisionCommittedAt": commit["commit"]["committer"]["date"],
        "treeSha": tree_sha,
        "treeStatus": "ok",
        "archived": bool(repo.get("archived")),
        "fork": bool(repo.get("fork")),
        "pushedAt": repo.get("pushed_at"),
        "starsWeakSignal": int(repo.get("stargazers_count") or 0),
        "licenseMetadata": license_key,
        "rootLicensePaths": root_license_paths,
        "licensePreflightState": license_state,
        "fileCount": len(paths),
        "skillMdCount": len(skill_paths),
        "sourceShape": source_shape,
        "componentSelectionReviewRequired": len(skill_paths) > 1,
        "agentHookFileCount": len(hook_paths),
        "independentHookReviewRequired": bool(hook_paths),
        "executableFileCount": len(executable_paths),
        "executableSurfaceReviewRequired": bool(executable_paths),
        "pluginManifestCount": sum(
            Path(path).name.lower() in {"plugin.json", "marketplace.json", "mcp.json"}
            for path in paths
        ),
        "claudeOrAgentsMdCount": sum(
            Path(path).name.lower() in {"claude.md", "agents.md"}
            for path in paths
        ),
        "sampleSkillPaths": skill_paths[:5],
        "sampleAgentHookPaths": hook_paths[:5],
        "sampleExecutablePaths": executable_paths[:5],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--source-field", default="comparisonToBroadDiscovery.newDirectSourceIds")
    parser.add_argument("--id", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    source_doc = load_json(ROOT / args.input)
    value: Any = source_doc
    for segment in args.source_field.split("."):
        value = value[segment]
    if not isinstance(value, list) or not value:
        raise ValueError("source field must resolve to a non-empty list")
    source_ids = [str(item) for item in value]
    sources: list[dict[str, Any]] = []
    for source_id in source_ids:
        try:
            sources.append(preflight(source_id))
        except subprocess.CalledProcessError as exc:
            detail = (exc.stderr or "").strip()
            if "HTTP 404" in detail or '"status":404' in detail or '"status": 404' in detail:
                error_class = "github-api-not-found"
            else:
                error_class = "github-api-error"
            sources.append(
                {
                    "sourceId": source_id,
                    "treeStatus": "unavailable",
                    "preflightError": error_class,
                    "errorDetail": detail.splitlines()[-1] if detail else f"exit-{exc.returncode}",
                }
            )
    document = {
        "schema": 1,
        "id": args.id,
        "date": args.date,
        "status": "verified-read-only-source-pinned-structure-preflight",
        "inputEvidence": args.input.replace("\\", "/"),
        "inputField": args.source_field,
        "sourceCount": len(sources),
        "sources": sources,
        "summary": {
            "treeOkCount": sum(item.get("treeStatus") == "ok" for item in sources),
            "treeUnavailableCount": sum(item.get("treeStatus") != "ok" for item in sources),
            "singleSkillSourceCount": sum(item.get("sourceShape") == "single-skill-source" for item in sources),
            "multiSkillSuiteCount": sum(item.get("sourceShape") == "multi-skill-suite" for item in sources),
            "noSkillMdCount": sum(item.get("sourceShape") == "no-skill-md-detected" for item in sources),
            "licenseArtifactOrMetadataPresentAmongAvailableCount": sum(
                item.get("treeStatus") == "ok"
                and item.get("licensePreflightState") != "missing-at-preflight"
                for item in sources
            ),
            "licenseMissingAmongAvailableCount": sum(
                item.get("treeStatus") == "ok"
                and item.get("licensePreflightState") == "missing-at-preflight"
                for item in sources
            ),
            "licenseUnknownBecauseUnavailableCount": sum(
                item.get("treeStatus") != "ok" for item in sources
            ),
            "agentHookSurfaceCount": sum(bool(item.get("agentHookFileCount")) for item in sources),
            "executableSurfaceCount": sum(bool(item.get("executableFileCount")) for item in sources),
        },
        "boundaries": {
            "metadataAndTreeOnly": True,
            "sourceBodyDownloaded": False,
            "candidateCodeExecuted": False,
            "installCommandExecuted": False,
            "agentOrHookMutated": False,
            "qualitySafetyLicenseFitnessOrAdmissionProven": False,
            "starsUsedAsApproval": False,
        },
        "nextGate": "classify ownership and source shape, deduplicate official or runtime baselines, then select the smallest demand-linked static review batch",
    }
    (ROOT / args.output).write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
