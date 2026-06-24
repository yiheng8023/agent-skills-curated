from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class DocumentationContractTests(unittest.TestCase):
    def test_readmes_use_matching_language_switches_and_role_structure(self) -> None:
        english = read("README.md")
        chinese = read("README.zh-CN.md")

        self.assertIn("English | [简体中文](README.zh-CN.md)", english)
        self.assertIn("[English](README.md) | 简体中文", chinese)

        for heading in (
            "## Repository Role",
            "## What This Repository Provides",
            "## What This Repository Does Not Own",
            "## Relationship To The Paired Repository",
            "## Layout",
            "## Verification",
            "## Update Rules",
            "## Safety Boundaries",
        ):
            with self.subTest(readme="English", heading=heading):
                self.assertIn(heading, english)

        for heading in (
            "## 仓库职责",
            "## 本仓库提供什么",
            "## 本仓库不负责什么",
            "## 与配对仓库的关系",
            "## 目录结构",
            "## 验证方式",
            "## 更新规则",
            "## 安全边界",
        ):
            with self.subTest(readme="Chinese", heading=heading):
                self.assertIn(heading, chinese)

    def test_governance_documents_define_three_noninterchangeable_layers(self) -> None:
        corpus = "\n".join(
            (
                read("AGENTS.md"),
                read("README.md"),
                read("docs/architecture.md"),
                read("policies/intake.md"),
                read("docs/official-external-capability-baselines.md"),
                read("docs/anthropic-official-skills-coverage.md"),
                read("docs/starred-capability-source-discovery.md"),
            )
        )

        for phrase in (
            "official, runtime-owned, or built-in",
            "external capability metadata",
            "must not be vendored",
            "third-party candidate",
            "must not enter an execution path",
            "curated approved",
            "status=approved",
            "approved release inventory",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, corpus)

    def test_starred_sources_are_discovery_hints_not_approval(self) -> None:
        discovery = read("docs/starred-capability-source-discovery.md")
        corpus = "\n".join((read("README.md"), read("policies/intake.md")))

        for phrase in (
            "Discovery surface",
            "not approval",
            "not installation",
            "not managed inventory",
            "third-party skill source",
            "official external baseline",
            "index / awesome list",
            "risk / exclusion",
            "normal intake process",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, discovery)

        for phrase in (
            "Stars are only discovery hints",
            "do not prove license safety",
            "must not enter `skills/`",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, corpus)

    def test_official_external_baselines_are_not_managed_inventory(self) -> None:
        baseline_policy = read("docs/official-external-capability-baselines.md")
        coverage = read("docs/anthropic-official-skills-coverage.md")
        corpus = "\n".join(
            (
                read("README.md"),
                read("AGENTS.md"),
                read("docs/architecture.md"),
                read("policies/intake.md"),
            )
        )

        for phrase in (
            "Official External Capability Baselines",
            "dated external baseline",
            "not managed inventory",
            "not proof of live availability",
            "coverage comparison",
            "gap analysis",
            "routing calibration",
            "adapt-candidate",
            "approved release",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, baseline_policy)

        for phrase in (
            "Anthropic official Skills",
            "first recorded instance",
            "source-available",
            "all-rights-reserved",
            "covered",
            "reference",
            "adapt-candidate",
            "skip",
            "release-manifest.json",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, coverage)

        for phrase in (
            "official external capability baselines",
            "does not approve import",
            "license/provenance",
            "neutralization",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, corpus)

    def test_pairing_and_router_boundaries_are_explicit(self) -> None:
        corpus = "\n".join(
            (read("AGENTS.md"), read("README.md"), read("docs/architecture.md"))
        )

        for phrase in (
            "capability decision router",
            "native reasoning",
            "recipe or DAG",
            "no skill needed",
            "human confirmation",
            "does not install",
            "does not write to `codex-user-config`",
            "does not write to a live Agent environment",
            "derived projections",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, corpus)

    def test_runtime_resolution_is_documented_as_a_structural_contract(self) -> None:
        for path in ("README.md", "README.zh-CN.md"):
            text = read(path)
            with self.subTest(path=path):
                self.assertIn("visible-capability-inventory", text)
                self.assertIn("runtimeResolution", text)

    def test_governance_roadmap_matches_current_contract_state(self) -> None:
        design = read("docs/superpowers/specs/2026-06-22-governance-contracts-design.md")

        for phrase in (
            "Current Implementation State",
            "Batch A is complete",
            "`registry/skills.json` remains schema 1",
            "manifest v2 has not been published",
            "The next bounded task is not a manifest upgrade",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, design)

        self.assertNotIn(
            "Batch A is the next implementation target after user review",
            design,
        )

    def test_skill_v2_contract_decision_avoids_second_truth_source(self) -> None:
        decision = read("docs/decisions/2026-06-23-skill-v2-contract-decision.md")

        for phrase in (
            "Decision: do not promote Skill v2 metadata into a new authoritative skills registry yet",
            "`registry/skills.json` remains the schema-1 approved release inventory",
            "`registry/routing.json` remains the authority for Skill routing metadata",
            "`registry/capabilities.json` remains the authority for abstract lifecycle coverage",
            "No second Skill truth source",
            "No manifest v2 publication",
            "Future promotion gate",
            "5-8 representative Skills",
            "legacy-pending",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, decision)


if __name__ == "__main__":
    unittest.main()
