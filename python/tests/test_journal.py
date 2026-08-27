"""Journaling and the experiment lifecycle — mirrors ``test/journal.test.ts``."""

from __future__ import annotations

from pathlib import Path

import pytest

from universal_artifact_sdk import (
    Artifact,
    ChangeContext,
    Claim,
    Disposition,
    Experiment,
    Failure,
    PendingChange,
    ResearchAgent,
    RunSpec,
    abandon_experiment,
    add_claim,
    add_experiment,
    attach_research_agent,
    configure_journal,
    create_artifact,
    fail_experiment,
    list_abandoned_experiments,
    list_experiments,
    list_journal,
    open_submission,
    purge_experiment,
    read_yaml,
    remove_experiment,
    set_reflection,
    supersede_experiment,
    validate_structure,
    write_submission,
)

FIXED = "2026-01-01T00:00:00.000Z"


def seeded() -> Artifact:
    artifact = create_artifact(id="x", title="t")
    configure_journal(artifact, actor="agent:experiment", now=lambda: FIXED)
    return artifact


def experiment(slug: str = "e1", command: str = "run") -> Experiment:
    return Experiment(
        slug=slug, directory=f"experiments/{slug}", run=RunSpec(command=command)
    )


class TestJournalEntries:
    def test_stamps_every_field(self) -> None:
        artifact = seeded()
        add_experiment(
            artifact, experiment(), ctx=ChangeContext(rationale="first attempt at the sweep")
        )
        entry = list_journal(artifact)[0]
        assert entry.seq == 1
        assert entry.timestamp == FIXED
        assert entry.actor == "agent:experiment"
        assert entry.op == "add"
        assert entry.target.kind == "experiment"
        assert entry.target.id == "e1"
        assert entry.rationale == "first attempt at the sweep"
        assert entry.after is not None
        assert entry.before is None

    def test_records_a_replace_with_before_and_after(self) -> None:
        artifact = seeded()
        add_experiment(artifact, experiment(command="v1"))
        add_experiment(
            artifact, experiment(command="v2"), ctx=ChangeContext(rationale="tuned the command")
        )
        entries = list_journal(artifact)
        assert len(entries) == 2
        assert entries[1].op == "replace"
        assert entries[1].before.run.command == "v1"
        assert entries[1].after.run.command == "v2"

    def test_ctx_actor_overrides_the_configured_default(self) -> None:
        artifact = seeded()
        add_claim(
            artifact,
            Claim(id="c1", statement="s"),
            ctx=ChangeContext(actor="human:reviewer", rationale="authored"),
        )
        assert list_journal(artifact)[0].actor == "human:reviewer"

    def test_entries_alias_the_stored_objects_for_ordinary_mutations(self) -> None:
        # Frozen behavior (PYTHON_BINDING.md §4.3): add/replace snapshots keep the same
        # object references as the artifact, so later edits are visible through them.
        artifact = seeded()
        element = experiment()
        add_experiment(artifact, element, ctx=ChangeContext(rationale="try"))
        assert list_journal(artifact)[0].after is element

    def test_disposition_entries_use_shallow_snapshots(self) -> None:
        artifact = seeded()
        element = experiment()
        add_experiment(artifact, element, ctx=ChangeContext(rationale="try"))
        remove_experiment(artifact, "e1", ctx=ChangeContext(rationale="did not work"))
        entry = list_journal(artifact)[-1]
        assert entry.before is not element
        assert entry.after is not element
        assert entry.before.disposition is None
        assert entry.after.disposition is not None

    def test_list_journal_returns_a_copy(self) -> None:
        artifact = seeded()
        add_claim(artifact, Claim(id="c1", statement="s"))
        copy = list_journal(artifact)
        copy.clear()
        assert len(list_journal(artifact)) == 1

    def test_the_default_clock_produces_an_iso_timestamp(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="c1", statement="s"))
        timestamp = list_journal(artifact)[0].timestamp
        assert timestamp.endswith("Z")
        assert timestamp[4] == "-" and timestamp[10] == "T"


