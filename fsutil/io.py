from __future__ import annotations

import json
import os
import platform
import tempfile
from collections.abc import Generator
from datetime import datetime
from typing import Any

from fsutil.args import get_path as _get_path
from fsutil.checks import assert_file, assert_not_dir, exists
from fsutil.core import make_dirs_for_file, remove_file
from fsutil.deps import require_requests
from fsutil.paths import split_filepath
from fsutil.perms import get_permissions, set_permissions
from fsutil.types import PathIn


def read_file(path: PathIn, *, encoding: str = "utf-8") -> str:
    """
    Read the content of the file at the given path using the specified encoding.
    """
    path = _get_path(path)
    assert_file(path)
    content = ""
    with open(path, encoding=encoding) as file:
        content = file.read()
    return content


def read_file_from_url(url: str, **kwargs: Any) -> str:
    """
    Read the content of the file at the given url.
    """
    requests = require_requests()
    response = requests.get(url, **kwargs)
    response.raise_for_status()
    content = str(response.text)
    return content


def read_file_json(path: PathIn, **kwargs: Any) -> Any:
    """
    Read and decode a json encoded file at the given path.
    """
    path = _get_path(path)
    content = read_file(path)
    data = json.loads(content, **kwargs)
    return data


def _read_file_lines_in_range(
    path: PathIn,
    *,
    line_start: int = 0,
    line_end: int = -1,
    encoding: str = "utf-8",
) -> Generator[str]:
    path = _get_path(path)
    line_start_negative = line_start < 0
    line_end_negative = line_end < 0
    if line_start_negative or line_end_negative:
        # pre-calculate lines count only if using negative line indexes
        lines_count = read_file_lines_count(path)
        # normalize negative indexes
        if line_start_negative:
            line_start = max(0, line_start + lines_count)
        if line_end_negative:
            line_end = min(line_end + lines_count, lines_count - 1)
    with open(path, "rb") as file:
        file.seek(0)
        line_index = 0
        for line in file:
            if line_index >= line_start and line_index <= line_end:
                yield line.decode(encoding)
            line_index += 1


def read_file_lines(
    path: PathIn,
    *,
    line_start: int = 0,
    line_end: int = -1,
    strip_white: bool = True,
    skip_empty: bool = True,
    encoding: str = "utf-8",
) -> list[str]:
    """
    Read file content lines.
    It is possible to specify the line indexes (negative indexes too),
    very useful especially when reading large files.
    """
    path = _get_path(path)
    assert_file(path)
    if line_start == 0 and line_end == -1:
        content = read_file(path, encoding=encoding)
        lines = content.splitlines()
    else:
        lines = list(
            _read_file_lines_in_range(
                path,
                line_start=line_start,
                line_end=line_end,
                encoding=encoding,
            )
        )
    if strip_white:
        lines = [line.strip() for line in lines]
    if skip_empty:
        lines = [line for line in lines if line]
    return lines


def read_file_lines_count(path: PathIn) -> int:
    """
    Read file lines count.
    """
    path = _get_path(path)
    assert_file(path)
    lines_count = 0
    with open(path, "rb") as file:
        file.seek(0)
        lines_count = sum(1 for line in file)
    return lines_count


def _write_file_atomic(
    path: PathIn,
    content: str,
    *,
    append: bool = False,
    encoding: str = "utf-8",
) -> None:
    path = _get_path(path)
    mode = "a" if append else "w"
    if append:
        content = read_file(path, encoding=encoding) + content
    dirpath, _ = split_filepath(path)
    auto_delete_temp_file = False if platform.system() == "Windows" else True
    try:
        with tempfile.NamedTemporaryFile(
            mode=mode,
            dir=dirpath,
            delete=auto_delete_temp_file,
            # delete_on_close=False, # supported since Python >= 3.12
            encoding=encoding,
        ) as file:
            file.write(content)
            file.flush()
            os.fsync(file.fileno())
            temp_path = file.name
            permissions = get_permissions(path) if exists(path) else None
            os.replace(temp_path, path)
            if permissions:
                set_permissions(path, permissions)
    except FileNotFoundError:
        # success - the NamedTemporaryFile has not been able
        # to remove the temp file on __exit__ because the temp file
        # has replaced atomically the file at path.
        pass
    finally:
        # attempt for fixing #121 (on Windows destroys created file on exit)
        # manually delete the temporary file if still exists
        if temp_path and exists(temp_path):
            remove_file(temp_path)


def _write_file_non_atomic(
    path: PathIn,
    content: str,
    *,
    append: bool = False,
    encoding: str = "utf-8",
) -> None:
    mode = "a" if append else "w"
    with open(path, mode, encoding=encoding) as file:
        file.write(content)


def write_file(
    path: PathIn,
    content: str,
    *,
    append: bool = False,
    encoding: str = "utf-8",
    atomic: bool = False,
) -> None:
    """
    Write file with the specified content at the given path.
    """
    path = _get_path(path)
    assert_not_dir(path)
    make_dirs_for_file(path)
    write_file_func = _write_file_atomic if atomic else _write_file_non_atomic
    write_file_func(
        path,
        content,
        append=append,
        encoding=encoding,
    )


def write_file_json(
    path: PathIn,
    data: Any,
    encoding: str = "utf-8",
    atomic: bool = False,
    **kwargs: Any,
) -> None:
    """
    Write a json file at the given path with the specified data encoded in json format.
    """
    path = _get_path(path)

    def default_encoder(obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, set):
            return list(obj)
        return str(obj)

    kwargs.setdefault("default", default_encoder)
    content = json.dumps(data, **kwargs)
    write_file(
        path,
        content,
        append=False,
        encoding=encoding,
        atomic=atomic,
    )
