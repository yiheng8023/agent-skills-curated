#!/usr/bin/env python3
"""Verify inventory, provenance, overlap decisions, graph, and portability."""

from __future__ import annotations

import json
import re
import subprocess
import sys
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
    "AGENTS.md", "README.md", "README.zh-CN.md", "THIRD_PARTY_NOTICES.md",
    "sources/lock.json", "sources/addyosmani-agent-skills/selection.json",
    "sources/addyosmani-agent-skills/LICENSE",
    "sources/addyosmani-agent-skills/files.sha256", "registry/skills.json",
    "registry/capabilities.json", "registry/relations.json",
    "registry/conflicts.json", "registry/recipes.json",
    "registry/radar-feedback.json",
    "registry/mvp-candidate-batches.json",
    "registry/mvp-candidate-reviews.json",
    "registry/mvp-transition-gates.json",
    "registry/mvp-adaptation-review-checklist.json",
    "registry/mvp-approval-requests.json",
    "registry/mvp02-preflight-readiness.json",
    "registry/mvp02-post-approval-execution-plan.json",
    "registry/mvp02-approval-events.json",
    "registry/mvp02-adapted-drafts.json",
    "registry/admissions.json", "registry/routing.json", "registry/scenarios.json",
    "policies/intake.md", "policies/portability.md", "policies/security.md",
    "policies/overlap-resolution.md", "policies/lifecycle.md",
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
    "docs/mvp-candidate-batch-2026-06-27.md",
    "docs/mvp-candidate-review-2026-06-27.md",
    "docs/mvp02-adaptation-transition-gate.md",
    "docs/mvp02-adaptation-review-template.md",
    "docs/mvp02-adaptation-approval-request.md",
    "docs/mvp02-preflight-readiness.md",
    "docs/mvp02-post-approval-execution-plan.md",
    "docs/mvp02-adapted-draft-review.md",
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
    selection_document = "sources/addyosmani-agent-skills/selection.json"
    selection_doc = load(selection_document)
    manifest = load("release-manifest.json")
    validate_skills_document(skills_doc, "registry/skills.json")
    validate_capabilities_document(capabilities_doc, "registry/capabilities.json")
    validate_relations_document(relations_doc, "registry/relations.json")
    validate_conflicts_document(conflicts_doc, "registry/conflicts.json")
    validate_recipes_document(recipes_doc, "registry/recipes.json")
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
    generated_text = (ROOT / "generated/routing-index.json").read_text(encoding="utf-8")
    allowed_dispositions = {"merge", "recipe-only", "adapter-only", "reject", "approved-payload-candidate"}
    for candidate_id, candidate in draft_candidates.items():
        if candidate_id in approved_directories:
            raise RuntimeError(f"MVP-02 adapted draft candidate unexpectedly approved: {candidate_id}")
        if f"skills/{candidate_id}/" in manifest_paths:
            raise RuntimeError(f"MVP-02 adapted draft candidate appears in release manifest: {candidate_id}")
        if candidate_id in routing_text or candidate_id in generated_text:
            raise RuntimeError(f"MVP-02 adapted draft candidate appears in executable routing surfaces: {candidate_id}")
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
