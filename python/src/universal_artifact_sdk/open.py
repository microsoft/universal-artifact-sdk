"""Reopen an existing on-disk submission back into the model (spec §4, §4.1).

Reads the generated index files so the next change is a small edit rather than a
from-scratch rebuild; authored blobs stay on disk untouched and are preserved by the next
:func:`write_submission`. Reopening mirrors the frozen compatibility behavior: it parses
and reconstructs, but does not reject incomplete or legacy-compatible content. Callers
may invoke :func:`validate_structure`; :func:`write_submission` always does.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.constructor import SafeConstructor

from .model import FORMAT_VERSION, SDK_VERSION, Artifact, artifact_from_dict

_INDEXES = (
    ("datasets", "datasets.yml"),
    ("traces", "traces.yml"),
    ("results", "results.yml"),
    ("claims", "claims.yml"),
    ("exhibits", "exhibits.yml"),
    ("assessments", "assessments.yml"),
    ("journal", "journal.yml"),
)


class _CoreConstructor(SafeConstructor):
    """A YAML 1.2 *core schema* constructor.

    ``ruamel.yaml`` keeps YAML 1.1 flavored implicit types even in 1.2 mode: an ISO-8601
    journal timestamp would become a ``datetime``, and an underscore-grouped scalar such
    as ``1_000`` would become an integer. The core schema resolves a plain scalar only to
    null, bool, int, float or string, so anything outside the core int/float grammar stays
    the string the producing binding wrote. Without this, reopening another binding's
    output could silently change a value's type.
    """

    def construct_yaml_int(self, node: Any) -> Any:
        if not _CORE_INT.match(str(node.value)):
            return str(node.value)
        return super().construct_yaml_int(node)

    def construct_yaml_float(self, node: Any) -> Any:
        if not _CORE_FLOAT.match(str(node.value)):
            return str(node.value)
        return super().construct_yaml_float(node)


_CORE_INT = re.compile(r"^[-+]?(?:[0-9]+|0o[0-7]+|0x[0-9a-fA-F]+)$")
_CORE_FLOAT = re.compile(
    r"^[-+]?(?:\.[0-9]+|[0-9]+(?:\.[0-9]*)?)(?:[eE][-+]?[0-9]+)?$"
    r"|^[-+]?\.(?:inf|Inf|INF)$"
    r"|^\.(?:nan|NaN|NAN)$"
)

_CoreConstructor.add_constructor(
    "tag:yaml.org,2002:timestamp", lambda loader, node: str(node.value)
)
_CoreConstructor.add_constructor(
    "tag:yaml.org,2002:int", _CoreConstructor.construct_yaml_int
)
_CoreConstructor.add_constructor(
    "tag:yaml.org,2002:float", _CoreConstructor.construct_yaml_float
)


def _yaml_reader() -> YAML:
    """A pure-Python safe loader pinned to YAML 1.2 core-schema resolution."""
    yaml = YAML(typ="safe", pure=True)
    yaml.version = (1, 2)
    yaml.Constructor = _CoreConstructor
    return yaml


def read_yaml(path: str | Path) -> dict[str, Any]:
    """Parse a YAML 1.2 document into plain data; an empty document reads as ``{}``."""
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        loaded = _yaml_reader().load(handle)
    return loaded if isinstance(loaded, dict) else {}


def open_submission(directory: str | Path) -> Artifact:
    """Reconstruct an :class:`Artifact` from a submission directory.

    Raises ``FileNotFoundError`` when ``manifest.yml`` is absent.
    """
    root = Path(directory)
    manifest_path = root / "manifest.yml"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"open_submission: no manifest.yml in {root}")
    manifest = read_yaml(manifest_path)
    declared_paths = manifest.get("paths")
    paths: dict[str, Any] = declared_paths if isinstance(declared_paths, dict) else {}

    def declared(key: str, default: Any) -> Any:
        """An absent or null manifest key falls back; an empty one is kept verbatim."""
        value = manifest.get(key)
        return default if value is None else value

    def read_index(key: str, default_name: str) -> list[Any]:
        relative = paths.get(key)
        if relative is None:
            relative = default_name
        if not relative:
            return []  # an index explicitly mapped to nothing is not read
        path = root / str(relative)
        if not path.is_file():
            return []
        values = read_yaml(path).get(key, [])
        return values if isinstance(values, list) else []

    data: dict[str, Any] = {
        "format_version": declared("format_version", FORMAT_VERSION),
        "sdk_version": declared("sdk_version", SDK_VERSION),
        "id": declared("id", ""),
        "title": declared("title", ""),
        "producer": manifest.get("producer"),
        "environment": manifest.get("environment"),
        "experiments": declared("experiments", []),
        "paper": manifest.get("paper"),
        "research_agent": manifest.get("research_agent"),
    }
    for key, default_name in _INDEXES:
        data[key] = read_index(key, default_name)

    reflection = root / "reflection.md"
    if reflection.is_file():
        with reflection.open("r", encoding="utf-8", newline="") as handle:
            data["reflection"] = handle.read()

    return artifact_from_dict(data)
