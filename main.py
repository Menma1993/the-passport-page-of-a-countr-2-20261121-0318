"""Entrypoint: draw the passport spread and write it to /output/entry.png.

draw.py does the drawing (PIL only, deterministic); this file only runs
it and copies the result, using the standard library alone, so both runs
write the same bytes.
"""
import os
import shutil

import draw


def main():
    draw.main()
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile("entry.png", "/output/entry.png")


if __name__ == "__main__":
    main()
