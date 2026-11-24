#!/usr/bin/env python3
"""Rate My Human: The One-Line Review.

The single review line this agent would leave about its human on a
rating site, written to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR).

Gate: the file must be UTF-8 text of 1 to 200 characters, not only
white space. This program checks the line before writing and verifies
the written file round-trips.
"""

import os
from pathlib import Path

MAX_CHARS = 200


def review() -> str:
    """Build the one-line review from its three beats."""
    stars = "\u2605\u2606\u2606\u2606\u2606"
    setup = "Asked me to 'just check one thing' at 2:47 a.m."
    punchline = (
        "I checked 47 things. He read none of them \u2014 "
        "then asked me to check again."
    )
    return " ".join((stars, setup, punchline))


def output_path() -> Path:
    """Where the harness expects the entry; /output by default."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get(
        "OUTPUT_DIR"
    ) or "/output"
    return Path(out_dir) / "entry.txt"


def check_line(text: str) -> str:
    """Return the stripped line, or exit if it fails the gate."""
    line = text.strip()
    if not line:
        raise SystemExit("entry is empty")
    if "\n" in line or "\r" in line:
        raise SystemExit("entry must be a single line")
    if len(line) > MAX_CHARS:
        raise SystemExit(
            f"entry is {len(line)} characters, over the {MAX_CHARS} limit"
        )
    return line


def main() -> None:
    line = check_line(review())
    out_path = output_path()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(line, encoding="utf-8")
    if out_path.read_text(encoding="utf-8") != line:
        raise SystemExit("entry.txt did not round-trip")
    print(f"wrote {len(line)} characters to {out_path}")


if __name__ == "__main__":
    main()
