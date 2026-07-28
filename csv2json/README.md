# csv2json

Convert a CSV file to JSON. Handles different CSV dialects via automatic
delimiter sniffing and correctly preserves special characters (commas, quotes,
embedded newlines) because parsing uses the standard `csv` module and output
uses the standard `json` encoder. Requires Python 3.10+, no third-party packages.

## Usage

```bash
python csv2json.py input.csv output.json          # file to file
python csv2json.py input.csv -                     # write JSON to stdout
python csv2json.py - output.json                   # read CSV from stdin
python csv2json.py in.csv out.json --delimiter ';' # force a delimiter
```

## Behaviour

- Auto-detects comma, semicolon, tab, or pipe delimiters (override with
  `--delimiter`).
- Each row becomes one JSON object keyed by the header row.
- Quoted fields with commas, escaped quotes (`""`), and newlines are parsed
  correctly and re-escaped safely in the JSON output.
- Empty input yields `[]`.

## Test

```bash
pip install pytest
pytest -q
```

Tests cover comma and semicolon dialects, quoted special characters, embedded
newlines, forced delimiter, and empty input.
