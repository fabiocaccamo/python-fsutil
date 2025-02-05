from __future__ import annotations

import os

from fsutil.args import get_path as _get_path
from fsutil.checks import assert_exists
from fsutil.types import PathIn


def get_permissions(path: PathIn) -> int:
    """
    Get the file/directory permissions.
    """
    path = _get_path(path)
    assert_exists(path)
    st_mode = os.stat(path).st_mode
    permissions = int(str(oct(st_mode & 0o777))[2:])
    return permissions


def set_permissions(path: PathIn, value: int) -> None:
    """
    Set the file/directory permissions.
    """
    path = _get_path(path)
    assert_exists(path)
    permissions = int(str(value), 8) & 0o777
    os.chmod(path, permissions)
