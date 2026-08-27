"""Structural validation — mirrors ``test/validation.test.ts``."""

from __future__ import annotations

import re

import pytest

from universal_artifact_sdk import (
    Artifact,
    Assessment,
    AttestValidator,
    BuiltinValidator,
    Claim,
    Dataset,
    Environment,
    Experiment,
    Image,
    InContainerLocation,
    LlmJudgeValidator,
    Paper,
    ProcedureValidator,
    ResearchAgent,
    Result,
    RunSpec,
    Trace,
    ValidationReport,
    add_claim,
    add_dataset,
    add_environment,
    add_result,
    add_trace,
    attach_paper,
    create_artifact,
    to_dict,
    validate_structure,
)
from universal_artifact_sdk.model import ExternalLocation


def report_of(artifact: Artifact) -> ValidationReport:
    return validate_structure(artifact)


def has_error(artifact: Artifact, pattern: str) -> bool:
    return any(
        re.search(pattern, f"{issue.path}: {issue.message}")
        for issue in validate_structure(artifact).errors
    )


def has_warning(artifact: Artifact, pattern: str) -> bool:
    return any(
        re.search(pattern, f"{issue.path}: {issue.message}")
        for issue in validate_structure(artifact).warnings
    )


class TestDatasets:
    def test_in_container_requires_an_environment_name(self) -> None:
        artifact = create_artifact(id="x", title="t")
        artifact.datasets.append(
            Dataset(id="d", location={"kind": "in_container", "path": "/opt/data"})
        )
        assert has_error(artifact, "in_container dataset requires `in_environment`")

    def test_in_container_without_a_declared_environment_warns(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_dataset(
            artifact,
            Dataset(
                id="d",
                location=InContainerLocation(path="/opt/data", in_environment="primary"),
            ),
        )
        assert has_warning(artifact, "in_container dataset but no environment declared")

    def test_in_container_is_accepted_when_the_environment_exists(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_environment(artifact, Environment(name="primary", image=Image(reference="img:1")))
        add_dataset(
            artifact,
            Dataset(
                id="d",
                location=InContainerLocation(path="/opt/data", in_environment="primary"),
            ),
        )
        assert report_of(artifact).ok is True

    def test_rejects_a_dataset_without_a_location_kind(self) -> None:
        artifact = create_artifact(id="x", title="t")
        artifact.datasets.append(Dataset(id="d", location={}))
        assert has_error(artifact, r"dataset requires `location.kind`")

    def test_external_datasets_require_a_checksum(self) -> None:
        artifact = create_artifact(id="x", title="t")
        artifact.datasets.append(
            Dataset(id="d", location={"kind": "external", "uri": "https://e/x.tar"})
        )
        assert has_error(artifact, "requires a `sha256`")

    def test_a_checksummed_external_dataset_is_accepted(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_dataset(
            artifact,
            Dataset(id="d", location=ExternalLocation(uri="https://e/x.tar", sha256="abc")),
        )
        assert report_of(artifact).ok is True


class TestExperiments:
    def test_requires_directory_and_run_command(self) -> None:
        artifact = create_artifact(id="x", title="t")
        artifact.experiments.append(
            Experiment(slug="e1", directory="", run=RunSpec(command=""))
        )
        report = report_of(artifact)
        assert any("requires `directory`" in issue.message for issue in report.errors)
        assert any("requires `run.command`" in issue.message for issue in report.errors)

    def test_flags_dangling_dataset_experiment_and_environment_references(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_environment(artifact, Environment(name="primary", image=Image(reference="img:1")))
        artifact.experiments.append(
            Experiment(
                slug="e1",
                directory="experiments/e1",
                run=RunSpec(command="run"),
                uses_data=[{"dataset": "ghost", "at": "data/x"}],  # type: ignore[list-item]
                depends_on=["missing"],
                runs_in="not-primary",
            )
        )
        assert has_error(artifact, "references unknown dataset 'ghost'")
        assert has_error(artifact, "references unknown experiment 'missing'")
        assert has_error(artifact, "references unknown environment 'not-primary'")


class TestTraces:
    def test_flags_covers_pointing_at_an_unknown_experiment(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_trace(
            artifact,
            Trace(id="T1", kind="agent_session", path="traces/t.jsonl", covers=["ghost"]),
        )
        assert has_error(
            artifact, r"trace\[T1\].covers: references unknown experiment 'ghost'"
        )

    def test_requires_id_and_path(self) -> None:
        artifact = create_artifact(id="x", title="t")
        artifact.traces.append(Trace(id="", kind="agent_session", path=""))
        assert report_of(artifact).ok is False

    def test_accepts_a_human_interaction_trace(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_trace(
            artifact,
            Trace(
                id="human-in-the-loop",
                kind="human_interaction",
                path="traces/human_interactions.md",
                counters={"entries": 3, "clarifications": 1, "gates": 2, "revisions": 1},
            ),
        )
        assert report_of(artifact).ok is True
        assert artifact.traces[0].kind == "human_interaction"


class TestResults:
    def test_rejects_an_illegal_validation_mode_and_unknown_produced_by(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_result(
            artifact,
            Result(
                id="R1",
                validates=[],
                evidence="e",
                kind="metrics",
                validation_mode="reticulate",
                produced_by="ghost",
            ),
        )
        assert has_error(artifact, "illegal validation_mode 'reticulate'")
        assert has_error(artifact, "produced_by: references unknown experiment 'ghost'")

    def test_requires_id_evidence_and_kind(self) -> None:
        artifact = create_artifact(id="x", title="t")
        artifact.results.append(Result(id="", validates=[], evidence="", kind=""))
        assert report_of(artifact).ok is False


class TestValidatorWellFormedness:
    def claim_with(self, validator: object) -> Artifact:
        artifact = create_artifact(id="x", title="t")
        artifact.claims.append(Claim(id="C1", statement="s", validators=[validator]))  # type: ignore[list-item]
        return artifact

    def test_builtin_requires_name(self) -> None:
        assert has_error(
            self.claim_with(BuiltinValidator(name="")), "builtin validator requires `name`"
        )

    def test_procedure_requires_instructions(self) -> None:
        assert has_error(
            self.claim_with(ProcedureValidator(instructions="")),
            "procedure validator requires `instructions`",
        )

    def test_attest_requires_checks(self) -> None:
        assert has_error(
            self.claim_with(AttestValidator(checks="")), "attest validator requires `checks`"
        )

    def test_llm_judge_requires_criteria(self) -> None:
        assert has_error(
            self.claim_with(LlmJudgeValidator(criteria="")),
            "llm_judge validator requires `criteria`",
        )

    def test_rejects_an_unknown_validator_kind(self) -> None:
        validator = BuiltinValidator(name="n")
        validator.kind = "wat"
        assert has_error(self.claim_with(validator), "unknown validator kind wat")

    def test_reports_a_missing_kind(self) -> None:
        validator = BuiltinValidator(name="n")
        validator.kind = ""
        assert has_error(self.claim_with(validator), "unknown validator kind <missing>")


class TestClaimsAndGating:
    def test_warns_on_a_claim_with_no_validators(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="C1", statement="s"))
        assert has_warning(artifact, "claim has no validator")
        assert report_of(artifact).ok is True

    def test_flags_gated_by_pointing_at_an_unknown_validator(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_result(artifact, Result(id="R1", validates=["C1"], evidence="e", kind="transcript"))
        add_claim(
            artifact,
            Claim(
                id="C1",
                statement="s",
                validators=[
                    LlmJudgeValidator(
                        id="v_inspect", criteria="c", inputs=["R1"], gated_by="ghost"
                    )
                ],
            ),
        )
        assert has_error(artifact, "references unknown validator 'ghost' on this claim")

    def test_accepts_a_well_formed_attest_gates_inspect_pair(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_result(artifact, Result(id="R1", validates=["C1"], evidence="e", kind="transcript"))
        add_claim(
            artifact,
            Claim(
                id="C1",
                statement="s",
                validators=[
                    AttestValidator(id="v_attest", checks="provenance", inputs=["R1"]),
                    LlmJudgeValidator(
                        id="v_inspect", criteria="c", inputs=["R1"], gated_by="v_attest"
                    ),
                ],
            ),
        )
        assert report_of(artifact).ok is True

    def test_rejects_gated_by_pointing_at_a_non_attest_validator(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_result(artifact, Result(id="R1", validates=["C1"], evidence="e", kind="metrics"))
        add_claim(
            artifact,
            Claim(
                id="C1",
                statement="s",
                validators=[
                    LlmJudgeValidator(id="v1", criteria="c", inputs=["R1"]),
                    LlmJudgeValidator(id="v2", criteria="c", inputs=["R1"], gated_by="v1"),
                ],
            ),
        )
        assert has_error(artifact, "must reference an attest validator")

    def test_flags_an_extra_backed_gated_by_on_an_attest_validator(self) -> None:
        # `AttestValidator` declares no `gated_by`, so a producer-authored one lands in
        # `extra`; the frozen TypeScript validator reads it off every validator kind.
        artifact = create_artifact(id="x", title="t")
        add_claim(
            artifact,
            Claim(
                id="C1",
                statement="s",
                validators=[
                    AttestValidator(
                        id="v_attest", checks="provenance", extra={"gated_by": "ghost"}
                    )
                ],
            ),
        )
        report = report_of(artifact)
        assert report.ok is False
        assert [issue.path for issue in report.errors] == [
            "claim[C1].validators[v_attest].gated_by"
        ]
        assert has_error(artifact, "references unknown validator 'ghost' on this claim")

    def test_flags_an_extra_backed_gated_by_pointing_at_a_non_attest_validator(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(
            artifact,
            Claim(
                id="C1",
                statement="s",
                validators=[
                    BuiltinValidator(id="v_builtin", name="contains"),
                    AttestValidator(
                        id="v_attest", checks="provenance", extra={"gated_by": "v_builtin"}
                    ),
                ],
            ),
        )
        report = report_of(artifact)
        assert [issue.path for issue in report.errors] == [
            "claim[C1].validators[v_attest].gated_by"
        ]
        assert has_error(artifact, "must reference an attest validator, got 'builtin'")

    def test_an_extra_backed_gated_by_survives_serialization(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(
            artifact,
            Claim(
                id="C1",
                statement="s",
                validators=[
                    AttestValidator(id="v_gate", checks="provenance"),
                    AttestValidator(
                        id="v_attest", checks="integrity", extra={"gated_by": "v_gate"}
                    ),
                ],
            ),
        )
        assert report_of(artifact).ok is True
        assert to_dict(artifact)["claims"][0]["validators"][1]["gated_by"] == "v_gate"

    def test_flags_plural_inputs_pointing_at_an_unknown_result(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(
            artifact,
            Claim(
                id="C1",
                statement="s",
                validators=[AttestValidator(id="v", checks="integrity", inputs=["R_ghost"])],
            ),
        )
        assert has_error(artifact, "inputs: references unknown result 'R_ghost'")

    def test_flags_a_builtin_input_result_that_is_dangling(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_result(artifact, Result(id="R1", validates=["C1"], evidence="e", kind="metrics"))
        add_claim(
            artifact,
            Claim(
                id="C1",
                statement="s",
                validators=[
                    BuiltinValidator(
                        name="monotonic",
                        input={"result": "NOPE", "series": ["a"]},
                        params={"direction": "decreasing"},
                    )
                ],
            ),
        )
        assert has_error(artifact, r"input.result.*unknown result 'NOPE'")

    def test_a_validator_without_a_kind_is_reported_not_coerced(self) -> None:
        artifact = create_artifact(id="x", title="t")
        artifact.claims.append(
            Claim(id="C1", statement="s", validators=[{"name": "contains"}])
        )
        report = report_of(artifact)
        assert report.ok is False
        assert [issue.message for issue in report.errors] == [
            "unknown validator kind <missing>"
        ]
        # The unrecognized validator is carried verbatim, never given a `kind`.
        assert to_dict(artifact)["claims"][0]["validators"] == [{"name": "contains"}]

    def test_an_unknown_validator_kind_is_carried_verbatim(self) -> None:
        artifact = create_artifact(id="x", title="t")
        artifact.claims.append(
            Claim(id="C1", statement="s", validators=[{"kind": "sorcery", "spell": 1}])
        )
        assert has_error(artifact, "unknown validator kind sorcery")
        assert to_dict(artifact)["claims"][0]["validators"] == [
            {"kind": "sorcery", "spell": 1}
        ]

    def test_an_empty_validator_id_stays_in_the_issue_path(self) -> None:
        artifact = create_artifact(id="x", title="t")
        artifact.claims.append(
            Claim(id="C1", statement="s", validators=[AttestValidator(id="", checks="")])
        )
        assert any(
            issue.path == "claim[C1].validators[]" for issue in report_of(artifact).errors
        )

    def test_indexes_an_anonymous_validator_by_position(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="C1", statement="s", validators=[BuiltinValidator(name="")]))
        assert any(
            issue.path == "claim[C1].validators[0]" for issue in report_of(artifact).errors
        )


class TestAssessments:
    def test_requires_dimension_and_a_legal_scope(self) -> None:
        artifact = create_artifact(id="x", title="t")
        artifact.assessments.append(Assessment(id="A1", dimension="", scope="galaxy"))
        report = report_of(artifact)
        assert any("requires `dimension`" in issue.message for issue in report.errors)
        assert any(
            "scope must be 'artifact' or 'paper'" in issue.message for issue in report.errors
        )


class TestArtifactRoot:
    def test_requires_id_and_title(self) -> None:
        artifact = create_artifact(id="x", title="t")
        artifact.id = ""
        artifact.title = ""
        report = report_of(artifact)
        assert any(issue.path == "artifact.id" for issue in report.errors)
        assert any(issue.path == "artifact.title" for issue in report.errors)


class TestEnvironmentPinning:
    def test_warns_on_a_bare_tag(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_environment(
            artifact, Environment(name="primary", image=Image(reference="registry/artifact:1.2"))
        )
        assert has_warning(artifact, "image is not pinned to a digest")
        assert report_of(artifact).ok is True

    def test_does_not_warn_when_the_digest_is_set(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_environment(
            artifact,
            Environment(
                name="primary",
                image=Image(reference="registry/artifact:1.2", digest="sha256:" + "a" * 64),
            ),
        )
        assert has_warning(artifact, "image is not pinned to a digest") is False

    def test_does_not_warn_when_the_reference_embeds_a_digest(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_environment(
            artifact,
            Environment(
                name="primary",
                image=Image(reference="registry/artifact:1.2@sha256:" + "b" * 64),
            ),
        )
        assert has_warning(artifact, "image is not pinned to a digest") is False


class TestPaper:
    @pytest.mark.parametrize(
        "paper",
        [
            Paper(pdf="paper.pdf"),
            Paper(source="paper/"),
            Paper(pdf="paper.pdf", source="paper/"),
        ],
    )
    def test_accepts_a_paper_with_pdf_or_source(self, paper: Paper) -> None:
        artifact = create_artifact(id="x", title="t")
        attach_paper(artifact, paper)
        assert has_error(artifact, "paper requires at least one") is False

    @pytest.mark.parametrize(
        "paper", [Paper(), Paper(pdf="   "), Paper(source="   ")]
    )
    def test_rejects_a_paper_with_neither(self, paper: Paper) -> None:
        artifact = create_artifact(id="x", title="t")
        attach_paper(artifact, paper)
        assert has_error(artifact, r"paper requires at least one of `pdf` or `source`")


class TestResearchAgent:
    def test_is_optional(self) -> None:
        artifact = create_artifact(id="x", title="t")
        assert artifact.research_agent is None
        assert report_of(artifact).ok is True

    @pytest.mark.parametrize(
        "path",
        [
            123,
            ".",
            ".sdk",
            ".SDK",
            ".sdk/agent.md",
            ".SDK/agent.md",
            "foo/..",
            "foo/../research-agent.md",
            "/abs-agent.md",
            "C:/agent.md",
            "C:agent.md",
            "manifest.yml",
            "Manifest.yml",
            "claims.yml/agent.md",
            "",
            "  padded.md",
        ],
    )
    def test_rejects_paths_that_are_not_plain_relative_files(self, path: object) -> None:
        artifact = create_artifact(id="x", title="t")
        artifact.research_agent = ResearchAgent(
            path=path,  # type: ignore[arg-type]
            model="m",
            grounding_sources=["claims.yml"],
        )
        report = report_of(artifact)
        assert report.ok is False
        assert any(issue.path == "research_agent.path" for issue in report.errors)

    @pytest.mark.parametrize(
        "sources",
        [
            [123],
            [""],
            ["   "],
            ["../outside.txt"],
            ["/abs.txt"],
            ["C:/secret"],
            ["C:secret"],
            ["foo/../bar.txt"],
            [".sdk"],
            [".SDK"],
            [".sdk/context.md"],
            [".SDK/context.md"],
            ["claims.yml/context.md"],
        ],
    )
    def test_rejects_unsafe_grounding_sources(self, sources: list[object]) -> None:
        artifact = create_artifact(id="x", title="t")
        artifact.research_agent = ResearchAgent(
            path="research-agent.md",
            model="m",
            grounding_sources=sources,  # type: ignore[arg-type]
        )
        report = report_of(artifact)
        assert report.ok is False
        assert any(
            issue.path == "research_agent.grounding_sources[0]" for issue in report.errors
        )

    @pytest.mark.parametrize("model", ["", "   ", 123])
    def test_requires_a_pinned_model(self, model: object) -> None:
        artifact = create_artifact(id="x", title="t")
        artifact.research_agent = ResearchAgent(
            path="research-agent.md",
            model=model,  # type: ignore[arg-type]
            grounding_sources=["claims.yml"],
        )
        report = report_of(artifact)
        assert report.ok is False
        assert any(issue.path == "research_agent.model" for issue in report.errors)

    def test_requires_at_least_one_grounding_source(self) -> None:
        artifact = create_artifact(id="x", title="t")
        artifact.research_agent = ResearchAgent(
            path="research-agent.md", model="m", grounding_sources=[]
        )
        report = report_of(artifact)
        assert report.ok is False
        assert any(
            issue.path == "research_agent.grounding_sources" for issue in report.errors
        )

    def test_accepts_a_generated_index_as_a_grounding_source(self) -> None:
        # Only descendants of a generated file are reserved at runtime; the canonical
        # schema is stricter, which parity/cases/schema-runtime-divergence.json records.
        artifact = create_artifact(id="x", title="t")
        artifact.research_agent = ResearchAgent(
            path="research-agent.md", model="m", grounding_sources=["claims.yml"]
        )
        assert report_of(artifact).ok is True


class TestIssueOrder:
    def test_issues_are_returned_in_traversal_order(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_result(
            artifact, Result(id="R", validates=["missing"], evidence="e.csv", kind="metrics")
        )
        add_trace(
            artifact, Trace(id="T", kind="execution_log", path="../unsafe", covers=["gone"])
        )
        report = report_of(artifact)
        assert [issue.path for issue in report.errors] == [
            "trace[T].path",
            "trace[T].covers",
            "result[R].validates",
        ]

    def test_a_structural_error_report_is_not_ok(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_result(
            artifact, Result(id="R", validates=["missing"], evidence="e.csv", kind="metrics")
        )
        report = report_of(artifact)
        assert report.ok is False
        # Errors and warnings are independent: the journal warning is still reported.
        assert [issue.path for issue in report.warnings] == ["journal[#1]"]
