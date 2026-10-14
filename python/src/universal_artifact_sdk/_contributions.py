"""Contribution-only canonical schema checks, bibliography IDs and safe file ownership."""

from __future__ import annotations

import hashlib
import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator
from ruamel.yaml.error import YAMLError

from .model import Artifact, canonical_schema_path


@lru_cache(maxsize=1)
def _validator() -> Draft7Validator:
    schema = json.loads(canonical_schema_path().read_text(encoding="utf-8"))
    return Draft7Validator({"$defs": schema["$defs"], **schema["properties"]["contributions"]})


def shape_issues(value: Any) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    for error in _validator().iter_errors(value):
        parts = list(error.absolute_path)
        if parts:
            index = parts.pop(0)
            record = value[index]
            candidate = record.get("id") if isinstance(record, dict) else None
            id = candidate if isinstance(candidate, str) else index
            path = f"contribution[{id}]"
        else:
            path = "contributions"
        for part in parts:
            path += f"[{part}]" if isinstance(part, int) else f".{part}"
        if error.validator == "required":
            for key in error.validator_value:
                if key not in error.instance:
                    issue = (f"{path}.{key}", f"requires {key}")
                    if issue not in issues:
                        issues.append(issue)
        else:
            issues.append((path, error.message))
    return issues


def safe_index_path(root: Path, relative: Any) -> Path:
    if not isinstance(relative, str) or not relative or relative.strip() != relative:
        raise ValueError("invalid contributions index path")
    slash = relative.replace("\\", "/")
    parts = slash.split("/")
    reserved = {
        "manifest.yml",
        "claims.yml",
        "results.yml",
        "datasets.yml",
        "exhibits.yml",
        "traces.yml",
        "assessments.yml",
        "journal.yml",
        "reflection.md",
        "sha256sums",
        ".sdk",
    }
    if (
        slash.startswith("/")
        or re.match(r"^[A-Za-z]:", slash)
        or any(p in ("", ".", "..") for p in parts)
        or parts[0].lower() in reserved
    ):
        raise ValueError(f"unsafe contributions index path: {relative}")
    path = root.resolve()
    for part in parts:
        path /= part
        if path.is_symlink():
            raise ValueError(f"symlink in contributions index path: {relative}")
    return path


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def capture_source(artifact: Artifact, path: Path) -> None:
    artifact.__dict__["_contribution_source"] = (str(path.resolve()), file_hash(path))


def write_plan(artifact: Artifact, root: Path) -> tuple[Path, bool]:
    path = safe_index_path(root, "contributions.yml")
    if not path.exists():
        return path, False
    hash = file_hash(path)
    state: dict[str, Any] = {}
    state_path = root / ".sdk/state.json"
    if state_path.is_file():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            pass
    hashes = state.get("generated_hashes") if isinstance(state, dict) else None
    owned = isinstance(hashes, dict) and hashes.get("contributions.yml") == hash
    source = getattr(artifact, "_contribution_source", None)
    if artifact.contributions and not owned and source != (str(path.resolve()), hash):
        raise ValueError(
            "Refusing to overwrite authored or externally edited contributions.yml; "
            "reopen before editing"
        )
    return path, not artifact.contributions and owned


def reference_ids_from_text(text: str, bibtex: bool) -> list[str] | None:
    from .open import _yaml_reader

    if bibtex:
        ids = []
        input = re.sub(r"^%.*$", "", text, flags=re.MULTILINE)
        entries = re.compile(r"@\s*([A-Za-z]+)\s*([{(])")
        position = 0
        while match := entries.search(input, position):
            start = match.end()
            opening = match[2]
            end = "}" if opening == "{" else ")"
            depth, braces, quoted, cursor = 1, 0, False, start
            while cursor < len(input):
                ch = input[cursor]
                if ch == "\\":
                    cursor += 2
                    continue
                if ch == '"' and (braces == 0 if opening == "(" else depth == 1):
                    quoted = not quoted
                if not quoted:
                    if opening == "(":
                        if ch == "{":
                            braces += 1
                        if ch == "}":
                            braces -= 1
                        if braces > 0 or ch == "}":
                            cursor += 1
                            continue
                    if ch == opening:
                        depth += 1
                    if ch == end:
                        depth -= 1
                    if depth == 0:
                        break
                cursor += 1
            if depth:
                return None
            position = cursor + 1
            if match[1].lower() in ("comment", "string", "preamble"):
                continue
            key = re.match(r"\s*([^,\s]+)\s*,", input[start:cursor])
            if not key:
                return None
            ids.append(key[1])
        return ids if ids or not text.strip() else None
    try:
        data = _yaml_reader().load(text)
        refs = data if isinstance(data, list) else data.get("references")
        if not isinstance(refs, list):
            return None
        ids = [
            next((r.get(k) for k in ("id", "key", "citation-key") if r.get(k) is not None), None)
            for r in refs
        ]
        return ids if all(isinstance(id, str) for id in ids) else None
    except (ValueError, AttributeError, TypeError, YAMLError):
        return None


def resolve_reference_ids(artifact: Artifact, roots: list[Path]) -> list[str] | None:
    relative = artifact.paper.references_export if artifact.paper else None
    if not relative:
        return None
    for root in roots:
        path = root / relative
        if path.is_file():
            try:
                return reference_ids_from_text(
                    path.read_text(encoding="utf-8"), relative.lower().endswith(".bib")
                )
            except (OSError, UnicodeError):
                return None
    return None
