"""Small, strict parsers for repository contracts."""

from __future__ import annotations

import json
import hashlib
import math
import os
import re
from pathlib import Path, PurePosixPath


_KEY = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")
_PLAIN_RESERVED = "-?:,[]{}#&*!|>'\"%@`"
_SKILL_ID = re.compile(r"skill\.curated\.[a-z0-9][a-z0-9-]*")
_DIRECTORY = re.compile(r"[a-z0-9][a-z0-9-]*")
_CAPABILITY_ID = re.compile(r"capability\.[a-z0-9][a-z0-9-]*")
_CONFLICT_ID = re.compile(r"conflict\.[a-z0-9][a-z0-9-]*")
_RECIPE_ID = re.compile(r"recipe\.[a-z0-9][a-z0-9-]*")
_MANIFEST_PATH = re.compile(
    r"^skills/(?:[A-Za-z0-9][A-Za-z0-9._-]*/)*[A-Za-z0-9][A-Za-z0-9._-]*$"
)
_DIGEST = re.compile(r"[0-9a-f]{64}")
_EXTERNAL_REFERENCE = re.compile(
    r"(?:external|upstream):[A-Za-z0-9][A-Za-z0-9._-]*(?:/[A-Za-z0-9][A-Za-z0-9._-]*)*"
)
_SKILL_STATUSES = {
    "candidate", "adapted", "reviewed", "approved", "deprecated", "retired",
}
_SELECTION_DISPOSITIONS = {
    "adopt", "merge", "adapter-only", "recipe-only", "reject",
}
_SOURCE_KINDS = {"git", "local"}
_PROVENANCE_STATUSES = {"complete", "incomplete"}
_REDISTRIBUTION_STATUSES = {"license-governed", "private-only"}


class ContractError(ValueError):
    """A contract violation tied to a document and pointer."""

    def __init__(self, document: str, pointer: str, message: str) -> None:
        self.document = document
        self.pointer = pointer
        self.message = message
        super().__init__(f"{document}:{pointer}: {message}")


def _join(pointer: str, part: str | int) -> str:
    escaped = str(part).replace("~", "~0").replace("/", "~1")
    return f"{pointer}/{escaped}" if pointer else f"/{escaped}"


