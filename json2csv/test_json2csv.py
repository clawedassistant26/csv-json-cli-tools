import csv
import io
import json

from json2csv import collect_fieldnames, load_rows, to_csv


def test_missing_keys_filled_with_empty_string():
    rows = [{"a": 1, "b": 2}, {"a": 3}]
    out = io.StringIO()
    to_csv(rows, out)
    lines = out.getvalue().splitlines()
    assert lines[0] == "a,b"
    assert lines[1] == "1,2"
    assert lines[2] == "3,"  # missing 'b' -> empty


def test_fieldname_union_preserves_first_seen_order():
    rows = [{"b": 1}, {"a": 2, "c": 3}]
    assert collect_fieldnames(rows) == ["b", "a", "c"]


def test_nested_values_serialized_as_json():
    # Nested values are JSON-serialized; the CSV layer quotes/escapes them, so
    # parse the CSV back and assert on the decoded cell rather than raw bytes.
    rows = [{"tags": ["x", "y"], "meta": {"k": 1}}]
    out = io.StringIO()
    to_csv(rows, out)
    parsed = list(csv.DictReader(io.StringIO(out.getvalue())))[0]
    assert json.loads(parsed["tags"]) == ["x", "y"]
    assert json.loads(parsed["meta"]) == {"k": 1}


def test_none_becomes_empty():
    # A lone empty field round-trips to an empty string via the csv reader
    # (Python writes it as "" so it is not confused with a blank line).
    rows = [{"a": None}]
    out = io.StringIO()
    to_csv(rows, out)
    parsed = list(csv.DictReader(io.StringIO(out.getvalue())))[0]
    assert parsed["a"] == ""


def test_load_rows_rejects_non_array():
    try:
        load_rows(json.dumps({"a": 1}))
    except ValueError:
        return
    raise AssertionError("expected ValueError for non-array input")
