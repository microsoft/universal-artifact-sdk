"""Export parity between the two bindings, and the public surface itself.

``PYTHON_BINDING.md`` §12 requires that every public TypeScript export representing
language-neutral SDK behavior has an idiomatic Python equivalent, "verified by a
maintained export-parity inventory". :data:`EXPORT_PARITY` is that inventory: it is
asserted to be exhaustive against the frozen TypeScript sources, so adding or renaming a
TypeScript export fails this test until the inventory is updated.
"""

from __future__ import annotations

import importlib
import inspect
import re
from pathlib import Path

import pytest

import universal_artifact_sdk as sdk

REPO_ROOT = Path(__file__).resolve().parents[2]
TS_SOURCE = REPO_ROOT / "src"
_TS_EXPORT = re.compile(
    r"^export\s+(?:declare\s+)?(?:async\s+)?(?:function|interface|type|const|class)\s+"
    r"([A-Za-z_][A-Za-z0-9_]*)",
    re.MULTILINE,
)

#: TypeScript export -> Python export. ``None`` records a deliberate, justified omission.
EXPORT_PARITY: dict[str, str | None] = {
    # constants
    "SDK_VERSION": "SDK_VERSION",
    "FORMAT_VERSION": "FORMAT_VERSION",
    "VALIDATION_MODES": "VALIDATION_MODES",
    "DISPOSITION_STATUSES": "DISPOSITION_STATUSES",
    "EXHIBIT_TYPES": "EXHIBIT_TYPES",
    "CLAIM_STANCES": "CLAIM_STANCES",
    "DEFAULT_CLAIM_STANCE": "DEFAULT_CLAIM_STANCE",
    # type aliases and open vocabularies
    "ValidationMode": "ValidationMode",
    "DispositionStatus": "DispositionStatus",
    "ClaimStance": "ClaimStance",
    "RationalePolicy": "RationalePolicy",
    "JournalOp": "JournalOp",
    "ResultKind": "ResultKind",
    "ExhibitType": "ExhibitType",
    "BuiltinCheck": "BuiltinCheck",
    "Locator": "Locator",
    "DatasetLocation": "DatasetLocation",
    "Validator": "Validator",
    # models
    "Artifact": "Artifact",
    "Environment": "Environment",
    "StudyMetadata": "StudyMetadata",
    "Dataset": "Dataset",
    "RunSpec": "RunSpec",
    "Experiment": "Experiment",
    "Disposition": "Disposition",
    "Trace": "Trace",
    "QualitativeSupport": "QualitativeSupport",
    "Result": "Result",
    "Exhibit": "Exhibit",
    "Claim": "Claim",
    "Assessment": "Assessment",
    "Paper": "Paper",
    "ResearchAgent": "ResearchAgent",
    "JournalTarget": "JournalTarget",
    "JournalEntry": "JournalEntry",
    "JournalConfig": "JournalConfig",
    "PendingChange": "PendingChange",
    "ChangeContext": "ChangeContext",
    "AddClaimInput": "AddClaimInput",
    "BuiltinValidator": "BuiltinValidator",
    "ProcedureValidator": "ProcedureValidator",
    "AttestValidator": "AttestValidator",
    "LlmJudgeValidator": "LlmJudgeValidator",
    "EvidenceInventory": "EvidenceInventory",
    "Issue": "Issue",
    "ValidationReport": "ValidationReport",
    "StructuralError": "StructuralError",
    "WriteOptions": "WriteOptions",
    "SubmissionReport": "SubmissionReport",
    # `createArtifact` takes keyword arguments in Python, so the input interface has no
    # Python counterpart; its fields are the signature of `create_artifact`.
    "CreateArtifactInput": None,
    # authoring
    "createArtifact": "create_artifact",
    "configureJournal": "configure_journal",
    "listJournal": "list_journal",
    "addEnvironment": "add_environment",
    "addDataset": "add_dataset",
    "getDataset": "get_dataset",
    "listDatasets": "list_datasets",
    "removeDataset": "remove_dataset",
    "addExperiment": "add_experiment",
    "getExperiment": "get_experiment",
    "listExperiments": "list_experiments",
    "listAbandonedExperiments": "list_abandoned_experiments",
    "removeExperiment": "remove_experiment",
    "abandonExperiment": "abandon_experiment",
    "failExperiment": "fail_experiment",
    "supersedeExperiment": "supersede_experiment",
    "purgeExperiment": "purge_experiment",
    "addTrace": "add_trace",
    "getTrace": "get_trace",
    "listTraces": "list_traces",
    "removeTrace": "remove_trace",
    "addResult": "add_result",
    "getResult": "get_result",
    "listResults": "list_results",
    "removeResult": "remove_result",
    "addExhibit": "add_exhibit",
    "getExhibit": "get_exhibit",
    "listExhibits": "list_exhibits",
    "removeExhibit": "remove_exhibit",
    "addClaim": "add_claim",
    "getClaim": "get_claim",
    "listClaims": "list_claims",
    "removeClaim": "remove_claim",
    "addAssessment": "add_assessment",
    "getAssessment": "get_assessment",
    "listAssessments": "list_assessments",
    "removeAssessment": "remove_assessment",
    "attachPaper": "attach_paper",
    "attachResearchAgent": "attach_research_agent",
    "setReflection": "set_reflection",
    # helpers, validation, inventory, serialization, reopening
    "pinnedDigest": "pinned_digest",
    "defaultValidationMode": "default_validation_mode",
    "defaultExhibitValidationMode": "default_exhibit_validation_mode",
    "validateStructure": "validate_structure",
    "computeEvidenceInventory": "compute_evidence_inventory",
    "writeSubmission": "write_submission",
    "openSubmission": "open_submission",
}

