"""Shared conformance harness — Python side.

Runs the language-neutral cases under ``parity/cases`` against the native Python binding
and reduces each run to a *normalized observation*: validation severities and paths, the
write report, the on-disk ledger, the emitted documents, the in-memory model, and the
model reopened from the binding's own output.

Observations are the unit of cross-binding comparison (``PYTHON_BINDING.md`` §8):
semantic equivalence, not byte identity. Normalization therefore erases the differences
the contract allows — binding-dependent hashes, integral ``1`` vs ``1.0``, an explicit
``null`` vs an omitted optional *model field*, and key insertion order — and nothing
else. A null value inside an opaque producer-authored map is not such a difference; the
``read_document`` operation marks those nulls so they survive normalization.
"""

from __future__ import annotations

import json
import shutil
from collections.abc import Callable
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator

from universal_artifact_sdk import (
    AddClaimInput,
    Artifact,
    ChangeContext,
    Environment,
    Failure,
    Paper,
    PendingChange,
    ResearchAgent,
    abandon_experiment,
    add_assessment,
    add_claim,
    add_dataset,
    add_environment,
    add_exhibit,
    add_experiment,
    add_result,
    add_trace,
    artifact_from_dict,
    attach_paper,
    attach_research_agent,
    canonical_schema_path,
    compute_evidence_inventory,
    configure_journal,
    create_artifact,
    default_exhibit_validation_mode,
    default_validation_mode,
    fail_experiment,
    get_assessment,
    get_claim,
    get_dataset,
    get_exhibit,
    get_experiment,
    get_result,
    get_trace,
    list_abandoned_experiments,
    list_assessments,
    list_claims,
    list_datasets,
    list_exhibits,
    list_experiments,
    list_journal,
    list_results,
    list_traces,
    open_submission,
    pinned_digest,
    purge_experiment,
    read_yaml,
    remove_assessment,
    remove_claim,
    remove_dataset,
    remove_exhibit,
    remove_experiment,
    remove_result,
    remove_trace,
    set_reflection,
    supersede_experiment,
    to_dict,
    validate_structure,
    write_submission,
)

PARITY_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PARITY_ROOT.parent
CASES_DIR = PARITY_ROOT / "cases"
SCRATCH_DIR = PARITY_ROOT / ".scratch"
FIXTURES_DIR = PARITY_ROOT / "fixtures"
HASH_PLACEHOLDER = "<sha256>"
NULL_PLACEHOLDER = "<null>"

_INDEX_DOCUMENTS = (
    "manifest.yml",
    "claims.yml",
    "results.yml",
    "datasets.yml",
    "exhibits.yml",
    "traces.yml",
    "assessments.yml",
    "journal.yml",
)


# --- normalization ----------------------------------------------------------


def normalize(value: Any) -> Any:
    """Reduce parsed data to the cross-binding comparable form."""
    if isinstance(value, bool):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if item is None:
                continue  # an explicit null is equivalent to an omitted optional field
            normalized = normalize(item)
            if isinstance(normalized, (list, dict)) and len(normalized) == 0:
                continue  # an empty collection is equivalent to an omitted one
            result[str(key)] = normalized
        return result
    return value


def normalize_model(artifact: Artifact) -> Any:
    return normalize(to_dict(artifact))


def mark_nulls(value: Any) -> Any:
    """Replace every explicit null with :data:`NULL_PLACEHOLDER`.

    Normalization treats a null as an omitted optional field, which is the reviewed
    divergence for *model fields* only. A null **value inside an opaque producer-authored
    map** — ``producer``, ``run.env``, ``counters``, ``locators``, a validator's
    ``input``/``params`` — is data both bindings must keep, so ``read_document`` marks it
    and the marker survives normalization.
    """
    if value is None:
        return NULL_PLACEHOLDER
    if isinstance(value, list):
        return [mark_nulls(item) for item in value]
    if isinstance(value, dict):
        return {key: mark_nulls(item) for key, item in value.items()}
    return value


def select(value: Any, path: list[Any]) -> Any:
    """Walk a document by a key/index path, e.g. ``["experiments", 0, "run", "env"]``."""
    for key in path:
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def canonical(value: Any) -> str:
    """A stable, key-order-insensitive rendering used for comparison and diagnostics."""
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False)


