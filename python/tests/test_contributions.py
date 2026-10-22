"""Contribution declarations, conservative ownership and v2 migration, without network."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft7Validator

from universal_artifact_sdk import (
    Artifact,
    ChangeContext,
    Claim,
    Contribution,
    ContributionComparison,
    ContributionOriginality,
    Paper,
    add_claim,
    add_contribution,
    artifact_from_dict,
    canonical_schema_path,
    compute_evidence_inventory,
    configure_journal,
    create_artifact,
    get_contribution,
    list_contributions,
    open_submission,
    read_yaml,
    remove_contribution,
    to_dict,
    validate_structure,
    write_submission,
)

REPO = Path(__file__).resolve().parents[2]
FULL = json.loads((REPO / "parity/cases/contributions-complete.json").read_text(encoding="utf-8"))[
    "artifact"
]
WHY = ChangeContext(rationale="declare or revise")


def model() -> Artifact:
    artifact = create_artifact(id="artifact", title="Candidate advances")
    add_claim(artifact, Claim(id="C1", statement="Hypothesis", stance="hypothesis"), ctx=WHY)
    return artifact


def test_editor_journal_ids_and_atomic_rejection() -> None:
    artifact = model()
    first = artifact_from_dict(FULL).contributions[0]
    configure_journal(
        artifact, policy="required", actor="human:author", now=lambda: "2026-10-14T00:00:00Z"
    )
    add_contribution(artifact, first, ctx=WHY)
    edited = Contribution(id=first.id, statement="Edited")
    add_contribution(artifact, edited, ctx=WHY)
    assert get_contribution(artifact, first.id) == edited
    listed = list_contributions(artifact)
    listed.clear()
    assert len(artifact.contributions) == 1
    entry = artifact.journal[-1]
    assert (entry.op, entry.target.kind, entry.target.id) == ("replace", "contribution", first.id)
    assert entry.before == first and entry.after == edited
    assert entry.actor == "human:author"
    with pytest.raises(ValueError, match="rationale"):
        remove_contribution(artifact, first.id)
    assert artifact.contributions == [edited]
    assert remove_contribution(artifact, first.id, ctx=WHY)
    assert not remove_contribution(artifact, first.id)
    assert get_contribution(artifact, first.id) is None
    assert [c.id for c in artifact.claims] == ["C1"]


def test_old_dataclass_callers_and_drafts_remain_legal() -> None:
    artifact = Artifact("old", "Old caller")
    assert validate_structure(artifact).ok
    assert not compute_evidence_inventory(artifact).has_contributions
    for id, links in (("N1", None), ("N2", []), ("N3", ["C1"])):
        artifact.contributions.append(
            Contribution(id=id, statement="Candidate", supporting_claims=links)
        )
    artifact.claims.append(Claim(id="C1", statement="Hypothesis", stance="hypothesis"))
    report = validate_structure(artifact)
    assert report.ok
    assert [w.path for w in report.warnings] == [
        "contribution[N1].supporting_claims",
        "contribution[N2].supporting_claims",
    ]
    assert compute_evidence_inventory(artifact).contribution_count == 3


def test_full_declaration_edit_write_reopen_all_fields_and_extensions(out_dir: Path) -> None:
    artifact = artifact_from_dict(FULL)
    report = write_submission(artifact, out_dir, stage_from=REPO / "parity/fixtures")
    assert "contributions.yml" in report.files_written
    assert read_yaml(out_dir / "manifest.yml")["paths"]["contributions"] == "contributions.yml"
    assert read_yaml(out_dir / "manifest.yml")["evidence_inventory"]["contribution_count"] == 3
    state = json.loads((out_dir / ".sdk/state.json").read_text(encoding="utf-8"))
    assert "contributions.yml" in state["generated_files"]
    assert len(state["generated_hashes"]["contributions.yml"]) == 64
    assert "  contributions.yml" in (out_dir / "SHA256SUMS").read_text(encoding="utf-8")
    reopened = open_submission(out_dir)
    assert to_dict(reopened.contributions) == FULL["contributions"]
    reopened.contributions[0].statement = "Refined"
    add_contribution(reopened, reopened.contributions[0], ctx=WHY)
    write_submission(reopened, out_dir)
    assert to_dict(open_submission(out_dir).contributions) == to_dict(reopened.contributions)
    assert reopened.contributions[0].id == FULL["contributions"][0]["id"]


def test_removal_deletes_only_unchanged_generated_index(out_dir: Path) -> None:
    artifact = model()
    add_contribution(artifact, Contribution(id="N1", statement="Draft"), ctx=WHY)
    write_submission(artifact, out_dir)
    assert remove_contribution(artifact, "N1", ctx=WHY)
    write_submission(artifact, out_dir)
    assert not (out_dir / "contributions.yml").exists()
    assert "contributions" not in read_yaml(out_dir / "manifest.yml")["paths"]
    assert open_submission(out_dir).contributions == []
    add_contribution(artifact, Contribution(id="N2", statement="Draft"), ctx=WHY)
    write_submission(artifact, out_dir)
    authored = "contributions:\n  - id: external\n    statement: External edit\n"
    (out_dir / "contributions.yml").write_text(authored, encoding="utf-8")
    remove_contribution(artifact, "N2", ctx=WHY)
    write_submission(artifact, out_dir)
    assert (out_dir / "contributions.yml").read_text(encoding="utf-8") == authored
    assert open_submission(out_dir).contributions == []
    state = json.loads((out_dir / ".sdk/state.json").read_text(encoding="utf-8"))
    assert "contributions.yml" in state["authored_files"]


def test_no_clobber_and_explicit_reopen_adoption(out_dir: Path) -> None:
    artifact = model()
    add_contribution(artifact, Contribution(id="N1", statement="Draft"), ctx=WHY)
    write_submission(artifact, out_dir)
    before = (out_dir / "manifest.yml").read_bytes()
    authored = (
        "contributions:\n  - id: N1\n    statement: External edit\n    x_field: {keep: null}\n"
    )
    (out_dir / "contributions.yml").write_text(authored, encoding="utf-8")
    with pytest.raises(ValueError, match="Refusing to overwrite"):
        write_submission(artifact, out_dir)
    assert (out_dir / "manifest.yml").read_bytes() == before
    reopened = open_submission(out_dir)
    reopened.contributions[0].statement = "Intentional revision"
    write_submission(reopened, out_dir)
    assert to_dict(open_submission(out_dir).contributions[0]) == {
        "id": "N1",
        "statement": "Intentional revision",
        "x_field": {"keep": None},
    }
    (out_dir / "contributions.yml").write_text(authored, encoding="utf-8")
    with pytest.raises(ValueError, match="Refusing to overwrite"):
        write_submission(reopened, out_dir)


def test_fresh_writer_does_not_adopt_authored_destination(out_dir: Path) -> None:
    artifact = model()
    (out_dir / "contributions.yml").write_text("authored notes", encoding="utf-8")
    add_contribution(artifact, Contribution(id="N1", statement="Draft"), ctx=WHY)
    with pytest.raises(ValueError, match="Refusing to overwrite"):
        write_submission(artifact, out_dir)
    assert not (out_dir / "manifest.yml").exists()


def test_relocated_authored_index_survives_canonical_rewrite(out_dir: Path) -> None:
    write_submission(model(), out_dir)
    (out_dir / "indexes").mkdir()
    authored = "contributions:\n  - id: N1\n    statement: Draft\n"
    (out_dir / "indexes/advances.yml").write_text(authored, encoding="utf-8")
    manifest = (
        (out_dir / "manifest.yml")
        .read_text(encoding="utf-8")
        .replace("paths:\n", "paths:\n  contributions: indexes/advances.yml\n")
    )
    (out_dir / "manifest.yml").write_text(manifest, encoding="utf-8")
    artifact = open_submission(out_dir)
    assert artifact.contributions[0].id == "N1"
    write_submission(artifact, out_dir)
    assert read_yaml(out_dir / "manifest.yml")["paths"]["contributions"] == "contributions.yml"
    remove_contribution(artifact, "N1", ctx=WHY)
    write_submission(artifact, out_dir)
    assert (out_dir / "indexes/advances.yml").read_text(encoding="utf-8") == authored


@pytest.mark.parametrize(
    "path",
    [
        "../outside.yml",
        "/absolute.yml",
        "C:outside.yml",
        "..\\outside.yml",
        ".sdk/state.json",
        "claims.yml",
        "contributions.yml/../claims.yml",
        "indexes//file.yml",
        "",
    ],
)
def test_unsafe_declared_paths_are_rejected(out_dir: Path, path: str) -> None:
    (out_dir / "manifest.yml").write_text(
        json.dumps(
            {
                "format_version": "evaluable-artifact/v3",
                "paths": {"contributions": path},
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="contributions index path"):
        open_submission(out_dir)


def test_symlink_missing_and_malformed_indexes(out_dir: Path, source_dir: Path) -> None:
    target = source_dir / "data.yml"
    target.write_text("contributions: []\n", encoding="utf-8")
    (out_dir / "contributions.yml").symlink_to(target)
    with pytest.raises(ValueError, match="symlink"):
        write_submission(model(), out_dir)
    (out_dir / "manifest.yml").write_text(
        json.dumps(
            {
                "format_version": "evaluable-artifact/v3",
                "paths": {"contributions": "contributions.yml"},
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="symlink"):
        open_submission(out_dir)
    (out_dir / "contributions.yml").unlink()
    with pytest.raises(ValueError, match="missing"):
        open_submission(out_dir)
    (out_dir / "contributions.yml").write_text("contributions: {}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="array"):
        open_submission(out_dir)


@pytest.mark.parametrize(
    "declaration",
    [
        {},
        {"id": "", "statement": "Draft"},
        {"id": "N", "statement": "  "},
        {"id": "N", "statement": "Draft", "supporting_claims": ["C1", "C1"]},
        {"id": "N", "statement": "Draft", "supporting_claims": "C1"},
        {"id": "N", "statement": "Draft", "significance": {"impact": "established"}},
        {"id": "N", "statement": "Draft", "significance": {"evidence": ["bare filename"]}},
        {"id": "N", "statement": "Draft", "originality": {"comparisons": [{"reference": "r"}]}},
        {"id": "N", "statement": "Draft", "originality": {"coverage": {"sources": "search"}}},
        {"id": "N", "statement": "Draft", "provenance": {"kind": "evaluator-verdict"}},
        {"id": "N", "statement": "Draft", "provenance": None},
        {"id": "N", "statement": "Draft", "originality": {"coverage": None}},
        {"id": "N", "statement": "Draft", "paper_ref": {"char_start": -1}},
        None,
        7,
        "declaration",
    ],
)
def test_schema_runtime_alignment_for_malformed_contributions(
    declaration: Any,
    out_dir: Path,
) -> None:
    data = to_dict(model())
    data["contributions"] = [declaration]
    schema = json.loads(canonical_schema_path().read_text(encoding="utf-8"))
    assert not Draft7Validator(schema).is_valid(data)
    artifact = artifact_from_dict(data)
    assert not validate_structure(artifact).ok
    with pytest.raises(ValueError, match="structural"):
        write_submission(artifact, out_dir / "unwritten")
    assert not (out_dir / "unwritten").exists()


def test_duplicate_dangling_and_reference_diagnostics() -> None:
    artifact = model()
    artifact.contributions = artifact_from_dict(
        {
            "contributions": [
                {
                    "id": "N",
                    "statement": "First",
                    "supporting_claims": ["missing"],
                    "significance": {
                        "evidence": ["result:missing", "claim:missing", "reference:missing"]
                    },
                    "originality": {
                        "comparisons": [{"reference": "missing", "distinction": "Different"}]
                    },
                },
                {"id": "N", "statement": "Duplicate"},
            ],
        }
    ).contributions
    assert [i.path for i in validate_structure(artifact, reference_ids=[]).errors] == [
        "contribution[N].supporting_claims",
        "contribution[N].significance.evidence[0]",
        "contribution[N].significance.evidence[1]",
        "contribution[N].significance.evidence[2]",
        "contribution[N].originality.comparisons[0].reference",
        "contribution[N].id",
    ]


@pytest.mark.parametrize("file", ["references.yml", "references.json", "references.bib"])
def test_bibliography_ids_resolved_on_write(
    out_dir: Path,
    source_dir: Path,
    file: str,
) -> None:
    artifact = model()
    artifact.paper = Paper(source="paper.md", references_export=file)
    (source_dir / "paper.md").write_text("Paper", encoding="utf-8")
    text = (
        "@article{existing, title={Prior work}}\n"
        if file.endswith(".bib")
        else json.dumps(
            {
                "references": [{"id": "existing"}],
            }
        )
    )
    (source_dir / file).write_text(text, encoding="utf-8")
    comparison = ContributionComparison(reference="existing", distinction="A declared distinction")
    add_contribution(
        artifact,
        Contribution(
            id="N",
            statement="Draft",
            originality=ContributionOriginality(comparisons=[comparison]),
        ),
        ctx=WHY,
    )
    assert any(i.path.endswith(".reference") for i in validate_structure(artifact).warnings)
    report = write_submission(artifact, out_dir, stage_from=source_dir)
    assert not any(i.path.endswith(".reference") for i in report.warnings)
    comparison.reference = "missing"
    with pytest.raises(ValueError, match="unknown bibliography ID"):
        write_submission(artifact, out_dir)


def test_reserved_destination_and_legacy_v2_migration(out_dir: Path) -> None:
    artifact = model()
    artifact.paper = Paper(pdf="contributions.yml")
    assert "paper.pdf" in [i.path for i in validate_structure(artifact).errors]
    (out_dir / "manifest.yml").write_text(
        "format_version: evaluable-artifact/v2\nid: legacy\ntitle: Legacy\n", encoding="utf-8"
    )
    legacy = open_submission(out_dir)
    assert legacy.format_version == "evaluable-artifact/v2"
    write_submission(legacy, out_dir)
    assert legacy.format_version == "evaluable-artifact/v2"
    reopened = open_submission(out_dir)
    assert reopened.format_version == "evaluable-artifact/v3"
    schema = json.loads(
        (REPO / "schema/evaluable-artifact-v2.schema.json").read_text(encoding="utf-8")
    )
    assert Draft7Validator(schema).is_valid(to_dict(legacy))
    assert not Draft7Validator(schema).is_valid(to_dict(reopened))
    (out_dir / "manifest.yml").write_text(
        "format_version: evaluable-artifact/v4\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="unsupported format"):
        open_submission(out_dir)


def test_empty_declared_index_does_not_retain_stale_manifest_path(out_dir: Path) -> None:
    (out_dir / "manifest.yml").write_text(
        json.dumps(
            {
                "format_version": "evaluable-artifact/v3",
                "id": "empty",
                "title": "Empty",
                "paths": {"contributions": "contributions.yml"},
            }
        ),
        encoding="utf-8",
    )
    (out_dir / "contributions.yml").write_text("contributions: []\n", encoding="utf-8")
    artifact = open_submission(out_dir)
    assert validate_structure(artifact).ok
    write_submission(artifact, out_dir)
    assert "contributions" not in read_yaml(out_dir / "manifest.yml")["paths"]
    assert open_submission(out_dir).contributions == []


def test_bibtex_entry_bodies_and_comments_do_not_invent_identities(out_dir: Path) -> None:
    artifact = model()
    artifact.paper = Paper(source="paper.md", references_export="refs.bib")
    (out_dir / "paper.md").write_text("Paper", encoding="utf-8")
    (out_dir / "refs.bib").write_text(
        "@comment{ @article{fake, title={not an entry}} }\n"
        "@article{real, title={Text @book{also-fake, year={2020}}}}\n",
        encoding="utf-8",
    )
    comparison = ContributionComparison(reference="real", distinction="Different")
    add_contribution(
        artifact,
        Contribution(
            id="N",
            statement="Draft",
            originality=ContributionOriginality(comparisons=[comparison]),
        ),
        ctx=WHY,
    )
    assert write_submission(artifact, out_dir).ok
    comparison.reference = "fake"
    with pytest.raises(ValueError, match="unknown bibliography ID"):
        write_submission(artifact, out_dir)


@pytest.mark.parametrize(
    "text",
    [
        "unrecognized export",
        "references: [",
        "references: [{title: unknown}]",
    ],
)
def test_unavailable_bibliography_identity_stays_explicit(out_dir: Path, text: str) -> None:
    artifact = model()
    artifact.paper = Paper(source="paper.md", references_export="refs.yml")
    (out_dir / "paper.md").write_text("Paper", encoding="utf-8")
    (out_dir / "refs.yml").write_text(text, encoding="utf-8")
    add_contribution(
        artifact,
        Contribution(
            id="N",
            statement="Draft",
            originality=ContributionOriginality(
                comparisons=[
                    ContributionComparison(reference="unknown", distinction="Different"),
                ]
            ),
        ),
        ctx=WHY,
    )
    report = write_submission(artifact, out_dir)
    assert any(i.path.endswith(".reference") for i in report.warnings)
