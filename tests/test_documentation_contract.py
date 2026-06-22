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


if __name__ == "__main__":
    unittest.main()
