from copy import deepcopy
import json
from pathlib import Path
import re
import unittest

from scripts import contracts
from scripts.contracts import (
    ContractError,
    validate_admissions_document,
    validate_capabilities_document,
    validate_conflicts_document,
    validate_recipes_document,
    validate_relations_document,
    validate_release_manifest_document,
    validate_routing_document,
    validate_scenarios_document,
    validate_selection_document,
    validate_skills_document,
    validate_sources_lock_document,
)
from tests.test_shape_contracts import ADMISSIONS, CAPABILITIES_V2, ROUTING, SCENARIOS_DOCUMENT


ROOT = Path(__file__).resolve().parent.parent
CASES = (
    ("skills", "registry/skills.json", validate_skills_document),
    ("capabilities", "registry/capabilities.json", validate_capabilities_document),
    ("relations", "registry/relations.json", validate_relations_document),
    ("conflicts", "registry/conflicts.json", validate_conflicts_document),
    ("recipes", "registry/recipes.json", validate_recipes_document),
    ("sources-lock", "sources/lock.json", validate_sources_lock_document),
    (
        "selection",
        "sources/addyosmani-agent-skills/selection.json",
        validate_selection_document,
    ),
    ("release-manifest", "release-manifest.json", validate_release_manifest_document),
)
ADDITIONAL_CASES = (
    ("admissions", 1, ADMISSIONS, validate_admissions_document),
    ("routing", 1, ROUTING, validate_routing_document),
    ("scenarios", 1, SCENARIOS_DOCUMENT, validate_scenarios_document),
    ("capabilities-v2", 2, CAPABILITIES_V2, validate_capabilities_document),
)
PATTERN_CANDIDATES = (
    "skill.curated.alpha",
    "skill.curated.Alpha",
    "capability.alpha",
    "conflict.alpha",
    "recipe.alpha",
    "scenario.alpha",
    "alpha",
    "a-1",
    "Alpha",
    "../bad",
    "skills/a/SKILL.md",
    "skills/a/reference.md",
    "skills\\a\\SKILL.md",
    "0" * 64,
    "f" * 64,
    "g" * 64,
    "0" * 63,
)


def load(path: str) -> dict[str, object]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def join(pointer: str, part: str | int) -> str:
    token = str(part).replace("~", "~0").replace("/", "~1")
    return f"{pointer}/{token}" if pointer else f"/{token}"


def resolve(document: object, pointer: str) -> object:
    value = document
    for raw in pointer.split("/")[1:]:
        token = raw.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]  # type: ignore[index]
    return value


def assign(document: object, pointer: str, value: object) -> None:
    parent_pointer, _, raw = pointer.rpartition("/")
    parent = resolve(document, parent_pointer)
    token = raw.replace("~1", "/").replace("~0", "~")
    if isinstance(parent, list):
        parent[int(token)] = value
    else:
        parent[token] = value  # type: ignore[index]


def property_facets(
    schema: dict[str, object], schema_pointer: str = "", document_pointer: str = ""
) -> list[tuple[str, str, dict[str, object]]]:
    """Inventory property/item facets; this deliberately does not validate schemas."""

    found: list[tuple[str, str, dict[str, object]]] = []
    properties = schema.get("properties", {})
    if isinstance(properties, dict):
        for name, raw in properties.items():
            if not isinstance(raw, dict):
                continue
            child_schema_pointer = join(join(schema_pointer, "properties"), name)
            child_document_pointer = join(document_pointer, name)
            found.append((child_schema_pointer, child_document_pointer, raw))
            found.extend(
                property_facets(raw, child_schema_pointer, child_document_pointer)
            )
    items = schema.get("items")
    if isinstance(items, dict):
        child_schema_pointer = join(schema_pointer, "items")
        child_document_pointer = join(document_pointer, 0)
        found.append((child_schema_pointer, child_document_pointer, items))
        found.extend(property_facets(items, child_schema_pointer, child_document_pointer))
    return found


class SchemaParityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cases = []
        for name, document_path, validator in CASES:
            self.cases.append(
                (
                    name,
                    load(f"schemas/v1/{name}.schema.json"),
                    load(document_path),
                    validator,
                )
            )
        for name, version, document, validator in ADDITIONAL_CASES:
            schema_name = "capabilities" if name == "capabilities-v2" else name
            self.cases.append((name, load(f"schemas/v{version}/{schema_name}.schema.json"), deepcopy(document), validator))

    def accepts(self, validator: object, document: dict[str, object]) -> bool:
        try:
            validator(document, "fixture.json")  # type: ignore[operator]
        except ContractError:
            return False
        return True

    def assert_rejected_at(
        self, validator: object, document: dict[str, object], pointer: str
    ) -> None:
        with self.assertRaises(ContractError) as raised:
            validator(document, "fixture.json")  # type: ignore[operator]
        self.assertEqual(raised.exception.pointer, pointer)

    def test_real_documents_are_valid_validator_fixtures(self) -> None:
        for name, _, document, validator in self.cases:
            with self.subTest(name=name):
                validator(document, "fixture.json")  # type: ignore[operator]

    def test_every_schema_required_field_is_required_by_validator(self) -> None:
        for name, schema, document, validator in self.cases:
            objects = [("", "", schema)] + [
                item for item in property_facets(schema) if "required" in item[2]
            ]
            for schema_pointer, document_pointer, node in objects:
                required = set(node.get("required", []))
                for field in node.get("properties", {}):
                    with self.subTest(
                        name=name,
                        schema=schema_pointer,
                        field=field,
                        required=field in required,
                    ):
                        changed = deepcopy(document)
                        target = resolve(changed, document_pointer)
                        self.assertIsInstance(target, dict)
                        if field not in target:  # type: ignore[operator]
                            self.assertNotIn(field, required)
                            self.assertTrue(self.accepts(validator, changed))
                            continue
                        del target[field]  # type: ignore[index]
                        if field in required:
                            self.assert_rejected_at(
                                validator, changed, join(document_pointer, field)
                            )
                        else:
                            if name == "capabilities-v2" and field == "curatedOwners":
                                target["coverageState"] = "native-sufficient"  # type: ignore[index]
                            self.assertTrue(self.accepts(validator, changed))

    def test_every_closed_object_rejects_unknown_fields(self) -> None:
        for name, schema, document, validator in self.cases:
            objects = [("", "", schema)] + [
                item
                for item in property_facets(schema)
                if item[2].get("additionalProperties") is False
            ]
            for schema_pointer, document_pointer, _ in objects:
                with self.subTest(name=name, schema=schema_pointer):
                    changed = deepcopy(document)
                    target = resolve(changed, document_pointer)
                    self.assertIsInstance(target, dict)
                    target["unknownFacet"] = True  # type: ignore[index]
                    self.assert_rejected_at(
                        validator, changed, join(document_pointer, "unknownFacet")
                    )

    def test_every_enum_value_and_an_invalid_value_match_validator(self) -> None:
        for name, schema, document, validator in self.cases:
            enum_fields = [item for item in property_facets(schema) if "enum" in item[2]]
            decisions = schema.get("properties", {}).get("decisions", {})  # type: ignore[union-attr]
            if isinstance(decisions, dict) and isinstance(
                decisions.get("additionalProperties"), dict
            ):
                enum_fields.append(
                    (
                        "/properties/decisions/additionalProperties",
                        join("/decisions", next(iter(document["decisions"]))),  # type: ignore[arg-type]
                        decisions["additionalProperties"],
                    )
                )
            for schema_pointer, document_pointer, node in enum_fields:
                allowed = node["enum"]
                for value in allowed:  # type: ignore[union-attr]
                    with self.subTest(name=name, schema=schema_pointer, value=value):
                        changed = deepcopy(document)
                        assign(changed, document_pointer, value)
                        if name == "capabilities-v2" and document_pointer.endswith("/coverageState"):
                            capability = changed["capabilities"][0]
                            if value == "curated":
                                capability["curatedOwners"] = ["skill.curated.alpha"]
                            else:
                                capability.pop("curatedOwners", None)
                        if (
                            name == "sources-lock"
                            and document_pointer == "/sources/0/kind"
                            and value == "local"
                        ):
                            source = changed["sources"][0]
                            for field in ("url", "revision", "license"):
                                source.pop(field, None)
                            source["provenanceStatus"] = "incomplete"
                            source["redistribution"] = "private-only"
                        self.assertTrue(self.accepts(validator, changed))
                invalid = "__not_in_schema_enum__"
                self.assertNotIn(invalid, allowed)
                changed = deepcopy(document)
                assign(changed, document_pointer, invalid)
                with self.subTest(name=name, schema=schema_pointer, value=invalid):
                    self.assert_rejected_at(validator, changed, document_pointer)

    def test_every_pattern_matches_validator_on_boundary_candidates(self) -> None:
        for name, schema, document, validator in self.cases:
            for schema_pointer, document_pointer, node in property_facets(schema):
                if "pattern" not in node:
                    continue
                expression = re.compile(node["pattern"])
                outcomes = set()
                for candidate in PATTERN_CANDIDATES:
                    schema_accepts = expression.fullmatch(candidate) is not None
                    changed = deepcopy(document)
                    assign(changed, document_pointer, candidate)
                    validator_accepts = self.accepts(validator, changed)
                    outcomes.add(schema_accepts)
                    with self.subTest(
                        name=name, schema=schema_pointer, candidate=candidate
                    ):
                        self.assertEqual(schema_accepts, validator_accepts)
                self.assertEqual(outcomes, {False, True})

    def test_schema_patterns_are_the_validator_pattern_sources(self) -> None:
        cases = (
            ("skills", "/properties/skills/items/properties/id", contracts._SKILL_ID),
            (
                "skills",
                "/properties/skills/items/properties/directory",
                contracts._DIRECTORY,
            ),
            (
                "capabilities",
                "/properties/capabilities/items/properties/id",
                contracts._CAPABILITY_ID,
            ),
            ("conflicts", "/properties/groups/items/properties/id", contracts._CONFLICT_ID),
            ("recipes", "/properties/recipes/items/properties/id", contracts._RECIPE_ID),
            (
                "release-manifest",
                "/properties/files/items/properties/path",
                contracts._MANIFEST_PATH,
            ),
            ("capabilities-v2", "/properties/capabilities/items/properties/id", contracts._CAPABILITY_ID),
            ("admissions", "/properties/admissions/items/properties/skill", contracts._SKILL_ID),
            ("routing", "/properties/routes/items/properties/skill", contracts._SKILL_ID),
            ("scenarios", "/properties/scenarios/items/properties/id", contracts._SCENARIO_ID),
            (
                "release-manifest",
                "/properties/files/items/properties/sha256",
                contracts._DIGEST,
            ),
        )
        schemas = {name: schema for name, schema, _, _ in self.cases}
        for name, pointer, validator_pattern in cases:
            with self.subTest(name=name, pointer=pointer):
                validator_source = validator_pattern.pattern
                if not validator_source.startswith("^"):
                    validator_source = "^" + validator_source
                if not validator_source.endswith("$"):
                    validator_source += "$"
                self.assertEqual(
                    resolve(schemas[name], pointer)["pattern"],  # type: ignore[index]
                    validator_source,
                )

    def test_schema_enums_are_the_validator_enum_sources(self) -> None:
        schemas = {name: schema for name, schema, _, _ in self.cases}
        cases = (
            (
                "skills",
                "/properties/skills/items/properties/status/enum",
                contracts._SKILL_STATUSES,
            ),
            (
                "selection",
                "/properties/decisions/additionalProperties/enum",
                contracts._SELECTION_DISPOSITIONS,
            ),
            (
                "sources-lock",
                "/properties/sources/items/properties/kind/enum",
                contracts._SOURCE_KINDS,
            ),
            (
                "sources-lock",
                "/properties/sources/items/properties/provenanceStatus/enum",
                contracts._PROVENANCE_STATUSES,
            ),
            (
                "sources-lock",
                "/properties/sources/items/properties/redistribution/enum",
                contracts._REDISTRIBUTION_STATUSES,
            ),
            ("admissions", "/properties/admissions/items/properties/disposition/enum", contracts._ADMISSION_DISPOSITIONS),
            ("routing", "/properties/routes/items/properties/riskLevel/enum", contracts._RISK_LEVELS),
            ("capabilities-v2", "/properties/capabilities/items/properties/coverageState/enum", contracts._COVERAGE_STATES),
        )
        for name, pointer, validator_values in cases:
            with self.subTest(name=name, pointer=pointer):
                self.assertEqual(set(resolve(schemas[name], pointer)), validator_values)

    def test_local_source_policy_is_declared_in_schema(self) -> None:
        schema = load("schemas/v1/sources-lock.schema.json")
        source = resolve(schema, "/properties/sources/items")
        self.assertEqual(
            source["if"],
            {"properties": {"kind": {"const": "local"}}, "required": ["kind"]},
        )
        self.assertEqual(
            source["then"],
            {
                "properties": {
                    "provenanceStatus": {"const": "incomplete"},
                    "redistribution": {"const": "private-only"},
                },
                "not": {"anyOf": [{"required": [field]} for field in ("url", "revision", "license")]},
            },
        )

    def test_min_length_and_min_items_boundaries_match_validator(self) -> None:
        for name, schema, document, validator in self.cases:
            for schema_pointer, document_pointer, node in property_facets(schema):
                if "minLength" in node:
                    minimum = node["minLength"]
                    for length, expected in ((minimum, True), (minimum - 1, False)):
                        changed = deepcopy(document)
                        assign(changed, document_pointer, "x" * length)
                        with self.subTest(
                            name=name, schema=schema_pointer, length=length
                        ):
                            self.assertEqual(expected, self.accepts(validator, changed))
                if "minItems" in node:
                    minimum = node["minItems"]
                    original = resolve(document, document_pointer)
                    allowed = deepcopy(original[:minimum])  # type: ignore[index]
                    prohibited = deepcopy(original[: minimum - 1])  # type: ignore[index]
                    for value, expected in ((allowed, True), (prohibited, False)):
                        changed = deepcopy(document)
                        assign(changed, document_pointer, value)
                        with self.subTest(
                            name=name, schema=schema_pointer, size=len(value)
                        ):
                            self.assertEqual(expected, self.accepts(validator, changed))

    def test_integer_and_minimum_boundaries_match_validator(self) -> None:
        for name, schema, document, validator in self.cases:
            for schema_pointer, document_pointer, node in property_facets(schema):
                if node.get("type") != "integer":
                    continue
                minimum = node.get("minimum", 0)
                for value, expected in (
                    (minimum, True),
                    (minimum - 1, False),
                    (minimum + 0.5, False),
                    (True, False),
                ):
                    changed = deepcopy(document)
                    assign(changed, document_pointer, value)
                    with self.subTest(name=name, schema=schema_pointer, value=value):
                        self.assertEqual(expected, self.accepts(validator, changed))

    def test_declared_types_match_validator(self) -> None:
        wrong_values = {"object": [], "array": {}, "string": []}
        for name, schema, document, validator in self.cases:
            fields = [("", "", schema)] + property_facets(schema)
            for schema_pointer, document_pointer, node in fields:
                declared = node.get("type")
                if declared not in wrong_values:
                    continue
                changed = deepcopy(document)
                if document_pointer:
                    assign(changed, document_pointer, wrong_values[declared])
                else:
                    changed = wrong_values[declared]
                with self.subTest(name=name, schema=schema_pointer, type=declared):
                    self.assertFalse(self.accepts(validator, changed))  # type: ignore[arg-type]

    def test_const_and_boolean_facets_match_validator(self) -> None:
        for name, schema, document, validator in self.cases:
            for schema_pointer, document_pointer, node in property_facets(schema):
                if "const" in node:
                    allowed = deepcopy(document)
                    assign(allowed, document_pointer, node["const"])
                    self.assertTrue(self.accepts(validator, allowed))
                    prohibited = deepcopy(document)
                    assign(prohibited, document_pointer, "__not_the_const__")
                    with self.subTest(name=name, schema=schema_pointer, facet="const"):
                        self.assertFalse(self.accepts(validator, prohibited))
                if node.get("type") == "boolean":
                    for value, expected in ((True, True), (False, True), (0, False)):
                        changed = deepcopy(document)
                        assign(changed, document_pointer, value)
                        if name == "admissions" and value is False:
                            changed["admissions"][0]["disposition"] = "reject"
                        with self.subTest(
                            name=name, schema=schema_pointer, value=value
                        ):
                            self.assertEqual(expected, self.accepts(validator, changed))

    def test_object_property_count_and_name_boundaries_match_validator(self) -> None:
        for name, schema, document, validator in self.cases:
            for schema_pointer, document_pointer, node in property_facets(schema):
                if "minProperties" in node:
                    minimum = node["minProperties"]
                    original = resolve(document, document_pointer)
                    entries = list(original.items())  # type: ignore[union-attr]
                    for size, expected in ((minimum, True), (minimum - 1, False)):
                        changed = deepcopy(document)
                        assign(changed, document_pointer, dict(entries[:size]))
                        with self.subTest(
                            name=name, schema=schema_pointer, size=size
                        ):
                            self.assertEqual(expected, self.accepts(validator, changed))
                property_names = node.get("propertyNames")
                if isinstance(property_names, dict) and "minLength" in property_names:
                    minimum = property_names["minLength"]
                    original = resolve(document, document_pointer)
                    value = next(iter(original.values()))  # type: ignore[union-attr]
                    for length, expected in ((minimum, True), (minimum - 1, False)):
                        changed = deepcopy(document)
                        assign(changed, document_pointer, {"x" * length: value})
                        with self.subTest(
                            name=name,
                            schema=join(schema_pointer, "propertyNames"),
                            length=length,
                        ):
                            self.assertEqual(expected, self.accepts(validator, changed))


if __name__ == "__main__":
    unittest.main()
