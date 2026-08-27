"""Serialization, staging, integrity and reopening — mirrors ``test/serialize.test.ts``."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from universal_artifact_sdk import (
    Assessment,
    AttestValidator,
    BuiltinValidator,
    ChangeContext,
    Claim,
    Dataset,
    Exhibit,
    Experiment,
    ExternalLocation,
    Paper,
    ResearchAgent,
    Result,
    RunSpec,
    StructuralError,
    StudyMetadata,
    SubmissionReport,
    Trace,
    WriteOptions,
    abandon_experiment,
    add_assessment,
    add_claim,
    add_dataset,
    add_exhibit,
    add_experiment,
    add_result,
    add_trace,
    artifact_from_dict,
    attach_paper,
    attach_research_agent,
    create_artifact,
    open_submission,
    read_yaml,
    set_reflection,
    to_dict,
    write_submission,
)


def state_of(out_dir: Path) -> dict[str, object]:
    return json.loads((out_dir / ".sdk" / "state.json").read_text(encoding="utf-8"))


class TestGeneratedIndexes:
    def test_writes_assessments_and_indexes_them_in_the_manifest(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        add_assessment(
            artifact,
            Assessment(
                id="A1",
                dimension="citation_integrity",
                scope="paper",
                evidence=["paper_references.yml"],
            ),
        )
        write_submission(artifact, out_dir)
        assert (out_dir / "assessments.yml").is_file()
        document = read_yaml(out_dir / "assessments.yml")
        assert document["assessments"][0]["dimension"] == "citation_integrity"
        manifest = read_yaml(out_dir / "manifest.yml")
        assert manifest["paths"]["assessments"] == "assessments.yml"

    def test_omits_optional_indexes_when_the_collections_are_empty(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        write_submission(artifact, out_dir)
        for name in ("traces.yml", "assessments.yml", "exhibits.yml", "journal.yml"):
            assert not (out_dir / name).exists()
        manifest = read_yaml(out_dir / "manifest.yml")
        assert set(manifest["paths"]) == {"claims", "results", "datasets"}

    def test_writes_every_optional_index_when_populated(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="C1", statement="s"), ctx=ChangeContext(rationale="why"))
        add_trace(artifact, Trace(id="T1", kind="execution_log", path="traces/t.log"))
        add_exhibit(
            artifact,
            Exhibit(id="X1", type="proof", caption="c", validates=["C1"], statement="QED"),
        )
        add_assessment(artifact, Assessment(id="A1", dimension="d", scope="paper"))
        write_submission(artifact, out_dir)
        manifest = read_yaml(out_dir / "manifest.yml")
        assert manifest["paths"] == {
            "claims": "claims.yml",
            "results": "results.yml",
            "datasets": "datasets.yml",
            "traces": "traces.yml",
            "exhibits": "exhibits.yml",
            "assessments": "assessments.yml",
            "journal": "journal.yml",
        }

    def test_writes_reflection_when_the_model_carries_it(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        set_reflection(artifact, "# limitations\nsmall sample.\n")
        write_submission(artifact, out_dir)
        assert "small sample" in (out_dir / "reflection.md").read_text(encoding="utf-8")
        assert "reflection.md" in state_of(out_dir)["generated_files"]  # type: ignore[operator]

    def test_marks_every_generated_document(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        write_submission(artifact, out_dir)
        for name in ("manifest.yml", "claims.yml", "results.yml", "datasets.yml"):
            assert read_yaml(out_dir / name)["_generated"].startswith("artifact-sdk/v1")


class TestMissingBlobs:
    def _artifact_with_absent_evidence(self) -> object:
        artifact = create_artifact(id="x", title="t")
        add_result(
            artifact,
            Result(id="R1", validates=["C1"], evidence="evidence/never.csv", kind="metrics"),
        )
        add_claim(artifact, Claim(id="C1", statement="s"))
        return artifact

    def test_reports_incomplete_with_a_missing_blob_warning(self, out_dir: Path) -> None:
        report = write_submission(self._artifact_with_absent_evidence(), out_dir)  # type: ignore[arg-type]
        assert report.incomplete is True
        assert "evidence/never.csv" in report.missing_blobs
        assert any("incomplete" in issue.message for issue in report.warnings)
        assert any(issue.path == "blob[evidence/never.csv]" for issue in report.warnings)

    def test_quiet_clears_only_the_incomplete_flag(self, out_dir: Path) -> None:
        report = write_submission(
            self._artifact_with_absent_evidence(), out_dir, quiet=True  # type: ignore[arg-type]
        )
        assert report.incomplete is False
        assert report.missing_blobs == ["evidence/never.csv"]
        assert any(issue.path == "blob[evidence/never.csv]" for issue in report.warnings)

    def test_stage_from_reports_blobs_absent_from_the_source_root(
        self, out_dir: Path, source_dir: Path
    ) -> None:
        report = write_submission(
            self._artifact_with_absent_evidence(), out_dir, stage_from=source_dir  # type: ignore[arg-type]
        )
        assert "evidence/never.csv" in report.missing_blobs
        assert report.incomplete is True

    def test_reports_missing_grounding_sources_even_when_stale_output_exists(
        self, out_dir: Path, source_dir: Path
    ) -> None:
        artifact = create_artifact(id="x", title="t")
        attach_research_agent(
            artifact,
            ResearchAgent(
                path="research-agent.md", model="m", grounding_sources=["agent/context.md"]
            ),
        )
        (source_dir / "research-agent.md").write_text("persona", encoding="utf-8")
        (out_dir / "agent").mkdir()
        (out_dir / "agent" / "context.md").write_text("stale", encoding="utf-8")
        report = write_submission(artifact, out_dir, stage_from=source_dir)
        assert "agent/context.md" in report.missing_blobs
        assert report.incomplete is True
        assert any(issue.path == "blob[agent/context.md]" for issue in report.warnings)

    def test_does_not_report_exact_generated_grounding_sources_as_missing(
        self, out_dir: Path, source_dir: Path
    ) -> None:
        artifact = create_artifact(id="x", title="t")
        attach_research_agent(
            artifact,
            ResearchAgent(
                path="research-agent.md",
                model="m",
                grounding_sources=["claims.yml", "Claims.yml"],
            ),
        )
        (source_dir / "research-agent.md").write_text("persona", encoding="utf-8")
        report = write_submission(artifact, out_dir, stage_from=source_dir)
        assert report.missing_blobs == []
        assert not any(issue.path.startswith("blob[") for issue in report.warnings)


class TestWriteTimeRejection:
    @pytest.mark.parametrize("evidence", ["../outside.csv", "C:secret.csv", "claims.yml"])
    def test_rejects_invalid_blob_references_before_writing(
        self, evidence: str, out_dir: Path, source_dir: Path
    ) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="C1", statement="s"))
        add_result(artifact, Result(id="R1", validates=["C1"], evidence=evidence, kind="metrics"))
        with pytest.raises(StructuralError, match=r"result\[R1\]\.evidence"):
            write_submission(artifact, out_dir, stage_from=source_dir)
        assert not (out_dir / "manifest.yml").exists()

    def test_structural_error_carries_the_issue_list(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        add_result(artifact, Result(id="R1", validates=["ghost"], evidence="e", kind="metrics"))
        with pytest.raises(StructuralError) as raised:
            write_submission(artifact, out_dir)
        assert [issue.path for issue in raised.value.issues] == ["result[R1].validates"]

    def test_rejects_authored_blobs_colliding_with_disposition_markers(
        self, out_dir: Path
    ) -> None:
        artifact = create_artifact(id="x", title="t")
        add_experiment(
            artifact,
            Experiment(slug="e", directory="experiments/e", run=RunSpec(command="true")),
        )
        abandon_experiment(artifact, "e", ctx=ChangeContext(rationale="not useful"))
        add_claim(artifact, Claim(id="C1", statement="s"))
        add_result(
            artifact,
            Result(
                id="R1",
                validates=["C1"],
                evidence="experiments/e/DISPOSITION.md",
                kind="metrics",
            ),
        )
        with pytest.raises(StructuralError, match="generated disposition marker"):
            write_submission(artifact, out_dir)

    def test_rejects_disposition_directories_that_shadow_authored_blobs(
        self, out_dir: Path
    ) -> None:
        artifact = create_artifact(id="x", title="t")
        attach_paper(artifact, Paper(pdf="paper.pdf"))
        add_experiment(
            artifact, Experiment(slug="paper", directory="paper.pdf", run=RunSpec(command="true"))
        )
        abandon_experiment(artifact, "paper", ctx=ChangeContext(rationale="not useful"))
        with pytest.raises(StructuralError, match=r"collides with authored blob paper\.pdf"):
            write_submission(artifact, out_dir)

    @pytest.mark.parametrize(
        "directory", ["../escape", "claims.yml", "claims.yml/child", ".sdk", ".SDK/child"]
    )
    def test_rejects_unsafe_disposition_marker_directories(
        self, directory: str, out_dir: Path
    ) -> None:
        artifact = create_artifact(id="x", title="t")
        add_experiment(
            artifact, Experiment(slug="bad", directory=directory, run=RunSpec(command="true"))
        )
        abandon_experiment(artifact, "bad", ctx=ChangeContext(rationale="not useful"))
        with pytest.raises(StructuralError, match=r"experiment\[bad\]\.directory"):
            write_submission(artifact, out_dir)

    def test_rejects_research_agent_paths_outside_the_submission_root(
        self, out_dir: Path, source_dir: Path
    ) -> None:
        artifact = create_artifact(id="x", title="t")
        attach_research_agent(
            artifact,
            ResearchAgent(
                path="../escaped-agent.md", model="m", grounding_sources=["claims.yml"]
            ),
        )
        with pytest.raises(StructuralError, match="research_agent.path"):
            write_submission(artifact, out_dir, stage_from=source_dir)


class TestFileClassification:
    def test_records_generated_and_authored_files(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        (out_dir / "note.txt").write_text("hello", encoding="utf-8")
        write_submission(artifact, out_dir)
        state = state_of(out_dir)
        assert "manifest.yml" in state["generated_files"]  # type: ignore[operator]
        assert "claims.yml" in state["generated_files"]  # type: ignore[operator]
        assert "note.txt" in state["authored_files"]  # type: ignore[operator]
        assert "note.txt" not in state["generated_files"]  # type: ignore[operator]

    def test_classifies_staged_blobs_as_authored(self, out_dir: Path, source_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="C1", statement="s"))
        add_result(
            artifact,
            Result(id="R1", validates=["C1"], evidence="evidence/metrics.csv", kind="metrics"),
        )
        (source_dir / "evidence").mkdir()
        (source_dir / "evidence" / "metrics.csv").write_text("metric,value\n", encoding="utf-8")
        report = write_submission(artifact, out_dir, stage_from=source_dir)
        assert report.missing_blobs == []
        state = state_of(out_dir)
        assert "evidence/metrics.csv" in state["authored_files"]  # type: ignore[operator]
        assert "evidence/metrics.csv" not in state["generated_files"]  # type: ignore[operator]
        assert "manifest.yml" in state["generated_files"]  # type: ignore[operator]
        assert "evidence/metrics.csv" in report.files_written

    def test_staging_replaces_an_existing_destination(
        self, out_dir: Path, source_dir: Path
    ) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="C1", statement="s"))
        add_result(
            artifact, Result(id="R1", validates=["C1"], evidence="result.txt", kind="metrics")
        )
        (source_dir / "result.txt").write_text("new", encoding="utf-8")
        (out_dir / "result.txt").write_text("old", encoding="utf-8")
        write_submission(artifact, out_dir, stage_from=source_dir)
        assert (out_dir / "result.txt").read_text(encoding="utf-8") == "new"

    def test_stages_a_referenced_directory_recursively(
        self, out_dir: Path, source_dir: Path
    ) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="C1", statement="s"))
        add_result(
            artifact, Result(id="R1", validates=["C1"], evidence="data/", kind="transcript")
        )
        (source_dir / "data" / "nested").mkdir(parents=True)
        (source_dir / "data" / "a.txt").write_text("a", encoding="utf-8")
        (source_dir / "data" / "nested" / "b.txt").write_text("b", encoding="utf-8")
        report = write_submission(artifact, out_dir, stage_from=source_dir)
        assert report.missing_blobs == []
        assert "data/a.txt" in report.files_written
        assert "data/nested/b.txt" in report.files_written
        assert "data/nested/b.txt" in state_of(out_dir)["authored_files"]  # type: ignore[operator]

    def test_staging_never_deletes_a_destination_of_the_opposite_type(
        self, out_dir: Path, source_dir: Path
    ) -> None:
        # The destination may hold authored content, so a directory/file mismatch fails
        # rather than replacing the tree.
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="C1", statement="s"))
        add_result(
            artifact, Result(id="R1", validates=["C1"], evidence="blob", kind="metrics")
        )
        (source_dir / "blob").write_text("new", encoding="utf-8")
        (out_dir / "blob" / "keep").mkdir(parents=True)
        (out_dir / "blob" / "keep" / "important.txt").write_text("keep me", encoding="utf-8")
        with pytest.raises(IsADirectoryError):
            write_submission(artifact, out_dir, stage_from=source_dir)
        assert (out_dir / "blob" / "keep" / "important.txt").is_file()
        assert not (out_dir / "blob" / "blob").exists()

    def test_staging_a_directory_never_replaces_an_authored_file(
        self, out_dir: Path, source_dir: Path
    ) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="C1", statement="s"))
        add_result(
            artifact, Result(id="R1", validates=["C1"], evidence="blob/", kind="transcript")
        )
        (source_dir / "blob").mkdir()
        (source_dir / "blob" / "a.txt").write_text("a", encoding="utf-8")
        (out_dir / "blob").write_text("authored", encoding="utf-8")
        with pytest.raises(NotADirectoryError):
            write_submission(artifact, out_dir, stage_from=source_dir)
        assert (out_dir / "blob").read_text(encoding="utf-8") == "authored"

    def test_stale_optional_index_is_reclassified_as_authored(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="C1", statement="s"))
        add_exhibit(
            artifact,
            Exhibit(id="X1", type="proof", caption="c", validates=["C1"], statement="QED"),
        )
        write_submission(artifact, out_dir)
        assert "exhibits.yml" in state_of(out_dir)["generated_files"]  # type: ignore[operator]
        artifact.exhibits.clear()
        write_submission(artifact, out_dir)
        state = state_of(out_dir)
        assert (out_dir / "exhibits.yml").is_file()
        assert "exhibits.yml" in state["authored_files"]  # type: ignore[operator]
        assert "exhibits.yml" not in state["generated_files"]  # type: ignore[operator]
        assert "exhibits.yml" in (out_dir / "SHA256SUMS").read_text(encoding="utf-8")


class TestIntegrity:
    def test_sha256sums_covers_every_shipped_file_but_itself(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        set_reflection(artifact, "notes")
        write_submission(artifact, out_dir)
        sums = (out_dir / "SHA256SUMS").read_text(encoding="utf-8")
        listed = {line.split("  ", 1)[1] for line in sums.splitlines() if line}
        assert listed == {
            "claims.yml",
            "datasets.yml",
            "journal.yml",
            "manifest.yml",
            "reflection.md",
            "results.yml",
        }
        assert sums.endswith("\n")

    def test_state_json_is_not_hashed_and_ends_with_a_newline(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        write_submission(artifact, out_dir)
        assert ".sdk/state.json" not in (out_dir / "SHA256SUMS").read_text(encoding="utf-8")
        assert (out_dir / ".sdk" / "state.json").read_text(encoding="utf-8").endswith("\n")


class TestIdempotency:
    def test_re_emitting_an_unchanged_artifact_produces_identical_bytes(
        self, out_dir: Path
    ) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(
            artifact,
            Claim(id="C1", statement="s", validators=[AttestValidator(checks="integrity")]),
        )
        attach_paper(artifact, Paper(pdf="paper.pdf"))
        names = ("manifest.yml", "claims.yml", "SHA256SUMS", ".sdk/state.json")
        write_submission(artifact, out_dir)
        first = {name: (out_dir / name).read_text(encoding="utf-8") for name in names}
        write_submission(artifact, out_dir)
        second = {name: (out_dir / name).read_text(encoding="utf-8") for name in names}
        assert second == first

    def test_write_open_write_is_idempotent(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(
            artifact,
            Claim(id="C1", statement="s", validators=[AttestValidator(checks="integrity")]),
        )
        set_reflection(artifact, "# reflection\n")
        write_submission(artifact, out_dir)
        first = (out_dir / "manifest.yml").read_text(encoding="utf-8")
        write_submission(open_submission(out_dir), out_dir)
        assert (out_dir / "manifest.yml").read_text(encoding="utf-8") == first


class TestOpaqueMapNulls:
    """A null *value* inside a producer-authored map is data, not an absent field."""

    def _artifact_with_nulls(self) -> object:
        artifact = create_artifact(
            id="nulls", title="t", producer={"name": "p", "orcid": None}
        )
        add_experiment(
            artifact,
            Experiment(
                slug="e1",
                directory="experiments/e1",
                run=RunSpec(command="run", env={"SEED": "1", "TOKEN": None}),  # type: ignore[dict-item]
            ),
        )
        add_trace(
            artifact,
            Trace(
                id="T1",
                kind="execution_log",
                path="traces/t.log",
                counters={"steps": 3, "cost_usd": None},  # type: ignore[dict-item]
            ),
        )
        add_result(
            artifact,
            Result(
                id="R1",
                validates=["C1"],
                evidence="results/out.csv",
                kind="metrics",
                locators={"accuracy": {"column": "acc", "row": None}},
            ),
        )
        add_claim(
            artifact,
            Claim(
                id="C1",
                statement="s",
                validators=[
                    BuiltinValidator(
                        name="numeric_close",
                        input={"result": "R1", "locator": None},
                        params={"tolerance": 0.01, "unit": None},
                    )
                ],
            ),
        )
        return artifact

    def test_nulls_are_written_verbatim(self, out_dir: Path) -> None:
        write_submission(self._artifact_with_nulls(), out_dir, quiet=True)  # type: ignore[arg-type]
        manifest = read_yaml(out_dir / "manifest.yml")
        assert manifest["producer"] == {"name": "p", "orcid": None}
        assert manifest["experiments"][0]["run"]["env"] == {"SEED": "1", "TOKEN": None}
        assert read_yaml(out_dir / "traces.yml")["traces"][0]["counters"] == {
            "steps": 3,
            "cost_usd": None,
        }
        result = read_yaml(out_dir / "results.yml")["results"][0]
        assert result["locators"] == {"accuracy": {"column": "acc", "row": None}}
        validator = read_yaml(out_dir / "claims.yml")["claims"][0]["validators"][0]
        assert validator["input"] == {"result": "R1", "locator": None}
        assert validator["params"] == {"tolerance": 0.01, "unit": None}

    def test_nulls_survive_reopen_and_rewrite(self, out_dir: Path) -> None:
        write_submission(self._artifact_with_nulls(), out_dir, quiet=True)  # type: ignore[arg-type]
        first = (out_dir / "manifest.yml").read_text(encoding="utf-8")

        reopened = open_submission(out_dir)
        assert reopened.producer == {"name": "p", "orcid": None}
        assert reopened.experiments[0].run.env == {"SEED": "1", "TOKEN": None}
        assert reopened.traces[0].counters == {"steps": 3, "cost_usd": None}
        assert reopened.results[0].locators == {"accuracy": {"column": "acc", "row": None}}
        validator = reopened.claims[0].validators[0]
        assert isinstance(validator, BuiltinValidator)
        assert validator.input == {"result": "R1", "locator": None}
        assert validator.params == {"tolerance": 0.01, "unit": None}

        write_submission(reopened, out_dir, quiet=True)
        assert (out_dir / "manifest.yml").read_text(encoding="utf-8") == first
        assert read_yaml(out_dir / "manifest.yml")["producer"] == {"name": "p", "orcid": None}

    def test_an_optional_model_field_is_still_omitted(self, out_dir: Path) -> None:
        artifact = create_artifact(id="nulls", title="t")
        add_claim(artifact, Claim(id="C1", statement="s"))
        add_result(
            artifact,
            Result(
                id="R1",
                validates=["C1"],
                evidence="results/out.csv",
                kind="metrics",
                locators=None,
                supersedes=None,
            ),
        )
        write_submission(artifact, out_dir, quiet=True)
        stored = read_yaml(out_dir / "results.yml")["results"][0]
        assert "locators" not in stored and "supersedes" not in stored


class TestWriteOptions:
    def test_options_object_and_keywords_agree(self, out_dir: Path, source_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="C1", statement="s"))
        options = WriteOptions(stage_from=source_dir, quiet=True)
        report = write_submission(artifact, out_dir, options)
        assert isinstance(report, SubmissionReport)
        assert report.incomplete is False
        assert options.stage_from == source_dir and options.quiet is True

    def test_keywords_override_the_options_object(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="C1", statement="s"))
        options = WriteOptions(quiet=True)
        report = write_submission(artifact, out_dir, options, quiet=False)
        assert report.incomplete is True
        assert options.quiet is True

    def test_report_shape(self, out_dir: Path) -> None:
        report = write_submission(create_artifact(id="x", title="t"), out_dir)
        assert report.out_dir == str(out_dir)
        assert report.ok is True
        assert report.missing_blobs == []
        assert report.files_written == sorted(report.files_written)


class TestOpenSubmission:
    def test_raises_when_there_is_no_manifest(self, out_dir: Path) -> None:
        with pytest.raises(FileNotFoundError, match="no manifest.yml"):
            open_submission(out_dir)

    def test_reopens_a_minimal_submission(self, out_dir: Path) -> None:
        artifact = create_artifact(id="min", title="t")
        add_claim(artifact, Claim(id="C1", statement="s"))
        write_submission(artifact, out_dir)
        reopened = open_submission(out_dir)
        assert reopened.id == "min"
        assert len(reopened.claims) == 1
        assert reopened.traces == []
        assert reopened.assessments == []
        assert reopened.paper is None
        assert reopened.reflection is None
        assert reopened.journal_config is None

    def test_round_trips_reflection_and_paper(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        set_reflection(artifact, "# reflection\n")
        attach_paper(artifact, Paper(pdf="paper.pdf", references_export="paper_references.yml"))
        write_submission(artifact, out_dir)
        reopened = open_submission(out_dir)
        assert reopened.reflection is not None and "reflection" in reopened.reflection
        assert reopened.paper is not None
        assert reopened.paper.references_export == "paper_references.yml"

    def test_tolerates_a_manifest_without_a_paths_index(self, out_dir: Path) -> None:
        (out_dir / "manifest.yml").write_text(
            "format_version: evaluable-artifact/v2\nid: hand\ntitle: Hand-written\n",
            encoding="utf-8",
        )
        reopened = open_submission(out_dir)
        assert reopened.id == "hand"
        assert reopened.title == "Hand-written"
        assert reopened.datasets == []
        assert reopened.results == []
        assert reopened.claims == []

    def test_an_index_mapped_to_an_empty_path_is_not_read(self, out_dir: Path) -> None:
        (out_dir / "manifest.yml").write_text(
            "format_version: ''\nid: empty\ntitle: Empty\npaths:\n  claims: ''\n",
            encoding="utf-8",
        )
        (out_dir / "claims.yml").write_text(
            "claims:\n  - id: C1\n    statement: s\n", encoding="utf-8"
        )
        reopened = open_submission(out_dir)
        assert reopened.claims == []
        # An explicitly empty version is kept rather than defaulted.
        assert reopened.format_version == ""

    def test_resolves_a_relocated_index_through_the_paths_map(self, out_dir: Path) -> None:
        (out_dir / "manifest.yml").write_text(
            "id: relocated\ntitle: Relocated\npaths:\n  claims: indexes/claims.yml\n",
            encoding="utf-8",
        )
        (out_dir / "indexes").mkdir()
        (out_dir / "indexes" / "claims.yml").write_text(
            "claims:\n  - id: C1\n    statement: s\n", encoding="utf-8"
        )
        reopened = open_submission(out_dir)
        assert [claim.id for claim in reopened.claims] == ["C1"]

    def test_drops_unknown_top_level_keys_and_keeps_nested_extensions(
        self, out_dir: Path
    ) -> None:
        artifact = create_artifact(id="x", title="t", producer={"extension": "kept"})
        write_submission(artifact, out_dir)
        manifest = out_dir / "manifest.yml"
        manifest.write_text(
            manifest.read_text(encoding="utf-8") + "root_extension: dropped\n", encoding="utf-8"
        )
        reopened = open_submission(out_dir)
        assert reopened.producer == {"extension": "kept"}
        assert not hasattr(reopened, "root_extension")


#: A `study` block whose spec-defined `extra` sub-map (SPEC §2.7, resolved §11 Q14) sits
#: alongside an unknown sibling key that only the extension bucket can carry.
STUDY_EXTRA = {
    "data_use_agreement": "DUA-99",
    "venue": {"ethics_track": "PARITY'26", "reviewers": 2, "waivers": ["audio-retention"]},
}
STUDY_DOCUMENT = {
    "ethics_approval": "IRB-2026-0001",
    "consent_basis": "informed, opt-in",
    "extra": STUDY_EXTRA,
    "x_board": "internal",
}


def study_dataset() -> Dataset:
    """A dataset with no blob to stage, so writes never report a missing file."""
    return Dataset(
        id="corpus",
        location=ExternalLocation(uri="https://example.test/corpus.zip", sha256="a" * 64),
        study=StudyMetadata(
            ethics_approval="IRB-2026-0001",
            consent_basis="informed, opt-in",
            extra=dict(STUDY_EXTRA),
            extensions={"x_board": "internal"},
        ),
    )


class TestStudyMetadataExtra:
    """`study.extra` is a contract field, not this binding's unknown-key bucket.

    Every other nested model overflows unrecognized sibling keys into an ``extra``
    attribute that serialization flattens back into siblings. `StudyMetadata.extra` is a
    spec-defined nested map, so it is emitted as ``extra:`` and unknown siblings overflow
    into ``extensions`` instead (``model.extension_field``).
    """

    def test_to_dict_nests_extra_and_flattens_the_extension_bucket(self) -> None:
        study = study_dataset().study
        assert study is not None
        assert to_dict(study) == STUDY_DOCUMENT

    def test_from_dict_splits_extra_from_unknown_siblings(self) -> None:
        dataset = artifact_from_dict({"datasets": [{"id": "corpus", "study": STUDY_DOCUMENT}]})
        study = dataset.datasets[0].study
        assert study is not None
        assert study.extra == STUDY_EXTRA
        assert study.extensions == {"x_board": "internal"}
        assert not hasattr(study, "x_board")

    def test_an_unauthored_extra_is_omitted_rather_than_emitted_empty(self) -> None:
        study = StudyMetadata(ethics_approval="IRB-1")
        assert study.extra is None
        assert to_dict(study) == {"ethics_approval": "IRB-1"}

    def test_round_trips_through_write_open_write(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        add_dataset(artifact, study_dataset())
        write_submission(artifact, out_dir)
        written = read_yaml(out_dir / "datasets.yml")["datasets"][0]["study"]
        assert written == STUDY_DOCUMENT

        reopened = open_submission(out_dir)
        study = reopened.datasets[0].study
        assert study is not None
        assert study.extra == STUDY_EXTRA
        assert study.extensions == {"x_board": "internal"}

        write_submission(reopened, out_dir)
        rewritten = read_yaml(out_dir / "datasets.yml")["datasets"][0]["study"]
        assert rewritten == STUDY_DOCUMENT

    def test_an_extension_can_never_shadow_extra(self) -> None:
        """The bucket is merged first, so a stray `extra` sibling loses to the field."""
        study = StudyMetadata(extra={"kept": True}, extensions={"extra": {"shadow": True}})
        assert to_dict(study) == {"extra": {"kept": True}}


class TestGenericModelExtensions:
    """Models that keep `extra` as their bucket are unchanged by the study split."""

    def test_neighbouring_models_still_flatten_unknown_keys(self, out_dir: Path) -> None:
        artifact = artifact_from_dict(
            {
                "id": "x",
                "title": "t",
                "environment": {
                    "name": "primary",
                    "image": {"reference": "registry.test/a:1", "x_registry": "internal"},
                    "x_provisioner": "terraform",
                },
                "datasets": [
                    {
                        "id": "corpus",
                        "location": {
                            "kind": "external",
                            "uri": "https://example.test/corpus.zip",
                            "sha256": "a" * 64,
                            "x_mirror": "s3://example",
                        },
                        "x_owner": "data-team",
                    }
                ],
                "experiments": [
                    {
                        "slug": "e1",
                        "directory": "experiments/e1",
                        "run": {"command": "python run.py", "x_scheduler": "slurm"},
                        "runs_in": "primary",
                    }
                ],
            }
        )
        environment = artifact.environment
        assert environment is not None
        assert environment.extra == {"x_provisioner": "terraform"}
        assert environment.image.extra == {"x_registry": "internal"}
        assert artifact.datasets[0].extra == {"x_owner": "data-team"}
        assert artifact.experiments[0].run.extra == {"x_scheduler": "slurm"}

        write_submission(artifact, out_dir)
        manifest = read_yaml(out_dir / "manifest.yml")
        assert manifest["environment"]["x_provisioner"] == "terraform"
        assert manifest["environment"]["image"]["x_registry"] == "internal"
        assert manifest["experiments"][0]["run"]["x_scheduler"] == "slurm"
        assert read_yaml(out_dir / "datasets.yml")["datasets"][0]["x_owner"] == "data-team"
