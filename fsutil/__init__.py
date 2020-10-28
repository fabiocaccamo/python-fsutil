# -*- coding: utf-8 -*-

from fsutil.metadata import (
    __author__, __copyright__, __description__,
    __email__, __license__, __title__, __version__, )

import errno
import glob
import hashlib
import os
import shutil
import sys

try:
    # python 2
    from urlparse import urlsplit
except ImportError:
    # python 3
    from urllib.parse import urlsplit


PY2 = bool(sys.version_info.major == 2)


def assert_dir(path):
    """
    Raise an OSError if the given path doesn't exist or it is not a directory.
    """
    if not is_dir(path):
        raise OSError(
            'Invalid directory path: {}'.format(path))


def assert_exists(path):
    """
    Raise an OSError if the given path doesn't exist.
    """
    if not exists(path):
        raise OSError(
            'Invalid item path: {}'.format(path))


def assert_file(path):
    """
    Raise an OSError if the given path doesn't exist or it is not a file.
    """
    if not is_file(path):
        raise OSError(
            'Invalid file path: {}'.format(path))


def assert_not_dir(path):
    """
    Raise an OSError if the given path is an existing directory.
    """
    if is_dir(path):
        raise OSError(
            'Invalid path, directory already exists: {}'.format(path))


def assert_not_exists(path):
    """
    Raise an OSError if the given path already exists.
    """
    if exists(path):
        raise OSError(
            'Invalid path, item already exists: {}'.format(path))


def assert_not_file(path):
    """
    Raise an OSError if the given path is an existing file.
    """
    if is_file(path):
        raise OSError('Invalid path, file already exists: {}'.format(path))


def _clean_dir_empty_dirs(path):
    for root, dirs, _ in os.walk(path, topdown=False):
        for dirname in dirs:
            dirpath = os.path.join(root, dirname)
            print(dirpath)
            if is_empty_dir(dirpath):
                remove_dir(dirpath)


def _clean_dir_empty_files(path):
    for root, _, files in os.walk(path, topdown=False):
        for filename in files:
            filepath = os.path.join(root, filename)
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
        kwargs.setdefault('dirs_exist_ok', True)
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


def create_file(path, content='', overwrite=False):
    """
    Create file with the specified content at the given path.
    If overwrite is not allowed and path exists, an OSError is raised.
    """
    if not overwrite:
        assert_not_exists(path)
    write_file(path, content)


def delete_dir(path):
    """
    Alias for remove_dir.
    """
    return remove_dir(path)


def delete_dirs(*paths):
    """
    Alias for delete_dirs.
    """
    remove_dirs(*paths)


def delete_file(path):
    """
    Alias for delete_file.
    """
    return remove_file(path)


def delete_files(*paths):
    """
    Alias for delete_files.
    """
    remove_files(*paths)


def exists(path):
    """
    Check if a directory of a file exists at the given path.
    """
    return os.path.exists(path)


def _filter_paths(basepath, relpaths, predicate=None):
    """
    Filter paths relative to basepath according to the optional predicate function.
    If predicate is defined, paths are filtered using it, otherwise all paths will be listed.
    """
    paths = []
    for relpath in relpaths:
        abspath = os.path.join(basepath, relpath)
        if predicate is None or predicate(abspath):
            paths.append((relpath, abspath, ))
    paths.sort(key=lambda path: path[0])
    return paths


def get_file_basename(path):
    """
    Get the file basename from the given path/url.
    """
    basename, _ = split_filename(path)
    return basename


def get_file_extension(path):
    """
    Get the file extension from the given path/url.
    """
    _, extension = split_filename(path)
    return extension


def get_filename(path):
    """
    Get the filename from the given path/url.
    """
    filepath = urlsplit(path).path
    filename = os.path.basename(filepath)
    return filename


def get_hash(path, func='md5'):
    """
    Get the hash of the file at the gived path using
    the specified algorithm function (md5 by default).
    """
    # hash = hashlib.md5()
    hash = hashlib.new(func)
    paths = list(path) if isinstance(path, (list, set, tuple, )) else [path]
    paths.sort()
    for path in paths:
        assert_file(path)
        with open(path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                hash.update(chunk)
    hash_hex = hash.hexdigest()
    return hash_hex


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
    assert_file(path)
    return os.stat(path).st_size == 0


def is_file(path):
    """
    Determine whether the specified path represents an existing file.
    """
    return os.path.isfile(path)


def join_filename(basename, extension):
    """
    Create a filename joining the file basename and the extension.
    """
    basename = basename.rstrip('.').strip()
    extension = extension.replace('.', '').strip()
    filename = '{}.{}'.format(basename, extension)
    return filename


def join_filepath(dirpath, filename):
    """
    Create a filepath joining the directory path and the filename.
    """
    filepath = os.path.join(dirpath, filename)
    return filepath


def join_path(path, *paths):
    """
    Create a path joining path and paths.
    If path is __file__ (or a .py file), the resulting path will be relative
    to the directory path of the module in which it's used.
    """
    basepath = path
    if path.endswith('.py'):
        basepath = os.path.dirname(os.path.realpath(path))
    return os.path.abspath(os.path.join(basepath, *paths))


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


def read_file(path, encoding='utf-8'):
    """
    Read the content of the file at the given path using the specified encoding.
    """
    assert_file(path)
    content = ''
    options = {} if PY2 else {'encoding': encoding}
    with open(path, 'r', **options) as file:
        content = file.read()
    return content


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


def search_dirs(path, pattern):
    """
    Search for directories at path matching the given pattern.
    """
    assert_dir(path)
    pathname = os.path.join(path, pattern)
    options = {} if PY2 else { 'recursive':True }
    subpaths = glob.glob(pathname, **options)
    return _filter_paths(path, subpaths, predicate=is_dir)


def search_files(path, pattern):
    """
    Search for files at path matching the given pattern.
    """
    assert_dir(path)
    pathname = os.path.join(path, pattern)
    options = {} if PY2 else { 'recursive':True }
    subpaths = glob.glob(pathname, **options)
    return _filter_paths(path, subpaths, predicate=is_file)


def split_filename(path):
    """
    Split a filename and returns its basename and extension.
    """
    filename = get_filename(path)
    basename, extension = os.path.splitext(filename)
    extension = extension.replace('.', '').strip()
    return (basename, extension, )


def split_filepath(path):
    """
    Split a filename and returns its directory-path and filename.
    """
    dirpath = os.path.dirname(path)
    filename = get_filename(path)
    return (dirpath, filename, )


def write_file(path, content, append=False, encoding='utf-8'):
    """
    Write file with the specified content at the given path.
    """
    make_dirs_for_file(path)
    mode = 'a' if append else 'w'
    options = {} if PY2 else {'encoding': encoding}
    with open(path, mode, **options) as file:
        file.write(content)
