#!/usr/bin/env python3
"""Verify inventory, provenance, overlap decisions, graph, and portability."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

from contracts import (
    ContractError,
    parse_frontmatter,
    validate_admissions_document,
    validate_adopted_selection,
    validate_capabilities_document,
    validate_conflicts_document,
    validate_inventory_counts,
    validate_lifecycle_coverage,
    validate_manifest_payload,
    validate_recipes_document,
    validate_references,
    validate_relations_document,
    validate_release_manifest_document,
    validate_routing_document,
    validate_scenarios_document,
    validate_selection_document,
    validate_skills_document,
    validate_source_selection,
    validate_sources_lock_document,
)
from simulate_routing import run_scenarios

ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_SOURCE_ID = "github:addyosmani/agent-skills"
ALLOWED_SELECTION_DISPOSITIONS = {
    "adopt",
    "merge",
    "adapter-only",
    "recipe-only",
    "reject",
}
FORBIDDEN_APPROVED_TEXT = (
    "using-agent-skills",
    "Chrome DevTools MCP",
    "git reset --hard",
    "Agent fixes → pushes",
    "/mnt/skills/",
    ".claude/",
)
REQUIRED_FILES = (
    ".github/workflows/discover-candidate-sources.yml",
    "AGENTS.md", "README.md", "README.zh-CN.md", "THIRD_PARTY_NOTICES.md",
    "sources/lock.json", "sources/addyosmani-agent-skills/selection.json",
    "sources/addyosmani-agent-skills/LICENSE",
    "sources/addyosmani-agent-skills/files.sha256", "registry/skills.json",
    "registry/capabilities.json", "registry/relations.json",
    "registry/conflicts.json", "registry/recipes.json",
    "registry/collaboration-domain-coverage.json",
    "registry/curation-expansion-rounds.json",
    "registry/curation-program-plan.json",
    "registry/program-acceptance-map.json",
    "registry/round-lifecycle-contract.json",
    "registry/radar-feedback.json",
    "registry/github-skill-discovery-profile.json",
    "registry/starred-skill-sources.json",
    "registry/source-intake-batches.json",
    "registry/round02-candidate-reviews.json",
    "registry/round02-obsidian-adaptation-gate.json",
    "registry/round02-pm-execution-adaptation-gate.json",
    "registry/round02-pm-analytics-adaptation-gate.json",
    "registry/round02-pm-market-discovery-adaptation-gate.json",
    "registry/round02-pm-toolkit-boundary-adaptation-gate.json",
    "registry/round02-huashu-design-guidance-adaptation-gate.json",
    "registry/round02-huashu-toolchain-media-adaptation-gate.json",
    "registry/round02-release-readiness-review.json",
    "registry/round02-release-admission-review-template.json",
    "registry/round02-release-admission-approval-request.json",
    "registry/round02-release-admission-approval-events.json",
    "registry/round02-release-admission-candidate-review.json",
    "registry/round02-approved-payload-routing-proposal-template.json",
    "registry/round02-release-execution-approval-request.json",
    "registry/round02-approved-payload-routing-approval-events.json",
    "registry/round02-approved-payload-routing-proposal.json",
    "registry/mvp-candidate-batches.json",
    "registry/mvp-candidate-reviews.json",
    "registry/mvp-transition-gates.json",
    "registry/mvp-adaptation-review-checklist.json",
    "registry/mvp-approval-requests.json",
    "registry/mvp02-preflight-readiness.json",
    "registry/mvp02-post-approval-execution-plan.json",
    "registry/mvp02-approval-events.json",
    "registry/mvp02-adapted-drafts.json",
    "registry/mvp03-release-or-routing-preflight.json",
    "registry/mvp03-release-or-routing-review-template.json",
    "registry/mvp03-release-or-routing-approval-request.json",
    "registry/mvp03-approval-events.json",
    "registry/mvp03-release-or-routing-candidate-review.json",
    "registry/mvp03-release-routing-execution.json",
    "registry/mvp06-lifecycle-feedback.json",
    "registry/admissions.json", "registry/routing.json", "registry/scenarios.json",
    "policies/intake.md", "policies/portability.md", "policies/security.md",
    "policies/overlap-resolution.md", "policies/lifecycle.md",
    "scripts/discover_github_skill_sources.py",
    "scripts/build_topology.py", "scripts/build_release_manifest.py",
    "scripts/verify.py", "scripts/simulate_routing.py", "release-manifest.json",
    "generated/routing-index.json", "generated/routing-simulation-report.json",
    "schemas/v1/skills.schema.json", "schemas/v1/capabilities.schema.json",
    "schemas/v1/relations.schema.json", "schemas/v1/conflicts.schema.json",
    "schemas/v1/recipes.schema.json", "schemas/v1/sources-lock.schema.json",
    "schemas/v1/selection.schema.json", "schemas/v1/release-manifest.schema.json",
    "schemas/v1/admissions.schema.json", "schemas/v1/routing.schema.json",
    "schemas/v1/scenarios.schema.json",
    "schemas/v2/capabilities.schema.json",
    "audits/addyosmani-agent-skills/17214a29c429a19f7a9607f2c06f9d650ea87eb0/security.md",
    "audits/addyosmani-agent-skills/17214a29c429a19f7a9607f2c06f9d650ea87eb0/overlap.md",
    "audits/addyosmani-agent-skills/17214a29c429a19f7a9607f2c06f9d650ea87eb0/portability.md",
    "sources/mattpocock-skills/LICENSE",
    "audits/mattpocock-skills/6eeb81b5fcfeeb5bd531dd47ab2f9f2bbea27461/security.md",
    "audits/mattpocock-skills/6eeb81b5fcfeeb5bd531dd47ab2f9f2bbea27461/overlap.md",
    "audits/mattpocock-skills/6eeb81b5fcfeeb5bd531dd47ab2f9f2bbea27461/portability.md",
    "sources/kepano-obsidian-skills/LICENSE",
    "docs/coverage-and-curation-expansion.md",
    "docs/curation-harness-model.md",
    "docs/round02-source-intake-2026-07-02.md",
    "docs/round02-candidate-review-2026-07-02.md",
    "docs/round02-obsidian-adaptation-gate.md",
    "docs/round02-pm-execution-adaptation-gate.md",
    "docs/round02-pm-analytics-adaptation-gate.md",
    "docs/round02-pm-market-discovery-adaptation-gate.md",
    "docs/round02-pm-toolkit-boundary-adaptation-gate.md",
    "docs/round02-huashu-design-guidance-adaptation-gate.md",
    "docs/round02-huashu-toolchain-media-adaptation-gate.md",
    "docs/round02-release-readiness-review.md",
    "docs/round02-release-admission-review-template.md",
    "docs/round02-release-admission-approval-request.md",
    "docs/round02-release-admission-candidate-review.md",
    "docs/round02-approved-payload-routing-proposal-template.md",
    "docs/round02-release-execution-approval-request.md",
    "docs/round02-approved-payload-routing-proposal.md",
    "docs/mvp-candidate-batch-2026-06-27.md",
    "docs/mvp-candidate-review-2026-06-27.md",
    "docs/mvp02-adaptation-transition-gate.md",
    "docs/mvp02-adaptation-review-template.md",
    "docs/mvp02-adaptation-approval-request.md",
    "docs/mvp02-preflight-readiness.md",
    "docs/mvp02-post-approval-execution-plan.md",
    "docs/mvp02-adapted-draft-review.md",
    "docs/mvp03-release-or-routing-preflight.md",
    "docs/mvp03-release-or-routing-review-template.md",
    "docs/mvp03-release-or-routing-approval-request.md",
    "docs/mvp03-release-or-routing-candidate-review.md",
    "docs/mvp03-release-routing-execution.md",
    "docs/mvp06-lifecycle-feedback.md",
    "drafts/round02-obsidian-adaptation/open-format-knowledge-files/DRAFT.md",
    "drafts/round02-obsidian-adaptation/obsidian-cli-runtime-adapter/DRAFT.md",
    "drafts/round02-obsidian-adaptation/defuddle-tool-adapter/DRAFT.md",
    "drafts/round02-pm-execution-adaptation/ai-shipping-governance/DRAFT.md",
    "drafts/round02-pm-execution-adaptation/product-execution-documents/DRAFT.md",
    "drafts/round02-pm-analytics-adaptation/data-analytics-runtime-equivalence/DRAFT.md",
    "drafts/round02-pm-analytics-adaptation/synthetic-data-and-sql-tooling/DRAFT.md",
    "drafts/round02-pm-market-discovery-adaptation/market-strategy-evidence-boundary/DRAFT.md",
    "drafts/round02-pm-market-discovery-adaptation/product-discovery-research-planning/DRAFT.md",
    "drafts/round02-pm-toolkit-boundary-adaptation/legal-privacy-document-boundary/DRAFT.md",
    "drafts/round02-pm-toolkit-boundary-adaptation/personal-document-and-copyediting-boundary/DRAFT.md",
    "drafts/round02-huashu-design-guidance-adaptation/design-direction-and-anti-slop-reference/DRAFT.md",
    "drafts/round02-huashu-design-guidance-adaptation/brand-asset-provenance-protocol/DRAFT.md",
    "drafts/round02-huashu-toolchain-media-adaptation/html-deck-animation-toolchain-boundary/DRAFT.md",
    "drafts/round02-huashu-toolchain-media-adaptation/voiceover-tts-media-pipeline-boundary/DRAFT.md",
    "drafts/round02-huashu-toolchain-media-adaptation/bundled-assets-redistribution-boundary/DRAFT.md",
    "drafts/mvp02-adaptation/spec-driven-development/DRAFT.md",
    "drafts/mvp02-adaptation/documentation-and-adrs/DRAFT.md",
    "drafts/mvp02-adaptation/code-review-and-quality/DRAFT.md",
)


def load(path: str) -> dict[str, object]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def verify() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        raise RuntimeError("Missing required files: " + ", ".join(missing))

    skills_doc = load("registry/skills.json")
    capabilities_doc = load("registry/capabilities.json")
    relations_doc = load("registry/relations.json")
    conflicts_doc = load("registry/conflicts.json")
    recipes_doc = load("registry/recipes.json")
    collaboration_domain_coverage_doc = load("registry/collaboration-domain-coverage.json")
    curation_expansion_rounds_doc = load("registry/curation-expansion-rounds.json")
    curation_program_plan_doc = load("registry/curation-program-plan.json")
    program_acceptance_map_doc = load("registry/program-acceptance-map.json")
    round_lifecycle_contract_doc = load("registry/round-lifecycle-contract.json")
    radar_feedback_doc = load("registry/radar-feedback.json")
    github_discovery_profile_doc = load("registry/github-skill-discovery-profile.json")
    starred_sources_doc = load("registry/starred-skill-sources.json")
    source_intake_batches_doc = load("registry/source-intake-batches.json")
    round02_candidate_reviews_doc = load("registry/round02-candidate-reviews.json")
    round02_obsidian_adaptation_gate_doc = load("registry/round02-obsidian-adaptation-gate.json")
    round02_pm_execution_adaptation_gate_doc = load("registry/round02-pm-execution-adaptation-gate.json")
    round02_pm_analytics_adaptation_gate_doc = load("registry/round02-pm-analytics-adaptation-gate.json")
    round02_pm_market_discovery_adaptation_gate_doc = load("registry/round02-pm-market-discovery-adaptation-gate.json")
    round02_pm_toolkit_boundary_adaptation_gate_doc = load("registry/round02-pm-toolkit-boundary-adaptation-gate.json")
    round02_huashu_design_guidance_adaptation_gate_doc = load("registry/round02-huashu-design-guidance-adaptation-gate.json")
    round02_huashu_toolchain_media_adaptation_gate_doc = load("registry/round02-huashu-toolchain-media-adaptation-gate.json")
    round02_release_readiness_review_doc = load("registry/round02-release-readiness-review.json")
    round02_release_admission_review_template_doc = load("registry/round02-release-admission-review-template.json")
    round02_release_admission_approval_request_doc = load("registry/round02-release-admission-approval-request.json")
    round02_release_admission_approval_events_doc = load("registry/round02-release-admission-approval-events.json")
    round02_release_admission_candidate_review_doc = load("registry/round02-release-admission-candidate-review.json")
    round02_approved_payload_routing_proposal_template_doc = load("registry/round02-approved-payload-routing-proposal-template.json")
    round02_release_execution_approval_request_doc = load("registry/round02-release-execution-approval-request.json")
    round02_approved_payload_routing_approval_events_doc = load("registry/round02-approved-payload-routing-approval-events.json")
    round02_approved_payload_routing_proposal_doc = load("registry/round02-approved-payload-routing-proposal.json")
    admissions_doc = load("registry/admissions.json")
    routing_doc = load("registry/routing.json")
    scenarios_doc = load("registry/scenarios.json")
    sources_doc = load("sources/lock.json")
    mvp_batches_doc = load("registry/mvp-candidate-batches.json")
    mvp_reviews_doc = load("registry/mvp-candidate-reviews.json")
    mvp_transition_gates_doc = load("registry/mvp-transition-gates.json")
    mvp_adaptation_checklist_doc = load("registry/mvp-adaptation-review-checklist.json")
    mvp_approval_requests_doc = load("registry/mvp-approval-requests.json")
    mvp02_preflight_doc = load("registry/mvp02-preflight-readiness.json")
    mvp02_post_approval_plan_doc = load("registry/mvp02-post-approval-execution-plan.json")
    mvp02_approval_events_doc = load("registry/mvp02-approval-events.json")
    mvp02_adapted_drafts_doc = load("registry/mvp02-adapted-drafts.json")
    mvp03_release_or_routing_preflight_doc = load("registry/mvp03-release-or-routing-preflight.json")
    mvp03_release_or_routing_review_template_doc = load("registry/mvp03-release-or-routing-review-template.json")
    mvp03_release_or_routing_approval_request_doc = load("registry/mvp03-release-or-routing-approval-request.json")
    mvp03_approval_events_doc = load("registry/mvp03-approval-events.json")
    mvp03_release_or_routing_candidate_review_doc = load("registry/mvp03-release-or-routing-candidate-review.json")
    mvp03_release_routing_execution_doc = load("registry/mvp03-release-routing-execution.json")
    mvp06_lifecycle_feedback_doc = load("registry/mvp06-lifecycle-feedback.json")
    selection_document = "sources/addyosmani-agent-skills/selection.json"
    selection_doc = load(selection_document)
    manifest = load("release-manifest.json")
    validate_skills_document(skills_doc, "registry/skills.json")
    validate_capabilities_document(capabilities_doc, "registry/capabilities.json")
    validate_relations_document(relations_doc, "registry/relations.json")
    validate_conflicts_document(conflicts_doc, "registry/conflicts.json")
    validate_recipes_document(recipes_doc, "registry/recipes.json")
    validate_collaboration_domain_coverage(collaboration_domain_coverage_doc)
    validate_curation_expansion_rounds(curation_expansion_rounds_doc, collaboration_domain_coverage_doc)
    validate_curation_program_plan(curation_program_plan_doc, curation_expansion_rounds_doc)
    validate_program_acceptance_map(program_acceptance_map_doc, curation_program_plan_doc)
    validate_round_lifecycle_contract(round_lifecycle_contract_doc, curation_expansion_rounds_doc)
    validate_radar_feedback(radar_feedback_doc)
    validate_github_skill_discovery_profile(github_discovery_profile_doc)
    validate_starred_skill_sources(starred_sources_doc)
    validate_source_intake_batches(source_intake_batches_doc, collaboration_domain_coverage_doc, curation_expansion_rounds_doc)
    validate_round02_candidate_reviews(round02_candidate_reviews_doc, source_intake_batches_doc, skills_doc, manifest)
    validate_round02_obsidian_adaptation_gate(round02_obsidian_adaptation_gate_doc, round02_candidate_reviews_doc, skills_doc, manifest)
    validate_round02_pm_execution_adaptation_gate(round02_pm_execution_adaptation_gate_doc, round02_candidate_reviews_doc, skills_doc, manifest)
    validate_round02_pm_analytics_adaptation_gate(round02_pm_analytics_adaptation_gate_doc, round02_candidate_reviews_doc, skills_doc, manifest)
    validate_round02_pm_market_discovery_adaptation_gate(round02_pm_market_discovery_adaptation_gate_doc, round02_candidate_reviews_doc, skills_doc, manifest)
    validate_round02_pm_toolkit_boundary_adaptation_gate(round02_pm_toolkit_boundary_adaptation_gate_doc, round02_candidate_reviews_doc, skills_doc, manifest)
    validate_round02_huashu_design_guidance_adaptation_gate(round02_huashu_design_guidance_adaptation_gate_doc, round02_candidate_reviews_doc, skills_doc, manifest)
    validate_round02_huashu_toolchain_media_adaptation_gate(round02_huashu_toolchain_media_adaptation_gate_doc, round02_candidate_reviews_doc, skills_doc, manifest)
    validate_round02_release_readiness_review(
        round02_release_readiness_review_doc,
        source_intake_batches_doc,
        round02_candidate_reviews_doc,
        [
            round02_obsidian_adaptation_gate_doc,
            round02_pm_execution_adaptation_gate_doc,
            round02_pm_analytics_adaptation_gate_doc,
            round02_pm_market_discovery_adaptation_gate_doc,
            round02_pm_toolkit_boundary_adaptation_gate_doc,
            round02_huashu_design_guidance_adaptation_gate_doc,
            round02_huashu_toolchain_media_adaptation_gate_doc,
        ],
        skills_doc,
        manifest,
    )
    validate_round02_release_admission_review_template(
        round02_release_admission_review_template_doc,
        round02_release_readiness_review_doc,
        [
            round02_obsidian_adaptation_gate_doc,
            round02_pm_execution_adaptation_gate_doc,
            round02_pm_analytics_adaptation_gate_doc,
            round02_pm_market_discovery_adaptation_gate_doc,
            round02_pm_toolkit_boundary_adaptation_gate_doc,
            round02_huashu_design_guidance_adaptation_gate_doc,
            round02_huashu_toolchain_media_adaptation_gate_doc,
        ],
    )
    validate_round02_release_admission_approval_request(
        round02_release_admission_approval_request_doc,
        round02_release_readiness_review_doc,
        round02_release_admission_review_template_doc,
    )
    validate_round02_release_admission_approval_events(
        round02_release_admission_approval_events_doc,
        round02_release_admission_approval_request_doc,
    )
    validate_round02_release_admission_candidate_review(
        round02_release_admission_candidate_review_doc,
        round02_release_admission_approval_events_doc,
        round02_release_readiness_review_doc,
        round02_release_admission_review_template_doc,
        [
            round02_obsidian_adaptation_gate_doc,
            round02_pm_execution_adaptation_gate_doc,
            round02_pm_analytics_adaptation_gate_doc,
            round02_pm_market_discovery_adaptation_gate_doc,
            round02_pm_toolkit_boundary_adaptation_gate_doc,
            round02_huashu_design_guidance_adaptation_gate_doc,
            round02_huashu_toolchain_media_adaptation_gate_doc,
        ],
        skills_doc,
        manifest,
    )
    validate_round02_approved_payload_routing_proposal_template(
        round02_approved_payload_routing_proposal_template_doc,
        round02_release_admission_candidate_review_doc,
    )
    validate_round02_release_execution_approval_request(
        round02_release_execution_approval_request_doc,
        round02_release_admission_candidate_review_doc,
        round02_approved_payload_routing_proposal_template_doc,
    )
    validate_round02_approved_payload_routing_approval_events(
        round02_approved_payload_routing_approval_events_doc,
        round02_release_execution_approval_request_doc,
    )
    validate_round02_approved_payload_routing_proposal(
        round02_approved_payload_routing_proposal_doc,
        round02_approved_payload_routing_approval_events_doc,
        round02_release_execution_approval_request_doc,
        round02_release_admission_candidate_review_doc,
        skills_doc,
        capabilities_doc,
        relations_doc,
        routing_doc,
        scenarios_doc,
        manifest,
        sources_doc,
    )
    validate_admissions_document(admissions_doc, "registry/admissions.json")
    validate_routing_document(routing_doc, "registry/routing.json")
    validate_scenarios_document(scenarios_doc, "registry/scenarios.json")
    validate_sources_lock_document(sources_doc, "sources/lock.json")
    validate_selection_document(selection_doc, selection_document)
    validate_release_manifest_document(manifest, "release-manifest.json")

    registry = skills_doc["skills"]
    directories = sorted(path.name for path in (ROOT / "skills").iterdir() if path.is_dir())
    registered = sorted(item["directory"] for item in registry)
    if directories != registered:
        raise RuntimeError("Skill registry does not match installed directories.")

    validate_inventory_counts(
        registry, manifest, directories, "release-manifest.json"
    )
    validate_manifest_payload(ROOT, manifest, registry)

    source_records = sources_doc["sources"]
    source_record = next(
        (item for item in source_records if item.get("id") == UPSTREAM_SOURCE_ID),
        None,
    )
    if source_record is None:
        raise RuntimeError(f"Missing source lock record: {UPSTREAM_SOURCE_ID}")
    validate_source_selection(
        selection_doc,
        source_record,
        ALLOWED_SELECTION_DISPOSITIONS,
        selection_document,
    )
    selection = selection_doc["decisions"]
    validate_adopted_selection(
        selection,
        registry,
        selection_doc["source"],
        selection_document,
    )
    validate_mvp_candidate_batches(
        mvp_batches_doc,
        sources_doc,
        selection_doc,
        skills_doc,
        manifest,
    )
    validate_mvp_candidate_reviews(
        mvp_reviews_doc,
        mvp_batches_doc,
        sources_doc,
        selection_doc,
        skills_doc,
        manifest,
    )
    validate_mvp_transition_gates(
        mvp_transition_gates_doc,
        mvp_batches_doc,
        mvp_reviews_doc,
        skills_doc,
        manifest,
        mvp02_approval_events_doc,
        mvp02_adapted_drafts_doc,
    )
    validate_mvp_adaptation_review_checklist(
        mvp_adaptation_checklist_doc,
        mvp_transition_gates_doc,
    )
    validate_mvp_approval_requests(
        mvp_approval_requests_doc,
        mvp_transition_gates_doc,
        mvp_adaptation_checklist_doc,
        mvp02_approval_events_doc,
        mvp02_adapted_drafts_doc,
    )
    validate_mvp02_preflight_readiness(
        mvp02_preflight_doc,
        mvp_batches_doc,
        mvp_reviews_doc,
        mvp_transition_gates_doc,
        mvp_adaptation_checklist_doc,
        mvp_approval_requests_doc,
        mvp02_approval_events_doc,
        mvp02_adapted_drafts_doc,
        skills_doc,
        manifest,
    )
    validate_mvp02_post_approval_execution_plan(
        mvp02_post_approval_plan_doc,
        mvp02_preflight_doc,
        mvp_batches_doc,
        mvp_reviews_doc,
        mvp_transition_gates_doc,
        mvp_adaptation_checklist_doc,
        mvp_approval_requests_doc,
        mvp02_approval_events_doc,
        mvp02_adapted_drafts_doc,
        skills_doc,
        manifest,
    )
    validate_mvp02_approval_events(
        mvp02_approval_events_doc,
        mvp_approval_requests_doc,
    )
    validate_mvp02_adapted_drafts(
        mvp02_adapted_drafts_doc,
        mvp02_approval_events_doc,
        mvp_batches_doc,
        mvp_reviews_doc,
        mvp_transition_gates_doc,
        mvp_adaptation_checklist_doc,
        mvp_approval_requests_doc,
        sources_doc,
        selection_doc,
        skills_doc,
        manifest,
    )
    validate_mvp03_release_or_routing_preflight(
        mvp03_release_or_routing_preflight_doc,
        mvp02_adapted_drafts_doc,
        skills_doc,
        manifest,
    )
    validate_mvp03_release_or_routing_review_template(
        mvp03_release_or_routing_review_template_doc,
        mvp03_release_or_routing_preflight_doc,
        mvp02_adapted_drafts_doc,
    )
    validate_mvp03_release_or_routing_approval_request(
        mvp03_release_or_routing_approval_request_doc,
        mvp03_release_or_routing_preflight_doc,
        mvp03_release_or_routing_review_template_doc,
    )
    validate_mvp03_approval_events(
        mvp03_approval_events_doc,
        mvp03_release_or_routing_approval_request_doc,
    )
    validate_mvp03_release_or_routing_candidate_review(
        mvp03_release_or_routing_candidate_review_doc,
        mvp03_approval_events_doc,
        mvp03_release_or_routing_preflight_doc,
        mvp03_release_or_routing_review_template_doc,
        mvp02_adapted_drafts_doc,
        skills_doc,
        manifest,
    )
    validate_mvp03_release_routing_execution(
        mvp03_release_routing_execution_doc,
        mvp03_release_or_routing_candidate_review_doc,
        skills_doc,
        capabilities_doc,
        recipes_doc,
        relations_doc,
        routing_doc,
        scenarios_doc,
        manifest,
    )
    validate_mvp06_lifecycle_feedback(
        mvp06_lifecycle_feedback_doc,
        mvp03_release_routing_execution_doc,
        mvp03_release_or_routing_candidate_review_doc,
        skills_doc,
        manifest,
    )
    validate_mvp06_radar_feedback_projection(
        radar_feedback_doc,
        mvp06_lifecycle_feedback_doc,
    )
    validate_references(
        {
            "skills": skills_doc,
            "capabilities": capabilities_doc,
            "relations": relations_doc,
            "conflicts": conflicts_doc,
            "recipes": recipes_doc,
            "sources": sources_doc,
            "admissions": admissions_doc,
            "routing": routing_doc,
            "scenarios": scenarios_doc,
        }
    )
    expected_report = run_scenarios(ROOT)
    if load("generated/routing-simulation-report.json") != expected_report:
        raise RuntimeError("Generated routing simulation report is stale.")
    if expected_report["failed"] or expected_report["unclassifiedLifecycleCapabilities"]:
        raise RuntimeError("Routing simulation did not close all scenarios and lifecycle capabilities.")
    validate_lifecycle_coverage(capabilities_doc, recipes_doc)
    adopted_directories = {
        name for name, disposition in selection.items() if disposition == "adopt"
    }

    for item in registry:
        path = ROOT / "skills" / item["directory"] / "SKILL.md"
        if not path.is_file():
            raise RuntimeError(f"Missing {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        meta = parse_frontmatter(text, path.relative_to(ROOT).as_posix())
        if meta.get("name") != item["name"] or meta.get("description") != item["description"]:
            raise RuntimeError(f"Registry/frontmatter drift: {item['directory']}")
        if item["directory"] in adopted_directories:
            if not meta["description"].startswith("Use when"):
                raise RuntimeError(f"Non-trigger description: {item['directory']}")
            for forbidden in FORBIDDEN_APPROVED_TEXT:
                if forbidden.lower() in text.lower():
                    raise RuntimeError(f"Agent-specific or unsafe text in {item['directory']}: {forbidden}")
            for reference in re.findall(r"`(references/[^`]+)`", text):
                if not (path.parent / reference).is_file():
                    raise RuntimeError(f"Dead adopted-Skill reference in {item['directory']}: {reference}")

    subprocess.run([sys.executable, str(ROOT / "scripts/build_topology.py"), "--check"], check=True)


def validate_radar_feedback(feedback_doc: dict[str, object]) -> None:
    if feedback_doc.get("schema") != 1:
        raise RuntimeError("Radar feedback schema must be 1.")
    decisions = feedback_doc.get("decisions", [])
    if not isinstance(decisions, list) or not decisions:
        raise RuntimeError("Radar feedback must contain decisions.")
    seen: set[str] = set()
    allowed_dispositions = {
        "reject",
        "reference-only",
        "already-reviewed",
        "approved-elsewhere",
    }
    for decision in decisions:
        if not isinstance(decision, dict):
            raise RuntimeError("Radar feedback decisions must be objects.")
        decision_id = decision.get("id")
        if not isinstance(decision_id, str) or not decision_id:
            raise RuntimeError("Radar feedback decision id is required.")
        if decision_id in seen:
            raise RuntimeError(f"Duplicate radar feedback decision: {decision_id}")
        seen.add(decision_id)
        if decision.get("disposition") not in allowed_dispositions:
            raise RuntimeError(f"Radar feedback disposition is unsupported: {decision_id}")
        applies_to = decision.get("appliesTo", [])
        if not isinstance(applies_to, list) or not applies_to:
            raise RuntimeError(f"Radar feedback appliesTo is required: {decision_id}")
        if "skill_candidate" not in applies_to:
            raise RuntimeError(f"Radar feedback must be scoped to skill candidates: {decision_id}")
        if not isinstance(decision.get("reason"), str) or not decision.get("reason"):
            raise RuntimeError(f"Radar feedback reason is required: {decision_id}")
        if not isinstance(decision.get("runtimeEligible"), bool):
            raise RuntimeError(f"Radar feedback runtimeEligible must be boolean: {decision_id}")
        for ref in decision.get("reviewRefs", []):
            if not isinstance(ref, str) or not (ROOT / ref).is_file():
                raise RuntimeError(f"Radar feedback has dead review ref: {decision_id}/{ref}")


def validate_starred_skill_sources(document: dict[str, object]) -> None:
    if document.get("schema") != 1:
        raise RuntimeError("Starred Skill sources schema must be 1.")
    snapshot = document.get("snapshot")
    if not isinstance(snapshot, dict):
        raise RuntimeError("Starred Skill sources snapshot is required.")
    entry_count = snapshot.get("entryCount")
    sources = document.get("sources")
    if not isinstance(sources, list) or not sources:
        raise RuntimeError("Starred Skill sources must contain sources.")
    if entry_count != len(sources):
        raise RuntimeError("Starred Skill source entryCount does not match sources.")
    if snapshot.get("purpose") and "not approval" not in str(snapshot.get("purpose")).lower():
        raise RuntimeError("Starred Skill sources purpose must state non-approval.")

    allowed_classes = {
        "official-external-baseline",
        "index-awesome-list",
        "large-skill-library",
        "third-party-skill-source",
        "methodology-skill-framework",
        "methodology-guidance",
    }
    allowed_disposition_prefixes = (
        "reference",
        "discovery-index",
        "candidate",
        "already-reviewed",
    )
    seen: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            raise RuntimeError("Starred Skill source entries must be objects.")
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id.startswith("github:"):
            raise RuntimeError("Starred Skill source id must be a github: id.")
        if source_id in seen:
            raise RuntimeError(f"Duplicate Starred Skill source: {source_id}")
        seen.add(source_id)
        if source.get("class") not in allowed_classes:
            raise RuntimeError(f"Unsupported Starred Skill source class: {source_id}")
        disposition = source.get("initialDisposition")
        if not isinstance(disposition, str) or not disposition.startswith(allowed_disposition_prefixes):
            raise RuntimeError(f"Unsupported Starred Skill source disposition: {source_id}")
        url = source.get("url")
        if not isinstance(url, str) or not url.startswith("https://github.com/"):
            raise RuntimeError(f"Starred Skill source URL must be a GitHub URL: {source_id}")
        detected = source.get("detected")
        if not isinstance(detected, dict):
            raise RuntimeError(f"Starred Skill source detected block is required: {source_id}")
        for key in ["skillMdCount", "claudeOrAgentsMdCount", "commandFileCount", "agentFileCount"]:
            if not isinstance(detected.get(key), int) or detected.get(key) < 0:
                raise RuntimeError(f"Starred Skill source detected count is invalid: {source_id}/{key}")
        if not isinstance(source.get("notes"), list) or not source.get("notes"):
            raise RuntimeError(f"Starred Skill source notes are required: {source_id}")

        if source.get("license") is None:
            text = " ".join(str(note).lower() for note in source.get("notes", []))
            if "license" not in text and source.get("class") != "official-external-baseline":
                raise RuntimeError(f"Unlicensed Starred Skill source must record a license caveat: {source_id}")
        if source.get("class") == "large-skill-library":
            text = " ".join(str(note).lower() for note in source.get("notes", []))
            for phrase in ["do not bulk import", "duplicate", "safety"]:
                if phrase not in text:
                    raise RuntimeError(f"Large Skill library must record bulk-import controls: {source_id}")


def validate_github_skill_discovery_profile(document: dict[str, object]) -> None:
    if document.get("schema") != 1:
        raise RuntimeError("GitHub Skill discovery profile schema must be 1.")
    purpose = str(document.get("purpose", "")).lower()
    for phrase in ["read-only", "not approval", "runtime installation"]:
        if phrase not in purpose:
            raise RuntimeError(f"GitHub Skill discovery profile purpose missing phrase: {phrase}")
    defaults = document.get("defaults")
    if not isinstance(defaults, dict):
        raise RuntimeError("GitHub Skill discovery profile defaults are required.")
    for key in ["perQueryLimit", "maxTreeInspections", "minimumPriorityStars", "activeWithinDays"]:
        if not isinstance(defaults.get(key), int) or defaults.get(key) <= 0:
            raise RuntimeError(f"GitHub Skill discovery profile default is invalid: {key}")
    schedule = document.get("schedule")
    if not isinstance(schedule, dict) or not schedule.get("cron"):
        raise RuntimeError("GitHub Skill discovery profile schedule is required.")
    queries = document.get("queries")
    if not isinstance(queries, list) or len(queries) < 3:
        raise RuntimeError("GitHub Skill discovery profile must define at least three queries.")
    seen: set[str] = set()
    for query in queries:
        if not isinstance(query, dict):
            raise RuntimeError("GitHub Skill discovery profile query entries must be objects.")
        query_id = query.get("id")
        if not isinstance(query_id, str) or not query_id:
            raise RuntimeError("GitHub Skill discovery profile query id is required.")
        if query_id in seen:
            raise RuntimeError(f"Duplicate GitHub Skill discovery query: {query_id}")
        seen.add(query_id)
        if not isinstance(query.get("query"), str) or not query.get("query"):
            raise RuntimeError(f"GitHub Skill discovery query text is required: {query_id}")
        if not isinstance(query.get("intent"), str) or not query.get("intent"):
            raise RuntimeError(f"GitHub Skill discovery query intent is required: {query_id}")
    policy = document.get("candidatePolicy")
    if not isinstance(policy, dict):
        raise RuntimeError("GitHub Skill discovery profile candidatePolicy is required.")
    if policy.get("starsAreWeakSignal") is not True:
        raise RuntimeError("GitHub Skill discovery profile must treat stars as weak signal.")
    if policy.get("quantityIsNotApproval") is not True:
        raise RuntimeError("GitHub Skill discovery profile must reject quantity as approval.")
    if policy.get("requiresHumanGateForRuntime") is not True:
        raise RuntimeError("GitHub Skill discovery profile must require a human runtime gate.")


def validate_collaboration_domain_coverage(document: dict[str, object]) -> None:
    if document.get("schema") != 1:
        raise RuntimeError("Collaboration domain coverage schema must be 1.")
    purpose = str(document.get("purpose", "")).lower()
    for phrase in ["not approval", "release inventory", "runtime installation"]:
        if phrase not in purpose:
            raise RuntimeError(f"Collaboration domain coverage purpose missing phrase: {phrase}")
    skill_types = document.get("skillTypes")
    if not isinstance(skill_types, list) or len(skill_types) < 2:
        raise RuntimeError("Collaboration domain coverage must define skill types.")
    type_ids = {
        item.get("id")
        for item in skill_types
        if isinstance(item, dict)
    }
    if type_ids != {"general", "specialist"}:
        raise RuntimeError("Collaboration domain coverage must define general and specialist Skill types.")
    domains = document.get("domains")
    if not isinstance(domains, list) or len(domains) < 8:
        raise RuntimeError("Collaboration domain coverage must define broad digital collaboration domains.")
    required_domains = {
        "daily-life-and-personal-productivity",
        "office-and-knowledge-work",
        "software-engineering",
        "business-and-commercial-work",
        "education-and-training",
        "academic-and-research-work",
        "creative-production-and-design",
        "data-analytics-and-reporting",
        "operations-projects-and-process",
        "security-privacy-and-compliance",
    }
    seen: set[str] = set()
    for domain in domains:
        if not isinstance(domain, dict):
            raise RuntimeError("Collaboration domain entries must be objects.")
        domain_id = domain.get("id")
        if not isinstance(domain_id, str) or not domain_id:
            raise RuntimeError("Collaboration domain id is required.")
        if domain_id in seen:
            raise RuntimeError(f"Duplicate collaboration domain: {domain_id}")
        seen.add(domain_id)
        for key in ["label", "coverageGoal"]:
            if not isinstance(domain.get(key), str) or not domain.get(key):
                raise RuntimeError(f"Collaboration domain missing {key}: {domain_id}")
        preferred = domain.get("preferredSkillTypes")
        if not isinstance(preferred, list) or not preferred or not set(preferred).issubset(type_ids):
            raise RuntimeError(f"Collaboration domain preferredSkillTypes invalid: {domain_id}")
        for key in ["candidateSignals", "riskNotes"]:
            if not isinstance(domain.get(key), list) or not domain.get(key):
                raise RuntimeError(f"Collaboration domain missing {key}: {domain_id}")
    if not required_domains.issubset(seen):
        missing = sorted(required_domains - seen)
        raise RuntimeError("Collaboration domain coverage missing required domains: " + ", ".join(missing))


def validate_program_acceptance_map(
    document: dict[str, object],
    program_doc: dict[str, object],
) -> None:
    """Validate objective -> acceptance -> verification -> evidence traceability."""
    if document.get("schema") != 1:
        raise RuntimeError("Program acceptance map schema must be 1.")
    if document.get("programPlan") != "registry/curation-program-plan.json":
        raise RuntimeError("Program acceptance map must reference the curation program plan.")
    if program_doc.get("acceptanceMap") != "registry/program-acceptance-map.json":
        raise RuntimeError("Curation program plan must reference the program acceptance map.")

    expected_assessments = {
        "planned",
        "partial",
        "verified",
        "stale",
        "blocked",
        "not-applicable",
    }
    if set(document.get("assessmentVocabulary", [])) != expected_assessments:
        raise RuntimeError("Program acceptance assessment vocabulary drifted.")

    def records(key: str) -> list[dict[str, object]]:
        value = document.get(key)
        if not isinstance(value, list) or not value:
            raise RuntimeError(f"Program acceptance map {key} must be a non-empty list.")
        if not all(isinstance(item, dict) for item in value):
            raise RuntimeError(f"Program acceptance map {key} entries must be objects.")
        return value

    def index_by_id(key: str) -> dict[str, dict[str, object]]:
        indexed: dict[str, dict[str, object]] = {}
        for item in records(key):
            item_id = item.get("id")
            if not isinstance(item_id, str) or not item_id:
                raise RuntimeError(f"Program acceptance map {key} id is required.")
            if item_id in indexed:
                raise RuntimeError(f"Program acceptance map duplicate id: {item_id}")
            indexed[item_id] = item
        return indexed

    objectives = index_by_id("objectives")
    criteria = index_by_id("acceptanceCriteria")
    verifications = index_by_id("verifications")
    evidence = index_by_id("evidence")

    program_objectives = program_doc.get("strategicObjectives")
    if not isinstance(program_objectives, list) or not program_objectives:
        raise RuntimeError("Curation program strategic objectives are required.")
    program_objective_ids = {
        item.get("id")
        for item in program_objectives
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    if program_objective_ids != set(objectives):
        raise RuntimeError("Program acceptance objective set must match the program plan.")

    referenced_criteria: set[str] = set()
    for objective_id, objective in objectives.items():
        acceptance_ids = objective.get("acceptanceIds")
        if not isinstance(acceptance_ids, list) or not acceptance_ids:
            raise RuntimeError(f"Program objective requires acceptance ids: {objective_id}")
        for acceptance_id in acceptance_ids:
            if acceptance_id not in criteria:
                raise RuntimeError(
                    f"Program objective {objective_id} references unknown acceptance id: {acceptance_id}"
                )
            referenced_criteria.add(str(acceptance_id))
        program_objective = next(
            item
            for item in program_objectives
            if isinstance(item, dict) and item.get("id") == objective_id
        )
        if program_objective.get("acceptanceIds") != acceptance_ids:
            raise RuntimeError(f"Program objective acceptance mapping drifted: {objective_id}")
    if referenced_criteria != set(criteria):
        raise RuntimeError("Every program acceptance criterion must be referenced by an objective.")

    referenced_verifications: set[str] = set()
    referenced_evidence: set[str] = set()
    for criterion_id, criterion in criteria.items():
        statement = criterion.get("statement")
        if not isinstance(statement, str) or not statement:
            raise RuntimeError(f"Program acceptance statement is required: {criterion_id}")
        assessment = criterion.get("assessment")
        if assessment not in expected_assessments:
            raise RuntimeError(f"Program acceptance assessment invalid: {criterion_id}")
        verification_ids = criterion.get("verificationIds")
        if not isinstance(verification_ids, list) or not verification_ids:
            raise RuntimeError(f"Program acceptance requires verification ids: {criterion_id}")
        for verification_id in verification_ids:
            if verification_id not in verifications:
                raise RuntimeError(
                    f"Program acceptance {criterion_id} references unknown verification id: {verification_id}"
                )
            referenced_verifications.add(str(verification_id))
        evidence_ids = criterion.get("evidenceIds")
        if not isinstance(evidence_ids, list):
            raise RuntimeError(f"Program acceptance evidence ids must be a list: {criterion_id}")
        if assessment == "verified" and not evidence_ids:
            raise RuntimeError(
                f"Program verified acceptance requires evidence: {criterion_id}"
            )
        for evidence_id in evidence_ids:
            if evidence_id not in evidence:
                raise RuntimeError(
                    f"Program acceptance {criterion_id} references unknown evidence id: {evidence_id}"
                )
            supports = evidence[evidence_id].get("supports")
            if not isinstance(supports, list) or criterion_id not in supports:
                raise RuntimeError(
                    f"Program evidence {evidence_id} does not declare support for {criterion_id}"
                )
            referenced_evidence.add(str(evidence_id))

    if referenced_verifications != set(verifications):
        raise RuntimeError("Every program verification must be referenced by acceptance criteria.")
    if referenced_evidence != set(evidence):
        raise RuntimeError("Every program evidence record must be referenced by acceptance criteria.")

    for verification_id, verification in verifications.items():
        for key in ["method", "expectedResult", "evidenceRequirement"]:
            value = verification.get(key)
            if not isinstance(value, str) or not value:
                raise RuntimeError(
                    f"Program verification {key} is required: {verification_id}"
                )
        command = verification.get("command")
        if command is not None and not isinstance(command, str):
            raise RuntimeError(f"Program verification command must be text: {verification_id}")

    criterion_ids = set(criteria)
    for evidence_id, evidence_record in evidence.items():
        path = evidence_record.get("path")
        if not isinstance(path, str) or not path:
            raise RuntimeError(f"Program evidence path is required: {evidence_id}")
        if not (ROOT / path).is_file():
            raise RuntimeError(f"Program evidence path does not exist: {path}")
        kind = evidence_record.get("kind")
        if not isinstance(kind, str) or not kind:
            raise RuntimeError(f"Program evidence kind is required: {evidence_id}")
        as_of = evidence_record.get("asOf")
        try:
            evidence_date = date.fromisoformat(str(as_of))
        except ValueError as error:
            raise RuntimeError(f"Program evidence asOf date invalid: {evidence_id}") from error
        if evidence_date > date.today():
            raise RuntimeError(f"Program evidence asOf date is in the future: {evidence_id}")
        supports = evidence_record.get("supports")
        if not isinstance(supports, list) or not supports:
            raise RuntimeError(f"Program evidence supports are required: {evidence_id}")
        unknown_supports = set(supports) - criterion_ids
        if unknown_supports:
            raise RuntimeError(
                f"Program evidence {evidence_id} references unknown acceptance ids: {sorted(unknown_supports)}"
            )
        for criterion_id in supports:
            if evidence_id not in criteria[criterion_id].get("evidenceIds", []):
                raise RuntimeError(
                    f"Program evidence support is not referenced by acceptance {criterion_id}: {evidence_id}"
                )


def validate_curation_expansion_rounds(
    document: dict[str, object],
    coverage_doc: dict[str, object],
) -> None:
    if document.get("schema") != 1:
        raise RuntimeError("Curation expansion rounds schema must be 1.")
    purpose = str(document.get("purpose", "")).lower()
    for phrase in ["not approval", "release inventory", "runtime installation"]:
        if phrase not in purpose:
            raise RuntimeError(f"Curation expansion rounds purpose missing phrase: {phrase}")
    if document.get("programPlan") != "registry/curation-program-plan.json":
        raise RuntimeError("Curation expansion rounds must reference the curation program plan.")
    if document.get("lifecycleContract") != "registry/round-lifecycle-contract.json":
        raise RuntimeError("Curation expansion rounds must reference the round lifecycle contract.")
    rounds = document.get("rounds")
    if not isinstance(rounds, list) or len(rounds) < 3:
        raise RuntimeError("Curation expansion rounds must define at least three rounds.")
    round_ids: list[str] = []
    for item in rounds:
        if not isinstance(item, dict):
            raise RuntimeError("Curation expansion round entries must be objects.")
        round_id = item.get("id")
        if not isinstance(round_id, str) or not round_id:
            raise RuntimeError("Curation expansion round id is required.")
        round_ids.append(round_id)
        if item.get("status") not in {"active", "planned", "needs-closeout", "closed"}:
            raise RuntimeError(f"Curation expansion round status invalid: {round_id}")
        for key in ["goal", "allowedChanges", "blockedChanges", "exitCriteria"]:
            value = item.get(key)
            if key == "goal":
                if not isinstance(value, str) or not value:
                    raise RuntimeError(f"Curation expansion round goal is required: {round_id}")
            elif not isinstance(value, list) or not value:
                raise RuntimeError(f"Curation expansion round {key} is required: {round_id}")
        lifecycle = item.get("lifecycle")
        if not isinstance(lifecycle, dict):
            raise RuntimeError(f"Curation expansion round lifecycle is required: {round_id}")
        if set(lifecycle) != {"plan", "execute", "acceptance", "stageCloseout"}:
            raise RuntimeError(f"Curation expansion round lifecycle keys drifted: {round_id}")
        allowed_lifecycle_values = {"planned", "recorded", "pending", "active", "passed", "closed"}
        if not set(lifecycle.values()).issubset(allowed_lifecycle_values):
            raise RuntimeError(f"Curation expansion round lifecycle value invalid: {round_id}")
        if item.get("status") == "closed":
            expected = {
                "plan": "recorded",
                "execute": "closed",
                "acceptance": "passed",
                "stageCloseout": "closed",
            }
            if lifecycle != expected:
                raise RuntimeError(f"Closed curation round lifecycle mismatch: {round_id}")
        elif item.get("status") == "active":
            if lifecycle.get("plan") != "recorded" or lifecycle.get("execute") != "active":
                raise RuntimeError(f"Active curation round must have recorded plan and active execution: {round_id}")
            if lifecycle.get("stageCloseout") != "pending":
                raise RuntimeError(f"Active curation round must not be stage-closed: {round_id}")
        elif item.get("status") == "needs-closeout":
            expected = {
                "plan": "recorded",
                "execute": "closed",
                "acceptance": "passed",
                "stageCloseout": "pending",
            }
            if lifecycle != expected:
                raise RuntimeError(f"Closeout-pending curation round lifecycle mismatch: {round_id}")
            evidence = item.get("evidence")
            if not isinstance(evidence, list) or not evidence:
                raise RuntimeError(f"Closeout-pending curation round requires evidence: {round_id}")
            for path in evidence:
                if not isinstance(path, str) or not (ROOT / path).is_file():
                    raise RuntimeError(f"Closeout-pending curation round evidence is missing: {path}")
            if not isinstance(item.get("nextGate"), str) or not item.get("nextGate"):
                raise RuntimeError(f"Closeout-pending curation round requires next gate: {round_id}")
        elif item.get("status") == "planned":
            expected = {
                "plan": "planned",
                "execute": "pending",
                "acceptance": "pending",
                "stageCloseout": "pending",
            }
            if lifecycle != expected:
                raise RuntimeError(f"Planned curation round lifecycle mismatch: {round_id}")
    if len(round_ids) != len(set(round_ids)):
        raise RuntimeError("Curation expansion round ids must be unique.")
    if document.get("currentRound") not in round_ids:
        raise RuntimeError("Curation expansion currentRound must reference a known round.")
    consumer_boundary = document.get("consumerProjectionBoundary")
    if not isinstance(consumer_boundary, dict):
        raise RuntimeError("Curation expansion consumer projection boundary is required.")
    if consumer_boundary.get("status") != "consumer-owned":
        raise RuntimeError("Curation expansion live integration must remain consumer-owned.")
    latest_evidence = consumer_boundary.get("latestDatedEvidence")
    if not isinstance(latest_evidence, str) or not (ROOT / latest_evidence).is_file():
        raise RuntimeError("Curation expansion consumer projection evidence is missing.")
    if consumer_boundary.get("currentLiveStateClaimed") is not False:
        raise RuntimeError("Curation expansion must not claim current live consumer state.")
    reason = str(consumer_boundary.get("reason", "")).lower()
    for phrase in ["dated", "consumer-owned", "fresh evidence"]:
        if phrase not in reason:
            raise RuntimeError(
                f"Curation expansion consumer projection boundary missing phrase: {phrase}"
            )
    if not coverage_doc.get("domains"):
        raise RuntimeError("Curation expansion rounds require collaboration domain coverage.")


def validate_curation_program_plan(
    document: dict[str, object],
    rounds_doc: dict[str, object],
) -> None:
    if document.get("schema") != 1:
        raise RuntimeError("Curation program plan schema must be 1.")
    purpose = str(document.get("purpose", "")).lower()
    for phrase in ["not approval", "release inventory", "runtime installation", "local sync authorization"]:
        if phrase not in purpose:
            raise RuntimeError(f"Curation program plan purpose missing phrase: {phrase}")
    if document.get("status") != "active":
        raise RuntimeError("Curation program plan must be active.")
    current_step = document.get("currentStep")
    if not isinstance(current_step, str) or not current_step:
        raise RuntimeError("Curation program plan currentStep is required.")
    allowed_program_states = {
        "planned",
        "active",
        "evidence-recorded",
        "needs-reconciliation",
        "complete",
    }
    if document.get("currentState") not in allowed_program_states:
        raise RuntimeError("Curation program plan currentState is invalid.")
    if document.get("stageCloseoutTarget") != "program-06-local-runtime-alignment-closeout":
        raise RuntimeError("Curation program plan stage closeout target drifted.")
    surfaces = set(document.get("controlledSurfaces", []))
    for required in {
        "agent-skills-curated repository",
        "approved release manifest",
        "generated routing projections",
        "reviewed third-party Skill bodies and provenance",
        "program acceptance mapping",
        "dated consumer integration evidence",
    }:
        if required not in surfaces:
            raise RuntimeError(f"Curation program plan missing controlled surface: {required}")

    positioning = document.get("strategicPositioning")
    if not isinstance(positioning, dict):
        raise RuntimeError("Curation program strategic positioning is required.")
    if positioning.get("systemRole") != "first-terminal-mvp-for-reviewed-skills":
        raise RuntimeError("Curation program must identify the reviewed Skills terminal MVP.")
    if positioning.get("internalAndExternalAudience") is not True:
        raise RuntimeError("Curation program must preserve its internal and external audience.")
    positioning_text = " ".join(str(value) for value in positioning.values()).lower()
    for phrase in [
        "resource-governance systems",
        "project-owned hard standards",
        "standard candidate",
        "future non-skill terminals",
    ]:
        if phrase not in positioning_text:
            raise RuntimeError(f"Curation program strategic positioning missing phrase: {phrase}")

    delivery = positioning.get("standardCandidateDelivery")
    expected_delivery = {
        "researchAndCandidateCustody": "YIYUAN-CALIBRATION",
        "consumerConfigurationRole": "dated-consumption-validation-and-feedback-only",
        "consumerConfigurationMayBeDurableAuthority": False,
        "projectAdmissionAuthority": "YIYUAN-ASSETS",
        "currentTransactionCrossRepositoryWritesAuthorized": False,
    }
    if delivery != expected_delivery:
        raise RuntimeError(
            "Curation program standard candidate delivery must preserve CALIBRATION custody, "
            "consumer non-authority, ASSETS admission, and the current no-write boundary."
        )

    strategic_objectives = document.get("strategicObjectives")
    if not isinstance(strategic_objectives, list) or len(strategic_objectives) != 6:
        raise RuntimeError("Curation program must define six strategic objectives.")
    objective_ids: list[str] = []
    for objective in strategic_objectives:
        if not isinstance(objective, dict):
            raise RuntimeError("Curation program strategic objectives must be objects.")
        objective_id = objective.get("id")
        if not isinstance(objective_id, str) or not objective_id:
            raise RuntimeError("Curation program strategic objective id is required.")
        objective_ids.append(objective_id)
        for key in ["statement", "authorityOwner"]:
            if not isinstance(objective.get(key), str) or not objective.get(key):
                raise RuntimeError(
                    f"Curation program strategic objective {key} is required: {objective_id}"
                )
        for key in ["nonGoals", "acceptanceIds"]:
            if not isinstance(objective.get(key), list) or not objective.get(key):
                raise RuntimeError(
                    f"Curation program strategic objective {key} is required: {objective_id}"
                )
    if len(objective_ids) != len(set(objective_ids)):
        raise RuntimeError("Curation program strategic objective ids must be unique.")

    upstream_boundary = document.get("upstreamInputBoundary")
    if not isinstance(upstream_boundary, dict):
        raise RuntimeError("Curation program plan upstream input boundary is required.")
    if upstream_boundary.get("role") != "downstream-consumer-of-broader-resource-governance-inputs":
        raise RuntimeError("Curation program plan upstream boundary role drifted.")
    entrypoints = upstream_boundary.get("knownUpstreamEntrypoints")
    if not isinstance(entrypoints, list) or not entrypoints:
        raise RuntimeError("Curation program plan upstream entrypoints are required.")
    yi_entry = next(
        (
            entry for entry in entrypoints
            if isinstance(entry, dict)
            and entry.get("id") == "github:yiheng8023/YIYUAN-MERIDIAN"
        ),
        None,
    )
    if not yi_entry or yi_entry.get("currentHandling") != "recorded-boundary-only":
        raise RuntimeError("YIYUAN-MERIDIAN must be recorded as boundary-only upstream input.")
    if yi_entry.get("url") != "https://github.com/yiheng8023/YIYUAN-MERIDIAN":
        raise RuntimeError("YIYUAN-MERIDIAN upstream URL drifted.")
    blocked_here = " ".join(str(item) for item in upstream_boundary.get("blockedHere", [])).lower()
    for phrase in [
        "upstream discovery as approval",
        "mutating yiyuan-meridian",
        "global upstream hub",
        "upstream completeness",
    ]:
        if phrase not in blocked_here:
            raise RuntimeError(f"Curation program plan upstream boundary missing blocked phrase: {phrase}")
    allowed_here = " ".join(str(item) for item in upstream_boundary.get("allowedHere", [])).lower()
    for phrase in [
        "stable upstream skill candidates",
        "upstream provenance",
        "curation and release gates",
    ]:
        if phrase not in allowed_here:
            raise RuntimeError(f"Curation program plan upstream boundary missing allowed phrase: {phrase}")

    harness_loop = document.get("harnessLoop")
    if not isinstance(harness_loop, dict):
        raise RuntimeError("Curation program plan harness loop is required.")
    if harness_loop.get("model") != "continuous-curation-harness":
        raise RuntimeError("Curation program plan harness model drifted.")
    expected_loop = [
        "discover",
        "filter",
        "review",
        "adapt",
        "verify",
        "release",
        "consume-sync",
        "feedback",
        "rediscover-or-revise",
    ]
    if harness_loop.get("loop") != expected_loop:
        raise RuntimeError("Curation program plan harness loop order drifted.")
    if harness_loop.get("completionModel") != "no-absolute-completion-only-versioned-stage-closeout":
        raise RuntimeError("Curation program plan completion model drifted.")
    standards = " ".join(str(item) for item in harness_loop.get("commercialDeliveryStandard", [])).lower()
    for phrase in [
        "source and license",
        "security and portability",
        "acceptance criteria",
        "deterministic verification",
        "release and rollback",
        "stage closeout",
    ]:
        if phrase not in standards:
            raise RuntimeError(f"Curation program plan commercial standard missing phrase: {phrase}")

    expected_steps = [
        "program-01-discovery-and-coverage",
        "program-02-source-intake-and-filtering",
        "program-03-review-and-adaptation",
        "program-04-curated-admission-and-release",
        "program-05-consumer-projection-readiness",
        "program-06-local-runtime-alignment-closeout",
    ]
    steps = document.get("steps")
    if not isinstance(steps, list) or [item.get("id") for item in steps if isinstance(item, dict)] != expected_steps:
        raise RuntimeError("Curation program plan step order drifted.")
    round_ids = {
        item.get("id")
        for item in rounds_doc.get("rounds", [])
        if isinstance(item, dict)
    }
    step_statuses: dict[str, str] = {}
    for step in steps:
        if not isinstance(step, dict):
            raise RuntimeError("Curation program plan steps must be objects.")
        step_id = step.get("id")
        step_status = step.get("status")
        if step_status not in allowed_program_states:
            raise RuntimeError(f"Curation program plan step status invalid: {step_id}")
        step_statuses[str(step_id)] = str(step_status)
        if step.get("mapsToRound") not in round_ids and not str(step.get("mapsToRound", "")).startswith(("post-release", "local-runtime")):
            raise RuntimeError(f"Curation program plan step mapsToRound is invalid: {step_id}")
        for key in [
            "goal",
            "actions",
            "acceptanceCriteria",
            "verificationStandards",
            "allowedChanges",
            "blockedActions",
            "closeoutEvidence",
        ]:
            value = step.get(key)
            if key == "goal":
                if not isinstance(value, str) or not value:
                    raise RuntimeError(f"Curation program plan goal is required: {step_id}")
            elif not isinstance(value, list) or not value:
                raise RuntimeError(f"Curation program plan {key} is required: {step_id}")
        blocked_actions = " ".join(str(item) for item in step.get("blockedActions", [])).lower()
        if step_id != "program-06-local-runtime-alignment-closeout":
            if "local codex/agents/cc-switch sync" not in blocked_actions and "writing local codex skills" not in blocked_actions:
                raise RuntimeError(f"Curation program plan must block local sync before closeout: {step_id}")
        if step_id == "program-06-local-runtime-alignment-closeout":
            acceptance_text = " ".join(str(item) for item in step.get("acceptanceCriteria", [])).lower()
            for phrase in [
                "local write authorization",
                "agents and cc switch",
                "codex",
                "source-intake-only",
                "backup",
            ]:
                if phrase not in acceptance_text:
                    raise RuntimeError(f"Local closeout acceptance missing phrase: {phrase}")
        if step.get("status") in {"evidence-recorded", "needs-reconciliation", "complete"}:
            closeout_evidence = step.get("closeoutEvidence", [])
            existing_paths = [
                item
                for item in closeout_evidence
                if isinstance(item, str) and (ROOT / item).is_file()
            ]
            if not existing_paths:
                raise RuntimeError(
                    f"Curation program evidence state requires checked-in evidence: {step_id}"
                )
    if current_step not in step_statuses:
        raise RuntimeError("Curation program currentStep must reference a known step.")
    if step_statuses[current_step] != document.get("currentState"):
        raise RuntimeError("Curation program currentState must match the current step status.")
    if document.get("stageCloseoutTarget") not in step_statuses:
        raise RuntimeError("Curation program stageCloseoutTarget must reference a known step.")
    required_global_verification = {
        "python -B scripts/verify.py",
        "python -B scripts/build_release_manifest.py --check",
        "python -B scripts/build_topology.py --check",
        "python -B scripts/simulate_routing.py --all",
        "python -B -m unittest discover -s tests -v",
    }
    if set(document.get("globalVerificationSet", [])) != required_global_verification:
        raise RuntimeError("Curation program plan global verification set drifted.")
    closeout_rule = str(document.get("stageCloseoutRule", "")).lower()
    for phrase in ["local codex", "agents", "cc switch", "approved", "authorization"]:
        if phrase not in closeout_rule:
            raise RuntimeError(f"Curation program plan closeout rule missing phrase: {phrase}")
    doc = " ".join(
        (ROOT / "docs/curation-program-plan.md").read_text(encoding="utf-8").split()
    )
    for phrase in [
        "first terminal MVP",
        "registry/program-acceptance-map.json",
        "stage-closeout reconciliation",
        "discovery and coverage",
        "source intake and filtering",
        "review and adaptation",
        "curated admission and release",
        "consumer projection readiness",
        "local runtime alignment closeout",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"Curation program plan doc missing phrase: {phrase}")
    harness_doc = " ".join(
        (ROOT / "docs/curation-harness-model.md").read_text(encoding="utf-8").split()
    )
    for phrase in [
        "continuous curation harness",
        "github:yiheng8023/YIYUAN-MERIDIAN",
        "does not treat upstream discovery as approval",
        "broader resource discovery",
        "standard candidate",
        "YIYUAN-CALIBRATION",
        "not the durable authority",
        "project-owned hard standards",
        "Future terminals",
        "commercial delivery artifacts",
        "no absolute completion state",
    ]:
        if phrase not in harness_doc:
            raise RuntimeError(f"Curation harness doc missing phrase: {phrase}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if "docs/curation-program-plan.md" not in readme:
        raise RuntimeError("README.md must link curation program plan.")
    if "docs/curation-program-plan.md" not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link curation program plan.")
    if "docs/curation-harness-model.md" not in readme:
        raise RuntimeError("README.md must link curation harness model.")
    if "docs/curation-harness-model.md" not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link curation harness model.")
    if "registry/program-acceptance-map.json" not in readme:
        raise RuntimeError("README.md must link program acceptance map.")
    if "registry/program-acceptance-map.json" not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link program acceptance map.")
    if "YIYUAN-CALIBRATION" not in readme or "durable research or standards custody" not in readme:
        raise RuntimeError("README.md must preserve the calibration custody boundary.")
    if "YIYUAN-CALIBRATION" not in readme_zh or "长期托管位置" not in readme_zh:
        raise RuntimeError("README.zh-CN.md must preserve the calibration custody boundary.")


def validate_round_lifecycle_contract(
    document: dict[str, object],
    rounds_doc: dict[str, object],
) -> None:
    if document.get("schema") != 1:
        raise RuntimeError("Round lifecycle contract schema must be 1.")
    purpose = str(document.get("purpose", "")).lower()
    for phrase in ["not approval", "release inventory", "runtime installation"]:
        if phrase not in purpose:
            raise RuntimeError(f"Round lifecycle contract purpose missing phrase: {phrase}")
    phase_order = document.get("phaseOrder")
    expected_phase_order = ["plan", "execute", "acceptance", "stageCloseout"]
    if phase_order != expected_phase_order:
        raise RuntimeError("Round lifecycle contract phase order drifted.")
    phase_contracts = document.get("phaseContracts")
    if not isinstance(phase_contracts, list) or len(phase_contracts) != len(expected_phase_order):
        raise RuntimeError("Round lifecycle contract must define all phase contracts.")
    seen_phases: list[str] = []
    for phase in phase_contracts:
        if not isinstance(phase, dict):
            raise RuntimeError("Round lifecycle phase contracts must be objects.")
        phase_id = phase.get("id")
        if not isinstance(phase_id, str):
            raise RuntimeError("Round lifecycle phase id is required.")
        seen_phases.append(phase_id)
        for key in ["requiredInputs", "allowedOutputs", "blockedActions", "verificationSurface", "exitEvidence"]:
            value = phase.get(key)
            if not isinstance(value, list) or not value:
                raise RuntimeError(f"Round lifecycle phase {key} is required: {phase_id}")
        blocked_actions = " ".join(str(item) for item in phase.get("blockedActions", [])).lower()
        if phase_id in {"plan", "execute", "stageCloseout"} and "local codex/agents/cc-switch sync" not in blocked_actions:
            raise RuntimeError(f"Round lifecycle phase must preserve local sync boundary: {phase_id}")
    if seen_phases != expected_phase_order:
        raise RuntimeError("Round lifecycle phase contracts must follow phase order.")
    expected_outcomes = {
        "complete",
        "partial",
        "blocked",
        "needs_verification",
        "needs_user_confirmation",
        "cannot_close",
    }
    if set(document.get("closeoutOutcomes", [])) != expected_outcomes:
        raise RuntimeError("Round lifecycle closeout outcomes drifted.")
    current_application = document.get("currentApplication")
    if not isinstance(current_application, dict):
        raise RuntimeError("Round lifecycle contract currentApplication is required.")
    if current_application.get("roundRegistry") != "registry/curation-expansion-rounds.json":
        raise RuntimeError("Round lifecycle currentApplication must reference the round registry.")
    if current_application.get("currentRound") != rounds_doc.get("currentRound"):
        raise RuntimeError("Round lifecycle currentRound must match the round registry.")
    current_round = next(
        (
            item
            for item in rounds_doc.get("rounds", [])
            if isinstance(item, dict) and item.get("id") == rounds_doc.get("currentRound")
        ),
        None,
    )
    if current_round is None:
        raise RuntimeError("Round lifecycle current round must resolve.")
    expected_application_state = {
        "planned": ("plan_pending", "not_ready"),
        "active": ("execute_active", "not_ready"),
        "needs-closeout": ("stage_closeout_pending", "needs_reconciliation"),
        "closed": ("stage_closed", "closed"),
    }.get(current_round.get("status"))
    if expected_application_state is None:
        raise RuntimeError("Round lifecycle current round status is unsupported.")
    if current_application.get("phaseState") != expected_application_state[0]:
        raise RuntimeError("Round lifecycle phase state must match the current round status.")
    if current_application.get("stageCloseout") != expected_application_state[1]:
        raise RuntimeError("Round lifecycle closeout state must match the current round status.")
    evidence = current_application.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise RuntimeError("Round lifecycle current application evidence is required.")
    for path in evidence:
        if not isinstance(path, str) or not (ROOT / path).is_file():
            raise RuntimeError(f"Round lifecycle current evidence is missing: {path}")
    deferred_actions = current_application.get("deferredActions")
    if not isinstance(deferred_actions, list):
        raise RuntimeError("Round lifecycle deferred actions are required.")
    if not deferred_actions:
        raise RuntimeError("Round lifecycle deferred actions must not be empty.")
    if current_round.get("status") == "needs-closeout":
        deferred_text = " ".join(str(item) for item in deferred_actions).lower()
        for phrase in ["claiming", "live runtime parity", "new candidate intake"]:
            if phrase not in deferred_text:
                raise RuntimeError(
                    f"Round lifecycle closeout deferral missing phrase: {phrase}"
                )
    if not isinstance(current_application.get("nextRequiredEvidence"), list) or not current_application.get("nextRequiredEvidence"):
        raise RuntimeError("Round lifecycle next required evidence is required.")
    doc = " ".join(
        (ROOT / "docs/round-lifecycle-contract.md").read_text(encoding="utf-8").split()
    )
    for phrase in [
        "Plan",
        "Execute",
        "Acceptance",
        "Stage closeout",
        "not approval",
        "local Codex, agents, and cc Switch sync",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"Round lifecycle doc missing phrase: {phrase}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if "docs/round-lifecycle-contract.md" not in readme:
        raise RuntimeError("README.md must link round lifecycle contract.")
    if "docs/round-lifecycle-contract.md" not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link round lifecycle contract.")


def validate_source_intake_batches(
    document: dict[str, object],
    coverage_doc: dict[str, object],
    rounds_doc: dict[str, object],
) -> None:
    if document.get("schema") != 1:
        raise RuntimeError("Source intake batches schema must be 1.")
    batches = document.get("batches")
    if not isinstance(batches, list) or not batches:
        raise RuntimeError("Source intake batches must contain batches.")
    current_batch = document.get("currentBatch")
    batch_ids = {
        batch.get("id")
        for batch in batches
        if isinstance(batch, dict)
    }
    if current_batch not in batch_ids:
        raise RuntimeError("Source intake currentBatch must reference a known batch.")
    domain_ids = {
        domain.get("id")
        for domain in coverage_doc.get("domains", [])
        if isinstance(domain, dict)
    }
    round_ids = {
        item.get("id")
        for item in rounds_doc.get("rounds", [])
        if isinstance(item, dict)
    }
    for batch in batches:
        if not isinstance(batch, dict):
            raise RuntimeError("Source intake batch entries must be objects.")
        batch_id = batch.get("id")
        if not isinstance(batch_id, str) or not batch_id:
            raise RuntimeError("Source intake batch id is required.")
        if batch.get("status") != "pinned_not_reviewed":
            raise RuntimeError(f"Source intake batch must stay pinned_not_reviewed: {batch_id}")
        purpose = str(batch.get("purpose", "")).lower()
        for phrase in ["not approval", "release inventory", "runtime installation"]:
            if phrase not in purpose:
                raise RuntimeError(f"Source intake batch purpose missing phrase: {batch_id}/{phrase}")
        if batch.get("round") not in round_ids:
            raise RuntimeError(f"Source intake batch round is unknown: {batch_id}")
        sources = batch.get("sources")
        if not isinstance(sources, list) or not sources:
            raise RuntimeError(f"Source intake batch sources are required: {batch_id}")
        blocked_actions = batch.get("blockedActions")
        if not isinstance(blocked_actions, list):
            raise RuntimeError(f"Source intake batch blockedActions are required: {batch_id}")
        for required in ["release manifest changes", "runtime installation", "local Codex/agents/cc-switch sync"]:
            if required not in blocked_actions:
                raise RuntimeError(f"Source intake batch must block action: {batch_id}/{required}")
        if batch.get("nextGate") != "license-provenance-security-portability-overlap-review":
            raise RuntimeError(f"Source intake batch nextGate is invalid: {batch_id}")

        seen_sources: set[str] = set()
        for source in sources:
            if not isinstance(source, dict):
                raise RuntimeError(f"Source intake source entries must be objects: {batch_id}")
            source_id = source.get("id")
            if not isinstance(source_id, str) or not source_id.startswith("github:"):
                raise RuntimeError(f"Source intake source id must be github: {batch_id}")
            if source_id in seen_sources:
                raise RuntimeError(f"Duplicate source intake source: {source_id}")
            seen_sources.add(source_id)
            if not isinstance(source.get("url"), str) or not source.get("url", "").startswith("https://github.com/"):
                raise RuntimeError(f"Source intake source URL must be GitHub: {source_id}")
            revision = source.get("revision")
            if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
                raise RuntimeError(f"Source intake source revision must be a full SHA: {source_id}")
            if source.get("license") not in {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "CC-BY-4.0", "CC0-1.0"}:
                raise RuntimeError(f"Source intake source license requires review or is unsupported: {source_id}")
            detected = source.get("detected")
            if not isinstance(detected, dict) or not isinstance(detected.get("skillMdCount"), int) or detected.get("skillMdCount") <= 0:
                raise RuntimeError(f"Source intake source must record positive Skill count: {source_id}")
            if not isinstance(detected.get("sampleSkillPaths"), list) or not detected.get("sampleSkillPaths"):
                raise RuntimeError(f"Source intake source must record sample Skill paths: {source_id}")
            coverage_hints = source.get("coverageHints")
            if not isinstance(coverage_hints, list) or not coverage_hints:
                raise RuntimeError(f"Source intake source coverageHints are required: {source_id}")
            if not set(coverage_hints).issubset(domain_ids):
                raise RuntimeError(f"Source intake source has unknown coverage hint: {source_id}")
            if not isinstance(source.get("reviewFocus"), list) or not source.get("reviewFocus"):
                raise RuntimeError(f"Source intake source reviewFocus is required: {source_id}")


def validate_round02_candidate_reviews(
    document: dict[str, object],
    source_intake_doc: dict[str, object],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if document.get("schema_version") != 1:
        raise RuntimeError("Round-02 candidate reviews schema_version must be 1.")
    if document.get("status") != "round02_candidate_review_recorded_not_release_approved":
        raise RuntimeError("Round-02 candidate reviews must remain not release approved.")
    if document.get("source_intake_batch") != "registry/source-intake-batches.json#round02-source-intake-2026-07-02":
        raise RuntimeError("Round-02 candidate reviews must reference the source intake batch.")

    permissions = document.get("current_permissions", {})
    if not isinstance(permissions, dict):
        raise RuntimeError("Round-02 candidate review permissions are required.")
    for key, value in permissions.items():
        expected = key == "candidate_review_allowed"
        if value is not expected:
            raise RuntimeError(f"Round-02 candidate review permission mismatch: {key}")

    batches = source_intake_doc.get("batches", [])
    current_batch = next(
        (
            batch
            for batch in batches
            if isinstance(batch, dict)
            and batch.get("id") == "round02-source-intake-2026-07-02"
        ),
        None,
    )
    if current_batch is None:
        raise RuntimeError("Round-02 source intake batch is missing.")
    source_records = {
        source.get("id"): source
        for source in current_batch.get("sources", [])
        if isinstance(source, dict)
    }
    expected_dispositions = {
        "github:kepano/obsidian-skills": "split-adapt-candidates-not-approved",
        "github:phuryn/pm-skills": "split-into-sub-batches-not-approved",
        "github:alchaincyf/huashu-design": "reference-and-adapter-candidate-not-approved",
    }
    expected_candidates = {
        "github:kepano/obsidian-skills": {
            "json-canvas": "adapter-or-merge-candidate",
            "obsidian-markdown": "merge-or-adapter-candidate",
            "obsidian-bases": "specialist-adapter-candidate",
            "obsidian-cli": "runtime-adapter-only-defer",
            "defuddle": "reference-or-tool-adapter-defer",
        },
        "github:phuryn/pm-skills": {
            "pm-ai-shipping-group": "merge-or-recipe-candidate",
            "pm-data-analytics-group": "runtime-equivalence-or-reference-review",
            "pm-execution-docs-group": "merge-into-existing-approved-skill-candidate",
            "pm-gtm-market-strategy-group": "future-specialist-batch-candidate",
            "pm-product-discovery-group": "future-product-discovery-batch-candidate",
            "pm-toolkit-legal-privacy-group": "defer-or-reference-only",
            "pm-synthetic-data-and-script-group": "tooling-or-reference-defer",
        },
        "github:alchaincyf/huashu-design": {
            "huashu-design-principles": "reference-or-merge-candidate",
            "huashu-brand-asset-protocol": "reference-candidate-with-copyright-boundary",
            "huashu-html-deck-animation-pipeline": "adapter-candidate-defer",
            "huashu-voiceover-tts-pipeline": "defer-high-boundary-toolchain",
            "huashu-bundled-assets": "do-not-vendor-before-asset-provenance-review",
        },
    }
    required_review_sections = {
        "source_integrity",
        "license_and_attribution",
        "security",
        "portability_and_neutralization",
        "overlap_and_conflict",
        "release_manifest_impact",
        "consumer_install_impact",
        "next_gate",
    }
    required_boundaries = {
        "skills/ unchanged",
        "release-manifest.json unchanged",
        "generated routing projections unchanged",
        "live Agent environments untouched",
        "source text not redistributed",
        "local Codex/agents/cc-switch sync blocked",
        "candidate decisions are not approved payload",
    }

    reviews = document.get("source_reviews", [])
    if not isinstance(reviews, list) or len(reviews) != len(source_records):
        raise RuntimeError("Round-02 candidate reviews must cover every source exactly once.")
    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = {
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    }

    seen_sources: set[str] = set()
    for review in reviews:
        if not isinstance(review, dict):
            raise RuntimeError("Round-02 candidate review entries must be objects.")
        source_id = review.get("source_id")
        if source_id in seen_sources:
            raise RuntimeError(f"Duplicate Round-02 candidate source review: {source_id}")
        seen_sources.add(str(source_id))
        source = source_records.get(source_id)
        if source is None:
            raise RuntimeError(f"Round-02 candidate review references unknown source: {source_id}")
        if review.get("revision") != source.get("revision"):
            raise RuntimeError(f"Round-02 candidate revision drifted: {source_id}")
        if review.get("license") != source.get("license"):
            raise RuntimeError(f"Round-02 candidate license drifted: {source_id}")
        detected = source.get("detected", {})
        if review.get("detected_skill_count") != detected.get("skillMdCount"):
            raise RuntimeError(f"Round-02 candidate Skill count drifted: {source_id}")
        if review.get("source_review_state") != "candidate_review_not_approved":
            raise RuntimeError(f"Round-02 candidate review state must stay not approved: {source_id}")
        if review.get("source_disposition") != expected_dispositions.get(source_id):
            raise RuntimeError(f"Round-02 candidate source disposition drifted: {source_id}")

        source_integrity = review.get("source_integrity", {})
        if not source_integrity.get("pinned_revision_verified") or not source_integrity.get("license_verified"):
            raise RuntimeError(f"Round-02 candidate source integrity not verified: {source_id}")
        review_sections = review.get("review_sections", {})
        if set(review_sections) != required_review_sections:
            raise RuntimeError(f"Round-02 candidate review sections drifted: {source_id}")
        if review_sections.get("source_integrity") != "pass":
            raise RuntimeError(f"Round-02 candidate source integrity did not pass: {source_id}")
        if review_sections.get("license_and_attribution") != "pass":
            raise RuntimeError(f"Round-02 candidate license review did not pass: {source_id}")
        if review_sections.get("release_manifest_impact") != "no_manifest_change":
            raise RuntimeError(f"Round-02 candidate must not affect manifest: {source_id}")
        if review_sections.get("consumer_install_impact") != "no_install_change":
            raise RuntimeError(f"Round-02 candidate must not affect install: {source_id}")
        for section_name in ["security", "portability_and_neutralization", "overlap_and_conflict"]:
            if review_sections.get(section_name) != "review_required":
                raise RuntimeError(f"Round-02 candidate section must require more review: {source_id}/{section_name}")

        risk_findings = review.get("risk_findings", [])
        if not isinstance(risk_findings, list) or len(risk_findings) < 3:
            raise RuntimeError(f"Round-02 candidate risk findings are incomplete: {source_id}")
        if set(review.get("boundary_assertions", [])) != required_boundaries:
            raise RuntimeError(f"Round-02 candidate boundary assertions drifted: {source_id}")

        decisions = {
            item.get("candidate_id"): item
            for item in review.get("candidate_dispositions", [])
            if isinstance(item, dict)
        }
        expected = expected_candidates.get(source_id, {})
        if set(decisions) != set(expected):
            raise RuntimeError(f"Round-02 candidate decisions drifted: {source_id}")
        for candidate_id, decision in decisions.items():
            if candidate_id in approved_directories:
                raise RuntimeError(f"Round-02 candidate unexpectedly approved: {candidate_id}")
            if any(path.startswith(f"skills/{candidate_id}/") for path in manifest_paths):
                raise RuntimeError(f"Round-02 candidate appears in release manifest: {candidate_id}")
            if decision.get("decision") != expected[candidate_id]:
                raise RuntimeError(f"Round-02 candidate disposition drifted: {candidate_id}")
            if not decision.get("rationale"):
                raise RuntimeError(f"Round-02 candidate rationale missing: {candidate_id}")
            if "separate" not in str(decision.get("next_gate", "")).lower():
                raise RuntimeError(f"Round-02 candidate next gate must be separate: {candidate_id}")

    if seen_sources != set(source_records):
        raise RuntimeError("Round-02 candidate reviews do not match source intake records.")

    validation = document.get("validation", {})
    if validation.get("status") not in {"pending_final_run", "passed"}:
        raise RuntimeError("Round-02 candidate review validation status is invalid.")
    required_commands = {
        "python -B scripts/verify.py",
        "python -B scripts/build_topology.py --check",
        "python -B scripts/build_release_manifest.py --check",
        "python -B scripts/simulate_routing.py --all",
        "python -B -m unittest discover -s tests -v",
    }
    if set(validation.get("required_commands", [])) != required_commands:
        raise RuntimeError("Round-02 candidate review required commands drifted.")
    for assertion in [
        "release-manifest.json remains unchanged",
        "generated routing projections remain unchanged",
        "skills/ remains unchanged",
        "live Agent environments are untouched",
        "source text is not redistributed as approved curated payload",
        "local Codex/agents/cc-switch sync remains blocked",
    ]:
        if assertion not in validation.get("boundary_assertions", []):
            raise RuntimeError(f"Round-02 candidate review missing boundary assertion: {assertion}")
    if "Separate approval is required" not in str(document.get("next_required_gate")):
        raise RuntimeError("Round-02 candidate review must require a separate next gate.")

    doc_path = document.get("evidence_doc")
    if doc_path != "docs/round02-candidate-review-2026-07-02.md":
        raise RuntimeError("Round-02 candidate review evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "candidate review evidence, not release approval",
        "approved payload allowed: false",
        "release manifest allowed: false",
        "routing projection allowed: false",
        "live install allowed: false",
        "local runtime sync allowed: false",
        "Source Decisions",
        "Boundary Checks",
        "Next Gates",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"Round-02 candidate review doc missing phrase: {phrase}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link Round-02 candidate review.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link Round-02 candidate review.")


def validate_round02_obsidian_adaptation_gate(
    document: dict[str, object],
    round02_reviews_doc: dict[str, object],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if document.get("schema_version") != 1:
        raise RuntimeError("Round-02 Obsidian adaptation gate schema_version must be 1.")
    if document.get("status") != "obsidian_adaptation_gate_recorded_not_release_approved":
        raise RuntimeError("Round-02 Obsidian adaptation gate status mismatch.")
    if document.get("source_review") != "registry/round02-candidate-reviews.json#github:kepano/obsidian-skills":
        raise RuntimeError("Round-02 Obsidian adaptation gate must reference the Kepano source review.")
    if document.get("source_intake_batch") != "registry/source-intake-batches.json#round02-source-intake-2026-07-02":
        raise RuntimeError("Round-02 Obsidian adaptation gate must reference the source intake batch.")
    if document.get("draft_root") != "drafts/round02-obsidian-adaptation/":
        raise RuntimeError("Round-02 Obsidian adaptation gate draft root drifted.")

    source = document.get("source", {})
    if source.get("id") != "github:kepano/obsidian-skills":
        raise RuntimeError("Round-02 Obsidian adaptation gate source id drifted.")
    if source.get("revision") != "a1dc48e68138490d522c04cbf5822214c6eb1202":
        raise RuntimeError("Round-02 Obsidian adaptation gate source revision drifted.")
    if source.get("license") != "MIT":
        raise RuntimeError("Round-02 Obsidian adaptation gate source license drifted.")

    source_reviews = {
        review.get("source_id"): review
        for review in round02_reviews_doc.get("source_reviews", [])
        if isinstance(review, dict)
    }
    kepano_review = source_reviews.get("github:kepano/obsidian-skills")
    if not kepano_review:
        raise RuntimeError("Round-02 Obsidian adaptation gate cannot find source review.")
    if kepano_review.get("revision") != source.get("revision"):
        raise RuntimeError("Round-02 Obsidian adaptation gate revision does not match source review.")
    if kepano_review.get("source_disposition") != "split-adapt-candidates-not-approved":
        raise RuntimeError("Round-02 Obsidian source review disposition drifted.")

    permissions = document.get("current_permissions", {})
    if not isinstance(permissions, dict):
        raise RuntimeError("Round-02 Obsidian adaptation gate permissions are required.")
    for key, value in permissions.items():
        expected = key == "adapted_draft_allowed"
        if value is not expected:
            raise RuntimeError(f"Round-02 Obsidian adaptation gate permission mismatch: {key}")

    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    approved_names = {item["name"] for item in skills_doc.get("skills", [])}
    approved_obsidian_items = {
        item
        for item in approved_directories | approved_names
        if "obsidian" in item.lower()
    }
    if approved_obsidian_items - {"obsidian-open-format-knowledge-files"}:
        raise RuntimeError("Round-02 Obsidian gate found an unexpected approved Obsidian Skill.")
    repository_truths = document.get("repository_truths", {})
    if repository_truths.get("approved_obsidian_skill_exists") is not False:
        raise RuntimeError("Round-02 Obsidian gate must record that no approved Obsidian Skill existed at gate time.")
    if "local runtime Skills are not repository release truth" not in str(repository_truths.get("reason", "")):
        raise RuntimeError("Round-02 Obsidian gate repository truth reason is missing the local/runtime boundary.")

    expected_drafts = {
        "obsidian-open-format-knowledge-files": (
            "new-skill-draft-candidate",
            "drafts/round02-obsidian-adaptation/open-format-knowledge-files/DRAFT.md",
            {
                "skills/json-canvas/SKILL.md": "97d1ae0728955c4203922753d5656890e5e4dd371b8306ea11884f9b510f1b85",
                "skills/obsidian-markdown/SKILL.md": "7ad72e1f0a9081ed325e76b6402ad5de50a00e63e2341fd403a92f147234a007",
                "skills/obsidian-bases/SKILL.md": "c0037f20926c7d8591cdd040365e4c0e4c0c4146386a506f28f241faee9a27d9",
            },
        ),
        "obsidian-cli-runtime-adapter": (
            "external-runtime-adapter-defer",
            "drafts/round02-obsidian-adaptation/obsidian-cli-runtime-adapter/DRAFT.md",
            {
                "skills/obsidian-cli/SKILL.md": "b54257cdc0e5d04488b35b0c797bfe427b24359f0848d3c73924dcacf8da6358",
            },
        ),
        "defuddle-tool-adapter": (
            "external-tool-adapter-defer",
            "drafts/round02-obsidian-adaptation/defuddle-tool-adapter/DRAFT.md",
            {
                "skills/defuddle/SKILL.md": "10673a4dc70a0a057612d443243ab7a5aa4abdd4a0fadc3f6eec5fd71ad5a971",
            },
        ),
    }
    manifest_paths = {
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    }
    drafts = {
        item.get("candidate_id"): item
        for item in document.get("adaptation_drafts", [])
        if isinstance(item, dict)
    }
    if set(drafts) != set(expected_drafts):
        raise RuntimeError("Round-02 Obsidian adaptation draft ids drifted.")
    for candidate_id, draft in drafts.items():
        expected_disposition, draft_path, expected_sources = expected_drafts[candidate_id]
        if draft.get("disposition") != expected_disposition:
            raise RuntimeError(f"Round-02 Obsidian draft disposition drifted: {candidate_id}")
        if draft.get("draft_path") != draft_path:
            raise RuntimeError(f"Round-02 Obsidian draft path drifted: {candidate_id}")
        if not (ROOT / draft_path).is_file():
            raise RuntimeError(f"Round-02 Obsidian draft path missing: {candidate_id}")
        if draft.get("source_text_copied") or draft.get("source_text_redistributed"):
            raise RuntimeError(f"Round-02 Obsidian draft must not copy or redistribute source text: {candidate_id}")
        if candidate_id in approved_directories and candidate_id != "obsidian-open-format-knowledge-files":
            raise RuntimeError(f"Round-02 Obsidian draft unexpectedly approved: {candidate_id}")
        if candidate_id != "obsidian-open-format-knowledge-files" and any(path.startswith(f"skills/{candidate_id}/") for path in manifest_paths):
            raise RuntimeError(f"Round-02 Obsidian draft appears in release manifest: {candidate_id}")
        source_candidates = {
            item.get("upstream_path"): item.get("upstream_sha256")
            for item in draft.get("source_candidates", [])
            if isinstance(item, dict)
        }
        if source_candidates != expected_sources:
            raise RuntimeError(f"Round-02 Obsidian draft source hashes drifted: {candidate_id}")
        if "separate" not in str(draft.get("next_gate", "")).lower():
            raise RuntimeError(f"Round-02 Obsidian draft must require a separate next gate: {candidate_id}")

    review_sections = document.get("review_sections", {})
    expected_sections = {
        "source_integrity": "pass",
        "license_and_attribution": "pass",
        "security": "bounded_in_drafts",
        "portability_and_neutralization": "bounded_in_drafts",
        "overlap_and_conflict": "repository_truth_recorded",
        "release_manifest_impact": "no_manifest_change",
        "consumer_install_impact": "no_install_change",
        "next_gate": "separate-release-or-routing-review",
    }
    if review_sections != expected_sections:
        raise RuntimeError("Round-02 Obsidian adaptation gate review sections drifted.")
    required_boundaries = {
        "skills/ unchanged",
        "release-manifest.json unchanged",
        "generated routing projections unchanged",
        "live Agent environments untouched",
        "source text not redistributed",
        "local Codex/agents/cc-switch sync blocked",
        "adaptation drafts are not approved payload",
    }
    if set(document.get("boundary_assertions", [])) != required_boundaries:
        raise RuntimeError("Round-02 Obsidian adaptation gate boundary assertions drifted.")

    validation = document.get("validation", {})
    if validation.get("status") not in {"pending_final_run", "passed"}:
        raise RuntimeError("Round-02 Obsidian adaptation gate validation status is invalid.")
    required_commands = {
        "python -B scripts/verify.py",
        "python -B scripts/build_topology.py --check",
        "python -B scripts/build_release_manifest.py --check",
        "python -B scripts/simulate_routing.py --all",
        "python -B -m unittest discover -s tests -v",
    }
    if set(validation.get("required_commands", [])) != required_commands:
        raise RuntimeError("Round-02 Obsidian adaptation gate required commands drifted.")
    for assertion in [
        "release-manifest.json remains unchanged",
        "generated routing projections remain unchanged",
        "skills/ remains unchanged",
        "live Agent environments are untouched",
        "source text is not redistributed as approved curated payload",
        "local Codex/agents/cc-switch sync remains blocked",
    ]:
        if assertion not in validation.get("boundary_assertions", []):
            raise RuntimeError(f"Round-02 Obsidian adaptation gate missing boundary assertion: {assertion}")
    if "Separate approval is required" not in str(document.get("next_required_gate")):
        raise RuntimeError("Round-02 Obsidian adaptation gate must require a separate next gate.")

    doc_path = document.get("evidence_doc")
    if doc_path != "docs/round02-obsidian-adaptation-gate.md":
        raise RuntimeError("Round-02 Obsidian adaptation gate evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "Obsidian sub-batch adaptation gate evidence, not release approval",
        "approved payload allowed: false",
        "release manifest allowed: false",
        "routing projection allowed: false",
        "live install allowed: false",
        "local runtime sync allowed: false",
        "current approved release inventory has no Obsidian-specific curated Skill",
        "Draft Decisions",
        "Boundary Checks",
        "Next Gate",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"Round-02 Obsidian adaptation gate doc missing phrase: {phrase}")

    draft_expectations = {
        "drafts/round02-obsidian-adaptation/open-format-knowledge-files/DRAFT.md": [
            "This is a file-format and knowledge-workflow candidate.",
            "Do not invoke an Obsidian CLI",
            "current repository release inventory has no approved `obsidian-vault` Skill",
        ],
        "drafts/round02-obsidian-adaptation/obsidian-cli-runtime-adapter/DRAFT.md": [
            "This is not portable Skill payload by itself.",
            "requires explicit confirmation",
            "Do not install the CLI",
        ],
        "drafts/round02-obsidian-adaptation/defuddle-tool-adapter/DRAFT.md": [
            "This is an external tool adapter",
            "Do not install npm packages",
            "Treat web fetching as an external network action.",
        ],
    }
    for path, phrases in draft_expectations.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                raise RuntimeError(f"Round-02 Obsidian draft missing phrase: {path}/{phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link Round-02 Obsidian adaptation gate.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link Round-02 Obsidian adaptation gate.")


def validate_round02_pm_execution_adaptation_gate(
    document: dict[str, object],
    round02_reviews_doc: dict[str, object],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if document.get("schema_version") != 1:
        raise RuntimeError("Round-02 PM execution adaptation gate schema_version must be 1.")
    if document.get("status") != "pm_execution_adaptation_gate_recorded_not_release_approved":
        raise RuntimeError("Round-02 PM execution adaptation gate status mismatch.")
    if document.get("source_review") != "registry/round02-candidate-reviews.json#github:phuryn/pm-skills":
        raise RuntimeError("Round-02 PM execution adaptation gate must reference the PM source review.")
    if document.get("source_intake_batch") != "registry/source-intake-batches.json#round02-source-intake-2026-07-02":
        raise RuntimeError("Round-02 PM execution adaptation gate must reference the source intake batch.")
    if document.get("draft_root") != "drafts/round02-pm-execution-adaptation/":
        raise RuntimeError("Round-02 PM execution adaptation gate draft root drifted.")

    source = document.get("source", {})
    if source.get("id") != "github:phuryn/pm-skills":
        raise RuntimeError("Round-02 PM execution adaptation gate source id drifted.")
    if source.get("revision") != "a0cd730d4c61e519ca8568b172334402257a74a9":
        raise RuntimeError("Round-02 PM execution adaptation gate source revision drifted.")
    if source.get("license") != "MIT":
        raise RuntimeError("Round-02 PM execution adaptation gate source license drifted.")

    source_reviews = {
        review.get("source_id"): review
        for review in round02_reviews_doc.get("source_reviews", [])
        if isinstance(review, dict)
    }
    pm_review = source_reviews.get("github:phuryn/pm-skills")
    if not pm_review:
        raise RuntimeError("Round-02 PM execution adaptation gate cannot find source review.")
    if pm_review.get("revision") != source.get("revision"):
        raise RuntimeError("Round-02 PM execution adaptation gate revision does not match source review.")
    if pm_review.get("source_disposition") != "split-into-sub-batches-not-approved":
        raise RuntimeError("Round-02 PM source review disposition drifted.")

    permissions = document.get("current_permissions", {})
    if not isinstance(permissions, dict):
        raise RuntimeError("Round-02 PM execution adaptation gate permissions are required.")
    for key, value in permissions.items():
        expected = key == "adapted_draft_allowed"
        if value is not expected:
            raise RuntimeError(f"Round-02 PM execution adaptation gate permission mismatch: {key}")

    subset = document.get("subset_boundary", {})
    if subset.get("included_groups") != ["pm-ai-shipping-group", "pm-execution-docs-group"]:
        raise RuntimeError("Round-02 PM execution adaptation included groups drifted.")
    expected_excluded = {
        "pm-data-analytics-group",
        "pm-gtm-market-strategy-group",
        "pm-product-discovery-group",
        "pm-toolkit-legal-privacy-group",
        "pm-synthetic-data-and-script-group",
    }
    if set(subset.get("excluded_groups", [])) != expected_excluded:
        raise RuntimeError("Round-02 PM execution adaptation excluded groups drifted.")
    if "require separate review" not in str(subset.get("reason", "")):
        raise RuntimeError("Round-02 PM execution adaptation subset reason must preserve separate review boundary.")

    expected_drafts = {
        "ai-shipping-governance": (
            "merge-or-recipe-candidate",
            "drafts/round02-pm-execution-adaptation/ai-shipping-governance/DRAFT.md",
            {
                "pm-ai-shipping/skills/intended-vs-implemented/SKILL.md": "66016f358e3e98275db3e9b0c48fe1fb533c0f7e8d10ed7c5dcd2230db42e5e4",
                "pm-ai-shipping/skills/shipping-artifacts/SKILL.md": "3f919b2181b21199c87a392afb5cfcc7ca677f140622e2871ef86853e8b40e28",
            },
        ),
        "product-execution-documents": (
            "merge-into-existing-approved-skill-candidate",
            "drafts/round02-pm-execution-adaptation/product-execution-documents/DRAFT.md",
            {
                "pm-execution/skills/create-prd/SKILL.md": "2a4059f16301c5559e10d0dfd00c9bdcde04d2cd964d8c360dbe43bd0161ed32",
                "pm-execution/skills/user-stories/SKILL.md": "8ce89cd81de5a3df7d504380d18c54cec6c59ccdb7fd18cbcb62b6b6183d0a55",
                "pm-execution/skills/job-stories/SKILL.md": "69f75264b311418a1ebaf06c9872ed1271203cfc6316466fcb99cc948ade800b",
                "pm-execution/skills/test-scenarios/SKILL.md": "2dc10ebb6359604275f26234d3c66c9ccc952e501ad5b685c23a5c0f34f634d4",
                "pm-execution/skills/release-notes/SKILL.md": "b617edd39e721267c9726286b6304f086991f5e2215b848c952a8ad9e001a0d3",
            },
        ),
    }
    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = {
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    }
    drafts = {
        item.get("candidate_id"): item
        for item in document.get("adaptation_drafts", [])
        if isinstance(item, dict)
    }
    if set(drafts) != set(expected_drafts):
        raise RuntimeError("Round-02 PM execution adaptation draft ids drifted.")
    for candidate_id, draft in drafts.items():
        expected_disposition, draft_path, expected_sources = expected_drafts[candidate_id]
        if draft.get("disposition") != expected_disposition:
            raise RuntimeError(f"Round-02 PM execution draft disposition drifted: {candidate_id}")
        if draft.get("draft_path") != draft_path:
            raise RuntimeError(f"Round-02 PM execution draft path drifted: {candidate_id}")
        if not (ROOT / draft_path).is_file():
            raise RuntimeError(f"Round-02 PM execution draft path missing: {candidate_id}")
        if draft.get("source_text_copied") or draft.get("source_text_redistributed"):
            raise RuntimeError(f"Round-02 PM execution draft must not copy or redistribute source text: {candidate_id}")
        if candidate_id in approved_directories:
            raise RuntimeError(f"Round-02 PM execution draft unexpectedly approved: {candidate_id}")
        if any(path.startswith(f"skills/{candidate_id}/") for path in manifest_paths):
            raise RuntimeError(f"Round-02 PM execution draft appears in release manifest: {candidate_id}")
        source_candidates = {
            item.get("upstream_path"): item.get("upstream_sha256")
            for item in draft.get("source_candidates", [])
            if isinstance(item, dict)
        }
        if source_candidates != expected_sources:
            raise RuntimeError(f"Round-02 PM execution draft source hashes drifted: {candidate_id}")
        if "separate" not in str(draft.get("next_gate", "")).lower():
            raise RuntimeError(f"Round-02 PM execution draft must require a separate next gate: {candidate_id}")
        if not isinstance(draft.get("likely_targets"), list) or not draft.get("likely_targets"):
            raise RuntimeError(f"Round-02 PM execution draft likely targets missing: {candidate_id}")

    expected_sections = {
        "source_integrity": "pass",
        "license_and_attribution": "pass",
        "security": "bounded_in_drafts",
        "portability_and_neutralization": "bounded_in_drafts",
        "overlap_and_conflict": "bounded_in_drafts",
        "release_manifest_impact": "no_manifest_change",
        "consumer_install_impact": "no_install_change",
        "next_gate": "separate-release-or-routing-review",
    }
    if document.get("review_sections") != expected_sections:
        raise RuntimeError("Round-02 PM execution adaptation gate review sections drifted.")
    required_boundaries = {
        "skills/ unchanged",
        "release-manifest.json unchanged",
        "generated routing projections unchanged",
        "live Agent environments untouched",
        "source text not redistributed",
        "local Codex/agents/cc-switch sync blocked",
        "adaptation drafts are not approved payload",
        "excluded PM groups remain unreviewed by this gate",
    }
    if set(document.get("boundary_assertions", [])) != required_boundaries:
        raise RuntimeError("Round-02 PM execution adaptation gate boundary assertions drifted.")

    validation = document.get("validation", {})
    if validation.get("status") not in {"pending_final_run", "passed"}:
        raise RuntimeError("Round-02 PM execution adaptation gate validation status is invalid.")
    required_commands = {
        "python -B scripts/verify.py",
        "python -B scripts/build_topology.py --check",
        "python -B scripts/build_release_manifest.py --check",
        "python -B scripts/simulate_routing.py --all",
        "python -B -m unittest discover -s tests -v",
    }
    if set(validation.get("required_commands", [])) != required_commands:
        raise RuntimeError("Round-02 PM execution adaptation gate required commands drifted.")
    for assertion in [
        "release-manifest.json remains unchanged",
        "generated routing projections remain unchanged",
        "skills/ remains unchanged",
        "live Agent environments are untouched",
        "source text is not redistributed as approved curated payload",
        "local Codex/agents/cc-switch sync remains blocked",
    ]:
        if assertion not in validation.get("boundary_assertions", []):
            raise RuntimeError(f"Round-02 PM execution adaptation gate missing boundary assertion: {assertion}")
    if "Separate approval is required" not in str(document.get("next_required_gate")):
        raise RuntimeError("Round-02 PM execution adaptation gate must require a separate next gate.")

    doc_path = document.get("evidence_doc")
    if doc_path != "docs/round02-pm-execution-adaptation-gate.md":
        raise RuntimeError("Round-02 PM execution adaptation gate evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "adaptation gate evidence, not",
        "approved payload allowed: false",
        "release manifest allowed: false",
        "routing projection allowed: false",
        "live install allowed: false",
        "local runtime sync allowed: false",
        "It explicitly excludes PM analytics",
        "Draft Decisions",
        "Boundary Checks",
        "Next Gate",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"Round-02 PM execution adaptation gate doc missing phrase: {phrase}")

    draft_expectations = {
        "drafts/round02-pm-execution-adaptation/ai-shipping-governance/DRAFT.md": [
            "This is a governance and review workflow candidate.",
            "Do not fabricate product intent from code behavior.",
            "does not replace a security scanner",
        ],
        "drafts/round02-pm-execution-adaptation/product-execution-documents/DRAFT.md": [
            "This is an execution-document workflow candidate.",
            "Do not save files by default",
            "Do not claim a release note describes shipped behavior without shipped evidence.",
        ],
    }
    for path, phrases in draft_expectations.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                raise RuntimeError(f"Round-02 PM execution draft missing phrase: {path}/{phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link Round-02 PM execution adaptation gate.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link Round-02 PM execution adaptation gate.")


def validate_round02_pm_analytics_adaptation_gate(
    document: dict[str, object],
    round02_reviews_doc: dict[str, object],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if document.get("schema_version") != 1:
        raise RuntimeError("Round-02 PM analytics adaptation gate schema_version must be 1.")
    if document.get("status") != "pm_analytics_adaptation_gate_recorded_not_release_approved":
        raise RuntimeError("Round-02 PM analytics adaptation gate status mismatch.")
    if document.get("source_review") != "registry/round02-candidate-reviews.json#github:phuryn/pm-skills":
        raise RuntimeError("Round-02 PM analytics adaptation gate must reference the PM source review.")
    if document.get("source_intake_batch") != "registry/source-intake-batches.json#round02-source-intake-2026-07-02":
        raise RuntimeError("Round-02 PM analytics adaptation gate must reference the source intake batch.")
    if document.get("draft_root") != "drafts/round02-pm-analytics-adaptation/":
        raise RuntimeError("Round-02 PM analytics adaptation gate draft root drifted.")

    source = document.get("source", {})
    if source.get("id") != "github:phuryn/pm-skills":
        raise RuntimeError("Round-02 PM analytics adaptation gate source id drifted.")
    if source.get("revision") != "a0cd730d4c61e519ca8568b172334402257a74a9":
        raise RuntimeError("Round-02 PM analytics adaptation gate source revision drifted.")
    if source.get("license") != "MIT":
        raise RuntimeError("Round-02 PM analytics adaptation gate source license drifted.")

    source_reviews = {
        review.get("source_id"): review
        for review in round02_reviews_doc.get("source_reviews", [])
        if isinstance(review, dict)
    }
    pm_review = source_reviews.get("github:phuryn/pm-skills")
    if not pm_review:
        raise RuntimeError("Round-02 PM analytics adaptation gate cannot find source review.")
    if pm_review.get("revision") != source.get("revision"):
        raise RuntimeError("Round-02 PM analytics adaptation gate revision does not match source review.")
    if pm_review.get("source_disposition") != "split-into-sub-batches-not-approved":
        raise RuntimeError("Round-02 PM source review disposition drifted.")

    permissions = document.get("current_permissions", {})
    if not isinstance(permissions, dict):
        raise RuntimeError("Round-02 PM analytics adaptation gate permissions are required.")
    for key, value in permissions.items():
        expected = key == "adapted_draft_allowed"
        if value is not expected:
            raise RuntimeError(f"Round-02 PM analytics adaptation gate permission mismatch: {key}")

    subset = document.get("subset_boundary", {})
    if subset.get("included_groups") != ["pm-data-analytics-group", "pm-synthetic-data-and-script-group"]:
        raise RuntimeError("Round-02 PM analytics adaptation included groups drifted.")
    expected_excluded = {
        "pm-ai-shipping-group",
        "pm-execution-docs-group",
        "pm-gtm-market-strategy-group",
        "pm-product-discovery-group",
        "pm-toolkit-legal-privacy-group",
    }
    if set(subset.get("excluded_groups", [])) != expected_excluded:
        raise RuntimeError("Round-02 PM analytics adaptation excluded groups drifted.")
    if "require separate review" not in str(subset.get("reason", "")):
        raise RuntimeError("Round-02 PM analytics adaptation subset reason must preserve separate review boundary.")

    expected_drafts = {
        "data-analytics-runtime-equivalence": (
            "runtime-equivalence-or-reference-candidate",
            "drafts/round02-pm-analytics-adaptation/data-analytics-runtime-equivalence/DRAFT.md",
            {
                "pm-data-analytics/skills/ab-test-analysis/SKILL.md": "ffe66e488c4866a53b8d76d07642f09d6b5551dfa31d74ba52d2abe699fd3bc2",
                "pm-data-analytics/skills/cohort-analysis/SKILL.md": "18d694475f0ce3ad5eb1c8ff02f929eb19d96b70b1d0090ebfc254f2dda0972b",
                "pm-data-analytics/skills/sql-queries/SKILL.md": "c7b402e74b1ebea7d17148e3afc17ca5f2c6620fdb40d371f940f766abc51670",
            },
        ),
        "synthetic-data-and-sql-tooling": (
            "tooling-or-reference-defer",
            "drafts/round02-pm-analytics-adaptation/synthetic-data-and-sql-tooling/DRAFT.md",
            {
                "pm-execution/skills/dummy-dataset/SKILL.md": "86968aef8853341ca9abd7d0403826c576926e39e5981b48b52964c82fe87d0d",
                "pm-data-analytics/skills/sql-queries/SKILL.md": "c7b402e74b1ebea7d17148e3afc17ca5f2c6620fdb40d371f940f766abc51670",
                "pm-data-analytics/skills/cohort-analysis/SKILL.md": "18d694475f0ce3ad5eb1c8ff02f929eb19d96b70b1d0090ebfc254f2dda0972b",
            },
        ),
    }
    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = {
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    }
    drafts = {
        item.get("candidate_id"): item
        for item in document.get("adaptation_drafts", [])
        if isinstance(item, dict)
    }
    if set(drafts) != set(expected_drafts):
        raise RuntimeError("Round-02 PM analytics adaptation draft ids drifted.")
    for candidate_id, draft in drafts.items():
        expected_disposition, draft_path, expected_sources = expected_drafts[candidate_id]
        if draft.get("disposition") != expected_disposition:
            raise RuntimeError(f"Round-02 PM analytics draft disposition drifted: {candidate_id}")
        if draft.get("draft_path") != draft_path:
            raise RuntimeError(f"Round-02 PM analytics draft path drifted: {candidate_id}")
        if not (ROOT / draft_path).is_file():
            raise RuntimeError(f"Round-02 PM analytics draft path missing: {candidate_id}")
        if draft.get("source_text_copied") or draft.get("source_text_redistributed"):
            raise RuntimeError(f"Round-02 PM analytics draft must not copy or redistribute source text: {candidate_id}")
        if candidate_id in approved_directories:
            raise RuntimeError(f"Round-02 PM analytics draft unexpectedly approved: {candidate_id}")
        if any(path.startswith(f"skills/{candidate_id}/") for path in manifest_paths):
            raise RuntimeError(f"Round-02 PM analytics draft appears in release manifest: {candidate_id}")
        source_candidates = {
            item.get("upstream_path"): item.get("upstream_sha256")
            for item in draft.get("source_candidates", [])
            if isinstance(item, dict)
        }
        if source_candidates != expected_sources:
            raise RuntimeError(f"Round-02 PM analytics draft source hashes drifted: {candidate_id}")
        if "separate" not in str(draft.get("next_gate", "")).lower():
            raise RuntimeError(f"Round-02 PM analytics draft must require a separate next gate: {candidate_id}")
        if not isinstance(draft.get("likely_targets"), list) or not draft.get("likely_targets"):
            raise RuntimeError(f"Round-02 PM analytics draft likely targets missing: {candidate_id}")

    expected_sections = {
        "source_integrity": "pass",
        "license_and_attribution": "pass",
        "security": "bounded_in_drafts",
        "portability_and_neutralization": "bounded_in_drafts",
        "overlap_and_conflict": "runtime_equivalence_bounded",
        "release_manifest_impact": "no_manifest_change",
        "consumer_install_impact": "no_install_change",
        "next_gate": "separate-release-or-routing-review",
    }
    if document.get("review_sections") != expected_sections:
        raise RuntimeError("Round-02 PM analytics adaptation gate review sections drifted.")
    required_boundaries = {
        "skills/ unchanged",
        "release-manifest.json unchanged",
        "generated routing projections unchanged",
        "live Agent environments untouched",
        "source text not redistributed",
        "local Codex/agents/cc-switch sync blocked",
        "adaptation drafts are not approved payload",
        "non-analytics PM groups remain outside this gate",
    }
    if set(document.get("boundary_assertions", [])) != required_boundaries:
        raise RuntimeError("Round-02 PM analytics adaptation gate boundary assertions drifted.")

    validation = document.get("validation", {})
    if validation.get("status") not in {"pending_final_run", "passed"}:
        raise RuntimeError("Round-02 PM analytics adaptation gate validation status is invalid.")
    required_commands = {
        "python -B scripts/verify.py",
        "python -B scripts/build_topology.py --check",
        "python -B scripts/build_release_manifest.py --check",
        "python -B scripts/simulate_routing.py --all",
        "python -B -m unittest discover -s tests -v",
    }
    if set(validation.get("required_commands", [])) != required_commands:
        raise RuntimeError("Round-02 PM analytics adaptation gate required commands drifted.")
    for assertion in [
        "release-manifest.json remains unchanged",
        "generated routing projections remain unchanged",
        "skills/ remains unchanged",
        "live Agent environments are untouched",
        "source text is not redistributed as approved curated payload",
        "local Codex/agents/cc-switch sync remains blocked",
    ]:
        if assertion not in validation.get("boundary_assertions", []):
            raise RuntimeError(f"Round-02 PM analytics adaptation gate missing boundary assertion: {assertion}")
    if "Separate approval is required" not in str(document.get("next_required_gate")):
        raise RuntimeError("Round-02 PM analytics adaptation gate must require a separate next gate.")

    doc_path = document.get("evidence_doc")
    if doc_path != "docs/round02-pm-analytics-adaptation-gate.md":
        raise RuntimeError("Round-02 PM analytics adaptation gate evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "PM analytics and data-safety adaptation gate evidence, not release approval",
        "approved payload allowed: false",
        "release manifest allowed: false",
        "routing projection allowed: false",
        "live install allowed: false",
        "local runtime sync allowed: false",
        "It explicitly excludes PM AI-shipping",
        "Draft Decisions",
        "Boundary Checks",
        "Next Gate",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"Round-02 PM analytics adaptation gate doc missing phrase: {phrase}")

    draft_expectations = {
        "drafts/round02-pm-analytics-adaptation/data-analytics-runtime-equivalence/DRAFT.md": [
            "This is a data-analysis runtime-equivalence candidate.",
            "Do not execute SQL or Python by default.",
            "Do not claim statistical significance without explicit assumptions.",
        ],
        "drafts/round02-pm-analytics-adaptation/synthetic-data-and-sql-tooling/DRAFT.md": [
            "This is a synthetic-data and SQL tooling candidate.",
            "Do not run generated SQL against a live database.",
            "Do not generate realistic personal data from real people.",
        ],
    }
    for path, phrases in draft_expectations.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                raise RuntimeError(f"Round-02 PM analytics draft missing phrase: {path}/{phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link Round-02 PM analytics adaptation gate.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link Round-02 PM analytics adaptation gate.")


def validate_round02_pm_market_discovery_adaptation_gate(
    document: dict[str, object],
    round02_reviews_doc: dict[str, object],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if document.get("schema_version") != 1:
        raise RuntimeError("Round-02 PM market/discovery adaptation gate schema_version must be 1.")
    if document.get("status") != "pm_market_discovery_adaptation_gate_recorded_not_release_approved":
        raise RuntimeError("Round-02 PM market/discovery adaptation gate status mismatch.")
    if document.get("source_review") != "registry/round02-candidate-reviews.json#github:phuryn/pm-skills":
        raise RuntimeError("Round-02 PM market/discovery adaptation gate must reference the PM source review.")
    if document.get("source_intake_batch") != "registry/source-intake-batches.json#round02-source-intake-2026-07-02":
        raise RuntimeError("Round-02 PM market/discovery adaptation gate must reference the source intake batch.")
    if document.get("draft_root") != "drafts/round02-pm-market-discovery-adaptation/":
        raise RuntimeError("Round-02 PM market/discovery adaptation gate draft root drifted.")

    source = document.get("source", {})
    if source.get("id") != "github:phuryn/pm-skills":
        raise RuntimeError("Round-02 PM market/discovery adaptation gate source id drifted.")
    if source.get("revision") != "a0cd730d4c61e519ca8568b172334402257a74a9":
        raise RuntimeError("Round-02 PM market/discovery adaptation gate source revision drifted.")
    if source.get("license") != "MIT":
        raise RuntimeError("Round-02 PM market/discovery adaptation gate source license drifted.")

    source_reviews = {
        review.get("source_id"): review
        for review in round02_reviews_doc.get("source_reviews", [])
        if isinstance(review, dict)
    }
    pm_review = source_reviews.get("github:phuryn/pm-skills")
    if not pm_review:
        raise RuntimeError("Round-02 PM market/discovery adaptation gate cannot find source review.")
    if pm_review.get("revision") != source.get("revision"):
        raise RuntimeError("Round-02 PM market/discovery adaptation gate revision does not match source review.")
    if pm_review.get("source_disposition") != "split-into-sub-batches-not-approved":
        raise RuntimeError("Round-02 PM source review disposition drifted.")

    permissions = document.get("current_permissions", {})
    if not isinstance(permissions, dict):
        raise RuntimeError("Round-02 PM market/discovery adaptation gate permissions are required.")
    for key, value in permissions.items():
        expected = key == "adapted_draft_allowed"
        if value is not expected:
            raise RuntimeError(f"Round-02 PM market/discovery adaptation gate permission mismatch: {key}")

    subset = document.get("subset_boundary", {})
    if subset.get("included_groups") != ["pm-gtm-market-strategy-group", "pm-product-discovery-group"]:
        raise RuntimeError("Round-02 PM market/discovery adaptation included groups drifted.")
    expected_excluded = {
        "pm-ai-shipping-group",
        "pm-execution-docs-group",
        "pm-data-analytics-group",
        "pm-toolkit-legal-privacy-group",
        "pm-synthetic-data-and-script-group",
    }
    if set(subset.get("excluded_groups", [])) != expected_excluded:
        raise RuntimeError("Round-02 PM market/discovery adaptation excluded groups drifted.")
    if "require separate review" not in str(subset.get("reason", "")):
        raise RuntimeError("Round-02 PM market/discovery adaptation subset reason must preserve separate review boundary.")

    expected_drafts = {
        "market-strategy-evidence-boundary": (
            "business-strategy-reference-or-recipe-candidate",
            "drafts/round02-pm-market-discovery-adaptation/market-strategy-evidence-boundary/DRAFT.md",
            {
                "pm-go-to-market/skills/competitive-battlecard/SKILL.md": "986bb9382a8e60f1283ff725da325b4a04f39d910938a976f36a3056deb44308",
                "pm-market-research/skills/competitor-analysis/SKILL.md": "ef66dae4ba0fa149efe63cdbae7744b5d6f0af86079e5b086d2dfed9e503176a",
                "pm-market-research/skills/market-sizing/SKILL.md": "7aa8c27712995b93105129e0b20d61cf19977c1c32e1464ee7a6dec3c28ac4a7",
                "pm-product-strategy/skills/product-strategy/SKILL.md": "89d79aca5083d5774f05760ce41326328f38284e47c7208c98f7f3c3dbf12ec0",
                "pm-marketing-growth/skills/positioning-ideas/SKILL.md": "1269dd4ffe819983ce14f3ccc826afa5f3828538730c0cb7a8a988b66c5d9e67",
            },
        ),
        "product-discovery-research-planning": (
            "product-discovery-merge-or-recipe-candidate",
            "drafts/round02-pm-market-discovery-adaptation/product-discovery-research-planning/DRAFT.md",
            {
                "pm-product-discovery/skills/opportunity-solution-tree/SKILL.md": "67c8644730477fd7518bfac3fda51358f236f55eb4070de4678256679a419180",
                "pm-product-discovery/skills/prioritize-features/SKILL.md": "ebad72f12a4389d5dbf5dfab78afd1ff9d382cc96bcf9c1dd8b730709e3d2a74",
                "pm-product-discovery/skills/metrics-dashboard/SKILL.md": "9933f2f8749c436d3d48129543719899b2d1da5c602ff6a5add1ee48239e33d5",
                "pm-product-discovery/skills/interview-script/SKILL.md": "be9fe91ec26b2ffea82578177f1e7e60be0a22b2a09cef9f1af62e5c21ee4819",
            },
        ),
    }
    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = {
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    }
    drafts = {
        item.get("candidate_id"): item
        for item in document.get("adaptation_drafts", [])
        if isinstance(item, dict)
    }
    if set(drafts) != set(expected_drafts):
        raise RuntimeError("Round-02 PM market/discovery adaptation draft ids drifted.")
    for candidate_id, draft in drafts.items():
        expected_disposition, draft_path, expected_sources = expected_drafts[candidate_id]
        if draft.get("disposition") != expected_disposition:
            raise RuntimeError(f"Round-02 PM market/discovery draft disposition drifted: {candidate_id}")
        if draft.get("draft_path") != draft_path:
            raise RuntimeError(f"Round-02 PM market/discovery draft path drifted: {candidate_id}")
        if not (ROOT / draft_path).is_file():
            raise RuntimeError(f"Round-02 PM market/discovery draft path missing: {candidate_id}")
        if draft.get("source_text_copied") or draft.get("source_text_redistributed"):
            raise RuntimeError(f"Round-02 PM market/discovery draft must not copy or redistribute source text: {candidate_id}")
        if candidate_id in approved_directories:
            raise RuntimeError(f"Round-02 PM market/discovery draft unexpectedly approved: {candidate_id}")
        if any(path.startswith(f"skills/{candidate_id}/") for path in manifest_paths):
            raise RuntimeError(f"Round-02 PM market/discovery draft appears in release manifest: {candidate_id}")
        source_candidates = {
            item.get("upstream_path"): item.get("upstream_sha256")
            for item in draft.get("source_candidates", [])
            if isinstance(item, dict)
        }
        if source_candidates != expected_sources:
            raise RuntimeError(f"Round-02 PM market/discovery draft source hashes drifted: {candidate_id}")
        if "separate" not in str(draft.get("next_gate", "")).lower():
            raise RuntimeError(f"Round-02 PM market/discovery draft must require a separate next gate: {candidate_id}")
        if not isinstance(draft.get("likely_targets"), list) or not draft.get("likely_targets"):
            raise RuntimeError(f"Round-02 PM market/discovery draft likely targets missing: {candidate_id}")

    expected_sections = {
        "source_integrity": "pass",
        "license_and_attribution": "pass",
        "security": "bounded_in_drafts",
        "portability_and_neutralization": "bounded_in_drafts",
        "overlap_and_conflict": "business_and_discovery_bounded",
        "release_manifest_impact": "no_manifest_change",
        "consumer_install_impact": "no_install_change",
        "next_gate": "separate-release-or-routing-review",
    }
    if document.get("review_sections") != expected_sections:
        raise RuntimeError("Round-02 PM market/discovery adaptation gate review sections drifted.")
    required_boundaries = {
        "skills/ unchanged",
        "release-manifest.json unchanged",
        "generated routing projections unchanged",
        "live Agent environments untouched",
        "source text not redistributed",
        "local Codex/agents/cc-switch sync blocked",
        "adaptation drafts are not approved payload",
        "analytics/script/legal PM groups remain outside this gate",
    }
    if set(document.get("boundary_assertions", [])) != required_boundaries:
        raise RuntimeError("Round-02 PM market/discovery adaptation gate boundary assertions drifted.")

    validation = document.get("validation", {})
    if validation.get("status") not in {"pending_final_run", "passed"}:
        raise RuntimeError("Round-02 PM market/discovery adaptation gate validation status is invalid.")
    required_commands = {
        "python -B scripts/verify.py",
        "python -B scripts/build_topology.py --check",
        "python -B scripts/build_release_manifest.py --check",
        "python -B scripts/simulate_routing.py --all",
        "python -B -m unittest discover -s tests -v",
    }
    if set(validation.get("required_commands", [])) != required_commands:
        raise RuntimeError("Round-02 PM market/discovery adaptation gate required commands drifted.")
    for assertion in [
        "release-manifest.json remains unchanged",
        "generated routing projections remain unchanged",
        "skills/ remains unchanged",
        "live Agent environments are untouched",
        "source text is not redistributed as approved curated payload",
        "local Codex/agents/cc-switch sync remains blocked",
    ]:
        if assertion not in validation.get("boundary_assertions", []):
            raise RuntimeError(f"Round-02 PM market/discovery adaptation gate missing boundary assertion: {assertion}")
    if "Separate approval is required" not in str(document.get("next_required_gate")):
        raise RuntimeError("Round-02 PM market/discovery adaptation gate must require a separate next gate.")

    doc_path = document.get("evidence_doc")
    if doc_path != "docs/round02-pm-market-discovery-adaptation-gate.md":
        raise RuntimeError("Round-02 PM market/discovery adaptation gate evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "PM market and product-discovery adaptation gate evidence, not release approval",
        "approved payload allowed: false",
        "release manifest allowed: false",
        "routing projection allowed: false",
        "live install allowed: false",
        "local runtime sync allowed: false",
        "It explicitly excludes PM AI-shipping",
        "Draft Decisions",
        "Boundary Checks",
        "Next Gate",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"Round-02 PM market/discovery adaptation gate doc missing phrase: {phrase}")

    draft_expectations = {
        "drafts/round02-pm-market-discovery-adaptation/market-strategy-evidence-boundary/DRAFT.md": [
            "This is a market and strategy evidence-boundary candidate.",
            "Do not present estimates, competitor claims, pricing, funding, or market share as current facts without dated sources.",
            "Do not provide investment, legal, financial, or guaranteed business advice.",
        ],
        "drafts/round02-pm-market-discovery-adaptation/product-discovery-research-planning/DRAFT.md": [
            "This is a product-discovery research-planning candidate.",
            "Do not treat interview opinions as validated demand.",
            "Do not collect or expose participant personal data without explicit scope and handling rules.",
        ],
    }
    for path, phrases in draft_expectations.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                raise RuntimeError(f"Round-02 PM market/discovery draft missing phrase: {path}/{phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link Round-02 PM market/discovery adaptation gate.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link Round-02 PM market/discovery adaptation gate.")


def validate_round02_pm_toolkit_boundary_adaptation_gate(
    document: dict[str, object],
    round02_reviews_doc: dict[str, object],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if document.get("schema_version") != 1:
        raise RuntimeError("Round-02 PM toolkit adaptation gate schema_version must be 1.")
    if document.get("status") != "pm_toolkit_boundary_adaptation_gate_recorded_not_release_approved":
        raise RuntimeError("Round-02 PM toolkit adaptation gate status mismatch.")
    if document.get("source_review") != "registry/round02-candidate-reviews.json#github:phuryn/pm-skills":
        raise RuntimeError("Round-02 PM toolkit adaptation gate must reference the PM source review.")
    if document.get("source_intake_batch") != "registry/source-intake-batches.json#round02-source-intake-2026-07-02":
        raise RuntimeError("Round-02 PM toolkit adaptation gate must reference the source intake batch.")
    if document.get("draft_root") != "drafts/round02-pm-toolkit-boundary-adaptation/":
        raise RuntimeError("Round-02 PM toolkit adaptation gate draft root drifted.")

    source = document.get("source", {})
    if source.get("id") != "github:phuryn/pm-skills":
        raise RuntimeError("Round-02 PM toolkit adaptation gate source id drifted.")
    if source.get("revision") != "a0cd730d4c61e519ca8568b172334402257a74a9":
        raise RuntimeError("Round-02 PM toolkit adaptation gate source revision drifted.")
    if source.get("license") != "MIT":
        raise RuntimeError("Round-02 PM toolkit adaptation gate source license drifted.")

    source_reviews = {
        review.get("source_id"): review
        for review in round02_reviews_doc.get("source_reviews", [])
        if isinstance(review, dict)
    }
    pm_review = source_reviews.get("github:phuryn/pm-skills")
    if not pm_review:
        raise RuntimeError("Round-02 PM toolkit adaptation gate cannot find source review.")
    if pm_review.get("revision") != source.get("revision"):
        raise RuntimeError("Round-02 PM toolkit adaptation gate revision does not match source review.")
    if pm_review.get("source_disposition") != "split-into-sub-batches-not-approved":
        raise RuntimeError("Round-02 PM source review disposition drifted.")

    permissions = document.get("current_permissions", {})
    if not isinstance(permissions, dict):
        raise RuntimeError("Round-02 PM toolkit adaptation gate permissions are required.")
    for key, value in permissions.items():
        expected = key == "adapted_draft_allowed"
        if value is not expected:
            raise RuntimeError(f"Round-02 PM toolkit adaptation gate permission mismatch: {key}")

    subset = document.get("subset_boundary", {})
    if subset.get("included_groups") != ["pm-toolkit-legal-privacy-group"]:
        raise RuntimeError("Round-02 PM toolkit adaptation included groups drifted.")
    expected_excluded = {
        "pm-ai-shipping-group",
        "pm-execution-docs-group",
        "pm-data-analytics-group",
        "pm-gtm-market-strategy-group",
        "pm-product-discovery-group",
        "pm-synthetic-data-and-script-group",
    }
    if set(subset.get("excluded_groups", [])) != expected_excluded:
        raise RuntimeError("Round-02 PM toolkit adaptation excluded groups drifted.")
    if "require separate review" not in str(subset.get("reason", "")):
        raise RuntimeError("Round-02 PM toolkit adaptation subset reason must preserve separate review boundary.")

    expected_drafts = {
        "legal-privacy-document-boundary": (
            "defer-high-stakes-reference-only",
            "drafts/round02-pm-toolkit-boundary-adaptation/legal-privacy-document-boundary/DRAFT.md",
            {
                "pm-toolkit/skills/draft-nda/SKILL.md": "3242473abc50b8de46106172258145840c9b2b9674b72523250dd2ae62aec5b4",
                "pm-toolkit/skills/privacy-policy/SKILL.md": "8e326c2f2608c6d59ba7724545d890ffd99e0c635883a321c5257c1de526965c",
            },
        ),
        "personal-document-and-copyediting-boundary": (
            "merge-or-reference-candidate",
            "drafts/round02-pm-toolkit-boundary-adaptation/personal-document-and-copyediting-boundary/DRAFT.md",
            {
                "pm-toolkit/skills/review-resume/SKILL.md": "54d1e41b80a381ce08d8e8c5d22482356fe9333320404ce550a7a4651bf5889b",
                "pm-toolkit/skills/grammar-check/SKILL.md": "1a9cb1a837f053fb83381b573bfa6ff2e7447517f5cf76c42373f0c180e313a7",
            },
        ),
    }
    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = {
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    }
    drafts = {
        item.get("candidate_id"): item
        for item in document.get("adaptation_drafts", [])
        if isinstance(item, dict)
    }
    if set(drafts) != set(expected_drafts):
        raise RuntimeError("Round-02 PM toolkit adaptation draft ids drifted.")
    for candidate_id, draft in drafts.items():
        expected_disposition, draft_path, expected_sources = expected_drafts[candidate_id]
        if draft.get("disposition") != expected_disposition:
            raise RuntimeError(f"Round-02 PM toolkit draft disposition drifted: {candidate_id}")
        if draft.get("draft_path") != draft_path:
            raise RuntimeError(f"Round-02 PM toolkit draft path drifted: {candidate_id}")
        if not (ROOT / draft_path).is_file():
            raise RuntimeError(f"Round-02 PM toolkit draft path missing: {candidate_id}")
        if draft.get("source_text_copied") or draft.get("source_text_redistributed"):
            raise RuntimeError(f"Round-02 PM toolkit draft must not copy or redistribute source text: {candidate_id}")
        if candidate_id in approved_directories:
            raise RuntimeError(f"Round-02 PM toolkit draft unexpectedly approved: {candidate_id}")
        if any(path.startswith(f"skills/{candidate_id}/") for path in manifest_paths):
            raise RuntimeError(f"Round-02 PM toolkit draft appears in release manifest: {candidate_id}")
        source_candidates = {
            item.get("upstream_path"): item.get("upstream_sha256")
            for item in draft.get("source_candidates", [])
            if isinstance(item, dict)
        }
        if source_candidates != expected_sources:
            raise RuntimeError(f"Round-02 PM toolkit draft source hashes drifted: {candidate_id}")
        if "separate" not in str(draft.get("next_gate", "")).lower():
            raise RuntimeError(f"Round-02 PM toolkit draft must require a separate next gate: {candidate_id}")
        if not isinstance(draft.get("likely_targets"), list) or not draft.get("likely_targets"):
            raise RuntimeError(f"Round-02 PM toolkit draft likely targets missing: {candidate_id}")

    expected_sections = {
        "source_integrity": "pass",
        "license_and_attribution": "pass",
        "security": "bounded_in_drafts",
        "portability_and_neutralization": "bounded_in_drafts",
        "overlap_and_conflict": "high_stakes_boundary_bounded",
        "release_manifest_impact": "no_manifest_change",
        "consumer_install_impact": "no_install_change",
        "next_gate": "separate-release-or-routing-review",
    }
    if document.get("review_sections") != expected_sections:
        raise RuntimeError("Round-02 PM toolkit adaptation gate review sections drifted.")
    required_boundaries = {
        "skills/ unchanged",
        "release-manifest.json unchanged",
        "generated routing projections unchanged",
        "live Agent environments untouched",
        "source text not redistributed",
        "local Codex/agents/cc-switch sync blocked",
        "adaptation drafts are not approved payload",
        "non-toolkit PM groups remain outside this gate",
    }
    if set(document.get("boundary_assertions", [])) != required_boundaries:
        raise RuntimeError("Round-02 PM toolkit adaptation gate boundary assertions drifted.")

    validation = document.get("validation", {})
    if validation.get("status") not in {"pending_final_run", "passed"}:
        raise RuntimeError("Round-02 PM toolkit adaptation gate validation status is invalid.")
    required_commands = {
        "python -B scripts/verify.py",
        "python -B scripts/build_topology.py --check",
        "python -B scripts/build_release_manifest.py --check",
        "python -B scripts/simulate_routing.py --all",
        "python -B -m unittest discover -s tests -v",
    }
    if set(validation.get("required_commands", [])) != required_commands:
        raise RuntimeError("Round-02 PM toolkit adaptation gate required commands drifted.")
    for assertion in [
        "release-manifest.json remains unchanged",
        "generated routing projections remain unchanged",
        "skills/ remains unchanged",
        "live Agent environments are untouched",
        "source text is not redistributed as approved curated payload",
        "local Codex/agents/cc-switch sync remains blocked",
    ]:
        if assertion not in validation.get("boundary_assertions", []):
            raise RuntimeError(f"Round-02 PM toolkit adaptation gate missing boundary assertion: {assertion}")
    if "Separate approval is required" not in str(document.get("next_required_gate")):
        raise RuntimeError("Round-02 PM toolkit adaptation gate must require a separate next gate.")

    doc_path = document.get("evidence_doc")
    if doc_path != "docs/round02-pm-toolkit-boundary-adaptation-gate.md":
        raise RuntimeError("Round-02 PM toolkit adaptation gate evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "PM toolkit high-boundary adaptation gate evidence, not release approval",
        "approved payload allowed: false",
        "release manifest allowed: false",
        "routing projection allowed: false",
        "live install allowed: false",
        "local runtime sync allowed: false",
        "It explicitly excludes PM AI-shipping",
        "Draft Decisions",
        "Boundary Checks",
        "Next Gate",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"Round-02 PM toolkit adaptation gate doc missing phrase: {phrase}")

    draft_expectations = {
        "drafts/round02-pm-toolkit-boundary-adaptation/legal-privacy-document-boundary/DRAFT.md": [
            "This is a legal and privacy document boundary candidate.",
            "Do not provide legal advice or claim compliance.",
            "Do not produce publish-ready legal documents without licensed review.",
        ],
        "drafts/round02-pm-toolkit-boundary-adaptation/personal-document-and-copyediting-boundary/DRAFT.md": [
            "This is a personal-document and copyediting boundary candidate.",
            "Do not make hiring, employment, immigration, or credential claims.",
            "Do not expose resume or job-posting personal data in public outputs.",
        ],
    }
    for path, phrases in draft_expectations.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                raise RuntimeError(f"Round-02 PM toolkit draft missing phrase: {path}/{phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link Round-02 PM toolkit adaptation gate.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link Round-02 PM toolkit adaptation gate.")


def validate_round02_huashu_design_guidance_adaptation_gate(
    document: dict[str, object],
    round02_reviews_doc: dict[str, object],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if document.get("schema_version") != 1:
        raise RuntimeError("Round-02 Huashu design guidance gate schema_version must be 1.")
    if document.get("status") != "huashu_design_guidance_adaptation_gate_recorded_not_release_approved":
        raise RuntimeError("Round-02 Huashu design guidance gate status mismatch.")
    if document.get("source_review") != "registry/round02-candidate-reviews.json#github:alchaincyf/huashu-design":
        raise RuntimeError("Round-02 Huashu design guidance gate must reference the Huashu source review.")
    if document.get("source_intake_batch") != "registry/source-intake-batches.json#round02-source-intake-2026-07-02":
        raise RuntimeError("Round-02 Huashu design guidance gate must reference the source intake batch.")
    if document.get("draft_root") != "drafts/round02-huashu-design-guidance-adaptation/":
        raise RuntimeError("Round-02 Huashu design guidance gate draft root drifted.")

    source = document.get("source", {})
    if source.get("id") != "github:alchaincyf/huashu-design":
        raise RuntimeError("Round-02 Huashu design guidance gate source id drifted.")
    if source.get("revision") != "ec9ec0fff8a66a932c4049b200ea4c2b09f8d25b":
        raise RuntimeError("Round-02 Huashu design guidance gate source revision drifted.")
    if source.get("license") != "MIT":
        raise RuntimeError("Round-02 Huashu design guidance gate source license drifted.")

    source_reviews = {
        review.get("source_id"): review
        for review in round02_reviews_doc.get("source_reviews", [])
        if isinstance(review, dict)
    }
    huashu_review = source_reviews.get("github:alchaincyf/huashu-design")
    if not huashu_review:
        raise RuntimeError("Round-02 Huashu design guidance gate cannot find source review.")
    if huashu_review.get("revision") != source.get("revision"):
        raise RuntimeError("Round-02 Huashu design guidance gate revision does not match source review.")
    if huashu_review.get("source_disposition") != "reference-and-adapter-candidate-not-approved":
        raise RuntimeError("Round-02 Huashu source review disposition drifted.")

    permissions = document.get("current_permissions", {})
    if not isinstance(permissions, dict):
        raise RuntimeError("Round-02 Huashu design guidance gate permissions are required.")
    for key, value in permissions.items():
        expected = key == "adapted_draft_allowed"
        if value is not expected:
            raise RuntimeError(f"Round-02 Huashu design guidance gate permission mismatch: {key}")

    subset = document.get("subset_boundary", {})
    if subset.get("included_candidates") != ["huashu-design-principles", "huashu-brand-asset-protocol"]:
        raise RuntimeError("Round-02 Huashu design guidance included candidates drifted.")
    expected_excluded = {
        "huashu-html-deck-animation-pipeline",
        "huashu-voiceover-tts-pipeline",
        "huashu-bundled-assets",
    }
    if set(subset.get("excluded_candidates", [])) != expected_excluded:
        raise RuntimeError("Round-02 Huashu design guidance excluded candidates drifted.")
    if "require separate review" not in str(subset.get("reason", "")):
        raise RuntimeError("Round-02 Huashu design guidance subset reason must preserve separate review boundary.")

    expected_drafts = {
        "design-direction-and-anti-slop-reference": (
            "design-guidance-reference-or-merge-candidate",
            "drafts/round02-huashu-design-guidance-adaptation/design-direction-and-anti-slop-reference/DRAFT.md",
            {
                "SKILL.md": "2830077dd711de0cccd4c3c00a840d7b5d69b14ac38446e19826540c99d914ad",
            },
        ),
        "brand-asset-provenance-protocol": (
            "asset-provenance-reference-candidate",
            "drafts/round02-huashu-design-guidance-adaptation/brand-asset-provenance-protocol/DRAFT.md",
            {
                "references/brand-asset-protocol.md": "b9de11c57843dd8029611417d97c84da610890d2a450de9a3f24e3428767e1ea",
            },
        ),
    }
    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = {
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    }
    drafts = {
        item.get("candidate_id"): item
        for item in document.get("adaptation_drafts", [])
        if isinstance(item, dict)
    }
    if set(drafts) != set(expected_drafts):
        raise RuntimeError("Round-02 Huashu design guidance draft ids drifted.")
    for candidate_id, draft in drafts.items():
        expected_disposition, draft_path, expected_sources = expected_drafts[candidate_id]
        if draft.get("disposition") != expected_disposition:
            raise RuntimeError(f"Round-02 Huashu design guidance draft disposition drifted: {candidate_id}")
        if draft.get("draft_path") != draft_path:
            raise RuntimeError(f"Round-02 Huashu design guidance draft path drifted: {candidate_id}")
        if not (ROOT / draft_path).is_file():
            raise RuntimeError(f"Round-02 Huashu design guidance draft path missing: {candidate_id}")
        if draft.get("source_text_copied") or draft.get("source_text_redistributed"):
            raise RuntimeError(f"Round-02 Huashu design guidance draft must not copy or redistribute source text: {candidate_id}")
        if candidate_id in approved_directories:
            raise RuntimeError(f"Round-02 Huashu design guidance draft unexpectedly approved: {candidate_id}")
        if any(path.startswith(f"skills/{candidate_id}/") for path in manifest_paths):
            raise RuntimeError(f"Round-02 Huashu design guidance draft appears in release manifest: {candidate_id}")
        source_candidates = {
            item.get("upstream_path"): item.get("upstream_sha256")
            for item in draft.get("source_candidates", [])
            if isinstance(item, dict)
        }
        if source_candidates != expected_sources:
            raise RuntimeError(f"Round-02 Huashu design guidance draft source hashes drifted: {candidate_id}")
        if "separate" not in str(draft.get("next_gate", "")).lower():
            raise RuntimeError(f"Round-02 Huashu design guidance draft must require a separate next gate: {candidate_id}")
        if not isinstance(draft.get("likely_targets"), list) or not draft.get("likely_targets"):
            raise RuntimeError(f"Round-02 Huashu design guidance draft likely targets missing: {candidate_id}")

    expected_sections = {
        "source_integrity": "pass",
        "license_and_attribution": "pass",
        "security": "bounded_in_drafts",
        "portability_and_neutralization": "bounded_in_drafts",
        "overlap_and_conflict": "design_guidance_bounded",
        "release_manifest_impact": "no_manifest_change",
        "consumer_install_impact": "no_install_change",
        "next_gate": "separate-release-or-routing-review",
    }
    if document.get("review_sections") != expected_sections:
        raise RuntimeError("Round-02 Huashu design guidance gate review sections drifted.")
    required_boundaries = {
        "skills/ unchanged",
        "release-manifest.json unchanged",
        "generated routing projections unchanged",
        "live Agent environments untouched",
        "source text not redistributed",
        "local Codex/agents/cc-switch sync blocked",
        "adaptation drafts are not approved payload",
        "Huashu toolchain and bundled assets remain outside this gate",
    }
    if set(document.get("boundary_assertions", [])) != required_boundaries:
        raise RuntimeError("Round-02 Huashu design guidance gate boundary assertions drifted.")

    validation = document.get("validation", {})
    if validation.get("status") not in {"pending_final_run", "passed"}:
        raise RuntimeError("Round-02 Huashu design guidance gate validation status is invalid.")
    required_commands = {
        "python -B scripts/verify.py",
        "python -B scripts/build_topology.py --check",
        "python -B scripts/build_release_manifest.py --check",
        "python -B scripts/simulate_routing.py --all",
        "python -B -m unittest discover -s tests -v",
    }
    if set(validation.get("required_commands", [])) != required_commands:
        raise RuntimeError("Round-02 Huashu design guidance gate required commands drifted.")
    for assertion in [
        "release-manifest.json remains unchanged",
        "generated routing projections remain unchanged",
        "skills/ remains unchanged",
        "live Agent environments are untouched",
        "source text is not redistributed as approved curated payload",
        "local Codex/agents/cc-switch sync remains blocked",
    ]:
        if assertion not in validation.get("boundary_assertions", []):
            raise RuntimeError(f"Round-02 Huashu design guidance gate missing boundary assertion: {assertion}")
    if "Separate approval is required" not in str(document.get("next_required_gate")):
        raise RuntimeError("Round-02 Huashu design guidance gate must require a separate next gate.")

    doc_path = document.get("evidence_doc")
    if doc_path != "docs/round02-huashu-design-guidance-adaptation-gate.md":
        raise RuntimeError("Round-02 Huashu design guidance gate evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "Huashu design-guidance adaptation gate evidence, not release approval",
        "approved payload allowed: false",
        "release manifest allowed: false",
        "routing projection allowed: false",
        "live install allowed: false",
        "local runtime sync allowed: false",
        "It explicitly excludes HTML deck, voiceover, and bundled asset toolchain candidates.",
        "Draft Decisions",
        "Boundary Checks",
        "Next Gate",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"Round-02 Huashu design guidance gate doc missing phrase: {phrase}")

    draft_expectations = {
        "drafts/round02-huashu-design-guidance-adaptation/design-direction-and-anti-slop-reference/DRAFT.md": [
            "This is a design-direction and anti-slop reference candidate.",
            "Do not hard-code a single visual style as universal good design.",
            "Do not rely on a tool-specific WebSearch name or agent-specific workflow.",
        ],
        "drafts/round02-huashu-design-guidance-adaptation/brand-asset-provenance-protocol/DRAFT.md": [
            "This is a brand-asset provenance protocol candidate.",
            "Do not scrape, download, or redistribute brand assets without permission and source review.",
            "Do not use CSS silhouettes, hand-drawn SVGs, or generic placeholders as if they were official product assets.",
        ],
    }
    for path, phrases in draft_expectations.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                raise RuntimeError(f"Round-02 Huashu design guidance draft missing phrase: {path}/{phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link Round-02 Huashu design guidance gate.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link Round-02 Huashu design guidance gate.")


def validate_round02_huashu_toolchain_media_adaptation_gate(
    document: dict[str, object],
    round02_reviews_doc: dict[str, object],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if document.get("schema_version") != 1:
        raise RuntimeError("Round-02 Huashu toolchain/media gate schema_version must be 1.")
    if document.get("status") != "huashu_toolchain_media_adaptation_gate_recorded_not_release_approved":
        raise RuntimeError("Round-02 Huashu toolchain/media gate status mismatch.")
    if document.get("source_review") != "registry/round02-candidate-reviews.json#github:alchaincyf/huashu-design":
        raise RuntimeError("Round-02 Huashu toolchain/media gate must reference the Huashu source review.")
    if document.get("source_intake_batch") != "registry/source-intake-batches.json#round02-source-intake-2026-07-02":
        raise RuntimeError("Round-02 Huashu toolchain/media gate must reference the source intake batch.")
    if document.get("draft_root") != "drafts/round02-huashu-toolchain-media-adaptation/":
        raise RuntimeError("Round-02 Huashu toolchain/media gate draft root drifted.")

    source = document.get("source", {})
    if source.get("id") != "github:alchaincyf/huashu-design":
        raise RuntimeError("Round-02 Huashu toolchain/media gate source id drifted.")
    if source.get("revision") != "ec9ec0fff8a66a932c4049b200ea4c2b09f8d25b":
        raise RuntimeError("Round-02 Huashu toolchain/media gate source revision drifted.")
    if source.get("license") != "MIT":
        raise RuntimeError("Round-02 Huashu toolchain/media gate source license drifted.")

    source_reviews = {
        review.get("source_id"): review
        for review in round02_reviews_doc.get("source_reviews", [])
        if isinstance(review, dict)
    }
    huashu_review = source_reviews.get("github:alchaincyf/huashu-design")
    if not huashu_review:
        raise RuntimeError("Round-02 Huashu toolchain/media gate cannot find source review.")
    if huashu_review.get("revision") != source.get("revision"):
        raise RuntimeError("Round-02 Huashu toolchain/media gate revision does not match source review.")
    if huashu_review.get("source_disposition") != "reference-and-adapter-candidate-not-approved":
        raise RuntimeError("Round-02 Huashu source review disposition drifted.")

    permissions = document.get("current_permissions", {})
    if not isinstance(permissions, dict):
        raise RuntimeError("Round-02 Huashu toolchain/media gate permissions are required.")
    for key, value in permissions.items():
        expected = key == "adapted_draft_allowed"
        if value is not expected:
            raise RuntimeError(f"Round-02 Huashu toolchain/media gate permission mismatch: {key}")

    subset = document.get("subset_boundary", {})
    if subset.get("included_candidates") != [
        "huashu-html-deck-animation-pipeline",
        "huashu-voiceover-tts-pipeline",
        "huashu-bundled-assets",
    ]:
        raise RuntimeError("Round-02 Huashu toolchain/media included candidates drifted.")
    if set(subset.get("excluded_candidates", [])) != {"huashu-design-principles", "huashu-brand-asset-protocol"}:
        raise RuntimeError("Round-02 Huashu toolchain/media excluded candidates drifted.")
    if "require separate review" not in str(subset.get("reason", "")):
        raise RuntimeError("Round-02 Huashu toolchain/media subset reason must preserve separate review boundary.")

    inventories = document.get("source_inventories", {})
    if inventories.get("assets") != {
        "root": "assets/",
        "file_count": 104,
        "total_bytes": 31739014,
        "aggregate_sha256": "8480def6729489f40427c5cc0d9b3e72b4cb22723c0230139f6604b2a7022421",
    }:
        raise RuntimeError("Round-02 Huashu toolchain/media assets inventory drifted.")
    if inventories.get("scripts") != {
        "root": "scripts/",
        "file_count": 15,
        "total_bytes": 128933,
    }:
        raise RuntimeError("Round-02 Huashu toolchain/media scripts inventory drifted.")

    expected_drafts = {
        "html-deck-animation-toolchain-boundary": (
            "toolchain-adapter-defer",
            "drafts/round02-huashu-toolchain-media-adaptation/html-deck-animation-toolchain-boundary/DRAFT.md",
            {
                "SKILL.md": "2830077dd711de0cccd4c3c00a840d7b5d69b14ac38446e19826540c99d914ad",
                "assets/deck_stage.js": "fc52ed7529e598b8cba1821418b848e5cbc17cf883bd0cc989a5186f58cd1e84",
                "scripts/export_deck_pdf.mjs": "345079e8d45dd521ce5a4f9bc639300b665069cb455de3e465b0fa29760d3d20",
                "scripts/export_deck_pptx.mjs": "190c86fd96ccc78970e8fef7785dc5d88f0bd0f94ca83837145c6cecc94650ab",
                "scripts/render-video.js": "1b7a2f88dcbffd54e76afe2135b7408c0c661d42d69def92cbc54c1bde6d63a9",
                "package.json": "b6a2c1e71b7072cf1e424b76ac2eefd586a45ac3f3123e7796ecf3af8a6f422d",
            },
        ),
        "voiceover-tts-media-pipeline-boundary": (
            "credential-cost-media-defer",
            "drafts/round02-huashu-toolchain-media-adaptation/voiceover-tts-media-pipeline-boundary/DRAFT.md",
            {
                "references/voiceover-pipeline.md": "c59a1e1391fb71ac9b50de6c1b159ae92ce2ddb2f199a4c5e0bba58c0cb025a0",
                "assets/narration_stage.jsx": "4590b9cb52028164d9bc4a0aed524d1d5f7dcbe78f7ea5d5b68b874b334b3e52",
                "scripts/tts-doubao.mjs": "6eef31f8dd34adf9bf933f088cfdb66a707c1b42ec97260ab3ec96f7b96ff32f",
                "scripts/narrate-pipeline.mjs": "6ac2c629706936033c616120aa5e5ec8e98cb96208065d44384db9f5a8c08466",
                "scripts/render-narration.sh": "c5da68c6affe3ab51dacc8ecba47f9ce5f63ab90577d8c7a10beab30db9429e9",
                ".env.example": "b886b4143441ab93274b9849be6cf1def6d127881d4b6e07ceed66809b921313",
            },
        ),
        "bundled-assets-redistribution-boundary": (
            "do-not-vendor-before-asset-provenance-review",
            "drafts/round02-huashu-toolchain-media-adaptation/bundled-assets-redistribution-boundary/DRAFT.md",
            {
                "assets/": "8480def6729489f40427c5cc0d9b3e72b4cb22723c0230139f6604b2a7022421",
            },
        ),
    }
    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = {
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    }
    drafts = {
        item.get("candidate_id"): item
        for item in document.get("adaptation_drafts", [])
        if isinstance(item, dict)
    }
    if set(drafts) != set(expected_drafts):
        raise RuntimeError("Round-02 Huashu toolchain/media draft ids drifted.")
    for candidate_id, draft in drafts.items():
        expected_disposition, draft_path, expected_sources = expected_drafts[candidate_id]
        if draft.get("disposition") != expected_disposition:
            raise RuntimeError(f"Round-02 Huashu toolchain/media draft disposition drifted: {candidate_id}")
        if draft.get("draft_path") != draft_path:
            raise RuntimeError(f"Round-02 Huashu toolchain/media draft path drifted: {candidate_id}")
        if not (ROOT / draft_path).is_file():
            raise RuntimeError(f"Round-02 Huashu toolchain/media draft path missing: {candidate_id}")
        if draft.get("source_text_copied") or draft.get("source_text_redistributed"):
            raise RuntimeError(f"Round-02 Huashu toolchain/media draft must not copy or redistribute source text: {candidate_id}")
        if candidate_id in approved_directories:
            raise RuntimeError(f"Round-02 Huashu toolchain/media draft unexpectedly approved: {candidate_id}")
        if any(path.startswith(f"skills/{candidate_id}/") for path in manifest_paths):
            raise RuntimeError(f"Round-02 Huashu toolchain/media draft appears in release manifest: {candidate_id}")
        source_candidates = {
            item.get("upstream_path"): item.get("upstream_sha256")
            for item in draft.get("source_candidates", [])
            if isinstance(item, dict)
        }
        if source_candidates != expected_sources:
            raise RuntimeError(f"Round-02 Huashu toolchain/media draft source hashes drifted: {candidate_id}")
        if "separate" not in str(draft.get("next_gate", "")).lower():
            raise RuntimeError(f"Round-02 Huashu toolchain/media draft must require a separate next gate: {candidate_id}")
        if not isinstance(draft.get("likely_targets"), list) or not draft.get("likely_targets"):
            raise RuntimeError(f"Round-02 Huashu toolchain/media draft likely targets missing: {candidate_id}")

    expected_sections = {
        "source_integrity": "pass",
        "license_and_attribution": "pass",
        "security": "bounded_in_drafts",
        "portability_and_neutralization": "bounded_in_drafts",
        "overlap_and_conflict": "toolchain_media_bounded",
        "release_manifest_impact": "no_manifest_change",
        "consumer_install_impact": "no_install_change",
        "next_gate": "separate-release-or-routing-review",
    }
    if document.get("review_sections") != expected_sections:
        raise RuntimeError("Round-02 Huashu toolchain/media gate review sections drifted.")
    required_boundaries = {
        "skills/ unchanged",
        "release-manifest.json unchanged",
        "generated routing projections unchanged",
        "live Agent environments untouched",
        "source text not redistributed",
        "source assets not redistributed",
        "local Codex/agents/cc-switch sync blocked",
        "adaptation drafts are not approved payload",
        "Huashu design guidance remains outside this gate",
    }
    if set(document.get("boundary_assertions", [])) != required_boundaries:
        raise RuntimeError("Round-02 Huashu toolchain/media gate boundary assertions drifted.")

    validation = document.get("validation", {})
    if validation.get("status") not in {"pending_final_run", "passed"}:
        raise RuntimeError("Round-02 Huashu toolchain/media gate validation status is invalid.")
    required_commands = {
        "python -B scripts/verify.py",
        "python -B scripts/build_topology.py --check",
        "python -B scripts/build_release_manifest.py --check",
        "python -B scripts/simulate_routing.py --all",
        "python -B -m unittest discover -s tests -v",
    }
    if set(validation.get("required_commands", [])) != required_commands:
        raise RuntimeError("Round-02 Huashu toolchain/media gate required commands drifted.")
    for assertion in [
        "release-manifest.json remains unchanged",
        "generated routing projections remain unchanged",
        "skills/ remains unchanged",
        "live Agent environments are untouched",
        "source text is not redistributed as approved curated payload",
        "local Codex/agents/cc-switch sync remains blocked",
    ]:
        if assertion not in validation.get("boundary_assertions", []):
            raise RuntimeError(f"Round-02 Huashu toolchain/media gate missing boundary assertion: {assertion}")
    if "Separate approval is required" not in str(document.get("next_required_gate")):
        raise RuntimeError("Round-02 Huashu toolchain/media gate must require a separate next gate.")

    doc_path = document.get("evidence_doc")
    if doc_path != "docs/round02-huashu-toolchain-media-adaptation-gate.md":
        raise RuntimeError("Round-02 Huashu toolchain/media gate evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "Huashu toolchain and media adaptation gate evidence, not release approval",
        "approved payload allowed: false",
        "release manifest allowed: false",
        "routing projection allowed: false",
        "live install allowed: false",
        "local runtime sync allowed: false",
        "It explicitly excludes design-guidance candidates already handled by the separate design guidance gate.",
        "Draft Decisions",
        "Boundary Checks",
        "Next Gate",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"Round-02 Huashu toolchain/media gate doc missing phrase: {phrase}")

    draft_expectations = {
        "drafts/round02-huashu-toolchain-media-adaptation/html-deck-animation-toolchain-boundary/DRAFT.md": [
            "This is an HTML deck and animation toolchain boundary candidate.",
            "Do not install dependencies, run Playwright, start servers, or export files without explicit authorization.",
            "Do not vendor scripts or generated media into approved payload from this gate.",
        ],
        "drafts/round02-huashu-toolchain-media-adaptation/voiceover-tts-media-pipeline-boundary/DRAFT.md": [
            "This is a voiceover, TTS, and media pipeline boundary candidate.",
            "Do not request, store, or use TTS credentials from this draft.",
            "Do not generate or publish audio/video without rights, cost, and user approval.",
        ],
        "drafts/round02-huashu-toolchain-media-adaptation/bundled-assets-redistribution-boundary/DRAFT.md": [
            "This is a bundled-assets redistribution boundary candidate.",
            "Do not redistribute bundled audio, image, demo, or showcase assets before asset-level provenance review.",
            "Do not assume MIT repository license automatically clears every bundled media asset for reuse.",
        ],
    }
    for path, phrases in draft_expectations.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                raise RuntimeError(f"Round-02 Huashu toolchain/media draft missing phrase: {path}/{phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link Round-02 Huashu toolchain/media gate.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link Round-02 Huashu toolchain/media gate.")


def validate_round02_release_readiness_review(
    document: dict[str, object],
    source_intake_batches_doc: dict[str, object],
    round02_reviews_doc: dict[str, object],
    gate_docs: list[dict[str, object]],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if document.get("schema_version") != 1:
        raise RuntimeError("Round-02 release readiness schema_version must be 1.")
    if document.get("status") != "round02_release_readiness_recorded_not_release_approved":
        raise RuntimeError("Round-02 release readiness status mismatch.")
    if document.get("record_id") != "round02-release-readiness-review-2026-07-02":
        raise RuntimeError("Round-02 release readiness record id mismatch.")
    if document.get("scope") != "github-stage-readiness-only":
        raise RuntimeError("Round-02 release readiness scope mismatch.")
    if document.get("source_intake_batch") != "registry/source-intake-batches.json#round02-source-intake-2026-07-02":
        raise RuntimeError("Round-02 release readiness source intake reference mismatch.")
    if document.get("candidate_review_record") != "registry/round02-candidate-reviews.json":
        raise RuntimeError("Round-02 release readiness candidate review reference mismatch.")
    if document.get("round_lifecycle_contract") != "registry/round-lifecycle-contract.json#stageCloseout":
        raise RuntimeError("Round-02 release readiness lifecycle reference mismatch.")
    if document.get("closeout_outcome") != "needs_user_confirmation":
        raise RuntimeError("Round-02 release readiness closeout outcome mismatch.")
    if document.get("release_readiness_conclusion") != "github_stage_ready_for_owner_review_not_release_approved":
        raise RuntimeError("Round-02 release readiness conclusion mismatch.")

    permissions = document.get("current_permissions", {})
    if not isinstance(permissions, dict):
        raise RuntimeError("Round-02 release readiness permissions are required.")
    for key, value in permissions.items():
        expected = key == "release_readiness_review_allowed"
        if value is not expected:
            raise RuntimeError(f"Round-02 release readiness permission mismatch: {key}")

    batches = {
        batch.get("id"): batch
        for batch in source_intake_batches_doc.get("batches", [])
        if isinstance(batch, dict)
    }
    batch = batches.get("round02-source-intake-2026-07-02")
    if not batch:
        raise RuntimeError("Round-02 release readiness cannot find source intake batch.")
    intake_sources = {
        source.get("id"): source
        for source in batch.get("sources", [])
        if isinstance(source, dict)
    }
    expected_source_ids = {
        "github:kepano/obsidian-skills",
        "github:phuryn/pm-skills",
        "github:alchaincyf/huashu-design",
    }
    if set(intake_sources) != expected_source_ids:
        raise RuntimeError("Round-02 release readiness intake source set drifted.")

    source_reviews = {
        review.get("source_id"): review
        for review in round02_reviews_doc.get("source_reviews", [])
        if isinstance(review, dict)
    }
    if set(source_reviews) != expected_source_ids:
        raise RuntimeError("Round-02 release readiness review source set drifted.")
    expected_dispositions = {
        "github:kepano/obsidian-skills": "split-adapt-candidates-not-approved",
        "github:phuryn/pm-skills": "split-into-sub-batches-not-approved",
        "github:alchaincyf/huashu-design": "reference-and-adapter-candidate-not-approved",
    }

    expected_gate_records = [
        "registry/round02-obsidian-adaptation-gate.json",
        "registry/round02-pm-execution-adaptation-gate.json",
        "registry/round02-pm-analytics-adaptation-gate.json",
        "registry/round02-pm-market-discovery-adaptation-gate.json",
        "registry/round02-pm-toolkit-boundary-adaptation-gate.json",
        "registry/round02-huashu-design-guidance-adaptation-gate.json",
        "registry/round02-huashu-toolchain-media-adaptation-gate.json",
    ]
    if document.get("completed_gate_records") != expected_gate_records:
        raise RuntimeError("Round-02 release readiness gate record list drifted.")
    if document.get("processed_source_count") != 3:
        raise RuntimeError("Round-02 release readiness processed source count mismatch.")
    if document.get("completed_gate_count") != len(expected_gate_records):
        raise RuntimeError("Round-02 release readiness completed gate count mismatch.")

    processed_sources = {
        item.get("source_id"): item
        for item in document.get("processed_sources", [])
        if isinstance(item, dict)
    }
    if set(processed_sources) != expected_source_ids:
        raise RuntimeError("Round-02 release readiness processed source set drifted.")
    for source_id, item in processed_sources.items():
        review = source_reviews[source_id]
        if item.get("revision") != review.get("revision") or item.get("revision") != intake_sources[source_id].get("revision"):
            raise RuntimeError(f"Round-02 release readiness source revision mismatch: {source_id}")
        if item.get("source_disposition") != expected_dispositions[source_id]:
            raise RuntimeError(f"Round-02 release readiness source disposition mismatch: {source_id}")
        if item.get("source_disposition") != review.get("source_disposition"):
            raise RuntimeError(f"Round-02 release readiness review disposition mismatch: {source_id}")
        if not item.get("gate_records"):
            raise RuntimeError(f"Round-02 release readiness source gate list missing: {source_id}")

    draft_candidate_ids: set[str] = set()
    for gate_doc in gate_docs:
        validation = gate_doc.get("validation", {})
        if validation.get("status") != "passed":
            raise RuntimeError("Round-02 release readiness requires all gate validations to pass.")
        gate_boundaries = set(gate_doc.get("boundary_assertions", []))
        for required in {
            "skills/ unchanged",
            "release-manifest.json unchanged",
            "generated routing projections unchanged",
            "live Agent environments untouched",
            "source text not redistributed",
            "local Codex/agents/cc-switch sync blocked",
        }:
            if required not in gate_boundaries:
                raise RuntimeError(f"Round-02 release readiness gate missing boundary: {required}")
        for draft in gate_doc.get("adaptation_drafts", []):
            if not isinstance(draft, dict):
                raise RuntimeError("Round-02 release readiness draft records must be objects.")
            candidate_id = draft.get("candidate_id")
            if not isinstance(candidate_id, str) or not candidate_id:
                raise RuntimeError("Round-02 release readiness draft candidate id missing.")
            draft_candidate_ids.add(candidate_id)

    if document.get("draft_candidate_count") != len(draft_candidate_ids) or len(draft_candidate_ids) != 16:
        raise RuntimeError("Round-02 release readiness draft candidate count mismatch.")
    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = {
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    }
    approved_round02_payload_candidate = "obsidian-open-format-knowledge-files"
    for candidate_id in draft_candidate_ids:
        if candidate_id in approved_directories and candidate_id != approved_round02_payload_candidate:
            raise RuntimeError(f"Round-02 draft candidate unexpectedly approved: {candidate_id}")
        if candidate_id != approved_round02_payload_candidate and any(path.startswith(f"skills/{candidate_id}/") for path in manifest_paths):
            raise RuntimeError(f"Round-02 draft candidate appears in release manifest: {candidate_id}")

    expected_acceptance = {
        "plan": "pass",
        "execute": "pass",
        "acceptance": "source_dispositions_recorded_no_release_decision",
        "stageCloseout": "github_stage_ready_needs_owner_confirmation",
    }
    acceptance = {
        item.get("phase"): item.get("status")
        for item in document.get("acceptance_mapping", [])
        if isinstance(item, dict)
    }
    if acceptance != expected_acceptance:
        raise RuntimeError("Round-02 release readiness acceptance mapping drifted.")

    required_boundaries = {
        "skills/ unchanged",
        "release-manifest.json unchanged",
        "generated routing projections unchanged",
        "live Agent environments untouched",
        "source text not redistributed",
        "source assets not redistributed",
        "approved payload admission blocked",
        "local Codex/agents/cc-switch sync blocked",
        "round-02 drafts are not approved payload",
        "next gate requires owner approval",
    }
    if set(document.get("boundary_assertions", [])) != required_boundaries:
        raise RuntimeError("Round-02 release readiness boundary assertions drifted.")

    validation = document.get("validation", {})
    if validation.get("status") not in {"pending_final_run", "passed"}:
        raise RuntimeError("Round-02 release readiness validation status is invalid.")
    required_commands = {
        "python -B scripts/verify.py",
        "python -B scripts/build_topology.py --check",
        "python -B scripts/build_release_manifest.py --check",
        "python -B scripts/simulate_routing.py --all",
        "python -B -m unittest discover -s tests -v",
    }
    if set(validation.get("required_commands", [])) != required_commands:
        raise RuntimeError("Round-02 release readiness required commands drifted.")
    for assertion in [
        "release-manifest.json remains unchanged",
        "generated routing projections remain unchanged",
        "skills/ remains unchanged",
        "live Agent environments are untouched",
        "source text is not redistributed as approved curated payload",
        "local Codex/agents/cc-switch sync remains blocked",
    ]:
        if assertion not in validation.get("boundary_assertions", []):
            raise RuntimeError(f"Round-02 release readiness missing validation boundary: {assertion}")
    if "Owner approval is required" not in str(document.get("next_required_gate", "")):
        raise RuntimeError("Round-02 release readiness must require owner approval as next gate.")

    doc_path = document.get("evidence_doc")
    if doc_path != "docs/round02-release-readiness-review.md":
        raise RuntimeError("Round-02 release readiness evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "Round-02 GitHub-stage release readiness review, not release approval",
        "closeout outcome: needs_user_confirmation",
        "approved payload allowed: false",
        "release manifest allowed: false",
        "routing projection allowed: false",
        "local runtime sync allowed: false",
        "completed gate records: 7",
        "No candidate entered `skills/`",
        "Local Codex/agents/cc Switch alignment remains blocked",
        "Next Gate",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"Round-02 release readiness doc missing phrase: {phrase}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link Round-02 release readiness review.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link Round-02 release readiness review.")


def validate_round02_release_admission_review_template(
    template_doc: dict[str, object],
    readiness_doc: dict[str, object],
    gate_docs: list[dict[str, object]],
) -> None:
    if template_doc.get("schema_version") != 1:
        raise RuntimeError("Round-02 release/admission review template schema_version must be 1.")
    if template_doc.get("id") != "round02-release-admission-review-template-2026-07-02":
        raise RuntimeError("Round-02 release/admission review template id mismatch.")
    if template_doc.get("status") != "template_only_not_candidate_decision":
        raise RuntimeError("Round-02 release/admission review template must remain template-only.")
    if template_doc.get("not_approval") is not True:
        raise RuntimeError("Round-02 release/admission review template must explicitly avoid approval.")
    if template_doc.get("approval_required_before_use") is not True:
        raise RuntimeError("Round-02 release/admission review template must require approval before use.")
    if template_doc.get("source_readiness_record") != "registry/round02-release-readiness-review.json":
        raise RuntimeError("Round-02 release/admission review template must reference readiness review.")
    if template_doc.get("source_approval_request") != "registry/round02-release-admission-approval-request.json":
        raise RuntimeError("Round-02 release/admission review template must reference approval request.")
    if readiness_doc.get("release_readiness_conclusion") != "github_stage_ready_for_owner_review_not_release_approved":
        raise RuntimeError("Round-02 release/admission review template expects readiness-only state.")

    candidate_ids: list[str] = []
    for gate_doc in gate_docs:
        for draft in gate_doc.get("adaptation_drafts", []):
            if isinstance(draft, dict) and isinstance(draft.get("candidate_id"), str):
                candidate_ids.append(draft["candidate_id"])
    expected_candidate_ids = [
        "obsidian-open-format-knowledge-files",
        "obsidian-cli-runtime-adapter",
        "defuddle-tool-adapter",
        "ai-shipping-governance",
        "product-execution-documents",
        "data-analytics-runtime-equivalence",
        "synthetic-data-and-sql-tooling",
        "market-strategy-evidence-boundary",
        "product-discovery-research-planning",
        "legal-privacy-document-boundary",
        "personal-document-and-copyediting-boundary",
        "design-direction-and-anti-slop-reference",
        "brand-asset-provenance-protocol",
        "html-deck-animation-toolchain-boundary",
        "voiceover-tts-media-pipeline-boundary",
        "bundled-assets-redistribution-boundary",
    ]
    if template_doc.get("candidate_ids") != expected_candidate_ids:
        raise RuntimeError("Round-02 release/admission review template candidate id order drifted.")
    if set(candidate_ids) != set(expected_candidate_ids):
        raise RuntimeError("Round-02 release/admission review template candidates must match gate drafts.")
    if template_doc.get("candidate_count") != len(expected_candidate_ids):
        raise RuntimeError("Round-02 release/admission review template candidate count mismatch.")
    if readiness_doc.get("draft_candidate_count") != len(expected_candidate_ids):
        raise RuntimeError("Round-02 release/admission review template must match readiness candidate count.")

    allowed_decisions = [
        "proposed-approved-payload",
        "merge-into-existing-approved-skill",
        "recipe-only",
        "adapter-only",
        "reference-only",
        "reject",
    ]
    if template_doc.get("allowed_decisions_after_approval") != allowed_decisions:
        raise RuntimeError("Round-02 release/admission review template decision enum changed.")
    required_sections = [
        "source_integrity",
        "license_and_attribution",
        "security",
        "portability_and_neutralization",
        "overlap_and_conflict",
        "native_or_runtime_equivalence",
        "routing_semantics",
        "release_manifest_impact",
        "consumer_install_impact",
        "source_text_redistribution_boundary",
        "source_asset_redistribution_boundary",
        "dependency_credential_and_media_boundary",
        "validation_plan",
        "rejected_alternatives",
        "next_gate",
    ]
    if template_doc.get("required_review_sections") != required_sections:
        raise RuntimeError("Round-02 release/admission review template sections changed.")

    decision_rules = template_doc.get("decision_rules", [])
    if {item.get("decision") for item in decision_rules if isinstance(item, dict)} != set(allowed_decisions):
        raise RuntimeError("Round-02 release/admission review template must define every allowed decision.")
    for item in decision_rules:
        if not isinstance(item, dict) or not item.get("requires"):
            raise RuntimeError(f"Round-02 decision rule missing requirements: {getattr(item, 'get', lambda _key: None)('decision')}")

    required_fail_closed = {
        "owner approval for Round-02 release/admission review is missing",
        "candidate source revision or upstream hash differs from Round-02 gate evidence",
        "license, provenance, attribution, source-text redistribution, or source-asset redistribution posture is unclear",
        "security, portability, overlap, native/runtime equivalence, or routing review is incomplete",
        "candidate would override repository, runtime, user, domain, legal, security, privacy, or human authority",
        "candidate would enter skills/, release-manifest.json, generated routing, publication, local runtime sync, or live environment before its later specific gate",
        "candidate would install dependencies, use credentials, call TTS providers, generate external media, or write files without explicit later authorization",
        "candidate decision is based only on enthusiasm, source popularity, broad usefulness, or coverage pressure without evidence",
    }
    if set(template_doc.get("fail_closed_conditions", [])) != required_fail_closed:
        raise RuntimeError("Round-02 release/admission review template fail-closed conditions changed.")

    permissions = template_doc.get("current_permissions", {})
    if not isinstance(permissions, dict):
        raise RuntimeError("Round-02 release/admission review template permissions are required.")
    for key, value in permissions.items():
        expected = key == "template_allowed"
        if value is not expected:
            raise RuntimeError(f"Round-02 release/admission review template permission mismatch: {key}")

    output_contract = template_doc.get("output_contract_after_approval", {})
    required_output = {
        "decision",
        "rationale",
        "evidence",
        "rejected_alternatives",
        "overlap_handling",
        "security_boundary",
        "portability_boundary",
        "source_text_boundary",
        "source_asset_boundary",
        "dependency_credential_and_media_boundary",
        "boundary_assertions",
        "validation_results",
        "next_gate",
    }
    if set(output_contract.get("must_include", [])) != required_output:
        raise RuntimeError("Round-02 release/admission review template output contract changed.")
    if output_contract.get("record_id") != "round02-release-admission-candidate-review-YYYY-MM-DD":
        raise RuntimeError("Round-02 release/admission review template output record id mismatch.")
    if "candidate_decisions" not in output_contract:
        raise RuntimeError("Round-02 release/admission review template must define candidate_decisions output.")

    doc_path = template_doc.get("evidence_doc")
    if doc_path != "docs/round02-release-admission-review-template.md":
        raise RuntimeError("Round-02 release/admission review template evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "Template only, not approval.",
        "Without that approval, this document remains scaffolding.",
        "Allowed decisions after approval",
        "does not by itself mutate `skills/`, `release-manifest.json`, generated",
        "Fail-closed conditions",
        "Output contract after approval",
        "Until that record exists and passes verification, Round-02 remains",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"Round-02 release/admission review template doc missing phrase: {phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link Round-02 release/admission review template.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link Round-02 release/admission review template.")


def validate_round02_release_admission_approval_request(
    request_doc: dict[str, object],
    readiness_doc: dict[str, object],
    template_doc: dict[str, object],
) -> None:
    if request_doc.get("schema_version") != 1:
        raise RuntimeError("Round-02 release/admission approval request schema_version must be 1.")
    if request_doc.get("id") != "round02-release-admission-review-approval-request-2026-07-02":
        raise RuntimeError("Round-02 release/admission approval request id mismatch.")
    if request_doc.get("status") != "owner_approval_recorded_for_round02_release_admission_review":
        raise RuntimeError("Round-02 release/admission approval request status mismatch.")
    if request_doc.get("not_approval") is not True:
        raise RuntimeError("Round-02 release/admission approval request must remain a request record, not the event.")
    if request_doc.get("approval_recorded") is not True:
        raise RuntimeError("Round-02 release/admission approval request must record the consumed approval state.")
    if request_doc.get("approval_event_record") != "registry/round02-release-admission-approval-events.json":
        raise RuntimeError("Round-02 release/admission approval request must reference the approval event record.")
    if request_doc.get("source_readiness_record") != "registry/round02-release-readiness-review.json":
        raise RuntimeError("Round-02 release/admission approval request must reference readiness review.")
    if request_doc.get("review_template") != "registry/round02-release-admission-review-template.json":
        raise RuntimeError("Round-02 release/admission approval request must reference review template.")
    if template_doc.get("source_approval_request") != "registry/round02-release-admission-approval-request.json":
        raise RuntimeError("Round-02 release/admission review template must point back to approval request.")
    if readiness_doc.get("closeout_outcome") != "needs_user_confirmation":
        raise RuntimeError("Round-02 release/admission approval request expects readiness to need user confirmation.")

    expected_sources = {
        item.get("source_id")
        for item in readiness_doc.get("processed_sources", [])
        if isinstance(item, dict)
    }
    if set(request_doc.get("source_ids", [])) != expected_sources:
        raise RuntimeError("Round-02 release/admission approval request source ids drifted.")
    if request_doc.get("gate_records") != readiness_doc.get("completed_gate_records"):
        raise RuntimeError("Round-02 release/admission approval request gate records must match readiness review.")

    permissions = request_doc.get("current_permissions", {})
    if not isinstance(permissions, dict):
        raise RuntimeError("Round-02 release/admission approval request permissions are required.")
    for key, value in permissions.items():
        expected = key in {
            "approval_request_allowed",
            "release_admission_review_allowed",
        }
        if value is not expected:
            raise RuntimeError(f"Round-02 release/admission approval request permission mismatch: {key}")

    required_requested_scope = {
        "enter Round-02 release/admission review for the 16 recorded draft candidates",
        "decide per candidate whether it is rejected, reference-only, adapter-only, recipe-only, merged into an existing approved Skill, or proposed as approved payload",
        "record rationale, evidence, rejected alternatives, overlap handling, security boundaries, portability boundaries, validation results, and next gate for each candidate",
        "keep any approved payload diff, release manifest update, generated routing projection update, publication, live install, and local runtime sync behind separate follow-up approval unless explicitly approved later",
    }
    if set(request_doc.get("requested_scope_if_approved", [])) != required_requested_scope:
        raise RuntimeError("Round-02 release/admission approval request requested scope changed.")

    required_disallowed = {
        "edit skills/",
        "update release-manifest.json",
        "update generated routing projections",
        "install or sync live Agent environments",
        "approve, release, or publish any candidate payload",
        "redistribute upstream source text as approved curated payload",
        "redistribute upstream source assets as approved curated payload",
        "install dependencies, use credentials, call TTS providers, or generate external media",
    }
    if set(request_doc.get("explicitly_not_requested", [])) != required_disallowed:
        raise RuntimeError("Round-02 release/admission approval request explicitly_not_requested changed.")
    if set(request_doc.get("still_disallowed", [])) != required_disallowed:
        raise RuntimeError("Round-02 release/admission approval request still_disallowed changed.")
    if request_doc.get("safe_approval_phrases") != [
        "批准进入 Round-02 release/admission 审查阶段",
        "Approve Round-02 release/admission review only",
    ]:
        raise RuntimeError("Round-02 release/admission approval request safe approval phrases changed.")
    if request_doc.get("next_state_if_approved") != "round02_release_admission_review":
        raise RuntimeError("Round-02 release/admission approval request next state mismatch.")

    required_next_evidence = {
        "owner approval event record",
        "candidate-specific release/admission disposition record",
        "rationale for reject, reference-only, adapter-only, recipe-only, merge, or proposed approved payload",
        "explicit record of overlap, security, portability, license, source-text, asset, dependency, credential, and media boundaries",
        "verification command results",
        "explicit record that live install, local runtime sync, publication, source redistribution, and asset redistribution remain unchanged unless separately approved",
    }
    if set(request_doc.get("next_required_evidence_if_approved", [])) != required_next_evidence:
        raise RuntimeError("Round-02 release/admission approval request next required evidence changed.")

    doc_path = request_doc.get("evidence_doc")
    if doc_path != "docs/round02-release-admission-approval-request.md":
        raise RuntimeError("Round-02 release/admission approval request evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "This is an approval request record, not the approval event itself.",
        "approval recorded: true",
        "release/admission review allowed: true",
        "Requested Approval",
        "批准进入 Round-02 release/admission 审查阶段",
        "Approve Round-02 release/admission review only",
        "Explicitly Not Requested",
        "The approval event now exists, so Round-02 may enter release/admission review.",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"Round-02 release/admission approval request doc missing phrase: {phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link Round-02 release/admission approval request.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link Round-02 release/admission approval request.")


def validate_round02_release_admission_approval_events(
    events_doc: dict[str, object],
    request_doc: dict[str, object],
) -> None:
    if events_doc.get("schema_version") != 1:
        raise RuntimeError("Round-02 release/admission approval events schema_version must be 1.")
    if events_doc.get("status") != "owner_approval_recorded_for_round02_release_admission_review":
        raise RuntimeError("Round-02 release/admission approval events status mismatch.")
    expected_permissions = {
        "approval_recorded": True,
        "release_admission_review_allowed": True,
        "candidate_decision_allowed": True,
        "approved_payload_allowed": False,
        "release_manifest_allowed": False,
        "routing_projection_allowed": False,
        "live_install_allowed": False,
        "local_runtime_sync_allowed": False,
        "source_text_redistribution_allowed": False,
        "source_asset_redistribution_allowed": False,
        "dependency_install_allowed": False,
        "credential_use_allowed": False,
        "external_media_generation_allowed": False,
    }
    for key, expected in expected_permissions.items():
        if events_doc.get(key) is not expected:
            raise RuntimeError(f"Round-02 release/admission approval event permission mismatch: {key}")

    events = events_doc.get("events", [])
    if not isinstance(events, list) or len(events) != 1 or not isinstance(events[0], dict):
        raise RuntimeError("Round-02 release/admission approval events must contain exactly one event.")
    event = events[0]
    if event.get("id") != "round02-owner-approval-2026-07-02-release-admission-review":
        raise RuntimeError("Round-02 release/admission approval event id mismatch.")
    if event.get("date") != "2026-07-02":
        raise RuntimeError("Round-02 release/admission approval event date mismatch.")
    if event.get("approval_phrase") != "批准进入 Round-02 release/admission 审查阶段":
        raise RuntimeError("Round-02 release/admission approval event phrase mismatch.")
    if event.get("approval_request_id") != request_doc.get("id"):
        raise RuntimeError("Round-02 release/admission approval event must reference the request id.")
    if event.get("next_state") != "round02_release_admission_review":
        raise RuntimeError("Round-02 release/admission approval event next state mismatch.")

    required_scope = {
        "enter Round-02 release/admission review for the 16 recorded draft candidates",
        "apply the Round-02 release/admission review template to record a decision for each candidate",
        "decide per candidate whether it is rejected, reference-only, adapter-only, recipe-only, merged into an existing approved Skill, or proposed as approved payload",
        "record rationale, evidence, rejected alternatives, overlap handling, security boundaries, portability boundaries, validation results, and next gate for each candidate",
    }
    if set(event.get("approved_scope", [])) != required_scope:
        raise RuntimeError("Round-02 release/admission approval event scope changed.")
    required_not_approved = {
        "edit skills/",
        "update release-manifest.json",
        "update generated routing projections",
        "install or sync live Agent environments",
        "approve, release, or publish any candidate payload",
        "redistribute upstream source text as approved curated payload",
        "redistribute upstream source assets as approved curated payload",
        "install dependencies, use credentials, call TTS providers, or generate external media",
    }
    if set(event.get("explicitly_not_approved", [])) != required_not_approved:
        raise RuntimeError("Round-02 release/admission approval event forbidden scope changed.")


def validate_round02_release_admission_candidate_review(
    review_doc: dict[str, object],
    approval_events_doc: dict[str, object],
    readiness_doc: dict[str, object],
    template_doc: dict[str, object],
    gate_docs: list[dict[str, object]],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if review_doc.get("schema_version") != 1:
        raise RuntimeError("Round-02 release/admission candidate review schema_version must be 1.")
    if review_doc.get("status") != "release_admission_candidate_review_recorded_not_release_approved":
        raise RuntimeError("Round-02 release/admission candidate review status mismatch.")
    if review_doc.get("review_id") != "round02-release-admission-candidate-review-2026-07-02":
        raise RuntimeError("Round-02 release/admission candidate review id mismatch.")
    if review_doc.get("approval_request_id") != "round02-release-admission-review-approval-request-2026-07-02":
        raise RuntimeError("Round-02 release/admission candidate review request id mismatch.")
    if review_doc.get("source_readiness_record") != "registry/round02-release-readiness-review.json":
        raise RuntimeError("Round-02 release/admission candidate review must reference readiness.")
    if review_doc.get("review_template") != "registry/round02-release-admission-review-template.json":
        raise RuntimeError("Round-02 release/admission candidate review must reference template.")

    event_ids = {
        event.get("id")
        for event in approval_events_doc.get("events", [])
        if isinstance(event, dict)
    }
    if review_doc.get("approval_event_id") not in event_ids:
        raise RuntimeError("Round-02 release/admission candidate review must reference a recorded approval event.")

    candidate_ids = review_doc.get("candidate_ids", [])
    if candidate_ids != template_doc.get("candidate_ids"):
        raise RuntimeError("Round-02 release/admission candidate ids must match the review template.")
    if len(candidate_ids) != readiness_doc.get("draft_candidate_count"):
        raise RuntimeError("Round-02 release/admission candidate count must match readiness.")
    draft_ids: set[str] = set()
    for gate_doc in gate_docs:
        for draft in gate_doc.get("adaptation_drafts", []):
            if isinstance(draft, dict) and isinstance(draft.get("candidate_id"), str):
                draft_ids.add(draft["candidate_id"])
    if set(candidate_ids) != draft_ids:
        raise RuntimeError("Round-02 release/admission candidate ids must match gate drafts.")

    permissions = review_doc.get("current_permissions", {})
    if not isinstance(permissions, dict):
        raise RuntimeError("Round-02 release/admission candidate review permissions are required.")
    for key, value in permissions.items():
        expected = key in {
            "release_admission_review_allowed",
            "candidate_decision_allowed",
        }
        if value is not expected:
            raise RuntimeError(f"Round-02 release/admission candidate review permission mismatch: {key}")

    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = {
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    }
    routing_text = (ROOT / "registry/routing.json").read_text(encoding="utf-8")
    decisions = {
        item.get("candidate_id"): item
        for item in review_doc.get("candidate_decisions", [])
        if isinstance(item, dict)
    }
    if set(decisions) != set(candidate_ids):
        raise RuntimeError("Round-02 release/admission review must contain one decision per candidate.")

    expected_decisions = {
        "obsidian-open-format-knowledge-files": "proposed-approved-payload",
        "obsidian-cli-runtime-adapter": "adapter-only",
        "defuddle-tool-adapter": "adapter-only",
        "ai-shipping-governance": "merge-into-existing-approved-skill",
        "product-execution-documents": "merge-into-existing-approved-skill",
        "data-analytics-runtime-equivalence": "reference-only",
        "synthetic-data-and-sql-tooling": "adapter-only",
        "market-strategy-evidence-boundary": "reference-only",
        "product-discovery-research-planning": "merge-into-existing-approved-skill",
        "legal-privacy-document-boundary": "reference-only",
        "personal-document-and-copyediting-boundary": "merge-into-existing-approved-skill",
        "design-direction-and-anti-slop-reference": "merge-into-existing-approved-skill",
        "brand-asset-provenance-protocol": "merge-into-existing-approved-skill",
        "html-deck-animation-toolchain-boundary": "adapter-only",
        "voiceover-tts-media-pipeline-boundary": "adapter-only",
        "bundled-assets-redistribution-boundary": "reject",
    }
    allowed_decisions = set(template_doc.get("allowed_decisions_after_approval", []))
    required_sections = set(template_doc.get("required_review_sections", []))
    required_output_fields = set(
        template_doc.get("output_contract_after_approval", {}).get("must_include", [])
    )
    required_boundaries = {
        "skills/ unchanged",
        "release-manifest.json unchanged",
        "generated routing projections unchanged",
        "live Agent environments untouched",
        "local Codex/agents/cc-switch sync blocked",
        "source text not redistributed",
        "source assets not redistributed",
        "candidate decision is not approved payload",
    }
    approved_round02_payload_candidate = "obsidian-open-format-knowledge-files"
    for candidate_id, decision in decisions.items():
        if candidate_id == approved_round02_payload_candidate:
            if candidate_id not in approved_directories:
                raise RuntimeError(f"Round-02 approved payload candidate missing from approved skills: {candidate_id}")
            if f"skills/{candidate_id}/SKILL.md" not in manifest_paths:
                raise RuntimeError(f"Round-02 approved payload candidate missing from release manifest: {candidate_id}")
        elif candidate_id in approved_directories:
            raise RuntimeError(f"Round-02 candidate unexpectedly appears in approved skills: {candidate_id}")
        if candidate_id != approved_round02_payload_candidate and f"skills/{candidate_id}/" in manifest_paths:
            raise RuntimeError(f"Round-02 candidate appears in release manifest: {candidate_id}")
        if candidate_id != approved_round02_payload_candidate and candidate_id in routing_text:
            raise RuntimeError(f"Round-02 candidate appears as a direct routing surface: {candidate_id}")
        if decision.get("decision") != expected_decisions[candidate_id]:
            raise RuntimeError(f"Round-02 candidate decision mismatch: {candidate_id}")
        if decision.get("decision") not in allowed_decisions:
            raise RuntimeError(f"Round-02 candidate decision is outside template enum: {candidate_id}")
        for field in required_output_fields:
            if field not in decision:
                raise RuntimeError(f"Round-02 candidate output field missing: {candidate_id}/{field}")
        if not decision.get("rationale"):
            raise RuntimeError(f"Round-02 candidate rationale missing: {candidate_id}")
        if not decision.get("rejected_alternatives"):
            raise RuntimeError(f"Round-02 candidate rejected alternatives missing: {candidate_id}")
        next_gate = str(decision.get("next_gate", "")).lower()
        if "separate" not in next_gate and decision.get("decision") != "reject":
            raise RuntimeError(f"Round-02 candidate must require a separate next gate: {candidate_id}")
        if decision.get("decision") == "reject" and "future" not in next_gate:
            raise RuntimeError(f"Round-02 rejected candidate must record future reconsideration boundary: {candidate_id}")
        if set(decision.get("boundary_assertions", [])) != required_boundaries:
            raise RuntimeError(f"Round-02 candidate boundary assertions mismatch: {candidate_id}")

        review_sections = decision.get("review_sections", {})
        if set(review_sections) != required_sections:
            raise RuntimeError(f"Round-02 candidate review sections mismatch: {candidate_id}")
        for field in [
            "source_integrity",
            "license_and_attribution",
            "security",
            "portability_and_neutralization",
            "overlap_and_conflict",
            "native_or_runtime_equivalence",
            "routing_semantics",
        ]:
            if review_sections.get(field) != "pass":
                raise RuntimeError(f"Round-02 candidate review section did not pass: {candidate_id}/{field}")
        if review_sections.get("release_manifest_impact") != "no_manifest_change":
            raise RuntimeError(f"Round-02 candidate manifest impact mismatch: {candidate_id}")
        if review_sections.get("consumer_install_impact") != "no_install_change":
            raise RuntimeError(f"Round-02 candidate install impact mismatch: {candidate_id}")
        if review_sections.get("source_text_redistribution_boundary") != "no_source_text_redistributed":
            raise RuntimeError(f"Round-02 candidate source text boundary mismatch: {candidate_id}")
        if review_sections.get("source_asset_redistribution_boundary") != "no_source_assets_redistributed":
            raise RuntimeError(f"Round-02 candidate source asset boundary mismatch: {candidate_id}")
        if review_sections.get("dependency_credential_and_media_boundary") != "no_dependency_credential_or_media_action":
            raise RuntimeError(f"Round-02 candidate dependency/media boundary mismatch: {candidate_id}")
        if review_sections.get("validation_plan") not in {"pending_final_run", "passed"}:
            raise RuntimeError(f"Round-02 candidate validation plan mismatch: {candidate_id}")
        if review_sections.get("rejected_alternatives") != "recorded":
            raise RuntimeError(f"Round-02 candidate rejected alternatives section mismatch: {candidate_id}")
        for evidence_path in decision.get("evidence", []):
            if not isinstance(evidence_path, str) or not (ROOT / evidence_path).is_file():
                raise RuntimeError(f"Round-02 candidate has dead evidence ref: {candidate_id}/{evidence_path}")
        validation_results = decision.get("validation_results", [])
        if not validation_results:
            raise RuntimeError(f"Round-02 candidate validation results missing: {candidate_id}")
        commands = {
            item.get("command")
            for item in validation_results
            if isinstance(item, dict)
        }
        if "python -B scripts/verify.py" not in commands:
            raise RuntimeError(f"Round-02 candidate must record verify.py validation: {candidate_id}")

    validation = review_doc.get("validation", {})
    if validation.get("status") not in {"pending_final_run", "passed"}:
        raise RuntimeError("Round-02 release/admission candidate review validation status is invalid.")
    required_commands = {
        "python -B scripts/verify.py",
        "python -B scripts/build_release_manifest.py --check",
        "python -B scripts/build_topology.py --check",
        "python -B scripts/simulate_routing.py --all",
        "python -B -m unittest discover -s tests -v",
    }
    if set(validation.get("required_commands", [])) != required_commands:
        raise RuntimeError("Round-02 release/admission candidate review required commands drifted.")
    for assertion in [
        "release-manifest.json remains unchanged",
        "generated routing projections remain unchanged",
        "skills/ remains unchanged",
        "live Agent environments are untouched",
        "source text is not redistributed as approved curated payload",
        "source assets are not redistributed as approved curated payload",
        "local Codex/agents/cc-switch sync remains blocked",
    ]:
        if assertion not in validation.get("boundary_assertions", []):
            raise RuntimeError(f"Round-02 candidate review missing boundary assertion: {assertion}")
    if "Separate approval is required" not in str(review_doc.get("next_required_gate")):
        raise RuntimeError("Round-02 release/admission candidate review must record a separate next gate.")

    doc_path = review_doc.get("evidence_doc")
    if doc_path != "docs/round02-release-admission-candidate-review.md":
        raise RuntimeError("Round-02 release/admission candidate review evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "release/admission candidate review evidence, not release approval",
        "approval phrase: 批准进入 Round-02 release/admission 审查阶段",
        "candidate decision allowed: true",
        "approved payload allowed: false",
        "source asset redistribution allowed: false",
        "Candidate Decisions",
        "Rejected Alternatives",
        "Boundary Checks",
        "Next Gates",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"Round-02 release/admission candidate review doc missing phrase: {phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link Round-02 release/admission candidate review.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link Round-02 release/admission candidate review.")


def validate_round02_approved_payload_routing_proposal_template(
    template_doc: dict[str, object],
    candidate_review_doc: dict[str, object],
) -> None:
    if template_doc.get("schema_version") != 1:
        raise RuntimeError("Round-02 approved-payload/routing template schema_version must be 1.")
    if template_doc.get("id") != "round02-approved-payload-routing-proposal-template-2026-07-02":
        raise RuntimeError("Round-02 approved-payload/routing template id mismatch.")
    if template_doc.get("status") != "template_only_not_execution":
        raise RuntimeError("Round-02 approved-payload/routing template must remain template-only.")
    if template_doc.get("not_approval") is not True:
        raise RuntimeError("Round-02 approved-payload/routing template must explicitly avoid approval.")
    if template_doc.get("approval_required_before_use") is not True:
        raise RuntimeError("Round-02 approved-payload/routing template must require approval before use.")
    if template_doc.get("source_candidate_review") != "registry/round02-release-admission-candidate-review.json":
        raise RuntimeError("Round-02 approved-payload/routing template must reference candidate review.")
    if template_doc.get("source_approval_request") != "registry/round02-release-execution-approval-request.json":
        raise RuntimeError("Round-02 approved-payload/routing template must reference approval request.")

    decisions = {
        item.get("candidate_id"): item.get("decision")
        for item in candidate_review_doc.get("candidate_decisions", [])
        if isinstance(item, dict)
    }
    expected_included = [
        "obsidian-open-format-knowledge-files",
        "ai-shipping-governance",
        "product-execution-documents",
        "product-discovery-research-planning",
        "personal-document-and-copyediting-boundary",
        "design-direction-and-anti-slop-reference",
        "brand-asset-provenance-protocol",
    ]
    expected_excluded = [
        "obsidian-cli-runtime-adapter",
        "defuddle-tool-adapter",
        "data-analytics-runtime-equivalence",
        "synthetic-data-and-sql-tooling",
        "market-strategy-evidence-boundary",
        "legal-privacy-document-boundary",
        "html-deck-animation-toolchain-boundary",
        "voiceover-tts-media-pipeline-boundary",
        "bundled-assets-redistribution-boundary",
    ]
    if template_doc.get("included_candidate_ids") != expected_included:
        raise RuntimeError("Round-02 approved-payload/routing template included candidates drifted.")
    if template_doc.get("excluded_candidate_ids") != expected_excluded:
        raise RuntimeError("Round-02 approved-payload/routing template excluded candidates drifted.")
    for candidate_id in expected_included:
        if decisions.get(candidate_id) not in {
            "proposed-approved-payload",
            "merge-into-existing-approved-skill",
        }:
            raise RuntimeError(f"Round-02 template included non-release candidate: {candidate_id}")
    for candidate_id in expected_excluded:
        if decisions.get(candidate_id) in {
            "proposed-approved-payload",
            "merge-into-existing-approved-skill",
        }:
            raise RuntimeError(f"Round-02 template excluded release candidate: {candidate_id}")

    allowed_changes = {
        "create or update source-text-neutral approved Skill body text for obsidian-open-format-knowledge-files",
        "merge bounded improvements into existing approved Skill bodies for the 6 merge candidates",
        "update governed registries only where required by the approved payload or merge proposal",
        "rebuild release-manifest.json only after approved payload changes exist",
        "rebuild deterministic generated projections only from governed registry inputs",
        "record validation and boundary evidence in a dedicated execution record",
    }
    if set(template_doc.get("allowed_changes_after_approval", [])) != allowed_changes:
        raise RuntimeError("Round-02 approved-payload/routing template allowed changes drifted.")
    required_sections = [
        "approval_event",
        "candidate_scope",
        "payload_diff",
        "merge_diff",
        "registry_diff",
        "release_manifest_diff",
        "generated_projection_diff",
        "excluded_candidate_boundary",
        "source_text_boundary",
        "source_asset_boundary",
        "dependency_credential_and_media_boundary",
        "local_runtime_sync_boundary",
        "validation_results",
        "next_gate",
    ]
    if template_doc.get("required_execution_sections") != required_sections:
        raise RuntimeError("Round-02 approved-payload/routing template sections changed.")
    required_exclusions = {
        "adapter-only candidates",
        "reference-only candidates",
        "rejected candidates",
        "live Agent environment install or sync",
        r"writes to C:\Users\15521\.codex\skills",
        r"writes to C:\Users\15521\.agents\skills",
        r"writes to C:\Users\15521\.cc-switch\skills",
        "source text redistribution as approved curated payload",
        "source asset redistribution as approved curated payload",
        "dependency installation",
        "credential use",
        "external media generation",
    }
    if set(template_doc.get("must_remain_excluded", [])) != required_exclusions:
        raise RuntimeError("Round-02 approved-payload/routing template exclusions changed.")
    required_fail_closed = {
        "owner approval for Round-02 approved-payload/routing proposal is missing",
        "included or excluded candidate set differs from the approval request",
        "a proposed Skill body copies upstream source text instead of using source-text-neutral adaptation",
        "a merge diff creates conflicting triggers, duplicate workflow authority, or hidden runtime dependencies",
        "a registry, manifest, or generated projection update is not explained by a bounded payload or merge diff",
        "an adapter-only, reference-only, or rejected candidate enters approved payload, manifest, routing, generated projection, publication, live install, or local sync",
        "source assets are copied, vendored, or redistributed",
        "dependencies are installed, credentials are used, TTS providers are called, or external media is generated",
        "local Codex, agents, or cc-switch directories are modified before a separate local runtime sync gate",
        "validation commands are missing or fail",
    }
    if set(template_doc.get("fail_closed_conditions", [])) != required_fail_closed:
        raise RuntimeError("Round-02 approved-payload/routing template fail-closed conditions changed.")

    permissions = template_doc.get("current_permissions", {})
    if not isinstance(permissions, dict):
        raise RuntimeError("Round-02 approved-payload/routing template permissions are required.")
    for key, value in permissions.items():
        expected = key == "template_allowed"
        if value is not expected:
            raise RuntimeError(f"Round-02 approved-payload/routing template permission mismatch: {key}")

    output_contract = template_doc.get("output_contract_after_approval", {})
    required_output = {
        "approval_event_id",
        "candidate_id",
        "execution_type",
        "target_files",
        "rationale",
        "diff_summary",
        "rejected_alternatives",
        "boundary_assertions",
        "validation_results",
        "next_gate",
    }
    if set(output_contract.get("must_include", [])) != required_output:
        raise RuntimeError("Round-02 approved-payload/routing template output contract changed.")
    if output_contract.get("record_id") != "round02-approved-payload-routing-proposal-YYYY-MM-DD":
        raise RuntimeError("Round-02 approved-payload/routing template output record id mismatch.")
    if "candidate_executions" not in output_contract:
        raise RuntimeError("Round-02 approved-payload/routing template must define candidate_executions output.")

    doc_path = template_doc.get("evidence_doc")
    if doc_path != "docs/round02-approved-payload-routing-proposal-template.md":
        raise RuntimeError("Round-02 approved-payload/routing template evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "Template only, not approval.",
        "Without that approval, this document remains scaffolding.",
        "Included Candidates",
        "Excluded Candidates",
        "Required Execution Sections",
        "Fail-Closed Conditions",
        "Output Contract After Approval",
        "Until that record exists and passes verification, Round-02 remains",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"Round-02 approved-payload/routing template doc missing phrase: {phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link Round-02 approved-payload/routing template.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link Round-02 approved-payload/routing template.")


def validate_round02_release_execution_approval_request(
    request_doc: dict[str, object],
    candidate_review_doc: dict[str, object],
    template_doc: dict[str, object],
) -> None:
    if request_doc.get("schema_version") != 1:
        raise RuntimeError("Round-02 release execution approval request schema_version must be 1.")
    if request_doc.get("id") != "round02-approved-payload-routing-proposal-approval-request-2026-07-02":
        raise RuntimeError("Round-02 release execution approval request id mismatch.")
    if request_doc.get("status") != "awaiting_owner_approval":
        raise RuntimeError("Round-02 release execution approval request must await owner approval.")
    if request_doc.get("not_approval") is not True:
        raise RuntimeError("Round-02 release execution approval request must explicitly avoid approval.")
    if request_doc.get("approval_recorded") is not False:
        raise RuntimeError("Round-02 release execution approval request must not record approval.")
    if request_doc.get("source_candidate_review") != "registry/round02-release-admission-candidate-review.json":
        raise RuntimeError("Round-02 release execution approval request must reference candidate review.")
    if request_doc.get("execution_template") != "registry/round02-approved-payload-routing-proposal-template.json":
        raise RuntimeError("Round-02 release execution approval request must reference execution template.")
    if template_doc.get("source_approval_request") != "registry/round02-release-execution-approval-request.json":
        raise RuntimeError("Round-02 release execution approval request must be referenced by template.")
    if candidate_review_doc.get("status") != "release_admission_candidate_review_recorded_not_release_approved":
        raise RuntimeError("Round-02 release execution approval request expects admission-reviewed state.")

    decisions = {
        item.get("candidate_id"): item.get("decision")
        for item in candidate_review_doc.get("candidate_decisions", [])
        if isinstance(item, dict)
    }
    expected_included = [
        "obsidian-open-format-knowledge-files",
        "ai-shipping-governance",
        "product-execution-documents",
        "product-discovery-research-planning",
        "personal-document-and-copyediting-boundary",
        "design-direction-and-anti-slop-reference",
        "brand-asset-provenance-protocol",
    ]
    expected_excluded = [
        "obsidian-cli-runtime-adapter",
        "defuddle-tool-adapter",
        "data-analytics-runtime-equivalence",
        "synthetic-data-and-sql-tooling",
        "market-strategy-evidence-boundary",
        "legal-privacy-document-boundary",
        "html-deck-animation-toolchain-boundary",
        "voiceover-tts-media-pipeline-boundary",
        "bundled-assets-redistribution-boundary",
    ]
    if request_doc.get("included_candidate_ids") != expected_included:
        raise RuntimeError("Round-02 release execution included candidates drifted.")
    if request_doc.get("excluded_candidate_ids") != expected_excluded:
        raise RuntimeError("Round-02 release execution excluded candidates drifted.")
    if template_doc.get("included_candidate_ids") != expected_included:
        raise RuntimeError("Round-02 release execution template included candidates must match request.")
    if template_doc.get("excluded_candidate_ids") != expected_excluded:
        raise RuntimeError("Round-02 release execution template excluded candidates must match request.")
    if set(expected_included + expected_excluded) != set(decisions):
        raise RuntimeError("Round-02 release execution request must partition all reviewed candidates.")
    for candidate_id in expected_included:
        if decisions.get(candidate_id) not in {
            "proposed-approved-payload",
            "merge-into-existing-approved-skill",
        }:
            raise RuntimeError(f"Round-02 release execution included non-release candidate: {candidate_id}")
    for candidate_id in expected_excluded:
        if decisions.get(candidate_id) in {
            "proposed-approved-payload",
            "merge-into-existing-approved-skill",
        }:
            raise RuntimeError(f"Round-02 release execution excluded release candidate: {candidate_id}")

    scope = request_doc.get("candidate_scope", {})
    if not isinstance(scope, dict):
        raise RuntimeError("Round-02 release execution request must include candidate_scope.")
    if scope.get("proposed_approved_payload_candidates") != ["obsidian-open-format-knowledge-files"]:
        raise RuntimeError("Round-02 release execution payload candidate scope drifted.")
    if scope.get("merge_into_existing_skill_candidates") != expected_included[1:]:
        raise RuntimeError("Round-02 release execution merge candidate scope drifted.")
    if scope.get("adapter_only_candidates_excluded") != [
        "obsidian-cli-runtime-adapter",
        "defuddle-tool-adapter",
        "synthetic-data-and-sql-tooling",
        "html-deck-animation-toolchain-boundary",
        "voiceover-tts-media-pipeline-boundary",
    ]:
        raise RuntimeError("Round-02 release execution adapter exclusion drifted.")
    if scope.get("reference_only_candidates_excluded") != [
        "data-analytics-runtime-equivalence",
        "market-strategy-evidence-boundary",
        "legal-privacy-document-boundary",
    ]:
        raise RuntimeError("Round-02 release execution reference exclusion drifted.")
    if scope.get("rejected_candidates_excluded") != ["bundled-assets-redistribution-boundary"]:
        raise RuntimeError("Round-02 release execution reject exclusion drifted.")

    permissions = request_doc.get("current_permissions", {})
    if not isinstance(permissions, dict):
        raise RuntimeError("Round-02 release execution approval request permissions are required.")
    for key, value in permissions.items():
        expected = key == "approval_request_allowed"
        if value is not expected:
            raise RuntimeError(f"Round-02 release execution approval request permission mismatch: {key}")

    required_requested_scope = {
        "enter a GitHub-only Round-02 approved-payload and routing proposal stage for the included 7 non-runtime candidates",
        "create a bounded approved-payload diff for obsidian-open-format-knowledge-files if its final Skill body remains source-text-neutral, agent-neutral, public-safe, and dependency-free",
        "create bounded merge diffs for the 6 merge candidates only where they improve existing approved Skills without conflicting triggers or hidden runtime dependencies",
        "update registry/skills.json, registry/capabilities.json, registry/relations.json, registry/conflicts.json, registry/recipes.json, registry/routing.json, release-manifest.json, and generated projections only as required by the approved GitHub-stage proposal",
        "run repository verification and record validation evidence before any follow-up local runtime sync request",
    }
    if set(request_doc.get("requested_scope_if_approved", [])) != required_requested_scope:
        raise RuntimeError("Round-02 release execution approval request requested scope changed.")

    required_disallowed = {
        "install or sync live Agent environments",
        r"write to C:\Users\15521\.codex\skills",
        r"write to C:\Users\15521\.agents\skills",
        r"write to C:\Users\15521\.cc-switch\skills",
        "publish a release outside GitHub repository commits",
        "redistribute upstream source text as approved curated payload",
        "redistribute upstream source assets as approved curated payload",
        "install dependencies, use credentials, call TTS providers, or generate external media",
        "execute adapter-only candidates or add their runtime dependencies",
        "promote reference-only candidates into runtime behavior",
        "reconsider rejected bundled assets without asset-level provenance review",
    }
    if set(request_doc.get("explicitly_not_requested", [])) != required_disallowed:
        raise RuntimeError("Round-02 release execution approval request explicitly_not_requested changed.")
    if set(request_doc.get("still_disallowed", [])) != required_disallowed:
        raise RuntimeError("Round-02 release execution approval request still_disallowed changed.")
    if request_doc.get("safe_approval_phrases") != [
        "批准进入 Round-02 approved-payload/routing 提案阶段",
        "Approve Round-02 approved-payload and routing proposal only",
    ]:
        raise RuntimeError("Round-02 release execution approval request safe approval phrases changed.")
    if request_doc.get("next_state_if_approved") != "round02_approved_payload_routing_proposal":
        raise RuntimeError("Round-02 release execution approval request next state mismatch.")

    required_next_evidence = {
        "owner approval event record",
        "bounded payload and merge execution record",
        "before/after inventory, manifest, routing, and generated projection diff summary",
        "candidate-specific rationale for each included payload or merge change",
        "explicit record that adapter-only, reference-only, rejected, live install, local sync, source redistribution, asset redistribution, dependency, credential, and media actions remain excluded",
        "verification command results",
    }
    if set(request_doc.get("next_required_evidence_if_approved", [])) != required_next_evidence:
        raise RuntimeError("Round-02 release execution approval request next required evidence changed.")

    doc_path = request_doc.get("evidence_doc")
    if doc_path != "docs/round02-release-execution-approval-request.md":
        raise RuntimeError("Round-02 release execution approval request evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "This is an approval request, not approval.",
        "Execution template:",
        "approval recorded: false",
        "approved payload diff allowed: false",
        "adapter runtime work allowed: false",
        "Included Candidates",
        "Excluded Candidates",
        "批准进入 Round-02 approved-payload/routing 提案阶段",
        "Approve Round-02 approved-payload and routing proposal only",
        "Explicitly Not Requested",
        "Until the approval event exists, Round-02 remains admission-reviewed but not",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"Round-02 release execution approval request doc missing phrase: {phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link Round-02 release execution approval request.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link Round-02 release execution approval request.")


def validate_round02_approved_payload_routing_approval_events(
    events_doc: dict[str, object],
    request_doc: dict[str, object],
) -> None:
    if events_doc.get("schema_version") != 1:
        raise RuntimeError("Round-02 approved payload/routing approval events schema_version must be 1.")
    if events_doc.get("status") != "owner_approval_recorded_for_round02_approved_payload_routing_proposal":
        raise RuntimeError("Round-02 approved payload/routing approval events status mismatch.")

    expected_true = {
        "approval_recorded",
        "approved_payload_allowed",
        "release_manifest_allowed",
        "routing_projection_allowed",
        "generated_projection_allowed",
    }
    expected_false = {
        "publication_allowed",
        "live_install_allowed",
        "local_runtime_sync_allowed",
        "source_text_redistribution_allowed",
        "source_asset_redistribution_allowed",
        "dependency_install_allowed",
        "credential_use_allowed",
        "external_media_generation_allowed",
        "adapter_runtime_work_allowed",
    }
    for key in expected_true:
        if events_doc.get(key) is not True:
            raise RuntimeError(f"Round-02 approved payload/routing approval event must allow {key}.")
    for key in expected_false:
        if events_doc.get(key) is not False:
            raise RuntimeError(f"Round-02 approved payload/routing approval event must block {key}.")

    events = events_doc.get("events")
    if not isinstance(events, list) or len(events) != 1 or not isinstance(events[0], dict):
        raise RuntimeError("Round-02 approved payload/routing approval events must contain one event.")
    event = events[0]
    if event.get("id") != "round02-owner-approval-2026-07-02-approved-payload-routing-proposal":
        raise RuntimeError("Round-02 approved payload/routing event id mismatch.")
    if event.get("approval_phrase") != "批准进入 Round-02 approved-payload/routing 提案阶段":
        raise RuntimeError("Round-02 approved payload/routing approval phrase mismatch.")
    if event.get("approval_request_id") != request_doc.get("id"):
        raise RuntimeError("Round-02 approved payload/routing approval request id mismatch.")
    if event.get("approved_scope") != request_doc.get("requested_scope_if_approved"):
        raise RuntimeError("Round-02 approved payload/routing approved scope must match request.")
    if event.get("explicitly_not_approved") != request_doc.get("explicitly_not_requested"):
        raise RuntimeError("Round-02 approved payload/routing disallowed scope must match request.")
    if event.get("next_state") != request_doc.get("next_state_if_approved"):
        raise RuntimeError("Round-02 approved payload/routing next state mismatch.")


def validate_round02_approved_payload_routing_proposal(
    proposal_doc: dict[str, object],
    approval_events_doc: dict[str, object],
    request_doc: dict[str, object],
    candidate_review_doc: dict[str, object],
    skills_doc: dict[str, object],
    capabilities_doc: dict[str, object],
    relations_doc: dict[str, object],
    routing_doc: dict[str, object],
    scenarios_doc: dict[str, object],
    manifest: dict[str, object],
    sources_doc: dict[str, object],
) -> None:
    expected_event_id = "round02-owner-approval-2026-07-02-approved-payload-routing-proposal"
    expected_included = [
        "obsidian-open-format-knowledge-files",
        "ai-shipping-governance",
        "product-execution-documents",
        "product-discovery-research-planning",
        "personal-document-and-copyediting-boundary",
        "design-direction-and-anti-slop-reference",
        "brand-asset-provenance-protocol",
    ]
    expected_excluded = [
        "obsidian-cli-runtime-adapter",
        "defuddle-tool-adapter",
        "data-analytics-runtime-equivalence",
        "synthetic-data-and-sql-tooling",
        "market-strategy-evidence-boundary",
        "legal-privacy-document-boundary",
        "html-deck-animation-toolchain-boundary",
        "voiceover-tts-media-pipeline-boundary",
        "bundled-assets-redistribution-boundary",
    ]
    expected_payload = ["obsidian-open-format-knowledge-files"]
    expected_merge = expected_included[1:]
    expected_deferred_targets = [
        "design-an-interface",
        "doc",
        "edit-article",
        "grill-me",
        "security-ownership-map",
        "writing-shape",
    ]
    required_commands = [
        "python -B scripts/build_topology.py",
        "python -B scripts/build_release_manifest.py",
        "python -B scripts/simulate_routing.py --report generated/routing-simulation-report.json",
        "python -B scripts/verify.py",
        "python -B scripts/build_topology.py --check",
        "python -B scripts/build_release_manifest.py --check",
        "python -B scripts/simulate_routing.py --all",
        "python -B -m unittest discover -s tests -v",
    ]

    if proposal_doc.get("schema_version") != 1:
        raise RuntimeError("Round-02 approved payload/routing proposal schema_version must be 1.")
    if proposal_doc.get("record_id") != "round02-approved-payload-routing-proposal-2026-07-02":
        raise RuntimeError("Round-02 approved payload/routing proposal record id mismatch.")
    if proposal_doc.get("status") not in {
        "approved_payload_routing_proposal_recorded_pending_final_validation",
        "approved_payload_routing_proposal_validated_github_only",
    }:
        raise RuntimeError("Round-02 approved payload/routing proposal status mismatch.")
    if proposal_doc.get("approval_event_id") != expected_event_id:
        raise RuntimeError("Round-02 approved payload/routing proposal event id mismatch.")
    if proposal_doc.get("approval_request_id") != request_doc.get("id"):
        raise RuntimeError("Round-02 approved payload/routing proposal request id mismatch.")
    if proposal_doc.get("source_candidate_review") != "registry/round02-release-admission-candidate-review.json":
        raise RuntimeError("Round-02 approved payload/routing proposal must reference candidate review.")
    if proposal_doc.get("execution_template") != "registry/round02-approved-payload-routing-proposal-template.json":
        raise RuntimeError("Round-02 approved payload/routing proposal must reference template.")
    if proposal_doc.get("approval_events") != "registry/round02-approved-payload-routing-approval-events.json":
        raise RuntimeError("Round-02 approved payload/routing proposal approval events path mismatch.")
    if proposal_doc.get("evidence_doc") != "docs/round02-approved-payload-routing-proposal.md":
        raise RuntimeError("Round-02 approved payload/routing proposal evidence doc path mismatch.")

    approval_events = approval_events_doc.get("events", [])
    if not isinstance(approval_events, list) or not approval_events:
        raise RuntimeError("Round-02 approved payload/routing proposal needs an approval event.")
    approval_event = approval_events[0]
    if not isinstance(approval_event, dict) or approval_event.get("id") != expected_event_id:
        raise RuntimeError("Round-02 approved payload/routing proposal approval event not found.")

    scope = proposal_doc.get("candidate_scope")
    if not isinstance(scope, dict):
        raise RuntimeError("Round-02 approved payload/routing proposal candidate_scope is required.")
    if scope.get("included_candidate_ids") != expected_included:
        raise RuntimeError("Round-02 approved payload/routing included candidate scope drifted.")
    if scope.get("excluded_candidate_ids") != expected_excluded:
        raise RuntimeError("Round-02 approved payload/routing excluded candidate scope drifted.")
    if scope.get("approved_payload_candidates") != expected_payload:
        raise RuntimeError("Round-02 approved payload/routing payload candidate scope drifted.")
    if scope.get("merge_candidates") != expected_merge:
        raise RuntimeError("Round-02 approved payload/routing merge candidate scope drifted.")
    if scope.get("deferred_merge_targets_not_in_approved_inventory") != expected_deferred_targets:
        raise RuntimeError("Round-02 approved payload/routing deferred target scope drifted.")

    decisions = {
        item.get("candidate_id"): item.get("decision")
        for item in candidate_review_doc.get("candidate_decisions", [])
        if isinstance(item, dict)
    }
    if set(decisions) != set(expected_included + expected_excluded):
        raise RuntimeError("Round-02 approved payload/routing proposal must cover all reviewed candidates.")
    for candidate_id in expected_payload:
        if decisions.get(candidate_id) != "proposed-approved-payload":
            raise RuntimeError(f"Round-02 approved payload candidate decision mismatch: {candidate_id}")
    for candidate_id in expected_merge:
        if decisions.get(candidate_id) != "merge-into-existing-approved-skill":
            raise RuntimeError(f"Round-02 merge candidate decision mismatch: {candidate_id}")
    for candidate_id in expected_excluded:
        if decisions.get(candidate_id) in {"proposed-approved-payload", "merge-into-existing-approved-skill"}:
            raise RuntimeError(f"Round-02 excluded candidate entered approved scope: {candidate_id}")

    executions = proposal_doc.get("candidate_executions")
    if not isinstance(executions, list) or len(executions) != len(expected_included):
        raise RuntimeError("Round-02 approved payload/routing proposal must include seven candidate executions.")
    execution_by_candidate = {
        item.get("candidate_id"): item
        for item in executions
        if isinstance(item, dict)
    }
    if set(execution_by_candidate) != set(expected_included):
        raise RuntimeError("Round-02 approved payload/routing candidate execution ids drifted.")
    for candidate_id, execution in execution_by_candidate.items():
        if execution.get("approval_event_id") != expected_event_id:
            raise RuntimeError(f"Round-02 candidate execution event id mismatch: {candidate_id}")
        if not execution.get("target_files"):
            raise RuntimeError(f"Round-02 candidate execution missing target files: {candidate_id}")
        for field in ["rationale", "diff_summary", "rejected_alternatives", "boundary_assertions", "next_gate"]:
            if not execution.get(field):
                raise RuntimeError(f"Round-02 candidate execution missing {field}: {candidate_id}")
    if execution_by_candidate["obsidian-open-format-knowledge-files"].get("execution_type") != "new-approved-skill-payload":
        raise RuntimeError("Round-02 Obsidian open-format candidate must be new approved payload.")
    for candidate_id in expected_merge:
        if execution_by_candidate[candidate_id].get("execution_type") != "bounded-merge-into-existing-approved-skills":
            raise RuntimeError(f"Round-02 candidate must be a bounded merge: {candidate_id}")

    skill_id = "skill.curated.obsidian-open-format-knowledge-files"
    skill_path = "skills/obsidian-open-format-knowledge-files/SKILL.md"
    skills = {
        item.get("id"): item
        for item in skills_doc.get("skills", [])
        if isinstance(item, dict)
    }
    skill = skills.get(skill_id)
    if not skill:
        raise RuntimeError("Round-02 approved payload skill missing from registry/skills.json.")
    if skill.get("directory") != "obsidian-open-format-knowledge-files":
        raise RuntimeError("Round-02 approved payload skill directory mismatch.")
    if skill.get("source") != "github:kepano/obsidian-skills":
        raise RuntimeError("Round-02 approved payload skill source mismatch.")
    if skill.get("status") != "approved":
        raise RuntimeError("Round-02 approved payload skill must be approved.")
    expected_description = (
        "Use when reading, creating, editing, or reviewing Obsidian-compatible Markdown notes, "
        "JSON Canvas files, or Bases files as portable open-format knowledge artifacts without "
        "assuming a live Obsidian app, CLI, plugin, or vault."
    )
    if skill.get("description") != expected_description:
        raise RuntimeError("Round-02 approved payload skill description drifted.")

    skill_text = (ROOT / skill_path).read_text(encoding="utf-8")
    for phrase in [
        "JSON Canvas",
        "Bases",
        "live Obsidian app",
        "Do not invoke an Obsidian CLI",
        "Do not install packages, plugins, CLIs, or dependencies.",
        "Do not fetch external links or assets as part of open-format editing.",
    ]:
        if phrase not in skill_text:
            raise RuntimeError(f"Round-02 approved payload skill missing phrase: {phrase}")

    capabilities = {
        item.get("id"): item
        for item in capabilities_doc.get("capabilities", [])
        if isinstance(item, dict)
    }
    capability = capabilities.get("capability.open-format-knowledge-files")
    if not capability:
        raise RuntimeError("Round-02 open-format knowledge-files capability missing.")
    if capability.get("coverageState") != "curated":
        raise RuntimeError("Round-02 open-format knowledge-files capability must be curated.")
    if capability.get("curatedOwners") != [skill_id]:
        raise RuntimeError("Round-02 open-format knowledge-files capability owner mismatch.")

    relations = {
        (item.get("from"), item.get("type"), item.get("to"))
        for item in relations_doc.get("relations", [])
        if isinstance(item, dict)
    }
    if (skill_id, "provides", "capability.open-format-knowledge-files") not in relations:
        raise RuntimeError("Round-02 open-format knowledge-files provides relation missing.")
    if ("capability.open-format-knowledge-files", "complements", "capability.knowledge-capture") not in relations:
        raise RuntimeError("Round-02 open-format knowledge-files complement relation missing.")

    routes = {
        item.get("skill"): item
        for item in routing_doc.get("routes", [])
        if isinstance(item, dict)
    }
    route = routes.get(skill_id)
    if not route:
        raise RuntimeError("Round-02 open-format knowledge-files routing entry missing.")
    if route.get("lifecycleCapabilities") != ["capability.open-format-knowledge-files"]:
        raise RuntimeError("Round-02 open-format knowledge-files route capability mismatch.")
    route_text = json.dumps(route, ensure_ascii=False)
    for phrase in ["JSON Canvas", "Bases", "live Obsidian app", "Obsidian CLI", "asset fetch"]:
        if phrase not in route_text:
            raise RuntimeError(f"Round-02 open-format knowledge-files route missing phrase: {phrase}")

    scenarios = {
        item.get("id"): item
        for item in scenarios_doc.get("scenarios", [])
        if isinstance(item, dict)
    }
    scenario = scenarios.get("scenario.lifecycle-27")
    if not scenario:
        raise RuntimeError("Round-02 open-format knowledge-files lifecycle scenario missing.")
    if scenario.get("expectedSkills") != [skill_id]:
        raise RuntimeError("Round-02 open-format knowledge-files scenario skill mismatch.")
    if scenario.get("expectedCapabilities") != ["capability.open-format-knowledge-files"]:
        raise RuntimeError("Round-02 open-format knowledge-files scenario capability mismatch.")

    sources = {
        item.get("id"): item
        for item in sources_doc.get("sources", [])
        if isinstance(item, dict)
    }
    source = sources.get("github:kepano/obsidian-skills")
    if not source:
        raise RuntimeError("Round-02 kepano source lock missing.")
    if source.get("revision") != "a1dc48e68138490d522c04cbf5822214c6eb1202":
        raise RuntimeError("Round-02 kepano source revision mismatch.")
    if source.get("license") != "MIT":
        raise RuntimeError("Round-02 kepano source license mismatch.")
    if "obsidian-open-format-knowledge-files" not in source.get("candidateIds", []):
        raise RuntimeError("Round-02 kepano source candidate id missing.")

    manifest_paths = {
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    }
    if manifest.get("skillCount") != 20 or manifest.get("fileCount") != 42:
        raise RuntimeError("Round-02 approved payload manifest counts must be 20 Skills and 42 files.")
    if skill_path not in manifest_paths:
        raise RuntimeError("Round-02 approved payload skill missing from release manifest.")

    excluded_skill_ids = {f"skill.curated.{candidate_id}" for candidate_id in expected_excluded}
    approved_skill_ids = set(skills)
    routed_skill_ids = set(routes)
    if excluded_skill_ids & approved_skill_ids:
        raise RuntimeError("Round-02 excluded candidates entered skill registry.")
    if excluded_skill_ids & routed_skill_ids:
        raise RuntimeError("Round-02 excluded candidates entered routing registry.")
    for candidate_id in expected_excluded:
        if f"skills/{candidate_id}/" in "\n".join(sorted(manifest_paths)):
            raise RuntimeError(f"Round-02 excluded candidate entered manifest: {candidate_id}")

    validation_results = proposal_doc.get("validation_results")
    if not isinstance(validation_results, dict):
        raise RuntimeError("Round-02 approved payload/routing validation_results missing.")
    if validation_results.get("required_commands") != required_commands:
        raise RuntimeError("Round-02 approved payload/routing required command set drifted.")
    validation_status = validation_results.get("status")
    if validation_status not in {"pending_final_run", "passed"}:
        raise RuntimeError("Round-02 approved payload/routing validation status mismatch.")
    if proposal_doc.get("status") == "approved_payload_routing_proposal_validated_github_only":
        if validation_status != "passed":
            raise RuntimeError("Round-02 approved payload/routing validated proposal must have passed validation.")
        executed = validation_results.get("executed_commands")
        if not isinstance(executed, list) or len(executed) < len(required_commands):
            raise RuntimeError("Round-02 approved payload/routing proposal must record executed commands.")
        executed_commands = {
            item.get("command")
            for item in executed
            if isinstance(item, dict) and item.get("result") == "passed"
        }
        if set(required_commands) - executed_commands:
            raise RuntimeError("Round-02 approved payload/routing proposal missing passed command evidence.")
    else:
        if validation_status != "pending_final_run":
            raise RuntimeError("Round-02 approved payload/routing pending proposal must be pending final run.")

    doc_path = proposal_doc.get("evidence_doc")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "Round-02 Approved Payload And Routing Proposal",
        "Owner approval phrase",
        "local runtime sync",
        "open-format Obsidian payload",
        "Validation",
        "Next Gate",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"Round-02 approved payload/routing doc missing phrase: {phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link Round-02 approved payload/routing proposal.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link Round-02 approved payload/routing proposal.")
    notices = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    for phrase in ["kepano/obsidian-skills", "Steph Ango", "sources/kepano-obsidian-skills/LICENSE"]:
        if phrase not in notices:
            raise RuntimeError(f"Third-party notices missing Round-02 kepano phrase: {phrase}")

    simulation_report = load("generated/routing-simulation-report.json")
    if simulation_report.get("scenarioCount") != 105 or simulation_report.get("failed") != 0:
        raise RuntimeError("Round-02 routing simulation report must cover 105 passing scenarios.")


def validate_mvp06_radar_feedback_projection(
    feedback_doc: dict[str, object],
    lifecycle_doc: dict[str, object],
) -> None:
    decisions = {
        item.get("id"): item
        for item in feedback_doc.get("decisions", [])
        if isinstance(item, dict)
    }
    metadata = lifecycle_doc.get("radar_feedback", {}).get("metadata", [])
    for item in metadata:
        source = item.get("source")
        candidate_id = item.get("candidate_id")
        if not isinstance(source, str) or "@" not in source:
            raise RuntimeError(f"MVP-06 radar feedback source is invalid: {candidate_id}")
        feedback_id, source_revision = source.rsplit("@", 1)
        decision = decisions.get(feedback_id)
        if not decision:
            raise RuntimeError(f"Missing MVP-06 radar feedback decision: {feedback_id}")
        if decision.get("disposition") != "already-reviewed":
            raise RuntimeError(f"MVP-06 radar feedback source disposition drifted: {feedback_id}")
        if decision.get("runtimeEligible") is not False:
            raise RuntimeError(f"MVP-06 radar feedback source must not be runtime eligible: {feedback_id}")
        if "dedupe_signal" not in decision.get("appliesTo", []):
            raise RuntimeError(f"MVP-06 radar feedback must be a dedupe signal: {feedback_id}")
        candidate_feedback = {
            entry.get("candidateId"): entry
            for entry in decision.get("candidateFeedback", [])
            if isinstance(entry, dict)
        }
        candidate_entry = candidate_feedback.get(candidate_id)
        if not candidate_entry:
            raise RuntimeError(f"Missing MVP-06 candidate feedback: {candidate_id}")
        if candidate_entry.get("sourceRevision") != source_revision:
            raise RuntimeError(f"MVP-06 candidate feedback revision drifted: {candidate_id}")
        if candidate_entry.get("outcome") != item.get("outcome"):
            raise RuntimeError(f"MVP-06 candidate feedback outcome drifted: {candidate_id}")
        if candidate_entry.get("runtimeSurface") != item.get("runtime_surface"):
            raise RuntimeError(f"MVP-06 candidate feedback runtime surface drifted: {candidate_id}")


def validate_mvp_candidate_batches(
    batches_doc: dict[str, object],
    sources_doc: dict[str, object],
    selection_doc: dict[str, object],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if batches_doc.get("schema_version") != 1:
        raise RuntimeError("MVP candidate batches schema_version must be 1.")
    if batches_doc.get("status") != "selection_recorded_not_approved":
        raise RuntimeError("MVP candidate batches must remain not approved.")
    source_records = {
        item["id"]: item
        for item in sources_doc.get("sources", [])
        if isinstance(item, dict) and "id" in item
    }
    selection_source = selection_doc.get("source")
    selection_revision = selection_doc.get("revision")
    decisions = selection_doc.get("decisions", {})
    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = "\n".join(
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    )
    batches = batches_doc.get("batches", [])
    if len(batches) != 1:
        raise RuntimeError("Expected exactly one MVP candidate batch.")
    for batch in batches:
        if batch.get("approval_state") != "selected_for_review_not_approved":
            raise RuntimeError("MVP candidate batch must not be approved.")
        if batch.get("runtime_allowed") or batch.get("release_manifest_allowed") or batch.get("routing_projection_allowed"):
            raise RuntimeError("MVP candidate batch must not be executable or releasable.")
        source_id = batch.get("source")
        source = source_records.get(source_id)
        if source is None:
            raise RuntimeError(f"MVP candidate batch references unknown source: {source_id}")
        if batch.get("revision") != source.get("revision") or batch.get("revision") != selection_revision:
            raise RuntimeError("MVP candidate batch revision must match source lock and selection.")
        if source_id != selection_source:
            raise RuntimeError("MVP candidate batch source must match selection document.")
        for ref in batch.get("review_refs", []):
            if not (ROOT / ref).is_file():
                raise RuntimeError(f"MVP candidate batch has dead review ref: {ref}")
        for candidate in batch.get("candidates", []):
            candidate_id = candidate.get("candidate_id")
            if candidate_id not in source.get("candidateIds", []):
                raise RuntimeError(f"MVP candidate not listed in source lock: {candidate_id}")
            if decisions.get(candidate_id) != candidate.get("source_selection_disposition"):
                raise RuntimeError(f"MVP candidate selection drift: {candidate_id}")
            if candidate.get("source_selection_disposition") != "merge":
                raise RuntimeError(f"MVP candidate batch should contain only merge candidates: {candidate_id}")
            if candidate_id in approved_directories:
                raise RuntimeError(f"MVP candidate already appears as approved Skill directory: {candidate_id}")
            if f"skills/{candidate_id}/" in manifest_paths:
                raise RuntimeError(f"MVP candidate appears in release manifest: {candidate_id}")
        doc = (ROOT / "docs/mvp-candidate-batch-2026-06-27.md").read_text(encoding="utf-8")
        for phrase in [
            "selection record, not approval",
            "Runtime allowed",
            "Release manifest allowed",
            "Routing projection allowed",
            "This document closes MVP-01 selection evidence only",
        ]:
            if phrase not in doc:
                raise RuntimeError(f"MVP candidate batch doc missing phrase: {phrase}")


def validate_mvp_candidate_reviews(
    reviews_doc: dict[str, object],
    batches_doc: dict[str, object],
    sources_doc: dict[str, object],
    selection_doc: dict[str, object],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if reviews_doc.get("schema_version") != 1:
        raise RuntimeError("MVP candidate reviews schema_version must be 1.")
    if reviews_doc.get("status") != "pre_adaptation_review_recorded_not_approved":
        raise RuntimeError("MVP candidate reviews must remain not approved.")

    reviews = reviews_doc.get("reviews", [])
    if len(reviews) != 1:
        raise RuntimeError("Expected exactly one MVP candidate review.")
    batches = batches_doc.get("batches", [])
    if len(batches) != 1:
        raise RuntimeError("Expected exactly one MVP candidate batch for review.")
    batch = batches[0]
    batch_candidates = {
        candidate.get("candidate_id")
        for candidate in batch.get("candidates", [])
        if isinstance(candidate, dict)
    }

    source_records = {
        item["id"]: item
        for item in sources_doc.get("sources", [])
        if isinstance(item, dict) and "id" in item
    }
    decisions = selection_doc.get("decisions", {})
    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = "\n".join(
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    )

    for review in reviews:
        if review.get("batch_id") != batch.get("id"):
            raise RuntimeError("MVP candidate review must reference the selected batch.")
        if review.get("review_state") != "pre_adaptation_review_not_approved":
            raise RuntimeError("MVP candidate review must remain pre-adaptation.")
        if (
            review.get("runtime_allowed")
            or review.get("release_manifest_allowed")
            or review.get("routing_projection_allowed")
            or review.get("adapted_payload_allowed")
            or review.get("source_text_redistributed")
        ):
            raise RuntimeError("MVP candidate review must not approve runtime, release, routing, adaptation, or source redistribution.")
        source_id = review.get("source")
        source = source_records.get(source_id)
        if source is None:
            raise RuntimeError(f"MVP candidate review references unknown source: {source_id}")
        if review.get("revision") != source.get("revision") or review.get("revision") != selection_doc.get("revision"):
            raise RuntimeError("MVP candidate review revision must match source lock and selection.")
        if source_id != selection_doc.get("source"):
            raise RuntimeError("MVP candidate review source must match selection document.")
        evidence_doc = review.get("evidence_doc")
        if not isinstance(evidence_doc, str) or not (ROOT / evidence_doc).is_file():
            raise RuntimeError("MVP candidate review evidence doc is missing.")
        for ref in review.get("review_refs", []):
            if not (ROOT / ref).is_file():
                raise RuntimeError(f"MVP candidate review has dead review ref: {ref}")
        review_candidates = review.get("candidates", [])
        review_ids = {
            candidate.get("candidate_id")
            for candidate in review_candidates
            if isinstance(candidate, dict)
        }
        if review_ids != batch_candidates:
            raise RuntimeError("MVP candidate review candidates must match the selected batch.")
        for candidate in review_candidates:
            candidate_id = candidate.get("candidate_id")
            if candidate_id not in source.get("candidateIds", []):
                raise RuntimeError(f"MVP reviewed candidate not listed in source lock: {candidate_id}")
            if decisions.get(candidate_id) != candidate.get("source_selection_disposition"):
                raise RuntimeError(f"MVP reviewed candidate selection drift: {candidate_id}")
            if candidate.get("source_selection_disposition") != "merge":
                raise RuntimeError(f"MVP review should contain only merge candidates: {candidate_id}")
            if candidate.get("instruction_surface") != "instruction_only":
                raise RuntimeError(f"MVP reviewed candidate must remain instruction-only: {candidate_id}")
            if candidate.get("embedded_executable_artifacts"):
                raise RuntimeError(f"MVP reviewed candidate cannot approve embedded executable artifacts: {candidate_id}")
            upstream_hash = candidate.get("upstream_sha256")
            if not isinstance(upstream_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", upstream_hash):
                raise RuntimeError(f"MVP reviewed candidate has invalid upstream hash: {candidate_id}")
            if candidate_id in approved_directories:
                raise RuntimeError(f"MVP reviewed candidate already appears as approved Skill directory: {candidate_id}")
            if f"skills/{candidate_id}/" in manifest_paths:
                raise RuntimeError(f"MVP reviewed candidate appears in release manifest: {candidate_id}")
            if not candidate.get("must_neutralize") or not candidate.get("mvp02_remaining_work"):
                raise RuntimeError(f"MVP reviewed candidate must record neutralization and remaining work: {candidate_id}")

    doc = (ROOT / "docs/mvp-candidate-review-2026-06-27.md").read_text(encoding="utf-8")
    for phrase in [
        "It is not approval",
        "Runtime allowed",
        "Release manifest allowed",
        "Routing projection allowed",
        "Adapted payload allowed",
        "This document does not close MVP-02",
        "Do not copy upstream source text into `skills/`",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"MVP candidate review doc missing phrase: {phrase}")


def validate_mvp_transition_gates(
    gates_doc: dict[str, object],
    batches_doc: dict[str, object],
    reviews_doc: dict[str, object],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
    approval_events_doc: dict[str, object],
    adapted_drafts_doc: dict[str, object],
) -> None:
    if gates_doc.get("schema_version") != 1:
        raise RuntimeError("MVP transition gates schema_version must be 1.")
    if gates_doc.get("status") != "adapted_draft_created_pending_next_gate":
        raise RuntimeError("MVP transition gate must record adapted draft creation pending next gate.")

    gates = gates_doc.get("gates", [])
    if len(gates) != 1:
        raise RuntimeError("Expected exactly one MVP transition gate.")
    batches = batches_doc.get("batches", [])
    reviews = reviews_doc.get("reviews", [])
    if len(batches) != 1 or len(reviews) != 1:
        raise RuntimeError("MVP transition gate expects one batch and one review.")

    batch = batches[0]
    review = reviews[0]
    batch_candidates = {
        candidate.get("candidate_id")
        for candidate in batch.get("candidates", [])
        if isinstance(candidate, dict)
    }
    review_candidates = {
        candidate.get("candidate_id")
        for candidate in review.get("candidates", [])
        if isinstance(candidate, dict)
    }
    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = "\n".join(
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    )

    gate = gates[0]
    if gate.get("batch_id") != batch.get("id"):
        raise RuntimeError("MVP transition gate must reference the selected batch.")
    if gate.get("review_id") != review.get("id"):
        raise RuntimeError("MVP transition gate must reference the pre-adaptation review.")
    if gate.get("transition_state") != "adapted_draft_review_recorded_pending_next_gate":
        raise RuntimeError("MVP transition gate must stop after adapted draft review.")
    if gate.get("explicit_human_approval_required") is not True:
        raise RuntimeError("MVP transition gate must require explicit human approval.")
    if gate.get("current_human_approval_recorded") is not True:
        raise RuntimeError("MVP transition gate must record bounded approval.")
    if gate.get("approval_event_id") != "mvp02-owner-approval-2026-06-27-adapted-draft":
        raise RuntimeError("MVP transition gate approval event mismatch.")
    if gate.get("adapted_draft_record") != "registry/mvp02-adapted-drafts.json":
        raise RuntimeError("MVP transition gate adapted draft record mismatch.")
    if gate.get("approval_event_id") not in {
        event.get("id")
        for event in approval_events_doc.get("events", [])
        if isinstance(event, dict)
    }:
        raise RuntimeError("MVP transition gate approval event is not recorded.")
    if adapted_drafts_doc.get("gate_id") != gate.get("id"):
        raise RuntimeError("MVP transition gate does not match adapted draft record.")

    current_permissions = gate.get("current_permissions", {})
    for key in [
        "adapted_output_allowed",
        "approved_payload_allowed",
        "runtime_allowed",
        "release_manifest_allowed",
        "routing_projection_allowed",
        "live_install_allowed",
        "source_text_redistribution_allowed",
    ]:
        expected = key == "adapted_output_allowed"
        if current_permissions.get(key) is not expected:
            raise RuntimeError(f"MVP transition gate must keep {key} false.")

    gate_candidates = {
        candidate.get("candidate_id")
        for candidate in gate.get("candidates", [])
        if isinstance(candidate, dict)
    }
    if gate_candidates != batch_candidates or gate_candidates != review_candidates:
        raise RuntimeError("MVP transition gate candidates must match batch and review.")
    for candidate in gate.get("candidates", []):
        candidate_id = candidate.get("candidate_id")
        if candidate_id in approved_directories:
            raise RuntimeError(f"MVP transition candidate already approved: {candidate_id}")
        if f"skills/{candidate_id}/" in manifest_paths:
            raise RuntimeError(f"MVP transition candidate appears in release manifest: {candidate_id}")
        if candidate.get("next_allowed_state") != "adaptation_draft_after_explicit_approval":
            raise RuntimeError(f"MVP transition candidate has wrong next state: {candidate_id}")
        if not candidate.get("required_decisions"):
            raise RuntimeError(f"MVP transition candidate needs required decisions: {candidate_id}")

    for list_key in [
        "preconditions_before_adaptation",
        "allowed_after_explicit_approval",
        "disallowed_without_approval",
        "fail_closed_conditions",
        "acceptance_to_leave_gate",
    ]:
        values = gate.get(list_key)
        if not isinstance(values, list) or not values:
            raise RuntimeError(f"MVP transition gate missing non-empty {list_key}.")

    doc_path = gate.get("evidence_doc")
    if doc_path != "docs/mvp02-adaptation-transition-gate.md":
        raise RuntimeError("MVP transition gate evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "This is a gate record, not release approval",
        "Current state: adapted draft created after explicit human approval",
        "Adapted output allowed | yes, only under `drafts/mvp02-adaptation/`",
        "Do not edit `skills/`",
        "Do not update `release-manifest.json`",
        "Do not update generated routing projections",
        "Do not install or sync live Agent environments",
        "Fail closed",
        "Acceptance to leave this gate",
        "separate next gate",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"MVP transition gate doc missing phrase: {phrase}")


def validate_mvp_adaptation_review_checklist(
    checklist_doc: dict[str, object],
    gates_doc: dict[str, object],
) -> None:
    if checklist_doc.get("schema_version") != 1:
        raise RuntimeError("MVP adaptation review checklist schema_version must be 1.")
    if checklist_doc.get("status") != "template_only_not_adapted_output":
        raise RuntimeError("MVP adaptation review checklist must remain template-only.")
    if checklist_doc.get("adapted_output_present") is not False:
        raise RuntimeError("MVP adaptation review checklist must not claim adapted output exists.")
    if checklist_doc.get("approval_required_before_use") is not True:
        raise RuntimeError("MVP adaptation review checklist must require approval before use.")

    gates = gates_doc.get("gates", [])
    if len(gates) != 1:
        raise RuntimeError("MVP adaptation review checklist expects one transition gate.")
    gate = gates[0]
    if checklist_doc.get("gate_id") != gate.get("id"):
        raise RuntimeError("MVP adaptation review checklist must reference the transition gate.")

    gate_candidates = {
        candidate.get("candidate_id")
        for candidate in gate.get("candidates", [])
        if isinstance(candidate, dict)
    }
    checklist_candidates = {
        candidate.get("candidate_id")
        for candidate in checklist_doc.get("candidate_checklists", [])
        if isinstance(candidate, dict)
    }
    if checklist_candidates != gate_candidates:
        raise RuntimeError("MVP adaptation review checklist candidates must match transition gate.")

    required_sections = {
        "source_integrity",
        "license_and_attribution",
        "security",
        "portability_and_neutralization",
        "overlap_and_conflict",
        "routing_and_runtime_boundary",
        "validation",
        "disposition",
    }
    actual_sections = {section.get("id") for section in checklist_doc.get("required_sections", [])}
    missing = required_sections - actual_sections
    if missing:
        raise RuntimeError("MVP adaptation review checklist missing sections: " + ", ".join(sorted(missing)))

    for section in checklist_doc.get("required_sections", []):
        if not section.get("must_record"):
            raise RuntimeError(f"MVP adaptation review checklist section missing must_record: {section.get('id')}")
        if section.get("fail_closed_if_missing") is not True:
            raise RuntimeError(f"MVP adaptation review checklist section must fail closed: {section.get('id')}")

    for candidate in checklist_doc.get("candidate_checklists", []):
        if not candidate.get("decision_questions"):
            raise RuntimeError(f"MVP adaptation candidate checklist missing decision questions: {candidate.get('candidate_id')}")
        if not candidate.get("forbidden_shortcuts"):
            raise RuntimeError(f"MVP adaptation candidate checklist missing forbidden shortcuts: {candidate.get('candidate_id')}")

    doc_path = checklist_doc.get("evidence_doc")
    if doc_path != "docs/mvp02-adaptation-review-template.md":
        raise RuntimeError("MVP adaptation review checklist evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "Template only, not adapted output",
        "Do not use this template as approval",
        "Source integrity",
        "License and attribution",
        "Security",
        "Portability and neutralization",
        "Overlap and conflict",
        "Routing and runtime boundary",
        "Validation",
        "Disposition",
        "Fail closed",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"MVP adaptation review template missing phrase: {phrase}")


def validate_mvp_approval_requests(
    requests_doc: dict[str, object],
    gates_doc: dict[str, object],
    checklist_doc: dict[str, object],
    approval_events_doc: dict[str, object],
    adapted_drafts_doc: dict[str, object],
) -> None:
    if requests_doc.get("schema_version") != 1:
        raise RuntimeError("MVP approval requests schema_version must be 1.")
    if requests_doc.get("status") != "owner_approved_adapted_draft_creation":
        raise RuntimeError("MVP approval request must record owner-approved adapted draft creation.")
    if requests_doc.get("approval_recorded") is not True:
        raise RuntimeError("MVP approval request must record bounded approval.")
    if requests_doc.get("adapted_output_present") is not True:
        raise RuntimeError("MVP approval request must record adapted output.")

    requests = requests_doc.get("requests", [])
    if len(requests) != 1:
        raise RuntimeError("Expected exactly one MVP approval request.")
    gates = gates_doc.get("gates", [])
    if len(gates) != 1:
        raise RuntimeError("MVP approval request expects one transition gate.")
    gate = gates[0]

    request = requests[0]
    if request.get("gate_id") != gate.get("id"):
        raise RuntimeError("MVP approval request must reference the transition gate.")
    if request.get("checklist_id") != checklist_doc.get("id"):
        raise RuntimeError("MVP approval request must reference the adaptation checklist.")
    if request.get("decision_state") != "approved_for_adapted_draft_creation":
        raise RuntimeError("MVP approval request decision must be approved for draft creation only.")
    if request.get("approval_recorded") is not True:
        raise RuntimeError("MVP approval request must record approval.")
    if request.get("approval_event_id") != "mvp02-owner-approval-2026-06-27-adapted-draft":
        raise RuntimeError("MVP approval request approval event mismatch.")
    if request.get("adapted_draft_record") != "registry/mvp02-adapted-drafts.json":
        raise RuntimeError("MVP approval request adapted draft record mismatch.")
    if request.get("approval_event_id") not in {
        event.get("id")
        for event in approval_events_doc.get("events", [])
        if isinstance(event, dict)
    }:
        raise RuntimeError("MVP approval request event is not recorded.")
    if adapted_drafts_doc.get("approval_request_id") != request.get("id"):
        raise RuntimeError("MVP approval request does not match adapted draft record.")

    gate_candidates = {
        candidate.get("candidate_id")
        for candidate in gate.get("candidates", [])
        if isinstance(candidate, dict)
    }
    request_candidates = set(request.get("candidate_ids", []))
    if request_candidates != gate_candidates:
        raise RuntimeError("MVP approval request candidates must match transition gate.")

    current_permissions = request.get("current_permissions", {})
    for key in [
        "adapted_output_allowed",
        "approved_payload_allowed",
        "release_manifest_allowed",
        "routing_projection_allowed",
        "live_install_allowed",
        "source_text_redistribution_allowed",
    ]:
        expected = key == "adapted_output_allowed"
        if current_permissions.get(key) is not expected:
            raise RuntimeError(f"MVP approval request permission mismatch: {key}")

    required_requested_scope = {
        "create adapted draft output in a non-runtime review surface",
        "apply the MVP-02 adaptation review checklist",
        "record candidate-specific disposition evidence",
    }
    requested_scope = set(request.get("requested_scope_if_approved", []))
    if not required_requested_scope <= requested_scope:
        raise RuntimeError("MVP approval request missing required requested scope.")

    required_not_requested = {
        "edit skills/",
        "update release-manifest.json",
        "update generated routing projections",
        "install or sync live Agent environments",
        "approve, release, or publish any candidate payload",
    }
    not_requested = set(request.get("explicitly_not_requested", []))
    if not required_not_requested <= not_requested:
        raise RuntimeError("MVP approval request missing explicit non-scope boundaries.")

    if not request.get("safe_approval_phrases"):
        raise RuntimeError("MVP approval request must provide safe approval phrases.")
    if not request.get("next_state_if_approved"):
        raise RuntimeError("MVP approval request must state next state if approved.")

    doc_path = request.get("evidence_doc")
    if doc_path != "docs/mvp02-adaptation-approval-request.md":
        raise RuntimeError("MVP approval request evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "Request record, not release approval",
        "Current decision: approved for adapted draft creation only",
        "Adapted output exists only under `drafts/mvp02-adaptation/`",
        "Approved scope",
        "Explicitly not approved",
        "Safe approval phrases",
        "批准进入 MVP-02 适配草案阶段",
        "The next state is adapted-output drafting",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"MVP approval request doc missing phrase: {phrase}")


def validate_mvp02_preflight_readiness(
    preflight_doc: dict[str, object],
    batches_doc: dict[str, object],
    reviews_doc: dict[str, object],
    gates_doc: dict[str, object],
    checklist_doc: dict[str, object],
    requests_doc: dict[str, object],
    approval_events_doc: dict[str, object],
    adapted_drafts_doc: dict[str, object],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if preflight_doc.get("schema_version") != 1:
        raise RuntimeError("MVP-02 preflight readiness schema_version must be 1.")
    if preflight_doc.get("status") != "preflight_consumed_by_owner_approval":
        raise RuntimeError("MVP-02 preflight readiness must be consumed by owner approval.")
    if preflight_doc.get("not_approval") is not True:
        raise RuntimeError("MVP-02 preflight readiness must explicitly not be approval.")
    if preflight_doc.get("approval_recorded") is not True:
        raise RuntimeError("MVP-02 preflight readiness must record the approval event.")
    if preflight_doc.get("adapted_output_present") is not True:
        raise RuntimeError("MVP-02 preflight readiness must record adapted output.")

    batches = batches_doc.get("batches", [])
    reviews = reviews_doc.get("reviews", [])
    gates = gates_doc.get("gates", [])
    requests = requests_doc.get("requests", [])
    if len(batches) != 1 or len(reviews) != 1 or len(gates) != 1 or len(requests) != 1:
        raise RuntimeError("MVP-02 preflight readiness expects one batch, review, gate, and request.")
    batch = batches[0]
    review = reviews[0]
    gate = gates[0]
    request = requests[0]
    if preflight_doc.get("batch_id") != batch.get("id"):
        raise RuntimeError("MVP-02 preflight readiness batch mismatch.")
    if preflight_doc.get("review_id") != review.get("id"):
        raise RuntimeError("MVP-02 preflight readiness review mismatch.")
    if preflight_doc.get("gate_id") != gate.get("id"):
        raise RuntimeError("MVP-02 preflight readiness gate mismatch.")
    if preflight_doc.get("checklist_id") != checklist_doc.get("id"):
        raise RuntimeError("MVP-02 preflight readiness checklist mismatch.")
    if preflight_doc.get("approval_request_id") != request.get("id"):
        raise RuntimeError("MVP-02 preflight readiness approval request mismatch.")
    if preflight_doc.get("approval_event_id") != "mvp02-owner-approval-2026-06-27-adapted-draft":
        raise RuntimeError("MVP-02 preflight readiness approval event mismatch.")
    if preflight_doc.get("adapted_draft_record") != "registry/mvp02-adapted-drafts.json":
        raise RuntimeError("MVP-02 preflight readiness adapted draft record mismatch.")
    if preflight_doc.get("approval_event_id") not in {
        event.get("id")
        for event in approval_events_doc.get("events", [])
        if isinstance(event, dict)
    }:
        raise RuntimeError("MVP-02 preflight readiness approval event is not recorded.")
    if adapted_drafts_doc.get("batch_id") != batch.get("id"):
        raise RuntimeError("MVP-02 preflight readiness adapted draft batch mismatch.")

    batch_candidates = {
        candidate.get("candidate_id")
        for candidate in batch.get("candidates", [])
        if isinstance(candidate, dict)
    }
    request_candidates = set(request.get("candidate_ids", []))
    preflight_candidates = set(preflight_doc.get("candidate_ids", []))
    if preflight_candidates != batch_candidates or preflight_candidates != request_candidates:
        raise RuntimeError("MVP-02 preflight readiness candidate set mismatch.")

    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = "\n".join(
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    )
    for candidate_id in preflight_candidates:
        if candidate_id in approved_directories:
            raise RuntimeError(f"MVP-02 preflight candidate already approved: {candidate_id}")
        if f"skills/{candidate_id}/" in manifest_paths:
            raise RuntimeError(f"MVP-02 preflight candidate appears in release manifest: {candidate_id}")

    for source, label in [
        (batch, "batch"),
        (review, "review"),
        (gate, "gate"),
        (request, "request"),
    ]:
        if source.get("runtime_allowed") is True:
            raise RuntimeError(f"MVP-02 preflight {label} unexpectedly allows runtime.")
        if source.get("release_manifest_allowed") is True:
            raise RuntimeError(f"MVP-02 preflight {label} unexpectedly allows release manifest.")
        if source.get("routing_projection_allowed") is True:
            raise RuntimeError(f"MVP-02 preflight {label} unexpectedly allows routing projection.")

    if gate.get("current_human_approval_recorded") is not True:
        raise RuntimeError("MVP-02 preflight gate must have bounded human approval recorded.")
    if request.get("approval_recorded") is not True:
        raise RuntimeError("MVP-02 preflight request must have approval recorded.")

    for permissions in [
        gate.get("current_permissions", {}),
        request.get("current_permissions", {}),
        preflight_doc.get("current_permissions", {}),
    ]:
        for key, value in permissions.items():
            expected = key == "adapted_output_allowed"
            if value is not expected:
                raise RuntimeError(f"MVP-02 preflight permission mismatch: {key}")

    required_check_ids = {
        "selected_batch_recorded",
        "pre_adaptation_review_recorded",
        "transition_gate_approval_consumed",
        "review_checklist_template_ready",
        "approval_request_approved_for_draft_only",
        "no_candidate_payload_released",
        "next_action_is_next_gate",
    }
    actual_check_ids = {
        item.get("id")
        for item in preflight_doc.get("preflight_checks", [])
        if isinstance(item, dict)
    }
    if required_check_ids != actual_check_ids:
        raise RuntimeError("MVP-02 preflight checks do not match required set.")
    for item in preflight_doc.get("preflight_checks", []):
        if item.get("status") != "pass":
            raise RuntimeError(f"MVP-02 preflight check is not pass: {item.get('id')}")
        if not item.get("evidence") or not item.get("meaning"):
            raise RuntimeError(f"MVP-02 preflight check missing evidence or meaning: {item.get('id')}")

    safe_phrases = set(preflight_doc.get("safe_approval_phrases", []))
    if safe_phrases != set(request.get("safe_approval_phrases", [])):
        raise RuntimeError("MVP-02 preflight safe approval phrases must match request.")
    if preflight_doc.get("next_state_if_approved") != request.get("next_state_if_approved"):
        raise RuntimeError("MVP-02 preflight next state must match request.")
    required_disallowed = {
        "edit skills/",
        "update release-manifest.json",
        "update generated routing projections",
        "install or sync live Agent environments",
        "approve, release, or publish any candidate payload",
        "redistribute upstream source text as approved curated payload",
    }
    if set(preflight_doc.get("still_disallowed", [])) != required_disallowed:
        raise RuntimeError("MVP-02 preflight still_disallowed list drifted.")
    if preflight_doc.get("preflight_result") != "owner_approval_received_and_adapted_draft_created":
        raise RuntimeError("MVP-02 preflight result is unexpected.")

    doc_path = preflight_doc.get("evidence_doc")
    if doc_path != "docs/mvp02-preflight-readiness.md":
        raise RuntimeError("MVP-02 preflight evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "historical readiness record, not release approval",
        "preflight_consumed_by_owner_approval",
        "approval recorded: true",
        "adapted output present: true",
        "Candidates are not approved Skills",
        "Candidates are not in `release-manifest.json`",
        "Safe approval phrases",
        "Still disallowed",
        "release, routing, payload, live-install, and publication boundaries remain closed",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"MVP-02 preflight readiness doc missing phrase: {phrase}")


def validate_mvp02_post_approval_execution_plan(
    plan_doc: dict[str, object],
    preflight_doc: dict[str, object],
    batches_doc: dict[str, object],
    reviews_doc: dict[str, object],
    gates_doc: dict[str, object],
    checklist_doc: dict[str, object],
    requests_doc: dict[str, object],
    approval_events_doc: dict[str, object],
    adapted_drafts_doc: dict[str, object],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if plan_doc.get("schema_version") != 1:
        raise RuntimeError("MVP-02 post-approval execution plan schema_version must be 1.")
    if plan_doc.get("status") != "executed_after_owner_approval_stopped_before_release_gate":
        raise RuntimeError("MVP-02 post-approval execution plan must record execution stopped before release gate.")
    if plan_doc.get("not_approval") is not True:
        raise RuntimeError("MVP-02 post-approval execution plan must explicitly not be approval.")
    if plan_doc.get("approval_recorded") is not True:
        raise RuntimeError("MVP-02 post-approval execution plan must record approval.")
    if plan_doc.get("adapted_output_present") is not True:
        raise RuntimeError("MVP-02 post-approval execution plan must record adapted output.")

    planned_output_root = plan_doc.get("planned_output_root")
    if planned_output_root != "drafts/mvp02-adaptation/":
        raise RuntimeError("MVP-02 post-approval execution plan must use the declared draft root.")
    if not (ROOT / planned_output_root).is_dir():
        raise RuntimeError("MVP-02 planned output root must exist after approval.")

    batches = batches_doc.get("batches", [])
    reviews = reviews_doc.get("reviews", [])
    gates = gates_doc.get("gates", [])
    requests = requests_doc.get("requests", [])
    if len(batches) != 1 or len(reviews) != 1 or len(gates) != 1 or len(requests) != 1:
        raise RuntimeError("MVP-02 post-approval plan expects one batch, review, gate, and request.")
    batch = batches[0]
    review = reviews[0]
    gate = gates[0]
    request = requests[0]

    expected_refs = {
        "batch_id": batch.get("id"),
        "review_id": review.get("id"),
        "gate_id": gate.get("id"),
        "checklist_id": checklist_doc.get("id"),
        "approval_request_id": request.get("id"),
        "approval_event_id": "mvp02-owner-approval-2026-06-27-adapted-draft",
        "adapted_draft_record": "registry/mvp02-adapted-drafts.json",
        "preflight_record": "registry/mvp02-preflight-readiness.json",
    }
    for key, expected_value in expected_refs.items():
        if plan_doc.get(key) != expected_value:
            raise RuntimeError(f"MVP-02 post-approval execution plan reference mismatch: {key}")

    batch_candidates = {
        candidate.get("candidate_id")
        for candidate in batch.get("candidates", [])
        if isinstance(candidate, dict)
    }
    request_candidates = set(request.get("candidate_ids", []))
    plan_candidates = set(plan_doc.get("candidate_ids", []))
    preflight_candidates = set(preflight_doc.get("candidate_ids", []))
    if plan_candidates != batch_candidates or plan_candidates != request_candidates or plan_candidates != preflight_candidates:
        raise RuntimeError("MVP-02 post-approval execution plan candidate set mismatch.")

    if set(plan_doc.get("safe_approval_phrases", [])) != set(request.get("safe_approval_phrases", [])):
        raise RuntimeError("MVP-02 post-approval execution plan safe approval phrases must match request.")
    if plan_doc.get("approval_event_id") not in {
        event.get("id")
        for event in approval_events_doc.get("events", [])
        if isinstance(event, dict)
    }:
        raise RuntimeError("MVP-02 post-approval execution plan approval event is not recorded.")
    if adapted_drafts_doc.get("approval_event_id") != plan_doc.get("approval_event_id"):
        raise RuntimeError("MVP-02 post-approval execution plan adapted draft event mismatch.")
    if plan_doc.get("next_state_after_execution") != "adapted_draft_review_recorded_pending_next_gate":
        raise RuntimeError("MVP-02 post-approval execution plan next state is unexpected.")

    for permissions in [
        request.get("current_permissions", {}),
        preflight_doc.get("current_permissions", {}),
        plan_doc.get("current_permissions", {}),
        adapted_drafts_doc.get("current_permissions", {}),
    ]:
        for key, value in permissions.items():
            expected = key == "adapted_output_allowed"
            if value is not expected:
                raise RuntimeError(f"MVP-02 post-approval execution plan permission mismatch: {key}")

    required_steps = [
        "record_approval_event",
        "create_non_runtime_review_surface",
        "draft_candidate_adaptations",
        "complete_review_checklist",
        "run_verification",
        "stop_before_next_gate",
    ]
    actual_steps = [step.get("id") for step in plan_doc.get("execution_sequence_after_approval", [])]
    if actual_steps != required_steps:
        raise RuntimeError("MVP-02 post-approval execution plan step order changed.")
    for step in plan_doc.get("execution_sequence_after_approval", []):
        if not step.get("goal") or not step.get("must_verify"):
            raise RuntimeError(f"MVP-02 post-approval execution plan step missing goal or verification: {step.get('id')}")

    required_disallowed = {
        "edit skills/",
        "update release-manifest.json",
        "update generated routing projections",
        "install or sync live Agent environments",
        "approve, release, or publish any candidate payload",
        "redistribute upstream source text as approved curated payload",
    }
    if set(plan_doc.get("still_disallowed_until_next_gate", [])) != required_disallowed:
        raise RuntimeError("MVP-02 post-approval execution plan still_disallowed list drifted.")

    required_next_evidence = {
        "approval event record",
        "adapted draft location under planned_output_root",
        "completed checklist sections",
        "candidate-specific disposition",
        "verification command results",
        "explicit record that manifest, routing projection, and live install remain unchanged",
    }
    if set(plan_doc.get("next_required_evidence_after_execution", [])) != required_next_evidence:
        raise RuntimeError("MVP-02 post-approval execution plan next evidence changed.")
    if "Separate owner approval is required" not in str(plan_doc.get("next_required_gate")):
        raise RuntimeError("MVP-02 post-approval execution plan must record the next owner gate.")

    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = "\n".join(
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    )
    for candidate_id in plan_candidates:
        if candidate_id in approved_directories:
            raise RuntimeError(f"MVP-02 planned candidate unexpectedly approved: {candidate_id}")
        if f"skills/{candidate_id}/" in manifest_paths:
            raise RuntimeError(f"MVP-02 planned candidate appears in release manifest: {candidate_id}")

    doc_path = plan_doc.get("evidence_doc")
    if doc_path != "docs/mvp02-post-approval-execution-plan.md":
        raise RuntimeError("MVP-02 post-approval execution plan evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "This is an executed plan record, not release approval",
        "approval recorded: true",
        "adapted output present: true",
        "planned output root: drafts/mvp02-adaptation/",
        "non-runtime adapted draft creation",
        "Still disallowed until the next gate",
        "Stop before the next gate",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"MVP-02 post-approval execution plan doc missing phrase: {phrase}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link MVP-02 post-approval execution plan.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link MVP-02 post-approval execution plan.")
    if "docs/mvp02-adapted-draft-review.md" not in readme:
        raise RuntimeError("README.md must link MVP-02 adapted draft review.")
    if "docs/mvp02-adapted-draft-review.md" not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link MVP-02 adapted draft review.")


def validate_mvp02_approval_events(
    approval_events_doc: dict[str, object],
    requests_doc: dict[str, object],
) -> None:
    if approval_events_doc.get("schema_version") != 1:
        raise RuntimeError("MVP-02 approval events schema_version must be 1.")
    if approval_events_doc.get("status") != "owner_approval_recorded_for_adapted_draft_creation":
        raise RuntimeError("MVP-02 approval events status is unexpected.")
    if approval_events_doc.get("approval_recorded") is not True:
        raise RuntimeError("MVP-02 approval events must record approval.")
    if approval_events_doc.get("adapted_output_present") is not True:
        raise RuntimeError("MVP-02 approval events must record adapted output.")
    events = approval_events_doc.get("events", [])
    requests = requests_doc.get("requests", [])
    if len(events) != 1 or len(requests) != 1:
        raise RuntimeError("MVP-02 approval events expects one event and one request.")
    event = events[0]
    request = requests[0]
    if event.get("id") != "mvp02-owner-approval-2026-06-27-adapted-draft":
        raise RuntimeError("MVP-02 approval event id mismatch.")
    if event.get("approval_request_id") != request.get("id"):
        raise RuntimeError("MVP-02 approval event request mismatch.")
    if event.get("approval_phrase") not in request.get("safe_approval_phrases", []):
        raise RuntimeError("MVP-02 approval event phrase must match a safe approval phrase.")

    required_scope = {
        "create adapted draft output in a non-runtime review surface",
        "apply the MVP-02 adaptation review checklist",
        "record candidate-specific disposition evidence",
        "run focused security, portability, overlap, attribution, and validation review on the adapted draft",
    }
    if set(event.get("approved_scope", [])) != required_scope:
        raise RuntimeError("MVP-02 approval event approved scope drifted.")

    required_not_approved = {
        "edit skills/",
        "update release-manifest.json",
        "update generated routing projections",
        "install or sync live Agent environments",
        "approve, release, or publish any candidate payload",
        "redistribute upstream source text as approved curated payload",
    }
    if set(event.get("explicitly_not_approved", [])) != required_not_approved:
        raise RuntimeError("MVP-02 approval event non-scope boundaries drifted.")
    if event.get("next_state") != "adapted_output_drafting_in_non_runtime_review_surface":
        raise RuntimeError("MVP-02 approval event next state mismatch.")


def validate_mvp02_adapted_drafts(
    drafts_doc: dict[str, object],
    approval_events_doc: dict[str, object],
    batches_doc: dict[str, object],
    reviews_doc: dict[str, object],
    gates_doc: dict[str, object],
    checklist_doc: dict[str, object],
    requests_doc: dict[str, object],
    sources_doc: dict[str, object],
    selection_doc: dict[str, object],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if drafts_doc.get("schema_version") != 1:
        raise RuntimeError("MVP-02 adapted drafts schema_version must be 1.")
    if drafts_doc.get("status") != "adapted_draft_review_recorded_not_approved":
        raise RuntimeError("MVP-02 adapted drafts must remain non-approved.")
    if drafts_doc.get("draft_root") != "drafts/mvp02-adaptation/":
        raise RuntimeError("MVP-02 adapted drafts root mismatch.")
    draft_root = ROOT / drafts_doc["draft_root"]
    if not draft_root.is_dir():
        raise RuntimeError("MVP-02 adapted draft root missing.")
    if drafts_doc.get("evidence_doc") != "docs/mvp02-adapted-draft-review.md":
        raise RuntimeError("MVP-02 adapted draft evidence doc mismatch.")

    batches = batches_doc.get("batches", [])
    reviews = reviews_doc.get("reviews", [])
    gates = gates_doc.get("gates", [])
    requests = requests_doc.get("requests", [])
    events = approval_events_doc.get("events", [])
    if len(batches) != 1 or len(reviews) != 1 or len(gates) != 1 or len(requests) != 1 or len(events) != 1:
        raise RuntimeError("MVP-02 adapted drafts expects one batch, review, gate, request, and event.")
    batch = batches[0]
    review = reviews[0]
    gate = gates[0]
    request = requests[0]
    event = events[0]

    expected_refs = {
        "approval_event_id": event.get("id"),
        "approval_request_id": request.get("id"),
        "batch_id": batch.get("id"),
        "review_id": review.get("id"),
        "gate_id": gate.get("id"),
        "checklist_id": checklist_doc.get("id"),
    }
    for key, expected_value in expected_refs.items():
        if drafts_doc.get(key) != expected_value:
            raise RuntimeError(f"MVP-02 adapted draft reference mismatch: {key}")

    source = drafts_doc.get("source", {})
    source_records = {
        item.get("id"): item
        for item in sources_doc.get("sources", [])
        if isinstance(item, dict)
    }
    locked_source = source_records.get(UPSTREAM_SOURCE_ID)
    if source.get("id") != UPSTREAM_SOURCE_ID:
        raise RuntimeError("MVP-02 adapted drafts source mismatch.")
    if locked_source is None or source.get("revision") != locked_source.get("revision"):
        raise RuntimeError("MVP-02 adapted drafts revision must match source lock.")
    if source.get("revision") != selection_doc.get("revision"):
        raise RuntimeError("MVP-02 adapted drafts revision must match selection.")
    if source.get("license") != "MIT":
        raise RuntimeError("MVP-02 adapted drafts license must remain MIT.")

    permissions = drafts_doc.get("current_permissions", {})
    for key, value in permissions.items():
        expected = key == "adapted_output_allowed"
        if value is not expected:
            raise RuntimeError(f"MVP-02 adapted draft permission mismatch: {key}")

    batch_candidates = {
        candidate.get("candidate_id")
        for candidate in batch.get("candidates", [])
        if isinstance(candidate, dict)
    }
    review_candidates = {
        candidate.get("candidate_id"): candidate
        for candidate in review.get("candidates", [])
        if isinstance(candidate, dict)
    }
    draft_candidates = {
        candidate.get("candidate_id"): candidate
        for candidate in drafts_doc.get("candidate_drafts", [])
        if isinstance(candidate, dict)
    }
    if set(draft_candidates) != batch_candidates or set(draft_candidates) != set(review_candidates):
        raise RuntimeError("MVP-02 adapted draft candidates must match batch and review.")

    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = "\n".join(
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    )
    routing_text = (ROOT / "registry/routing.json").read_text(encoding="utf-8")
    allowed_dispositions = {"merge", "recipe-only", "adapter-only", "reject", "approved-payload-candidate"}
    for candidate_id, candidate in draft_candidates.items():
        if candidate_id in approved_directories:
            raise RuntimeError(f"MVP-02 adapted draft candidate unexpectedly approved: {candidate_id}")
        if f"skills/{candidate_id}/" in manifest_paths:
            raise RuntimeError(f"MVP-02 adapted draft candidate appears in release manifest: {candidate_id}")
        if candidate_id in routing_text:
            raise RuntimeError(f"MVP-02 adapted draft candidate appears as a direct curated routing surface: {candidate_id}")
        if candidate.get("upstream_path") != review_candidates[candidate_id].get("upstream_path"):
            raise RuntimeError(f"MVP-02 adapted draft upstream path drift: {candidate_id}")
        if candidate.get("upstream_sha256") != review_candidates[candidate_id].get("upstream_sha256"):
            raise RuntimeError(f"MVP-02 adapted draft upstream hash drift: {candidate_id}")
        draft_path = candidate.get("draft_path")
        if not isinstance(draft_path, str) or ".." in draft_path.replace("\\", "/"):
            raise RuntimeError(f"MVP-02 adapted draft path is unsafe: {candidate_id}")
        if not draft_path.startswith(drafts_doc["draft_root"]):
            raise RuntimeError(f"MVP-02 adapted draft path outside root: {candidate_id}")
        if not (ROOT / draft_path).is_file():
            raise RuntimeError(f"MVP-02 adapted draft file missing: {candidate_id}")
        if candidate.get("checklist_sections_complete") is not True:
            raise RuntimeError(f"MVP-02 adapted draft checklist incomplete: {candidate_id}")
        if candidate.get("source_text_copied") is not False:
            raise RuntimeError(f"MVP-02 adapted draft must not copy source text: {candidate_id}")
        if candidate.get("source_text_redistributed") is not False:
            raise RuntimeError(f"MVP-02 adapted draft must not redistribute source text: {candidate_id}")
        if candidate.get("disposition") not in allowed_dispositions:
            raise RuntimeError(f"MVP-02 adapted draft has invalid disposition: {candidate_id}")
        if candidate.get("next_gate") != "mvp03-release-or-routing-candidate-review":
            raise RuntimeError(f"MVP-02 adapted draft next gate mismatch: {candidate_id}")

        draft = (ROOT / draft_path).read_text(encoding="utf-8")
        for phrase in [
            "Status: non-runtime adapted draft, not approved payload.",
            "Source integrity",
            "License and attribution",
            "Security",
            "Portability and neutralization",
            "Overlap and conflict",
            "Routing and runtime boundary",
            "Validation",
            "Disposition",
            "release-manifest.json",
            "live Agent environments",
        ]:
            if phrase not in draft:
                raise RuntimeError(f"MVP-02 adapted draft missing phrase for {candidate_id}: {phrase}")

    validation = drafts_doc.get("validation", {})
    if validation.get("status") not in {"pending_command_run", "passed"}:
        raise RuntimeError("MVP-02 adapted draft validation status is invalid.")
    required_commands = {
        "python -B scripts/verify.py",
        "python -B scripts/build_topology.py --check",
        "python -B -m unittest discover -s tests -v",
    }
    if set(validation.get("required_commands", [])) != required_commands:
        raise RuntimeError("MVP-02 adapted draft required commands drifted.")
    for assertion in [
        "release-manifest.json remains unchanged",
        "generated routing projections remain unchanged",
        "skills/ remains unchanged",
        "live Agent environments are untouched",
    ]:
        if assertion not in validation.get("boundary_assertions", []):
            raise RuntimeError(f"MVP-02 adapted draft missing boundary assertion: {assertion}")
    if "Separate owner approval is required" not in str(drafts_doc.get("next_required_gate")):
        raise RuntimeError("MVP-02 adapted drafts must record next owner gate.")

    doc = (ROOT / drafts_doc["evidence_doc"]).read_text(encoding="utf-8")
    for phrase in [
        "adapted draft evidence, not release approval",
        "draft root: drafts/mvp02-adaptation/",
        "approved payload allowed: false",
        "release manifest allowed: false",
        "routing projection allowed: false",
        "live install allowed: false",
        "Candidate dispositions",
        "No upstream source body is copied as an approved curated payload",
        "Next gate",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"MVP-02 adapted draft review doc missing phrase: {phrase}")


def validate_mvp03_release_or_routing_preflight(
    preflight_doc: dict[str, object],
    adapted_drafts_doc: dict[str, object],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if preflight_doc.get("schema_version") != 1:
        raise RuntimeError("MVP-03 preflight schema_version must be 1.")
    if preflight_doc.get("status") != "release_or_routing_review_preflight_ready_not_approved":
        raise RuntimeError("MVP-03 preflight must remain review-ready but not approved.")
    if preflight_doc.get("not_approval") is not True:
        raise RuntimeError("MVP-03 preflight must explicitly avoid approval.")
    if preflight_doc.get("approval_recorded") is not False:
        raise RuntimeError("MVP-03 preflight must not record approval.")
    if preflight_doc.get("source_draft_record") != "registry/mvp02-adapted-drafts.json":
        raise RuntimeError("MVP-03 preflight must reference the MVP-02 adapted draft record.")
    if preflight_doc.get("review_template") != "registry/mvp03-release-or-routing-review-template.json":
        raise RuntimeError("MVP-03 preflight must reference the MVP-03 review template.")
    if preflight_doc.get("review_template_doc") != "docs/mvp03-release-or-routing-review-template.md":
        raise RuntimeError("MVP-03 preflight must reference the MVP-03 review template doc.")
    if preflight_doc.get("approval_request_record") != "registry/mvp03-release-or-routing-approval-request.json":
        raise RuntimeError("MVP-03 preflight must reference the MVP-03 approval request.")
    if preflight_doc.get("approval_request_doc") != "docs/mvp03-release-or-routing-approval-request.md":
        raise RuntimeError("MVP-03 preflight must reference the MVP-03 approval request doc.")
    if preflight_doc.get("gate_id") != "mvp03-release-or-routing-candidate-review":
        raise RuntimeError("MVP-03 preflight gate id mismatch.")

    candidate_ids = preflight_doc.get("candidate_ids", [])
    draft_candidates = {
        candidate.get("candidate_id"): candidate
        for candidate in adapted_drafts_doc.get("candidate_drafts", [])
        if isinstance(candidate, dict)
    }
    if set(candidate_ids) != set(draft_candidates):
        raise RuntimeError("MVP-03 preflight candidates must match MVP-02 adapted drafts.")

    permissions = preflight_doc.get("current_permissions", {})
    for key, value in permissions.items():
        expected = key == "release_review_scaffolding_allowed"
        if value is not expected:
            raise RuntimeError(f"MVP-03 preflight permission mismatch: {key}")

    required_checks = {
        "adapted_drafts_exist",
        "source_and_license_locked",
        "current_dispositions_recorded",
        "approved_inventory_unchanged",
        "manifest_and_routing_exclude_candidates",
        "next_gate_requires_owner_decision",
    }
    checks = preflight_doc.get("preflight_checks", [])
    actual_checks = {item.get("id") for item in checks if isinstance(item, dict)}
    if actual_checks != required_checks:
        raise RuntimeError("MVP-03 preflight checks changed.")
    for item in checks:
        if item.get("status") != "pass" or not item.get("evidence") or not item.get("meaning"):
            raise RuntimeError(f"MVP-03 preflight check is incomplete: {item.get('id')}")

    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = {item["path"] for item in manifest.get("files", [])}
    routing_text = (ROOT / "registry/routing.json").read_text(encoding="utf-8")
    review_targets = {
        item.get("candidate_id"): item
        for item in preflight_doc.get("candidate_review_targets", [])
        if isinstance(item, dict)
    }
    allowed_options = {
        "release-payload-candidate",
        "recipe-routing-proposal",
        "merge-into-existing-approved-skill",
        "reference-only",
        "reject",
    }
    if set(review_targets) != set(candidate_ids):
        raise RuntimeError("MVP-03 preflight review targets must match candidates.")
    for candidate_id in candidate_ids:
        if candidate_id in approved_directories:
            raise RuntimeError(f"MVP-03 candidate unexpectedly approved: {candidate_id}")
        if f"skills/{candidate_id}/" in manifest_paths:
            raise RuntimeError(f"MVP-03 candidate appears in release manifest: {candidate_id}")
        if candidate_id in routing_text:
            raise RuntimeError(f"MVP-03 candidate appears as a direct curated routing surface: {candidate_id}")
        target = review_targets[candidate_id]
        if target.get("current_disposition") != draft_candidates[candidate_id].get("disposition"):
            raise RuntimeError(f"MVP-03 candidate disposition mismatch: {candidate_id}")
        if target.get("review_status") != "pending_owner_approval":
            raise RuntimeError(f"MVP-03 candidate review must wait for owner approval: {candidate_id}")
        if not target.get("recommended_review_bias"):
            raise RuntimeError(f"MVP-03 candidate review bias missing: {candidate_id}")
        options = set(target.get("mvp03_decision_options", []))
        if not options or not options <= allowed_options:
            raise RuntimeError(f"MVP-03 candidate has invalid decision options: {candidate_id}")

    required_requested_scope = {
        "enter candidate-specific release-or-routing review for the three MVP-02 adapted drafts",
        "decide per draft whether it remains reference-only, becomes a recipe/routing proposal, merges into an existing approved Skill, becomes a release-payload candidate, or is rejected",
        "record the rationale, evidence, rejected alternatives, and next required gate for each candidate",
        "prepare proposed diffs only if the owner separately approves a manifest, routing, or approved-payload change",
    }
    if set(preflight_doc.get("requested_scope_if_approved", [])) != required_requested_scope:
        raise RuntimeError("MVP-03 preflight requested scope changed.")

    required_disallowed = {
        "edit skills/",
        "update release-manifest.json",
        "update generated routing projections",
        "install or sync live Agent environments",
        "approve, release, or publish any candidate payload",
        "redistribute upstream source text as approved curated payload",
    }
    if set(preflight_doc.get("explicitly_not_requested", [])) != required_disallowed:
        raise RuntimeError("MVP-03 preflight explicitly_not_requested changed.")
    if set(preflight_doc.get("still_disallowed", [])) != required_disallowed:
        raise RuntimeError("MVP-03 preflight still_disallowed changed.")
    if preflight_doc.get("safe_approval_phrases") != [
        "批准进入 MVP-03 release/routing 候选审查阶段",
        "Approve MVP-03 release-or-routing candidate review only",
    ]:
        raise RuntimeError("MVP-03 preflight safe approval phrases changed.")
    if preflight_doc.get("next_state_if_approved") != "release_or_routing_candidate_review":
        raise RuntimeError("MVP-03 preflight next state mismatch.")
    if preflight_doc.get("preflight_result") != "ready_to_request_owner_approval_for_mvp03_review_only":
        raise RuntimeError("MVP-03 preflight result mismatch.")

    doc_path = preflight_doc.get("evidence_doc")
    if doc_path != "docs/mvp03-release-or-routing-preflight.md":
        raise RuntimeError("MVP-03 preflight evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "This is a preflight and approval request, not approval.",
        "approval recorded: false",
        "Candidate IDs are not in `release-manifest.json`",
        "Requested approval scope",
        "批准进入 MVP-03 release/routing 候选审查阶段",
        "Approve MVP-03 release-or-routing candidate review only",
        "Still disallowed",
        "Candidate review bias",
        "Review template",
        "Approval request",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"MVP-03 preflight doc missing phrase: {phrase}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link MVP-03 preflight.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link MVP-03 preflight.")


def validate_mvp03_release_or_routing_review_template(
    template_doc: dict[str, object],
    preflight_doc: dict[str, object],
    adapted_drafts_doc: dict[str, object],
) -> None:
    if template_doc.get("schema_version") != 1:
        raise RuntimeError("MVP-03 review template schema_version must be 1.")
    if template_doc.get("status") != "template_only_not_candidate_decision":
        raise RuntimeError("MVP-03 review template must remain template-only.")
    if template_doc.get("not_approval") is not True:
        raise RuntimeError("MVP-03 review template must explicitly avoid approval.")
    if template_doc.get("approval_required_before_use") is not True:
        raise RuntimeError("MVP-03 review template must require approval before use.")
    if template_doc.get("source_preflight_record") != "registry/mvp03-release-or-routing-preflight.json":
        raise RuntimeError("MVP-03 review template must reference the preflight record.")
    if template_doc.get("source_draft_record") != "registry/mvp02-adapted-drafts.json":
        raise RuntimeError("MVP-03 review template must reference the adapted draft record.")

    candidate_ids = template_doc.get("candidate_ids", [])
    if candidate_ids != preflight_doc.get("candidate_ids"):
        raise RuntimeError("MVP-03 review template candidates must match preflight candidates.")
    draft_candidate_ids = [
        item.get("candidate_id")
        for item in adapted_drafts_doc.get("candidate_drafts", [])
        if isinstance(item, dict)
    ]
    if set(candidate_ids) != set(draft_candidate_ids):
        raise RuntimeError("MVP-03 review template candidates must match adapted drafts.")

    allowed_decisions = [
        "release-payload-candidate",
        "recipe-routing-proposal",
        "merge-into-existing-approved-skill",
        "reference-only",
        "reject",
    ]
    if template_doc.get("allowed_decisions_after_approval") != allowed_decisions:
        raise RuntimeError("MVP-03 review template decision enum changed.")
    required_sections = [
        "source_integrity",
        "license_and_attribution",
        "security",
        "portability_and_neutralization",
        "overlap_and_conflict",
        "native_or_runtime_equivalence",
        "routing_semantics",
        "release_manifest_impact",
        "consumer_install_impact",
        "validation_plan",
        "rejected_alternatives",
        "next_gate",
    ]
    if template_doc.get("required_review_sections") != required_sections:
        raise RuntimeError("MVP-03 review template sections changed.")

    decision_rules = template_doc.get("decision_rules", [])
    if {item.get("decision") for item in decision_rules if isinstance(item, dict)} != set(allowed_decisions):
        raise RuntimeError("MVP-03 review template must define every allowed decision.")
    for item in decision_rules:
        if not item.get("requires"):
            raise RuntimeError(f"MVP-03 decision rule missing requirements: {item.get('decision')}")

    required_fail_closed = {
        "owner approval for MVP-03 review is missing",
        "candidate source revision or upstream hash differs from MVP-02 evidence",
        "license, provenance, attribution, or redistribution posture is unclear",
        "security, portability, overlap, or native/runtime equivalence review is incomplete",
        "candidate would override repository, runtime, or human authority",
        "candidate would enter skills/, release-manifest.json, generated routing, or live environment before its later specific gate",
        "candidate decision is based only on enthusiasm, source popularity, or broad usefulness without evidence",
    }
    if set(template_doc.get("fail_closed_conditions", [])) != required_fail_closed:
        raise RuntimeError("MVP-03 review template fail-closed conditions changed.")

    permissions = template_doc.get("current_permissions", {})
    for key, value in permissions.items():
        expected = key == "template_allowed"
        if value is not expected:
            raise RuntimeError(f"MVP-03 review template permission mismatch: {key}")

    output_contract = template_doc.get("output_contract_after_approval", {})
    required_output = {
        "decision",
        "rationale",
        "evidence",
        "rejected_alternatives",
        "boundary_assertions",
        "validation_results",
        "next_gate",
    }
    if set(output_contract.get("must_include", [])) != required_output:
        raise RuntimeError("MVP-03 review template output contract changed.")
    if "candidate_decisions" not in output_contract:
        raise RuntimeError("MVP-03 review template must define candidate_decisions output.")

    doc_path = template_doc.get("evidence_doc")
    if doc_path != "docs/mvp03-release-or-routing-review-template.md":
        raise RuntimeError("MVP-03 review template evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "Template only, not approval.",
        "Without that approval, this document remains scaffolding.",
        "Allowed decisions after approval",
        "does not by itself mutate `skills/`, `release-manifest.json`, generated",
        "Fail-closed conditions",
        "Output contract after approval",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"MVP-03 review template doc missing phrase: {phrase}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link MVP-03 review template.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link MVP-03 review template.")


def validate_mvp03_release_or_routing_approval_request(
    request_doc: dict[str, object],
    preflight_doc: dict[str, object],
    template_doc: dict[str, object],
) -> None:
    if request_doc.get("schema_version") != 1:
        raise RuntimeError("MVP-03 approval request schema_version must be 1.")
    if request_doc.get("id") != preflight_doc.get("approval_request_id"):
        raise RuntimeError("MVP-03 approval request id must match preflight.")
    if request_doc.get("status") != "awaiting_owner_approval":
        raise RuntimeError("MVP-03 approval request must await owner approval.")
    if request_doc.get("not_approval") is not True:
        raise RuntimeError("MVP-03 approval request must explicitly avoid approval.")
    if request_doc.get("approval_recorded") is not False:
        raise RuntimeError("MVP-03 approval request must not record approval.")
    if request_doc.get("source_preflight_record") != "registry/mvp03-release-or-routing-preflight.json":
        raise RuntimeError("MVP-03 approval request must reference the preflight.")
    if request_doc.get("review_template") != template_doc.get("evidence_doc", "").replace("docs/", "registry/").replace(".md", ".json"):
        raise RuntimeError("MVP-03 approval request must reference the review template.")
    if request_doc.get("candidate_ids") != preflight_doc.get("candidate_ids"):
        raise RuntimeError("MVP-03 approval request candidates must match preflight.")

    permissions = request_doc.get("current_permissions", {})
    for key, value in permissions.items():
        expected = key == "approval_request_allowed"
        if value is not expected:
            raise RuntimeError(f"MVP-03 approval request permission mismatch: {key}")

    required_requested_scope = {
        "enter candidate-specific release-or-routing review for the three MVP-02 adapted drafts",
        "apply the MVP-03 review template to record a decision for each candidate",
        "decide per draft whether it remains reference-only, becomes a recipe/routing proposal, merges into an existing approved Skill, becomes a release-payload candidate, or is rejected",
        "record rationale, evidence, rejected alternatives, boundary assertions, validation results, and next gate for each candidate",
    }
    if set(request_doc.get("requested_scope_if_approved", [])) != required_requested_scope:
        raise RuntimeError("MVP-03 approval request requested scope changed.")

    required_disallowed = {
        "edit skills/",
        "update release-manifest.json",
        "update generated routing projections",
        "install or sync live Agent environments",
        "approve, release, or publish any candidate payload",
        "redistribute upstream source text as approved curated payload",
    }
    if set(request_doc.get("explicitly_not_requested", [])) != required_disallowed:
        raise RuntimeError("MVP-03 approval request explicitly_not_requested changed.")
    if set(request_doc.get("still_disallowed", [])) != required_disallowed:
        raise RuntimeError("MVP-03 approval request still_disallowed changed.")
    if request_doc.get("safe_approval_phrases") != preflight_doc.get("safe_approval_phrases"):
        raise RuntimeError("MVP-03 approval request safe approval phrases must match preflight.")
    if request_doc.get("next_state_if_approved") != "release_or_routing_candidate_review":
        raise RuntimeError("MVP-03 approval request next state mismatch.")

    required_next_evidence = {
        "owner approval event record",
        "candidate-specific release/routing disposition record",
        "rationale for release payload, recipe/routing proposal, merge, reference-only, or reject",
        "verification command results",
        "explicit record that live install, publication, and source redistribution remain unchanged unless separately approved",
    }
    if set(request_doc.get("next_required_evidence_if_approved", [])) != required_next_evidence:
        raise RuntimeError("MVP-03 approval request next required evidence changed.")

    doc_path = request_doc.get("evidence_doc")
    if doc_path != "docs/mvp03-release-or-routing-approval-request.md":
        raise RuntimeError("MVP-03 approval request evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "This is an approval request, not approval.",
        "approval recorded: false",
        "candidate review allowed: false",
        "Requested approval",
        "批准进入 MVP-03 release/routing 候选审查阶段",
        "Approve MVP-03 release-or-routing candidate review only",
        "Explicitly not requested",
        "Until the approval event exists, MVP-03 remains preflight-only",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"MVP-03 approval request doc missing phrase: {phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link MVP-03 approval request.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link MVP-03 approval request.")


def validate_mvp03_approval_events(
    events_doc: dict[str, object],
    request_doc: dict[str, object],
) -> None:
    if events_doc.get("schema_version") != 1:
        raise RuntimeError("MVP-03 approval events schema_version must be 1.")
    if events_doc.get("status") != "owner_approval_recorded_for_release_or_routing_candidate_review":
        raise RuntimeError("MVP-03 approval events status mismatch.")
    expected_flags = {
        "approval_recorded": True,
        "candidate_review_allowed": True,
        "approved_payload_allowed": False,
        "release_manifest_allowed": False,
        "routing_projection_allowed": False,
        "live_install_allowed": False,
        "source_text_redistribution_allowed": False,
    }
    for key, expected in expected_flags.items():
        if events_doc.get(key) is not expected:
            raise RuntimeError(f"MVP-03 approval event flag mismatch: {key}")

    events = events_doc.get("events", [])
    if not isinstance(events, list) or len(events) != 1:
        raise RuntimeError("MVP-03 approval events must contain exactly one event.")
    event = events[0]
    if not isinstance(event, dict):
        raise RuntimeError("MVP-03 approval event must be an object.")
    if event.get("id") != "mvp03-owner-approval-2026-06-27-release-or-routing-candidate-review":
        raise RuntimeError("MVP-03 approval event id mismatch.")
    if event.get("approval_phrase") != "批准进入 MVP-03 release/routing 候选审查阶段":
        raise RuntimeError("MVP-03 approval event phrase mismatch.")
    if event.get("approval_request_id") != request_doc.get("id"):
        raise RuntimeError("MVP-03 approval event must reference the request id.")
    if set(event.get("approved_scope", [])) != set(request_doc.get("requested_scope_if_approved", [])):
        raise RuntimeError("MVP-03 approval event scope must match the request.")
    if set(event.get("explicitly_not_approved", [])) != set(request_doc.get("explicitly_not_requested", [])):
        raise RuntimeError("MVP-03 approval event disallowed scope must match the request.")
    if event.get("next_state") != request_doc.get("next_state_if_approved"):
        raise RuntimeError("MVP-03 approval event next_state mismatch.")


def validate_mvp03_release_or_routing_candidate_review(
    review_doc: dict[str, object],
    approval_events_doc: dict[str, object],
    preflight_doc: dict[str, object],
    template_doc: dict[str, object],
    adapted_drafts_doc: dict[str, object],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if review_doc.get("schema_version") != 1:
        raise RuntimeError("MVP-03 candidate review schema_version must be 1.")
    if review_doc.get("status") != "candidate_review_recorded_not_release_approved":
        raise RuntimeError("MVP-03 candidate review status mismatch.")
    if review_doc.get("approval_request_id") != preflight_doc.get("approval_request_id"):
        raise RuntimeError("MVP-03 candidate review request id mismatch.")
    event_ids = {
        event.get("id")
        for event in approval_events_doc.get("events", [])
        if isinstance(event, dict)
    }
    if review_doc.get("approval_event_id") not in event_ids:
        raise RuntimeError("MVP-03 candidate review must reference a recorded approval event.")
    if review_doc.get("source_preflight_record") != "registry/mvp03-release-or-routing-preflight.json":
        raise RuntimeError("MVP-03 candidate review must reference the preflight record.")
    if review_doc.get("review_template") != "registry/mvp03-release-or-routing-review-template.json":
        raise RuntimeError("MVP-03 candidate review must reference the review template.")
    if review_doc.get("source_draft_record") != "registry/mvp02-adapted-drafts.json":
        raise RuntimeError("MVP-03 candidate review must reference the adapted draft record.")

    candidate_ids = review_doc.get("candidate_ids", [])
    if candidate_ids != preflight_doc.get("candidate_ids") or candidate_ids != template_doc.get("candidate_ids"):
        raise RuntimeError("MVP-03 candidate review candidates must match preflight and template.")
    draft_candidates = {
        item.get("candidate_id"): item
        for item in adapted_drafts_doc.get("candidate_drafts", [])
        if isinstance(item, dict)
    }
    if set(candidate_ids) != set(draft_candidates):
        raise RuntimeError("MVP-03 candidate review candidates must match adapted drafts.")

    permissions = review_doc.get("current_permissions", {})
    for key, value in permissions.items():
        expected = key == "candidate_review_allowed"
        if value is not expected:
            raise RuntimeError(f"MVP-03 candidate review permission mismatch: {key}")

    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = {
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    }
    routing_text = (ROOT / "registry/routing.json").read_text(encoding="utf-8")
    decisions = {
        item.get("candidate_id"): item
        for item in review_doc.get("candidate_decisions", [])
        if isinstance(item, dict)
    }
    if set(decisions) != set(candidate_ids):
        raise RuntimeError("MVP-03 candidate review must contain one decision per candidate.")

    expected_decisions = {
        "spec-driven-development": "recipe-routing-proposal",
        "documentation-and-adrs": "merge-into-existing-approved-skill",
        "code-review-and-quality": "merge-into-existing-approved-skill",
    }
    allowed_decisions = set(template_doc.get("allowed_decisions_after_approval", []))
    required_sections = set(template_doc.get("required_review_sections", []))
    required_boundaries = {
        "skills/ unchanged",
        "release-manifest.json unchanged",
        "generated routing projections unchanged",
        "live Agent environments untouched",
        "source text not redistributed",
        "candidate decision is not approved payload",
    }
    for candidate_id, decision in decisions.items():
        if candidate_id in approved_directories:
            raise RuntimeError(f"MVP-03 candidate unexpectedly approved: {candidate_id}")
        if f"skills/{candidate_id}/" in manifest_paths:
            raise RuntimeError(f"MVP-03 candidate appears in release manifest: {candidate_id}")
        if candidate_id in routing_text:
            raise RuntimeError(f"MVP-03 candidate appears as a direct curated routing surface: {candidate_id}")
        if decision.get("decision") != expected_decisions[candidate_id]:
            raise RuntimeError(f"MVP-03 candidate decision mismatch: {candidate_id}")
        if decision.get("decision") not in allowed_decisions:
            raise RuntimeError(f"MVP-03 candidate decision is outside template enum: {candidate_id}")
        if not decision.get("rationale"):
            raise RuntimeError(f"MVP-03 candidate rationale missing: {candidate_id}")
        if not decision.get("rejected_alternatives"):
            raise RuntimeError(f"MVP-03 candidate rejected alternatives missing: {candidate_id}")
        if not decision.get("next_gate") or "separate" not in str(decision.get("next_gate")).lower():
            raise RuntimeError(f"MVP-03 candidate must require a separate next gate: {candidate_id}")
        if set(decision.get("boundary_assertions", [])) != required_boundaries:
            raise RuntimeError(f"MVP-03 candidate boundary assertions mismatch: {candidate_id}")
        review_sections = decision.get("review_sections", {})
        if set(review_sections) != required_sections:
            raise RuntimeError(f"MVP-03 candidate review sections mismatch: {candidate_id}")
        for field in [
            "source_integrity",
            "license_and_attribution",
            "security",
            "portability_and_neutralization",
            "overlap_and_conflict",
            "native_or_runtime_equivalence",
            "routing_semantics",
        ]:
            if review_sections.get(field) != "pass":
                raise RuntimeError(f"MVP-03 candidate review section did not pass: {candidate_id}/{field}")
        if review_sections.get("release_manifest_impact") != "no_manifest_change":
            raise RuntimeError(f"MVP-03 candidate manifest impact mismatch: {candidate_id}")
        if review_sections.get("consumer_install_impact") != "no_install_change":
            raise RuntimeError(f"MVP-03 candidate install impact mismatch: {candidate_id}")
        if review_sections.get("validation_plan") not in {"pending_final_run", "passed"}:
            raise RuntimeError(f"MVP-03 candidate validation plan mismatch: {candidate_id}")
        if review_sections.get("rejected_alternatives") != "recorded":
            raise RuntimeError(f"MVP-03 candidate rejected alternatives section mismatch: {candidate_id}")
        for evidence_path in decision.get("evidence", []):
            if not isinstance(evidence_path, str) or not (ROOT / evidence_path).is_file():
                raise RuntimeError(f"MVP-03 candidate has dead evidence ref: {candidate_id}/{evidence_path}")
        validation_results = decision.get("validation_results", [])
        if not validation_results:
            raise RuntimeError(f"MVP-03 candidate validation results missing: {candidate_id}")
        commands = {
            item.get("command")
            for item in validation_results
            if isinstance(item, dict)
        }
        if "python -B scripts/verify.py" not in commands:
            raise RuntimeError(f"MVP-03 candidate must record verify.py validation: {candidate_id}")

    validation = review_doc.get("validation", {})
    if validation.get("status") not in {"pending_final_run", "passed"}:
        raise RuntimeError("MVP-03 candidate review validation status is invalid.")
    required_commands = {
        "python -B scripts/verify.py",
        "python -B scripts/build_topology.py --check",
        "python -B scripts/build_release_manifest.py --check",
        "python -B scripts/simulate_routing.py --all",
        "python -B -m unittest discover -s tests -v",
    }
    if set(validation.get("required_commands", [])) != required_commands:
        raise RuntimeError("MVP-03 candidate review required commands drifted.")
    for assertion in [
        "release-manifest.json remains unchanged",
        "generated routing projections remain unchanged",
        "skills/ remains unchanged",
        "live Agent environments are untouched",
        "source text is not redistributed as approved curated payload",
    ]:
        if assertion not in validation.get("boundary_assertions", []):
            raise RuntimeError(f"MVP-03 candidate review missing boundary assertion: {assertion}")
    if "Separate approval is required" not in str(review_doc.get("next_required_gate")):
        raise RuntimeError("MVP-03 candidate review must record a separate next gate.")

    doc_path = review_doc.get("evidence_doc")
    if doc_path != "docs/mvp03-release-or-routing-candidate-review.md":
        raise RuntimeError("MVP-03 candidate review evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "candidate review evidence, not release approval",
        "approval phrase: 批准进入 MVP-03 release/routing 候选审查阶段",
        "approved payload allowed: false",
        "release manifest allowed: false",
        "routing projection allowed: false",
        "live install allowed: false",
        "Candidate decisions",
        "Rejected alternatives",
        "Boundary checks",
        "Next gates",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"MVP-03 candidate review doc missing phrase: {phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link MVP-03 candidate review.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link MVP-03 candidate review.")


def validate_mvp03_release_routing_execution(
    execution_doc: dict[str, object],
    candidate_review_doc: dict[str, object],
    skills_doc: dict[str, object],
    capabilities_doc: dict[str, object],
    recipes_doc: dict[str, object],
    relations_doc: dict[str, object],
    routing_doc: dict[str, object],
    scenarios_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if execution_doc.get("schema_version") != 1:
        raise RuntimeError("MVP-03 execution schema_version must be 1.")
    if execution_doc.get("status") != "curated_release_and_routing_ready_for_consumer_install":
        raise RuntimeError("MVP-03 execution status mismatch.")
    if execution_doc.get("source_candidate_review") != "registry/mvp03-release-or-routing-candidate-review.json":
        raise RuntimeError("MVP-03 execution must reference the candidate review record.")
    if execution_doc.get("approval_phrase") != "routing projection proposal、merge proposal、approved payload diff、manifest change 或 runtime install proof全部批准。":
        raise RuntimeError("MVP-03 execution approval phrase mismatch.")

    scope = execution_doc.get("authorized_scope", {})
    expected_scope = {
        "routing_projection_proposal_allowed": True,
        "merge_proposal_allowed": True,
        "approved_payload_diff_allowed": True,
        "release_manifest_allowed": True,
        "runtime_install_proof_allowed": True,
        "new_source_discovery_allowed": False,
        "third_party_source_import_allowed": False,
        "official_skill_vendoring_allowed": False,
        "public_promotion_allowed": False,
        "source_text_redistribution_allowed": False,
    }
    if scope != expected_scope:
        raise RuntimeError("MVP-03 execution authorized scope drifted.")

    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = {
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    }
    for candidate_id in candidate_review_doc.get("candidate_ids", []):
        if candidate_id in approved_directories:
            raise RuntimeError(f"MVP-03 execution must not add standalone Skill directory: {candidate_id}")
        if f"skills/{candidate_id}/" in manifest_paths:
            raise RuntimeError(f"MVP-03 execution must not manifest standalone candidate: {candidate_id}")

    capabilities = {
        item.get("id"): item
        for item in capabilities_doc.get("capabilities", [])
        if isinstance(item, dict)
    }
    spec_capability = capabilities.get("capability.spec-driven-development")
    if not spec_capability or spec_capability.get("coverageState") != "recipe":
        raise RuntimeError("MVP-03 execution must model spec-driven-development as recipe coverage.")

    recipes = {
        item.get("id"): item
        for item in recipes_doc.get("recipes", [])
        if isinstance(item, dict)
    }
    spec_recipe = recipes.get("recipe.spec-driven-development")
    if not spec_recipe:
        raise RuntimeError("MVP-03 execution must define recipe.spec-driven-development.")
    spec_steps = {
        step.get("capability")
        for step in spec_recipe.get("steps", [])
        if isinstance(step, dict)
    }
    for required_capability in {
        "capability.requirements-clarification",
        "capability.prd-rfc",
        "capability.problem-decomposition",
        "capability.test-strategy",
        "capability.tdd",
        "capability.code-review",
        "capability.release-readiness",
    }:
        if required_capability not in spec_steps:
            raise RuntimeError(f"MVP-03 spec recipe missing step: {required_capability}")

    relations = {
        (item.get("from"), item.get("type"), item.get("to"))
        for item in relations_doc.get("relations", [])
        if isinstance(item, dict)
    }
    for required_relation in {
        ("capability.spec-driven-development", "triggers", "capability.requirements-clarification"),
        ("capability.spec-driven-development", "precedes", "capability.problem-decomposition"),
        ("capability.spec-driven-development", "constrains", "capability.test-strategy"),
        ("capability.spec-driven-development", "validates", "capability.release-readiness"),
    }:
        if required_relation not in relations:
            raise RuntimeError(f"MVP-03 spec relation missing: {required_relation}")

    scenarios = {
        item.get("id"): item
        for item in scenarios_doc.get("scenarios", [])
        if isinstance(item, dict)
    }
    for scenario_id in {
        "scenario.spec-driven-development-recipe-01",
        "scenario.spec-driven-development-recipe-02",
    }:
        scenario = scenarios.get(scenario_id)
        if not scenario or scenario.get("expectedDecision") != "recipe":
            raise RuntimeError(f"MVP-03 spec scenario missing or not recipe: {scenario_id}")
        if "recipe.spec-driven-development" not in scenario.get("expectedSkills", []):
            raise RuntimeError(f"MVP-03 spec scenario missing recipe selection: {scenario_id}")

    routes = {
        item.get("skill"): item
        for item in routing_doc.get("routes", [])
        if isinstance(item, dict)
    }
    grill_route = routes.get("skill.curated.grill-with-docs")
    review_route = routes.get("skill.curated.review")
    if not grill_route or "ADR or documentation update proposal with context, decision, alternatives, consequences, status, supersession path, and evidence when warranted." not in grill_route.get("outputs", []):
        raise RuntimeError("MVP-03 documentation/ADR routing merge is missing.")
    if not review_route or "Quality-axis escalation notes when security, performance, observability, CI/CD, migration, or release readiness should own the next pass." not in review_route.get("outputs", []):
        raise RuntimeError("MVP-03 code-review/quality routing merge is missing.")

    skill_checks = {
        "skills/grill-with-docs/SKILL.md": "Preserve documentation authority",
        "skills/review/SKILL.md": "Review depth",
    }
    for path, phrase in skill_checks.items():
        if phrase not in (ROOT / path).read_text(encoding="utf-8"):
            raise RuntimeError(f"MVP-03 approved payload merge missing phrase: {path}")
        if path not in manifest_paths:
            raise RuntimeError(f"MVP-03 approved payload path missing from manifest: {path}")

    validation = execution_doc.get("validation", {})
    if validation.get("status") not in {"pending_final_run", "passed"}:
        raise RuntimeError("MVP-03 execution validation status is invalid.")
    required_commands = {
        "python -B scripts/build_topology.py",
        "python -B scripts/build_release_manifest.py",
        "python -B scripts/simulate_routing.py --report generated/routing-simulation-report.json",
        "python -B scripts/verify.py",
        "python -B scripts/build_topology.py --check",
        "python -B scripts/build_release_manifest.py --check",
        "python -B scripts/simulate_routing.py --all",
        "python -B -m unittest discover -s tests -v",
    }
    if set(validation.get("required_commands", [])) != required_commands:
        raise RuntimeError("MVP-03 execution required commands drifted.")

    doc_path = execution_doc.get("evidence_doc")
    if doc_path != "docs/mvp03-release-routing-execution.md":
        raise RuntimeError("MVP-03 execution evidence doc path is unexpected.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "routing projection proposal allowed: true",
        "approved payload diff allowed: true",
        "release manifest allowed: true",
        "runtime install proof allowed: true",
        "No candidate is added as a standalone approved Skill directory.",
        "Runtime install proof belongs to the consumer repository",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"MVP-03 execution doc missing phrase: {phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link MVP-03 execution.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link MVP-03 execution.")


def validate_mvp06_lifecycle_feedback(
    lifecycle_doc: dict[str, object],
    execution_doc: dict[str, object],
    candidate_review_doc: dict[str, object],
    skills_doc: dict[str, object],
    manifest: dict[str, object],
) -> None:
    if lifecycle_doc.get("schema_version") != 1:
        raise RuntimeError("MVP-06 lifecycle feedback schema_version must be 1.")
    if lifecycle_doc.get("record_id") != "mvp06-lifecycle-feedback-2026-06-27":
        raise RuntimeError("MVP-06 lifecycle feedback record id mismatch.")
    if lifecycle_doc.get("status") != "lifecycle_feedback_recorded":
        raise RuntimeError("MVP-06 lifecycle feedback status mismatch.")
    if lifecycle_doc.get("not_completion_claim") is not True:
        raise RuntimeError("MVP-06 lifecycle feedback must not claim global completion.")
    if lifecycle_doc.get("source_execution_record") != "registry/mvp03-release-routing-execution.json":
        raise RuntimeError("MVP-06 lifecycle feedback must reference MVP-03 execution.")
    if lifecycle_doc.get("consumer_repository") != "codex-user-config":
        raise RuntimeError("MVP-06 consumer repository mismatch.")
    if lifecycle_doc.get("consumer_head") != "a89b61737f066118b13264510cb4dbe5566e2269":
        raise RuntimeError("MVP-06 consumer head mismatch.")

    runtime_evidence = lifecycle_doc.get("runtime_evidence", {})
    if not isinstance(runtime_evidence, dict):
        raise RuntimeError("MVP-06 runtime evidence must be an object.")
    if runtime_evidence.get("install_plan") != {
        "add": 0,
        "unchanged": 17,
        "replace": 2,
        "retire": 0,
    }:
        raise RuntimeError("MVP-06 install plan drifted.")
    if runtime_evidence.get("installed_curated_skills") != 19:
        raise RuntimeError("MVP-06 installed curated Skill count mismatch.")
    if runtime_evidence.get("replaced") != ["grill-with-docs", "review"]:
        raise RuntimeError("MVP-06 replaced Skill list mismatch.")
    if runtime_evidence.get("routing_index") != "replaced and verified":
        raise RuntimeError("MVP-06 routing index evidence mismatch.")
    if runtime_evidence.get("private_runtime_details") != "private":
        raise RuntimeError("MVP-06 must keep private runtime details private.")

    candidate_ids = candidate_review_doc.get("candidate_ids", [])
    if candidate_ids != execution_doc.get("candidate_ids", candidate_ids):
        raise RuntimeError("MVP-06 candidate ids must match MVP-03 records.")
    expected_lifecycle = {
        "spec-driven-development": (
            "accepted_as_recipe_projection",
            "recipe.spec-driven-development",
        ),
        "documentation-and-adrs": (
            "accepted_as_merge_into_existing_skill",
            "skill.curated.grill-with-docs",
        ),
        "code-review-and-quality": (
            "accepted_as_merge_into_existing_skill",
            "skill.curated.review",
        ),
    }
    lifecycle_items = {
        item.get("candidate_id"): item
        for item in lifecycle_doc.get("candidate_lifecycle", [])
        if isinstance(item, dict)
    }
    if set(lifecycle_items) != set(candidate_ids) or set(lifecycle_items) != set(expected_lifecycle):
        raise RuntimeError("MVP-06 lifecycle candidates must match the selected batch.")

    approved_directories = {item["directory"] for item in skills_doc.get("skills", [])}
    manifest_paths = {
        item.get("path", "")
        for item in manifest.get("files", [])
        if isinstance(item, dict)
    }
    for candidate_id, item in lifecycle_items.items():
        expected_state, expected_surface = expected_lifecycle[candidate_id]
        if item.get("lifecycle_state") != expected_state:
            raise RuntimeError(f"MVP-06 lifecycle state mismatch: {candidate_id}")
        if item.get("runtime_surface") != expected_surface:
            raise RuntimeError(f"MVP-06 runtime surface mismatch: {candidate_id}")
        if item.get("decision") != "keep_active":
            raise RuntimeError(f"MVP-06 lifecycle decision mismatch: {candidate_id}")
        if item.get("deprecated") or item.get("retired"):
            raise RuntimeError(f"MVP-06 must not deprecate or retire selected candidate: {candidate_id}")
        if candidate_id in approved_directories:
            raise RuntimeError(f"MVP-06 must not add standalone approved Skill directory: {candidate_id}")
        if f"skills/{candidate_id}/" in manifest_paths:
            raise RuntimeError(f"MVP-06 must not add standalone candidate to manifest: {candidate_id}")

    radar_feedback = lifecycle_doc.get("radar_feedback", {})
    if not isinstance(radar_feedback, dict):
        raise RuntimeError("MVP-06 radar feedback must be an object.")
    if radar_feedback.get("safe_to_publish") is not True:
        raise RuntimeError("MVP-06 radar feedback must be public-safe.")
    if radar_feedback.get("dedupe_action") != "suppress_exact_candidate_reproposal_for_this_batch":
        raise RuntimeError("MVP-06 radar feedback dedupe action mismatch.")
    if radar_feedback.get("does_not_reject_upstream_repository") is not True:
        raise RuntimeError("MVP-06 must not reject the upstream repository globally.")
    if radar_feedback.get("does_not_approve_new_sources") is not True:
        raise RuntimeError("MVP-06 must not approve new sources.")
    metadata = radar_feedback.get("metadata", [])
    if len(metadata) != len(candidate_ids):
        raise RuntimeError("MVP-06 radar feedback metadata count mismatch.")
    for item in metadata:
        if not isinstance(item, dict):
            raise RuntimeError("MVP-06 radar feedback metadata entries must be objects.")
        candidate_id = item.get("candidate_id")
        if candidate_id not in expected_lifecycle:
            raise RuntimeError(f"MVP-06 radar feedback unknown candidate: {candidate_id}")
        if item.get("runtime_surface") != expected_lifecycle[candidate_id][1]:
            raise RuntimeError(f"MVP-06 radar feedback runtime surface mismatch: {candidate_id}")
        if item.get("outcome") != expected_lifecycle[candidate_id][0]:
            raise RuntimeError(f"MVP-06 radar feedback outcome mismatch: {candidate_id}")

    next_step = lifecycle_doc.get("next_step_decision", {})
    if not isinstance(next_step, dict):
        raise RuntimeError("MVP-06 next step decision must be an object.")
    if next_step.get("decision") != "pause_and_observe_before_next_batch":
        raise RuntimeError("MVP-06 next step decision mismatch.")
    if next_step.get("new_batch_requires_new_gate") is not True:
        raise RuntimeError("MVP-06 must require a new gate for another batch.")
    if next_step.get("new_terminal_consumer_requires_graduation_gate") is not True:
        raise RuntimeError("MVP-06 must require a graduation gate for another consumer.")

    validation = lifecycle_doc.get("validation", {})
    if validation.get("status") != "passed":
        raise RuntimeError("MVP-06 validation must be passed.")
    if set(validation.get("required_commands", [])) != {
        "python -B scripts/verify.py",
        "python -B scripts/simulate_routing.py --all",
    }:
        raise RuntimeError("MVP-06 validation commands drifted.")

    doc_path = lifecycle_doc.get("evidence_doc")
    if doc_path != "docs/mvp06-lifecycle-feedback.md":
        raise RuntimeError("MVP-06 evidence doc path mismatch.")
    doc = (ROOT / doc_path).read_text(encoding="utf-8")
    for phrase in [
        "not a completion claim",
        "not a new source intake approval",
        "not a public promotion decision",
        "Resource radar feedback",
        "pause and observe before the next batch",
        "another terminal consumer requires a separate graduation gate",
    ]:
        if phrase not in doc:
            raise RuntimeError(f"MVP-06 lifecycle doc missing phrase: {phrase}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if doc_path not in readme:
        raise RuntimeError("README.md must link MVP-06 lifecycle feedback.")
    if doc_path not in readme_zh:
        raise RuntimeError("README.zh-CN.md must link MVP-06 lifecycle feedback.")


def main() -> int:
    try:
        verify()
    except ContractError as exc:
        print(f"Contract error: {exc}", file=sys.stderr)
        return 1
    print("Agent Skills Curated validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
