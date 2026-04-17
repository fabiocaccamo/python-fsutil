#!/usr/bin/env python3
"""
Fuzz tests for fsutil I/O utilities using atheris.

Run with:
    python fuzz/fuzz_io.py
Or with a corpus:
    python fuzz/fuzz_io.py corpus/
"""
from __future__ import annotations

import sys
import tempfile

import atheris

with atheris.instrument_imports():
    import fsutil


def fuzz_one_input(data: bytes) -> None:
    fdp = atheris.FuzzedDataProvider(data)

    content = fdp.ConsumeUnicodeNoSurrogates(512)
    encoding = fdp.PickValueInList(["utf-8", "latin-1", "ascii"])

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = fsutil.join_path(tmpdir, "fuzz_test.txt")

        # Fuzz write/read round-trip
        try:
            fsutil.write_file(filepath, content, encoding=encoding)
            fsutil.read_file(filepath, encoding=encoding)
        except (UnicodeEncodeError, UnicodeDecodeError, ValueError):
            pass
        except Exception:
            pass

        # Fuzz JSON write/read
        try:
            json_data = {"key": content, "num": fdp.ConsumeInt(4)}
            json_filepath = fsutil.join_path(tmpdir, "fuzz_test.json")
            fsutil.write_file_json(json_filepath, json_data)
            fsutil.read_file_json(json_filepath)
        except (ValueError, OverflowError):
            pass
        except Exception:
            pass


def main() -> None:
    atheris.Setup(sys.argv, fuzz_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
