"""Shared fixtures.

The suite is deterministic and offline: no test reaches the network, and every test
writes into a per-test temporary directory rather than the repository tree.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from universal_artifact_sdk import (
    Artifact,
    AttestValidator,
    BuiltinValidator,
    Claim,
    Dataset,
    Environment,
    Experiment,
    ExternalLocation,
    Image,
    InArtifactLocation,
    InterRaterReliability,
    LlmJudgeValidator,
    PaperReference,
    QualitativeExcerpt,
    QualitativeSupport,
    Result,
    RunSpec,
    StudyMetadata,
    Trace,
    add_claim,
    add_dataset,
    add_environment,
    add_experiment,
    add_result,
    add_trace,
    attach_paper,
    canonical_schema_path,
    create_artifact,
)
from universal_artifact_sdk.model import DataUse, Paper

REPO_ROOT = Path(__file__).resolve().parents[2]
TS_FIXTURE_SOURCE = REPO_ROOT / "test" / "fixtures" / "source"


@pytest.fixture
def out_dir(tmp_path: Path) -> Path:
    """A fresh, empty submission directory."""
    target = tmp_path / "out"
    target.mkdir()
    return target


@pytest.fixture
def source_dir(tmp_path: Path) -> Path:
    """A fresh, empty producer blob root for ``stage_from``."""
    target = tmp_path / "source"
    target.mkdir()
    return target


@pytest.fixture(scope="session")
def canonical_schema() -> dict[str, Any]:
    return json.loads(canonical_schema_path().read_text(encoding="utf-8"))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_worked_example() -> Artifact:
    """The Appendix A worked example, mirroring ``test/worked-example.test.ts``."""
    artifact = create_artifact(id="expt-42", title="Feedback-driven contraction")
    add_environment(
        artifact,
        Environment(
            name="primary",
            image=Image(reference="reg/artifact:1.2", digest="sha256:abc"),
        ),
    )
    add_dataset(
        artifact,
        Dataset(
            id="sample_corpus",
            location=ExternalLocation(
                uri="https://example.org/corpus-v3.tar.gz",
                sha256="def",
                bytes=294721271,
                access="public",
            ),
            prepare="tar -xzf corpus-v3.tar.gz -C ./data",
        ),
    )
    add_experiment(
        artifact,
        Experiment(
            slug="posterior_contraction",
            directory="experiments/posterior_contraction",
            run=RunSpec(command="python run.py --seed 0", entrypoint="run.py", seed=0),
            uses_data=[DataUse(dataset="sample_corpus", at="data/corpus.parquet")],
            runs_in="primary",
        ),
    )
    add_result(
        artifact,
        Result(
            id="R1",
            produced_by="posterior_contraction",
            validates=["C1"],
            evidence="experiments/posterior_contraction/contraction.csv",
            kind="metrics",
            locators={
                "kl_final": {"column": "kl_divergence", "row": "final"},
                "kl_initial": {"column": "kl_divergence", "row": "0"},
            },
        ),
    )
    add_claim(
        artifact,
        Claim(
            id="C1",
            statement="Posterior contraction improves with more feedback rounds.",
            paper_ref=PaperReference(section="5.2", figure="3"),
            validators=[
                BuiltinValidator(
                    name="monotonic",
                    input={"result": "R1", "series": ["kl_initial", "kl_final"]},
                    params={"direction": "decreasing"},
                )
            ],
        ),
    )
    add_dataset(
        artifact,
        Dataset(
            id="interviews",
            location=InArtifactLocation(path="data/interviews/"),
            study=StudyMetadata(
                ethics_approval="IRB-2025-0142",
                consent_basis="informed, opt-in",
                deidentification="names redacted",
                sampling="convenience; n=18",
            ),
        ),
    )
    add_trace(
        artifact,
        Trace(
            id="T1",
            kind="agent_session",
            path="traces/run_0007.jsonl",
            covers=["posterior_contraction"],
            terminal_state="completed_with_outputs",
        ),
    )
    add_result(
        artifact,
        Result(
            id="R2",
            validates=["C7"],
            evidence="data/interviews/",
            kind="transcript",
            validation_mode="inspect",
            support=QualitativeSupport(
                excerpts=[QualitativeExcerpt(file="data/interviews/P07.txt", lines="40-55")],
                inter_rater_reliability=InterRaterReliability(metric="cohen_kappa", value=0.81),
            ),
        ),
    )
    add_claim(
        artifact,
        Claim(
            id="C7",
            statement="Participants distrusted the tool's suggestions.",
            paper_ref=PaperReference(section="6.1"),
            validators=[
                AttestValidator(id="v_attest", checks="provenance", inputs=["R2"]),
                LlmJudgeValidator(
                    id="v_inspect",
                    criteria="The cited excerpts express distrust of the tool's suggestions.",
                    inputs=["R2"],
                    gated_by="v_attest",
                ),
            ],
        ),
    )
    attach_paper(
        artifact,
        Paper(pdf="paper.pdf", source="paper/", references_export="paper_references.yml"),
    )
    return artifact
