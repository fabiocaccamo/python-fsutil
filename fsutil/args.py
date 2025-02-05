from __future__ import annotations

import os

from fsutil.types import PathIn


def get_path(path: PathIn) -> str:
    if isinstance(path, str):
        return os.path.normpath(path)
    return str(path)
