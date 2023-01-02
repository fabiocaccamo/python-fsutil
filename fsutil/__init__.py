import errno
import glob
import hashlib
import json
import os
import pathlib
import shutil
import tempfile
import uuid
import zipfile
from datetime import datetime
from urllib.parse import urlsplit

try:
    import requests

    requests_installed = True
except ImportError:
    requests_installed = False

from fsutil.metadata import (
    __author__,
    __copyright__,
    __description__,
    __email__,
    __license__,
    __title__,
    __version__,
)

__all__ = [
    "__author__",
    "__copyright__",
    "__description__",
    "__email__",
    "__license__",
    "__title__",
    "__version__",
    "assert_dir",
    "assert_exists",
    "assert_file",
    "assert_not_dir",
    "assert_not_exists",
    "assert_not_file",
    "clean_dir",
    "convert_size_bytes_to_string",
    "convert_size_string_to_bytes",
    "copy_dir",
    "copy_dir_content",
    "copy_file",
    "create_dir",
    "create_file",
    "create_zip_file",
    "delete_dir",
    "delete_dir_content",
    "delete_dirs",
    "delete_file",
    "delete_files",
    "download_file",
    "exists",
    "extract_zip_file",
    "get_dir_creation_date",
    "get_dir_creation_date_formatted",
    "get_dir_last_modified_date",
    "get_dir_last_modified_date_formatted",
    "get_dir_size",
    "get_dir_size_formatted",
    "get_file_basename",
    "get_file_creation_date",
    "get_file_creation_date_formatted",
    "get_file_extension",
    "get_file_hash",
    "get_file_last_modified_date",
    "get_file_last_modified_date_formatted",
    "get_file_size",
    "get_file_size_formatted",
    "get_filename",
    "get_parent_dir",
    "get_unique_name",
    "is_dir",
    "is_empty",
    "is_empty_dir",
    "is_empty_file",
    "is_file",
    "join_filename",
    "join_filepath",
    "join_path",
    "list_dirs",
    "list_files",
    "make_dirs",
    "make_dirs_for_file",
    "move_dir",
    "move_file",
    "read_file",
    "read_file_from_url",
    "read_file_json",
    "read_file_lines",
    "read_file_lines_count",
    "remove_dir",
    "remove_dir_content",
    "remove_dirs",
    "remove_file",
    "remove_files",
    "rename_dir",
    "rename_file",
    "rename_file_basename",
    "rename_file_extension",
    "replace_dir",
    "replace_file",
    "search_dirs",
    "search_files",
    "split_filename",
    "split_filepath",
    "split_path",
    "write_file",
    "write_file_json",
]

