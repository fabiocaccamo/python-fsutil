[![](https://img.shields.io/pypi/pyversions/python-fsutil.svg?color=blue&logo=python&logoColor=white)](https://www.python.org/)
[![](https://img.shields.io/pypi/v/python-fsutil.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/python-fsutil/)
[![](https://pepy.tech/badge/python-fsutil)](https://pepy.tech/project/python-fsutil)
[![](https://img.shields.io/github/stars/fabiocaccamo/python-fsutil?logo=github)](https://github.com/fabiocaccamo/python-fsutil/)
[![](https://badges.pufler.dev/visits/fabiocaccamo/python-fsutil?label=visitors&color=blue)](https://badges.pufler.dev)
[![](https://img.shields.io/pypi/l/python-fsutil.svg?color=blue)](https://github.com/fabiocaccamo/python-fsutil/blob/master/LICENSE.txt)

[![](https://img.shields.io/travis/fabiocaccamo/python-fsutil?logo=travis&label=build)](https://travis-ci.org/fabiocaccamo/python-fsutil)
[![](https://img.shields.io/circleci/build/gh/fabiocaccamo/python-fsutil?logo=circleci&label=build)](https://circleci.com/gh/fabiocaccamo/python-fsutil)
[![](https://img.shields.io/codecov/c/gh/fabiocaccamo/python-fsutil?logo=codecov)](https://codecov.io/gh/fabiocaccamo/python-fsutil)
[![](https://img.shields.io/codacy/grade/fc40788ae7d74d1fb34a38934113c4e5?logo=codacy)](https://www.codacy.com/app/fabiocaccamo/python-fsutil)
[![](https://img.shields.io/codeclimate/maintainability/fabiocaccamo/python-fsutil?logo=code-climate)](https://codeclimate.com/github/fabiocaccamo/python-fsutil/)
[![](https://requires.io/github/fabiocaccamo/python-fsutil/requirements.svg?branch=master)](https://requires.io/github/fabiocaccamo/python-fsutil/requirements/?branch=master)

# python-fsutil
file-system utilities for lazy devs.

## Features
-   Simple and intuitive.
-   Zero dependencies.
-   Compatibile with python 2 and 3.
-   Well tested.

## Index
-   [Installation](#installation)
-   [Usage](#usage)
-   [Testing](#testing)
-   [License](#license)

## Installation

```bash
pip install python-fsutil
```

## Usage

Just import the main module and call its methods.

```python
import fsutil
```

### Methods

-   [`assert_dir`](#assert_dir)
-   [`assert_exists`](#assert_exists)
-   [`assert_file`](#assert_file)
-   [`assert_not_dir`](#assert_not_dir)
-   [`assert_not_exists`](#assert_not_exists)
-   [`assert_not_file`](#assert_not_file)
-   [`clean_dir`](#clean_dir)
-   [`convert_size_bytes_to_string`](#convert_size_bytes_to_string)
-   [`convert_size_string_to_bytes`](#convert_size_string_to_bytes)
-   [`copy_dir`](#copy_dir)
-   [`copy_dir_content`](#copy_dir_content)
-   [`copy_file`](#copy_file)
-   [`create_dir`](#create_dir)
-   [`create_file`](#create_file)
-   [`delete_dir`](#delete_dir)
-   [`delete_dirs`](#delete_dirs)
-   [`delete_file`](#delete_file)
-   [`delete_files`](#delete_files)
-   [`exists`](#exists)
-   [`get_dir_size`](#get_dir_size)
-   [`get_dir_size_formatted`](#get_dir_size_formatted)
-   [`get_file_basename`](#get_file_basename)
-   [`get_file_extension`](#get_file_extension)
-   [`get_file_hash`](#get_file_hash)
-   [`get_file_size`](#get_file_size)
-   [`get_file_size_formatted`](#get_file_size_formatted)
-   [`get_filename`](#get_filename)
-   [`is_dir`](#is_dir)
-   [`is_empty`](#is_empty)
-   [`is_empty_dir`](#is_empty_dir)
-   [`is_empty_file`](#is_empty_file)
-   [`is_file`](#is_file)
-   [`join_filename`](#join_filename)
-   [`join_filepath`](#join_filepath)
-   [`join_path`](#join_path)
-   [`list_dirs`](#list_dirs)
-   [`list_files`](#list_files)
-   [`make_dirs`](#make_dirs)
-   [`make_dirs_for_file`](#make_dirs_for_file)
-   [`move_dir`](#move_dir)
-   [`move_file`](#move_file)
-   [`read_file`](#read_file)
-   [`remove_dir`](#remove_dir)
-   [`remove_dirs`](#remove_dirs)
-   [`remove_file`](#remove_file)
-   [`remove_files`](#remove_files)
-   [`rename_dir`](#rename_dir)
-   [`rename_file`](#rename_file)
-   [`rename_file_basename`](#rename_file_basename)
-   [`rename_file_extension`](#rename_file_extension)
-   [`search_dirs`](#search_dirs)
-   [`search_files`](#search_files)
-   [`split_filename`](#split_filename)
-   [`split_filepath`](#split_filepath)
-   [`split_path`](#split_path)
-   [`write_file`](#write_file)


#### `assert_dir`

```python
# Raise an OSError if the given path doesn't exist or it is not a directory.
fsutil.assert_dir(path)
```

#### `assert_exists`

```python
# Raise an OSError if the given path doesn't exist.
fsutil.assert_exists(path)
```

#### `assert_file`

```python
# Raise an OSError if the given path doesn't exist or it is not a file.
fsutil.assert_file(path)
```

#### `assert_not_dir`

```python
# Raise an OSError if the given path is an existing directory.
fsutil.assert_not_dir(path)
```

#### `assert_not_exists`

```python
# Raise an OSError if the given path already exists.
fsutil.assert_not_exists(path)
```

#### `assert_not_file`

```python
# Raise an OSError if the given path is an existing file.
fsutil.assert_not_file(path)
```

#### `clean_dir`

```python
# Clean a directory by removing empty sub-directories and/or empty files.
fsutil.clean_dir(path, dirs=True, files=True)
```

#### `convert_size_bytes_to_string`

```python
# Convert the given size bytes to string using the right unit suffix.
size_str = fsutil.convert_size_bytes_to_string(size)
```

#### `convert_size_string_to_bytes`

```python
# Convert the given size string to bytes.
size_bytes = fsutil.convert_size_string_to_bytes(size)
```

#### `copy_dir`

```python
# Copy the directory at the given path and all its content to dest path.
# If overwrite is not allowed and dest path exists, an OSError is raised.
# More informations about kwargs supported options here:
# https://docs.python.org/3/library/shutil.html#shutil.copytree
fsutil.copy_dir(path, dest, overwrite=False, **kwargs)
```

#### `copy_dir_content`

```python
# Copy the content of the directory at the given path to dest path.
# More informations about kwargs supported options here:
# https://docs.python.org/3/library/shutil.html#shutil.copytree
fsutil.copy_dir_content(path, dest, **kwargs)
```

#### `copy_file`

```python
# Copy the file at the given path and its metadata to dest path.
# If overwrite is not allowed and dest path exists, an OSError is raised.
# More informations about kwargs supported options here:
# https://docs.python.org/3/library/shutil.html#shutil.copy2
fsutil.copy_file(path, dest, overwrite=False, **kwargs)
```

#### `create_dir`

```python
# Create directory at the given path.
# If overwrite is not allowed and path exists, an OSError is raised.
fsutil.create_dir(path, overwrite=False)
```

#### `create_file`

```python
# Create file with the specified content at the given path.
# If overwrite is not allowed and path exists, an OSError is raised.
fsutil.create_file(path, content='', overwrite=False)
```

#### `delete_dir`

```python
# Alias for remove_dir.
fsutil.delete_dir(path)
```

#### `delete_dirs`

```python
# Alias for delete_dirs.
fsutil.delete_dirs(*paths)
```

#### `delete_file`

```python
# Alias for delete_file.
fsutil.delete_file(path)
```

#### `delete_files`

```python
# Alias for delete_files.
fsutil.delete_files(*paths)
```

#### `exists`

```python
# Check if a directory of a file exists at the given path.
value = fsutil.exists(path)
```

#### `get_dir_size`

```python
# Get the directory size in bytes.
size = fsutil.get_dir_size(path)
```

#### `get_dir_size_formatted`

```python
# Get the directory size formatted using the right unit suffix.
size_str = fsutil.get_dir_size_formatted(path)
```

#### `get_file_basename`

```python
# Get the file basename from the given path/url.
basename = fsutil.get_file_basename(path)
```

#### `get_file_extension`

```python
# Get the file extension from the given path/url.
extension = fsutil.get_file_extension(path)
```

#### `get_file_hash`

```python
# Get the hash of the file at the given path using
# the specified algorithm function (md5 by default).
filehash = fsutil.get_file_hash(path, func='md5')
```

#### `get_file_size`

```python
# Get the file size in bytes.
size = fsutil.get_file_size(path)
```

#### `get_file_size_formatted`

```python
# Get the file size formatted using the right unit suffix.
size_str = fsutil.get_file_size_formatted(path)
```

#### `get_filename`

```python
# Get the filename from the given path/url.
filename = fsutil.get_filename(path)
```

#### `is_dir`

```python
# Determine whether the specified path represents an existing directory.
value = fsutil.is_dir(path)
```

#### `is_empty`

```python
# Determine whether the specified path represents an empty directory or an empty file.
value = fsutil.is_empty(path)
```

#### `is_empty_dir`

```python
# Determine whether the specified path represents an empty directory.
value = fsutil.is_empty_dir(path)
```

#### `is_empty_file`

```python
# Determine whether the specified path represents an empty file.
value = fsutil.is_empty_file(path)
```

#### `is_file`

```python
# Determine whether the specified path represents an existing file.
value = fsutil.is_file(path)
```

#### `join_filename`

```python
# Create a filename joining the file basename and the extension.
filename = fsutil.join_filename(basename, extension)
```

#### `join_filepath`

```python
# Create a filepath joining the directory path and the filename.
filepath = fsutil.join_filepath(dirpath, filename)
```

#### `join_path`

```python
# Create a path joining path and paths.
# If path is __file__ (or a .py file), the resulting path will be relative
# to the directory path of the module in which it's used.
path = fsutil.get_path(basefile, path)
```

#### `list_dirs`

```python
# List all directories contained at the given directory path.
dirs = fsutil.list_dirs(path)
```

#### `list_files`

```python
# List all files contained at the given directory path.
files = fsutil.list_files(path)
```

#### `make_dirs`

```python
# Create the directories needed to ensure that the given path exists.
# If a file already exists at the given path an OSError is raised.
fsutil.make_dirs(path)
```

#### `make_dirs_for_file`

```python
# Create the directories needed to ensure that the given path exists.
# If a directory already exists at the given path an OSError is raised.
fsutil.make_dirs_for_file(path)
```

#### `move_dir`

```python
# Move an existing dir from path to dest directory.
# If overwrite is not allowed and dest path exists, an OSError is raised.
# More informations about kwargs supported options here:
# https://docs.python.org/3/library/shutil.html#shutil.move
fsutil.move_dir(path, dest, overwrite=False, **kwargs)
```

#### `move_file`

```python
# Move an existing file from path to dest directory.
# If overwrite is not allowed and dest path exists, an OSError is raised.
# More informations about kwargs supported options here:
# https://docs.python.org/3/library/shutil.html#shutil.move
fsutil.move_file(path, dest, overwrite=False, **kwargs)
```

#### `read_file`

```python
# Read the content of the file at the given path using the specified encoding.
content = fsutil.read_file(path, encoding='utf-8')
```

#### `remove_dir`

```python
# Remove a directory at the given path and all its content.
# If the directory is removed with success returns True, otherwise False.
# More informations about kwargs supported options here:
# https://docs.python.org/3/library/shutil.html#shutil.rmtree
fsutil.remove_dir(path, **kwargs)
```

#### `remove_dirs`

```python
# Remove multiple directories at the given paths and all their content.
fsutil.remove_dirs(*paths)
```

#### `remove_file`

```python
# Remove a file at the given path.
# If the file is removed with success returns True, otherwise False.
fsutil.remove_file(path)
```

#### `remove_files`

```python
# Remove multiple files at the given paths.
fsutil.remove_files(*paths)
```

#### `rename_dir`

```python
# Rename a directory with the given name.
# If a directory or a file with the given name already exists, an OSError is raised.
fsutil.rename_dir(path, name)
```

#### `rename_file`

```python
# Rename a file with the given name.
# If a directory or a file with the given name already exists, an OSError is raised.
fsutil.rename_file(path, name)
```

#### `rename_file_basename`

```python
# Rename a file basename with the given basename.
fsutil.rename_file_basename(path, basename)
```

#### `rename_file_extension`

```python
# Rename a file extension with the given extension.
fsutil.rename_file_extension(path, extension)
```

#### `search_dirs`

```python
# Search for directories at path matching the given pattern.
dirs = fsutil.search_dirs(path, pattern)
```

#### `search_files`

```python
# Search for files at path matching the given pattern.
files = fsutil.search_files(path, pattern)
```

#### `split_filename`

```python
# Split a filename and returns its basename and extension.
basename, extension = fsutil.split_filename(path)
```

#### `split_filepath`

```python
# Split a filename and returns its directory-path and filename.
dirpath, filename = fsutil.split_filepath(path)
```

#### `split_path`

```python
# Split a path and returns its path-names.
path_names = fsutil.split_path(path)
```

#### `write_file`

```python
# Write file with the specified content at the given path.
fsutil.write_file(path, content, append=False, encoding='utf-8')
```

## Testing
```bash
# create python virtual environment
virtualenv testing_fsutil

# activate virtualenv
cd testing_fsutil && . bin/activate

# clone repo
git clone https://github.com/fabiocaccamo/python-fsutil.git src && cd src

# install requirements
pip install --upgrade pip
pip install -r requirements.txt

# run tests using tox
tox

# or run tests using unittest
python -m unittest

# or run tests using setuptools
python setup.py test
```

## License
Released under [MIT License](LICENSE.txt).