def require_object(value: object, document: str, pointer: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ContractError(document, pointer, "must be an object")
    return value


def require_array(
    value: object, document: str, pointer: str, min_items: int = 0
) -> list[object]:
    if not isinstance(value, list):
        raise ContractError(document, pointer, "must be an array")
    if len(value) < min_items:
        raise ContractError(document, pointer, f"must contain at least {min_items} item(s)")
    return value


def require_string(value: object, document: str, pointer: str) -> str:
    if not isinstance(value, str):
        raise ContractError(document, pointer, "must be a string")
    return value


def require_min_length(
    value: object, min_length: int, document: str, pointer: str
) -> str:
    text = require_string(value, document, pointer)
    if len(text) < min_length:
        raise ContractError(
            document, pointer, f"must contain at least {min_length} character(s)"
        )
    return text


def require_int(value: object, document: str, pointer: str) -> int:
    if isinstance(value, bool):
        raise ContractError(document, pointer, "must be an integer")
    if isinstance(value, int):
        return value
    if isinstance(value, float) and math.isfinite(value) and value.is_integer():
        return int(value)
    raise ContractError(document, pointer, "must be an integer")


def require_keys(
    value: dict[str, object], required: set[str], document: str, pointer: str
) -> None:
    for key in sorted(required):
        if key not in value:
            raise ContractError(document, _join(pointer, key), "is required")


def reject_unknown(
    value: dict[str, object], allowed: set[str], document: str, pointer: str
) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise ContractError(document, _join(pointer, unknown[0]), "unknown field")


def require_enum(
    value: object, allowed: set[str], document: str, pointer: str
) -> str:
    text = require_string(value, document, pointer)
    if text not in allowed:
        raise ContractError(document, pointer, f"must be one of: {', '.join(sorted(allowed))}")
    return text


def require_pattern(
    value: object, expression: re.Pattern[str], document: str, pointer: str
) -> str:
    text = require_string(value, document, pointer)
    if not expression.fullmatch(text):
        raise ContractError(document, pointer, "has invalid format")
    return text


# Short public aliases matching the contract vocabulary.
keys = require_keys
enum = require_enum
pattern = require_pattern


def _require_bool(value: object, document: str, pointer: str) -> bool:
    if not isinstance(value, bool):
        raise ContractError(document, pointer, "must be a boolean")
    return value


def _strings(
    value: object,
    document: str,
    pointer: str,
    *,
    min_items: int = 0,
) -> list[object]:
    items = require_array(value, document, pointer, min_items)
    for index, item in enumerate(items):
        require_min_length(item, 1, document, _join(pointer, index))
    return items


def _document(
    value: object,
    document: str,
    collection: str,
    top_allowed: set[str] | None = None,
) -> tuple[dict[str, object], list[object]]:
    root = require_object(value, document, "")
    allowed = top_allowed or {"schema", collection}
    require_keys(root, {"schema", collection}, document, "")
    reject_unknown(root, allowed, document, "")
    if require_int(root["schema"], document, "/schema") != 1:
        raise ContractError(document, "/schema", "must equal 1")
    return root, require_array(root[collection], document, f"/{collection}", 1)


def validate_skills_document(value: object, document: str) -> None:
    _, items = _document(value, document, "skills")
    allowed = {"id", "directory", "name", "description", "status", "phase", "source"}
    required = set(allowed)
    for index, raw in enumerate(items):
        pointer = f"/skills/{index}"
        item = require_object(raw, document, pointer)
        require_keys(item, required, document, pointer)
        reject_unknown(item, allowed, document, pointer)
        require_pattern(item["id"], _SKILL_ID, document, _join(pointer, "id"))
        require_pattern(
            item["directory"], _DIRECTORY, document, _join(pointer, "directory")
        )
        for field in ("name", "description", "phase", "source"):
            require_min_length(item[field], 1, document, _join(pointer, field))
        require_enum(
            item["status"], _SKILL_STATUSES, document, _join(pointer, "status")
        )


def validate_capabilities_document(value: object, document: str) -> None:
    _, items = _document(value, document, "capabilities")
    allowed = {"id", "canonicalOwner"}
    for index, raw in enumerate(items):
        pointer = f"/capabilities/{index}"
        item = require_object(raw, document, pointer)
        require_keys(item, allowed, document, pointer)
        reject_unknown(item, allowed, document, pointer)
        require_pattern(item["id"], _CAPABILITY_ID, document, _join(pointer, "id"))
        require_min_length(
            item["canonicalOwner"], 1, document, _join(pointer, "canonicalOwner")
        )


def validate_relations_document(value: object, document: str) -> None:
    root = require_object(value, document, "")
    allowed_top = {"schema", "relationTypes", "relations"}
    require_keys(root, allowed_top, document, "")
    reject_unknown(root, allowed_top, document, "")
    if require_int(root["schema"], document, "/schema") != 1:
        raise ContractError(document, "/schema", "must equal 1")
    _strings(root["relationTypes"], document, "/relationTypes", min_items=1)
    relations = require_array(root["relations"], document, "/relations", 1)
    required = {"from", "type", "to"}
    allowed = required | {"condition"}
    for index, raw in enumerate(relations):
        pointer = f"/relations/{index}"
        item = require_object(raw, document, pointer)
        require_keys(item, required, document, pointer)
        reject_unknown(item, allowed, document, pointer)
        for field in item:
            require_min_length(item[field], 1, document, _join(pointer, field))


def validate_conflicts_document(value: object, document: str) -> None:
    _, groups = _document(value, document, "groups")
    allowed = {"id", "defaultOwner", "members", "resolution"}
    for index, raw in enumerate(groups):
        pointer = f"/groups/{index}"
        item = require_object(raw, document, pointer)
        require_keys(item, allowed, document, pointer)
        reject_unknown(item, allowed, document, pointer)
        require_pattern(item["id"], _CONFLICT_ID, document, _join(pointer, "id"))
        for field in ("defaultOwner", "resolution"):
            require_min_length(item[field], 1, document, _join(pointer, field))
        _strings(item["members"], document, _join(pointer, "members"), min_items=1)


def validate_recipes_document(value: object, document: str) -> None:
    _, recipes = _document(value, document, "recipes")
    allowed = {"id", "trigger", "steps", "authorization"}
    required = {"id", "trigger", "steps"}
    step_allowed = {"capability", "when"}
    for index, raw in enumerate(recipes):
        pointer = f"/recipes/{index}"
        item = require_object(raw, document, pointer)
        require_keys(item, required, document, pointer)
        reject_unknown(item, allowed, document, pointer)
        require_pattern(item["id"], _RECIPE_ID, document, _join(pointer, "id"))
        require_min_length(item["trigger"], 1, document, _join(pointer, "trigger"))
        if "authorization" in item:
            require_min_length(
                item["authorization"], 1, document, _join(pointer, "authorization")
            )
        steps = require_array(item["steps"], document, _join(pointer, "steps"), 1)
        for step_index, raw_step in enumerate(steps):
            step_pointer = _join(_join(pointer, "steps"), step_index)
            step = require_object(raw_step, document, step_pointer)
            require_keys(step, {"capability"}, document, step_pointer)
            reject_unknown(step, step_allowed, document, step_pointer)
            for field in step:
                require_min_length(step[field], 1, document, _join(step_pointer, field))


def validate_sources_lock_document(value: object, document: str) -> None:
    _, sources = _document(value, document, "sources")
    allowed = {
        "id", "url", "revision", "candidateIds", "license", "status",
        "approvedForRuntime", "notes", "kind", "provenanceStatus",
        "redistribution", "reviewRefs",
    }
    required = {
        "id", "candidateIds", "status", "approvedForRuntime", "notes", "kind",
        "provenanceStatus", "redistribution", "reviewRefs",
    }
    for index, raw in enumerate(sources):
        pointer = f"/sources/{index}"
        item = require_object(raw, document, pointer)
        require_keys(item, required, document, pointer)
        reject_unknown(item, allowed, document, pointer)
        for field in ("id", "url", "revision", "license", "status"):
            if field in item:
                require_min_length(item[field], 1, document, _join(pointer, field))
        _strings(
            item["candidateIds"], document, _join(pointer, "candidateIds"), min_items=1
        )
        _require_bool(item["approvedForRuntime"], document, _join(pointer, "approvedForRuntime"))
        _strings(item["notes"], document, _join(pointer, "notes"), min_items=1)
        require_enum(item["kind"], _SOURCE_KINDS, document, _join(pointer, "kind"))
        require_enum(
            item["provenanceStatus"],
            _PROVENANCE_STATUSES,
            document,
            _join(pointer, "provenanceStatus"),
        )
        require_enum(
            item["redistribution"],
            _REDISTRIBUTION_STATUSES,
            document,
            _join(pointer, "redistribution"),
        )
        _strings(item["reviewRefs"], document, _join(pointer, "reviewRefs"), min_items=1)
        if item["kind"] == "local":
            for field in ("url", "revision", "license"):
                if field in item:
                    raise ContractError(
                        document, _join(pointer, field), "is not allowed for local sources"
                    )
            if item["provenanceStatus"] != "incomplete":
                raise ContractError(
                    document,
                    _join(pointer, "provenanceStatus"),
                    "must be incomplete for local sources",
                )
            if item["redistribution"] != "private-only":
                raise ContractError(
                    document,
                    _join(pointer, "redistribution"),
                    "must be private-only for local sources",
                )


def validate_selection_document(value: object, document: str) -> None:
    root = require_object(value, document, "")
    allowed = {"schema", "source", "revision", "decisions", "excludedExecutables"}
    required = {"schema", "source", "revision", "decisions"}
    require_keys(root, required, document, "")
    reject_unknown(root, allowed, document, "")
    if require_int(root["schema"], document, "/schema") != 1:
        raise ContractError(document, "/schema", "must equal 1")
    require_min_length(root["source"], 1, document, "/source")
    require_min_length(root["revision"], 1, document, "/revision")
    decisions = require_object(root["decisions"], document, "/decisions")
    if not decisions:
        raise ContractError(document, "/decisions", "must contain at least 1 property")
    for name, disposition in decisions.items():
        require_min_length(name, 1, document, _join("/decisions", name))
        require_enum(
            disposition,
            _SELECTION_DISPOSITIONS,
            document,
            _join("/decisions", name),
        )
    if "excludedExecutables" in root:
        _strings(root["excludedExecutables"], document, "/excludedExecutables")


def canonical_payload_path(
    raw: object, document: str, pointer: str
) -> PurePosixPath:
    """Return a canonical manifest path confined to a nested Skill payload."""

    text = require_string(raw, document, pointer)
    if not text or "\\" in text or "//" in text or text.endswith("/"):
        raise ContractError(document, pointer, "must be a canonical POSIX path")
    path = PurePosixPath(text)
    parts = path.parts
    if path.is_absolute() or any(part in {".", ".."} for part in parts):
        raise ContractError(document, pointer, "must be a canonical relative path")
    if len(parts) < 3 or parts[0] != "skills":
        raise ContractError(document, pointer, "must be nested under skills/<directory>")
    if not _MANIFEST_PATH.fullmatch(text):
        raise ContractError(document, pointer, "has invalid format")
    return path


def validate_manifest_entries(
    manifest: dict[str, object], document: str
) -> dict[PurePosixPath, tuple[int, dict[str, object]]]:
    """Validate manifest entry identity and scalar integrity."""

    files = require_array(manifest.get("files"), document, "/files")
    entries: dict[PurePosixPath, tuple[int, dict[str, object]]] = {}
    folded_paths: dict[str, str] = {}
    fields = {"path", "sha256", "size"}
    for index, raw in enumerate(files):
        pointer = f"/files/{index}"
        item = require_object(raw, document, pointer)
        require_keys(item, fields, document, pointer)
        reject_unknown(item, fields, document, pointer)
        path_pointer = _join(pointer, "path")
        path = canonical_payload_path(item["path"], document, path_pointer)
        text = path.as_posix()
        folded = text.casefold()
        if path in entries:
            raise ContractError(document, path_pointer, "duplicate manifest path")
        if folded in folded_paths:
            raise ContractError(
                document, path_pointer, "manifest path has a casefold collision"
            )
        digest_pointer = _join(pointer, "sha256")
        require_pattern(item["sha256"], _DIGEST, document, digest_pointer)
        size_pointer = _join(pointer, "size")
        size = require_int(item["size"], document, size_pointer)
        if size < 0:
            raise ContractError(document, size_pointer, "must be non-negative")
        entries[path] = (index, item)
        folded_paths[folded] = text
    return entries


def validate_release_manifest_document(value: object, document: str) -> None:
    root = require_object(value, document, "")
    allowed = {"schema", "skillCount", "fileCount", "files"}
    require_keys(root, allowed, document, "")
    reject_unknown(root, allowed, document, "")
    if require_int(root["schema"], document, "/schema") != 1:
        raise ContractError(document, "/schema", "must equal 1")
    skill_count = require_int(root["skillCount"], document, "/skillCount")
    if skill_count < 0:
        raise ContractError(document, "/skillCount", "must be non-negative")
    file_count = require_int(root["fileCount"], document, "/fileCount")
    if file_count < 0:
        raise ContractError(document, "/fileCount", "must be non-negative")
    validate_manifest_entries(root, document)


def is_link_or_reparse(path: Path) -> bool:
    """Detect POSIX symlinks and Windows reparse points without following them."""

    if path.is_symlink():
        return True
    attributes = getattr(path.lstat(), "st_file_attributes", 0)
    reparse_point = getattr(os.stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(attributes & reparse_point)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_manifest_payload(
    root: Path,
    manifest: dict[str, object],
    registry: list[dict[str, object]],
) -> None:
    """Validate exact, link-free Skill payload coverage and file metadata."""

    document = "release-manifest.json"
    entries = validate_manifest_entries(manifest, document)

    registered: dict[str, tuple[int, str]] = {}
    for index, item in enumerate(registry):
        status_pointer = f"/skills/{index}/status"
        if item.get("status") != "approved":
            raise ContractError(
                "registry/skills.json",
                status_pointer,
                "must be approved to enter the release payload",
            )
        directory = item.get("directory")
        pointer = f"/skills/{index}/directory"
        if not isinstance(directory, str):
            raise ContractError("registry/skills.json", pointer, "must be a string")
        folded = directory.casefold()
        if folded in registered:
            raise ContractError(
                "registry/skills.json", pointer, "duplicate Skill directory"
            )
        registered[folded] = (index, directory)

    for path, (index, _) in entries.items():
        if path.parts[1].casefold() not in registered:
            raise ContractError(
                document,
                f"/files/{index}/path",
                "manifest path uses an unregistered Skill root",
            )

    skills_root = root / "skills"
    for boundary in (root, skills_root):
        if is_link_or_reparse(boundary):
            raise ContractError(document, "/files", "payload contains a symlink or reparse point")

    for child in skills_root.iterdir():
        if is_link_or_reparse(child):
            raise ContractError(document, "/files", "payload contains a symlink or reparse point")
        if child.is_dir():
            registration = registered.get(child.name.casefold())
            if registration is None or registration[1] != child.name:
                raise ContractError(
                    document,
                    "/files",
                    "payload contains an unregistered Skill root",
                )

    actual: dict[PurePosixPath, Path] = {}
    actual_folded: dict[str, str] = {}

    def reject_walk_error(error: OSError) -> None:
        raise ContractError(
            document,
            "/files",
            f"cannot enumerate Skill payload: {error}",
        ) from error

    for current, dirs, files in os.walk(
        skills_root,
        topdown=True,
        onerror=reject_walk_error,
        followlinks=False,
    ):
        current_path = Path(current)
        if is_link_or_reparse(current_path):
            raise ContractError(document, "/files", "payload contains a symlink or reparse point")
        for name in dirs + files:
            candidate = current_path / name
            if is_link_or_reparse(candidate):
                raise ContractError(
                    document, "/files", "payload contains a symlink or reparse point"
                )
        for name in files:
            candidate = current_path / name
            relative = PurePosixPath(candidate.relative_to(root).as_posix())
            folded = relative.as_posix().casefold()
            if folded in actual_folded:
                raise ContractError(document, "/files", "payload path has a casefold collision")
            actual[relative] = candidate
            actual_folded[folded] = relative.as_posix()

    for path, (index, _) in entries.items():
        if path not in actual:
            raise ContractError(
                document, f"/files/{index}/path", "manifest file does not exist"
            )
    if set(entries) != set(actual):
        raise ContractError(document, "/files", "manifest must exactly cover Skill files")

    for _, directory in registered.values():
        skill_file = PurePosixPath("skills", directory, "SKILL.md")
        if skill_file not in entries:
            raise ContractError(
                document,
                "/files",
                f"registered Skill {directory} requires exactly one SKILL.md",
            )

    for path, (index, item) in entries.items():
        payload = actual[path]
        if payload.stat().st_size != item["size"]:
            raise ContractError(document, f"/files/{index}/size", "does not match payload")
        if _sha256(payload) != item["sha256"]:
            raise ContractError(document, f"/files/{index}/sha256", "does not match payload")


def _error(document: str, line_number: int, message: str) -> ContractError:
    return ContractError(document, f"line {line_number}", message)


def _inline_scalar(value: str, document: str, line_number: int) -> str:
    if not value:
        raise _error(document, line_number, "empty scalar is not supported")
    if value.startswith('"'):
        try:
            decoded = json.loads(value)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise _error(document, line_number, "invalid double-quoted scalar") from exc
        if not isinstance(decoded, str):
            raise _error(document, line_number, "only string scalars are supported")
        return decoded
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            raise _error(document, line_number, "invalid single-quoted scalar")
        inner = value[1:-1]
        remainder = inner.replace("''", "")
        if "'" in remainder:
            raise _error(document, line_number, "invalid single-quoted scalar")
        return inner.replace("''", "'")
    if value[0] in _PLAIN_RESERVED:
        raise _error(document, line_number, "reserved YAML indicator in plain scalar")
    if ": " in value or " #" in value:
        raise _error(document, line_number, "ambiguous YAML syntax in plain scalar")
    return value


def _block_scalar(lines: list[str], style: str) -> str:
    if style == "|":
        return "\n".join(lines)
    return " ".join(lines)


def parse_frontmatter(text: str, document: str) -> dict[str, object]:
    """Parse the repository's scalar and one-level-mapping YAML subset."""

    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ContractError(document, "line 1", "missing YAML frontmatter")
    try:
        closing_index = lines.index("---", 1)
    except ValueError as exc:
        raise ContractError(document, "frontmatter", "unclosed YAML frontmatter") from exc

    frontmatter = lines[1:closing_index]
    if any("\t" in line for line in frontmatter):
        line_index = next(index for index, line in enumerate(frontmatter, 2) if "\t" in line)
        raise _error(document, line_index, "tabs are not allowed in frontmatter")

    values: dict[str, object] = {}
    index = 0
    while index < len(frontmatter):
        line = frontmatter[index]
        line_number = index + 2
        if not line:
            index += 1
            continue
        if line[0].isspace() or ":" not in line:
            raise _error(document, line_number, "invalid top-level frontmatter structure")

        key, raw_value = line.split(":", 1)
        if not _KEY.fullmatch(key):
            raise _error(document, line_number, "invalid top-level frontmatter key")
        if key in values:
            raise _error(document, line_number, f"duplicate key: {key}")
        if raw_value and not raw_value.startswith(" "):
            raise _error(document, line_number, "a space is required after ':'")
        value = raw_value.strip()

        if not value:
            index += 1
            mapping: dict[str, str] = {}
            while index < len(frontmatter):
                nested_line = frontmatter[index]
                nested_line_number = index + 2
                if not nested_line or not nested_line[0].isspace():
                    break
                leading = len(nested_line) - len(nested_line.lstrip(" "))
                if leading != 2:
                    raise _error(document, nested_line_number, "malformed mapping indentation")
                nested = nested_line[2:]
                if ":" not in nested:
                    raise _error(document, nested_line_number, "invalid mapping entry")
                nested_key, nested_raw_value = nested.split(":", 1)
                if not _KEY.fullmatch(nested_key):
                    raise _error(document, nested_line_number, "invalid mapping key")
                if nested_key in mapping:
                    raise _error(document, nested_line_number, f"duplicate key: {nested_key}")
                if not nested_raw_value.startswith(" "):
                    raise _error(document, nested_line_number, "a space is required after ':'")
                nested_value = nested_raw_value.strip()
                if nested_value in (">", "|") or not nested_value:
                    raise _error(document, nested_line_number, "nested structures are not supported")
                mapping[nested_key] = _inline_scalar(
                    nested_value, document, nested_line_number
                )
                index += 1
            if not mapping:
                raise _error(document, line_number, "mapping requires indented scalar entries")
            values[key] = mapping
            continue

        if value in (">", "|"):
            style = value
            index += 1
            block: list[str] = []
            while index < len(frontmatter):
                block_line = frontmatter[index]
                if block_line and not block_line[0].isspace():
                    break
                if not block_line:
                    raise _error(document, index + 2, "blank block scalar lines are not supported")
                leading = len(block_line) - len(block_line.lstrip(" "))
                if leading != 2:
                    raise _error(document, index + 2, "malformed block scalar indentation")
                content = block_line[2:]
                if not content:
                    raise _error(document, index + 2, "empty block scalar lines are not supported")
                block.append(content)
                index += 1
            if not block:
                raise _error(document, line_number, "block scalar requires indented content")
            values[key] = _block_scalar(block, style)
            continue

        values[key] = _inline_scalar(value, document, line_number)
        index += 1

    return values


def validate_inventory_counts(
    registry: list[dict[str, object]],
    manifest: dict[str, object],
    directories: list[str],
    document: str,
) -> None:
    """Validate manifest counts against the inventory they summarize."""

    skill_count = manifest.get("skillCount")
    if skill_count != len(registry) or skill_count != len(directories):
        raise ContractError(
            document,
            "/skillCount",
            "must match registry entries and installed Skill directories",
        )

    files = manifest.get("files")
    if not isinstance(files, list):
        raise ContractError(document, "/files", "must be an array")
    if manifest.get("fileCount") != len(files):
        raise ContractError(document, "/fileCount", "must match the files array")

    skill_roots = {
        parts[1]
        for item in files
        if isinstance(item, dict)
        and isinstance(item.get("path"), str)
        and len(parts := item["path"].split("/")) >= 3
        and parts[0] == "skills"
    }
    if len(skill_roots) != skill_count:
        raise ContractError(
            document,
            "/skillCount",
            "must match the distinct Skill roots represented by files",
        )
    registry_directories = {item.get("directory") for item in registry}
    if skill_roots != registry_directories:
        raise ContractError(
            document,
            "/files",
            "Skill roots must match registry directories",
        )


def validate_selection_closure(
    decisions: dict[str, str], allowed_dispositions: set[str], document: str
) -> None:
    """Validate that a source selection is nonempty and uses known dispositions."""

    if not decisions:
        raise ContractError(document, "/decisions", "must contain at least one decision")
    for name, disposition in decisions.items():
        if not name:
            raise ContractError(document, "/decisions", "decision names must not be empty")
        if disposition not in allowed_dispositions:
            raise ContractError(
                document,
                _join("/decisions", name),
                f"unknown disposition: {disposition}",
            )


def validate_source_selection(
    selection: dict[str, object],
    source_record: dict[str, object],
    allowed_dispositions: set[str],
    document: str,
) -> None:
    """Validate a source selection against its pinned source inventory."""

    if selection.get("source") != source_record.get("id"):
        raise ContractError(document, "/source", "must match the pinned source id")
    if selection.get("revision") != source_record.get("revision"):
        raise ContractError(
            document, "/revision", "must match the pinned source revision"
        )
    decisions = selection["decisions"]
    candidates = set(source_record["candidateIds"])  # type: ignore[arg-type]
    missing = candidates - set(decisions)  # type: ignore[arg-type]
    if missing:
        name = sorted(missing)[0]
        raise ContractError(
            document,
            _join("/decisions", name),
            "missing pinned source candidate decision",
        )
    extra = set(decisions) - candidates  # type: ignore[arg-type]
    if extra:
        name = sorted(extra)[0]
        raise ContractError(
            document,
            _join("/decisions", name),
            "decision is not a pinned source candidate",
        )
    validate_selection_closure(
        decisions, allowed_dispositions, document  # type: ignore[arg-type]
    )


def validate_adopted_selection(
    decisions: dict[str, str],
    registry: list[dict[str, object]],
    source_id: str,
    document: str,
) -> None:
    """Validate adopted decisions against registry entries from their source."""

    entries = {item.get("directory"): item for item in registry}
    for name, disposition in decisions.items():
        if disposition != "adopt":
            continue
        entry = entries.get(name)
        if entry is None:
            raise ContractError(
                document,
                _join("/decisions", name),
                "adopted Skill is missing from registry",
            )
        if entry.get("source") != source_id:
            raise ContractError(
                document,
                _join("/decisions", name),
                "adopted Skill registry source does not match selection source",
            )

    for item in registry:
        if item.get("source") == source_id:
            name = item.get("directory")
            if not isinstance(name, str) or decisions.get(name) != "adopt":
                pointer = _join("/decisions", name) if name else "/decisions"
                raise ContractError(
                    document,
                    pointer,
                    "source Skill requires a matching adopt decision",
                )


_REFERENCE_DOCUMENTS = {
    "skills": "registry/skills.json",
    "capabilities": "registry/capabilities.json",
    "relations": "registry/relations.json",
    "conflicts": "registry/conflicts.json",
    "recipes": "registry/recipes.json",
    "sources": "sources/lock.json",
}


def _unique_field(
    items: list[object], field: str, collection: str, document: str
) -> set[str]:
    values: set[str] = set()
    for index, raw in enumerate(items):
        item = raw  # Shape validation runs before reference validation.
        value = item[field]  # type: ignore[index]
        if value in values:
            raise ContractError(
                document, f"/{collection}/{index}/{field}", f"duplicate {field}"
            )
        values.add(value)  # type: ignore[arg-type]
    return values


def _is_external_reference(value: str) -> bool:
    return _EXTERNAL_REFERENCE.fullmatch(value) is not None


def validate_references(documents: dict[str, object]) -> None:
    """Validate cross-document identity and reference closure after shape checks."""

    skills = documents["skills"]["skills"]  # type: ignore[index]
    capabilities = documents["capabilities"]["capabilities"]  # type: ignore[index]
    relations = documents["relations"]["relations"]  # type: ignore[index]
    conflicts = documents["conflicts"]["groups"]  # type: ignore[index]
    recipes = documents["recipes"]["recipes"]  # type: ignore[index]
    sources = documents["sources"]["sources"]  # type: ignore[index]

    skill_ids = _unique_field(
        skills, "id", "skills", _REFERENCE_DOCUMENTS["skills"]  # type: ignore[arg-type]
    )
    _unique_field(
        skills, "directory", "skills", _REFERENCE_DOCUMENTS["skills"]  # type: ignore[arg-type]
    )
    _unique_field(
        skills, "name", "skills", _REFERENCE_DOCUMENTS["skills"]  # type: ignore[arg-type]
    )
    capability_ids = _unique_field(
        capabilities,
        "id",
        "capabilities",
        _REFERENCE_DOCUMENTS["capabilities"],  # type: ignore[arg-type]
    )
    _unique_field(
        conflicts, "id", "groups", _REFERENCE_DOCUMENTS["conflicts"]  # type: ignore[arg-type]
    )
    _unique_field(
        recipes, "id", "recipes", _REFERENCE_DOCUMENTS["recipes"]  # type: ignore[arg-type]
    )

    source_ids = _unique_field(
        sources, "id", "sources", _REFERENCE_DOCUMENTS["sources"]  # type: ignore[arg-type]
    )
    for index, item in enumerate(skills):  # type: ignore[assignment]
        if item["source"] not in source_ids:
            raise ContractError(
                _REFERENCE_DOCUMENTS["skills"],
                f"/skills/{index}/source",
                "source must resolve to a source lock record",
            )

    internal_ids = skill_ids | capability_ids
    relation_types = set(documents["relations"]["relationTypes"])  # type: ignore[index,arg-type]
    provided = set()
    relation_keys = set()
    for index, relation in enumerate(relations):  # type: ignore[assignment]
        pointer = f"/relations/{index}"
        if relation["type"] not in relation_types:
            raise ContractError(
                _REFERENCE_DOCUMENTS["relations"],
                _join(pointer, "type"),
                "must be declared in relationTypes",
            )
        for endpoint in ("from", "to"):
            value = relation[endpoint]
            if value not in internal_ids and not _is_external_reference(value):
                raise ContractError(
                    _REFERENCE_DOCUMENTS["relations"],
                    _join(pointer, endpoint),
                    "must resolve internally or use external:/upstream:",
                )
        if relation["type"] == "provides":
            if relation["from"] not in skill_ids:
                raise ContractError(
                    _REFERENCE_DOCUMENTS["relations"],
                    _join(pointer, "from"),
                    "provides must start at a Skill",
                )
            if relation["to"] not in capability_ids:
                raise ContractError(
                    _REFERENCE_DOCUMENTS["relations"],
                    _join(pointer, "to"),
                    "provides must end at a capability",
                )
            provided.add((relation["from"], relation["to"]))
        key = (
            relation["from"],
            relation["type"],
            relation["to"],
            relation.get("condition"),
        )
        if key in relation_keys:
            raise ContractError(
                _REFERENCE_DOCUMENTS["relations"], pointer, "duplicate relation"
            )
        relation_keys.add(key)

    for index, capability in enumerate(capabilities):  # type: ignore[assignment]
        owner = capability["canonicalOwner"]
        pointer = f"/capabilities/{index}/canonicalOwner"
        if owner.startswith("skill.curated."):
            if owner not in skill_ids or (owner, capability["id"]) not in provided:
                raise ContractError(
                    _REFERENCE_DOCUMENTS["capabilities"],
                    pointer,
                    "curated owner must exist and provide this capability",
                )
        elif not _is_external_reference(owner):
            raise ContractError(
                _REFERENCE_DOCUMENTS["capabilities"],
                pointer,
                "must be a curated Skill or use external:/upstream:",
            )

    for group_index, group in enumerate(conflicts):  # type: ignore[assignment]
        members = group["members"]
        if group["defaultOwner"] not in members:
            raise ContractError(
                _REFERENCE_DOCUMENTS["conflicts"],
                f"/groups/{group_index}/defaultOwner",
                "must be one of the conflict members",
            )
        seen_members = set()
        for member_index, member in enumerate(members):
            pointer = f"/groups/{group_index}/members/{member_index}"
            if member in seen_members:
                raise ContractError(
                    _REFERENCE_DOCUMENTS["conflicts"], pointer, "duplicate member"
                )
            seen_members.add(member)
            if member not in internal_ids and not _is_external_reference(member):
                raise ContractError(
                    _REFERENCE_DOCUMENTS["conflicts"],
                    pointer,
                    "must resolve internally or use external:/upstream:",
                )

    for recipe_index, recipe in enumerate(recipes):  # type: ignore[assignment]
        for step_index, step in enumerate(recipe["steps"]):
            if step["capability"] not in capability_ids:
                raise ContractError(
                    _REFERENCE_DOCUMENTS["recipes"],
                    f"/recipes/{recipe_index}/steps/{step_index}/capability",
                    "must resolve to a capability",
                )
