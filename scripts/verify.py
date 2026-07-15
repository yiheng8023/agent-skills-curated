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
    "registry/program-control-acceptance-event-2026-07-15.json",
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
    "registry/round02-local-runtime-sync-approval-request.json",
    "registry/round02-local-runtime-sync-approval-events.json",
    "registry/round02-local-runtime-sync-execution.json",
    "registry/round02-stage-closeout-review.json",
    "registry/round02-stage-closeout-acceptance-event-2026-07-15.json",
    "registry/round03-capability-survey-rebaseline.json",
    "registry/round03-demand-coordinate-source-contract.json",
    "registry/round03-demand-records-batch-01.json",
    "registry/round03-native-runtime-baseline-2026-07-15.json",
    "registry/round03-public-discovery-snapshot-2026-07-15.json",
    "registry/round03-representative-source-review-batch-01.json",
    "registry/round03-capability-survey-rebaseline-acceptance-event-2026-07-15.json",
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
    "docs/round02-local-runtime-sync-approval-request.md",
    "docs/round02-local-runtime-sync-execution.md",
    "docs/round02-stage-closeout-review.md",
    "docs/round02-stage-closeout-review.zh-CN.md",
    "docs/round02-stage-closeout-acceptance.md",
    "docs/round02-stage-closeout-acceptance.zh-CN.md",
    "docs/round03-capability-survey-rebaseline.md",
    "docs/round03-capability-survey-rebaseline.zh-CN.md",
    "docs/round03-demand-coordinate-source-contract.md",
    "docs/round03-demand-coordinate-source-contract.zh-CN.md",
    "docs/round03-demand-records-batch-01.md",
    "docs/round03-demand-records-batch-01.zh-CN.md",
    "docs/round03-native-runtime-baseline-2026-07-15.md",
    "docs/round03-native-runtime-baseline-2026-07-15.zh-CN.md",
    "docs/round03-public-discovery-snapshot-2026-07-15.md",
    "docs/round03-public-discovery-snapshot-2026-07-15.zh-CN.md",
    "docs/round03-representative-source-review-batch-01.md",
    "docs/round03-representative-source-review-batch-01.zh-CN.md",
    "docs/round03-capability-survey-rebaseline-acceptance.md",
    "docs/round03-capability-survey-rebaseline-acceptance.zh-CN.md",
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
    program_control_acceptance_event_doc = load("registry/program-control-acceptance-event-2026-07-15.json")
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
    round02_local_runtime_sync_execution_doc = load("registry/round02-local-runtime-sync-execution.json")
    round02_stage_closeout_review_doc = load("registry/round02-stage-closeout-review.json")
    round02_stage_closeout_acceptance_event_doc = load("registry/round02-stage-closeout-acceptance-event-2026-07-15.json")
    round03_capability_survey_rebaseline_doc = load("registry/round03-capability-survey-rebaseline.json")
    round03_demand_coordinate_source_contract_doc = load("registry/round03-demand-coordinate-source-contract.json")
    round03_demand_records_batch_01_doc = load("registry/round03-demand-records-batch-01.json")
    round03_native_runtime_baseline_doc = load("registry/round03-native-runtime-baseline-2026-07-15.json")
    round03_public_discovery_snapshot_doc = load("registry/round03-public-discovery-snapshot-2026-07-15.json")
    round03_representative_source_review_batch_01_doc = load("registry/round03-representative-source-review-batch-01.json")
    round03_capability_survey_rebaseline_acceptance_event_doc = load("registry/round03-capability-survey-rebaseline-acceptance-event-2026-07-15.json")
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
    validate_program_control_acceptance_event(
        program_control_acceptance_event_doc,
        curation_program_plan_doc,
        program_acceptance_map_doc,
    )
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
    validate_round02_stage_closeout_review(
        round02_stage_closeout_review_doc,
        curation_expansion_rounds_doc,
        curation_program_plan_doc,
        round_lifecycle_contract_doc,
        source_intake_batches_doc,
        round02_release_admission_candidate_review_doc,
        round02_approved_payload_routing_proposal_doc,
        round02_local_runtime_sync_execution_doc,
    )
    validate_round02_stage_closeout_acceptance_event(
        round02_stage_closeout_acceptance_event_doc,
        round02_stage_closeout_review_doc,
        curation_expansion_rounds_doc,
        curation_program_plan_doc,
        round_lifecycle_contract_doc,
        program_acceptance_map_doc,
    )
    validate_round03_demand_coordinate_source_contract(
        round03_demand_coordinate_source_contract_doc,
        curation_expansion_rounds_doc,
        curation_program_plan_doc,
        round_lifecycle_contract_doc,
        program_acceptance_map_doc,
    )
    validate_round03_demand_records_batch_01(
        round03_demand_records_batch_01_doc,
        round03_demand_coordinate_source_contract_doc,
        program_acceptance_map_doc,
    )
    validate_round03_native_runtime_baseline(
        round03_native_runtime_baseline_doc,
        round03_demand_records_batch_01_doc,
        round03_demand_coordinate_source_contract_doc,
        curation_expansion_rounds_doc,
        round_lifecycle_contract_doc,
        program_acceptance_map_doc,
    )
    validate_round03_public_discovery_snapshot(
        round03_public_discovery_snapshot_doc,
        round03_native_runtime_baseline_doc,
        curation_expansion_rounds_doc,
        round_lifecycle_contract_doc,
        program_acceptance_map_doc,
    )
    validate_round03_representative_source_review_batch_01(
        round03_representative_source_review_batch_01_doc,
        round03_public_discovery_snapshot_doc,
        curation_expansion_rounds_doc,
        round_lifecycle_contract_doc,
        program_acceptance_map_doc,
    )
    validate_round03_capability_survey_rebaseline(
        round03_capability_survey_rebaseline_doc,
        round03_demand_coordinate_source_contract_doc,
        curation_expansion_rounds_doc,
        curation_program_plan_doc,
        round_lifecycle_contract_doc,
        program_acceptance_map_doc,
    )
    validate_round03_capability_survey_rebaseline_acceptance_event(
        round03_capability_survey_rebaseline_acceptance_event_doc,
        round03_capability_survey_rebaseline_doc,
        round03_demand_coordinate_source_contract_doc,
        curation_expansion_rounds_doc,
        curation_program_plan_doc,
        round_lifecycle_contract_doc,
        program_acceptance_map_doc,
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

    program_initiatives = program_doc.get("currentInitiatives")
    if not isinstance(program_initiatives, list) or not program_initiatives:
        raise RuntimeError("Curation program current initiatives are required for acceptance mapping.")
    for initiative in program_initiatives:
        if not isinstance(initiative, dict):
            raise RuntimeError("Curation program initiatives must be objects for acceptance mapping.")
        initiative_id = initiative.get("id")
        acceptance_ids = initiative.get("acceptanceIds")
        if not isinstance(acceptance_ids, list) or not acceptance_ids:
            raise RuntimeError(f"Program initiative requires acceptance ids: {initiative_id}")
        for acceptance_id in acceptance_ids:
            if acceptance_id not in criteria:
                raise RuntimeError(
                    f"Program initiative {initiative_id} references unknown acceptance id: {acceptance_id}"
                )

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


def validate_program_control_acceptance_event(
    document: dict[str, object],
    program_doc: dict[str, object],
    acceptance_doc: dict[str, object],
) -> None:
    """Validate the owner decision that closed program-control reconciliation."""
    if document.get("schema") != 1:
        raise RuntimeError("Program control acceptance event schema must be 1.")
    if document.get("id") != "program-control-acceptance-event-2026-07-15":
        raise RuntimeError("Program control acceptance event id drifted.")
    if document.get("date") != "2026-07-15":
        raise RuntimeError("Program control acceptance event date drifted.")
    if document.get("decision") != "accepted-and-merged-locally":
        raise RuntimeError("Program control acceptance event decision drifted.")
    if document.get("authoritySource") != "owner-selected-local-merge-option-1":
        raise RuntimeError("Program control acceptance event authority source drifted.")
    accepted_commit = document.get("acceptedBaselineCommit")
    if accepted_commit != "7513da41e9c2950de1a6132ce9c9d65fb11a8098":
        raise RuntimeError("Program control acceptance event baseline commit drifted.")
    if not isinstance(accepted_commit, str) or not re.fullmatch(r"[0-9a-f]{40}", accepted_commit):
        raise RuntimeError("Program control acceptance event requires a full commit hash.")
    if document.get("mergedInto") != "main" or document.get("localMergeObserved") is not True:
        raise RuntimeError("Program control acceptance event must record the observed local main merge.")
    if document.get("remotePushAuthorized") is not False:
        raise RuntimeError("Program control acceptance event must not authorize remote push.")
    if document.get("nextInitiativeId") != "initiative.round02-stage-closeout-reconciliation":
        raise RuntimeError("Program control acceptance event next initiative drifted.")
    accepted_scope = " ".join(str(item) for item in document.get("acceptedScope", [])).lower()
    for phrase in ["completeness", "dependency-graph", "acceptance", "english and chinese"]:
        if phrase not in accepted_scope:
            raise RuntimeError(f"Program control acceptance event scope missing phrase: {phrase}")
    excluded = " ".join(str(item) for item in document.get("doesNotAuthorize", [])).lower()
    for phrase in [
        "remote push",
        "external discovery",
        "candidate code execution",
        "runtime mutation",
        "cross-repository",
        "round 02 stage closeout",
    ]:
        if phrase not in excluded:
            raise RuntimeError(f"Program control acceptance event exclusion missing phrase: {phrase}")

    initiatives = program_doc.get("currentInitiatives", [])
    completeness = next(
        (
            item
            for item in initiatives
            if isinstance(item, dict)
            and item.get("id") == "initiative.program-control-completeness-reconciliation"
        ),
        None,
    )
    round02 = next(
        (
            item
            for item in initiatives
            if isinstance(item, dict)
            and item.get("id") == "initiative.round02-stage-closeout-reconciliation"
        ),
        None,
    )
    if not completeness or completeness.get("status") != "accepted":
        raise RuntimeError("Program control completeness initiative must be accepted.")
    if completeness.get("decisionEvidence") != "registry/program-control-acceptance-event-2026-07-15.json":
        raise RuntimeError("Program control completeness initiative decision evidence drifted.")
    if not round02 or round02.get("status") != "accepted":
        raise RuntimeError("Round 02 reconciliation initiative must retain its accepted state.")
    if round02.get("decisionEvidence") != "registry/round02-stage-closeout-acceptance-event-2026-07-15.json":
        raise RuntimeError("Round 02 reconciliation decision evidence drifted.")

    criteria = {
        item.get("id"): item
        for item in acceptance_doc.get("acceptanceCriteria", [])
        if isinstance(item, dict)
    }
    criterion = criteria.get("acceptance.program-control-completeness")
    if not criterion or criterion.get("assessment") != "verified":
        raise RuntimeError("Program control completeness acceptance must be verified after owner decision.")
    if "evidence.program-control-acceptance" not in criterion.get("evidenceIds", []):
        raise RuntimeError("Program control completeness acceptance event evidence is missing.")


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
        if item.get("status") not in {"active", "planned", "needs-rebaseline", "needs-closeout", "closed"}:
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
        allowed_lifecycle_values = {"planned", "recorded", "accepted", "pending", "active", "passed", "closed"}
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
            if lifecycle.get("plan") not in {"recorded", "accepted"} or lifecycle.get("execute") != "active":
                raise RuntimeError(f"Active curation round must have a recorded or accepted plan and active execution: {round_id}")
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
        elif item.get("status") == "needs-rebaseline":
            expected = {
                "plan": "recorded",
                "execute": "pending",
                "acceptance": "pending",
                "stageCloseout": "pending",
            }
            if lifecycle != expected:
                raise RuntimeError(f"Rebaseline-pending curation round lifecycle mismatch: {round_id}")
            evidence = item.get("evidence")
            if not isinstance(evidence, list) or not evidence:
                raise RuntimeError(f"Rebaseline-pending curation round requires evidence: {round_id}")
            for path in evidence:
                if not isinstance(path, str) or not (ROOT / path).is_file():
                    raise RuntimeError(f"Rebaseline-pending curation round evidence is missing: {path}")
            if not isinstance(item.get("nextGate"), str) or not item.get("nextGate"):
                raise RuntimeError(f"Rebaseline-pending curation round requires next gate: {round_id}")
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
        "closed",
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

    architecture = document.get("programArchitecture")
    if not isinstance(architecture, dict):
        raise RuntimeError("Curation program stable architecture is required.")
    if architecture.get("model") != "stable-operating-lanes-with-bounded-initiatives-and-historical-rounds":
        raise RuntimeError("Curation program architecture model drifted.")
    control_layers = architecture.get("controlLayers")
    if not isinstance(control_layers, list) or len(control_layers) < 5:
        raise RuntimeError("Curation program architecture control layers are incomplete.")
    operating_lanes = architecture.get("operatingLanes")
    if not isinstance(operating_lanes, list):
        raise RuntimeError("Curation program operating lanes are required.")
    expected_core_path = [
        "lane.demand-evidence",
        "lane.native-official-runtime-baseline",
        "lane.discovery-and-clustering",
        "lane.representative-deep-review",
        "lane.solution-alternative-comparison",
        "lane.residual-gap-decision",
        "lane.candidate-governance-and-adaptation",
        "lane.admission-verification-and-release",
    ]
    expected_lane_ids = [
        *expected_core_path,
        "lane.consumer-evidence-and-feedback",
        "lane.lifecycle-metabolism",
        "lane.standard-extraction-and-calibration-handoff",
    ]
    execution_semantics = architecture.get("executionSemantics")
    if not isinstance(execution_semantics, dict):
        raise RuntimeError("Curation program dependency graph execution semantics are required.")
    if execution_semantics.get("model") != "dependency-graph-with-optional-and-cross-cutting-lanes":
        raise RuntimeError("Curation program dependency graph model drifted.")
    if execution_semantics.get("displayOrderIsExecutionOrder") is not False:
        raise RuntimeError("Curation program lane display order must not claim linear execution order.")
    if execution_semantics.get("corePath") != expected_core_path:
        raise RuntimeError("Curation program dependency graph core path drifted.")
    expected_branch_semantics = {
        "optionalBranches": ["lane.consumer-evidence-and-feedback"],
        "crossCuttingLanes": ["lane.lifecycle-metabolism"],
        "conditionalBranches": ["lane.standard-extraction-and-calibration-handoff"],
    }
    for key, expected in expected_branch_semantics.items():
        if execution_semantics.get(key) != expected:
            raise RuntimeError(f"Curation program dependency graph {key} drifted.")
    safe_parallelism = execution_semantics.get("safeParallelism")
    if not isinstance(safe_parallelism, list) or len(safe_parallelism) < 3:
        raise RuntimeError("Curation program dependency graph safe parallelism is incomplete.")
    parallel_text = " ".join(str(item) for item in safe_parallelism).lower()
    for phrase in ["host and model", "metadata triage", "join before alternative comparison"]:
        if phrase not in parallel_text:
            raise RuntimeError(f"Curation program safe parallelism missing phrase: {phrase}")
    radar_boundary = str(execution_semantics.get("upstreamRadarBoundary", "")).lower()
    for phrase in ["independently", "demand", "source-trust", "acceptance"]:
        if phrase not in radar_boundary:
            raise RuntimeError(f"Curation program upstream radar order boundary missing phrase: {phrase}")
    closeout_join = str(execution_semantics.get("closeoutJoin", "")).lower()
    for phrase in ["initiative", "residual risks", "owner decision", "next candidate-intake"]:
        if phrase not in closeout_join:
            raise RuntimeError(f"Curation program closeout join missing phrase: {phrase}")

    expected_lane_semantics = {
        "lane.demand-evidence": ("core", []),
        "lane.native-official-runtime-baseline": ("core", ["lane.demand-evidence"]),
        "lane.discovery-and-clustering": ("core", ["lane.native-official-runtime-baseline"]),
        "lane.representative-deep-review": ("core", ["lane.discovery-and-clustering"]),
        "lane.solution-alternative-comparison": (
            "core",
            ["lane.native-official-runtime-baseline", "lane.representative-deep-review"],
        ),
        "lane.residual-gap-decision": ("core", ["lane.solution-alternative-comparison"]),
        "lane.candidate-governance-and-adaptation": ("core", ["lane.residual-gap-decision"]),
        "lane.admission-verification-and-release": (
            "core",
            ["lane.candidate-governance-and-adaptation"],
        ),
        "lane.consumer-evidence-and-feedback": (
            "optional-branch",
            ["lane.admission-verification-and-release"],
        ),
        "lane.lifecycle-metabolism": ("cross-cutting", []),
        "lane.standard-extraction-and-calibration-handoff": ("conditional-branch", []),
    }
    lane_ids = [item.get("id") for item in operating_lanes if isinstance(item, dict)]
    for lane in operating_lanes:
        if not isinstance(lane, dict):
            raise RuntimeError("Curation program operating lanes must be objects.")
        lane_id = lane.get("id")
        if not isinstance(lane_id, str) or not lane_id:
            raise RuntimeError("Curation program operating lane id is required.")
        purpose_text = str(lane.get("purpose", "")).lower()
        if "runtime-sync" in lane_id or "local runtime sync" in purpose_text:
            raise RuntimeError(
                "Curation program consumer runtime sync must not be a mandatory stable lane."
            )
        if not isinstance(lane.get("purpose"), str) or not lane.get("purpose"):
            raise RuntimeError(f"Curation program operating lane purpose is required: {lane_id}")
        if lane_id not in expected_lane_semantics:
            raise RuntimeError(f"Curation program operating lane is not governed: {lane_id}")
        expected_mode, expected_dependencies = expected_lane_semantics[lane_id]
        if lane.get("executionMode") != expected_mode:
            raise RuntimeError(f"Curation program operating lane execution mode drifted: {lane_id}")
        if lane.get("dependsOn") != expected_dependencies:
            raise RuntimeError(f"Curation program operating lane dependencies drifted: {lane_id}")
        for key in [
            "requiredInputs",
            "allowedOutputs",
            "blockedTransitions",
            "verificationSurface",
            "rerouteTriggers",
        ]:
            if not isinstance(lane.get(key), list) or not lane.get(key):
                raise RuntimeError(
                    f"Curation program operating lane {key} is required: {lane_id}"
                )
        if lane_id == "lane.representative-deep-review":
            review_inputs = " ".join(str(item) for item in lane.get("requiredInputs", [])).lower()
            for phrase in ["exact source pin", "license and provenance"]:
                if phrase not in review_inputs:
                    raise RuntimeError(
                        f"Curation program representative deep review requires source pin evidence: {phrase}"
                    )
        if lane_id == "lane.lifecycle-metabolism":
            lifecycle_inputs = " ".join(str(item) for item in lane.get("requiredInputs", [])).lower()
            if "release and consumer" in lifecycle_inputs:
                raise RuntimeError("Curation program lifecycle must not require consumer evidence.")
            triggers = lane.get("triggerInputsAnyOf")
            if not isinstance(triggers, list) or len(triggers) < 4:
                raise RuntimeError("Curation program lifecycle any-of triggers are incomplete.")
        if lane_id == "lane.standard-extraction-and-calibration-handoff":
            triggers = lane.get("triggerInputsAnyOf")
            if not isinstance(triggers, list) or len(triggers) < 4:
                raise RuntimeError("Curation program standard extraction any-of triggers are incomplete.")
    if lane_ids != expected_lane_ids:
        raise RuntimeError("Curation program operating lane order drifted.")

    origin_policy = document.get("candidateOriginPolicy")
    if not isinstance(origin_policy, dict):
        raise RuntimeError("Curation program candidate origin policy is required.")
    origin_classes = origin_policy.get("classes")
    if not isinstance(origin_classes, list):
        raise RuntimeError("Curation program candidate origin classes are required.")
    expected_origin_ids = [
        "platform-runtime-vendor-first-party-baseline",
        "third-party-candidate",
        "repository-authored-gap-fill-candidate",
        "curated-approved-release",
    ]
    origin_ids = [item.get("id") for item in origin_classes if isinstance(item, dict)]
    if origin_ids != expected_origin_ids:
        raise RuntimeError("Curation program candidate origin classes drifted.")
    for origin in origin_classes:
        if not isinstance(origin, dict):
            raise RuntimeError("Curation program candidate origin classes must be objects.")
        origin_id = origin.get("id")
        if not isinstance(origin.get("eligibilityGate"), str) or not origin.get("eligibilityGate"):
            raise RuntimeError(f"Curation program candidate eligibility gate is required: {origin_id}")
        if not isinstance(origin.get("releaseEligible"), bool):
            raise RuntimeError(f"Curation program candidate release eligibility is required: {origin_id}")
        if not isinstance(origin.get("requiredEvidence"), list) or not origin.get("requiredEvidence"):
            raise RuntimeError(f"Curation program candidate evidence is required: {origin_id}")
    repository_authored = next(
        item
        for item in origin_classes
        if isinstance(item, dict)
        and item.get("id") == "repository-authored-gap-fill-candidate"
    )
    repository_authored_text = " ".join(
        [
            str(repository_authored.get("eligibilityGate", "")),
            *[str(item) for item in repository_authored.get("requiredEvidence", [])],
        ]
    ).lower()
    for phrase in ["residual-gap-supported", "alternative comparison", "tests", "owner approval"]:
        if phrase not in repository_authored_text:
            raise RuntimeError(
                f"Curation program repository-authored candidate missing residual gap gate evidence: {phrase}"
            )

    sequence_gates = document.get("sequenceGates")
    if not isinstance(sequence_gates, list):
        raise RuntimeError("Curation program sequence gates are required.")
    expected_sequence_gate_ids = [
        "gate.demand-before-gap-claim",
        "gate.baseline-before-substitution",
        "gate.clustering-before-deep-review",
        "gate.source-pin-before-deep-review",
        "gate.alternatives-before-residual-gap",
        "gate.residual-gap-before-repository-authoring",
        "gate.admission-before-release",
        "gate.release-before-consumer-projection",
        "gate.repeated-evidence-before-standard-extraction",
        "gate.calibration-before-assets-admission",
        "gate.closeout-before-next-intake",
    ]
    sequence_gate_ids = [
        item.get("id") for item in sequence_gates if isinstance(item, dict)
    ]
    if sequence_gate_ids != expected_sequence_gate_ids:
        raise RuntimeError("Curation program sequence gate order drifted.")
    for gate in sequence_gates:
        if not isinstance(gate, dict):
            raise RuntimeError("Curation program sequence gates must be objects.")
        for key in ["id", "prerequisite", "blockedUntil", "verification"]:
            if not isinstance(gate.get(key), str) or not gate.get(key):
                raise RuntimeError(f"Curation program sequence gate {key} is required.")

    initiatives = document.get("currentInitiatives")
    if not isinstance(initiatives, list):
        raise RuntimeError("Curation program current initiatives are required.")
    initiative_ids = [item.get("id") for item in initiatives if isinstance(item, dict)]
    required_initiative_ids = {
        "initiative.program-control-completeness-reconciliation",
        "initiative.round02-stage-closeout-reconciliation",
        "initiative.round03-capability-survey-rebaseline",
        "initiative.capability-survey-gap-proof",
    }
    if not required_initiative_ids <= set(initiative_ids):
        raise RuntimeError("Curation program required initiatives are missing.")
    if len(initiative_ids) != len(set(initiative_ids)):
        raise RuntimeError("Curation program initiative ids must be unique.")
    for initiative in initiatives:
        if not isinstance(initiative, dict):
            raise RuntimeError("Curation program initiatives must be objects.")
        initiative_id = initiative.get("id")
        if not isinstance(initiative.get("status"), str) or not initiative.get("status"):
            raise RuntimeError(f"Curation program initiative status is required: {initiative_id}")
        for key in [
            "prerequisites",
            "allowedActions",
            "blockedActions",
            "resultPackage",
            "acceptanceIds",
        ]:
            if not isinstance(initiative.get(key), list) or not initiative.get(key):
                raise RuntimeError(
                    f"Curation program initiative {key} is required: {initiative_id}"
                )
        if not isinstance(initiative.get("decisionGate"), str) or not initiative.get("decisionGate"):
            raise RuntimeError(f"Curation program initiative decision gate is required: {initiative_id}")
    current_initiative_id = document.get("currentInitiativeId")
    if current_initiative_id != "initiative.capability-survey-gap-proof":
        raise RuntimeError("Curation program current initiative must be the active capability survey.")
    current_initiative = next(
        item
        for item in initiatives
        if isinstance(item, dict) and item.get("id") == current_initiative_id
    )
    if current_initiative.get("status") != "active":
        raise RuntimeError("Curation program capability survey must be active after owner acceptance.")
    current_blocked_text = " ".join(
        str(item) for item in current_initiative.get("blockedActions", [])
    ).lower()
    for phrase in ["candidate code execution", "installation", "hook enablement", "runtime mutation", "cross-repository", "remote push"]:
        if phrase not in current_blocked_text:
            raise RuntimeError(f"Curation program current initiative missing blocked action: {phrase}")
    rebaseline = next(
        item
        for item in initiatives
        if isinstance(item, dict)
        and item.get("id") == "initiative.round03-capability-survey-rebaseline"
    )
    if rebaseline.get("status") != "accepted":
        raise RuntimeError("Curation program Round 03 rebaseline must record owner acceptance.")
    if rebaseline.get("decisionEvidence") != "registry/round03-capability-survey-rebaseline-acceptance-event-2026-07-15.json":
        raise RuntimeError("Curation program Round 03 rebaseline decision evidence drifted.")
    capability_survey = next(
        item
        for item in initiatives
        if isinstance(item, dict)
        and item.get("id") == "initiative.capability-survey-gap-proof"
    )
    if capability_survey.get("status") != "active":
        raise RuntimeError("Curation capability survey must be active after prerequisites close.")
    survey_blocked_text = " ".join(
        str(item) for item in capability_survey.get("blockedActions", [])
    ).lower()
    for phrase in ["candidate code execution", "installation", "runtime mutation", "remote push"]:
        if phrase not in survey_blocked_text:
            raise RuntimeError(f"Curation capability survey missing blocked action: {phrase}")
    survey_result_text = " ".join(
        str(item) for item in capability_survey.get("resultPackage", [])
    ).lower()
    for phrase in [
        "native agent",
        "clustered and deduplicated",
        "stm, p, and sg",
        "single-skill and composed",
        "candidate dispositions",
        "residual gaps",
        "host, model, reasoning, loader",
        "intent-contract",
        "discovery stop rationale",
        "non-authorization",
    ]:
        if phrase not in survey_result_text:
            raise RuntimeError(f"Curation capability survey result package missing phrase: {phrase}")

    strategic_objectives = document.get("strategicObjectives")
    if not isinstance(strategic_objectives, list) or not strategic_objectives:
        raise RuntimeError("Curation program strategic objectives are required.")
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
    required_objective_ids = {
        "objective.skills-terminal-mvp",
        "objective.multi-domain-coverage",
        "objective.evidence-backed-demand-model",
        "objective.reuse-before-build-gap-proof",
        "objective.full-chain-capability-coverage",
        "objective.decision-ready-external-brain",
        "objective.reviewed-third-party-governance",
        "objective.multi-agent-consumer-mapping",
        "objective.layered-collaboration-reliability",
        "objective.standard-candidate-extraction",
        "objective.lifecycle-metabolism",
    }
    missing_objectives = required_objective_ids - set(objective_ids)
    if missing_objectives:
        raise RuntimeError(
            f"Curation program required strategic objectives are missing: {sorted(missing_objectives)}"
        )

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
    if harness_loop.get("executionSemanticsRef") != "programArchitecture.executionSemantics":
        raise RuntimeError("Curation program harness must reference dependency graph semantics.")
    if harness_loop.get("loopIsLinearExecutionOrder") is not False:
        raise RuntimeError("Curation program harness loop must not claim linear execution order.")
    expected_loop = [
        "demand-evidence",
        "native-official-runtime-baseline",
        "discover-and-cluster",
        "representative-deep-review",
        "compare-alternatives",
        "prove-residual-gap",
        "govern-adapt-or-author-candidate",
        "verify-admit-and-release",
        "optional-consumer-projection",
        "feedback",
        "metabolize",
        "extract-standard-candidate-for-calibration",
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

    if document.get("stepsRole") != "historical-execution-projection-not-stable-operating-architecture":
        raise RuntimeError("Curation program historical steps role drifted.")
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
        if step.get("status") in {"evidence-recorded", "needs-reconciliation", "complete", "closed"}:
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
        "registry/program-control-acceptance-event-2026-07-15.json",
        "registry/round02-stage-closeout-acceptance-event-2026-07-15.json",
        "registry/round03-capability-survey-rebaseline-acceptance-event-2026-07-15.json",
        "initiative.round03-capability-survey-rebaseline",
        "Round 03 rebaseline has been owner-accepted",
        "evidenced demand or shortfall",
        "native / official / runtime baseline",
        "discovery, clustering, deduplication",
        "native / single-Skill / composition / non-Skill comparison",
        "admission, verification, and release",
        "reuse before build",
        "residual gap",
        "repository-authored",
        "capability-survey",
        "optional consumer",
        "dependency graph",
        "optional branch",
        "cross-cutting",
        "exact source pin",
        "machine-bound current initiative",
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
        "reuse before build",
        "residual gap",
        "repository-authored",
        "Decision-Ready External-Brain Outcome",
        "Consumer projection is an optional branch",
        "Dependency Graph Semantics",
        "optional branch",
        "cross-cutting",
        "exact source pin",
        "radar signal does not bypass",
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
    for phrase in [
        "multi-domain",
        "reuse before build",
        "residual gap",
        "decision-ready",
        "repository-authored gap-fill",
        "dependency graph",
        "optional branch",
        "cross-cutting",
        "exact source pin",
        "current initiative",
    ]:
        if phrase not in readme:
            raise RuntimeError(f"README.md missing stable program concept: {phrase}")
    for phrase in [
        "多领域",
        "复用优先于自制",
        "剩余缺口",
        "决策就绪的外脑",
        "仓库自制",
        "依赖图",
        "可选分支",
        "跨阶段",
        "精确来源固定",
        "当前 initiative",
    ]:
        if phrase not in readme_zh:
            raise RuntimeError(f"README.zh-CN.md missing stable program concept: {phrase}")


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
        "needs-rebaseline": ("plan_rebaseline_pending", "not_ready"),
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


def validate_round02_stage_closeout_review(
    document: dict[str, object],
    rounds_doc: dict[str, object],
    program_doc: dict[str, object],
    lifecycle_doc: dict[str, object],
    intake_doc: dict[str, object],
    admission_review_doc: dict[str, object],
    proposal_doc: dict[str, object],
    runtime_sync_doc: dict[str, object],
) -> None:
    if document.get("schema") != 1:
        raise RuntimeError("Round 02 stage-closeout review schema must be 1.")
    if document.get("id") != "round02-stage-closeout-review-2026-07-15":
        raise RuntimeError("Round 02 stage-closeout review id drifted.")
    if document.get("status") != "owner_decision_required":
        raise RuntimeError("Round 02 stage-closeout review must remain owner-decision pending.")
    if document.get("roundId") != "round-02-source-intake-and-filtering":
        raise RuntimeError("Round 02 stage-closeout review round id drifted.")
    if document.get("lifecycleContract") != "registry/round-lifecycle-contract.json#stageCloseout":
        raise RuntimeError("Round 02 stage-closeout review lifecycle contract drifted.")
    if document.get("programPlan") != "registry/curation-program-plan.json#initiative.round02-stage-closeout-reconciliation":
        raise RuntimeError("Round 02 stage-closeout review program initiative drifted.")

    expected_docs = {
        "docs/round02-stage-closeout-review.md",
        "docs/round02-stage-closeout-review.zh-CN.md",
    }
    if set(document.get("evidenceDocs", [])) != expected_docs:
        raise RuntimeError("Round 02 stage-closeout review evidence docs drifted.")
    for path in expected_docs:
        if not (ROOT / path).is_file():
            raise RuntimeError(f"Round 02 stage-closeout review evidence doc is missing: {path}")
    evidence = document.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise RuntimeError("Round 02 stage-closeout review evidence is required.")
    for reference in evidence:
        if not isinstance(reference, str):
            raise RuntimeError("Round 02 stage-closeout evidence references must be strings.")
        path = reference.split("#", 1)[0]
        if not (ROOT / path).is_file():
            raise RuntimeError(f"Round 02 stage-closeout evidence is missing: {path}")

    round02 = next(
        (
            item
            for item in rounds_doc.get("rounds", [])
            if isinstance(item, dict)
            and item.get("id") == "round-02-source-intake-and-filtering"
        ),
        None,
    )
    if round02 is None:
        raise RuntimeError("Round 02 stage-closeout review cannot resolve Round 02.")
    if round02.get("status") != "closed":
        raise RuntimeError("Round 02 must retain the accepted closed state.")
    lifecycle = round02.get("lifecycle", {})
    if lifecycle.get("stageCloseout") != "closed":
        raise RuntimeError("Round 02 stageCloseout must retain the accepted closed state.")
    if "registry/round02-stage-closeout-review.json" not in round02.get("evidence", []):
        raise RuntimeError("Round 02 round registry must link the closeout review.")

    initiative = next(
        (
            item
            for item in program_doc.get("currentInitiatives", [])
            if isinstance(item, dict)
            and item.get("id") == "initiative.round02-stage-closeout-reconciliation"
        ),
        None,
    )
    if initiative is None or initiative.get("status") != "accepted":
        raise RuntimeError("Round 02 closeout initiative must retain the accepted state.")
    if initiative.get("decisionPreparation") != "registry/round02-stage-closeout-review.json":
        raise RuntimeError("Round 02 closeout initiative must link the decision preparation.")
    if initiative.get("decisionEvidence") != "registry/round02-stage-closeout-acceptance-event-2026-07-15.json":
        raise RuntimeError("Round 02 closeout initiative must link the owner decision event.")

    expected_requirement_ids = {
        "round02.exit.source-pin-and-license-review",
        "round02.exit.candidate-dispositions",
        "round02.exit.approval-before-release",
        "round02.closeout.verification",
        "round02.closeout.residual-risk-and-next-decision",
    }
    reconciliation = document.get("requirementReconciliation")
    if not isinstance(reconciliation, list):
        raise RuntimeError("Round 02 requirement reconciliation is required.")
    requirement_ids = {
        item.get("id") for item in reconciliation if isinstance(item, dict)
    }
    if requirement_ids != expected_requirement_ids:
        raise RuntimeError("Round 02 requirement reconciliation coverage drifted.")
    if any(item.get("assessment") != "covered" for item in reconciliation):
        raise RuntimeError("Round 02 proposed closeout requires every stated requirement to be covered.")
    for item in reconciliation:
        if not item.get("evidence") or not item.get("result"):
            raise RuntimeError("Round 02 reconciled requirements need evidence and results.")

    batch = next(
        (
            item
            for item in intake_doc.get("batches", [])
            if isinstance(item, dict) and item.get("id") == "round02-source-intake-2026-07-02"
        ),
        None,
    )
    if batch is None:
        raise RuntimeError("Round 02 source intake batch is missing.")
    source_ids = [
        item.get("id") for item in batch.get("sources", []) if isinstance(item, dict)
    ]
    source_summary = document.get("sourceSummary", {})
    if source_summary.get("sourceCount") != 3 or source_summary.get("pinnedAndLicenseReviewedCount") != 3:
        raise RuntimeError("Round 02 source closeout counts drifted.")
    if source_summary.get("sourceIds") != source_ids:
        raise RuntimeError("Round 02 source closeout ids must match the intake batch.")
    if source_ids != round02.get("candidateSourceIds"):
        raise RuntimeError("Round 02 source intake and round registry drifted.")
    for source in batch.get("sources", []):
        if not isinstance(source, dict):
            raise RuntimeError("Round 02 source intake entries must be objects.")
        revision = str(source.get("revision", ""))
        if len(revision) != 40 or source.get("license") != "MIT":
            raise RuntimeError("Round 02 closeout requires full revisions and reviewed MIT licenses.")

    decisions = [
        item
        for item in admission_review_doc.get("candidate_decisions", [])
        if isinstance(item, dict)
    ]
    observed_dispositions: dict[str, int] = {}
    for item in decisions:
        decision = str(item.get("decision", ""))
        observed_dispositions[decision] = observed_dispositions.get(decision, 0) + 1
    candidate_summary = document.get("candidateOutcomeSummary", {})
    if candidate_summary.get("reviewedCandidateCount") != len(decisions):
        raise RuntimeError("Round 02 reviewed candidate count drifted.")
    if candidate_summary.get("reviewDispositionCounts") != observed_dispositions:
        raise RuntimeError("Round 02 candidate disposition counts drifted.")
    executions = [
        item for item in proposal_doc.get("candidate_executions", []) if isinstance(item, dict)
    ]
    execution_types: dict[str, int] = {}
    for item in executions:
        execution_type = str(item.get("execution_type", ""))
        execution_types[execution_type] = execution_types.get(execution_type, 0) + 1
    if candidate_summary.get("executedApprovedChangeCount") != len(executions):
        raise RuntimeError("Round 02 executed approved change count drifted.")
    if candidate_summary.get("executedApprovedChanges") != execution_types:
        raise RuntimeError("Round 02 executed approved change classes drifted.")
    if candidate_summary.get("deferredOrNonReleaseCount") != len(decisions) - len(executions):
        raise RuntimeError("Round 02 deferred candidate count drifted.")
    if runtime_sync_doc.get("status") != "passed_with_junction_fallback":
        raise RuntimeError("Round 02 closeout must reference the recorded passing runtime sync evidence.")

    expected_risks = {
        "risk.current-live-consumer-parity-unverified": "unverified",
        "risk.deferred-high-boundary-candidates": "deferred",
        "risk.upstream-evidence-aging": "deferred",
        "risk.round03-contract-overlap": "needs-rebaseline",
    }
    risks = {
        item.get("id"): item.get("status")
        for item in document.get("residualRisks", [])
        if isinstance(item, dict)
    }
    if risks != expected_risks:
        raise RuntimeError("Round 02 residual-risk record drifted.")
    if not document.get("deferredWork"):
        raise RuntimeError("Round 02 deferred work must remain visible.")
    if document.get("recommendedOutcome") != "complete":
        raise RuntimeError("Round 02 review recommendation drifted.")
    if document.get("recommendedNextDecision") != "close-round-02-and-pause-for-round-03-rebaseline":
        raise RuntimeError("Round 02 next-decision recommendation drifted.")

    authority = document.get("authorityBoundary", {})
    expected_authority = {
        "ownerDecisionRequired": True,
        "roundStateMutationApplied": False,
        "round03ActivationAuthorized": False,
        "remotePushAuthorized": False,
        "globalProgramCompletionClaimed": False,
    }
    if authority != expected_authority:
        raise RuntimeError("Round 02 closeout authority boundary drifted.")
    option_ids = {
        item.get("id")
        for item in document.get("decisionOptions", [])
        if isinstance(item, dict)
    }
    if option_ids != {"accept-recommended-closeout", "return-for-more-evidence"}:
        raise RuntimeError("Round 02 owner decision options drifted.")
    if document.get("nextGate") != "owner-reviewed Round 02 stage-closeout decision":
        raise RuntimeError("Round 02 stage-closeout next gate drifted.")

    doc_requirements = {
        "docs/round02-stage-closeout-review.md": [
            "Owner Decision Required",
            "Recommended Round 02 outcome: `complete`",
            "Round 03 remains inactive",
            "does not mutate the round state",
            "Remote push remains outside",
        ],
        "docs/round02-stage-closeout-review.zh-CN.md": [
            "等待所有者决策",
            "建议将 Round 02 的阶段结果判定为：`complete`",
            "Round 03 仍未激活",
            "不允许修改 Round 02 的关闭状态",
            "不包含远端推送授权",
        ],
    }
    for path, phrases in doc_requirements.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                raise RuntimeError(f"Round 02 closeout doc missing phrase in {path}: {phrase}")


def validate_round02_stage_closeout_acceptance_event(
    document: dict[str, object],
    review_doc: dict[str, object],
    rounds_doc: dict[str, object],
    program_doc: dict[str, object],
    lifecycle_doc: dict[str, object],
    acceptance_doc: dict[str, object],
) -> None:
    expected_scalars = {
        "schema": 1,
        "id": "round02-stage-closeout-acceptance-event-2026-07-15",
        "date": "2026-07-15",
        "decision": "accepted-complete-and-pause-for-round03-rebaseline",
        "authoritySource": "owner-selected-option-1",
        "acceptedReview": "registry/round02-stage-closeout-review.json",
        "acceptedReviewCommit": "e4efbe1fdd513941fed60504688a34d1049cb104",
        "acceptedOutcome": "complete",
        "roundId": "round-02-source-intake-and-filtering",
        "roundStateMutationAuthorized": True,
        "round03ActivationAuthorized": False,
        "remotePushAuthorized": False,
        "globalProgramCompletionClaimed": False,
        "nextInitiativeId": "initiative.round03-capability-survey-rebaseline",
    }
    for key, expected in expected_scalars.items():
        if document.get(key) != expected:
            raise RuntimeError(f"Round 02 closeout acceptance event {key} drifted.")
    if review_doc.get("recommendedOutcome") != document.get("acceptedOutcome"):
        raise RuntimeError("Round 02 accepted outcome must match the verified review recommendation.")
    review_risks = {
        item.get("id")
        for item in review_doc.get("residualRisks", [])
        if isinstance(item, dict)
    }
    if set(document.get("acceptedResidualRisks", [])) != review_risks:
        raise RuntimeError("Round 02 accepted residual risks drifted from the review.")
    if document.get("acceptedDeferredWork") != review_doc.get("deferredWork"):
        raise RuntimeError("Round 02 accepted deferred work drifted from the review.")
    expected_effects = {
        "round02Status": "closed",
        "round02StageCloseout": "closed",
        "round03Status": "needs-rebaseline",
        "round03ExecutionActivated": False,
        "currentInitiativeId": "initiative.round03-capability-survey-rebaseline",
    }
    if document.get("stateEffects") != expected_effects:
        raise RuntimeError("Round 02 closeout acceptance state effects drifted.")
    excluded = " ".join(str(item) for item in document.get("doesNotAuthorize", [])).lower()
    for phrase in [
        "round 03 execution",
        "external candidate discovery",
        "candidate code execution",
        "skill admission",
        "runtime mutation",
        "cross-repository delivery",
        "remote push",
        "global program completion",
    ]:
        if phrase not in excluded:
            raise RuntimeError(f"Round 02 closeout acceptance missing non-authorization: {phrase}")

    rounds = {
        item.get("id"): item
        for item in rounds_doc.get("rounds", [])
        if isinstance(item, dict)
    }
    round02 = rounds.get("round-02-source-intake-and-filtering", {})
    round03 = rounds.get("round-03-adaptation-and-curated-admission", {})
    if rounds_doc.get("currentRound") != "round-03-adaptation-and-curated-admission":
        raise RuntimeError("Round registry must advance to the inactive Round 03 rebaseline target.")
    if round02.get("status") != "closed" or round02.get("lifecycle") != {
        "plan": "recorded",
        "execute": "closed",
        "acceptance": "passed",
        "stageCloseout": "closed",
    }:
        raise RuntimeError("Round 02 accepted closeout state drifted.")
    if round02.get("closeoutOutcome") != "complete":
        raise RuntimeError("Round 02 closeout outcome must be complete.")
    if "registry/round02-stage-closeout-acceptance-event-2026-07-15.json" not in round02.get("evidence", []):
        raise RuntimeError("Round 02 must link its closeout acceptance event.")
    if round03.get("status") != "active" or round03.get("lifecycle", {}).get("execute") != "active":
        raise RuntimeError("Round 03 must reflect its later, separately authorized activation.")

    initiatives = {
        item.get("id"): item
        for item in program_doc.get("currentInitiatives", [])
        if isinstance(item, dict)
    }
    round02_initiative = initiatives.get("initiative.round02-stage-closeout-reconciliation", {})
    if round02_initiative.get("status") != "accepted":
        raise RuntimeError("Round 02 initiative must be accepted after the owner decision.")
    if round02_initiative.get("decisionEvidence") != "registry/round02-stage-closeout-acceptance-event-2026-07-15.json":
        raise RuntimeError("Round 02 initiative decision evidence drifted.")
    rebaseline_initiative = initiatives.get(document.get("nextInitiativeId"), {})
    if rebaseline_initiative.get("status") != "accepted":
        raise RuntimeError("The Round 02 next initiative must retain its later owner acceptance.")
    if program_doc.get("currentInitiativeId") != "initiative.capability-survey-gap-proof":
        raise RuntimeError("Program current initiative must reflect the later Round 03 activation.")

    application = lifecycle_doc.get("currentApplication", {})
    if application.get("currentRound") != "round-03-adaptation-and-curated-admission":
        raise RuntimeError("Lifecycle application must advance to Round 03 rebaseline.")
    if application.get("phaseState") != "execute_active" or application.get("stageCloseout") != "not_ready":
        raise RuntimeError("Lifecycle application must reflect the later bounded Round 03 activation.")

    criteria = {
        item.get("id"): item
        for item in acceptance_doc.get("acceptanceCriteria", [])
        if isinstance(item, dict)
    }
    criterion = criteria.get("acceptance.round02-stage-closeout", {})
    if criterion.get("assessment") != "verified":
        raise RuntimeError("Round 02 stage-closeout acceptance must be verified.")
    if "evidence.round02-stage-closeout-acceptance" not in criterion.get("evidenceIds", []):
        raise RuntimeError("Round 02 stage-closeout acceptance evidence is missing.")

    expected_docs = {
        "docs/round02-stage-closeout-acceptance.md": [
            "owner selected option 1",
            "outcome `complete`",
            "Round 03 is not activated",
            "does not authorize",
            "remote push",
        ],
        "docs/round02-stage-closeout-acceptance.zh-CN.md": [
            "所有者选择了",
            "阶段结果接受为 `complete`",
            "Round 03 没有被激活",
            "不授权",
            "远端推送",
        ],
    }
    if set(document.get("evidenceDocs", [])) != set(expected_docs):
        raise RuntimeError("Round 02 closeout acceptance evidence docs drifted.")
    for path, phrases in expected_docs.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                raise RuntimeError(f"Round 02 closeout acceptance doc missing phrase in {path}: {phrase}")


def validate_round03_demand_coordinate_source_contract(
    document: dict[str, object],
    rounds_doc: dict[str, object],
    program_doc: dict[str, object],
    lifecycle_doc: dict[str, object],
    acceptance_doc: dict[str, object],
) -> None:
    expected_scalars = {
        "schema": 1,
        "id": "round03-demand-coordinate-source-contract-2026-07-15",
        "date": "2026-07-15",
        "status": "verified-input-contract",
        "roundId": "round-03-adaptation-and-curated-admission",
        "nextGate": "bounded public metadata discovery for the baseline-eligible demand records",
    }
    for key, expected in expected_scalars.items():
        if document.get(key) != expected:
            raise RuntimeError(f"Round 03 demand-coordinate source contract {key} drifted.")

    expected_binding = {
        "kind": "user-provided-handoff",
        "locator": "C:/tmp/agent-skills-curated-capability-survey-handoff-20260714.md",
        "sha256": "0baedfbf6cb25ff3f30ffba0322f131e02509b37e56a8574cc4d2528a2d0d7a7",
        "bytes": 20564,
        "lines": 441,
    }
    binding = document.get("bindingSource", {})
    for key, expected in expected_binding.items():
        if binding.get(key) != expected:
            raise RuntimeError(f"Round 03 demand-coordinate handoff {key} drifted.")
    if "navigation aid" not in str(binding.get("role", "")).lower():
        raise RuntimeError("Round 03 handoff must remain a non-authoritative navigation aid.")

    expected_sources = {
        "demand-source.research-refresh": (
            "docs/audits/human-ai-shortfall-research-refresh-20260712.md",
            "6c284d003529495d454d5bd8035348a8c347869f2b670a07602fd31380c2f0cd",
            22234,
            293,
        ),
        "demand-source.evidence-ledger": (
            "docs/audits/human-ai-shortfall-evidence-ledger-20260712.md",
            "fb6f339f40a711a0943c956b6fcd6e6a3ee8434bddc1ab9169c65c8fce90c496",
            50688,
            331,
        ),
        "demand-source.two-layer-taxonomy": (
            "docs/audits/human-ai-shortfall-two-layer-taxonomy-20260712.md",
            "2b134dcea65d6e3c6bfdd1386debc421ca1572a4e6bb1610f393dea1eeaa5f4a",
            21330,
            369,
        ),
        "demand-source.problem-owner-gap-matrix": (
            "docs/audits/m1-problem-owner-standard-gap-matrix-20260712.md",
            "dd671768dba9c5ce408f5c33dd88f42125fb4b4027bbbcfc0c36cc679991b9f5",
            39151,
            338,
        ),
    }
    sources = {
        item.get("id"): item
        for item in document.get("sources", [])
        if isinstance(item, dict)
    }
    if set(sources) != set(expected_sources):
        raise RuntimeError("Round 03 demand-coordinate source set drifted.")
    for source_id, expected in expected_sources.items():
        source = sources[source_id]
        path, digest, size, lines = expected
        if (
            source.get("sourceRepository") != "codex-user-config"
            or source.get("repositoryRelativePath") != path
            or source.get("sha256") != digest
            or source.get("bytes") != size
            or source.get("lines") != lines
            or source.get("stage") != "M1/A1"
        ):
            raise RuntimeError(f"Round 03 demand-coordinate source identity drifted: {source_id}")
        if source.get("bodyRedistributionAuthorized") is not False:
            raise RuntimeError(f"Round 03 demand source body redistribution must remain blocked: {source_id}")
        authority = str(source.get("authority", "")).lower()
        if not any(marker in authority for marker in ["not", "only", "authorize no"]) or not any(
            phrase in authority for phrase in ["standard", "audit structure", "diagnostic routing"]
        ):
            raise RuntimeError(f"Round 03 demand source authority is incomplete: {source_id}")

    expected_families = {
        "STM": ("STM-01", "STM-26", 26, "demand-source.two-layer-taxonomy", "candidate-audit-structure-only"),
        "P": ("P1", "P24", 24, "demand-source.two-layer-taxonomy", "historical-alias-and-candidate-control-axis"),
        "SG": ("SG-01", "SG-12", 12, "demand-source.problem-owner-gap-matrix", "candidate-routing-aid-only"),
    }
    families = {
        item.get("family"): item
        for item in document.get("coordinateFamilies", [])
        if isinstance(item, dict)
    }
    if set(families) != set(expected_families):
        raise RuntimeError("Round 03 demand-coordinate family set drifted.")
    for family_id, expected in expected_families.items():
        family = families[family_id]
        actual = (
            family.get("firstId"),
            family.get("lastId"),
            family.get("count"),
            family.get("sourceId"),
            family.get("authorityState"),
        )
        if actual != expected or not family.get("axis"):
            raise RuntimeError(f"Round 03 demand-coordinate family drifted: {family_id}")

    expected_vocabulary = {
        "claimClass": ["FACT", "INTERPRETATION", "INFERENCE", "RECOMMENDATION", "NORMATIVE", "APPLICABILITY"],
        "sourceKind": ["META", "PRIMARY-EMPIRICAL", "BENCHMARK", "PREPRINT", "LAW", "STANDARD", "OFFICIAL-GUIDANCE", "COMMUNITY-GUIDANCE", "VENDOR-PRACTICE", "PRACTITIONER-REFERENCE", "STANDARD-CATALOGUE", "SECONDARY-SYNTHESIS", "PROJECT-INFERENCE"],
        "directness": ["D2-direct", "D1-indirect", "D0-unsupported"],
        "empiricalStrength": ["ES-NA", "ES0", "ES1", "ES2", "ES3"],
        "normativeAuthority": ["NA0", "NA1", "NA2", "NA3"],
        "applicability": ["direct", "bounded-analogy", "out-of-scope", "unknown"],
        "verificationState": ["not-checked", "locator-checked", "claim-checked", "version-mismatch", "contradicted", "held-source-gap"],
        "adoptionState": ["not-adopted", "candidate", "candidate-with-limits", "held", "rejected", "superseded"],
        "freshnessRequired": ["publication-or-update-date", "version-edition-article-report-or-stable-locator", "checked-at-date", "recheck-trigger"],
    }
    if document.get("evidenceVocabulary") != expected_vocabulary:
        raise RuntimeError("Round 03 demand-coordinate evidence vocabulary drifted.")

    binding_rules = " ".join(str(item) for item in document.get("bindingRules", [])).lower()
    if len(document.get("bindingRules", [])) != 5:
        raise RuntimeError("Round 03 demand-coordinate binding rules are incomplete.")
    for phrase in [
        "distinct many-to-many axes",
        "does not prove recurrence",
        "held claims",
        "cannot support a residual-gap claim",
        "not vendored",
    ]:
        if phrase not in binding_rules:
            raise RuntimeError(f"Round 03 demand-coordinate binding rule missing phrase: {phrase}")

    firewall = " ".join(str(item) for item in document.get("promotionFirewall", [])).lower()
    if len(document.get("promotionFirewall", [])) != 4:
        raise RuntimeError("Round 03 demand-coordinate promotion firewall is incomplete.")
    for phrase in [
        "cannot directly authorize a skill",
        "residual failure",
        "yiyuan-calibration",
        "default remains no hook",
    ]:
        if phrase not in firewall:
            raise RuntimeError(f"Round 03 demand-coordinate firewall missing phrase: {phrase}")
    if len(document.get("recheckTriggers", [])) != 5:
        raise RuntimeError("Round 03 demand-coordinate recheck triggers are incomplete.")

    authority = document.get("authorityBoundary", {})
    if len(authority.get("allowed", [])) != 3 or len(authority.get("blocked", [])) != 4:
        raise RuntimeError("Round 03 demand-coordinate authority boundary is incomplete.")
    blocked = " ".join(str(item) for item in authority.get("blocked", [])).lower()
    for phrase in ["copying", "residual-gap proof", "enabling a hook", "activating round 03"]:
        if phrase not in blocked:
            raise RuntimeError(f"Round 03 demand-coordinate blocked authority missing phrase: {phrase}")
    if len(document.get("verificationSurface", [])) != 6:
        raise RuntimeError("Round 03 demand-coordinate verification surface is incomplete.")

    expected_readiness = {
        "sourceIdentityVerified": True,
        "inputContractVerified": True,
        "firstGovernedDemandBatchVerified": True,
        "demandRecordExtractionComplete": False,
        "datedNativeRuntimeBaselineVerified": True,
        "ownerReviewRequired": False,
        "round03ExecutionActivated": True,
        "externalDiscoveryAuthorized": True,
    }
    if document.get("readiness") != expected_readiness:
        raise RuntimeError("Round 03 demand-coordinate readiness drifted.")
    acceptance_event_path = "registry/round03-capability-survey-rebaseline-acceptance-event-2026-07-15.json"
    if document.get("activationEvidence") != acceptance_event_path:
        raise RuntimeError("Round 03 demand-coordinate activation evidence drifted.")
    if document.get("demandRecordBatches") != ["registry/round03-demand-records-batch-01.json"]:
        raise RuntimeError("Round 03 demand-coordinate batch linkage drifted.")
    if document.get("nativeRuntimeBaselines") != ["registry/round03-native-runtime-baseline-2026-07-15.json"]:
        raise RuntimeError("Round 03 native/runtime baseline linkage drifted.")

    round03 = next(
        item
        for item in rounds_doc.get("rounds", [])
        if isinstance(item, dict) and item.get("id") == document.get("roundId")
    )
    path = "registry/round03-demand-coordinate-source-contract.json"
    if path not in round03.get("evidence", []):
        raise RuntimeError("Round 03 registry must link the demand-coordinate source contract.")
    lifecycle_evidence = lifecycle_doc.get("currentApplication", {}).get("evidence", [])
    if path not in lifecycle_evidence:
        raise RuntimeError("Round 03 lifecycle must link the demand-coordinate source contract.")
    initiatives = {
        item.get("id"): item
        for item in program_doc.get("currentInitiatives", [])
        if isinstance(item, dict)
    }
    rebaseline = initiatives.get("initiative.round03-capability-survey-rebaseline", {})
    if "source-pinned demand-coordinate input contract" not in rebaseline.get("resultPackage", []):
        raise RuntimeError("Round 03 rebaseline initiative must include the demand input contract.")

    criteria = {
        item.get("id"): item
        for item in acceptance_doc.get("acceptanceCriteria", [])
        if isinstance(item, dict)
    }
    criterion = criteria.get("acceptance.demand-coordinate-contract", {})
    if criterion.get("assessment") != "partial":
        raise RuntimeError("Demand-coordinate acceptance must remain partial until demand records exist.")
    expected_evidence = {
        "evidence.round03-rebaseline",
        "evidence.round03-demand-coordinate-source-contract",
        "evidence.round03-demand-records-batch-01",
        "evidence.verify-script",
    }
    if set(criterion.get("evidenceIds", [])) != expected_evidence:
        raise RuntimeError("Demand-coordinate acceptance evidence drifted.")
    evidence = {
        item.get("id"): item
        for item in acceptance_doc.get("evidence", [])
        if isinstance(item, dict)
    }
    evidence_record = evidence.get("evidence.round03-demand-coordinate-source-contract", {})
    if evidence_record.get("path") != path or evidence_record.get("kind") != "source-pinned-read-only-input-contract":
        raise RuntimeError("Demand-coordinate source-contract evidence record drifted.")

    expected_docs = {
        "docs/round03-demand-coordinate-source-contract.md": [
            "source-pinned",
            "not copied",
            "does not prove recurrence",
            "no Hook is the default",
            "activated Round 03",
            "first governed demand-record batch",
        ],
        "docs/round03-demand-coordinate-source-contract.zh-CN.md": [
            "按来源身份",
            "不会复制进本仓库",
            "不能证明问题反复发生",
            "默认不使用 Hook",
            "激活 Round 03",
            "第一批受治理需求记录",
        ],
    }
    if set(document.get("evidenceDocs", [])) != set(expected_docs):
        raise RuntimeError("Round 03 demand-coordinate evidence docs drifted.")
    for doc_path, phrases in expected_docs.items():
        text = (ROOT / doc_path).read_text(encoding="utf-8")
        normalized_text = " ".join(text.split())
        for phrase in phrases:
            if phrase not in normalized_text:
                raise RuntimeError(f"Round 03 demand-coordinate doc missing phrase in {doc_path}: {phrase}")


def validate_round03_demand_records_batch_01(
    document: dict[str, object],
    source_contract: dict[str, object],
    acceptance_doc: dict[str, object],
) -> None:
    expected_scalars = {
        "schema": 1,
        "id": "round03-demand-records-batch-01-2026-07-15",
        "date": "2026-07-15",
        "status": "verified-read-only-demand-batch",
        "roundId": "round-03-adaptation-and-curated-admission",
        "sourceContract": "registry/round03-demand-coordinate-source-contract.json",
    }
    for key, expected in expected_scalars.items():
        if document.get(key) != expected:
            raise RuntimeError(f"Round 03 demand-record batch {key} drifted.")
    if document.get("roundId") != source_contract.get("roundId"):
        raise RuntimeError("Round 03 demand-record batch round linkage drifted.")
    if "registry/round03-demand-records-batch-01.json" not in source_contract.get("demandRecordBatches", []):
        raise RuntimeError("Round 03 demand-record source linkage drifted.")

    scope = document.get("scope", {})
    expected_scope = {
        "recordCount": 4,
        "coordinateSelectionMode": "source-selected-discriminating-lanes-not-exhaustive-coordinate-enumeration",
        "sourceLaneIds": ["EL-01", "EL-02", "EL-03", "EL-04"],
        "sourceIds": [
            "demand-source.evidence-ledger",
            "demand-source.two-layer-taxonomy",
            "demand-source.problem-owner-gap-matrix",
        ],
        "researchBodyCopied": False,
        "demandExtractionComplete": False,
        "nativeRuntimeBaselineRequiredBeforeDiscovery": True,
    }
    if scope != expected_scope:
        raise RuntimeError("Round 03 demand-record batch scope drifted.")

    expected_records = {
        "EL-01": ("round03-demand.el-01-transition-continuity", {"SG-02", "SG-07"}),
        "EL-02": ("round03-demand.el-02-routing-portability-cost", {"SG-04", "SG-09", "SG-12"}),
        "EL-03": ("round03-demand.el-03-evidence-human-review", {"SG-06", "SG-08"}),
        "EL-04": ("round03-demand.el-04-projection-governance", {"SG-11"}),
    }
    records = {
        item.get("sourceLaneId"): item
        for item in document.get("records", [])
        if isinstance(item, dict)
    }
    if len(document.get("records", [])) != 4 or set(records) != set(expected_records):
        raise RuntimeError("Round 03 demand-record lane set drifted.")
    all_claims: set[str] = set()
    for lane_id, (record_id, expected_sg) in expected_records.items():
        record = records[lane_id]
        if record.get("id") != record_id or not record.get("title") or not record.get("demand"):
            raise RuntimeError(f"Round 03 demand record identity drifted: {lane_id}")
        coordinates = record.get("coordinateIds", {})
        if set(coordinates) != {"SG", "P", "STM"} or set(coordinates.get("SG", [])) != expected_sg:
            raise RuntimeError(f"Round 03 demand record SG mapping drifted: {lane_id}")
        for family, pattern in [("SG", r"SG-(0[1-9]|1[0-2])"), ("P", r"P([1-9]|1[0-9]|2[0-4])"), ("STM", r"STM-(0[1-9]|1[0-9]|2[0-6])")]:
            values = coordinates.get(family, [])
            if not values or len(values) != len(set(values)) or any(re.fullmatch(pattern, value) is None for value in values):
                raise RuntimeError(f"Round 03 demand record coordinate mapping invalid: {lane_id}/{family}")
        claim_ids = record.get("evidenceClaimIds", [])
        if not claim_ids or any(re.fullmatch(r"CLM-(00[1-9]|0[1-4][0-9]|05[0-2])", value) is None for value in claim_ids):
            raise RuntimeError(f"Round 03 demand record evidence claims invalid: {lane_id}")
        all_claims.update(claim_ids)
        evidence_state = record.get("evidenceState", {})
        if set(evidence_state) != {"verificationStates", "adoptionStates", "applicability"} or any(
            not evidence_state.get(key) for key in evidence_state
        ):
            raise RuntimeError(f"Round 03 demand record evidence state incomplete: {lane_id}")
        vocabulary = source_contract.get("evidenceVocabulary", {})
        expected_vocabularies = {
            "verificationStates": set(vocabulary.get("verificationState", [])),
            "adoptionStates": set(vocabulary.get("adoptionState", [])),
            "applicability": set(vocabulary.get("applicability", [])),
        }
        for field, allowed_values in expected_vocabularies.items():
            if not set(evidence_state.get(field, [])).issubset(allowed_values):
                raise RuntimeError(f"Round 03 demand record evidence vocabulary drifted: {lane_id}/{field}")
        for field in ["uncertainty", "heldClaims", "affectedSubjects", "recheckTriggers"]:
            if len(record.get(field, [])) < 2:
                raise RuntimeError(f"Round 03 demand record {field} incomplete: {lane_id}")
        expected_route = (
            ("baseline-recorded-human-authority-route", False)
            if lane_id == "EL-03"
            else ("baseline-recorded-discovery-question-bound", True)
        )
        if (
            record.get("surveyState") != expected_route[0]
            or record.get("residualGapState") != "not-assessed"
            or record.get("candidateDiscoveryEligible") is not expected_route[1]
        ):
            raise RuntimeError(f"Round 03 demand record gate drifted: {lane_id}")
    for required_claim in ["CLM-003", "CLM-044", "CLM-051", "CLM-001", "CLM-009", "CLM-005", "CLM-039"]:
        if required_claim not in all_claims:
            raise RuntimeError(f"Round 03 demand-record evidence coverage missing: {required_claim}")

    expected_decision = {
        "demandCoordinatesBound": True,
        "coordinateCorpusExhaustivelyEnumerated": False,
        "nativeRuntimeBaselineComplete": True,
        "publicCandidateDiscoveryMayStart": True,
        "candidateExecutionAuthorized": False,
        "skillOrHookCreationAuthorized": False,
        "standardPromotionAuthorized": False,
        "nextGate": "bounded public metadata discovery for EL-01, EL-02, and EL-04; EL-03 remains on the human/domain-authority path",
    }
    if document.get("batchDecision") != expected_decision:
        raise RuntimeError("Round 03 demand-record batch decision drifted.")
    if len(document.get("verificationSurface", [])) != 5:
        raise RuntimeError("Round 03 demand-record verification surface drifted.")

    evidence = {
        item.get("id"): item
        for item in acceptance_doc.get("evidence", [])
        if isinstance(item, dict)
    }
    evidence_record = evidence.get("evidence.round03-demand-records-batch-01", {})
    if (
        evidence_record.get("path") != "registry/round03-demand-records-batch-01.json"
        or evidence_record.get("kind") != "verified-read-only-demand-batch"
        or evidence_record.get("supports") != ["acceptance.demand-coordinate-contract"]
    ):
        raise RuntimeError("Round 03 demand-record acceptance evidence drifted.")

    expected_docs = {
        "docs/round03-demand-records-batch-01.md": [
            "four discriminating evidence lanes",
            "not complete",
            "Bounded public metadata discovery is eligible only",
            "does not authorize candidate execution",
        ],
        "docs/round03-demand-records-batch-01.zh-CN.md": [
            "4 条“可区分根因的证据通道”",
            "尚未完成",
            "只有 `EL-01`、`EL-02`、`EL-04` 具备",
            "不授权执行候选",
        ],
    }
    if set(document.get("evidenceDocs", [])) != set(expected_docs):
        raise RuntimeError("Round 03 demand-record evidence docs drifted.")
    for doc_path, phrases in expected_docs.items():
        text = " ".join((ROOT / doc_path).read_text(encoding="utf-8").split())
        for phrase in phrases:
            if phrase not in text:
                raise RuntimeError(f"Round 03 demand-record doc missing phrase in {doc_path}: {phrase}")


def validate_round03_native_runtime_baseline(
    document: dict[str, object],
    demand_batch: dict[str, object],
    source_contract: dict[str, object],
    rounds_doc: dict[str, object],
    lifecycle_doc: dict[str, object],
    acceptance_doc: dict[str, object],
) -> None:
    expected_scalars = {
        "schema": 1,
        "id": "round03-native-runtime-baseline-2026-07-15",
        "date": "2026-07-15",
        "status": "verified-dated-local-metadata-baseline",
        "roundId": "round-03-adaptation-and-curated-admission",
        "demandBatch": "registry/round03-demand-records-batch-01.json",
    }
    for key, expected in expected_scalars.items():
        if document.get(key) != expected:
            raise RuntimeError(f"Round 03 native/runtime baseline {key} drifted.")
    if document.get("roundId") != demand_batch.get("roundId") or document.get("roundId") != source_contract.get("roundId"):
        raise RuntimeError("Round 03 native/runtime baseline round linkage drifted.")
    if document.get("demandBatch") not in source_contract.get("demandRecordBatches", []):
        raise RuntimeError("Round 03 native/runtime baseline demand linkage drifted.")

    scope = document.get("scope", {})
    expected_scope = {
        "host": "OpenAI Codex desktop on Windows",
        "cliVersionObserved": "codex-cli 0.144.4",
        "desktopPackagePathVersionObserved": "26.707.9981.0",
        "modelIdentity": "runtime-declared GPT-5 family; exact model build not exposed to this repository baseline",
        "reasoningLevel": "not observable from the local metadata probes",
        "loader": "current Codex session exposes Skill metadata and loads selected Skill bodies; this artifact does not claim deterministic implicit activation",
        "permissions": "workspace write limited to the bound repository and temporary workspace; local capability inspection was read-only",
        "workspace": "C:/Projects/agent-skills-curated",
        "accountBoundary": "no account connection, OAuth, credential read, private remote, or external write",
        "crossHostClaim": False,
    }
    if scope != expected_scope:
        raise RuntimeError("Round 03 native/runtime baseline scope drifted.")

    observations = document.get("observations", {})
    expected_roots = {
        "C:/Users/15521/.codex/skills": 8,
        "C:/Users/15521/.agents/skills": 30,
        "C:/Users/15521/.cc-switch/skills": 73,
        "C:/Users/15521/.codex/plugins/cache": 311,
    }
    roots = {item.get("path"): item.get("skillFileCount") for item in observations.get("skillRoots", [])}
    if roots != expected_roots:
        raise RuntimeError("Round 03 native/runtime Skill-root snapshot drifted.")
    name_surface = observations.get("skillNameSurface", {})
    if (
        name_surface.get("skillFileCount") != 422
        or name_surface.get("uniqueDirectoryNameCount") != 326
        or name_surface.get("duplicateDirectoryNameGroupCount") != 87
        or name_surface.get("maximumObservedCopiesForOneDirectoryName") != 3
        or "does not prove" not in str(name_surface.get("interpretation", ""))
    ):
        raise RuntimeError("Round 03 native/runtime Skill-name surface drifted.")
    expected_contracts = {
        "intent-contract": (29139, "1d67e4b84856bcd0828d89b82803a7275d95d8e586fd8efcd127f89e82845753"),
        "capability-router": (22018, "eb9f7d253d12682a3e8b9f87faf5bad4284a2d268b25c30cc5ad9f6dd36eb8fe"),
        "closure-contract": (12187, "59edfc131c45b7aa1ef85a1737317a0cc97adcfb0ddceb7ee81e9c744b13bbb3"),
    }
    pairs = {item.get("id"): item for item in observations.get("contractSkillPairs", [])}
    if set(pairs) != set(expected_contracts):
        raise RuntimeError("Round 03 native/runtime contract-Skill pair set drifted.")
    for skill_id, (size, digest) in expected_contracts.items():
        pair = pairs[skill_id]
        if pair.get("bytesEach") != size or pair.get("sha256Each") != digest or pair.get("identicalAtObservation") is not True or len(pair.get("paths", [])) != 2:
            raise RuntimeError(f"Round 03 native/runtime contract-Skill identity drifted: {skill_id}")
    hook = observations.get("hookMetadata", {})
    if (
        hook.get("candidatePolicyId") != "capability-ecosystem-recall"
        or hook.get("declaredMode") != "auto"
        or hook.get("filePresenceProvesActivation") is not False
        or hook.get("effectiveActivationObserved") != "not-checked"
        or hook.get("behaviorProbeRun") is not False
    ):
        raise RuntimeError("Round 03 native/runtime Hook metadata boundary drifted.")
    posture = observations.get("repositoryPosture", {})
    if posture.get("branch") != "main" or posture.get("head") != "603ac684ecdac70efc1467bdffb95676ebfeee3a" or posture.get("dirtyAtObservation") is not False or posture.get("remotePushAuthorized") is not False:
        raise RuntimeError("Round 03 native/runtime repository posture drifted.")

    demand_records = {item.get("id"): item for item in demand_batch.get("records", [])}
    baselines = {item.get("demandRecordId"): item for item in document.get("demandBaselines", [])}
    if len(document.get("demandBaselines", [])) != 4 or set(baselines) != set(demand_records):
        raise RuntimeError("Round 03 native/runtime demand coverage drifted.")
    eligible = {
        "round03-demand.el-01-transition-continuity",
        "round03-demand.el-02-routing-portability-cost",
        "round03-demand.el-04-projection-governance",
    }
    for demand_id, baseline in baselines.items():
        expected_eligible = demand_id in eligible
        if (
            not baseline.get("currentPaths")
            or not baseline.get("observedSupport")
            or not baseline.get("insufficiency")
            or not baseline.get("gapClass")
            or baseline.get("publicMetadataDiscoveryEligible") is not expected_eligible
            or baseline.get("residualGapState") != "not-assessed"
        ):
            raise RuntimeError(f"Round 03 native/runtime demand baseline incomplete: {demand_id}")
        if expected_eligible != bool(baseline.get("externalMetadataQuestion")):
            raise RuntimeError(f"Round 03 native/runtime discovery question drifted: {demand_id}")
        if demand_records[demand_id].get("candidateDiscoveryEligible") is not expected_eligible:
            raise RuntimeError(f"Round 03 native/runtime demand eligibility mismatch: {demand_id}")

    expected_decision = {
        "baselineRecordedForEveryDemandRecord": True,
        "currentCapabilityInsufficiencyBoundForEligibleDiscovery": True,
        "eligibleDemandRecordIds": sorted(eligible),
        "excludedDemandRecordIds": ["round03-demand.el-03-evidence-human-review"],
        "boundedPublicMetadataDiscoveryMayStart": True,
        "behavioralCoverageProven": False,
        "residualGapProven": False,
        "candidateExecutionAuthorized": False,
        "hookEnablementAuthorized": False,
        "standardPromotionAuthorized": False,
        "nextGate": "bounded public metadata discovery, clustering, and source-pinned non-executing representative review for the three eligible demand records",
    }
    decision = document.get("baselineDecision", {})
    if {**decision, "eligibleDemandRecordIds": sorted(decision.get("eligibleDemandRecordIds", []))} != expected_decision:
        raise RuntimeError("Round 03 native/runtime baseline decision drifted.")
    if len(document.get("limitations", [])) != 5 or len(document.get("recheckTriggers", [])) != 5:
        raise RuntimeError("Round 03 native/runtime limitations or recheck triggers drifted.")

    baseline_path = "registry/round03-native-runtime-baseline-2026-07-15.json"
    round03 = next(item for item in rounds_doc.get("rounds", []) if isinstance(item, dict) and item.get("id") == document.get("roundId"))
    if baseline_path not in round03.get("evidence", []) or demand_batch.get("id") is None:
        raise RuntimeError("Round 03 registry must link the native/runtime baseline.")
    if baseline_path not in lifecycle_doc.get("currentApplication", {}).get("evidence", []):
        raise RuntimeError("Round 03 lifecycle must link the native/runtime baseline.")
    evidence = {item.get("id"): item for item in acceptance_doc.get("evidence", []) if isinstance(item, dict)}
    evidence_record = evidence.get("evidence.round03-native-runtime-baseline", {})
    if evidence_record.get("path") != baseline_path or evidence_record.get("kind") != "verified-dated-local-metadata-baseline":
        raise RuntimeError("Round 03 native/runtime acceptance evidence drifted.")
    criteria = {item.get("id"): item for item in acceptance_doc.get("acceptanceCriteria", []) if isinstance(item, dict)}
    criterion = criteria.get("acceptance.native-runtime-baseline", {})
    if criterion.get("assessment") != "partial" or criterion.get("evidenceIds") != ["evidence.round03-native-runtime-baseline"]:
        raise RuntimeError("Round 03 native/runtime acceptance mapping drifted.")

    expected_docs = {
        "docs/round03-native-runtime-baseline-2026-07-15.md": ["422", "87 duplicate-name groups", "file presence does not prove activation", "EL-03", "neither behavioral coverage nor a residual gap"],
        "docs/round03-native-runtime-baseline-2026-07-15.zh-CN.md": ["422", "87 组重名", "文件存在不能证明已激活", "EL-03", "既不证明行为覆盖，也不证明残余缺口"],
    }
    if set(document.get("evidenceDocs", [])) != set(expected_docs):
        raise RuntimeError("Round 03 native/runtime evidence docs drifted.")
    for doc_path, phrases in expected_docs.items():
        text = " ".join((ROOT / doc_path).read_text(encoding="utf-8").split())
        for phrase in phrases:
            if phrase not in text:
                raise RuntimeError(f"Round 03 native/runtime doc missing phrase in {doc_path}: {phrase}")


def validate_round03_public_discovery_snapshot(
    document: dict[str, object],
    baseline_doc: dict[str, object],
    rounds_doc: dict[str, object],
    lifecycle_doc: dict[str, object],
    acceptance_doc: dict[str, object],
) -> None:
    expected_scalars = {
        "schema": 1,
        "id": "round03-public-discovery-snapshot-2026-07-15",
        "observedAt": "2026-07-15T06:10:09.8213981Z",
        "status": "verified-public-metadata-snapshot",
        "roundId": "round-03-adaptation-and-curated-admission",
        "baseline": "registry/round03-native-runtime-baseline-2026-07-15.json",
    }
    for key, expected in expected_scalars.items():
        if document.get(key) != expected:
            raise RuntimeError(f"Round 03 public discovery snapshot {key} drifted.")
    if document.get("roundId") != baseline_doc.get("roundId"):
        raise RuntimeError("Round 03 public discovery baseline linkage drifted.")
    expected_boundary = {
        "githubVisibility": "public-only",
        "queriesRequire": "is:public",
        "privateRepositoryMetadataAllowed": False,
        "credentialsOrAccountDataRecorded": False,
        "sourceBodiesVendored": False,
        "candidateCodeExecuted": False,
        "candidateInstalledOrConnected": False,
        "externalWritePerformed": False,
    }
    if document.get("dataBoundary") != expected_boundary:
        raise RuntimeError("Round 03 public discovery data boundary drifted.")

    expected_queries = {
        "broad-public-agent-skills": ("agent skills is:public", 86559),
        "el01-state-handoff": ("agent skills handoff state continuation is:public", 1),
        "el02-manager-registry": ("agent skills manager registry is:public", 26),
        "el04-provenance-lifecycle": ("agent skills provenance lifecycle registry is:public", 0),
        "skill-md-public": ("AI agent skills SKILL.md is:public", 549),
        "awesome-public": ("awesome agent skills is:public", 636),
        "el04-lockfile": ("agent skill lockfile is:public", 19),
        "el04-supply-chain": ("agent skill supply chain is:public", 110),
        "el04-sync-governance": ("agent skill sync governance is:public", 11),
    }
    queries = {}
    for query_round in document.get("queryRounds", []):
        for query in query_round.get("queries", []):
            queries[query.get("id")] = query
    if set(queries) != set(expected_queries):
        raise RuntimeError("Round 03 public discovery query set drifted.")
    for query_id, (query_text, total_count) in expected_queries.items():
        query = queries[query_id]
        if query.get("query") != query_text or query.get("totalCount") != total_count or not query.get("assessment"):
            raise RuntimeError(f"Round 03 public discovery query evidence drifted: {query_id}")
        if "is:public" not in query_text:
            raise RuntimeError(f"Round 03 public discovery query lost public-only boundary: {query_id}")
    if "not absence evidence" not in queries["el04-provenance-lifecycle"].get("assessment", ""):
        raise RuntimeError("Round 03 public discovery must reject zero-hit absence inference.")

    expected_clusters = {
        "cluster.official-external-baselines",
        "cluster.state-continuity-and-handoff",
        "cluster.package-management-reproducibility-and-projection",
        "cluster.validation-security-and-policy",
        "cluster.index-and-radar",
    }
    clusters = {item.get("id"): item for item in document.get("clusters", []) if isinstance(item, dict)}
    if set(clusters) != expected_clusters:
        raise RuntimeError("Round 03 public discovery cluster set drifted.")
    for cluster_id, cluster in clusters.items():
        if not cluster.get("demandRecordIds") or not cluster.get("role") or not cluster.get("representativeSourceIds") or not cluster.get("boundary"):
            raise RuntimeError(f"Round 03 public discovery cluster incomplete: {cluster_id}")

    expected_sources = {
        "github:anthropics/skills": ("9d2f1ae187231d8199c64b5b762e1bdf2244733d", "NOASSERTION", 18, "official-external-baseline"),
        "github:github/awesome-copilot": ("2c2461a7fa383f664bb75546f03a2c6087f3819d", "MIT", 389, "official-external-baseline"),
        "github:OthmanAdi/planning-with-files": ("f90780c92f0506d21c5f6c4865ce95517a8b1964", "MIT", 17, "third-party-state-and-continuity-system"),
        "github:cskwork/handoff-skill": ("7bf202579770b6b0dc94cbeba12fa36f0b2a3929", "MIT", 1, "third-party-handoff-skill"),
        "github:tankpkg/tank": ("bd0df404e39086194e5e34126daa052d59a5a043", "MIT", 6, "external-skill-package-manager-and-security-baseline"),
        "github:astra-sh/qvr": ("71783910729031afe6ad1d640728b1534ee4c198", "MIT", 30, "external-lockfile-first-skill-package-manager"),
        "github:Narwhal-Lab/MagicSkills": ("00f3e8640445b0d91682a670b8ba7cc4465151cb", "MIT", 1, "external-shared-skill-pool-and-projection-tooling"),
        "github:agent-sh/agnix": ("1a9edf65a9804893429c7444f3f4f69e7a0cdf28", "Apache-2.0", 41, "external-agent-configuration-validator"),
        "github:VoltAgent/awesome-agent-skills": ("c97eda5e3406670f3285c6bf9eb7639a7ecc03cc", "MIT", 0, "public-skill-index"),
    }
    sources = {item.get("id"): item for item in document.get("representativeSources", []) if isinstance(item, dict)}
    if len(document.get("representativeSources", [])) != 9 or set(sources) != set(expected_sources):
        raise RuntimeError("Round 03 public discovery representative source set drifted.")
    for source_id, (commit, license_id, skill_count, source_class) in expected_sources.items():
        source = sources[source_id]
        if (
            source.get("commit") != commit
            or source.get("licenseMetadata") != license_id
            or source.get("skillMdCount") != skill_count
            or source.get("sourceClass") != source_class
            or source.get("treeTruncated") is not False
            or source.get("archived") is not False
            or not source.get("initialDisposition")
            or not source.get("reviewSignals")
            or not source.get("reviewRisks")
        ):
            raise RuntimeError(f"Round 03 public discovery representative source drifted: {source_id}")
        if not re.fullmatch(r"[0-9a-f]{40}", source.get("commit", "")):
            raise RuntimeError(f"Round 03 public discovery source is not commit-pinned: {source_id}")
    if "no-body-admission" not in sources["github:anthropics/skills"].get("initialDisposition", ""):
        raise RuntimeError("Round 03 official baseline body boundary drifted.")
    if sources["github:VoltAgent/awesome-agent-skills"].get("initialDisposition") != "discovery-index-child-sources-only":
        raise RuntimeError("Round 03 index disposition drifted.")

    saturation = document.get("saturation", {})
    if saturation.get("queryExpansionStopped") is not True or saturation.get("marginalYield") != "low-for-new-cluster-discovery, still-material-for-child-source-enumeration":
        raise RuntimeError("Round 03 public discovery saturation state drifted.")
    if len(saturation.get("remainingUncertainty", [])) != 5 or len(saturation.get("recheckTriggers", [])) != 5:
        raise RuntimeError("Round 03 public discovery saturation evidence is incomplete.")
    decision = document.get("snapshotDecision", {})
    expected_false = ["officialBodiesAdmitted", "thirdPartyCandidateApproved", "candidateExecutionAuthorized", "installationAuthorized", "hookEnablementAuthorized", "residualGapProven", "standardPromotionAuthorized"]
    if any(decision.get(key) is not False for key in expected_false) or decision.get("nextGate") != "pinned license, security, portability, overlap, and architecture review for the representative sources before alternative comparison":
        raise RuntimeError("Round 03 public discovery non-approval decision drifted.")

    snapshot_path = "registry/round03-public-discovery-snapshot-2026-07-15.json"
    round03 = next(item for item in rounds_doc.get("rounds", []) if isinstance(item, dict) and item.get("id") == document.get("roundId"))
    if snapshot_path not in round03.get("evidence", []):
        raise RuntimeError("Round 03 registry must link the public discovery snapshot.")
    application = lifecycle_doc.get("currentApplication", {})
    if snapshot_path not in application.get("evidence", []) or application.get("nextRequiredEvidence") != ["demand-level alternative comparison before any residual-gap, repository-authoring, or Hook decision"]:
        raise RuntimeError("Round 03 lifecycle public discovery evidence drifted.")
    evidence = {item.get("id"): item for item in acceptance_doc.get("evidence", []) if isinstance(item, dict)}
    evidence_record = evidence.get("evidence.round03-public-discovery-snapshot", {})
    if evidence_record.get("path") != snapshot_path or evidence_record.get("kind") != "verified-public-metadata-snapshot":
        raise RuntimeError("Round 03 public discovery acceptance evidence drifted.")
    criteria = {item.get("id"): item for item in acceptance_doc.get("acceptanceCriteria", []) if isinstance(item, dict)}
    criterion = criteria.get("acceptance.discovery-clustering-stop-rule", {})
    if criterion.get("assessment") != "partial" or "evidence.round03-public-discovery-snapshot" not in criterion.get("evidenceIds", []):
        raise RuntimeError("Round 03 public discovery acceptance mapping drifted.")

    expected_docs = {
        "docs/round03-public-discovery-snapshot-2026-07-15.md": ["public-only", "five clusters", "zero results", "Nine representative public sources", "No residual gap or Hook need is proven"],
        "docs/round03-public-discovery-snapshot-2026-07-15.zh-CN.md": ["仅公共", "5 个簇", "返回 0 条", "9 个公共代表源", "残余缺口和 Hook 必要性也都没有成立"],
    }
    if set(document.get("evidenceDocs", [])) != set(expected_docs):
        raise RuntimeError("Round 03 public discovery evidence docs drifted.")
    for doc_path, phrases in expected_docs.items():
        text = " ".join((ROOT / doc_path).read_text(encoding="utf-8").split())
        for phrase in phrases:
            if phrase not in text:
                raise RuntimeError(f"Round 03 public discovery doc missing phrase in {doc_path}: {phrase}")


def validate_round03_representative_source_review_batch_01(
    document: dict[str, object],
    discovery_doc: dict[str, object],
    rounds_doc: dict[str, object],
    lifecycle_doc: dict[str, object],
    acceptance_doc: dict[str, object],
) -> None:
    expected_scalars = {
        "schema": 1,
        "id": "round03-representative-source-review-batch-01-2026-07-15",
        "date": "2026-07-15",
        "status": "verified-non-executing-static-review",
        "roundId": "round-03-adaptation-and-curated-admission",
        "discoverySnapshot": "registry/round03-public-discovery-snapshot-2026-07-15.json",
    }
    for key, expected in expected_scalars.items():
        if document.get(key) != expected:
            raise RuntimeError(f"Round 03 representative review {key} drifted.")
    if document.get("roundId") != discovery_doc.get("roundId"):
        raise RuntimeError("Round 03 representative review discovery linkage drifted.")
    expected_boundary = {
        "sourceCommitPinned": True,
        "publicSourceTextOnly": True,
        "licenseMetadataAloneAccepted": False,
        "candidateCodeExecuted": False,
        "candidateInstalledOrConnected": False,
        "runtimeOrHookMutated": False,
        "crossRepositoryWritePerformed": False,
        "approvalOrAdmissionGranted": False,
    }
    if document.get("reviewBoundary") != expected_boundary:
        raise RuntimeError("Round 03 representative review boundary drifted.")

    discovered_sources = {item.get("id"): item for item in discovery_doc.get("representativeSources", []) if isinstance(item, dict)}
    reviews = {item.get("sourceId"): item for item in document.get("reviews", []) if isinstance(item, dict)}
    if len(document.get("reviews", [])) != 9 or set(reviews) != set(discovered_sources):
        raise RuntimeError("Round 03 representative review source set drifted.")
    expected_license_blobs = {
        "github:anthropics/skills": {"ffef92c48b351a3ed036556ed32dda934e8cf41a"},
        "github:github/awesome-copilot": {"89bc5e962c9944cdb050887062afdaaf89be504a"},
        "github:OthmanAdi/planning-with-files": {"a00edac2c06c65f72f6fa7dc75512541213aa771"},
        "github:cskwork/handoff-skill": {"a021cf23a307b4507384a9cddbb84c06dc1b962d"},
        "github:tankpkg/tank": {"6e1bbf0f1a97a1b717b9338a2acaadb2f881856f"},
        "github:astra-sh/qvr": {"7662dc97b8d6fc689224e91a7df1257092beb642"},
        "github:Narwhal-Lab/MagicSkills": {"c13f99117e366fd54b4c097b67ca34dfb1fb8ba1"},
        "github:agent-sh/agnix": {"20353a1578f42da974a8ddd0ce6bb7501b9267d6", "99731088716bc07bc882beb13d727eaee198c2d0"},
        "github:VoltAgent/awesome-agent-skills": {"a0d0a9bbe350d5c6f22a61ca408364e1c36c964d"},
    }
    for source_id, review in reviews.items():
        if review.get("sourceClass") != discovered_sources[source_id].get("sourceClass"):
            raise RuntimeError(f"Round 03 representative review source class drifted: {source_id}")
        license_review = review.get("licenseReview", {})
        blobs = {item.get("gitBlob") for item in license_review.get("evidence", []) if isinstance(item, dict)}
        if blobs != expected_license_blobs[source_id] or not license_review.get("state") or not license_review.get("limit"):
            raise RuntimeError(f"Round 03 representative license review drifted: {source_id}")
        for field in ["architecture", "executableSurfaceState", "securityState", "portabilityState", "overlapState", "disposition", "nextUse"]:
            if not review.get(field):
                raise RuntimeError(f"Round 03 representative review field missing: {source_id}/{field}")

    planning = reviews["github:OthmanAdi/planning-with-files"]
    for phrase in ["235 executable", "Hook", "completion"]:
        if phrase not in planning.get("architecture", ""):
            raise RuntimeError(f"Round 03 planning-system executable review missing: {phrase}")
    if planning.get("disposition") != "hold-as-heavy-system-reference-not-skill-admission-candidate":
        raise RuntimeError("Round 03 planning-system disposition drifted.")
    handoff = reviews["github:cskwork/handoff-skill"]
    expected_identity = {
        "pinnedBodySha256": "f77dea488eb8242b58be186b2a354a004b5571841cd61b9ad4bb4fa82f5735d2",
        "installedComparisonSha256": "d215dd8f2a19bf85fdaf67a3cdb5077641f6b4108f229ba79579414793d7b0a3",
        "exactDuplicate": False,
    }
    if handoff.get("contentIdentity") != expected_identity or handoff.get("disposition") != "candidate-with-limits-for-content-and-alternative-comparison":
        raise RuntimeError("Round 03 handoff overlap review drifted.")
    expected_tool_counts = {
        "github:tankpkg/tank": "784 executable",
        "github:astra-sh/qvr": "434 executable",
        "github:Narwhal-Lab/MagicSkills": "42 executable",
        "github:agent-sh/agnix": "205 executable",
    }
    for source_id, phrase in expected_tool_counts.items():
        review = reviews[source_id]
        if phrase not in review.get("architecture", "") or "non-skill" not in review.get("disposition", ""):
            raise RuntimeError(f"Round 03 non-Skill tooling review drifted: {source_id}")
    if reviews["github:anthropics/skills"].get("disposition") != "exclude-official-bodies-from-managed-inventory":
        raise RuntimeError("Round 03 official body exclusion drifted.")
    if reviews["github:VoltAgent/awesome-agent-skills"].get("disposition") != "discovery-index-only":
        raise RuntimeError("Round 03 index-only disposition drifted.")

    expected_decision = {
        "reviewedSourceCount": 9,
        "officialBaselineCount": 2,
        "indexCount": 1,
        "skillContentComparisonCount": 2,
        "nonSkillToolingAlternativeCount": 4,
        "approvedCandidateCount": 0,
        "executableCandidateCount": 0,
        "residualGapProven": False,
        "hookNeedProven": False,
        "nextGate": "demand-level alternative comparison across native, installed handoff, the two reviewed Skill systems, four non-Skill tooling paths, project standards, and human authority",
    }
    if document.get("batchDecision") != expected_decision:
        raise RuntimeError("Round 03 representative review decision drifted.")
    if len(document.get("recheckTriggers", [])) != 5:
        raise RuntimeError("Round 03 representative review triggers drifted.")

    review_path = "registry/round03-representative-source-review-batch-01.json"
    round03 = next(item for item in rounds_doc.get("rounds", []) if isinstance(item, dict) and item.get("id") == document.get("roundId"))
    if review_path not in round03.get("evidence", []):
        raise RuntimeError("Round 03 registry must link the representative review.")
    application = lifecycle_doc.get("currentApplication", {})
    if review_path not in application.get("evidence", []) or application.get("nextRequiredEvidence") != ["demand-level alternative comparison before any residual-gap, repository-authoring, or Hook decision"]:
        raise RuntimeError("Round 03 lifecycle representative review evidence drifted.")
    evidence = {item.get("id"): item for item in acceptance_doc.get("evidence", []) if isinstance(item, dict)}
    evidence_record = evidence.get("evidence.round03-representative-source-review-batch-01", {})
    if evidence_record.get("path") != review_path or evidence_record.get("kind") != "verified-non-executing-static-review":
        raise RuntimeError("Round 03 representative review acceptance evidence drifted.")
    criteria = {item.get("id"): item for item in acceptance_doc.get("acceptanceCriteria", []) if isinstance(item, dict)}
    criterion = criteria.get("acceptance.discovery-clustering-stop-rule", {})
    if criterion.get("assessment") != "partial" or "evidence.round03-representative-source-review-batch-01" not in criterion.get("evidenceIds", []):
        raise RuntimeError("Round 03 representative review acceptance mapping drifted.")

    expected_docs = {
        "docs/round03-representative-source-review-batch-01.md": ["nine pinned representatives", "not an exact duplicate", "235 executable", "No source is approved or executable"],
        "docs/round03-representative-source-review-batch-01.zh-CN.md": ["9 个固定提交", "并非精确重复", "235 个可执行", "没有任何来源获批或可执行"],
    }
    if set(document.get("evidenceDocs", [])) != set(expected_docs):
        raise RuntimeError("Round 03 representative review evidence docs drifted.")
    for doc_path, phrases in expected_docs.items():
        text = " ".join((ROOT / doc_path).read_text(encoding="utf-8").split())
        for phrase in phrases:
            if phrase not in text:
                raise RuntimeError(f"Round 03 representative review doc missing phrase in {doc_path}: {phrase}")


def validate_round03_capability_survey_rebaseline(
    document: dict[str, object],
    demand_contract: dict[str, object],
    rounds_doc: dict[str, object],
    program_doc: dict[str, object],
    lifecycle_doc: dict[str, object],
    acceptance_doc: dict[str, object],
) -> None:
    expected_scalars = {
        "schema": 1,
        "id": "round03-capability-survey-rebaseline-2026-07-15",
        "date": "2026-07-15",
        "status": "accepted",
        "roundId": "round-03-adaptation-and-curated-admission",
        "initiativeId": "initiative.round03-capability-survey-rebaseline",
        "nextGate": "bounded public metadata discovery for EL-01, EL-02, and EL-04",
    }
    for key, expected in expected_scalars.items():
        if document.get(key) != expected:
            raise RuntimeError(f"Round 03 capability-survey rebaseline {key} drifted.")
    for path in document.get("basis", []):
        if not isinstance(path, str) or not (ROOT / path).is_file():
            raise RuntimeError(f"Round 03 rebaseline basis is missing: {path}")
    demand_contract_path = "registry/round03-demand-coordinate-source-contract.json"
    if document.get("demandInputContract") != demand_contract_path:
        raise RuntimeError("Round 03 rebaseline demand input contract link drifted.")
    if demand_contract_path not in document.get("basis", []):
        raise RuntimeError("Round 03 rebaseline basis must include the demand input contract.")
    if demand_contract.get("roundId") != document.get("roundId"):
        raise RuntimeError("Round 03 rebaseline and demand input contract round identity drifted.")
    scope = document.get("scope", {})
    if not scope.get("allowed") or not scope.get("blocked"):
        raise RuntimeError("Round 03 rebaseline scope must declare allowed and blocked work.")
    blocked = " ".join(str(item) for item in scope.get("blocked", [])).lower()
    for phrase in [
        "bulk clone",
        "executing candidate",
        "oauth",
        "runtime mutation",
        "skill admission",
        "cross-repository",
        "global program completion",
    ]:
        if phrase not in blocked:
            raise RuntimeError(f"Round 03 rebaseline blocked scope missing phrase: {phrase}")
    boundary = document.get("dataAndAuthorityBoundary", {})
    expected_boundary_keys = {
        "publicExternalData",
        "localInputs",
        "executionBoundary",
        "accountBoundary",
        "writeBoundary",
        "releaseBoundary",
    }
    if set(boundary) != expected_boundary_keys:
        raise RuntimeError("Round 03 rebaseline data and authority boundary drifted.")
    semantics = document.get("executionSemantics", {})
    if semantics.get("model") != "dependency-graph-with-bounded-parallel-research":
        raise RuntimeError("Round 03 rebaseline execution model drifted.")
    expected_core_path = [
        "bind-demand-coordinates-and-evidence-limits",
        "measure-native-official-runtime-and-installed-baselines",
        "run-bounded-public-metadata-discovery",
        "cluster-deduplicate-and-select-representatives",
        "pin-sources-and-deep-review-minimum-representatives",
        "compare-native-single-composed-and-non-skill-alternatives",
        "classify-covered-supported-gap-or-unproven-gap",
        "select-gap-fill-carrier-only-after-residual-gap-is-supported",
        "produce-result-package-and-next-round-candidates",
    ]
    if semantics.get("corePath") != expected_core_path:
        raise RuntimeError("Round 03 rebaseline core path drifted.")
    if len(semantics.get("safeParallelism", [])) != 3 or not semantics.get("rerouteTriggers"):
        raise RuntimeError("Round 03 rebaseline parallelism or reroute triggers are incomplete.")
    stop_rule = str(semantics.get("stopRule", "")).lower()
    for phrase in ["additional candidates", "materially change", "remaining uncertainty", "recheck triggers"]:
        if phrase not in stop_rule:
            raise RuntimeError(f"Round 03 rebaseline stop rule missing phrase: {phrase}")

    carrier = document.get("gapFillCarrierDecision", {})
    if "residual gap is supported" not in str(carrier.get("entryCondition", "")).lower():
        raise RuntimeError("Round 03 Hook consideration must occur only after residual-gap proof.")
    carrier_options = " ".join(str(item) for item in carrier.get("options", [])).lower()
    for phrase in [
        "skill without a hook",
        "skill with a consumer-owned hook",
        "hook or another non-skill harness",
        "project-owned hard standard",
        "human or domain-authority",
        "gap remains unproven",
    ]:
        if phrase not in carrier_options:
            raise RuntimeError(f"Round 03 gap-fill carrier options missing phrase: {phrase}")
    if len(carrier.get("hookSuitabilitySignals", [])) != 4:
        raise RuntimeError("Round 03 Hook suitability signals are incomplete.")
    if len(carrier.get("hookRejectionSignals", [])) != 5:
        raise RuntimeError("Round 03 Hook rejection signals are incomplete.")
    authority_rule = str(carrier.get("authorityRule", "")).lower()
    for phrase in ["optional", "never evidence", "approval", "permission"]:
        if phrase not in authority_rule:
            raise RuntimeError(f"Round 03 Hook authority rule missing phrase: {phrase}")
    if not str(carrier.get("default", "")).lower().startswith("no hook"):
        raise RuntimeError("Round 03 Hook decision must default to no Hook without proof.")

    initiatives = {
        item.get("id"): item
        for item in program_doc.get("currentInitiatives", [])
        if isinstance(item, dict)
    }
    survey = initiatives.get("initiative.capability-survey-gap-proof", {})
    if document.get("requiredResultPackage") != survey.get("resultPackage"):
        raise RuntimeError("Round 03 rebaseline result package must match the capability-survey contract.")
    expected_acceptance = {
        "acceptance.demand-coordinate-contract",
        "acceptance.native-runtime-baseline",
        "acceptance.discovery-clustering-stop-rule",
        "acceptance.alternative-comparison",
        "acceptance.residual-gap-proof",
        "acceptance.capability-survey-result-package",
        "acceptance.cross-agent-claim-limits",
        "acceptance.sequence-integrity",
    }
    if set(document.get("acceptanceIds", [])) != expected_acceptance:
        raise RuntimeError("Round 03 rebaseline acceptance mapping drifted.")
    if len(document.get("verificationSurface", [])) != 6:
        raise RuntimeError("Round 03 rebaseline verification surface is incomplete.")
    expected_activation = {
        "ownerReviewRequired": False,
        "executionActivated": True,
        "externalDiscoveryAuthorizedByThisRecord": False,
        "candidateExecutionAuthorized": False,
        "runtimeMutationAuthorized": False,
        "crossRepositoryWriteAuthorized": False,
        "remotePushAuthorized": False,
    }
    if document.get("activationGate") != expected_activation:
        raise RuntimeError("Round 03 rebaseline activation gate drifted.")
    acceptance_event_path = "registry/round03-capability-survey-rebaseline-acceptance-event-2026-07-15.json"
    if document.get("acceptanceEvent") != acceptance_event_path:
        raise RuntimeError("Round 03 rebaseline acceptance event link drifted.")

    round03 = next(
        item
        for item in rounds_doc.get("rounds", [])
        if isinstance(item, dict) and item.get("id") == document.get("roundId")
    )
    if round03.get("status") != "active" or round03.get("lifecycle", {}).get("execute") != "active":
        raise RuntimeError("Round 03 registry must be active after owner acceptance.")
    if "registry/round03-capability-survey-rebaseline.json" not in round03.get("evidence", []):
        raise RuntimeError("Round 03 registry must link the rebaseline review.")
    initiative = initiatives.get("initiative.round03-capability-survey-rebaseline", {})
    if program_doc.get("currentInitiativeId") != "initiative.capability-survey-gap-proof":
        raise RuntimeError("The capability survey must be current after rebaseline acceptance.")
    if initiative.get("status") != "accepted":
        raise RuntimeError("Round 03 rebaseline initiative must record acceptance.")
    if initiative.get("decisionPreparation") != "registry/round03-capability-survey-rebaseline.json":
        raise RuntimeError("Round 03 rebaseline initiative must link its decision preparation.")
    if initiative.get("decisionEvidence") != acceptance_event_path:
        raise RuntimeError("Round 03 rebaseline initiative must link its acceptance event.")
    application = lifecycle_doc.get("currentApplication", {})
    if application.get("phaseState") != "execute_active" or application.get("stageCloseout") != "not_ready":
        raise RuntimeError("Round 03 lifecycle must be active and not ready for closeout.")
    if application.get("nextRequiredEvidence") != [
        "demand-level alternative comparison before any residual-gap, repository-authoring, or Hook decision"
    ]:
        raise RuntimeError("Round 03 lifecycle next evidence must preserve alternative-comparison order.")

    criteria = {
        item.get("id"): item
        for item in acceptance_doc.get("acceptanceCriteria", [])
        if isinstance(item, dict)
    }
    criterion = criteria.get("acceptance.round03-rebaseline", {})
    if criterion.get("assessment") != "verified":
        raise RuntimeError("Round 03 rebaseline acceptance must be verified after owner review.")
    if not {"evidence.round03-rebaseline", "evidence.round03-rebaseline-acceptance"} <= set(criterion.get("evidenceIds", [])):
        raise RuntimeError("Round 03 rebaseline acceptance evidence is missing.")

    expected_docs = {
        "docs/round03-capability-survey-rebaseline.md": [
            "Accepted",
            "Round 03 is active",
            "residual-gap proof",
            "No candidate code",
            "Hook is considered only after",
            "never an authority",
            "Owner review is satisfied",
        ],
        "docs/round03-capability-survey-rebaseline.zh-CN.md": [
            "已接受",
            "Round 03 现已",
            "残余缺口证明",
            "不执行候选代码",
            "Hook 只在重要残余缺口已经成立后",
            "不是权威源",
            "所有者审查已经满足",
        ],
    }
    if set(document.get("evidenceDocs", [])) != set(expected_docs):
        raise RuntimeError("Round 03 rebaseline evidence docs drifted.")
    for path, phrases in expected_docs.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                raise RuntimeError(f"Round 03 rebaseline doc missing phrase in {path}: {phrase}")


def validate_round03_capability_survey_rebaseline_acceptance_event(
    document: dict[str, object],
    rebaseline_doc: dict[str, object],
    demand_contract: dict[str, object],
    rounds_doc: dict[str, object],
    program_doc: dict[str, object],
    lifecycle_doc: dict[str, object],
    acceptance_doc: dict[str, object],
) -> None:
    expected_scalars = {
        "schema": 1,
        "id": "round03-capability-survey-rebaseline-acceptance-event-2026-07-15",
        "date": "2026-07-15",
        "status": "recorded",
        "decision": "accepted-and-activate-bounded-read-only-capability-survey",
        "authoritySource": "owner-selected-option-1",
        "ownerDecision": "1",
        "acceptedRebaseline": "registry/round03-capability-survey-rebaseline.json",
        "acceptedDemandInputContract": "registry/round03-demand-coordinate-source-contract.json",
        "acceptedCommit": "43cde9488182a76af8edc3a54d442e9020c4d901",
        "nextGate": "verified demand records and native/runtime baseline before public candidate metadata discovery",
    }
    for key, expected in expected_scalars.items():
        if document.get(key) != expected:
            raise RuntimeError(f"Round 03 rebaseline acceptance event {key} drifted.")

    expected_authorization = {
        "round03ActivationAuthorized": True,
        "demandRecordExtractionAuthorized": True,
        "nativeOfficialRuntimeBaselineAuthorized": True,
        "publicReadOnlyMetadataDiscoveryAuthorized": True,
        "sourcePinnedRepresentativeReviewAuthorized": True,
        "currentRepositoryEvidenceWritesAuthorized": True,
        "candidateExecutionAuthorized": False,
        "installationOrAccountConnectionAuthorized": False,
        "runtimeMutationAuthorized": False,
        "crossRepositoryWriteAuthorized": False,
        "skillAdmissionOrReleaseMutationAuthorized": False,
        "standardPromotionAuthorized": False,
        "remotePushAuthorized": False,
        "globalProgramCompletionClaimed": False,
    }
    if document.get("authorization") != expected_authorization:
        raise RuntimeError("Round 03 rebaseline acceptance authorization drifted.")
    if len(document.get("authorizedData", [])) != 4:
        raise RuntimeError("Round 03 accepted data boundary is incomplete.")
    sequence = document.get("authorizedSequence", [])
    if len(sequence) != 7:
        raise RuntimeError("Round 03 accepted sequence is incomplete.")
    sequence_text = " ".join(str(item) for item in sequence).lower()
    ordered_phrases = [
        "demand records",
        "native, official, runtime",
        "public candidate metadata",
        "cluster",
        "pin sources",
        "compare native",
        "residual gaps",
    ]
    positions = [sequence_text.find(phrase) for phrase in ordered_phrases]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        raise RuntimeError("Round 03 accepted sequence order drifted.")
    blocked = " ".join(str(item) for item in document.get("blockedActions", [])).lower()
    for phrase in [
        "bulk clone",
        "executing candidate code",
        "oauth",
        "live runtime",
        "another repository",
        "enabling a hook",
        "remote push",
    ]:
        if phrase not in blocked:
            raise RuntimeError(f"Round 03 acceptance blocked action missing phrase: {phrase}")

    expected_state = {
        "roundId": "round-03-adaptation-and-curated-admission",
        "roundStatus": "active",
        "phaseState": "execute_active",
        "currentInitiativeId": "initiative.capability-survey-gap-proof",
        "nextRequiredEvidence": "governed Round 03 demand records and dated native/runtime baseline before public candidate metadata discovery",
    }
    if document.get("effectiveState") != expected_state:
        raise RuntimeError("Round 03 acceptance effective state drifted.")
    if len(document.get("verification", [])) != 5 or len(document.get("residualLimits", [])) != 4:
        raise RuntimeError("Round 03 acceptance verification or residual limits are incomplete.")

    event_path = "registry/round03-capability-survey-rebaseline-acceptance-event-2026-07-15.json"
    if rebaseline_doc.get("status") != "accepted" or rebaseline_doc.get("acceptanceEvent") != event_path:
        raise RuntimeError("Round 03 accepted rebaseline state drifted.")
    if demand_contract.get("activationEvidence") != event_path:
        raise RuntimeError("Round 03 accepted demand-contract state drifted.")
    readiness = demand_contract.get("readiness", {})
    if (
        readiness.get("round03ExecutionActivated") is not True
        or readiness.get("externalDiscoveryAuthorized") is not True
        or readiness.get("demandRecordExtractionComplete") is not False
    ):
        raise RuntimeError("Round 03 demand-contract readiness must preserve the active pre-discovery gate.")

    round03 = next(
        item
        for item in rounds_doc.get("rounds", [])
        if isinstance(item, dict) and item.get("id") == expected_state["roundId"]
    )
    if round03.get("status") != "active" or event_path not in round03.get("evidence", []):
        raise RuntimeError("Round 03 registry must link the owner activation event.")
    if round03.get("lifecycle") != {
        "plan": "accepted",
        "execute": "active",
        "acceptance": "pending",
        "stageCloseout": "pending",
    }:
        raise RuntimeError("Round 03 active lifecycle drifted.")

    initiatives = {
        item.get("id"): item
        for item in program_doc.get("currentInitiatives", [])
        if isinstance(item, dict)
    }
    if program_doc.get("currentInitiativeId") != expected_state["currentInitiativeId"]:
        raise RuntimeError("Round 03 acceptance program initiative drifted.")
    if initiatives.get("initiative.capability-survey-gap-proof", {}).get("status") != "active":
        raise RuntimeError("Round 03 capability survey must be active.")
    rebaseline = initiatives.get("initiative.round03-capability-survey-rebaseline", {})
    if rebaseline.get("status") != "accepted" or rebaseline.get("decisionEvidence") != event_path:
        raise RuntimeError("Round 03 rebaseline initiative acceptance drifted.")

    application = lifecycle_doc.get("currentApplication", {})
    if application.get("phaseState") != expected_state["phaseState"] or event_path not in application.get("evidence", []):
        raise RuntimeError("Round 03 lifecycle activation evidence drifted.")
    if application.get("nextRequiredEvidence") != [
        "demand-level alternative comparison before any residual-gap, repository-authoring, or Hook decision"
    ]:
        raise RuntimeError("Round 03 lifecycle post-review alternative gate drifted.")

    criteria = {
        item.get("id"): item
        for item in acceptance_doc.get("acceptanceCriteria", [])
        if isinstance(item, dict)
    }
    criterion = criteria.get("acceptance.round03-rebaseline", {})
    if criterion.get("assessment") != "verified" or "evidence.round03-rebaseline-acceptance" not in criterion.get("evidenceIds", []):
        raise RuntimeError("Round 03 rebaseline owner acceptance mapping drifted.")
    evidence = {
        item.get("id"): item
        for item in acceptance_doc.get("evidence", [])
        if isinstance(item, dict)
    }
    evidence_record = evidence.get("evidence.round03-rebaseline-acceptance", {})
    if evidence_record.get("path") != event_path or evidence_record.get("kind") != "owner-activation-decision":
        raise RuntimeError("Round 03 rebaseline acceptance evidence record drifted.")

    expected_docs = {
        "docs/round03-capability-survey-rebaseline-acceptance.md": [
            "owner selected option 1",
            "Round 03 is active",
            "does not authorize bulk cloning",
            "default remains no Hook",
            "before public candidate metadata discovery",
        ],
        "docs/round03-capability-survey-rebaseline-acceptance.zh-CN.md": [
            "所有者选择了选项 1",
            "现已针对有边界的只读能力调研激活",
            "不授权批量克隆",
            "默认不使用",
            "公开候选元数据发现开始之前",
        ],
    }
    if set(document.get("evidenceDocs", [])) != set(expected_docs):
        raise RuntimeError("Round 03 rebaseline acceptance docs drifted.")
    for path, phrases in expected_docs.items():
        text = " ".join((ROOT / path).read_text(encoding="utf-8").split())
        for phrase in phrases:
            if phrase not in text:
                raise RuntimeError(f"Round 03 rebaseline acceptance doc missing phrase in {path}: {phrase}")


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
