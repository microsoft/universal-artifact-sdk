"""Serialization (spec §5): turn the in-memory model into the on-disk layout.

The SDK serializes the **generated** index files (manifest, claims, results, datasets,
exhibits, traces, assessments, journal, per-experiment ``DISPOSITION.md`` markers) plus
``reflection.md`` — everything reconstructable from the model — and computes integrity
(``SHA256SUMS``, ``.sdk/state.json``). Blob files the producer places are **authored**:
the SDK copies them verbatim and never clobbers them. ``.sdk/state.json`` classifies each
file by that *nature*, independent of whether ``stage_from`` was passed on a given run.

Output is UTF-8 with ``\\n`` line endings, stable dictionary insertion order, stable list
order, and deterministic YAML settings, so re-emitting an unchanged artifact with this
package rewrites the same bytes. Cross-binding byte identity is explicitly not required.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from collections.abc import Iterable
from dataclasses import dataclass, field, replace
from io import StringIO
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.representer import SafeRepresenter

from .inventory import compute_evidence_inventory
from .model import Artifact, to_dict
from .validate import GENERATED_RESERVED_PATHS, Issue, StructuralError, validate_structure

GENERATED_MARKER = "artifact-sdk/v1 (universal-artifact-sdk) — do not edit; regenerate"

_GENERATED_RESERVED_BLOB_KEYS = {name.lower() for name in GENERATED_RESERVED_PATHS}
_DRIVE_LETTER = re.compile(r"^[A-Za-z]:")

# A plain scalar matching any of these would be resolved as a non-string by some
# conforming YAML parser (YAML 1.1 bools/sexagesimals/timestamps, YAML 1.2 core numbers
# and null). Quoting them keeps every value that is a string in the model a string in
# every binding that reads the file back. Anything else is emitted plain.
_AMBIGUOUS_SCALAR = re.compile(
    r"""(?x)
    ^(?:
        [-+]?(?:0b[01_]+|0o?[0-7_]+|[0-9][0-9_]*|0x[0-9a-fA-F_]+)            # integers
      | [-+]?(?:[0-9][0-9_]*)?\.[0-9_]*(?:[eE][-+]?[0-9]+)?                  # floats
      | [-+]?[0-9][0-9_]*(?:[eE][-+]?[0-9]+)                                 # exponents
      | [-+]?\.(?:inf|Inf|INF|nan|NaN|NAN)                                   # inf / nan
      | [-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+(?:\.[0-9_]*)?                     # sexagesimals
      | (?:true|True|TRUE|false|False|FALSE)                                 # 1.2 booleans
      | (?:yes|Yes|YES|no|No|NO|on|On|ON|off|Off|OFF|y|Y|n|N)                # 1.1 booleans
      | (?:null|Null|NULL|~)                                                 # nulls
      | [0-9]{4}-[0-9]{1,2}-[0-9]{1,2}(?:[Tt \t]+[0-9:.\t\ \-+Zz]*)?         # timestamps
    )$
    """
)


@dataclass
class WriteOptions:
    """Options accepted by :func:`write_submission`."""

    stage_from: str | Path | None = None
    quiet: bool = False


@dataclass
class SubmissionReport:
    """What :func:`write_submission` emitted, and what is still missing."""

    out_dir: str
    ok: bool
    incomplete: bool
    warnings: list[Issue] = field(default_factory=list)
    files_written: list[str] = field(default_factory=list)
    missing_blobs: list[str] = field(default_factory=list)


class _DeterministicRepresenter(SafeRepresenter):
    """Emit strings plain unless a conforming parser could resolve them as another type."""

    def represent_str(self, data: str) -> Any:
        ambiguous = data == "" or data.strip() != data or bool(_AMBIGUOUS_SCALAR.match(data))
        style = "'" if ambiguous else None
        return self.represent_scalar("tag:yaml.org,2002:str", data, style=style)


_DeterministicRepresenter.add_representer(str, _DeterministicRepresenter.represent_str)


def _yaml_writer() -> YAML:
    """A YAML 1.2 emitter with stable insertion order and no line wrapping."""
    yaml = YAML(typ="safe", pure=True)
    yaml.default_flow_style = False
    yaml.allow_unicode = True
    yaml.width = 2**31 - 1
    yaml.Representer = _DeterministicRepresenter
    # Insertion order is the SDK's contract; alphabetical output is not.
    yaml.representer.sort_base_mapping_type_on_output = False
    return yaml


def yaml_document(data: Any) -> str:
    """Render ``data`` as a deterministic YAML 1.2 document."""
    stream = StringIO()
    _yaml_writer().dump(data, stream)
    return stream.getvalue().replace("\r\n", "\n")


def _normalize_relative_path(value: str) -> str:
    """Collapse ``.`` and duplicate separators the way POSIX normalization does."""
    slash_path = value.replace("\\", "/")
    segments = [part for part in slash_path.split("/") if part not in ("", ".")]
    normalized = "/".join(segments)
    if slash_path.endswith("/") and normalized:
        normalized += "/"
    return normalized


def _safe_relative_path(value: str) -> str:
    """Reject anything that would escape the submission root, mirroring the write guard."""
    slash_path = value.replace("\\", "/")
    normalized = _normalize_relative_path(value)
    if (
        normalized in ("", ".", "..")
        or normalized.startswith("../")
        or slash_path.startswith("/")
        or _DRIVE_LETTER.match(value)
        or ".." in slash_path.split("/")
    ):
        raise ValueError(f"Refusing to write outside submission root: {value}")
    return normalized


def _write_text(root: Path, relative: str, content: str, written: list[str]) -> None:
    safe_relative = _safe_relative_path(relative)
    destination = root / safe_relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
    written.append(safe_relative)


def _walk_files(root: Path) -> list[str]:
    return sorted(
        path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()
    )


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _location_field(location: Any, key: str) -> Any:
    if isinstance(location, dict):
        return location.get(key)
    return getattr(location, key, None)


def _referenced_blobs(artifact: Artifact) -> list[str]:
    """Blob paths the model references, in stable first-seen order."""
    paths: dict[str, None] = {}

    def add(value: Any) -> None:
        if isinstance(value, str) and value:
            paths.setdefault(value, None)

    for dataset in artifact.datasets:
        location = dataset.location
        if _location_field(location, "kind") == "in_artifact":
            add(_location_field(location, "path"))
        if dataset.sample is not None:
            add(dataset.sample.path)
    for result in artifact.results:
        add(result.evidence)
    for exhibit in artifact.exhibits:
        add(exhibit.path)
        add(exhibit.source)
    for trace in artifact.traces:
        add(trace.path)
    if artifact.paper is not None:
        add(artifact.paper.pdf)
        add(artifact.paper.source)
        add(artifact.paper.claims_export)
        add(artifact.paper.references_export)
    agent = artifact.research_agent
    if agent is not None:
        add(agent.path)
        for source in agent.grounding_sources or []:
            if isinstance(source, str) and source.lower() not in _GENERATED_RESERVED_BLOB_KEYS:
                add(source)
    return list(paths)


def _stage_blobs(
    artifact: Artifact, root: Path, source_root: Path, staged: list[str]
) -> list[str]:
    """Copy referenced producer blobs in from ``source_root``; report what was absent."""
    missing: list[str] = []
    for relative in _referenced_blobs(artifact):
        safe_relative = _safe_relative_path(relative)
        origin = source_root / safe_relative
        if not origin.exists():
            missing.append(safe_relative)
            continue
        destination = root / safe_relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        # A staged file replaces an existing file, but a directory/file type mismatch is
        # refused: the destination may hold authored content the SDK must never delete,
        # and the frozen TypeScript `cpSync` refuses the same mismatch.
        if origin.is_dir():
            if destination.is_file():
                raise NotADirectoryError(
                    f"Refusing to replace the file {safe_relative} with a directory"
                )
            shutil.copytree(origin, destination, dirs_exist_ok=True)
            staged.extend(
                path.relative_to(root).as_posix()
                for path in destination.rglob("*")
                if path.is_file()
            )
        else:
            if destination.is_dir():
                raise IsADirectoryError(
                    f"Refusing to replace the directory {safe_relative} with a file"
                )
            shutil.copy2(origin, destination)
            staged.append(safe_relative)
    return missing


def _missing_blobs(artifact: Artifact, root: Path) -> list[str]:
    """Referenced blobs absent from the finished submission (→ incomplete warning)."""
    return [
        relative
        for relative in _referenced_blobs(artifact)
        if not (root / _safe_relative_path(relative)).exists()
    ]


def _disposition_marker(slug: str, disposition: Any) -> str:
    lines = [
        f"> **Auto-generated** by {GENERATED_MARKER}",
        "",
        f"# Experiment `{slug}` — {disposition.status}",
        "",
        f"**Status:** {disposition.status}",
    ]
    if disposition.superseded_by:
        lines.append(f"**Superseded by:** `{disposition.superseded_by}`")
    if disposition.failure:
        lines.append(
            f"**Failure:** {disposition.failure.stage} — {disposition.failure.summary}"
        )
    lines.extend(["", "## Rationale", "", disposition.rationale or "_(no rationale recorded)_", ""])
    return "\n".join(lines)


def _index_document(key: str, values: Iterable[Any]) -> str:
    return yaml_document({"_generated": GENERATED_MARKER, key: to_dict(list(values))})


def _build_manifest(artifact: Artifact, paths: dict[str, str]) -> dict[str, Any]:
    manifest: dict[str, Any] = {
        "_generated": GENERATED_MARKER,
        "format_version": artifact.format_version,
        "sdk_version": artifact.sdk_version,
        "id": artifact.id,
        "title": artifact.title,
    }
    if artifact.producer is not None:
        manifest["producer"] = to_dict(artifact.producer)
    if artifact.environment is not None:
        manifest["environment"] = to_dict(artifact.environment)
    manifest["experiments"] = to_dict(artifact.experiments)
    manifest["paths"] = paths
    if artifact.paper is not None:
        manifest["paper"] = to_dict(artifact.paper)
    if artifact.research_agent is not None:
        manifest["research_agent"] = to_dict(artifact.research_agent)
    manifest["evidence_inventory"] = to_dict(compute_evidence_inventory(artifact))
    return manifest


def write_submission(
    artifact: Artifact,
    out_dir: str | Path,
    options: WriteOptions | None = None,
    *,
    stage_from: str | Path | None = None,
    quiet: bool | None = None,
) -> SubmissionReport:
    """Validate, then write ``artifact`` into ``out_dir`` (spec §5).

    Raises :class:`StructuralError` before touching the output directory when structural
    errors exist. Options may be supplied as a :class:`WriteOptions` value or as keyword
    arguments; explicit keywords win. The caller's ``options`` value is never mutated.
    """
    resolved = replace(options) if options is not None else WriteOptions()
    if stage_from is not None:
        resolved.stage_from = stage_from
    if quiet is not None:
        resolved.quiet = quiet

    report = validate_structure(artifact)
    if not report.ok:
        raise StructuralError(report.errors)

    root = Path(out_dir)
    root.mkdir(parents=True, exist_ok=True)

    # Two ledgers, split by the *nature* of the file rather than by what this run touched:
    # `written` holds files serialized from the model (→ generated_files) and `staged`
    # holds producer blobs copied in verbatim (→ authored_files, never clobbered).
    written: list[str] = []
    staged: list[str] = []

    # 0. stage producer blobs if a source root was given
    stage_missing = (
        _stage_blobs(artifact, root, Path(resolved.stage_from), staged)
        if resolved.stage_from is not None
        else []
    )

    # 1. reflection (authored in nature, but the model may carry seed text)
    if artifact.reflection is not None:
        _write_text(root, "reflection.md", artifact.reflection, written)

    # 2. generated index files
    paths: dict[str, str] = {
        "claims": "claims.yml",
        "results": "results.yml",
        "datasets": "datasets.yml",
    }
    if artifact.traces:
        paths["traces"] = "traces.yml"
    if artifact.exhibits:
        paths["exhibits"] = "exhibits.yml"
    if artifact.assessments:
        paths["assessments"] = "assessments.yml"
    if artifact.journal:
        paths["journal"] = "journal.yml"

    _write_text(root, "manifest.yml", yaml_document(_build_manifest(artifact, paths)), written)
    _write_text(root, "claims.yml", _index_document("claims", artifact.claims), written)
    _write_text(root, "results.yml", _index_document("results", artifact.results), written)
    _write_text(root, "datasets.yml", _index_document("datasets", artifact.datasets), written)
    for filename, key, values in (
        ("exhibits.yml", "exhibits", artifact.exhibits),
        ("traces.yml", "traces", artifact.traces),
        ("assessments.yml", "assessments", artifact.assessments),
        ("journal.yml", "journal", artifact.journal),
    ):
        if values:
            _write_text(root, filename, _index_document(key, values), written)

    # 2b. per-experiment disposition markers for non-active experiments (spec §2.2.2)
    for experiment in artifact.experiments:
        disposition = experiment.disposition
        if not disposition or disposition.status == "active":
            continue
        _write_text(
            root,
            f"{experiment.directory}/DISPOSITION.md",
            _disposition_marker(experiment.slug, disposition),
            written,
        )

    # 3. integrity: SHA256SUMS over every shipped file, then .sdk/state.json
    generated = set(written)
    shipped = [
        path
        for path in _walk_files(root)
        if path != "SHA256SUMS" and not path.startswith(".sdk/")
    ]
    sums = "\n".join(f"{_sha256_file(root / path)}  {path}" for path in shipped) + "\n"
    _write_text(root, "SHA256SUMS", sums, written)

    authored = {path: _sha256_file(root / path) for path in shipped if path not in generated}
    state = {
        "_generated": GENERATED_MARKER,
        "sdk_version": artifact.sdk_version,
        "generated_files": sorted(generated),
        "authored_files": authored,
    }
    _write_text(
        root, ".sdk/state.json", json.dumps(state, indent=2, ensure_ascii=False) + "\n", written
    )

    missing = sorted(set(stage_missing) | set(_missing_blobs(artifact, root)))
    warnings = list(report.warnings) + [
        Issue(f"blob[{path}]", "referenced file not present in submission (incomplete)")
        for path in missing
    ]
    return SubmissionReport(
        out_dir=str(out_dir),
        ok=True,
        # `quiet` only clears the flag: warnings and missing blobs are still reported.
        incomplete=not resolved.quiet and len(warnings) > 0,
        warnings=warnings,
        files_written=sorted(set(written) | set(staged)),
        missing_blobs=missing,
    )
