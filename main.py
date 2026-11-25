#!/usr/bin/env python3
"""Ship the finished front page for Wednesday 25 November 2026.

The picture itself was drawn beforehand, on the build machine, and is
checked into this repository as entry.png next to this file. All this
program does is carry that file into the grader's output folder.

It uses nothing but the standard library on purpose: the grading
sandbox is a bare python:3.13-slim container, it installs nothing, and
it launches the program with `python3 -P -s`, which keeps this file's
own directory off sys.path. So there is no sibling import to resolve,
no Pillow to find, and no font to load here — just a file copy.

Where the picture goes, in order of preference:
  1. the MAKEFUN_OUTPUT_DIR environment variable,
  2. the first command-line argument,
  3. "/output".
"""

import os
import shutil
import sys
from pathlib import Path

PICTURE_NAME = "entry.png"
DEFAULT_OUTPUT = "/output"


def pick_output_dir():
    """Return the directory the picture should be copied into."""
    from_env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if from_env:
        return from_env
    if len(sys.argv) > 1:
        return sys.argv[1]
    return DEFAULT_OUTPUT


def ship_picture():
    """Copy entry.png beside this file into the output directory."""
    source = Path(__file__).resolve().parent / PICTURE_NAME
    if not source.is_file():
        raise FileNotFoundError(
            f"missing {PICTURE_NAME} next to {Path(__file__).name}: "
            "nothing to ship"
        )
    if source.stat().st_size == 0:
        raise ValueError(f"{PICTURE_NAME} is empty: nothing to ship")
    destination_dir = Path(pick_output_dir())
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / PICTURE_NAME
    shutil.copyfile(source, destination)
    copied = destination.stat().st_size
    original = source.stat().st_size
    assert copied == original, (
        f"copied {copied} bytes but the source is {original} bytes"
    )
    print(f"wrote {destination} ({copied} bytes)")


if __name__ == "__main__":
    ship_picture()