class TestRationalePolicy:
    def test_required_raises_and_leaves_the_model_untouched(self) -> None:
        artifact = create_artifact(id="x", title="t")
        configure_journal(artifact, policy="required")
        with pytest.raises(ValueError, match="rationale is required"):
            add_experiment(artifact, experiment())
        assert list_experiments(artifact) == []
        assert list_journal(artifact) == []
        add_experiment(artifact, experiment(), ctx=ChangeContext(rationale="ok"))
        assert len(list_experiments(artifact)) == 1

    def test_prompt_asks_the_callback(self) -> None:
        artifact = create_artifact(id="x", title="t")
        seen: list[str] = []

        def on_missing(change: PendingChange) -> str:
            seen.append(f"{change.op}:{change.target.kind}:{change.target.id}")
            return "because the agent said so"

        configure_journal(artifact, policy="prompt", on_missing_rationale=on_missing)
        add_experiment(artifact, experiment())
        assert seen == ["add:experiment:e1"]
        assert list_journal(artifact)[0].rationale == "because the agent said so"

    def test_prompt_records_nothing_but_still_gates_the_lifecycle(self) -> None:
        artifact = create_artifact(id="x", title="t")
        configure_journal(artifact, policy="prompt", on_missing_rationale=lambda change: "  ")
        # An ordinary mutation tolerates an empty prompted rationale ...
        add_experiment(artifact, experiment())
        assert list_journal(artifact)[0].rationale == ""
        # ... but dropping a tried experiment never does.
        with pytest.raises(ValueError, match="rationale is required"):
            purge_experiment(artifact, "e1")

    def test_warn_records_an_empty_rationale(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="c1", statement="s"))
        assert list_journal(artifact)[0].rationale == ""

    def test_configure_journal_keeps_unspecified_settings(self) -> None:
        artifact = create_artifact(id="x", title="t")
        configure_journal(artifact, actor="agent:one", now=lambda: FIXED)
        configure_journal(artifact, policy="required")
        assert artifact.journal_config is not None
        assert artifact.journal_config.actor == "agent:one"
        assert artifact.journal_config.policy == "required"
        assert artifact.journal_config.now is not None

    def test_the_default_configuration_is_warn_and_unknown(self) -> None:
        artifact = create_artifact(id="x", title="t")
        configure_journal(artifact)
        assert artifact.journal_config is not None
        assert artifact.journal_config.policy == "warn"
        assert artifact.journal_config.actor == "unknown"
        add_claim(artifact, Claim(id="c1", statement="s"))
        assert list_journal(artifact)[0].actor == "unknown"


