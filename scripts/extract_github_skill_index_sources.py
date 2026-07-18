#!/usr/bin/env python3
"""Extract reproducible GitHub source leads from a pinned public index body."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DIRECT_ADD_RE = re.compile(
    r"\bnpx\s+skills\s+add\s+([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)",
    re.IGNORECASE,
)
GITHUB_LINK_RE = re.compile(
    r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)",
    re.IGNORECASE,
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_unique(values: list[str]) -> list[str]:
    by_casefold: dict[str, str] = {}
    for value in values:
        by_casefold.setdefault(value.casefold(), value)
    return sorted(by_casefold.values(), key=str.casefold)


def extract_document(
    source_bytes: bytes,
    *,
    source_id: str,
    revision: str,
    git_blob: str,
    source_path: str,
    observed_date: str,
    broad_discovery: dict[str, Any],
) -> dict[str, Any]:
    text = source_bytes.decode("utf-8")
    direct_ids = stable_unique(
        [f"github:{match.group(1)}" for match in DIRECT_ADD_RE.finditer(text)]
    )
    github_link_ids = stable_unique(
        [f"github:{match.group(1)}" for match in GITHUB_LINK_RE.finditer(text)]
    )
    all_ids = stable_unique(direct_ids + github_link_ids)
    broad_ids = {
        str(value).casefold()
        for value in broad_discovery.get("discoveredSourceIds", [])
        if isinstance(value, str)
    }
    overlap = [value for value in direct_ids if value.casefold() in broad_ids]
    new_ids = [value for value in direct_ids if value.casefold() not in broad_ids]
    return {
        "schema": 1,
        "id": "user-starred-index-child-source-extraction-2026-07-18",
        "date": observed_date,
        "status": "verified-pinned-index-text-extraction",
        "source": {
            "sourceId": source_id,
            "revision": revision,
            "path": source_path,
            "gitBlob": git_blob,
            "bytes": len(source_bytes),
            "sha256": hashlib.sha256(source_bytes).hexdigest().upper(),
        },
        "extraction": {
            "directInstallCommand": "npx skills add owner/repository",
            "directInstallSourceCount": len(direct_ids),
            "directInstallSourceIds": direct_ids,
            "githubLinkSourceCount": len(github_link_ids),
            "githubLinkSourceIds": github_link_ids,
            "allObservedGithubSourceCount": len(all_ids),
            "allObservedGithubSourceIds": all_ids,
        },
        "comparisonToBroadDiscovery": {
            "evidence": "registry/public-skill-source-discovery-preflight-2026-07-18.json",
            "directOverlapCount": len(overlap),
            "directOverlapSourceIds": overlap,
            "newDirectSourceCount": len(new_ids),
            "newDirectSourceIds": new_ids,
        },
        "boundaries": {
            "indexRecommendationsAreReviewEvidence": False,
            "installCommandsExecuted": False,
            "childSourcesDownloaded": False,
            "childSourcesPinnedByThisExtraction": False,
            "qualitySafetyLicenseOrAdmissionProven": False,
            "discoveryLimitedToThisIndex": False,
        },
        "nextGate": "read-only metadata and immutable-revision preflight for the new direct source IDs before any child-source download or review",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--git-blob", required=True)
    parser.add_argument("--source-path", default="README.md")
    parser.add_argument("--date", required=True)
    parser.add_argument(
        "--broad-discovery",
        default="registry/public-skill-source-discovery-preflight-2026-07-18.json",
    )
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    source_file = Path(args.source_file)
    broad_path = ROOT / args.broad_discovery
    output_path = ROOT / args.output
    document = extract_document(
        source_file.read_bytes(),
        source_id=args.source_id,
        revision=args.revision,
        git_blob=args.git_blob,
        source_path=args.source_path,
        observed_date=args.date,
        broad_discovery=load_json(broad_path),
    )
    output_path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
