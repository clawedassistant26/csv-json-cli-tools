#!/usr/bin/env python3
"""Convert a JSON file (array of flat objects) to CSV.

Missing keys are filled with an empty string. The CSV header is the union of
all keys across every object, preserving first-seen order so the output is
stable and predictable.

Usage:
    python json2csv.py input.json output.csv
    cat input.json | python json2csv.py - output.csv   # read JSON from stdin
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from typing import Any


def collect_fieldnames(rows: list[dict[str, Any]]) -> list[str]:
    """Union of keys across all rows, in first-seen order."""
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    return fieldnames


def load_rows(text: str) -> list[dict[str, Any]]:
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError("Top-level JSON must be an array of objects.")
    rows: list[dict[str, Any]] = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Element {i} is not an object (got {type(item).__name__}).")
        rows.append(item)
    return rows


def to_csv(rows: list[dict[str, Any]], out) -> None:
    fieldnames = collect_fieldnames(rows)
    writer = csv.DictWriter(out, fieldnames=fieldnames, restval="", extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        # Serialize nested values (lists/dicts) as JSON so nothing is lost silently.
        clean = {
            k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else
                ("" if v is None else v))
            for k, v in row.items()
        }
        writer.writerow(clean)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert JSON array-of-objects to CSV.")
    parser.add_argument("input", help="Path to input JSON file, or - for stdin.")
    parser.add_argument("output", help="Path to output CSV file, or - for stdout.")
    args = parser.parse_args(argv)

    text = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    try:
        rows = load_rows(text)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.output == "-":
        to_csv(rows, sys.stdout)
    else:
        with open(args.output, "w", newline="", encoding="utf-8") as fh:
            to_csv(rows, fh)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
