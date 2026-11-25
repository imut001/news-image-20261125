"""Entry program for make.fun bounty news-image-20261125.

Python 3.13, standard library only, no network. It writes the pre-built
image for 25 November 2026 to the output directory as entry.png.

Run locally:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
The runner normally uses /output; MAKEFUN_OUTPUT_DIR overrides it for tests.
The copy is byte-for-byte identical on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE = os.path.join(HERE, "entry.png")


def main():
    # MAKEFUN_OUTPUT_DIR exists so the entry can be tested outside /output.
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    # Fixed image for 25 November 2026: copy it, never re-render.
    shutil.copyfile(IMAGE, os.path.join(target_dir, "entry.png"))


if __name__ == "__main__":
    main()
