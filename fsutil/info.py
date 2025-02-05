from __future__ import annotations

import hashlib
import os
from datetime import datetime

from fsutil.args import get_path as _get_path
from fsutil.checks import assert_dir, assert_file
from fsutil.converters import convert_size_bytes_to_string
from fsutil.core import search_files
from fsutil.types import PathIn


def get_dir_creation_date(path: PathIn) -> datetime:
    """
    Get the directory creation date.
    """
    path = _get_path(path)
    assert_dir(path)
    creation_timestamp = os.path.getctime(path)
    creation_date = datetime.fromtimestamp(creation_timestamp)
    return creation_date


def get_dir_creation_date_formatted(
    path: PathIn, *, format: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """
    Get the directory creation date formatted using the given format.
    """
    path = _get_path(path)
    date = get_dir_creation_date(path)
    return date.strftime(format)


def get_dir_hash(path: PathIn, *, func: str = "md5") -> str:
    """
    Get the hash of the directory at the given path using
    the specified algorithm function (md5 by default).
    """
    path = _get_path(path)
    assert_dir(path)
    hash = hashlib.new(func)
    files = search_files(path)
    for file in sorted(files):
        file_hash = get_file_hash(file, func=func)
        file_hash_b = bytes(file_hash, "utf-8")
        hash.update(file_hash_b)
    hash_hex = hash.hexdigest()
    return hash_hex


def get_dir_last_modified_date(path: PathIn) -> datetime:
    """
    Get the directory last modification date.
    """
    path = _get_path(path)
    assert_dir(path)
    last_modified_timestamp = os.path.getmtime(path)
    for basepath, dirnames, filenames in os.walk(path):
        for dirname in dirnames:
            dirpath = os.path.join(basepath, dirname)
            last_modified_timestamp = max(
                last_modified_timestamp, os.path.getmtime(dirpath)
            )
        for filename in filenames:
            filepath = os.path.join(basepath, filename)
            last_modified_timestamp = max(
                last_modified_timestamp, os.path.getmtime(filepath)
            )
    last_modified_date = datetime.fromtimestamp(last_modified_timestamp)
    return last_modified_date


def get_dir_last_modified_date_formatted(
    path: PathIn, *, format: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """
    Get the directory last modification date formatted using the given format.
    """
    path = _get_path(path)
    date = get_dir_last_modified_date(path)
    return date.strftime(format)


def get_dir_size(path: PathIn) -> int:
    """
    Get the directory size in bytes.
    """
    path = _get_path(path)
    assert_dir(path)
    size = 0
    for basepath, _, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(basepath, filename)
            if not os.path.islink(filepath):
                size += get_file_size(filepath)
    return size


def get_dir_size_formatted(path: PathIn) -> str:
    """
    Get the directory size formatted using the right unit suffix.
    """
    size = get_dir_size(path)
    size_formatted = convert_size_bytes_to_string(size)
    return size_formatted


def get_file_creation_date(path: PathIn) -> datetime:
    """
    Get the file creation date.
    """
    path = _get_path(path)
    assert_file(path)
    creation_timestamp = os.path.getctime(path)
    creation_date = datetime.fromtimestamp(creation_timestamp)
    return creation_date


def get_file_creation_date_formatted(
    path: PathIn, *, format: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """
    Get the file creation date formatted using the given format.
    """
    path = _get_path(path)
    date = get_file_creation_date(path)
    return date.strftime(format)


def get_file_hash(path: PathIn, *, func: str = "md5") -> str:
    """
    Get the hash of the file at the given path using
    the specified algorithm function (md5 by default).
    """
    path = _get_path(path)
    assert_file(path)
    hash = hashlib.new(func)
    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash.update(chunk)
    hash_hex = hash.hexdigest()
    return hash_hex


def get_file_last_modified_date(path: PathIn) -> datetime:
    """
    Get the file last modification date.
    """
    path = _get_path(path)
    assert_file(path)
    last_modified_timestamp = os.path.getmtime(path)
    last_modified_date = datetime.fromtimestamp(last_modified_timestamp)
    return last_modified_date


def get_file_last_modified_date_formatted(
    path: PathIn, *, format: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """
    Get the file last modification date formatted using the given format.
    """
    path = _get_path(path)
    date = get_file_last_modified_date(path)
    return date.strftime(format)


def get_file_size(path: PathIn) -> int:
    """
    Get the directory size in bytes.
    """
    path = _get_path(path)
    assert_file(path)
    # size = os.stat(path).st_size
    size = os.path.getsize(path)
    return size


def get_file_size_formatted(path: PathIn) -> str:
    """
    Get the directory size formatted using the right unit suffix.
    """
    path = _get_path(path)
    size = get_file_size(path)
    size_formatted = convert_size_bytes_to_string(size)
    return size_formatted
