"""Shared cross-binding conformance cases, run against the Python binding.

The same case files drive ``parity/run-ts.mjs``. This module is the Python half of the
corpus and needs no Node.js, so the Python CI job runs it directly; the parity CI job
additionally runs both runners' ``cross-open`` phase, which asserts that each binding
reopens the other's output into the same normalized model.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft7Validator

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "parity"))

from harness import (  # noqa: E402
    CASES_DIR,
    canonical,
    load_cases,
    normalize,
    run_case,
)

sys.path.insert(0, str(REPO_ROOT / "parity"))

from run_py import check_expectations  # noqa: E402

CASES = load_cases()
CASE_IDS = [case["name"] for case in CASES]
CASE_SCHEMA = json.loads((REPO_ROOT / "parity" / "case.schema.json").read_text(encoding="utf-8"))


@pytest.fixture(params=CASES, ids=CASE_IDS)
def case(request: pytest.FixtureRequest) -> dict[str, Any]:
    return request.param


def test_the_corpus_is_not_empty() -> None:
    assert len(CASES) >= 10
    assert len(set(CASE_IDS)) == len(CASE_IDS)


def test_the_corpus_covers_every_required_category() -> None:
    # PYTHON_BINDING.md §8 lists the initial corpus categories.
    required = {
        "complete-worked-example",
        "minimal-empty-artifact",
        "partial-artifact-warnings",
        "referential-failure",
        "unsafe-paths",
        "reserved-collisions",
        "nested-extensions",
        "ambiguous-yaml-scalars",
        "schema-runtime-divergence",
        "builder-defaults-upserts-removals",
        "journal-lifecycle-fixed-clock",
        "rationale-policies",
        "staging-authored-and-missing-blobs",
        "reflection-and-stale-index",
        "hand-written-manifest-reopen",
        "attest-gating-on-every-validator-kind",
        "disposition-omitted-rationale",
        "opaque-map-null-values",
        "study-metadata-extra",
    }
    assert required <= set(CASE_IDS)


def test_both_case_kinds_are_represented() -> None:
    kinds = {case["kind"] for case in CASES}
    assert kinds == {"artifact", "operation"}


def test_every_case_matches_the_case_schema(case: dict[str, Any]) -> None:
    errors = sorted(
        Draft7Validator(CASE_SCHEMA).iter_errors(case), key=lambda error: list(error.path)
    )
    assert errors == [], f"{case['name']}: {errors[0].message if errors else ''}"


def test_case_expectations_hold(case: dict[str, Any], tmp_path: Path) -> None:
    observation = run_case(case, tmp_path)
    check_expectations(case, observation)


def test_written_output_reopens_into_an_equivalent_model(
    case: dict[str, Any], tmp_path: Path
) -> None:
    """Reopening a binding's own output yields an equivalent model (§8.6)."""
    if case["kind"] != "artifact":
        pytest.skip("an operation case's final model is not its written submission")
    observation = run_case(case, tmp_path)
    if "reopened" not in observation:
        pytest.skip("case does not write a submission")
    # The reopened model is compared against the case's declared artifact, not against
    # anything the harness derived from the same reopen call.
    assert canonical(observation["reopened"]) == canonical(observation["model"])
    assert canonical(observation["model"]) == canonical(normalize(case["artifact"]))


def test_writes_are_idempotent(case: dict[str, Any], tmp_path: Path) -> None:
    """A write → open → write round trip is idempotent within a binding (§8.7).

    Only artifact cases assert this: operation cases deliberately construct directories
    that a write must *change*, such as a hand-written manifest with no index files, or
    a stale optional index that reopening picks up again.
    """
    if case["kind"] != "artifact":
        pytest.skip("operation cases deliberately exercise non-idempotent directories")
    observation = run_case(case, tmp_path)
    if "output" not in observation:
        pytest.skip("case does not write a submission")
    assert observation["idempotent"] is True


def test_the_fixture_tree_is_referenced_by_the_corpus() -> None:
    fixtures = {
        path.relative_to(REPO_ROOT / "parity" / "fixtures").as_posix()
        for path in (REPO_ROOT / "parity" / "fixtures").rglob("*")
        if path.is_file()
    }
    text = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(CASES_DIR.glob("*.json"))
    )
    unused = {
        name
        for name in fixtures
        if name not in text and Path(name).parent.as_posix() not in text
    }
    assert unused == set(), f"unused parity fixtures: {sorted(unused)}"
