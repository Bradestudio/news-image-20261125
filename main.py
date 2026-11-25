#!/usr/bin/env python3
"""Copy-only entry runner for the news-image-20261125 bounty.

The front page is pre-rendered as entry.png (sitting next to this file).
This program only copies that file into the output directory.

Output directory resolution, in order:
  1. the MAKEFUN_OUTPUT_DIR environment variable,
  2. the first command-line argument,
  3. "/output".

Standard library only. No image work, no fonts, no network,
no local imports, no clock, no randomness.
"""

import os
import shutil
import sys
from pathlib import Path


def main(argv):
    here = Path(__file__).resolve().parent
    source = here / "entry.png"

    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    arg_dir = argv[1] if len(argv) > 1 else None
    out_dir = env_dir or arg_dir or "/output"

    destination_dir = Path(out_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination_dir / "entry.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
