import hashlib
import json
from pathlib import Path
import unittest

from scripts.build_topology import render


ROOT = Path(__file__).resolve().parent.parent
INPUTS = (
    "registry/capabilities.json",
    "registry/routing.json",
    "registry/relations.json",
    "registry/conflicts.json",
    "registry/recipes.json",
)


class RoutingProjectionTests(unittest.TestCase):
    def test_projection_contains_only_governed_abstract_routing_inputs(self) -> None:
        projection = json.loads(render()["routing-index.json"])
        self.assertEqual(projection["schema"], 1)
        self.assertEqual(
            set(projection),
            {
                "schema",
                "authoritativeInputDigests",
                "capabilities",
                "routes",
                "relations",
                "conflicts",
                "recipes",
            },
        )
        self.assertEqual(
            {route["skill"] for route in projection["routes"]},
            {
                item["id"]
                for item in json.loads((ROOT / "registry/skills.json").read_text(encoding="utf-8"))["skills"]
                if item["status"] == "approved"
            },
        )

    def test_projection_digests_bind_every_authoritative_input(self) -> None:
        projection = json.loads(render()["routing-index.json"])
        expected = {
            path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            for path in INPUTS
        }
        self.assertEqual(projection["authoritativeInputDigests"], expected)

    def test_checked_in_projection_is_deterministic(self) -> None:
        self.assertEqual(
            (ROOT / "generated/routing-index.json").read_text(encoding="utf-8"),
            render()["routing-index.json"],
        )


if __name__ == "__main__":
    unittest.main()
