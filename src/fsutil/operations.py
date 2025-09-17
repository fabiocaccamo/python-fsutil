from __future__ import annotations

import glob
import os
import re
import shutil
import tempfile
import uuid
from collections.abc import Callable
from typing import Any

from fsutil.args import get_path as _get_path
from fsutil.checks import (
    assert_dir,
    assert_file,
    assert_not_dir,
    assert_not_exists,
    assert_not_file,
    exists,
    is_dir,
    is_empty_dir,
    is_empty_file,
    is_file,
)
from fsutil.deps import require_requests
from fsutil.paths import (
    get_file_basename,
    get_file_extension,
    get_filename,
    get_unique_name,
    join_filename,
    join_filepath,
    join_path,
    split_filename,
    split_filepath,
)
from fsutil.types import PathIn


def _clean_dir_empty_dirs(path: PathIn) -> None:
    path = _get_path(path)
    for basepath, dirnames, _ in os.walk(path, topdown=False):
        for dirname in dirnames:
            dirpath = os.path.join(basepath, dirname)
            if is_empty_dir(dirpath):
                remove_dir(dirpath)


def _clean_dir_empty_files(path: PathIn) -> None:
    path = _get_path(path)
    for basepath, _, filenames in os.walk(path, topdown=False):
        for filename in filenames:
            filepath = os.path.join(basepath, filename)
            if is_empty_file(filepath):
                remove_file(filepath)


def clean_dir(path: PathIn, *, dirs: bool = True, files: bool = True) -> None:
    """
    Clean a directory by removing empty directories and/or empty files.
    """
    path = _get_path(path)
    assert_dir(path)
    if files:
        _clean_dir_empty_files(path)
    if dirs:
        _clean_dir_empty_dirs(path)


def copy_dir(
    path: PathIn, dest: PathIn, *, overwrite: bool = False, **kwargs: Any
) -> None:
    """
    Copy the directory at the given path and all its content to dest path.
    If overwrite is not allowed and dest path exists, an OSError is raised.
    More informations about kwargs supported options here:
    https://docs.python.org/3/library/shutil.html#shutil.copytree
    """
    path = _get_path(path)
    dest = _get_path(dest)
    assert_dir(path)
    dirname = os.path.basename(os.path.normpath(path))
    dest = os.path.join(dest, dirname)
    assert_not_file(dest)
    if not overwrite:
        assert_not_exists(dest)
    copy_dir_content(path, dest, **kwargs)


def copy_dir_content(path: PathIn, dest: PathIn, **kwargs: Any) -> None:
    """
    Copy the content of the directory at the given path to dest path.
    More informations about kwargs supported options here:
    https://docs.python.org/3/library/shutil.html#shutil.copytree
    """
    path = _get_path(path)
    dest = _get_path(dest)
    assert_dir(path)
    assert_not_file(dest)
    make_dirs(dest)
    kwargs.setdefault("dirs_exist_ok", True)
    shutil.copytree(path, dest, **kwargs)


def copy_file(
    path: PathIn, dest: PathIn, *, overwrite: bool = False, **kwargs: Any
) -> None:
    """
    Copy the file at the given path and its metadata to dest path.
    If overwrite is not allowed and dest path exists, an OSError is raised.
    More informations about kwargs supported options here:
    https://docs.python.org/3/library/shutil.html#shutil.copy2
    """
    path = _get_path(path)
    dest = _get_path(dest)
    assert_file(path)
    assert_not_dir(dest)
    if not overwrite:
        assert_not_exists(dest)
    make_dirs_for_file(dest)
    shutil.copy2(path, dest, **kwargs)


def create_dir(path: PathIn, *, overwrite: bool = False) -> None:
    """
    Create directory at the given path.
    If overwrite is not allowed and path exists, an OSError is raised.
    """
    path = _get_path(path)
    assert_not_file(path)
    if not overwrite:
        assert_not_exists(path)
    make_dirs(path)


def create_file(path: PathIn, content: str = "", *, overwrite: bool = False) -> None:
    """
    Create file with the specified content at the given path.
    If overwrite is not allowed and path exists, an OSError is raised.
    """
    from fsutil.io import write_file

    path = _get_path(path)
    assert_not_dir(path)
    if not overwrite:
        assert_not_exists(path)
    write_file(path, content)


def delete_dir(path: PathIn) -> bool:
    """
    Alias for remove_dir.
    """
    removed = remove_dir(path)
    return removed


def delete_dir_content(path: PathIn) -> None:
    """
    Alias for remove_dir_content.
    """
    remove_dir_content(path)


def delete_dirs(*paths: PathIn) -> None:
    """
    Alias for remove_dirs.
    """
    remove_dirs(*paths)


def delete_file(path: PathIn) -> bool:
    """
    Alias for remove_file.
    """
    removed = remove_file(path)
    return removed


def delete_files(*paths: PathIn) -> None:
    """
    Alias for remove_files.
    """
    remove_files(*paths)


