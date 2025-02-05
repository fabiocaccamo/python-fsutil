from __future__ import annotations

import os
import sys
import tarfile
import zipfile
from collections.abc import Callable, Iterable
from typing import Literal

from fsutil.args import get_path as _get_path
from fsutil.checks import (
    assert_exists,
    assert_file,
    assert_not_dir,
    assert_not_exists,
    assert_not_file,
    is_dir,
    is_file,
)
from fsutil.core import make_dirs, make_dirs_for_file, remove_file
from fsutil.paths import get_filename, join_path
from fsutil.types import PathIn


def create_tar_file(
    path: PathIn,
    content_paths: list[PathIn],
    *,
    overwrite: bool = True,
    compression: str = "",  # literal: gz, bz2, xz
) -> None:
    """
    Create tar file at path compressing directories/files listed in content_paths.
    If overwrite is allowed and dest tar already exists, it will be overwritten.
    """
    path = _get_path(path)
    assert_not_dir(path)
    if not overwrite:
        assert_not_exists(path)
    make_dirs_for_file(path)

    def _write_content_to_tar_file(
        file: tarfile.TarFile, content_path: PathIn, basedir: str = ""
    ) -> None:
        path = _get_path(content_path)
        assert_exists(path)
        if is_file(path):
            filename = get_filename(path)
            filepath = join_path(basedir, filename)
            file.add(path, filepath)
        elif is_dir(path):
            for item_name in os.listdir(path):
                item_path = join_path(path, item_name)
                item_basedir = (
                    join_path(basedir, item_name) if is_dir(item_path) else basedir
                )
                _write_content_to_tar_file(file, item_path, item_basedir)

    mode = f"w:{compression}" if compression else "w"
    with tarfile.open(path, mode=mode) as file:  # type: ignore
        for content_path in content_paths:
            _write_content_to_tar_file(file, content_path)


def create_zip_file(
    path: PathIn,
    content_paths: list[PathIn],
    *,
    overwrite: bool = True,
    compression: int = zipfile.ZIP_DEFLATED,
) -> None:
    """
    Create zip file at path compressing directories/files listed in content_paths.
    If overwrite is allowed and dest zip already exists, it will be overwritten.
    """
    path = _get_path(path)
    assert_not_dir(path)
    if not overwrite:
        assert_not_exists(path)
    make_dirs_for_file(path)

    def _write_content_to_zip_file(
        file: zipfile.ZipFile, content_path: PathIn, basedir: str = ""
    ) -> None:
        path = _get_path(content_path)
        assert_exists(path)
        if is_file(path):
            filename = get_filename(path)
            filepath = join_path(basedir, filename)
            file.write(path, filepath)
        elif is_dir(path):
            for item_name in os.listdir(path):
                item_path = join_path(path, item_name)
                item_basedir = (
                    join_path(basedir, item_name) if is_dir(item_path) else basedir
                )
                _write_content_to_zip_file(file, item_path, item_basedir)

    with zipfile.ZipFile(path, "w", compression) as file:
        for content_path in content_paths:
            _write_content_to_zip_file(file, content_path)


def extract_tar_file(
    path: PathIn,
    dest: PathIn,
    *,
    autodelete: bool = False,
    content_paths: Iterable[tarfile.TarInfo] | None = None,
    filter: (
        Callable[[tarfile.TarInfo, str], tarfile.TarInfo | None]
        | Literal["fully_trusted", "tar", "data"]
    )
    | None = None,
) -> None:
    """
    Extract tar file at path to dest path.
    If autodelete, the archive will be deleted after extraction.
    If content_paths list is defined,
    only listed items will be extracted, otherwise all.
    """
    path = _get_path(path)
    dest = _get_path(dest)
    assert_file(path)
    assert_not_file(dest)
    make_dirs(dest)
    with tarfile.TarFile(path, "r") as file:
        if sys.version_info < (3, 12):
            file.extractall(dest, members=content_paths)
        else:
            # https://docs.python.org/3/library/tarfile.html#tarfile-extraction-filter
            file.extractall(
                dest,
                members=content_paths,
                numeric_owner=False,
                filter=(filter or "data"),
            )
    if autodelete:
        remove_file(path)


def extract_zip_file(
    path: PathIn,
    dest: PathIn,
    *,
    autodelete: bool = False,
    content_paths: Iterable[str | zipfile.ZipInfo] | None = None,
) -> None:
    """
    Extract zip file at path to dest path.
    If autodelete, the archive will be deleted after extraction.
    If content_paths list is defined,
    only listed items will be extracted, otherwise all.
    """
    path = _get_path(path)
    dest = _get_path(dest)
    assert_file(path)
    assert_not_file(dest)
    make_dirs(dest)
    with zipfile.ZipFile(path, "r") as file:
        file.extractall(dest, members=content_paths)
    if autodelete:
        remove_file(path)
