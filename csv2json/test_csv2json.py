import pytest

from csv2json import main, parse_csv


def test_basic_comma():
    rows = parse_csv("a,b\n1,2\n3,4\n")
    assert rows == [{"a": "1", "b": "2"}, {"a": "3", "b": "4"}]


def test_semicolon_autodetect():
    rows = parse_csv("name;age\nAda;36\n")
    assert rows == [{"name": "Ada", "age": "36"}]


def test_special_characters_escaped_via_quotes():
    # A field containing a comma and quotes, properly CSV-quoted.
    rows = parse_csv('note,val\n"hello, ""world""",1\n')
    assert rows[0]["note"] == 'hello, "world"'
    assert rows[0]["val"] == "1"


def test_newline_inside_quoted_field():
    rows = parse_csv('a,b\n"line1\nline2",x\n')
    assert rows[0]["a"] == "line1\nline2"


def test_forced_delimiter_pipe():
    rows = parse_csv("a|b\n1|2\n", delimiter="|")
    assert rows == [{"a": "1", "b": "2"}]


def test_empty_input():
    assert parse_csv("") == []


def test_main_rejects_multi_character_delimiter(tmp_path):
    src = tmp_path / "in.csv"
    src.write_text("a;b\n1;2\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc_info:
        main([str(src), str(tmp_path / "out.json"), "--delimiter", ";;"])
    assert exc_info.value.code == 2
