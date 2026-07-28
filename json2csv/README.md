# json2csv

Convert a JSON file (array of flat objects) to CSV. Missing keys are filled with
an empty string. Requires Python 3.10+ and no third-party packages.

## Usage

```bash
python json2csv.py input.json output.csv     # file to file
cat input.json | python json2csv.py - output.csv   # stdin to file
python json2csv.py input.json -              # write CSV to stdout
```

## Behaviour

- Header is the union of all keys across every object, in first-seen order.
- Missing key on a row is written as an empty value.
- `null` is written as an empty value.
- Nested arrays/objects are serialised as compact JSON so no data is lost.
- Clear error and exit code 1 if the top level is not an array of objects, or
  the JSON is invalid.

## Test

```bash
pip install pytest
pytest -q
```

All tests cover: missing-key fill, header ordering, nested-value serialisation,
null handling, and non-array rejection.
