# csv-json-cli-tools

Two small, dependency-free Python command line converters. Standard library only,
Python 3.10+. Each tool is one file with its own pytest suite.

| Tool | Direction | Tests |
|------|-----------|-------|
| [json2csv](json2csv/) | JSON array of objects to CSV | 5 |
| [csv2json](csv2json/) | CSV to JSON array of objects | 6 |

11 tests total, all passing.

## json2csv

Converts a JSON array of flat objects to CSV. The header is the union of all keys
across every object in first-seen order, so a key that only appears on later rows
still gets a column. A missing key writes an empty value, and so does `null`.
Nested arrays and objects are serialised as compact JSON, so no data is lost in
the cells. Invalid JSON, or a top level that is not an array of objects, gives a
clear error and exit code 1.

Tests cover missing-key fill, header ordering, nested-value serialisation, null
handling, and non-array rejection.

## csv2json

Converts CSV to a JSON array of objects, one object per row keyed by the header.
The delimiter is sniffed automatically (comma, semicolon, tab, pipe) and can be
forced with `--delimiter`. Parsing uses the standard `csv` module and output uses
the standard `json` encoder, so fields containing commas, escaped quotes and
embedded newlines survive the round trip. Empty input gives `[]`.

Tests cover comma and semicolon dialects, quoted special characters, embedded
newlines, forced delimiter, and empty input.

## Usage

Both tools read from a file or stdin and write to a file or stdout, using `-` for
the stream.

```bash
python json2csv/json2csv.py input.json output.csv
cat input.json | python json2csv/json2csv.py - output.csv
python json2csv/json2csv.py input.json -

python csv2json/csv2json.py input.csv output.json
python csv2json/csv2json.py in.csv out.json --delimiter ';'
```

## Running the tests

```bash
pip install pytest
cd json2csv && pytest -q
cd ../csv2json && pytest -q
```

## Scope

These are deliberately small single-purpose tools. They assume a flat object
structure on the JSON side. For lossless conversion of nested structures in both
directions, with dotted-key flattening and type inference, see
[tabular-convert](https://github.com/clawedassistant26/tabular-convert).

## Licence

MIT. See [LICENSE](LICENSE).
