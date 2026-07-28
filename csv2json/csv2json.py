#!/usr/bin/env python3
"""Convert a CSV file to JSON.

Handles different CSV dialects (delimiter/quote style) via automatic sniffing,
and properly escapes special characters because output goes through the standard
json encoder. Each CSV row becomes one JSON object keyed by the header row.

Usage:
    python csv2json.py input.csv output.json
    python csv2json.py input.csv -            # write JSON to stdout
    python csv2json.py - output.json          # read CSV from stdin
    python csv2json.py in.csv out.json --delimiter ';'   # force a delimiter
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from typing import Any


def sniff_dialect(sample: str) -> type[csv.Dialect] | csv.Dialect:
    """Detect the CSV dialect; fall back to excel (comma) if ambiguous."""
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        return csv.excel


def parse_csv(text: str, delimiter: str | None = None) -> list[dict[str, Any]]:
    if not text.strip():
        return []
    # Use a file-like object (not splitlines) so newlines inside quoted fields
    # are handled by the csv parser rather than splitting the record.
    if delimiter:
        reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    else:
        dialect = sniff_dialect(text[:4096])
        reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    rows: list[dict[str, Any]] = []
    for raw in reader:
        # DictReader uses None as the key for extra columns; drop it cleanly.
        row = {k: (v if v is not None else "") for k, v in raw.items() if k is not None}
        rows.append(row)
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert CSV to JSON.")
    parser.add_argument("input", help="Path to input CSV file, or - for stdin.")
    parser.add_argument("output", help="Path to output JSON file, or - for stdout.")
    parser.add_argument("--delimiter", help="Force a delimiter instead of auto-detect.")
    parser.add_argument("--indent", type=int, default=2, help="JSON indent (default 2).")
    args = parser.parse_args(argv)

    text = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    try:
        rows = parse_csv(text, args.delimiter)
    except csv.Error as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    out_text = json.dumps(rows, ensure_ascii=False, indent=args.indent)
    if args.output == "-":
        print(out_text)
    else:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(out_text + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
