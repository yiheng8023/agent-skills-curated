from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent


class CiContractTests(unittest.TestCase):
    def test_governance_contract_tests_run_before_repository_verification(self) -> None:
        workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")

        tests = workflow.index("python -m unittest discover -s tests -v")
        verify = workflow.index("python scripts/verify.py")

        self.assertLess(tests, verify)

    def test_generated_and_routing_gates_run_before_repository_verification(self) -> None:
        workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")

        manifest = workflow.index("python scripts/build_release_manifest.py --check")
        topology = workflow.index("python scripts/build_topology.py --check")
        routing = workflow.index("python scripts/simulate_routing.py --all")
        verify = workflow.index("python scripts/verify.py")

        self.assertLess(manifest, verify)
        self.assertLess(topology, verify)
        self.assertLess(routing, verify)


if __name__ == "__main__":
    unittest.main()