SIZE_UNITS = ["bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]


def _require_requests_installed():
    if not requests_installed:
        raise ModuleNotFoundError(
            "'requests' module is not installed, "
            "it can be installed by running: 'pip install requests'"
        )


def _get_path(path):
    if isinstance(path, str):
        return path
    elif isinstance(path, pathlib.Path):
        return str(path)
    else:
        return path


def assert_dir(path):
    """
    Raise an OSError if the given path doesn't exist or it is not a directory.
    """
    path = _get_path(path)
    if not is_dir(path):
        raise OSError(f"Invalid directory path: {path}")


def assert_exists(path):
    """
    Raise an OSError if the given path doesn't exist.
    """
    path = _get_path(path)
    if not exists(path):
        raise OSError(f"Invalid item path: {path}")


def assert_file(path):
    """
    Raise an OSError if the given path doesn't exist or it is not a file.
    """
    path = _get_path(path)
    if not is_file(path):
        raise OSError(f"Invalid file path: {path}")


def assert_not_dir(path):
    """
    Raise an OSError if the given path is an existing directory.
    """
    path = _get_path(path)
    if is_dir(path):
        raise OSError(f"Invalid path, directory already exists: {path}")


def assert_not_exists(path):
    """
    Raise an OSError if the given path already exists.
    """
    path = _get_path(path)
    if exists(path):
        raise OSError(f"Invalid path, item already exists: {path}")


def assert_not_file(path):
    """
    Raise an OSError if the given path is an existing file.
    """
    path = _get_path(path)
    if is_file(path):
        raise OSError(f"Invalid path, file already exists: {path}")


def _clean_dir_empty_dirs(path):
    path = _get_path(path)
    for basepath, dirnames, _ in os.walk(path, topdown=False):
        for dirname in dirnames:
            dirpath = os.path.join(basepath, dirname)
            if is_empty_dir(dirpath):
                remove_dir(dirpath)


def _clean_dir_empty_files(path):
    path = _get_path(path)
    for basepath, _, filenames in os.walk(path, topdown=False):
        for filename in filenames:
            filepath = os.path.join(basepath, filename)
            if is_empty_file(filepath):
                remove_file(filepath)


def clean_dir(path, dirs=True, files=True):
    """
    Clean a directory by removing empty directories and/or empty files.
    """
    path = _get_path(path)
    assert_dir(path)
    if files:
        _clean_dir_empty_files(path)
    if dirs:
        _clean_dir_empty_dirs(path)


def convert_size_bytes_to_string(size):
    """
    Convert the given size bytes to string using the right unit suffix.
    """
    size = float(size)
    units = SIZE_UNITS
    factor = 0
    factor_limit = len(units) - 1
    while (size >= 1024) and (factor <= factor_limit):
        size /= 1024
        factor += 1
    size_units = units[factor]
    size_str = f"{size:.2f}" if (factor > 1) else f"{size:.0f}"
    size_str = f"{size_str} {size_units}"
    return size_str


def convert_size_string_to_bytes(size):
    """
    Convert the given size string to bytes.
    """
    units = [item.lower() for item in SIZE_UNITS]
    parts = size.strip().replace("  ", " ").split(" ")
    amount = float(parts[0])
    unit = parts[1]
    factor = units.index(unit.lower())
    if not factor:
        return amount
    return int((1024**factor) * amount)


def copy_dir(path, dest, overwrite=False, **kwargs):
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


def copy_dir_content(path, dest, **kwargs):
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


def copy_file(path, dest, overwrite=False, **kwargs):
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


def create_dir(path, overwrite=False):
    """
    Create directory at the given path.
    If overwrite is not allowed and path exists, an OSError is raised.
    """
    path = _get_path(path)
    assert_not_file(path)
    if not overwrite:
        assert_not_exists(path)
    make_dirs(path)


def create_file(path, content="", overwrite=False):
    """
    Create file with the specified content at the given path.
    If overwrite is not allowed and path exists, an OSError is raised.
    """
    path = _get_path(path)
    assert_not_dir(path)
    if not overwrite:
        assert_not_exists(path)
    write_file(path, content)


def create_zip_file(
    path, content_paths, overwrite=True, compression=zipfile.ZIP_DEFLATED
):
    """
    Create zip file at path compressing directories/files listed in content_paths.
    If overwrite is allowed and dest zip already exists, it will be overwritten.
    """
    path = _get_path(path)
    assert_not_dir(path)
    if not overwrite:
        assert_not_exists(path)
    make_dirs_for_file(path)

    def _write_content_to_zip_file(file, path, basedir=""):
        path = _get_path(path)
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


def delete_dir(path):
    """
    Alias for remove_dir.
    """
    removed = remove_dir(path)
    return removed


def delete_dir_content(path):
    """
    Alias for remove_dir_content.
    """
    remove_dir_content(path)


def delete_dirs(*paths):
    """
    Alias for remove_dirs.
    """
    remove_dirs(*paths)


def delete_file(path):
    """
    Alias for remove_file.
    """
    removed = remove_file(path)
    return removed


def delete_files(*paths):
    """
    Alias for remove_files.
    """
    remove_files(*paths)


def download_file(url, dirpath=None, filename=None, chunk_size=8192, **kwargs):
    """
    Download a file from url to dirpath.
    If filename is provided, the file will be named using filename.
    It is possible to pass extra request options (eg. for authentication) using **kwargs.
    """
    _require_requests_installed()
    # https://stackoverflow.com/a/16696317/2096218
    dirpath = dirpath or tempfile.gettempdir()
    dirpath = _get_path(dirpath)
    filename = filename or get_filename(url) or "download"
    filepath = join_path(dirpath, filename)
    make_dirs_for_file(filepath)
    kwargs["stream"] = True
    with requests.get(url, **kwargs) as response:
        response.raise_for_status()
        with open(filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
    return filepath


def exists(path):
    """
    Check if a directory of a file exists at the given path.
    """
    path = _get_path(path)
    return os.path.exists(path)


def extract_zip_file(path, dest, autodelete=False, content_paths=None):
    """
    Extract zip file at path to dest path.
    If autodelete, the archive will be deleted after extraction.
    If content_paths list is defined, only listed items will be extracted, otherwise all.
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


def _filter_paths(basepath, relpaths, predicate=None):
    """
    Filter paths relative to basepath according to the optional predicate function.
    If predicate is defined, paths are filtered using it, otherwise all paths will be listed.
    """
    paths = []
    for relpath in relpaths:
        abspath = os.path.join(basepath, relpath)
        if predicate is None or predicate(abspath):
            paths.append(abspath)
    paths.sort()
    return paths


def get_dir_creation_date(path):
    """
    Get the directory creation date.
    """
    path = _get_path(path)
    assert_dir(path)
    creation_timestamp = os.path.getctime(path)
    creation_date = datetime.fromtimestamp(creation_timestamp)
    return creation_date


def get_dir_creation_date_formatted(path, format="%Y-%m-%d %H:%M:%S"):
    """
    Get the directory creation date formatted using the given format.
    """
    path = _get_path(path)
    date = get_dir_creation_date(path)
    return date.strftime(format)


def get_dir_hash(path, func="md5"):
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


def get_dir_last_modified_date(path):
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


def get_dir_last_modified_date_formatted(path, format="%Y-%m-%d %H:%M:%S"):
    """
    Get the directory last modification date formatted using the given format.
    """
    path = _get_path(path)
    date = get_dir_last_modified_date(path)
    return date.strftime(format)


def get_dir_size(path):
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


def get_dir_size_formatted(path):
    """
    Get the directory size formatted using the right unit suffix.
    """
    size = get_dir_size(path)
    size_formatted = convert_size_bytes_to_string(size)
    return size_formatted


def get_file_basename(path):
    """
    Get the file basename from the given path/url.
    """
    path = _get_path(path)
    basename, _ = split_filename(path)
    return basename


def get_file_creation_date(path):
    """
    Get the file creation date.
    """
    path = _get_path(path)
    assert_file(path)
    creation_timestamp = os.path.getctime(path)
    creation_date = datetime.fromtimestamp(creation_timestamp)
    return creation_date


def get_file_creation_date_formatted(path, format="%Y-%m-%d %H:%M:%S"):
    """
    Get the file creation date formatted using the given format.
    """
    path = _get_path(path)
    date = get_file_creation_date(path)
    return date.strftime(format)


def get_file_extension(path):
    """
    Get the file extension from the given path/url.
    """
    path = _get_path(path)
    _, extension = split_filename(path)
    return extension


def get_file_hash(path, func="md5"):
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


def get_file_last_modified_date(path):
    """
    Get the file last modification date.
    """
    path = _get_path(path)
    assert_file(path)
    last_modified_timestamp = os.path.getmtime(path)
    last_modified_date = datetime.fromtimestamp(last_modified_timestamp)
    return last_modified_date


def get_file_last_modified_date_formatted(path, format="%Y-%m-%d %H:%M:%S"):
    """
    Get the file last modification date formatted using the given format.
    """
    path = _get_path(path)
    date = get_file_last_modified_date(path)
    return date.strftime(format)


def get_file_size(path):
    """
    Get the directory size in bytes.
    """
    path = _get_path(path)
    assert_file(path)
    # size = os.stat(path).st_size
    size = os.path.getsize(path)
    return size


def get_file_size_formatted(path):
    """
    Get the directory size formatted using the right unit suffix.
    """
    path = _get_path(path)
    size = get_file_size(path)
    size_formatted = convert_size_bytes_to_string(size)
    return size_formatted


def get_filename(path):
    """
    Get the filename from the given path/url.
    """
    path = _get_path(path)
    filepath = urlsplit(path).path
    filename = os.path.basename(filepath)
    return filename


def get_parent_dir(path, levels=1):
    """
    Get the parent directory for the given path going up N levels.
    """
    path = _get_path(path)
    return join_path(path, *([os.pardir] * max(1, levels)))


def get_unique_name(path, prefix="", suffix="", extension="", separator="-"):
    """
    Gets a unique name for a directory/file ath the given directory path.
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


def is_dir(path):
    """
    Determine whether the specified path represents an existing directory.
    """
    path = _get_path(path)
    return os.path.isdir(path)


def is_empty(path):
    """
    Determine whether the specified path represents an empty directory or an empty file.
    """
    path = _get_path(path)
    assert_exists(path)
    if is_dir(path):
        return is_empty_dir(path)
    return is_empty_file(path)


def is_empty_dir(path):
    """
    Determine whether the specified path represents an empty directory.
    """
    path = _get_path(path)
    assert_dir(path)
    return len(os.listdir(path)) == 0


def is_empty_file(path):
    """
    Determine whether the specified path represents an empty file.
    """
    path = _get_path(path)
    return get_file_size(path) == 0


def is_file(path):
    """
    Determine whether the specified path represents an existing file.
    """
    path = _get_path(path)
    return os.path.isfile(path)


def join_filename(basename, extension):
    """
    Create a filename joining the file basename and the extension.
    """
    basename = basename.rstrip(".").strip()
    extension = extension.replace(".", "").strip()
    filename = f"{basename}.{extension}"
    return filename


def join_filepath(dirpath, filename):
    """
    Create a filepath joining the directory path and the filename.
    """
    dirpath = _get_path(dirpath)
    return join_path(dirpath, filename)


def join_path(path, *paths):
    """
    Create a path joining path and paths.
    If path is __file__ (or a .py file), the resulting path will be relative
    to the directory path of the module in which it's used.
    """
    path = _get_path(path)
    basepath = path
    if get_file_extension(path) in ["py", "pyc", "pyo"]:
        basepath = os.path.dirname(os.path.realpath(path))
    paths = [_get_path(path.lstrip(os.sep)) for path in paths]
    return os.path.normpath(os.path.join(basepath, *paths))


def list_dirs(path):
    """
    List all directories contained at the given directory path.
    """
    path = _get_path(path)
    return _filter_paths(path, os.listdir(path), predicate=is_dir)


def list_files(path):
    """
    List all files contained at the given directory path.
    """
    path = _get_path(path)
    return _filter_paths(path, os.listdir(path), predicate=is_file)


def make_dirs(path):
    """
    Create the directories needed to ensure that the given path exists.
    If a file already exists at the given path an OSError is raised.
    """
    path = _get_path(path)
    if is_dir(path):
        return
    assert_not_file(path)
    os.makedirs(path, exist_ok=True)


def make_dirs_for_file(path):
    """
    Create the directories needed to ensure that the given path exists.
    If a directory already exists at the given path an OSError is raised.
    """
    path = _get_path(path)
    if is_file(path):
        return
    assert_not_dir(path)
    dirpath, _ = split_filepath(path)
    make_dirs(dirpath)


def move_dir(path, dest, overwrite=False, **kwargs):
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


def move_file(path, dest, overwrite=False, **kwargs):
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


def read_file(path, encoding="utf-8"):
    """
    Read the content of the file at the given path using the specified encoding.
    """
    path = _get_path(path)
    assert_file(path)
    content = ""
    with open(path, encoding=encoding) as file:
        content = file.read()
    return content


def read_file_from_url(url, **kwargs):
    """
    Read the content of the file at the given url.
    """
    _require_requests_installed()
    response = requests.get(url, **kwargs)
    response.raise_for_status()
    content = response.text
    return content


def read_file_json(
    path,
    cls=None,
    object_hook=None,
    parse_float=None,
    parse_int=None,
    parse_constant=None,
    object_pairs_hook=None,
):
    """
    Read and decode a json encoded file at the given path.
    """
    path = _get_path(path)
    content = read_file(path)
    data = json.loads(
        content,
        cls=cls,
        object_hook=object_hook,
        parse_float=parse_float,
        parse_int=parse_int,
        parse_constant=parse_constant,
        object_pairs_hook=object_pairs_hook,
    )
    return data


def _read_file_lines_in_range(path, line_start=0, line_end=-1, encoding="utf-8"):
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
    path, line_start=0, line_end=-1, strip_white=True, skip_empty=True, encoding="utf-8"
):
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
        lines = _read_file_lines_in_range(
            path, line_start=line_start, line_end=line_end, encoding=encoding
        )
    if strip_white:
        lines = [line.strip() for line in lines]
    if skip_empty:
        lines = [line for line in lines if line]
    if not isinstance(lines, list):
        lines = list(lines)
    return lines


def read_file_lines_count(path):
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


def remove_dir(path, **kwargs):
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


def remove_dir_content(path):
    """
    Removes all directory content (both sub-directories and files).
    """
    path = _get_path(path)
    assert_dir(path)
    remove_dirs(*list_dirs(path))
    remove_files(*list_files(path))


def remove_dirs(*paths):
    """
    Remove multiple directories at the given paths and all their content.
    """
    for path in paths:
        remove_dir(path)


def remove_file(path):
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


def remove_files(*paths):
    """
    Remove multiple files at the given paths.
    """
    for path in paths:
        remove_file(path)


def rename_dir(path, name):
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


def rename_file(path, name):
    """
    Rename a file with the given name.
    If a directory or a file with the given name already exists, an OSError is raised.
    """
    path = _get_path(path)
    assert_file(path)
    dirpath, filename = split_filepath(path)
    dest = join_filepath(dirpath, name)
    assert_not_exists(dest)
    os.rename(path, dest)


def rename_file_basename(path, basename):
    """
    Rename a file basename with the given basename.
    """
    path = _get_path(path)
    extension = get_file_extension(path)
    filename = join_filename(basename, extension)
    rename_file(path, filename)


def rename_file_extension(path, extension):
    """
    Rename a file extension with the given extension.
    """
    path = _get_path(path)
    basename = get_file_basename(path)
    filename = join_filename(basename, extension)
    rename_file(path, filename)


def replace_dir(path, src, autodelete=False):
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


def replace_file(path, src, autodelete=False):
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


def _search_paths(path, pattern):
    """
    Search all paths relative to path matching the given pattern.
    """
    path = _get_path(path)
    assert_dir(path)
    pathname = os.path.join(path, pattern)
    paths = glob.glob(pathname, recursive=True)
    return paths


def search_dirs(path, pattern="**/*"):
    """
    Search for directories at path matching the given pattern.
    """
    path = _get_path(path)
    return _filter_paths(path, _search_paths(path, pattern), predicate=is_dir)


def search_files(path, pattern="**/*.*"):
    """
    Search for files at path matching the given pattern.
    """
    path = _get_path(path)
    return _filter_paths(path, _search_paths(path, pattern), predicate=is_file)


def split_filename(path):
    """
    Split a filename and returns its basename and extension.
    """
    path = _get_path(path)
    filename = get_filename(path)
    basename, extension = os.path.splitext(filename)
    extension = extension.replace(".", "").strip()
    return (basename, extension)


def split_filepath(path):
    """
    Split a filepath and returns its directory-path and filename.
    """
    path = _get_path(path)
    dirpath = os.path.dirname(path)
    filename = get_filename(path)
    return (dirpath, filename)


def split_path(path):
    """
    Split a path and returns its path-names.
    """
    path = _get_path(path)
    head, tail = os.path.split(path)
    names = head.split(os.sep) + [tail]
    names = list(filter(None, names))
    return names


def write_file(path, content, append=False, encoding="utf-8"):
    """
    Write file with the specified content at the given path.
    """
    path = _get_path(path)
    assert_not_dir(path)
    make_dirs_for_file(path)
    mode = "a" if append else "w"
    with open(path, mode, encoding=encoding) as file:
        file.write(content)


def write_file_json(
    path,
    data,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    cls=None,
    indent=None,
    separators=None,
    default=None,
    sort_keys=False,
):
    """
    Write a json file at the given path with the specified data encoded in json format.
    """
    path = _get_path(path)

    def default_encoder(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, set):
            return list(obj)
        return str(obj)

    content = json.dumps(
        data,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        cls=cls,
        indent=indent,
        separators=separators,
        default=default or default_encoder,
        sort_keys=sort_keys,
    )
    write_file(path, content)
