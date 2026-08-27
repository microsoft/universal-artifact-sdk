"""Deterministic YAML emission (spec §5, PYTHON_BINDING.md §7).

Output must keep stable insertion order, avoid blanket quoting, and stay unambiguous for
any conforming YAML parser: a value that is a string in the model must read back as a
string in YAML 1.2 *and* in YAML 1.1, because the other binding may use either.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from ruamel.yaml import YAML

from universal_artifact_sdk import (
    Claim,
    Result,
    add_claim,
    add_result,
    create_artifact,
    open_submission,
    read_yaml,
    to_dict,
    write_submission,
    yaml_document,
)

AMBIGUOUS_STRINGS = [
    "no",
    "No",
    "NO",
    "yes",
    "on",
    "off",
    "y",
    "N",
    "true",
    "False",
    "12:30",
    "12:30:45",
    "2001-12-14",
    "2026-01-01T00:00:00.000Z",
    "null",
    "Null",
    "~",
    "",
    "1",
    "1.0",
    "-3",
    "0x1f",
    "0o17",
    "1_000",
    ".inf",
    "-1.5e3",
    " padded ",
]


def load_as(text: str, version: tuple[int, int]) -> Any:
    yaml = YAML(typ="safe", pure=True)
    yaml.version = version
    return yaml.load(text)


class TestScalarSafety:
    @pytest.mark.parametrize("value", AMBIGUOUS_STRINGS)
    def test_round_trips_under_yaml_1_1_and_1_2(self, value: str) -> None:
        text = yaml_document({"value": value})
        assert load_as(text, (1, 1))["value"] == value
        assert load_as(text, (1, 2))["value"] == value
        assert read_yaml_text(text)["value"] == value

    @pytest.mark.parametrize(
        "value", [12, 0, -3, 1.5, 2.0, True, False, "plain text", "path/to/file.csv"]
    )
    def test_round_trips_genuine_scalars(self, value: object) -> None:
        text = yaml_document({"value": value})
        assert load_as(text, (1, 2))["value"] == value

    def test_a_null_inside_an_opaque_map_is_kept_by_model_conversion(self) -> None:
        # A null *value* in a producer-authored map is data, not an absent optional
        # field, so `to_dict` keeps it (PYTHON_BINDING.md §4.2).
        text = yaml_document(to_dict({"kept": 1, "null_valued": None}))
        assert load_as(text, (1, 2)) == {"kept": 1, "null_valued": None}

    def test_a_null_optional_model_field_is_dropped_by_model_conversion(self) -> None:
        # An optional model field that is None is omitted, so an explicit null and an
        # omitted optional field are the same thing on disk (PYTHON_BINDING.md §8.4).
        text = yaml_document(to_dict(Claim(id="C1", statement="s", stance=None)))
        assert load_as(text, (1, 2)) == {"id": "C1", "statement": "s", "validators": []}

    def test_reading_an_explicit_null_yields_none(self) -> None:
        assert load_as("value: null\n", (1, 2))["value"] is None
        assert load_as("value: ~\n", (1, 2))["value"] is None

    def test_ambiguous_keys_are_quoted_too(self) -> None:
        text = yaml_document({"no": 1, "12:30": 2, "plain": 3})
        assert load_as(text, (1, 1)) == {"no": 1, "12:30": 2, "plain": 3}

    def test_unambiguous_strings_are_not_quoted(self) -> None:
        text = yaml_document({"a": "plain text", "b": "path/to/file.csv", "c": "sha256:abc"})
        assert "'" not in text and '"' not in text

    def test_multiline_and_unicode_survive(self) -> None:
        value = "line one\nline two — em dash\n"
        text = yaml_document({"value": value})
        assert load_as(text, (1, 2))["value"] == value
        assert load_as(text, (1, 1))["value"] == value


def read_yaml_text(text: str) -> Any:
    """Parse with the SDK's own reader, via a temporary file."""
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "doc.yml"
        path.write_text(text, encoding="utf-8")
        return read_yaml(path)


