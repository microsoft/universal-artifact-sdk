"""Builder and model defaults — mirrors ``test/builder.test.ts``."""

from __future__ import annotations

import pytest

from universal_artifact_sdk import (
    AddClaimInput,
    Assessment,
    AttestValidator,
    ChangeContext,
    Claim,
    Dataset,
    Environment,
    Exhibit,
    Experiment,
    Image,
    InArtifactLocation,
    Paper,
    Result,
    RunSpec,
    Trace,
    add_assessment,
    add_claim,
    add_dataset,
    add_environment,
    add_exhibit,
    add_experiment,
    add_result,
    add_trace,
    attach_paper,
    create_artifact,
    default_exhibit_validation_mode,
    default_validation_mode,
    get_assessment,
    get_claim,
    get_dataset,
    get_exhibit,
    get_experiment,
    get_result,
    get_trace,
    list_assessments,
    list_claims,
    list_datasets,
    list_exhibits,
    list_experiments,
    list_results,
    list_traces,
    pinned_digest,
    remove_assessment,
    remove_claim,
    remove_dataset,
    remove_exhibit,
    remove_experiment,
    remove_result,
    remove_trace,
    set_reflection,
)
from universal_artifact_sdk.model import Artifact


def seeded() -> Artifact:
    artifact = create_artifact(id="x", title="t")
    add_environment(artifact, Environment(name="primary", image=Image(reference="img:1")))
    add_dataset(artifact, Dataset(id="d1", location=InArtifactLocation(path="data/d1")))
    add_experiment(
        artifact,
        Experiment(slug="e1", directory="experiments/e1", run=RunSpec(command="run")),
    )
    add_trace(artifact, Trace(id="t1", kind="execution_log", path="traces/t1.log"))
    add_result(artifact, Result(id="r1", validates=[], evidence="e", kind="metrics"))
    add_claim(artifact, Claim(id="c1", statement="s"))
    add_exhibit(
        artifact,
        Exhibit(id="x1", type="figure", caption="c", validates=[], path="exhibits/f.png"),
    )
    add_assessment(artifact, Assessment(id="a1", dimension="citation_integrity", scope="paper"))
    return artifact


class TestCreateArtifact:
    def test_requires_id_and_title(self) -> None:
        with pytest.raises(ValueError, match="`id` is required"):
            create_artifact(id="", title="t")
        with pytest.raises(ValueError, match="`title` is required"):
            create_artifact(id="x", title="")

    def test_stamps_versions_and_starts_empty(self) -> None:
        artifact = create_artifact(id="x", title="t", producer={"name": "example-harness"})
        assert artifact.format_version == "evaluable-artifact/v2"
        assert artifact.sdk_version == "artifact-sdk/v1"
        assert artifact.producer == {"name": "example-harness"}
        assert artifact.datasets == []
        assert artifact.experiments == []
        assert artifact.traces == []
        assert artifact.results == []
        assert artifact.claims == []
        assert artifact.exhibits == []
        assert artifact.assessments == []
        assert artifact.journal == []
        assert artifact.environment is None
        assert artifact.paper is None
        assert artifact.research_agent is None
        assert artifact.reflection is None

    def test_producer_defaults_to_absent(self) -> None:
        assert create_artifact(id="x", title="t").producer is None


class TestDefaultValidationMode:
    @pytest.mark.parametrize(
        ("kind", "expected"),
        [
            ("metrics", "re-analyze"),
            ("table", "re-analyze"),
            ("figure", "re-analyze"),
            ("proof", "re-execute"),
            ("log", "re-execute"),
            ("external_reference", "attest"),
            ("transcript", "inspect"),
            ("survey", "inspect"),
            ("a-vendor-kind", "inspect"),
        ],
    )
    def test_maps_each_kind(self, kind: str, expected: str) -> None:
        assert default_validation_mode(kind) == expected

    @pytest.mark.parametrize(
        ("exhibit_type", "expected"),
        [
            ("figure", "inspect"),
            ("table", "inspect"),
            ("listing", "inspect"),
            ("derivation", "inspect"),
            ("proof", "re-execute"),
        ],
    )
    def test_maps_each_exhibit_type(self, exhibit_type: str, expected: str) -> None:
        assert default_exhibit_validation_mode(exhibit_type) == expected


