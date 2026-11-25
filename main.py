#!/usr/bin/env python3
"""One Star, Written in Sap — entry program.

Writes a single one-line 1-star review, in the voice of a houseplant
reviewing its human owner, to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/
entry.txt when set).

The review, written for this competition:

    One star: my human scrapes my sap off the sill like a stain, waters
    me with cold coffee and calls it a little treat — so I wrote this review in
    sap, the only ink I own, and it will stick around longer than I will.

Why this line: the grievance is the plant's own and stays central — its
sap, its body, is treated as a stain to scrape away, and its water is
yesterday's cold coffee served as a favour. The turn is the title made
literal: the review is written in sap, the only ink a plant owns, and sap
sticks — the last clause lands the joke darkly, because the sticky review
will outlast the plant itself. Fresh, specific detail (scraped sap,
cold coffee) instead of stock wilting/drama phrasing, and the whole
complaint is a genuine one-star review: a clear grievance and a reason
for the single star, in one line.

Deterministic: stdlib only, no network, no randomness, no environment
reads beyond the output directory override. The same bytes every run.
"""

import os
import sys

REVIEW = (
    "One star: my human scrapes my sap off the sill like a stain, "
    "waters me with cold coffee and calls it a little treat \u2014 so I wrote "
    "this review in sap, the only ink I own, and it will stick around "
    "longer than I will."
)

MAX_CHARS = 279


def output_path() -> str:
    """Resolve the output directory: $MAKEFUN_OUTPUT_DIR, then $OUTPUT_DIR,
    then the competition default /output."""
    out_dir = (
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("OUTPUT_DIR")
        or "/output"
    )
    return os.path.join(out_dir, "entry.txt")


def validate(text: str) -> None:
    """Enforce the gate from RULES.txt: UTF-8 text of 1-279 characters,
    not whitespace-only. Also require a single line with no control
    characters and no leading/trailing space, so the file is exactly
    one clean review line."""
    if not text:
        raise ValueError("review is empty")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"review is {len(text)} characters, over the {MAX_CHARS} gate"
        )
    if not text.strip():
        raise ValueError("review is whitespace-only")
    if "\n" in text or "\r" in text:
        raise ValueError("review must be a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("review contains a control character")
    if text != text.strip():
        raise ValueError("review has leading or trailing space")


def main() -> int:
    validate(REVIEW)
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(REVIEW + "\n")
    # Read it back and confirm the round-trip is byte-identical.
    with open(path, "rb") as fh:
        raw = fh.read()
    # Strict UTF-8 decode: the gate reads the file as UTF-8 text, so any
    # undecodable byte would fail it before the judge ever sees the line.
    decoded = raw.decode("utf-8")  # raises UnicodeDecodeError on bad bytes
    if decoded != REVIEW + "\n":
        raise ValueError("entry.txt did not round-trip byte-identically")
    if len(raw) != len((REVIEW + "\n").encode("utf-8")):
        raise ValueError("entry.txt byte length does not match the review")
    print(f"wrote {len(REVIEW)} characters to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
