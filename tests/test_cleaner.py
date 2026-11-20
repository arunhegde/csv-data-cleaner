import csv
import pytest
from csv_cleaner import CleaningError, clean_file, clean_rows


def test_strip_and_dedupe():
    rows = [{"id": " 1 ", "name": " Ada "}, {"id": "1", "name": " Ada "}]
    cleaned, removed = clean_rows(rows, ["id", "name"], required=["id"], dedupe_by=["id"])
    assert cleaned == [{"id": "1", "name": "Ada"}]
    assert removed == 1


def test_missing_required_value():
    with pytest.raises(CleaningError, match="line 2"):
        clean_rows([{"id": "  "}], ["id"], required=["id"])


def test_unknown_column():
    with pytest.raises(CleaningError, match="Unknown columns"):
        clean_rows([], ["id"], dedupe_by=["email"])


def test_malformed_row():
    with pytest.raises(CleaningError, match="Malformed"):
        clean_rows([{"id": "1", None: ["extra"]}], ["id"])


def test_empty_csv_header():
    with pytest.raises(CleaningError, match="header"):
        clean_rows([], [])


def test_file_roundtrip(tmp_path):
    source = tmp_path / "source.csv"
    target = tmp_path / "target.csv"
    source.write_text("id,name\n1, Ada \n1, Ada\n2, Bob\n", encoding="utf-8")
    assert clean_file(source, target, required=["id"], dedupe_by=["id"]) == (2, 1)
    with target.open(newline="", encoding="utf-8") as f:
        assert list(csv.DictReader(f)) == [
            {"id": "1", "name": "Ada"}, {"id": "2", "name": "Bob"}
        ]


def test_invalid_data_does_not_create_output(tmp_path):
    source = tmp_path / "source.csv"
    target = tmp_path / "target.csv"
    source.write_text("id,name\n,Missing ID\n", encoding="utf-8")
    with pytest.raises(CleaningError):
        clean_file(source, target, required=["id"])
    assert not target.exists()


def test_same_input_output_rejected(tmp_path):
    source = tmp_path / "source.csv"
    source.write_text("id\n1\n", encoding="utf-8")
    with pytest.raises(CleaningError, match="must differ"):
        clean_file(source, source)