def _normalize_sums(text: str) -> list[str]:
    lines = []
    for line in text.splitlines():
        if not line.strip():
            continue
        _, _, path = line.partition("  ")
        lines.append(f"{HASH_PLACEHOLDER}  {path}")
    return sorted(lines)


def _read_state(out_dir: Path) -> dict[str, Any]:
    state_path = out_dir / ".sdk" / "state.json"
    if not state_path.is_file():
        return {}
    state = json.loads(state_path.read_text(encoding="utf-8"))
    return {
        "generated_files": sorted(state.get("generated_files", [])),
        "authored_files": sorted(state.get("authored_files", {}).keys()),
    }


def observe_output(out_dir: Path) -> dict[str, Any]:
    """Reduce a written submission directory to its normalized observation."""
    files = sorted(
        path.relative_to(out_dir).as_posix() for path in out_dir.rglob("*") if path.is_file()
    )
    documents = {
        name: normalize(read_yaml(out_dir / name))
        for name in _INDEX_DOCUMENTS
        if (out_dir / name).is_file()
    }
    markers = {
        path: (out_dir / path).read_text(encoding="utf-8")
        for path in files
        if path.endswith("DISPOSITION.md")
    }
    reflection_path = out_dir / "reflection.md"
    observation: dict[str, Any] = {
        "files": files,
        "state": _read_state(out_dir),
        "sums": _normalize_sums((out_dir / "SHA256SUMS").read_text(encoding="utf-8"))
        if (out_dir / "SHA256SUMS").is_file()
        else [],
        "documents": documents,
        "disposition_markers": markers,
    }
    if reflection_path.is_file():
        observation["reflection"] = reflection_path.read_text(encoding="utf-8")
    return observation


def observe_report(report: Any) -> dict[str, Any]:
    return {
        "ok": report.ok,
        "incomplete": report.incomplete,
        "warning_paths": [issue.path for issue in report.warnings],
        "files_written": sorted(report.files_written),
        "missing_blobs": sorted(report.missing_blobs),
    }


def observe_schema(artifact_data: dict[str, Any]) -> dict[str, Any]:
    """Validate raw case data against the canonical draft-07 schema (§6.1)."""
    schema = json.loads(canonical_schema_path().read_text(encoding="utf-8"))
    errors = list(Draft7Validator(schema).iter_errors(artifact_data))
    paths = sorted(
        {"/" + "/".join(str(part) for part in error.absolute_path) for error in errors}
    )
    return {"valid": len(errors) == 0, "paths": paths}


def observe_validation(report: Any) -> dict[str, Any]:
    return {
        "ok": report.ok,
        "error_paths": [issue.path for issue in report.errors],
        "warning_paths": [issue.path for issue in report.warnings],
    }


# --- operation dispatch -----------------------------------------------------


class _Session:
    """Mutable state threaded through an operation case's steps."""

    def __init__(self, out_root: Path) -> None:
        self.out_root = out_root
        self.artifact: Artifact | None = None
        self.now_values: list[str] = ["1970-01-01T00:00:00.000Z"]
        self.now_index = 0
        self.prompt_rationale = ""

    @property
    def current(self) -> Artifact:
        if self.artifact is None:
            raise ValueError("operation case: create_artifact must run first")
        return self.artifact

    def clock(self) -> str:
        value = self.now_values[min(self.now_index, len(self.now_values) - 1)]
        self.now_index += 1
        return value

    def resolve(self, relative: str) -> Path:
        return self.out_root / relative


def _context(step: dict[str, Any]) -> ChangeContext | None:
    context = step.get("context")
    if not context:
        return None
    return ChangeContext(actor=context.get("actor"), rationale=context.get("rationale"))


def _element(collection: str, args: dict[str, Any]) -> Any:
    """Rebuild one collection element from case data, preserving nested extensions."""
    holder = artifact_from_dict({collection: [args]})
    return getattr(holder, collection)[0]


def _environment(args: dict[str, Any]) -> Environment:
    environment = artifact_from_dict({"environment": args}).environment
    if environment is None:
        raise ValueError("add_environment: an environment object is required")
    return environment