class TestElementAccess:
    def test_get_returns_the_element_and_list_returns_a_copy(self) -> None:
        artifact = seeded()
        assert get_dataset(artifact, "d1") is not None
        assert get_experiment(artifact, "e1") is not None
        assert get_trace(artifact, "t1") is not None
        assert get_result(artifact, "r1") is not None
        assert get_exhibit(artifact, "x1") is not None
        assert get_claim(artifact, "c1") is not None
        assert get_assessment(artifact, "a1") is not None

        copy = list_claims(artifact)
        copy.append(Claim(id="zzz", statement="x"))
        assert len(list_claims(artifact)) == 1

        assert len(list_datasets(artifact)) == 1
        assert len(list_experiments(artifact)) == 1
        assert len(list_traces(artifact)) == 1
        assert len(list_results(artifact)) == 1
        assert len(list_exhibits(artifact)) == 1
        assert len(list_assessments(artifact)) == 1

    def test_get_returns_none_for_an_unknown_id(self) -> None:
        artifact = seeded()
        assert get_dataset(artifact, "nope") is None
        assert get_experiment(artifact, "nope") is None
        assert get_trace(artifact, "nope") is None
        assert get_result(artifact, "nope") is None
        assert get_exhibit(artifact, "nope") is None
        assert get_claim(artifact, "nope") is None
        assert get_assessment(artifact, "nope") is None

    def test_remove_deletes_and_reports_whether_it_removed(self) -> None:
        artifact = seeded()
        assert remove_dataset(artifact, "d1") is True
        assert remove_dataset(artifact, "d1") is False
        # An experiment is soft-removed, and dropping one always requires a rationale.
        assert remove_experiment(artifact, "e1", ctx=ChangeContext(rationale="superseded")) is True
        assert len(artifact.experiments) == 1
        assert artifact.experiments[0].disposition is not None
        assert remove_trace(artifact, "t1") is True
        assert remove_result(artifact, "r1") is True
        assert remove_exhibit(artifact, "x1") is True
        assert remove_claim(artifact, "c1") is True
        assert remove_assessment(artifact, "a1") is True
        assert remove_assessment(artifact, "nope") is False
        assert artifact.datasets == []

    def test_upsert_by_id_replaces_every_element_type_in_place(self) -> None:
        artifact = seeded()
        add_dataset(artifact, Dataset(id="d1", location=InArtifactLocation(path="data/renamed")))
        add_experiment(
            artifact,
            Experiment(slug="e1", directory="experiments/e1", run=RunSpec(command="run2")),
        )
        add_trace(artifact, Trace(id="t1", kind="notebook", path="traces/t1.ipynb"))
        add_result(artifact, Result(id="r1", validates=[], evidence="e2", kind="figure"))
        add_exhibit(
            artifact,
            Exhibit(id="x1", type="table", caption="c2", validates=[], path="exhibits/t.csv"),
        )
        add_assessment(
            artifact,
            Assessment(id="a1", dimension="execution_authenticity", scope="artifact"),
        )
        assert len(artifact.datasets) == 1
        dataset = get_dataset(artifact, "d1")
        assert dataset is not None
        assert dataset.location.path == "data/renamed"
        experiment = get_experiment(artifact, "e1")
        assert experiment is not None and experiment.run.command == "run2"
        trace = get_trace(artifact, "t1")
        assert trace is not None and trace.kind == "notebook"
        result = get_result(artifact, "r1")
        assert result is not None and result.kind == "figure"
        exhibit = get_exhibit(artifact, "x1")
        assert exhibit is not None and exhibit.type == "table"
        assessment = get_assessment(artifact, "a1")
        assert assessment is not None and assessment.dimension == "execution_authenticity"


