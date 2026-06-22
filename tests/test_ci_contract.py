from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent


class CiContractTests(unittest.TestCase):
    def test_governance_contract_tests_run_before_repository_verification(self) -> None:
        workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")

        tests = workflow.index("python -m unittest discover -s tests -v")
        verify = workflow.index("python scripts/verify.py")

        self.assertLess(tests, verify)


if __name__ == "__main__":
    unittest.main()