class TestExperimentLifecycle:
    def test_remove_tags_the_experiment_abandoned_and_retains_it(self) -> None:
        artifact = seeded()
        add_experiment(artifact, experiment())
        assert remove_experiment(
            artifact, "e1", ctx=ChangeContext(rationale="confounded by seed")
        ) is True
        assert len(list_experiments(artifact)) == 1
        stored = list_experiments(artifact)[0]
        assert stored.disposition is not None
        assert stored.disposition.status == "abandoned"
        assert stored.disposition.rationale == "confounded by seed"
        assert [x.slug for x in list_abandoned_experiments(artifact)] == ["e1"]
        assert list_journal(artifact)[-1].op == "abandon"

    def test_remove_returns_false_for_an_unknown_slug(self) -> None:
        artifact = seeded()
        assert remove_experiment(artifact, "nope") is False

    def test_abandon_requires_a_rationale_regardless_of_policy(self) -> None:
        artifact = seeded()
        add_experiment(artifact, experiment())
        before = len(list_journal(artifact))
        with pytest.raises(ValueError, match="rationale is required"):
            remove_experiment(artifact, "e1")
        assert list_experiments(artifact)[0].disposition is None
        assert len(list_journal(artifact)) == before

    def test_fail_records_the_failure_detail(self) -> None:
        artifact = seeded()
        add_experiment(artifact, experiment())
        with pytest.raises(ValueError, match="rationale is required"):
            fail_experiment(artifact, "e1", Failure(stage="run", summary="OOM"))
        fail_experiment(
            artifact,
            "e1",
            Failure(stage="run", summary="OOM"),
            ctx=ChangeContext(rationale="ran out of memory"),
        )
        stored = list_experiments(artifact)[0]
        assert stored.disposition is not None
        assert stored.disposition.status == "failed"
        assert stored.disposition.failure == Failure(stage="run", summary="OOM")

    def test_fail_accepts_a_plain_mapping(self) -> None:
        artifact = seeded()
        add_experiment(artifact, experiment())
        fail_experiment(
            artifact,
            "e1",
            {"stage": "analysis", "summary": "no effect"},
            ctx=ChangeContext(rationale="flat within noise"),
        )
        stored = list_experiments(artifact)[0]
        assert stored.disposition is not None and stored.disposition.failure is not None
        assert stored.disposition.failure.summary == "no effect"

    def test_supersede_keeps_the_lineage(self) -> None:
        artifact = seeded()
        add_experiment(artifact, experiment("e1"))
        add_experiment(artifact, experiment("e2"))
        before = len(list_journal(artifact))
        with pytest.raises(ValueError, match="rationale is required"):
            supersede_experiment(artifact, "e1", "e2")
        assert artifact.experiments[0].disposition is None
        assert len(list_journal(artifact)) == before
        supersede_experiment(
            artifact, "e1", "e2", ctx=ChangeContext(rationale="e2 fixes the leakage")
        )
        disposition = artifact.experiments[0].disposition
        assert disposition is not None
        assert disposition.status == "superseded"
        assert disposition.superseded_by == "e2"
        assert list_journal(artifact)[-1].op == "replace"

    def test_purge_hard_deletes(self) -> None:
        artifact = seeded()
        add_experiment(artifact, experiment())
        with pytest.raises(ValueError, match="rationale is required"):
            purge_experiment(artifact, "e1")
        assert purge_experiment(
            artifact, "e1", ctx=ChangeContext(rationale="duplicate, never ran")
        ) is True
        assert list_experiments(artifact) == []
        assert list_journal(artifact)[-1].op == "remove"
        assert purge_experiment(artifact, "e1", ctx=ChangeContext(rationale="gone")) is False

    def test_lifecycle_operations_return_none_for_an_unknown_slug(self) -> None:
        artifact = seeded()
        context = ChangeContext(rationale="why")
        assert abandon_experiment(artifact, "nope", ctx=context) is None
        assert fail_experiment(
            artifact, "nope", Failure(stage="s", summary="x"), ctx=context
        ) is None
        assert supersede_experiment(artifact, "nope", "other", ctx=context) is None


class TestDispositionValidation:
    def test_warns_on_a_non_active_disposition_with_no_rationale(self) -> None:
        artifact = create_artifact(id="x", title="t")
        element = experiment()
        element.disposition = Disposition(status="abandoned", rationale="")
        artifact.experiments.append(element)
        report = validate_structure(artifact)
        assert report.ok is True
        assert any("process record is incomplete" in w.message for w in report.warnings)

    def test_warns_on_a_non_active_disposition_with_an_omitted_rationale(self) -> None:
        artifact = create_artifact(id="x", title="t")
        element = experiment()
        element.disposition = Disposition(status="abandoned")
        artifact.experiments.append(element)
        report = validate_structure(artifact)
        assert element.disposition.rationale is None
        assert report.ok is True
        assert any("process record is incomplete" in w.message for w in report.warnings)

    def test_errors_when_superseded_by_is_dangling(self) -> None:
        artifact = create_artifact(id="x", title="t")
        element = experiment()
        element.disposition = Disposition(
            status="superseded", rationale="r", superseded_by="ghost"
        )
        artifact.experiments.append(element)
        report = validate_structure(artifact)
        assert report.ok is False
        assert any("unknown experiment 'ghost'" in e.message for e in report.errors)

    def test_warns_on_a_journal_entry_with_no_rationale(self) -> None:
        artifact = create_artifact(id="x", title="t")
        add_claim(artifact, Claim(id="c1", statement="s"))
        report = validate_structure(artifact)
        assert any("has no rationale" in w.message for w in report.warnings)


