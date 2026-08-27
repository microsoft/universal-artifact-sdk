"""Research agent, worked example and canonical-schema conformance.

Mirrors ``test/research-agent.test.ts`` and ``test/worked-example.test.ts``.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft7Validator

from universal_artifact_sdk import (
    ChangeContext,
    Claim,
    Dataset,
    ExternalLocation,
    ResearchAgent,
    Result,
    add_claim,
    add_dataset,
    add_result,
    attach_research_agent,
    canonical_schema_path,
    configure_journal,
    create_artifact,
    list_journal,
    open_submission,
    read_yaml,
    to_dict,
    validate_structure,
    write_submission,
)
from universal_artifact_sdk.model import (
    Artifact,
    AttestValidator,
    BuiltinValidator,
    LlmJudgeValidator,
)
from universal_artifact_sdk.serialize import StructuralError

from conftest import TS_FIXTURE_SOURCE, build_worked_example

FIXED = "2026-01-01T00:00:00.000Z"


def seeded() -> Artifact:
    artifact = create_artifact(id="x", title="t")
    configure_journal(artifact, actor="agent:experiment", now=lambda: FIXED)
    return artifact


def schema_errors(schema: dict[str, Any], data: Any) -> list[str]:
    return [
        "/" + "/".join(str(part) for part in error.absolute_path)
        for error in Draft7Validator(schema).iter_errors(data)
    ]


class TestResearchAgent:
    def test_is_absent_by_default(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        assert artifact.research_agent is None
        assert validate_structure(artifact).ok is True
        write_submission(artifact, out_dir)
        manifest = read_yaml(out_dir / "manifest.yml")
        assert "research_agent" not in manifest
        assert manifest["evidence_inventory"]["has_research_agent"] is False

    def test_attaches_with_a_default_path(self) -> None:
        artifact = seeded()
        agent = attach_research_agent(
            artifact,
            ResearchAgent(
                path="",
                model="copilot/gpt-5.5@2026-06-01",
                grounding_sources=["claims.yml", "results.yml"],
                scope=["research", "negative-results"],
            ),
        )
        assert agent.path == "research-agent.md"
        assert artifact.research_agent is not None
        assert artifact.research_agent.model == "copilot/gpt-5.5@2026-06-01"
        assert validate_structure(artifact).ok is True

    def test_journals_the_attach(self) -> None:
        artifact = seeded()
        attach_research_agent(
            artifact,
            ResearchAgent(path="research-agent.md", model="m", grounding_sources=["claims.yml"]),
            ctx=ChangeContext(rationale="ship the witness"),
        )
        entry = list_journal(artifact)[-1]
        assert entry.op == "attach"
        assert entry.target.kind == "research_agent"
        assert entry.target.id == "research-agent.md"
        assert entry.rationale == "ship the witness"

    def test_reattaching_records_a_replace(self) -> None:
        artifact = seeded()
        agent = ResearchAgent(path="research-agent.md", model="m", grounding_sources=["claims.yml"])
        attach_research_agent(artifact, agent, ctx=ChangeContext(rationale="first"))
        attach_research_agent(artifact, agent, ctx=ChangeContext(rationale="second"))
        assert [e.op for e in list_journal(artifact)] == ["attach", "replace"]

    def test_round_trips_through_serialize_and_open(
        self, out_dir: Path, source_dir: Path
    ) -> None:
        (source_dir / "research-agent.md").write_text(
            "# persona\nask me anything", encoding="utf-8"
        )
        artifact = seeded()
        attach_research_agent(
            artifact,
            ResearchAgent(
                path="research-agent.md",
                model="copilot/gpt-5.5@2026-06-01",
                grounding_sources=["claims.yml", "paper/"],
                scope=["results"],
            ),
        )
        write_submission(artifact, out_dir, stage_from=source_dir)
        manifest = read_yaml(out_dir / "manifest.yml")
        assert manifest["research_agent"]["model"] == "copilot/gpt-5.5@2026-06-01"
        assert manifest["research_agent"]["grounding_sources"] == ["claims.yml", "paper/"]
        assert manifest["evidence_inventory"]["has_research_agent"] is True
        assert "persona" in (out_dir / "research-agent.md").read_text(encoding="utf-8")
        assert open_submission(out_dir).research_agent == artifact.research_agent

    def test_stages_grounding_source_files(self, out_dir: Path, source_dir: Path) -> None:
        (source_dir / "research-agent.md").write_text("# persona", encoding="utf-8")
        (source_dir / "agent").mkdir()
        (source_dir / "agent" / "context.md").write_text("context", encoding="utf-8")
        artifact = seeded()
        attach_research_agent(
            artifact,
            ResearchAgent(
                path="research-agent.md", model="m", grounding_sources=["agent/context.md"]
            ),
        )
        report = write_submission(artifact, out_dir, stage_from=source_dir)
        assert report.missing_blobs == []
        assert (out_dir / "agent" / "context.md").is_file()
        assert "agent/context.md" in (out_dir / "SHA256SUMS").read_text(encoding="utf-8")

    def test_a_malformed_agent_blocks_the_write(self, out_dir: Path) -> None:
        artifact = seeded()
        artifact.research_agent = ResearchAgent(
            path=None,  # type: ignore[arg-type]
            model="m",
            grounding_sources=["claims.yml"],
        )
        report = validate_structure(artifact)
        assert report.ok is False
        assert any(issue.path == "research_agent.path" for issue in report.errors)
        with pytest.raises(StructuralError, match="research_agent.path"):
            write_submission(artifact, out_dir)


class TestWorkedExample:
    def test_emits_the_expected_layout(self, out_dir: Path) -> None:
        report = write_submission(
            build_worked_example(), out_dir, stage_from=TS_FIXTURE_SOURCE
        )
        assert report.ok is True
        assert report.missing_blobs == []
        for name in (
            "manifest.yml",
            "claims.yml",
            "results.yml",
            "datasets.yml",
            "traces.yml",
            "journal.yml",
            "SHA256SUMS",
            ".sdk/state.json",
        ):
            assert (out_dir / name).is_file(), name
        assert not (out_dir / "assessments.yml").exists()
        assert not (out_dir / "exhibits.yml").exists()
        for staged in (
            "experiments/posterior_contraction/contraction.csv",
            "data/interviews/P07.txt",
            "traces/run_0007.jsonl",
            "paper.pdf",
            "paper/main.tex",
            "paper_references.yml",
        ):
            assert (out_dir / staged).is_file(), staged

    def test_stamps_versions_and_computes_the_inventory(self, out_dir: Path) -> None:
        write_submission(build_worked_example(), out_dir, stage_from=TS_FIXTURE_SOURCE)
        manifest = read_yaml(out_dir / "manifest.yml")
        assert manifest["format_version"] == "evaluable-artifact/v2"
        assert manifest["sdk_version"] == "artifact-sdk/v1"
        assert "artifact-sdk/v1" in manifest["_generated"]
        inventory = manifest["evidence_inventory"]
        assert inventory["has_runnable_experiments"] is True
        assert inventory["has_traces"] is True
        assert inventory["trace_count"] == 1
        assert inventory["has_released_data"] is True
        assert inventory["has_citations_export"] is True
        assert "metrics" in inventory["evidence_kinds"]
        assert "transcript" in inventory["evidence_kinds"]
        assert "inspect" in inventory["validation_modes"]

    def test_serializes_claims_with_validators_and_gating(self, out_dir: Path) -> None:
        write_submission(build_worked_example(), out_dir, stage_from=TS_FIXTURE_SOURCE)
        claims = read_yaml(out_dir / "claims.yml")["claims"]
        c7 = next(claim for claim in claims if claim["id"] == "C7")
        assert len(c7["validators"]) == 2
        assert c7["validators"][0]["kind"] == "attest"
        assert c7["validators"][1]["gated_by"] == "v_attest"

    def test_sha256sums_covers_shipped_files(self, out_dir: Path) -> None:
        write_submission(build_worked_example(), out_dir, stage_from=TS_FIXTURE_SOURCE)
        sums = (out_dir / "SHA256SUMS").read_text(encoding="utf-8")
        assert "manifest.yml" in sums
        assert "experiments/posterior_contraction/contraction.csv" in sums
        assert "SHA256SUMS" not in sums

    def test_reopening_round_trips_and_preserves_authored_blobs(self, out_dir: Path) -> None:
        write_submission(build_worked_example(), out_dir, stage_from=TS_FIXTURE_SOURCE)
        reopened = open_submission(out_dir)
        assert reopened.id == "expt-42"
        assert sorted(claim.id for claim in reopened.claims) == ["C1", "C7"]
        assert sorted(result.id for result in reopened.results) == ["R1", "R2"]
        assert len(reopened.traces) == 1
        assert reopened.results[0].locators is not None
        assert reopened.results[1].support is not None
        assert reopened.results[1].support.inter_rater_reliability is not None
        assert reopened.results[1].support.inter_rater_reliability.value == 0.81
        assert reopened.datasets[1].study is not None
        assert reopened.datasets[1].study.ethics_approval == "IRB-2025-0142"
        report = write_submission(reopened, out_dir)
        assert report.ok is True
        assert (out_dir / "data" / "interviews" / "P07.txt").is_file()

    def test_upsert_by_id_replaces_rather_than_duplicates(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="C1", statement="first"))
        add_claim(artifact, Claim(id="C1", statement="second"))
        assert len(artifact.claims) == 1
        assert artifact.claims[0].statement == "second"


class TestStructuralGatesOnWrite:
    def test_rejects_a_dangling_result_claim_reference(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        add_result(artifact, Result(id="R1", validates=["NOPE"], evidence="e.csv", kind="metrics"))
        with pytest.raises(StructuralError, match="unknown claim 'NOPE'"):
            write_submission(artifact, out_dir)

    def test_rejects_an_external_dataset_without_a_checksum(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        add_dataset(
            artifact,
            Dataset(id="d", location=ExternalLocation(uri="https://e/x.tar", sha256="")),
        )
        with pytest.raises(StructuralError, match="requires a `sha256`"):
            write_submission(artifact, out_dir)

    def test_rejects_a_dangling_builtin_input_result(self, out_dir: Path) -> None:
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
        with pytest.raises(StructuralError, match="unknown result 'NOPE'"):
            write_submission(artifact, out_dir)

    def test_rejects_gating_on_a_non_attest_validator(self, out_dir: Path) -> None:
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
        with pytest.raises(StructuralError, match="must reference an attest validator"):
            write_submission(artifact, out_dir)


class TestCanonicalSchema:
    def test_the_schema_ships_with_the_package(self) -> None:
        assert canonical_schema_path().is_file()
        assert canonical_schema_path().name == "evaluable-artifact-v2.schema.json"

    def test_the_worked_example_validates(self, canonical_schema: dict[str, Any]) -> None:
        assert schema_errors(canonical_schema, to_dict(build_worked_example())) == []

    def test_a_reopened_artifact_validates(
        self, canonical_schema: dict[str, Any], out_dir: Path
    ) -> None:
        write_submission(build_worked_example(), out_dir, stage_from=TS_FIXTURE_SOURCE)
        assert schema_errors(canonical_schema, to_dict(open_submission(out_dir))) == []

    @pytest.mark.parametrize(
        "path",
        [
            "",
            ".",
            ".sdk",
            ".SDK",
            ".sdk/agent.md",
            "foo/..",
            "../agent.md",
            "/agent.md",
            "C:/agent.md",
            "C:agent.md",
            "manifest.yml",
            "Manifest.yml",
            "claims.yml/agent.md",
        ],
    )
    def test_rejects_unsafe_research_agent_paths(
        self, canonical_schema: dict[str, Any], path: str
    ) -> None:
        model = to_dict(build_worked_example())
        model["research_agent"] = {
            "path": path,
            "model": "m",
            "grounding_sources": ["agent/context.md"],
        }
        assert "/research_agent/path" in schema_errors(canonical_schema, model)

    @pytest.mark.parametrize(
        "paper",
        [
            {"pdf": ""},
            {"pdf": "   "},
            {"source": ""},
            {"pdf": "../paper.pdf"},
            {"pdf": "..\\paper.pdf"},
            {"source": "C:paper.tex"},
            {"claims_export": "../claims.yml", "source": "paper.tex"},
            {"references_export": "claims.yml", "source": "paper.tex"},
        ],
    )
    def test_rejects_unsafe_paper_paths(
        self, canonical_schema: dict[str, Any], paper: dict[str, str]
    ) -> None:
        model = to_dict(build_worked_example())
        model["paper"] = paper
        assert any(
            path.startswith("/paper/") for path in schema_errors(canonical_schema, model)
        )

    @pytest.mark.parametrize(
        "directory",
        ["../escape", "claims.yml", "claims.yml/child", ".sdk", ".SDK/child", "C:agent"],
    )
    def test_rejects_unsafe_experiment_directories(
        self, canonical_schema: dict[str, Any], directory: str
    ) -> None:
        model = to_dict(build_worked_example())
        model["experiments"][0]["directory"] = directory
        assert "/experiments/0/directory" in schema_errors(canonical_schema, model)

    @pytest.mark.parametrize("evidence", ["claims.yml", "claims.yml\\child", "..\\evidence.csv"])
    def test_rejects_unsafe_result_evidence(
        self, canonical_schema: dict[str, Any], evidence: str
    ) -> None:
        model = to_dict(build_worked_example())
        model["results"][0]["evidence"] = evidence
        assert "/results/0/evidence" in schema_errors(canonical_schema, model)

    def test_accepts_nested_extension_keys(self, canonical_schema: dict[str, Any]) -> None:
        model = copy.deepcopy(to_dict(build_worked_example()))
        model["claims"][0]["x_confidence"] = 0.75
        model["results"][0]["x_units"] = "percent"
        assert schema_errors(canonical_schema, model) == []


class TestValidatorVariantsRoundTrip:
    def test_every_validator_kind_survives_write_and_reopen(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        add_result(artifact, Result(id="R1", validates=["C1"], evidence="e.csv", kind="metrics"))
        add_claim(
            artifact,
            Claim(
                id="C1",
                statement="s",
                validators=[
                    AttestValidator(id="v_attest", checks="provenance", inputs=["R1"]),
                    BuiltinValidator(
                        id="v_builtin",
                        name="numeric_close",
                        input={"result": "R1"},
                        params={"tolerance": 0.01},
                        gated_by="v_attest",
                    ),
                    LlmJudgeValidator(id="v_judge", criteria="c", inputs=["R1"]),
                ],
            ),
        )
        write_submission(artifact, out_dir)
        reopened = open_submission(out_dir)
        kinds = [validator.kind for validator in reopened.claims[0].validators]
        assert kinds == ["attest", "builtin", "llm_judge"]
        builtin = reopened.claims[0].validators[1]
        assert isinstance(builtin, BuiltinValidator)
        assert builtin.params == {"tolerance": 0.01}
        assert builtin.gated_by == "v_attest"