def _paper(args: dict[str, Any]) -> Paper:
    paper = artifact_from_dict({"paper": args}).paper
    if paper is None:
        raise ValueError("attach_paper: a paper object is required")
    return paper


def _research_agent(args: dict[str, Any]) -> ResearchAgent:
    agent = artifact_from_dict({"research_agent": args}).research_agent
    if agent is None:
        raise ValueError("attach_research_agent: a research agent object is required")
    return agent


def _claim_input(args: dict[str, Any]) -> AddClaimInput:
    """Map case arguments onto the language-neutral add_claim input (spec §2.4)."""
    claim = _element("claims", {**args, "validators": args.get("validators") or []})
    validator = None
    if args.get("validator") is not None:
        holder = _element(
            "claims", {"id": "x", "statement": "x", "validators": [args["validator"]]}
        )
        validator = holder.validators[0]
    return AddClaimInput(
        id=claim.id,
        statement=claim.statement,
        validators=list(claim.validators) if args.get("validators") is not None else None,
        validator=validator,
        stance=claim.stance,
        tested_by=claim.tested_by,
        paper_ref=claim.paper_ref,
    )


def _operations() -> dict[str, Callable[[_Session, dict[str, Any], dict[str, Any]], Any]]:
    def create(session: _Session, args: dict[str, Any], step: dict[str, Any]) -> Any:
        session.artifact = create_artifact(
            id=args["id"], title=args["title"], producer=args.get("producer")
        )
        return None

    def configure(session: _Session, args: dict[str, Any], step: dict[str, Any]) -> Any:
        if args.get("now"):
            session.now_values = list(args["now"])
            session.now_index = 0
        session.prompt_rationale = args.get("prompt_rationale", "")

        def on_missing(change: PendingChange) -> str:
            return f"{session.prompt_rationale}" if session.prompt_rationale else ""

        configure_journal(
            session.current,
            policy=args.get("policy"),
            actor=args.get("actor"),
            on_missing_rationale=on_missing if args.get("prompt_rationale") is not None else None,
            now=session.clock,
        )
        return None

    def prepare_file(session: _Session, args: dict[str, Any], step: dict[str, Any]) -> Any:
        target = session.resolve(args["path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(args.get("content", ""), encoding="utf-8")
        return None

    def read_file(session: _Session, args: dict[str, Any], step: dict[str, Any]) -> Any:
        return session.resolve(args["path"]).read_text(encoding="utf-8")

    def read_document(session: _Session, args: dict[str, Any], step: dict[str, Any]) -> Any:
        """Parse an emitted YAML document, keeping explicit nulls observable."""
        document = read_yaml(session.resolve(args["path"]))
        return mark_nulls(select(document, list(args.get("select") or [])))

    def write(session: _Session, args: dict[str, Any], step: dict[str, Any]) -> Any:
        stage_from = args.get("stage_from")
        report = write_submission(
            session.current,
            session.resolve(args.get("out", "out")),
            stage_from=str(PARITY_ROOT / stage_from) if stage_from else None,
            quiet=args.get("quiet"),
        )
        return observe_report(report)

    def reopen(session: _Session, args: dict[str, Any], step: dict[str, Any]) -> Any:
        artifact = open_submission(session.resolve(args.get("out", "out")))
        if args.get("into_session"):
            # Continue the script from the reopened artifact, so a later write exercises
            # the reopen → write round trip.
            session.artifact = artifact
        return normalize_model(artifact)

    def validate(session: _Session, args: dict[str, Any], step: dict[str, Any]) -> Any:
        return observe_validation(validate_structure(session.current))

    def inventory(session: _Session, args: dict[str, Any], step: dict[str, Any]) -> Any:
        return normalize(to_dict(compute_evidence_inventory(session.current)))

    return {
        "create_artifact": create,
        "default_validation_mode": lambda s, a, st: default_validation_mode(a["kind"]),
        "default_exhibit_validation_mode": lambda s, a, st: default_exhibit_validation_mode(
            a["type"]
        ),
        "pinned_digest": lambda s, a, st: pinned_digest(a["reference"]),
        "configure_journal": configure,
        "prepare_file": prepare_file,
        "read_file": read_file,
        "read_document": read_document,
        "write_submission": write,
        "open_submission": reopen,
        "validate_structure": validate,
        "compute_evidence_inventory": inventory,
        "add_environment": lambda s, a, st: normalize(
            to_dict(add_environment(s.current, _environment(a), ctx=_context(st)))
        ),
        "add_dataset": lambda s, a, st: normalize(
            to_dict(add_dataset(s.current, _element("datasets", a), ctx=_context(st)))
        ),
        "add_experiment": lambda s, a, st: normalize(
            to_dict(add_experiment(s.current, _element("experiments", a), ctx=_context(st)))
        ),
        "add_trace": lambda s, a, st: normalize(
            to_dict(add_trace(s.current, _element("traces", a), ctx=_context(st)))
        ),
        "add_result": lambda s, a, st: normalize(
            to_dict(add_result(s.current, _element("results", a), ctx=_context(st)))
        ),
        "add_exhibit": lambda s, a, st: normalize(
            to_dict(add_exhibit(s.current, _element("exhibits", a), ctx=_context(st)))
        ),
        "add_claim": lambda s, a, st: normalize(
            to_dict(add_claim(s.current, _claim_input(a), ctx=_context(st)))
        ),
        "add_assessment": lambda s, a, st: normalize(
            to_dict(add_assessment(s.current, _element("assessments", a), ctx=_context(st)))
        ),
        "attach_paper": lambda s, a, st: normalize(
            to_dict(attach_paper(s.current, _paper(a), ctx=_context(st)))
        ),
        "attach_research_agent": lambda s, a, st: normalize(
            to_dict(attach_research_agent(s.current, _research_agent(a), ctx=_context(st)))
        ),
        "set_reflection": lambda s, a, st: set_reflection(
            s.current, a["markdown"], ctx=_context(st)
        ),
        "abandon_experiment": lambda s, a, st: normalize(
            to_dict(abandon_experiment(s.current, a["slug"], ctx=_context(st)))
        ),
        "fail_experiment": lambda s, a, st: normalize(
            to_dict(
                fail_experiment(
                    s.current, a["slug"], Failure(**a["failure"]), ctx=_context(st)
                )
            )
        ),
        "supersede_experiment": lambda s, a, st: normalize(
            to_dict(
                supersede_experiment(
                    s.current, a["slug"], a["superseded_by"], ctx=_context(st)
                )
            )
        ),
        "purge_experiment": lambda s, a, st: purge_experiment(
            s.current, a["slug"], ctx=_context(st)
        ),
        "remove_experiment": lambda s, a, st: remove_experiment(
            s.current, a["slug"], ctx=_context(st)
        ),
        "remove_dataset": lambda s, a, st: remove_dataset(s.current, a["id"], ctx=_context(st)),
        "remove_trace": lambda s, a, st: remove_trace(s.current, a["id"], ctx=_context(st)),
        "remove_result": lambda s, a, st: remove_result(s.current, a["id"], ctx=_context(st)),
        "remove_exhibit": lambda s, a, st: remove_exhibit(s.current, a["id"], ctx=_context(st)),
        "remove_claim": lambda s, a, st: remove_claim(s.current, a["id"], ctx=_context(st)),
        "remove_assessment": lambda s, a, st: remove_assessment(
            s.current, a["id"], ctx=_context(st)
        ),
        "get_dataset": lambda s, a, st: normalize(to_dict(get_dataset(s.current, a["id"]))),
        "get_experiment": lambda s, a, st: normalize(
            to_dict(get_experiment(s.current, a["slug"]))
        ),
        "get_trace": lambda s, a, st: normalize(to_dict(get_trace(s.current, a["id"]))),
        "get_result": lambda s, a, st: normalize(to_dict(get_result(s.current, a["id"]))),
        "get_exhibit": lambda s, a, st: normalize(to_dict(get_exhibit(s.current, a["id"]))),
        "get_claim": lambda s, a, st: normalize(to_dict(get_claim(s.current, a["id"]))),
        "get_assessment": lambda s, a, st: normalize(
            to_dict(get_assessment(s.current, a["id"]))
        ),
        "list_datasets": lambda s, a, st: normalize(to_dict(list_datasets(s.current))),
        "list_experiments": lambda s, a, st: normalize(to_dict(list_experiments(s.current))),
        "list_abandoned_experiments": lambda s, a, st: normalize(
            to_dict(list_abandoned_experiments(s.current))
        ),
        "list_traces": lambda s, a, st: normalize(to_dict(list_traces(s.current))),
        "list_results": lambda s, a, st: normalize(to_dict(list_results(s.current))),
        "list_exhibits": lambda s, a, st: normalize(to_dict(list_exhibits(s.current))),
        "list_claims": lambda s, a, st: normalize(to_dict(list_claims(s.current))),
        "list_assessments": lambda s, a, st: normalize(to_dict(list_assessments(s.current))),
        "list_journal": lambda s, a, st: normalize(to_dict(list_journal(s.current))),
    }


OPERATIONS = _operations()


# --- case execution ---------------------------------------------------------


def load_cases() -> list[dict[str, Any]]:
    """Load every reviewed case, in stable filename order."""
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(CASES_DIR.glob("*.json"))
    ]


def case_out_dir(root: Path, case: dict[str, Any]) -> Path:
    return root / case["name"]


def run_case(case: dict[str, Any], root: Path) -> dict[str, Any]:
    """Execute one case and return its normalized observation."""
    out_root = case_out_dir(root, case)
    shutil.rmtree(out_root, ignore_errors=True)
    out_root.mkdir(parents=True, exist_ok=True)
    if case["kind"] == "artifact":
        return _run_artifact_case(case, out_root)
    return _run_operation_case(case, out_root)


def _run_artifact_case(case: dict[str, Any], out_root: Path) -> dict[str, Any]:
    artifact = artifact_from_dict(case["artifact"])
    report = validate_structure(artifact)
    observation: dict[str, Any] = {
        "name": case["name"],
        "kind": "artifact",
        "validation": observe_validation(report),
        "schema": observe_schema(case["artifact"]),
        "model": normalize_model(artifact),
    }
    if not report.ok:
        return observation
    write_options = case.get("write", {})
    stage_from = write_options.get("stage_from")
    out_dir = out_root / "out"
    result = write_submission(
        artifact,
        out_dir,
        stage_from=str(PARITY_ROOT / stage_from) if stage_from else None,
        quiet=write_options.get("quiet", False),
    )
    observation["write"] = observe_report(result)
    observation["output"] = observe_output(out_dir)
    observation["reopened"] = normalize_model(open_submission(out_dir))
    # A write → open → write round trip is idempotent within a binding (§8.7).
    reopened_dir = out_root / "reopened"
    reopened_dir.mkdir(parents=True, exist_ok=True)
    for name in observation["output"]["files"]:
        source = out_dir / name
        target = reopened_dir / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    write_submission(open_submission(reopened_dir), reopened_dir)
    observation["idempotent"] = observe_output(reopened_dir)["documents"] == (
        observation["output"]["documents"]
    )
    return observation


def _run_operation_case(case: dict[str, Any], out_root: Path) -> dict[str, Any]:
    session = _Session(out_root)
    steps: list[dict[str, Any]] = []
    for index, step in enumerate(case["operations"]):
        name = step["operation"]
        handler = OPERATIONS.get(name)
        if handler is None:
            raise ValueError(f"{case['name']}: unknown operation '{name}'")
        record: dict[str, Any] = {"index": index, "operation": name}
        try:
            record["returned"] = normalize(handler(session, step.get("arguments", {}), step))
        except Exception as error:  # noqa: BLE001 - the case declares the expectation
            record["raised"] = True
            if not step.get("expects_error"):
                raise AssertionError(
                    f"{case['name']} step {index} ({name}) raised unexpectedly: {error}"
                ) from error
        else:
            if step.get("expects_error"):
                raise AssertionError(
                    f"{case['name']} step {index} ({name}) was expected to raise"
                )
        steps.append(record)
    observation: dict[str, Any] = {
        "name": case["name"],
        "kind": "operation",
        "steps": steps,
        "model": normalize_model(session.current),
        "validation": observe_validation(validate_structure(session.current)),
    }
    out_dir = out_root / "out"
    if (out_dir / "manifest.yml").is_file():
        observation["output"] = observe_output(out_dir)
        observation["reopened"] = normalize_model(open_submission(out_dir))
    return observation
