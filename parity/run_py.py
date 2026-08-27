#!/usr/bin/env python3
"""Parity runner — Python side.

``emit``       run every shared case and record this binding's normalized observations
``cross-open`` open the TypeScript binding's output and compare both bindings' results

Observations are contract-neutral reductions (see ``harness.py``); this runner never
turns one binding's current output into an expectation.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from universal_artifact_sdk import open_submission  # noqa: E402

from harness import (  # noqa: E402
    SCRATCH_DIR,
    canonical,
    case_out_dir,
    load_cases,
    normalize_model,
    run_case,
)

PY_ROOT = SCRATCH_DIR / "py"
TS_ROOT = SCRATCH_DIR / "ts"
PY_OBSERVATIONS = SCRATCH_DIR / "observations" / "py"
TS_OBSERVATIONS = SCRATCH_DIR / "observations" / "ts"


def _fail(message: str) -> None:
    print(f"parity(python): {message}", file=sys.stderr)
    raise SystemExit(1)


def _expect_equal(label: str, actual: Any, expected: Any) -> None:
    if canonical(actual) != canonical(expected):
        _fail(
            f"{label}\n--- actual ---\n{canonical(actual)}"
            f"\n--- expected ---\n{canonical(expected)}"
        )


def emit() -> None:
    shutil.rmtree(PY_ROOT, ignore_errors=True)
    shutil.rmtree(PY_OBSERVATIONS, ignore_errors=True)
    PY_OBSERVATIONS.mkdir(parents=True, exist_ok=True)
    cases = load_cases()
    for case in cases:
        observation = run_case(case, PY_ROOT)
        check_expectations(case, observation)
        (PY_OBSERVATIONS / f"{case['name']}.json").write_text(
            canonical(observation) + "\n", encoding="utf-8"
        )
    print(f"parity(python): {len(cases)} cases emitted")


def check_expectations(case: dict[str, Any], observation: dict[str, Any]) -> None:
    """Assert the reviewed expectations recorded in the case file."""
    expected = case["expected"]
    name = case["name"]
    _expect_equal(f"{name}: validation.ok", observation["validation"]["ok"], expected["ok"])
    _expect_equal(
        f"{name}: error paths", observation["validation"]["error_paths"], expected["error_paths"]
    )
    _expect_equal(
        f"{name}: warning paths",
        observation["validation"]["warning_paths"],
        expected["warning_paths"],
    )
    if "schema_valid" in expected:
        _expect_equal(
            f"{name}: schema validity", observation["schema"]["valid"], expected["schema_valid"]
        )
    for path in expected.get("schema_error_paths", []):
        if path not in observation["schema"]["paths"]:
            actual = observation["schema"]["paths"]
            _fail(f"{name}: expected a schema error at '{path}', got {actual}")
    if "model" in expected:
        _expect_equal(f"{name}: model", observation["model"], expected["model"])
    if "report" in expected:
        _expect_equal(f"{name}: write report", observation["write"], expected["report"])
    if "output" in expected:
        for key, value in expected["output"].items():
            _expect_equal(f"{name}: output.{key}", observation["output"][key], value)
    if "state" in expected:
        _expect_equal(f"{name}: state", observation["output"]["state"], expected["state"])
    if "reopened" in expected:
        _expect_equal(f"{name}: reopened model", observation["reopened"], expected["reopened"])
    if "steps" in expected:
        _expect_equal(f"{name}: steps", observation["steps"], expected["steps"])
    for index, value in (expected.get("step_returns") or {}).items():
        step = observation["steps"][int(index)]
        label = f"{name}: step {index} ({step['operation']}) return"
        _expect_equal(label, step.get("returned"), value)
    for index in expected.get("raising_steps", []):
        step = observation["steps"][int(index)]
        if not step.get("raised"):
            _fail(f"{name}: step {index} ({step['operation']}) was expected to raise")
    if observation.get("idempotent") is False:
        _fail(f"{name}: write → open → write was not idempotent")


def cross_open() -> None:
    """Open the TypeScript binding's output and compare both bindings' observations."""
    cases = load_cases()
    compared = 0
    for case in cases:
        name = case["name"]
        mine_path = PY_OBSERVATIONS / f"{name}.json"
        theirs_path = TS_OBSERVATIONS / f"{name}.json"
        if not mine_path.is_file():
            _fail(f"{name}: missing Python observation — run `emit` first")
        if not theirs_path.is_file():
            _fail(f"{name}: missing TypeScript observation — run the TypeScript runner first")
        mine = json.loads(mine_path.read_text(encoding="utf-8"))
        theirs = json.loads(theirs_path.read_text(encoding="utf-8"))
        for key in ("validation", "write", "model", "reopened", "steps", "output"):
            if key in mine or key in theirs:
                _expect_equal(
                    f"{name}: {key} differs between bindings", mine.get(key), theirs.get(key)
                )
        if "schema" in mine or "schema" in theirs:
            # Both bindings must accept or reject the same artifact; the two schema
            # libraries report sub-schema failures at different granularity, so only
            # the verdict is a cross-binding contract (PYTHON_BINDING.md §8.1).
            _expect_equal(
                f"{name}: schema verdict differs between bindings",
                (mine.get("schema") or {}).get("valid"),
                (theirs.get("schema") or {}).get("valid"),
            )
        if "reopened" not in mine:
            compared += 1
            continue
        ts_out = case_out_dir(TS_ROOT, case) / "out"
        if not (ts_out / "manifest.yml").is_file():
            _fail(f"{name}: TypeScript output is missing at {ts_out}")
        cross = normalize_model(open_submission(ts_out))
        _expect_equal(f"{name}: Python reopening TypeScript output", cross, mine["reopened"])
        compared += 1
    print(f"parity(python): {compared} cases cross-opened and compared")


def main(argv: list[str]) -> None:
    phase = argv[1] if len(argv) > 1 else "emit"
    if phase == "emit":
        emit()
    elif phase == "cross-open":
        cross_open()
    else:
        _fail(f"unknown phase '{phase}' (expected 'emit' or 'cross-open')")


if __name__ == "__main__":
    main(sys.argv)