#: Python exports with no TypeScript counterpart, and why each one exists.
PYTHON_ONLY_EXPORTS: dict[str, str] = {
    "BUILTIN_CHECKS": "documents the open BuiltinCheck vocabulary TypeScript states inline",
    "RESULT_KINDS": "documents the open ResultKind vocabulary TypeScript states inline",
    "TRACE_KINDS": "documents the open Trace kind vocabulary TypeScript states inline",
    "GENERATED_MARKER": "the marker TypeScript keeps module-private but Python tests assert",
    "GENERATED_RESERVED_PATHS": "the reserved-path list, shared by validation and serialization",
    "TraceKind": "type alias for the open trace vocabulary",
    "Image": "named dataclass for an inline TypeScript object type",
    "Hardware": "named dataclass for an inline TypeScript object type",
    "Sample": "named dataclass for an inline TypeScript object type",
    "DataUse": "named dataclass for an inline TypeScript object type",
    "Failure": "named dataclass for an inline TypeScript object type",
    "PaperReference": "named dataclass for an inline TypeScript object type",
    "ProcedureTool": "named dataclass for an inline TypeScript object type",
    "QualitativeExcerpt": "named dataclass for an inline TypeScript object type",
    "InterRaterReliability": "named dataclass for an inline TypeScript object type",
    "InArtifactLocation": "named dataclass for a DatasetLocation union member",
    "InContainerLocation": "named dataclass for a DatasetLocation union member",
    "ExternalLocation": "named dataclass for a DatasetLocation union member",
    "artifact_from_dict": "dataclasses need an explicit constructor from plain data",
    "validator_from_dict": "dataclasses need an explicit constructor from plain data",
    "to_dict": "dataclasses need an explicit conversion to schema-shaped data",
    "read_yaml": "reading an index with the binding's YAML 1.2 core settings",
    "yaml_document": "rendering a document with the binding's deterministic YAML settings",
    "canonical_schema_path": "locating the schema packaged as Python package data",
}


def typescript_exports() -> set[str]:
    names: set[str] = set()
    for path in sorted(TS_SOURCE.glob("*.ts")):
        names.update(_TS_EXPORT.findall(path.read_text(encoding="utf-8")))
    return names


class TestExportParity:
    def test_the_inventory_covers_every_typescript_export(self) -> None:
        missing = typescript_exports() - set(EXPORT_PARITY)
        assert missing == set(), f"unmapped TypeScript exports: {sorted(missing)}"

    def test_the_inventory_has_no_stale_entries(self) -> None:
        stale = set(EXPORT_PARITY) - typescript_exports()
        assert stale == set(), f"inventory entries with no TypeScript export: {sorted(stale)}"

    @pytest.mark.parametrize(
        ("ts_name", "py_name"),
        sorted((k, v) for k, v in EXPORT_PARITY.items() if v is not None),
    )
    def test_each_mapped_export_exists(self, ts_name: str, py_name: str) -> None:
        assert py_name in sdk.__all__, f"{ts_name} maps to missing export {py_name}"
        assert hasattr(sdk, py_name)

    def test_python_only_exports_are_documented(self) -> None:
        mapped = {value for value in EXPORT_PARITY.values() if value is not None}
        extra = set(sdk.__all__) - mapped
        assert extra == set(PYTHON_ONLY_EXPORTS), (
            "undocumented Python-only exports: "
            f"{sorted(extra - set(PYTHON_ONLY_EXPORTS))}; "
            f"documented but absent: {sorted(set(PYTHON_ONLY_EXPORTS) - extra)}"
        )

    def test_no_camel_case_aliases_are_exported(self) -> None:
        camel = [
            name
            for name in sdk.__all__
            if name[0].islower() and re.search(r"[a-z][A-Z]", name)
        ]
        assert camel == []


class TestPublicSurface:
    def test_all_entries_are_unique(self) -> None:
        duplicates = sorted({n for n in sdk.__all__ if sdk.__all__.count(n) > 1})
        assert duplicates == []

    def test_all_is_grouped_into_sorted_runs(self) -> None:
        # `__all__` is maintained in commented sections, each kept in sorted order.
        runs: list[list[str]] = [[]]
        for name in sdk.__all__:
            if runs[-1] and name < runs[-1][-1]:
                runs.append([])
            runs[-1].append(name)
        assert len(runs) <= 6, [run[0] for run in runs]
        for run in runs:
            assert run == sorted(run)

    def test_every_name_in_all_is_importable(self) -> None:
        module = importlib.import_module("universal_artifact_sdk")
        for name in sdk.__all__:
            assert hasattr(module, name), name

    def test_all_matches_the_module_namespace(self) -> None:
        public = {
            name
            for name in vars(sdk)
            if not name.startswith("_")
            and not inspect.ismodule(getattr(sdk, name))
        }
        assert public == set(sdk.__all__)

    def test_the_package_is_typed(self) -> None:
        marker = Path(sdk.__file__).resolve().parent / "py.typed"
        assert marker.is_file()

    def test_mutating_functions_accept_a_keyword_only_change_context(self) -> None:
        for name in sdk.__all__:
            if not name.startswith(("add_", "remove_", "attach_", "set_", "abandon_", "fail_",
                                    "supersede_", "purge_")):
                continue
            signature = inspect.signature(getattr(sdk, name))
            parameter = signature.parameters.get("ctx")
            assert parameter is not None, name
            assert parameter.kind is inspect.Parameter.KEYWORD_ONLY, name
            assert parameter.default is None, name

    def test_create_artifact_is_keyword_only(self) -> None:
        signature = inspect.signature(sdk.create_artifact)
        assert [p.kind for p in signature.parameters.values()] == [
            inspect.Parameter.KEYWORD_ONLY
        ] * 3
