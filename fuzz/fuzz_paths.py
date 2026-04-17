#!/usr/bin/env python3
"""
Fuzz tests for fsutil path utilities using atheris.

Run with:
    python fuzz/fuzz_paths.py
Or with a corpus:
    python fuzz/fuzz_paths.py corpus/
"""
from __future__ import annotations

import sys

import atheris

with atheris.instrument_imports():
    import fsutil


def fuzz_one_input(data: bytes) -> None:
    fdp = atheris.FuzzedDataProvider(data)

    path = fdp.ConsumeUnicodeNoSurrogates(128)

    # Fuzz pure path manipulation functions (no filesystem access)
    try:
        fsutil.get_filename(path)
    except Exception:
        pass

    try:
        fsutil.get_file_basename(path)
    except Exception:
        pass

    try:
        fsutil.get_file_extension(path)
    except Exception:
        pass

    try:
        fsutil.split_filename(path)
    except Exception:
        pass

    try:
        fsutil.split_filepath(path)
    except Exception:
        pass

    try:
        fsutil.split_path(path)
    except Exception:
        pass

    basename = fdp.ConsumeUnicodeNoSurrogates(64)
    extension = fdp.ConsumeUnicodeNoSurrogates(16)

    try:
        fsutil.join_filename(basename, extension)
    except Exception:
        pass

    try:
        fsutil.join_filepath(path, basename)
    except Exception:
        pass

    try:
        fsutil.join_path(path, basename)
    except Exception:
        pass


def main() -> None:
    atheris.Setup(sys.argv, fuzz_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