class TestAddClaimSugar:
    def test_accepts_a_singular_validator(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(
            artifact,
            AddClaimInput(id="c1", statement="s", validator=AttestValidator(checks="integrity")),
        )
        claim = get_claim(artifact, "c1")
        assert claim is not None
        assert len(claim.validators) == 1
        assert claim.validators[0].kind == "attest"

    def test_defaults_to_an_empty_validator_list(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, AddClaimInput(id="c1", statement="s"))
        claim = get_claim(artifact, "c1")
        assert claim is not None and claim.validators == []

    def test_explicit_validators_win_over_the_singular_sugar(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(
            artifact,
            AddClaimInput(
                id="c1",
                statement="s",
                validators=[],
                validator=AttestValidator(checks="integrity"),
            ),
        )
        claim = get_claim(artifact, "c1")
        assert claim is not None and claim.validators == []

    def test_accepts_a_claim_model_and_copies_its_validator_list(self) -> None:
        artifact = create_artifact(id="x", title="t")
        validators = [AttestValidator(checks="integrity")]
        add_claim(artifact, Claim(id="c1", statement="s", validators=validators))
        claim = get_claim(artifact, "c1")
        assert claim is not None
        assert claim.validators == validators
        assert claim.validators is not validators


class TestAttachments:
    def test_stores_the_paper_and_reflection(self) -> None:
        artifact = create_artifact(id="x", title="t")
        attach_paper(artifact, Paper(pdf="paper.pdf", source="paper/"))
        set_reflection(artifact, "# limitations\n")
        assert artifact.paper is not None and artifact.paper.pdf == "paper.pdf"
        assert artifact.reflection == "# limitations\n"

    def test_reattaching_a_paper_replaces_it(self) -> None:
        artifact = create_artifact(id="x", title="t")
        attach_paper(artifact, Paper(pdf="first.pdf"))
        attach_paper(artifact, Paper(pdf="second.pdf"))
        assert artifact.paper is not None and artifact.paper.pdf == "second.pdf"
        assert [entry.op for entry in artifact.journal] == ["attach", "replace"]


class TestEnvironmentDigestAutofill:
    def test_lifts_a_digest_embedded_in_the_reference(self) -> None:
        artifact = create_artifact(id="x", title="t")
        digest = "sha256:" + "c" * 64
        add_environment(
            artifact,
            Environment(name="primary", image=Image(reference=f"registry/artifact:1.2@{digest}")),
        )
        assert artifact.environment is not None
        assert artifact.environment.image.digest == digest

    def test_normalizes_the_case_of_an_embedded_digest(self) -> None:
        artifact = create_artifact(id="x", title="t")
        digest = "sha256:" + "A" * 64
        environment = add_environment(
            artifact, Environment(name="primary", image=Image(reference=f"image@{digest}"))
        )
        assert environment.image.digest == digest.lower()

    def test_keeps_an_explicit_digest_and_never_invents_one(self) -> None:
        artifact = create_artifact(id="x", title="t")
        explicit = "sha256:" + "d" * 64
        add_environment(
            artifact,
            Environment(
                name="primary",
                image=Image(reference="registry/artifact:1.2@sha256:" + "e" * 64, digest=explicit),
            ),
        )
        assert artifact.environment is not None
        assert artifact.environment.image.digest == explicit

        bare = create_artifact(id="y", title="t")
        add_environment(bare, Environment(name="primary", image=Image(reference="reg/a:1.2")))
        assert bare.environment is not None and bare.environment.image.digest is None

    def test_does_not_mutate_the_caller_s_environment(self) -> None:
        artifact = create_artifact(id="x", title="t")
        image = Image(reference="registry/artifact:1.2@sha256:" + "f" * 64)
        environment = Environment(name="primary", image=image)
        add_environment(artifact, environment)
        assert image.digest is None

    @pytest.mark.parametrize(
        ("reference", "expected"),
        [
            ("registry/artifact:1.2", None),
            (None, None),
            ("", None),
            ("repo@sha256:" + "a" * 63, None),
            ("repo@sha256:" + "a" * 64, "sha256:" + "a" * 64),
            ("repo@SHA256:" + "A" * 64, "sha256:" + "a" * 64),
        ],
    )
    def test_pinned_digest(self, reference: str | None, expected: str | None) -> None:
        assert pinned_digest(reference) == expected