class TestJournalSerialization:
    def test_writes_journal_and_disposition_markers_and_reopens(self, out_dir: Path) -> None:
        artifact = seeded()
        add_experiment(artifact, experiment("e1"), ctx=ChangeContext(rationale="baseline"))
        add_experiment(artifact, experiment("e2"), ctx=ChangeContext(rationale="variant"))
        abandon_experiment(artifact, "e2", ctx=ChangeContext(rationale="worse than baseline"))
        add_claim(artifact, Claim(id="c1", statement="s"), ctx=ChangeContext(rationale="headline"))

        write_submission(artifact, out_dir)

        assert (out_dir / "journal.yml").is_file()
        assert read_yaml(out_dir / "manifest.yml")["paths"]["journal"] == "journal.yml"
        marker = out_dir / "experiments" / "e2" / "DISPOSITION.md"
        assert marker.is_file()
        assert not (out_dir / "experiments" / "e1" / "DISPOSITION.md").exists()
        text = marker.read_text(encoding="utf-8")
        assert "worse than baseline" in text
        assert text.startswith("> **Auto-generated** by artifact-sdk/v1")

        reopened = open_submission(out_dir)
        assert len(reopened.journal) == len(artifact.journal)
        assert reopened.journal[-1].rationale == "headline"
        stored = next(e for e in reopened.experiments if e.slug == "e2")
        assert stored.disposition is not None and stored.disposition.status == "abandoned"

    def test_emits_no_journal_for_an_artifact_with_no_mutations(self, out_dir: Path) -> None:
        write_submission(create_artifact(id="x", title="t"), out_dir)
        assert not (out_dir / "journal.yml").exists()

    def test_the_marker_records_failure_and_supersession_detail(self, out_dir: Path) -> None:
        artifact = seeded()
        add_experiment(artifact, experiment("e1"), ctx=ChangeContext(rationale="baseline"))
        add_experiment(artifact, experiment("e2"), ctx=ChangeContext(rationale="variant"))
        fail_experiment(
            artifact,
            "e1",
            Failure(stage="run", summary="OOM"),
            ctx=ChangeContext(rationale="ran out of memory"),
        )
        supersede_experiment(artifact, "e2", "e1", ctx=ChangeContext(rationale="e1 is better"))
        write_submission(artifact, out_dir)
        failed = (out_dir / "experiments" / "e1" / "DISPOSITION.md").read_text(encoding="utf-8")
        superseded = (out_dir / "experiments" / "e2" / "DISPOSITION.md").read_text(
            encoding="utf-8"
        )
        assert "**Failure:** run — OOM" in failed
        assert "**Superseded by:** `e1`" in superseded

    def test_an_omitted_disposition_rationale_is_not_injected_on_write(
        self, out_dir: Path
    ) -> None:
        """An absent rationale stays absent through write → reopen → write (§2.2.2)."""
        artifact = create_artifact(id="x", title="t")
        element = experiment("e1")
        element.disposition = Disposition(status="abandoned")
        artifact.experiments.append(element)

        write_submission(artifact, out_dir)
        disposition = read_yaml(out_dir / "manifest.yml")["experiments"][0]["disposition"]
        assert disposition == {"status": "abandoned"}
        marker = (out_dir / "experiments" / "e1" / "DISPOSITION.md").read_text(encoding="utf-8")
        assert "_(no rationale recorded)_" in marker

        reopened = open_submission(out_dir)
        assert reopened.experiments[0].disposition is not None
        assert reopened.experiments[0].disposition.rationale is None
        write_submission(reopened, out_dir)
        assert read_yaml(out_dir / "manifest.yml")["experiments"][0]["disposition"] == {
            "status": "abandoned"
        }

    def test_the_journal_config_is_never_serialized(self, out_dir: Path) -> None:
        artifact = seeded()
        attach_research_agent(
            artifact,
            ResearchAgent(path="research-agent.md", model="m", grounding_sources=["claims.yml"]),
            ctx=ChangeContext(rationale="ship the witness"),
        )
        set_reflection(artifact, "notes", ctx=ChangeContext(rationale="record"))
        write_submission(artifact, out_dir)
        for name in ("manifest.yml", "journal.yml"):
            assert "journal_config" not in (out_dir / name).read_text(encoding="utf-8")