def download_file(
    url: str,
    *,
    dirpath: PathIn | None = None,
    filename: str | None = None,
    chunk_size: int = 8192,
    **kwargs: Any,
) -> str:
    """
    Download a file from url to dirpath.
    If dirpath is not provided, the file will be downloaded to a temp directory.
    If filename is provided, the file will be named using filename.
    It is possible to pass extra request options
    (eg. for authentication) using **kwargs.
    """
    requests = require_requests()
    # https://stackoverflow.com/a/16696317/2096218

    kwargs["stream"] = True
    with requests.get(url, **kwargs) as response:
        response.raise_for_status()

        # build filename
        if not filename:
            # detect filename from headers
            content_disposition = response.headers.get("content-disposition", "") or ""
            # Improved regex to handle various filename formats in Content-Disposition
            filename_patterns = [
                r'filename\*=UTF-8\'\'([^;]+)',  # RFC 5987 encoded filename
                r'filename="([^"]*)"',           # quoted filename
                r"filename='([^']*)'",           # single quoted filename
                r'filename=([^;]+)',             # unquoted filename
            ]
            for pattern in filename_patterns:
                filename_match = re.search(pattern, content_disposition, re.IGNORECASE)
                if filename_match:
                    filename = filename_match.group(1).strip()
                    # URL decode if it's an encoded filename
                    if pattern.startswith(r'filename\*'):
                        import urllib.parse
                        filename = urllib.parse.unquote(filename)
                    break

            # or detect filename from url
            if not filename:
                filename = get_filename(url)
            # or fallback to a unique name
            if not filename:
                filename_uuid = str(uuid.uuid4())
                filename = f"download-{filename_uuid}"

        # build filepath
        dirpath = dirpath or tempfile.gettempdir()
        dirpath = _get_path(dirpath)
        filepath = join_path(dirpath, filename)
        make_dirs_for_file(filepath)

        # write file to disk
        with open(filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
    return filepath


def _filter_paths(
    basepath: str,
    relpaths: list[str],
    *,
    predicate: Callable[[str], bool] | None = None,
) -> list[str]:
    """
    Filter paths relative to basepath according to the optional predicate function.
    If predicate is defined, paths are filtered using it,
    otherwise all paths will be listed.
    """
    paths = []
    for relpath in relpaths:
        abspath = os.path.join(basepath, relpath)
        if predicate is None or predicate(abspath):
            paths.append(abspath)
    paths.sort()
    return paths


def list_dirs(path: PathIn) -> list[str]:
    """
    List all directories contained at the given directory path.
    """
    path = _get_path(path)
    return _filter_paths(path, os.listdir(path), predicate=is_dir)


def list_files(path: PathIn) -> list[str]:
    """
    List all files contained at the given directory path.
    """
    path = _get_path(path)
    return _filter_paths(path, os.listdir(path), predicate=is_file)


def make_dirs(path: PathIn) -> None:
    """
    Create the directories needed to ensure that the given path exists.
    If a file already exists at the given path an OSError is raised.
    """
    path = _get_path(path)
    if is_dir(path):
        return
    assert_not_file(path)
    os.makedirs(path, exist_ok=True)


def make_dirs_for_file(path: PathIn) -> None:
    """
    Create the directories needed to ensure that the given path exists.
    If a directory already exists at the given path an OSError is raised.
    """
    path = _get_path(path)
    if is_file(path):
        return
    assert_not_dir(path)
    dirpath, _ = split_filepath(path)
    if dirpath:
        make_dirs(dirpath)


def move_dir(
    path: PathIn, dest: PathIn, *, overwrite: bool = False, **kwargs: Any
) -> None:
    """
    Move an existing dir from path to dest directory.
    If overwrite is not allowed and dest path exists, an OSError is raised.
    More informations about kwargs supported options here:
    https://docs.python.org/3/library/shutil.html#shutil.move
    """
    path = _get_path(path)
    dest = _get_path(dest)
    assert_dir(path)
    assert_not_file(dest)
    if not overwrite:
        assert_not_exists(dest)
    make_dirs(dest)
    shutil.move(path, dest, **kwargs)


def move_file(
    path: PathIn, dest: PathIn, *, overwrite: bool = False, **kwargs: Any
) -> None:
    """
    Move an existing file from path to dest directory.
    If overwrite is not allowed and dest path exists, an OSError is raised.
    More informations about kwargs supported options here:
    https://docs.python.org/3/library/shutil.html#shutil.move
    """
    path = _get_path(path)
    dest = _get_path(dest)
    assert_file(path)
    assert_not_file(dest)
    dest = os.path.join(dest, get_filename(path))
    assert_not_dir(dest)
    if not overwrite:
        assert_not_exists(dest)
    make_dirs_for_file(dest)
    shutil.move(path, dest, **kwargs)


def remove_dir(path: PathIn, **kwargs: Any) -> bool:
    """
    Remove a directory at the given path and all its content.
    If the directory is removed with success returns True, otherwise False.
    More informations about kwargs supported options here:
    https://docs.python.org/3/library/shutil.html#shutil.rmtree
    """
    path = _get_path(path)
    if not exists(path):
        return False
    assert_dir(path)
    shutil.rmtree(path, **kwargs)
    return not exists(path)


def remove_dir_content(path: PathIn) -> None:
    """
    Removes all directory content (both sub-directories and files).
    """
    path = _get_path(path)
    assert_dir(path)
    remove_dirs(*list_dirs(path))
    remove_files(*list_files(path))


def remove_dirs(*paths: PathIn) -> None:
    """
    Remove multiple directories at the given paths and all their content.
    """
    for path in paths:
        remove_dir(path)


def remove_file(path: PathIn) -> bool:
    """
    Remove a file at the given path.
    If the file is removed with success returns True, otherwise False.
    """
    path = _get_path(path)
    if not exists(path):
        return False
    assert_file(path)
    os.remove(path)
    return not exists(path)


def remove_files(*paths: PathIn) -> None:
    """
    Remove multiple files at the given paths.
    """
    for path in paths:
        remove_file(path)


def rename_dir(path: PathIn, name: str) -> None:
    """
    Rename a directory with the given name.
    If a directory or a file with the given name already exists, an OSError is raised.
    """
    path = _get_path(path)
    assert_dir(path)
    comps = list(os.path.split(path))
    comps[-1] = name
    dest = os.path.join(*comps)
    assert_not_exists(dest)
    os.rename(path, dest)


def rename_file(path: PathIn, name: str) -> None:
    """
    Rename a file with the given name.
    If a directory or a file with the given name already exists, an OSError is raised.
    """
    path = _get_path(path)
    assert_file(path)
    dirpath, _ = split_filepath(path)
    dest = join_filepath(dirpath, name)
    assert_not_exists(dest)
    os.rename(path, dest)


def rename_file_basename(path: PathIn, basename: str) -> None:
    """
    Rename a file basename with the given basename.
    """
    path = _get_path(path)
    extension = get_file_extension(path)
    filename = join_filename(basename, extension)
    rename_file(path, filename)


def rename_file_extension(path: PathIn, extension: str) -> None:
    """
    Rename a file extension with the given extension.
    """
    path = _get_path(path)
    basename = get_file_basename(path)
    filename = join_filename(basename, extension)
    rename_file(path, filename)


def replace_dir(path: PathIn, src: PathIn, *, autodelete: bool = False) -> None:
    """
    Replace directory at the specified path with the directory located at src.
    If autodelete, the src directory will be removed at the end of the operation.
    Optimized for large files.
    """
    path = _get_path(path)
    src = _get_path(src)
    assert_not_file(path)
    assert_dir(src)

    if path == src:
        return

    make_dirs(path)

    dirpath, dirname = split_filepath(path)
    # safe temporary name to avoid clashes with existing files/directories
    temp_dirname = get_unique_name(dirpath)
    temp_dest = join_path(dirpath, temp_dirname)
    copy_dir_content(src, temp_dest)

    if exists(path):
        temp_dirname = get_unique_name(dirpath)
        temp_path = join_path(dirpath, temp_dirname)
        rename_dir(path=path, name=temp_dirname)
        rename_dir(path=temp_dest, name=dirname)
        remove_dir(path=temp_path)
    else:
        rename_dir(path=temp_dest, name=dirname)

    if autodelete:
        remove_dir(path=src)


def replace_file(path: PathIn, src: PathIn, *, autodelete: bool = False) -> None:
    """
    Replace file at the specified path with the file located at src.
    If autodelete, the src file will be removed at the end of the operation.
    Optimized for large files.
    """
    path = _get_path(path)
    src = _get_path(src)
    assert_not_dir(path)
    assert_file(src)
    if path == src:
        return

    make_dirs_for_file(path)

    dirpath, filename = split_filepath(path)
    _, extension = split_filename(filename)
    # safe temporary name to avoid clashes with existing files/directories
    temp_filename = get_unique_name(dirpath, extension=extension)
    temp_dest = join_path(dirpath, temp_filename)
    copy_file(path=src, dest=temp_dest, overwrite=False)

    if exists(path):
        temp_filename = get_unique_name(dirpath, extension=extension)
        temp_path = join_path(dirpath, temp_filename)
        rename_file(path=path, name=temp_filename)
        rename_file(path=temp_dest, name=filename)
        remove_file(path=temp_path)
    else:
        rename_file(path=temp_dest, name=filename)

    if autodelete:
        remove_file(path=src)


def _search_paths(path: PathIn, pattern: str) -> list[str]:
    """
    Search all paths relative to path matching the given pattern.
    """
    path = _get_path(path)
    assert_dir(path)
    pathname = os.path.join(path, pattern)
    paths = glob.glob(pathname, recursive=True)
    return paths


def search_dirs(path: PathIn, pattern: str = "**/*") -> list[str]:
    """
    Search for directories at path matching the given pattern.
    """
    path = _get_path(path)
    return _filter_paths(path, _search_paths(path, pattern), predicate=is_dir)


def search_files(path: PathIn, pattern: str = "**/*.*") -> list[str]:
    """
    Search for files at path matching the given pattern.
    """
    path = _get_path(path)
    return _filter_paths(path, _search_paths(path, pattern), predicate=is_file)
