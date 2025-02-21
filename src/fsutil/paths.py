from __future__ import annotations

import os
import uuid
from collections.abc import Callable
from urllib.parse import urlsplit

from fsutil.args import get_path as _get_path
from fsutil.checks import assert_dir, exists
from fsutil.types import PathIn


def get_filename(path: PathIn) -> str:
    """
    Get the filename from the given path/url.
    """
    path = _get_path(path)
    filepath = urlsplit(path).path
    filename = os.path.basename(filepath)
    return filename


def get_file_basename(path: PathIn) -> str:
    """
    Get the file basename from the given path/url.
    """
    path = _get_path(path)
    basename, _ = split_filename(path)
    return basename


def get_file_extension(path: PathIn) -> str:
    """
    Get the file extension from the given path/url.
    """
    path = _get_path(path)
    _, extension = split_filename(path)
    return extension


def get_parent_dir(path: PathIn, *, levels: int = 1) -> str:
    """
    Get the parent directory for the given path going up N levels.
    """
    path = _get_path(path)
    return join_path(path, *([os.pardir] * max(1, levels)))


def get_unique_name(
    path: PathIn,
    *,
    prefix: str = "",
    suffix: str = "",
    extension: str = "",
    separator: str = "-",
) -> str:
    """
    Get a unique name for a directory/file at the given directory path.
    """
    path = _get_path(path)
    assert_dir(path)
    name = ""
    while True:
        if prefix:
            name += f"{prefix}{separator}"
        uid = uuid.uuid4()
        name += f"{uid}"
        if suffix:
            name += f"{separator}{suffix}"
        if extension:
            extension = extension.lstrip(".").lower()
            name += f".{extension}"
        if exists(join_path(path, name)):
            continue
        break
    return name


def join_filename(basename: str, extension: str) -> str:
    """
    Create a filename joining the file basename and the extension.
    """
    basename = basename.rstrip(".").strip()
    extension = extension.replace(".", "").strip()
    if basename and extension:
        filename = f"{basename}.{extension}"
        return filename
    return basename or extension


def join_filepath(dirpath: PathIn, filename: str) -> str:
    """
    Create a filepath joining the directory path and the filename.
    """
    dirpath = _get_path(dirpath)
    return join_path(dirpath, filename)


def join_path(path: PathIn, *paths: PathIn) -> str:
    """
    Create a path joining path and paths.
    If path is __file__ (or a .py file), the resulting path will be relative
    to the directory path of the module in which it's used.
    """
    path = _get_path(path)
    basepath = path
    if get_file_extension(path) in ["py", "pyc", "pyo"]:
        basepath = os.path.dirname(os.path.realpath(path))
    paths_str = [_get_path(path).lstrip("/\\") for path in paths]
    return os.path.normpath(os.path.join(basepath, *paths_str))


def split_filename(path: PathIn) -> tuple[str, str]:
    """
    Split a filename and returns its basename and extension.
    """
    path = _get_path(path)
    filename = get_filename(path)
    basename, extension = os.path.splitext(filename)
    extension = extension.replace(".", "").strip()
    return (basename, extension)


def split_filepath(path: PathIn) -> tuple[str, str]:
    """
    Split a filepath and returns its directory-path and filename.
    """
    path = _get_path(path)
    dirpath = os.path.dirname(path)
    filename = get_filename(path)
    return (dirpath, filename)


def split_path(path: PathIn) -> list[str]:
    """
    Split a path and returns its path-names.
    """
    path = _get_path(path)
    head, tail = os.path.split(path)
    names = head.split(os.sep) + [tail]
    names = list(filter(None, names))
    return names


def transform_filepath(
    path: PathIn,
    *,
    dirpath: str | Callable[[str], str] | None = None,
    basename: str | Callable[[str], str] | None = None,
    extension: str | Callable[[str], str] | None = None,
) -> str:
    """
    Trasform a filepath by applying the provided optional changes.

    :param path: The path.
    :type path: PathIn
    :param dirpath: The new dirpath or a callable.
    :type dirpath: str | Callable[[str], str] | None
    :param basename: The new basename or a callable.
    :type basename: str | Callable[[str], str] | None
    :param extension: The new extension or a callable.
    :type extension: str | Callable[[str], str] | None

    :returns: The filepath with the applied changes.
    :rtype: str
    """

    def _get_value(
        new_value: str | Callable[[str], str] | None,
        old_value: str,
    ) -> str:
        value = old_value
        if new_value is not None:
            if callable(new_value):
                value = new_value(old_value)
            elif isinstance(new_value, str):
                value = new_value
            else:
                value = old_value
        return value

    if all([dirpath is None, basename is None, extension is None]):
        raise ValueError(
            "Invalid arguments: at least one of "
            "'dirpath', 'basename' or 'extension' is required."
        )
    old_dirpath, old_filename = split_filepath(path)
    old_basename, old_extension = split_filename(old_filename)
    new_dirpath = _get_value(dirpath, old_dirpath)
    new_basename = _get_value(basename, old_basename)
    new_extension = _get_value(extension, old_extension)
    if not any([new_dirpath, new_basename, new_extension]):
        raise ValueError(
            "Invalid arguments: at least one of "
            "'dirpath', 'basename' or 'extension' is required."
        )
    new_filename = join_filename(new_basename, new_extension)
    new_filepath = join_filepath(new_dirpath, new_filename)
    return new_filepath
