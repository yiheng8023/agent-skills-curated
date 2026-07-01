#!/usr/bin/env python3
"""Discover candidate Agent Skill sources from GitHub search.

This script is read-only. It produces a candidate radar snapshot for review; it
does not modify repository state, approve sources, install Skills, star
repositories, or vendor third-party content.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
GITHUB_API = "https://api.github.com"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def request_json(path: str, token: str | None) -> dict[str, Any]:
    request = urllib.request.Request(
        f"{GITHUB_API}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "agent-skills-curated-discovery",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def safe_request(path: str, token: str | None) -> dict[str, Any] | None:
    try:
        return request_json(path, token)
    except urllib.error.HTTPError as exc:
        print(f"warning: GitHub API returned {exc.code} for {path}", file=sys.stderr)
        return None
    except urllib.error.URLError as exc:
        print(f"warning: GitHub API failed for {path}: {exc}", file=sys.stderr)
        return None


def search_repositories(query: str, limit: int, token: str | None) -> list[dict[str, Any]]:
    encoded = urllib.parse.quote(query)
    payload = safe_request(
        f"/search/repositories?q={encoded}&sort=stars&order=desc&per_page={limit}",
        token,
    )
    if not payload:
        return []
    return list(payload.get("items", []))


def count_tree_signals(repo: dict[str, Any], token: str | None) -> dict[str, Any]:
    owner = repo.get("owner", {}).get("login")
    name = repo.get("name")
    branch = repo.get("default_branch")
    if not owner or not name or not branch:
        return {"treeStatus": "missing-default-branch"}
    encoded_branch = urllib.parse.quote(str(branch), safe="")
    payload = safe_request(
        f"/repos/{owner}/{name}/git/trees/{encoded_branch}?recursive=1",
        token,
    )
    if not payload or payload.get("truncated"):
        return {"treeStatus": "unavailable-or-truncated"}
    tree = payload.get("tree", [])
    paths = [
        item.get("path", "")
        for item in tree
        if item.get("type") == "blob" and isinstance(item.get("path"), str)
    ]
    skill_paths = [path for path in paths if path.endswith("SKILL.md")]
    return {
        "treeStatus": "ok",
        "skillMdCount": len(skill_paths),
        "claudeOrAgentsMdCount": sum(
            1 for path in paths if path.endswith("CLAUDE.md") or path.endswith("AGENTS.md")
        ),
        "commandFileCount": sum(1 for path in paths if "/commands/" in f"/{path}/"),
        "agentFileCount": sum(1 for path in paths if "/agents/" in f"/{path}/"),
        "sampleSkillPaths": skill_paths[:5],
    }


def normalize_license(repo: dict[str, Any]) -> str | None:
    license_info = repo.get("license")
    if isinstance(license_info, dict):
        key = license_info.get("key")
        if isinstance(key, str) and key:
            return key.lower()
    return None


def classify(repo: dict[str, Any], detected: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    rules = profile["classificationRules"]
    policy = profile["candidatePolicy"]
    full_name = str(repo.get("full_name", ""))
    owner = full_name.split("/", 1)[0].lower() if "/" in full_name else ""
    text = " ".join(
        str(repo.get(key) or "").lower()
        for key in ["full_name", "name", "description"]
    )
    license_key = normalize_license(repo)
    archived = bool(repo.get("archived"))
    stars = int(repo.get("stargazers_count") or 0)
    skill_count = int(detected.get("skillMdCount") or 0)

    signals: list[str] = []
    risks: list[str] = []
    if stars >= int(profile["defaults"]["minimumPriorityStars"]):
        signals.append("community-signal")
    if license_key in set(rules["permissiveLicenses"]):
        signals.append("permissive-license")
    elif license_key is None:
        risks.append("missing-license")
    else:
        risks.append(f"license-review:{license_key}")
    if skill_count:
        signals.append("skill-md-present")
    if archived:
        risks.append("archived")
    if any(term in text for term in rules["riskTerms"]):
        risks.append("risk-term")

    if owner in set(rules["officialOwnerLogins"]):
        source_class = "official-external-baseline"
        disposition = policy["officialSourceDisposition"]
    elif any(term in text for term in rules["indexTerms"]):
        source_class = "index-awesome-list"
        disposition = policy["indexDisposition"]
    elif any(term in text for term in rules["toolingTerms"]):
        source_class = "agent-skill-tooling"
        disposition = policy["toolingDisposition"]
    elif skill_count:
        source_class = "third-party-skill-source"
        disposition = policy["directSkillSourceDisposition"]
    else:
        source_class = "candidate-needs-structure-confirmation"
        disposition = "candidate-needs-structure-confirmation"

    if license_key is None and source_class != "official-external-baseline":
        disposition = policy["missingLicenseDisposition"]

    return {
        "class": source_class,
        "initialDisposition": disposition,
        "signals": signals,
        "risks": risks,
    }


def discover(profile: dict[str, Any], token: str | None) -> dict[str, Any]:
    per_query_limit = int(profile["defaults"]["perQueryLimit"])
    max_tree_inspections = int(profile["defaults"]["maxTreeInspections"])
    repos: dict[str, dict[str, Any]] = {}

    for query in profile["queries"]:
        results = search_repositories(query["query"], per_query_limit, token)
        for repo in results:
            full_name = repo.get("full_name")
            if not isinstance(full_name, str):
                continue
            entry = repos.setdefault(full_name, repo)
            entry.setdefault("_queryHits", []).append(query["id"])
        time.sleep(0.25)

    ranked = sorted(
        repos.values(),
        key=lambda repo: int(repo.get("stargazers_count") or 0),
        reverse=True,
    )

    entries: list[dict[str, Any]] = []
    for index, repo in enumerate(ranked):
        detected = (
            count_tree_signals(repo, token)
            if index < max_tree_inspections
            else {"treeStatus": "not-inspected"}
        )
        classification = classify(repo, detected, profile)
        full_name = str(repo.get("full_name"))
        entries.append(
            {
                "id": f"github:{full_name}",
                "url": repo.get("html_url"),
                "description": repo.get("description"),
                "stars": repo.get("stargazers_count"),
                "updatedAt": repo.get("updated_at"),
                "pushedAt": repo.get("pushed_at"),
                "license": normalize_license(repo),
                "archived": bool(repo.get("archived")),
                "queryHits": sorted(repo.get("_queryHits", [])),
                "detected": detected,
                **classification,
            }
        )
        time.sleep(0.15)

    return {
        "schema": 1,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "profile": profile["id"],
        "nonApproval": True,
        "resultCount": len(entries),
        "queries": [query["id"] for query in profile["queries"]],
        "results": entries,
    }


def render_summary(snapshot: dict[str, Any]) -> str:
    rows = []
    for item in snapshot["results"][:25]:
        rows.append(
            "| {id} | {stars} | {class_} | {disposition} | {license} | {skills} |".format(
                id=item["id"],
                stars=item.get("stars", 0),
                class_=item.get("class", ""),
                disposition=item.get("initialDisposition", ""),
                license=item.get("license") or "unknown",
                skills=item.get("detected", {}).get("skillMdCount", "n/a"),
            )
        )
    return "\n".join(
        [
            "# GitHub Skill Discovery Snapshot",
            "",
            f"Generated: {snapshot['generatedAt']}",
            f"Profile: `{snapshot['profile']}`",
            f"Result count: {snapshot['resultCount']}",
            "",
            "This is candidate radar output only. It is not approval, release inventory, or runtime installation evidence.",
            "",
            "| Source | Stars | Class | Initial disposition | License | SKILL.md count |",
            "| --- | ---: | --- | --- | --- | ---: |",
            *rows,
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        default="registry/github-skill-discovery-profile.json",
        help="Discovery profile JSON path relative to the repository root.",
    )
    parser.add_argument("--output", required=True, help="Snapshot JSON output path.")
    parser.add_argument("--summary", help="Optional Markdown summary output path.")
    args = parser.parse_args()

    profile_path = ROOT / args.profile
    profile = load_json(profile_path)
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    snapshot = discover(profile, token)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    if args.summary:
        summary_path = Path(args.summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(render_summary(snapshot), encoding="utf-8", newline="\n")
    print(f"Discovered {snapshot['resultCount']} candidate source records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
