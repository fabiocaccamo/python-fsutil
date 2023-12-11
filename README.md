[![](https://img.shields.io/pypi/pyversions/python-fsutil.svg?color=blue&logo=python&logoColor=white)](https://www.python.org/)
[![](https://img.shields.io/pypi/v/python-fsutil.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/python-fsutil/)
[![](https://static.pepy.tech/badge/python-fsutil/month)](https://pepy.tech/project/python-fsutil)
[![](https://img.shields.io/github/stars/fabiocaccamo/python-fsutil?logo=github)](https://github.com/fabiocaccamo/python-fsutil/stargazers)
[![](https://img.shields.io/pypi/l/python-fsutil.svg?color=blue)](https://github.com/fabiocaccamo/python-fsutil/blob/main/LICENSE.txt)

[![](https://results.pre-commit.ci/badge/github/fabiocaccamo/python-fsutil/main.svg)](https://results.pre-commit.ci/latest/github/fabiocaccamo/python-fsutil/main)
[![](https://img.shields.io/github/actions/workflow/status/fabiocaccamo/python-fsutil/test-package.yml?branch=main&label=build&logo=github)](https://github.com/fabiocaccamo/python-fsutil)
[![](https://img.shields.io/codecov/c/gh/fabiocaccamo/python-fsutil?logo=codecov)](https://codecov.io/gh/fabiocaccamo/python-fsutil)
[![](https://img.shields.io/codacy/grade/fc40788ae7d74d1fb34a38934113c4e5?logo=codacy)](https://www.codacy.com/app/fabiocaccamo/python-fsutil)
[![](https://img.shields.io/codeclimate/maintainability/fabiocaccamo/python-fsutil?logo=code-climate)](https://codeclimate.com/github/fabiocaccamo/python-fsutil/)
[![](https://img.shields.io/badge/code%20style-black-000000.svg?logo=python&logoColor=black)](https://github.com/psf/black)
[![](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# python-fsutil
high-level file-system operations for lazy devs.

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
-   [`create_tar_file`](#create_tar_file)
-   [`create_zip_file`](#create_zip_file)
-   [`delete_dir`](#delete_dir)
-   [`delete_dir_content`](#delete_dir_content)
-   [`delete_dirs`](#delete_dirs)
-   [`delete_file`](#delete_file)
-   [`delete_files`](#delete_files)
-   [`download_file`](#download_file) *(require `requests` to be installed)*
-   [`exists`](#exists)
-   [`extract_tar_file`](#extract_tar_file)
-   [`extract_zip_file`](#extract_zip_file)
-   [`get_dir_creation_date`](#get_dir_creation_date)
-   [`get_dir_creation_date_formatted`](#get_dir_creation_date_formatted)
-   [`get_dir_hash`](#get_dir_hash)
-   [`get_dir_last_modified_date`](#get_dir_last_modified_date)
-   [`get_dir_last_modified_date_formatted`](#get_dir_last_modified_date_formatted)
-   [`get_dir_size`](#get_dir_size)
-   [`get_dir_size_formatted`](#get_dir_size_formatted)
-   [`get_file_basename`](#get_file_basename)
-   [`get_file_creation_date`](#get_file_creation_date)
-   [`get_file_creation_date_formatted`](#get_file_creation_date_formatted)
-   [`get_file_extension`](#get_file_extension)
-   [`get_file_hash`](#get_file_hash)
-   [`get_file_last_modified_date`](#get_file_last_modified_date)
-   [`get_file_last_modified_date_formatted`](#get_file_last_modified_date_formatted)
-   [`get_file_size`](#get_file_size)
-   [`get_file_size_formatted`](#get_file_size_formatted)
-   [`get_filename`](#get_filename)
-   [`get_parent_dir`](#get_parent_dir)
-   [`get_unique_name`](#get_unique_name)
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
-   [`read_file_from_url`](#read_file_from_url) *(requires `requests` to be installed)*
-   [`read_file_json`](#read_file_json)
-   [`read_file_lines`](#read_file_lines)
-   [`read_file_lines_count`](#read_file_lines_count)
-   [`remove_dir`](#remove_dir)
-   [`remove_dir_content`](#remove_dir_content)
-   [`remove_dirs`](#remove_dirs)
-   [`remove_file`](#remove_file)
-   [`remove_files`](#remove_files)
-   [`rename_dir`](#rename_dir)
-   [`rename_file`](#rename_file)
-   [`rename_file_basename`](#rename_file_basename)
-   [`rename_file_extension`](#rename_file_extension)
-   [`replace_dir`](#replace_dir)
-   [`replace_file`](#replace_file)
-   [`search_dirs`](#search_dirs)
-   [`search_files`](#search_files)
-   [`split_filename`](#split_filename)
-   [`split_filepath`](#split_filepath)
-   [`split_path`](#split_path)
-   [`write_file`](#write_file)
-   [`write_file_json`](#write_file_json)


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
fsutil.create_file(path, content="", overwrite=False)
```

#### `create_tar_file`

```python
# Create tar file at path compressing directories/files listed in content_paths.
# If overwrite is allowed and dest tar already exists, it will be overwritten.
fsutil.create_tar_file(path, content_paths, overwrite=True, compression="gzip")
```

#### `create_zip_file`

```python
# Create zip file at path compressing directories/files listed in content_paths.
# If overwrite is allowed and dest zip already exists, it will be overwritten.
fsutil.create_zip_file(path, content_paths, overwrite=True, compression=zipfile.ZIP_DEFLATED)
```

#### `delete_dir`

```python
# Alias for remove_dir.
fsutil.delete_dir(path)
```

#### `delete_dir_content`

```python
# Alias for remove_dir_content.
fsutil.delete_dir_content(path)
```

#### `delete_dirs`

```python
# Alias for remove_dirs.
fsutil.delete_dirs(*paths)
```

#### `delete_file`

```python
# Alias for remove_file.
fsutil.delete_file(path)
```

#### `delete_files`

```python
# Alias for remove_files.
fsutil.delete_files(*paths)
```

#### `download_file`

```python
# Download a file from url to the given dirpath and return the filepath.
# If dirpath is not provided, the file will be downloaded to a temp directory.
# If filename is provided, the file will be named using filename.
# It is possible to pass extra request options (eg. for authentication) using **kwargs.
filepath = fsutil.download_file(url, dirpath=None, filename="archive.zip", chunk_size=8192, **kwargs)
```

#### `exists`

```python
# Check if a directory of a file exists at the given path.
value = fsutil.exists(path)
```

#### `extract_tar_file`

```python
# Extract tar file at path to dest path.
# If autodelete, the archive will be deleted after extraction.
# If content_paths list is defined, only listed items will be extracted, otherwise all.
fsutil.extract_tar_file(path, dest, content_paths=None, autodelete=False)
```

#### `extract_zip_file`

```python
# Extract zip file at path to dest path.
# If autodelete, the archive will be deleted after extraction.
# If content_paths list is defined, only listed items will be extracted, otherwise all.
fsutil.extract_zip_file(path, dest, content_paths=None, autodelete=False)
```

#### `get_dir_creation_date`

```python
# Get the directory creation date.
date = fsutil.get_dir_creation_date(path)
```

#### `get_dir_creation_date_formatted`

```python
# Get the directory creation date formatted using the given format.
date_str = fsutil.get_dir_creation_date_formatted(path, format='%Y-%m-%d %H:%M:%S')
```

#### `get_dir_hash`

```python
# Get the hash of the directory at the given path using
# the specified algorithm function (md5 by default).
hash = fsutil.get_dir_hash(path, func="md5")
```

#### `get_dir_last_modified_date`

```python
# Get the directory last modification date.
date = fsutil.get_dir_last_modified_date(path)
```

#### `get_dir_last_modified_date_formatted`

```python
# Get the directory last modification date formatted using the given format.
date_str = fsutil.get_dir_last_modified_date_formatted(path, format="%Y-%m-%d %H:%M:%S")
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

#### `get_file_creation_date`

```python
# Get the file creation date.
date = fsutil.get_file_creation_date(path)
```

#### `get_file_creation_date_formatted`

```python
# Get the file creation date formatted using the given format.
date_str = fsutil.get_file_creation_date_formatted(path, format="%Y-%m-%d %H:%M:%S")
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
filehash = fsutil.get_file_hash(path, func="md5")
```

#### `get_file_last_modified_date`

```python
# Get the file last modification date.
date = fsutil.get_file_last_modified_date(path)
```

#### `get_file_last_modified_date_formatted`

```python
# Get the file last modification date formatted using the given format.
date_str = fsutil.get_file_last_modified_date_formatted(path, format="%Y-%m-%d %H:%M:%S")
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

#### `get_parent_dir`

```python
# Get the parent directory for the given path going up N levels.
parent_dir = fsutil.get_parent_dir(path, levels=1)
```

#### `get_unique_name`

```python
# Gets a unique name for a directory/file ath the given directory path.
unique_name = fsutil.get_unique_name(path, prefix="", suffix="", extension="", separator="-")
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
path = fsutil.join_path(path, *paths)
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
content = fsutil.read_file(path, encoding="utf-8")
```

#### `read_file_from_url`

```python
# Read the content of the file at the given url.
content = fsutil.read_file_from_url(url, **kwargs)
```

#### `read_file_json`

```python
# Read and decode a json encoded file at the given path.
data = fsutil.read_file_json(path, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None)
```

#### `read_file_lines`

```python
# Read file content lines.
# It is possible to specify the line indexes (negative indexes too),
# very useful especially when reading large files.
content = fsutil.read_file_lines(path, line_start=0, line_end=-1, strip_white=True, skip_empty=True, encoding="utf-8")
```

#### `read_file_lines_count`

```python
# Read file lines count.
lines_count = fsutil.read_file_lines_count(path)
```

#### `remove_dir`

```python
# Remove a directory at the given path and all its content.
# If the directory is removed with success returns True, otherwise False.
# More informations about kwargs supported options here:
# https://docs.python.org/3/library/shutil.html#shutil.rmtree
fsutil.remove_dir(path, **kwargs)
```

#### `remove_dir_content`

```python
# Removes all directory content (both sub-directories and files).
fsutil.remove_dir_content(path)
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

#### `replace_dir`

```python
# Replace directory at the specified path with the directory located at src.
# If autodelete, the src directory will be removed at the end of the operation.
# Optimized for large directories.
fsutil.replace_dir(path, src, autodelete=False)
```

#### `replace_file`

```python
# Replace file at the specified path with the file located at src.
# If autodelete, the src file will be removed at the end of the operation.
# Optimized for large files.
fsutil.replace_file(path, src, autodelete=False)
```

#### `search_dirs`

```python
# Search for directories at path matching the given pattern.
dirs = fsutil.search_dirs(path, pattern="**/*")
```

#### `search_files`

```python
# Search for files at path matching the given pattern.
files = fsutil.search_files(path, pattern="**/*.*")
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
fsutil.write_file(path, content, append=False, encoding="utf-8", atomic=False)
```

#### `write_file_json`

```python
# Write a json file at the given path with the specified data encoded in json format.
fsutil.write_file_json(path, data, encoding="utf-8", atomic=False, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False)
```

## Testing
```bash
# clone repository
git clone https://github.com/fabiocaccamo/python-fsutil.git && cd python-fsutil

# create virtualenv and activate it
python -m venv venv && . venv/bin/activate

# upgrade pip
python -m pip install --upgrade pip

# install requirements
python -m pip install -r requirements.txt -r requirements-test.txt

# install pre-commit to run formatters and linters
pre-commit install --install-hooks

# run tests using tox
tox

# or run tests using unittest
python -m unittest
```

## License
Released under [MIT License](LICENSE.txt).

---

## Supporting

- :star: Star this project on [GitHub](https://github.com/fabiocaccamo/python-fsutil)
- :octocat: Follow me on [GitHub](https://github.com/fabiocaccamo)
- :blue_heart: Follow me on [Twitter](https://twitter.com/fabiocaccamo)
- :moneybag: Sponsor me on [Github](https://github.com/sponsors/fabiocaccamo)

## See also

- [`python-benedict`](https://github.com/fabiocaccamo/python-benedict) - dict subclass with keylist/keypath support, I/O shortcuts (base64, csv, json, pickle, plist, query-string, toml, xml, yaml) and many utilities. 📘

- [`python-fontbro`](https://github.com/fabiocaccamo/python-fontbro) - friendly font operations on top of fontTools. 🧢
