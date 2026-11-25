#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261124 bounty (v2).

Copies the finished poster (poster.png, drawn by poster.py) to the
output directory as entry.png. Standard library only, no network,
deterministic: running it twice writes byte-identical output.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "poster.png")
    dst = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(src):
        print("missing poster.png next to main.py", file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)
    print("wrote", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