class TestDocumentShape:
    def test_keys_keep_insertion_order(self) -> None:
        text = yaml_document({"z": 1, "m": 2, "a": 3})
        assert [line.split(":")[0] for line in text.splitlines()] == ["z", "m", "a"]

    def test_block_style_and_no_line_wrapping(self) -> None:
        long_value = "word " * 60
        text = yaml_document({"items": [1, 2, 3], "long": long_value.strip()})
        assert "items:\n- 1\n- 2\n- 3\n" in text
        assert len(text.splitlines()) == 5

    def test_documents_end_with_a_newline_and_use_unix_endings(self) -> None:
        text = yaml_document({"a": 1})
        assert text.endswith("\n")
        assert "\r" not in text


class TestReaderIsCoreSchema:
    @pytest.mark.parametrize(
        ("source", "expected"),
        [
            ("value: no\n", "no"),
            ("value: on\n", "on"),
            ("value: 12:30\n", "12:30"),
            ("value: 1_000\n", "1_000"),
            ("value: 2026-01-01T00:00:00.000Z\n", "2026-01-01T00:00:00.000Z"),
            ("value: true\n", True),
            ("value: 12\n", 12),
            ("value: 0x1f\n", 31),
            ("value: 1.5\n", 1.5),
            ("value: null\n", None),
        ],
    )
    def test_plain_scalars_resolve_by_the_core_schema(self, source: str, expected: object) -> None:
        # The other binding emits YAML 1.2; reading it with 1.1 rules would change types.
        assert read_yaml_text(source)["value"] == expected

    def test_an_empty_document_reads_as_an_empty_mapping(self) -> None:
        assert read_yaml_text("") == {}


class TestScalarsThroughTheModel:
    def test_ambiguous_values_survive_write_and_reopen(self, out_dir: Path) -> None:
        artifact = create_artifact(
            id="scalars", title="no", producer={"values": AMBIGUOUS_STRINGS}
        )
        add_claim(artifact, Claim(id="null", statement="12:30"))
        add_result(
            artifact,
            Result(id="on", validates=["null"], evidence="results/out.csv", kind="metrics"),
        )
        write_submission(artifact, out_dir)
        reopened = open_submission(out_dir)
        assert reopened.title == "no"
        assert reopened.producer == {"values": AMBIGUOUS_STRINGS}
        assert reopened.claims[0].id == "null"
        assert reopened.claims[0].statement == "12:30"
        assert reopened.results[0].id == "on"

    def test_numbers_and_booleans_keep_their_types(self, out_dir: Path) -> None:
        artifact = create_artifact(
            id="numbers",
            title="t",
            producer={"count": 12, "ratio": 0.5, "whole": 2.0, "flag": True, "off": False},
        )
        write_submission(artifact, out_dir)
        producer = open_submission(out_dir).producer
        assert producer is not None
        assert producer["count"] == 12 and isinstance(producer["count"], int)
        assert producer["ratio"] == 0.5
        assert producer["whole"] == 2.0
        assert producer["flag"] is True
        assert producer["off"] is False

    def test_an_explicit_null_in_an_opaque_map_survives_write_and_reopen(
        self, out_dir: Path
    ) -> None:
        artifact = create_artifact(
            id="nulls", title="t", producer={"kept": 1, "null_valued": None}
        )
        write_submission(artifact, out_dir)
        manifest = read_yaml(out_dir / "manifest.yml")
        assert manifest["producer"] == {"kept": 1, "null_valued": None}
        assert open_submission(out_dir).producer == {"kept": 1, "null_valued": None}

    def test_a_null_optional_model_field_is_dropped_on_write(self, out_dir: Path) -> None:
        artifact = create_artifact(id="nulls", title="t")
        add_claim(artifact, Claim(id="C1", statement="s", stance=None))
        write_submission(artifact, out_dir)
        assert "stance" not in read_yaml(out_dir / "claims.yml")["claims"][0]
        assert open_submission(out_dir).claims[0].stance is None

    def test_emission_is_byte_idempotent_for_ambiguous_content(self, out_dir: Path) -> None:
        artifact = create_artifact(id="scalars", title="no", producer={"v": AMBIGUOUS_STRINGS})
        write_submission(artifact, out_dir)
        first = (out_dir / "manifest.yml").read_text(encoding="utf-8")
        write_submission(open_submission(out_dir), out_dir)
        assert (out_dir / "manifest.yml").read_text(encoding="utf-8") == first
