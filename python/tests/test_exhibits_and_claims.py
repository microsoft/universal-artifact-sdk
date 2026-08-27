"""Exhibits, claim stance and the evidence inventory.

Mirrors ``test/exhibits.test.ts`` and ``test/claim-stance.test.ts``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from universal_artifact_sdk import (
    Artifact,
    AttestValidator,
    Claim,
    Dataset,
    Exhibit,
    Experiment,
    ExternalLocation,
    Failure,
    InArtifactLocation,
    Paper,
    Result,
    RunSpec,
    Trace,
    add_claim,
    add_dataset,
    add_exhibit,
    add_experiment,
    add_result,
    add_trace,
    attach_paper,
    attach_research_agent,
    compute_evidence_inventory,
    create_artifact,
    default_exhibit_validation_mode,
    fail_experiment,
    get_claim,
    get_exhibit,
    list_exhibits,
    open_submission,
    read_yaml,
    remove_exhibit,
    validate_structure,
    write_submission,
)
from universal_artifact_sdk.model import ChangeContext, ResearchAgent


def base_artifact() -> Artifact:
    artifact = create_artifact(id="art", title="Bloom FPR")
    add_experiment(
        artifact,
        Experiment(
            slug="fpr-sweep",
            directory="experiments/fpr_sweep",
            run=RunSpec(command="python run.py"),
        ),
    )
    add_claim(
        artifact,
        Claim(id="C4", statement="FPR is U-shaped in k with a minimum near k*."),
    )
    return artifact


def has_error(artifact: Artifact, fragment: str) -> bool:
    return any(
        fragment in f"{issue.path}: {issue.message}"
        for issue in validate_structure(artifact).errors
    )


def has_warning(artifact: Artifact, fragment: str) -> bool:
    return any(
        fragment in f"{issue.path}: {issue.message}"
        for issue in validate_structure(artifact).warnings
    )


class TestExhibitBuilder:
    def test_adds_gets_lists_and_removes(self) -> None:
        artifact = base_artifact()
        add_exhibit(
            artifact,
            Exhibit(
                id="X1",
                type="figure",
                caption="FPR vs k; U-shaped.",
                validates=["C4"],
                path="experiments/fpr_sweep/figure1.png",
            ),
        )
        assert [item.id for item in list_exhibits(artifact)] == ["X1"]
        exhibit = get_exhibit(artifact, "X1")
        assert exhibit is not None and exhibit.type == "figure"
        assert remove_exhibit(artifact, "X1") is True
        assert list_exhibits(artifact) == []
        assert remove_exhibit(artifact, "X1") is False

    def test_records_a_journal_entry(self) -> None:
        artifact = base_artifact()
        add_exhibit(
            artifact,
            Exhibit(id="X1", type="figure", caption="c", validates=["C4"], path="a/f.png"),
            ctx=ChangeContext(actor="producer", rationale="figure substantiates C4"),
        )
        entry = next(e for e in artifact.journal if e.target.kind == "exhibit")
        assert entry.target.id == "X1"
        assert entry.op == "add"
        assert entry.actor == "producer"


class TestExhibitSerialization:
    def test_writes_exhibits_and_indexes_them(self, out_dir: Path, source_dir: Path) -> None:
        artifact = base_artifact()
        (source_dir / "experiments" / "fpr_sweep").mkdir(parents=True)
        (source_dir / "experiments" / "fpr_sweep" / "figure1.png").write_text(
            "PNGDATA", encoding="utf-8"
        )
        add_exhibit(
            artifact,
            Exhibit(
                id="X1",
                type="figure",
                caption="FPR vs k; U-shaped.",
                validates=["C4"],
                path="experiments/fpr_sweep/figure1.png",
                produced_by="fpr-sweep",
                alt_text="Line plot of FPR against k.",
                order=1,
            ),
        )
        write_submission(artifact, out_dir, stage_from=source_dir)
        assert (out_dir / "exhibits.yml").is_file()
        assert (out_dir / "experiments" / "fpr_sweep" / "figure1.png").is_file()
        document = read_yaml(out_dir / "exhibits.yml")
        assert document["exhibits"][0]["id"] == "X1"
        assert document["exhibits"][0]["caption"] == "FPR vs k; U-shaped."
        manifest = read_yaml(out_dir / "manifest.yml")
        assert manifest["paths"]["exhibits"] == "exhibits.yml"
        assert manifest["evidence_inventory"]["has_exhibits"] is True
        assert manifest["evidence_inventory"]["exhibit_count"] == 1
        reopened = open_submission(out_dir)
        assert len(reopened.exhibits) == 1
        assert reopened.exhibits[0].alt_text == "Line plot of FPR against k."
        assert reopened.exhibits[0].order == 1

    def test_omits_exhibits_when_none_are_declared(self, out_dir: Path) -> None:
        write_submission(base_artifact(), out_dir)
        assert not (out_dir / "exhibits.yml").exists()
        manifest = read_yaml(out_dir / "manifest.yml")
        assert "exhibits" not in manifest["paths"]
        assert manifest["evidence_inventory"]["has_exhibits"] is False
        assert manifest["evidence_inventory"]["exhibit_count"] == 0

    def test_touching_the_exhibit_api_does_not_change_output(self, tmp_path: Path) -> None:
        untouched = tmp_path / "untouched"
        touched = tmp_path / "touched"
        write_submission(base_artifact(), untouched)
        artifact = base_artifact()
        add_exhibit(
            artifact,
            Exhibit(id="X1", type="figure", caption="c", validates=["C4"], path="a/f.png"),
        )
        remove_exhibit(artifact, "X1")
        write_submission(artifact, touched)
        assert (touched / "manifest.yml").read_text(encoding="utf-8") == (
            untouched / "manifest.yml"
        ).read_text(encoding="utf-8")


class TestExhibitValidation:
    def test_requires_id_type_caption_and_path(self) -> None:
        artifact = base_artifact()
        artifact.exhibits.append(Exhibit(id="", type="", caption="  ", validates=["C4"]))
        assert has_error(artifact, "exhibit requires `type`")
        assert has_error(artifact, "exhibit requires a non-empty `caption`")
        assert has_error(artifact, "exhibit requires `path`")

    def test_flags_dangling_references(self) -> None:
        artifact = base_artifact()
        add_exhibit(
            artifact,
            Exhibit(
                id="X1",
                type="figure",
                caption="c",
                validates=["C_missing"],
                path="a/f.png",
                produced_by="no-such-exp",
                from_result="R_missing",
            ),
        )
        assert has_error(artifact, "references unknown claim 'C_missing'")
        assert has_error(artifact, "references unknown experiment 'no-such-exp'")
        assert has_error(artifact, "references unknown result 'R_missing'")

    def test_resolves_a_valid_from_result_cross_link(self) -> None:
        artifact = base_artifact()
        add_result(
            artifact,
            Result(
                id="R1",
                validates=["C4"],
                evidence="experiments/fpr_sweep/data.csv",
                kind="metrics",
            ),
        )
        add_exhibit(
            artifact,
            Exhibit(
                id="X1",
                type="figure",
                caption="c",
                validates=["C4"],
                path="a/f.png",
                from_result="R1",
            ),
        )
        assert has_error(artifact, "exhibit[X1]") is False

    def test_rejects_a_path_that_collides_with_a_generated_file(self) -> None:
        artifact = base_artifact()
        add_exhibit(
            artifact,
            Exhibit(id="X1", type="table", caption="c", validates=["C4"], path="exhibits.yml"),
        )
        assert has_error(artifact, "collide with SDK-generated files")

    def test_accepts_a_statement_only_proof(self) -> None:
        artifact = base_artifact()
        add_exhibit(
            artifact,
            Exhibit(
                id="X1",
                type="proof",
                caption="Soundness of the FPR bound.",
                validates=["C4"],
                statement="For all k, FPR(k) >= (1 - e^{-kn/m})^k.",
            ),
        )
        assert has_error(artifact, "exhibit[X1]") is False

    @pytest.mark.parametrize("exhibit_type", ["figure", "proof", "table"])
    def test_requires_path_or_statement(self, exhibit_type: str) -> None:
        artifact = base_artifact()
        add_exhibit(artifact, Exhibit(id="X1", type=exhibit_type, caption="c", validates=["C4"]))
        assert has_error(artifact, "exhibit requires `path`")

    def test_rejects_an_illegal_validation_mode(self) -> None:
        artifact = base_artifact()
        add_exhibit(
            artifact,
            Exhibit(
                id="X1",
                type="figure",
                caption="c",
                validates=["C4"],
                path="a/f.png",
                validation_mode="vibes",
            ),
        )
        assert has_error(artifact, "illegal validation_mode 'vibes'")

    def test_warns_on_an_unrecognized_type(self) -> None:
        artifact = base_artifact()
        add_exhibit(
            artifact,
            Exhibit(id="X1", type="hologram", caption="c", validates=["C4"], path="a/f.png"),
        )
        assert has_warning(artifact, "unrecognized exhibit type 'hologram'")
        assert has_error(artifact, "exhibit[X1].type") is False

    def test_detects_self_dependencies_and_cycles(self) -> None:
        selfish = base_artifact()
        add_exhibit(
            selfish,
            Exhibit(
                id="X1",
                type="proof",
                caption="c",
                validates=["C4"],
                path="p/x1.md",
                depends_on=["X1"],
            ),
        )
        assert has_error(selfish, "exhibit cannot depend on itself")

        cyclic = base_artifact()
        add_exhibit(
            cyclic,
            Exhibit(
                id="X1",
                type="proof",
                caption="c",
                validates=["C4"],
                path="p/x1.md",
                depends_on=["X2"],
            ),
        )
        add_exhibit(
            cyclic,
            Exhibit(
                id="X2",
                type="proof",
                caption="c",
                validates=["C4"],
                path="p/x2.md",
                depends_on=["X1"],
            ),
        )
        errors = [i for i in validate_structure(cyclic).errors if "cycle" in i.message]
        assert len(errors) == 1
        assert errors[0].message.endswith("X1 -> X2 -> X1") or errors[0].message.endswith(
            "X2 -> X1 -> X2"
        )

    def test_accepts_an_acyclic_proof_lemma_dag(self) -> None:
        artifact = base_artifact()
        add_exhibit(
            artifact,
            Exhibit(
                id="X1",
                type="proof",
                caption="Theorem 2.",
                validates=["C4"],
                path="p/thm.md",
                statement="E[FPR] >= (1/2)^k",
                depends_on=["X2"],
            ),
        )
        add_exhibit(
            artifact,
            Exhibit(
                id="X2",
                type="proof",
                caption="Lemma 1.",
                validates=["C4"],
                path="p/lemma.md",
                statement="...",
            ),
        )
        assert has_error(artifact, "exhibit[") is False

    def test_flags_a_dangling_dependency(self) -> None:
        artifact = base_artifact()
        add_exhibit(
            artifact,
            Exhibit(
                id="X1",
                type="proof",
                caption="c",
                validates=["C4"],
                path="p/x1.md",
                depends_on=["ghost"],
            ),
        )
        assert has_error(artifact, "references unknown exhibit 'ghost'")

    def test_default_exhibit_validation_mode_is_not_written_into_the_model(self) -> None:
        artifact = base_artifact()
        add_exhibit(
            artifact,
            Exhibit(id="X1", type="proof", caption="c", validates=["C4"], statement="QED"),
        )
        exhibit = get_exhibit(artifact, "X1")
        assert exhibit is not None and exhibit.validation_mode is None
        assert default_exhibit_validation_mode("proof") == "re-execute"


class TestClaimStance:
    def test_a_plain_claim_declares_no_stance(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(
            artifact,
            Claim(id="c1", statement="s", validators=[AttestValidator(checks="integrity")]),
        )
        claim = get_claim(artifact, "c1")
        assert claim is not None and claim.stance is None

    def test_records_an_explicit_hypothesis_and_tested_by(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_experiment(
            artifact, Experiment(slug="e1", directory="d", run=RunSpec(command="r"))
        )
        add_claim(
            artifact,
            Claim(id="h1", statement="caching helps", stance="hypothesis", tested_by=["e1"]),
        )
        claim = get_claim(artifact, "h1")
        assert claim is not None
        assert claim.stance == "hypothesis"
        assert claim.tested_by == ["e1"]

    def test_a_hypothesis_without_a_validator_is_not_warned_about(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="h1", statement="s", stance="hypothesis"))
        assert has_warning(artifact, "claim[h1]: claim has no validator") is False

    def test_a_finding_without_a_validator_is_warned_about(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="c1", statement="s"))
        assert has_warning(artifact, "claim has no validator")

    def test_rejects_an_illegal_stance(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="c1", statement="s", stance="guess"))
        assert has_error(artifact, "invalid stance 'guess'")

    def test_flags_tested_by_pointing_at_an_unknown_experiment(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(
            artifact, Claim(id="h1", statement="s", stance="hypothesis", tested_by=["nope"])
        )
        assert has_error(artifact, "references unknown experiment 'nope'")

    def test_supports_the_hypothesis_to_finding_lifecycle(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_experiment(
            artifact, Experiment(slug="e1", directory="d", run=RunSpec(command="r"))
        )
        add_claim(
            artifact, Claim(id="h1", statement="s", stance="hypothesis", tested_by=["e1"])
        )
        add_claim(
            artifact,
            Claim(
                id="h1",
                statement="s",
                stance="finding",
                tested_by=["e1"],
                validators=[AttestValidator(checks="integrity")],
            ),
            ctx=ChangeContext(actor="writer", rationale="e1 supported the hypothesis"),
        )
        claim = get_claim(artifact, "h1")
        assert claim is not None and claim.stance == "finding"
        assert any(e.target.kind == "claim" and e.op == "replace" for e in artifact.journal)

    def test_keeps_a_refuted_hypothesis_as_a_negative_result(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_experiment(
            artifact, Experiment(slug="e1", directory="d", run=RunSpec(command="r"))
        )
        add_claim(
            artifact, Claim(id="h1", statement="s", stance="hypothesis", tested_by=["e1"])
        )
        fail_experiment(
            artifact,
            "e1",
            Failure(stage="analysis", summary="no effect"),
            ctx=ChangeContext(rationale="flat within noise"),
        )
        claim = get_claim(artifact, "h1")
        assert claim is not None and claim.stance == "hypothesis"
        experiment = artifact.experiments[0]
        assert experiment.disposition is not None
        assert experiment.disposition.status == "failed"

    def test_round_trips_stance_and_tested_by(self, out_dir: Path) -> None:
        artifact = create_artifact(id="x", title="t")
        add_experiment(
            artifact, Experiment(slug="e1", directory="d", run=RunSpec(command="r"))
        )
        add_claim(
            artifact, Claim(id="h1", statement="s", stance="hypothesis", tested_by=["e1"])
        )
        write_submission(artifact, out_dir)
        claim = next(c for c in open_submission(out_dir).claims if c.id == "h1")
        assert claim.stance == "hypothesis"
        assert claim.tested_by == ["e1"]


class TestEvidenceInventory:
    def test_reports_exhibit_presence_and_count(self) -> None:
        artifact = base_artifact()
        assert compute_evidence_inventory(artifact).has_exhibits is False
        add_exhibit(
            artifact,
            Exhibit(id="X1", type="figure", caption="c", validates=["C4"], path="a/f.png"),
        )
        inventory = compute_evidence_inventory(artifact)
        assert inventory.has_exhibits is True
        assert inventory.exhibit_count == 1

    def test_summarizes_a_populated_artifact(self) -> None:
        artifact = base_artifact()
        add_dataset(artifact, Dataset(id="d1", location=InArtifactLocation(path="data/d1")))
        add_dataset(
            artifact,
            Dataset(id="d2", location=ExternalLocation(uri="https://e/x", sha256="abc")),
        )
        add_trace(artifact, Trace(id="T1", kind="execution_log", path="traces/t.log"))
        add_result(
            artifact,
            Result(
                id="R1",
                validates=["C4"],
                evidence="e.csv",
                kind="metrics",
                validation_mode="re-analyze",
            ),
        )
        add_result(
            artifact,
            Result(
                id="R2",
                validates=["C4"],
                evidence="t.txt",
                kind="transcript",
                validation_mode="inspect",
            ),
        )
        attach_paper(
            artifact,
            Paper(pdf="paper.pdf", source="paper/", references_export="refs.yml"),
        )
        attach_research_agent(
            artifact,
            ResearchAgent(path="research-agent.md", model="m", grounding_sources=["claims.yml"]),
        )
        inventory = compute_evidence_inventory(artifact)
        assert inventory.has_runnable_experiments is True
        assert inventory.has_traces is True and inventory.trace_count == 1
        assert inventory.has_released_data is True
        assert inventory.has_paper_source is True
        assert inventory.has_citations_export is True
        assert inventory.has_journal is True
        assert inventory.has_research_agent is True
        assert inventory.experiments_attempted == 1
        assert inventory.experiments_reported == 1
        assert inventory.evidence_kinds == ["metrics", "transcript"]
        assert inventory.validation_modes == ["inspect", "re-analyze"]

    def test_counts_only_active_experiments_as_reported(self) -> None:
        artifact = base_artifact()
        fail_experiment(
            artifact,
            "fpr-sweep",
            Failure(stage="run", summary="OOM"),
            ctx=ChangeContext(rationale="out of memory"),
        )
        inventory = compute_evidence_inventory(artifact)
        assert inventory.experiments_attempted == 1
        assert inventory.experiments_reported == 0
        assert inventory.has_runnable_experiments is False

    def test_an_empty_artifact_reports_nothing(self) -> None:
        inventory = compute_evidence_inventory(create_artifact(id="x", title="t"))
        assert inventory.has_runnable_experiments is False
        assert inventory.evidence_kinds == []
        assert inventory.validation_modes == []
        assert inventory.has_released_data is False
