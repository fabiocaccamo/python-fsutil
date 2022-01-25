# -*- coding: utf-8 -*-

from fsutil.metadata import (
    __author__,
    __copyright__,
    __description__,
    __email__,
    __license__,
    __title__,
    __version__,
)

import datetime as dt
import errno
import glob
import hashlib
import json
import os

try:
    import requests

    requests_installed = True
except ImportError:
    requests_installed = False

import shutil
import sys
import zipfile

try:
    # python 2
    from urlparse import urlsplit
except ImportError:
    # python 3
    from urllib.parse import urlsplit


PY2 = bool(sys.version_info.major == 2)
SIZE_UNITS = ["bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]


def _require_requests_installed():
    if not requests_installed:
        raise ModuleNotFoundError(
            "'requests' module is not installed, "
            "it can be installed by running: 'pip install requests'"
        )


def assert_dir(path):
    """
    Raise an OSError if the given path doesn't exist or it is not a directory.
    """
    if not is_dir(path):
        raise OSError("Invalid directory path: {}".format(path))


def assert_exists(path):
    """
    Raise an OSError if the given path doesn't exist.
    """
    if not exists(path):
        raise OSError("Invalid item path: {}".format(path))


def assert_file(path):
    """
    Raise an OSError if the given path doesn't exist or it is not a file.
    """
    if not is_file(path):
        raise OSError("Invalid file path: {}".format(path))


def assert_not_dir(path):
    """
    Raise an OSError if the given path is an existing directory.
    """
    if is_dir(path):
        raise OSError("Invalid path, directory already exists: {}".format(path))


def assert_not_exists(path):
    """
    Raise an OSError if the given path already exists.
    """
    if exists(path):
        raise OSError("Invalid path, item already exists: {}".format(path))


def assert_not_file(path):
    """
    Raise an OSError if the given path is an existing file.
    """
    if is_file(path):
        raise OSError("Invalid path, file already exists: {}".format(path))


def _clean_dir_empty_dirs(path):
    for basepath, dirnames, _ in os.walk(path, topdown=False):
        for dirname in dirnames:
            dirpath = os.path.join(basepath, dirname)
            if is_empty_dir(dirpath):
                remove_dir(dirpath)


def _clean_dir_empty_files(path):
    for basepath, _, filenames in os.walk(path, topdown=False):
        for filename in filenames:
            filepath = os.path.join(basepath, filename)
            if is_empty_file(filepath):
                remove_file(filepath)


def clean_dir(path, dirs=True, files=True):
    """
    Clean a directory by removing empty directories and/or empty files.
    """
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
    s_format = "{:.2f} {}" if (factor > 1) else "{:.0f} {}"
    s = s_format.format(size, units[factor])
    return s


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
    return int((1024 ** factor) * amount)


def copy_dir(path, dest, overwrite=False, **kwargs):
    """
    Copy the directory at the given path and all its content to dest path.
    If overwrite is not allowed and dest path exists, an OSError is raised.
    More informations about kwargs supported options here:
    https://docs.python.org/3/library/shutil.html#shutil.copytree
    """
    assert_not_file(path)
    dirname = os.path.basename(os.path.normpath(path))
    dest = os.path.join(dest, dirname)
    if not overwrite:
        assert_not_exists(dest)
    else:
        # only if python < 3.8
        if not (sys.version_info.major >= 3 and sys.version_info.minor >= 8):
            if is_dir(dest):
                remove_dir(dest)
    copy_dir_content(path, dest, **kwargs)


def copy_dir_content(path, dest, **kwargs):
    """
    Copy the content of the directory at the given path to dest path.
    More informations about kwargs supported options here:
    https://docs.python.org/3/library/shutil.html#shutil.copytree
    """
    assert_dir(path)
    # only if python >= 3.8
    if sys.version_info.major >= 3 and sys.version_info.minor >= 8:
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
    assert_file(path)
    if not overwrite:
        assert_not_exists(dest)
    make_dirs_for_file(dest)
    shutil.copy2(path, dest, **kwargs)


def create_dir(path, overwrite=False):
    """
    Create directory at the given path.
    If overwrite is not allowed and path exists, an OSError is raised.
    """
    if not overwrite:
        assert_not_exists(path)
    make_dirs(path)


def create_file(path, content="", overwrite=False):
    """
    Create file with the specified content at the given path.
    If overwrite is not allowed and path exists, an OSError is raised.
    """
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
    assert_not_dir(path)
    if not overwrite:
        assert_not_exists(path)
    make_dirs_for_file(path)

    def _write_content_to_zip_file(file, path, basedir=""):
        assert_exists(path)
        if is_file(path):
            filename = get_filename(path)
            filepath = join_path(basedir, filename)
            file.write(path, filepath)
        elif is_dir(path):
            for item_name in os.listdir(path):
                item_path = join_path(path, item_name)
                if is_dir(item_path):
                    basedir = join_path(basedir, item_name)
                _write_content_to_zip_file(file, item_path, basedir)

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


def download_file(url, dirpath, filename=None, chunk_size=8192, **kwargs):
    """
    Download a file from url to dirpath.
    If filename is provided, the file will be named using filename.
    It is possible to pass extra request options (eg. for authentication) using **kwargs.
    """
    _require_requests_installed()
    # https://stackoverflow.com/a/16696317/2096218
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
    return os.path.exists(path)


def extract_zip_file(path, dest, autodelete=False, content_paths=None):
    """
    Extract zip file at path to dest path.
    If autodelete, the archive will be deleted after extraction.
    If content_paths list is defined, only listed items will be extracted, otherwise all.
    """
    assert_file(path)
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
    assert_dir(path)
    creation_timestamp = os.path.getctime(path)
    creation_date = dt.datetime.fromtimestamp(creation_timestamp)
    return creation_date


def get_dir_creation_date_formatted(path, format="%Y-%m-%d %H:%M:%S"):
    """
    Get the directory creation date formatted using the given format.
    """
    date = get_dir_creation_date(path)
    return date.strftime(format)


def get_dir_last_modified_date(path):
    """
    Get the directory last modification date.
    """
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
    last_modified_date = dt.datetime.fromtimestamp(last_modified_timestamp)
    return last_modified_date


def get_dir_last_modified_date_formatted(path, format="%Y-%m-%d %H:%M:%S"):
    """
    Get the directory last modification date formatted using the given format.
    """
    date = get_dir_last_modified_date(path)
    return date.strftime(format)


def get_dir_size(path):
    """
    Get the directory size in bytes.
    """
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
    basename, _ = split_filename(path)
    return basename


def get_file_creation_date(path):
    """
    Get the file creation date.
    """
    assert_file(path)
    creation_timestamp = os.path.getctime(path)
    creation_date = dt.datetime.fromtimestamp(creation_timestamp)
    return creation_date


def get_file_creation_date_formatted(path, format="%Y-%m-%d %H:%M:%S"):
    """
    Get the file creation date formatted using the given format.
    """
    date = get_file_creation_date(path)
    return date.strftime(format)


def get_file_extension(path):
    """
    Get the file extension from the given path/url.
    """
    _, extension = split_filename(path)
    return extension


def get_file_hash(path, func="md5"):
    """
    Get the hash of the file at the gived path using
    the specified algorithm function (md5 by default).
    """
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
    assert_file(path)
    last_modified_timestamp = os.path.getmtime(path)
    last_modified_date = dt.datetime.fromtimestamp(last_modified_timestamp)
    return last_modified_date


def get_file_last_modified_date_formatted(path, format="%Y-%m-%d %H:%M:%S"):
    """
    Get the file last modification date formatted using the given format.
    """
    date = get_file_last_modified_date(path)
    return date.strftime(format)


def get_file_size(path):
    """
    Get the directory size in bytes.
    """
    assert_file(path)
    # size = os.stat(path).st_size
    size = os.path.getsize(path)
    return size


def get_file_size_formatted(path):
    """
    Get the directory size formatted using the right unit suffix.
    """
    size = get_file_size(path)
    size_formatted = convert_size_bytes_to_string(size)
    return size_formatted


def get_filename(path):
    """
    Get the filename from the given path/url.
    """
    filepath = urlsplit(path).path
    filename = os.path.basename(filepath)
    return filename


def get_parent_dir(path, levels=1):
    """
    Get the parent directory for the given path going up N levels.
    """
    return join_path(path, *([os.pardir] * max(1, levels)))


def is_dir(path):
    """
    Determine whether the specified path represents an existing directory.
    """
    return os.path.isdir(path)


def is_empty(path):
    """
    Determine whether the specified path represents an empty directory or an empty file.
    """
    assert_exists(path)
    if is_dir(path):
        return is_empty_dir(path)
    return is_empty_file(path)


def is_empty_dir(path):
    """
    Determine whether the specified path represents an empty directory.
    """
    assert_dir(path)
    return len(os.listdir(path)) == 0


def is_empty_file(path):
    """
    Determine whether the specified path represents an empty file.
    """
    return get_file_size(path) == 0


def is_file(path):
    """
    Determine whether the specified path represents an existing file.
    """
    return os.path.isfile(path)


def join_filename(basename, extension):
    """
    Create a filename joining the file basename and the extension.
    """
    basename = basename.rstrip(".").strip()
    extension = extension.replace(".", "").strip()
    filename = "{}.{}".format(basename, extension)
    return filename


def join_filepath(dirpath, filename):
    """
    Create a filepath joining the directory path and the filename.
    """
    return join_path(dirpath, filename)


def join_path(path, *paths):
    """
    Create a path joining path and paths.
    If path is __file__ (or a .py file), the resulting path will be relative
    to the directory path of the module in which it's used.
    """
    basepath = path
    if get_file_extension(path) in ["py", "pyc", "pyo"]:
        basepath = os.path.dirname(os.path.realpath(path))
    paths = [path.lstrip(os.sep) for path in paths]
    return os.path.normpath(os.path.join(basepath, *paths))


def list_dirs(path):
    """
    List all directories contained at the given directory path.
    """
    return _filter_paths(path, os.listdir(path), predicate=is_dir)


def list_files(path):
    """
    List all files contained at the given directory path.
    """
    return _filter_paths(path, os.listdir(path), predicate=is_file)


def _make_dirs_py2(path):
    # https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
    try:
        os.makedirs(path)
    except OSError as e:
        # Guard against race condition
        if e.errno != errno.EEXIST:
            raise e


def make_dirs(path):
    """
    Create the directories needed to ensure that the given path exists.
    If a file already exists at the given path an OSError is raised.
    """
    if is_dir(path):
        return
    assert_not_file(path)
    if PY2:
        _make_dirs_py2(path)
        return
    os.makedirs(path, exist_ok=True)


def make_dirs_for_file(path):
    """
    Create the directories needed to ensure that the given path exists.
    If a directory already exists at the given path an OSError is raised.
    """
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
    assert_file(path)
    content = ""
    options = {} if PY2 else {"encoding": encoding}
    with open(path, "r", **options) as file:
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


def read_file_lines(path, strip_white=True, skip_empty=True, encoding="utf-8"):
    """
    Read file content lines according to the given options.
    """
    content = read_file(path, encoding)
    lines = content.splitlines()
    if strip_white:
        lines = [line.strip() for line in lines]
    if skip_empty:
        lines = [line for line in lines if line]
    return lines


def remove_dir(path, **kwargs):
    """
    Remove a directory at the given path and all its content.
    If the directory is removed with success returns True, otherwise False.
    More informations about kwargs supported options here:
    https://docs.python.org/3/library/shutil.html#shutil.rmtree
    """
    if not exists(path):
        return False
    assert_dir(path)
    shutil.rmtree(path, **kwargs)
    return not exists(path)


def remove_dir_content(path):
    """
    Removes all directory content (both sub-directories and files).
    """
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
    assert_file(path)
    dirpath, filename = split_filepath(path)
    dest = join_filepath(dirpath, name)
    assert_not_exists(dest)
    os.rename(path, dest)


def rename_file_basename(path, basename):
    """
    Rename a file basename with the given basename.
    """
    extension = get_file_extension(path)
    filename = join_filename(basename, extension)
    rename_file(path, filename)


def rename_file_extension(path, extension):
    """
    Rename a file extension with the given extension.
    """
    basename = get_file_basename(path)
    filename = join_filename(basename, extension)
    rename_file(path, filename)


def _search_paths(path, pattern):
    """
    Search all paths relative to path matching the given pattern.
    """
    assert_dir(path)
    pathname = os.path.join(path, pattern)
    options = {} if PY2 else {"recursive": True}
    paths = glob.glob(pathname, **options)
    return paths


def search_dirs(path, pattern):
    """
    Search for directories at path matching the given pattern.
    """
    return _filter_paths(path, _search_paths(path, pattern), predicate=is_dir)


def search_files(path, pattern):
    """
    Search for files at path matching the given pattern.
    """
    return _filter_paths(path, _search_paths(path, pattern), predicate=is_file)


def split_filename(path):
    """
    Split a filename and returns its basename and extension.
    """
    filename = get_filename(path)
    basename, extension = os.path.splitext(filename)
    extension = extension.replace(".", "").strip()
    return (basename, extension)


def split_filepath(path):
    """
    Split a filepath and returns its directory-path and filename.
    """
    dirpath = os.path.dirname(path)
    filename = get_filename(path)
    return (dirpath, filename)


def split_path(path):
    """
    Split a path and returns its path-names.
    """
    head, tail = os.path.split(path)
    names = head.split(os.sep) + [tail]
    names = list(filter(None, names))
    return names


def write_file(path, content, append=False, encoding="utf-8"):
    """
    Write file with the specified content at the given path.
    """
    make_dirs_for_file(path)
    mode = "a" if append else "w"
    options = {} if PY2 else {"encoding": encoding}
    with open(path, mode, **options) as file:
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
    content = json.dumps(
        data,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        cls=cls,
        indent=indent,
        separators=separators,
        default=default,
        sort_keys=sort_keys,
    )
    write_file(path, content)
