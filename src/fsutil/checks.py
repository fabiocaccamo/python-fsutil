from __future__ import annotations

import os

from fsutil.args import get_path as _get_path
from fsutil.types import PathIn


def assert_dir(path: PathIn) -> None:
    """
    Raise an OSError if the given path doesn't exist or it is not a directory.
    """
    path = _get_path(path)
    if not is_dir(path):
        raise OSError(f"Invalid directory path: {path}")


def assert_exists(path: PathIn) -> None:
    """
    Raise an OSError if the given path doesn't exist.
    """
    path = _get_path(path)
    if not exists(path):
        raise OSError(f"Invalid item path: {path}")


def assert_file(path: PathIn) -> None:
    """
    Raise an OSError if the given path doesn't exist or it is not a file.
    """
    path = _get_path(path)
    if not is_file(path):
        raise OSError(f"Invalid file path: {path}")


def assert_not_dir(path: PathIn) -> None:
    """
    Raise an OSError if the given path is an existing directory.
    """
    path = _get_path(path)
    if is_dir(path):
        raise OSError(f"Invalid path, directory already exists: {path}")


def assert_not_exists(path: PathIn) -> None:
    """
    Raise an OSError if the given path already exists.
    """
    path = _get_path(path)
    if exists(path):
        raise OSError(f"Invalid path, item already exists: {path}")


def assert_not_file(path: PathIn) -> None:
    """
    Raise an OSError if the given path is an existing file.
    """
    path = _get_path(path)
    if is_file(path):
        raise OSError(f"Invalid path, file already exists: {path}")


def exists(path: PathIn) -> bool:
    """
    Check if a directory of a file exists at the given path.
    """
    path = _get_path(path)
    return os.path.exists(path)


def is_dir(path: PathIn) -> bool:
    """
    Determine whether the specified path represents an existing directory.
    """
    path = _get_path(path)
    return os.path.isdir(path)


def is_empty(path: PathIn) -> bool:
    """
    Determine whether the specified path represents an empty directory or an empty file.
    """
    path = _get_path(path)
    assert_exists(path)
    if is_dir(path):
        return is_empty_dir(path)
    return is_empty_file(path)


def is_empty_dir(path: PathIn) -> bool:
    """
    Determine whether the specified path represents an empty directory.
    """
    path = _get_path(path)
    assert_dir(path)
    return len(os.listdir(path)) == 0


def is_empty_file(path: PathIn) -> bool:
    """
    Determine whether the specified path represents an empty file.
    """
    from fsutil.info import get_file_size

    path = _get_path(path)
    return get_file_size(path) == 0


def is_file(path: PathIn) -> bool:
    """
    Determine whether the specified path represents an existing file.
    """
    path = _get_path(path)
    return os.path.isfile(path)
