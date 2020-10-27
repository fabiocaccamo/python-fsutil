[![](https://img.shields.io/pypi/pyversions/python-fsutil.svg?color=blue&logo=python&logoColor=white)](https://www.python.org/)
[![](https://img.shields.io/pypi/v/python-fsutil.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/python-fsutil/)
[![](https://pepy.tech/badge/python-fsutil)](https://pepy.tech/project/python-fsutil)
[![](https://img.shields.io/github/stars/fabiocaccamo/python-fsutil?logo=github)](https://github.com/fabiocaccamo/python-fsutil/)
[![](https://badges.pufler.dev/visits/fabiocaccamo/python-fsutil?label=visitors&color=blue)](https://badges.pufler.dev)
[![](https://img.shields.io/pypi/l/python-fsutil.svg?color=blue)](https://github.com/fabiocaccamo/python-fsutil/blob/master/LICENSE.txt)

[![](https://img.shields.io/travis/fabiocaccamo/python-fsutil?logo=travis&label=build)](https://travis-ci.org/fabiocaccamo/python-fsutil)
[![](https://img.shields.io/circleci/build/gh/fabiocaccamo/python-fsutil?logo=circleci&label=build)](https://circleci.com/gh/fabiocaccamo/python-fsutil)
[![](https://img.shields.io/codecov/c/gh/fabiocaccamo/python-fsutil?logo=codecov)](https://codecov.io/gh/fabiocaccamo/python-fsutil)
[![](https://img.shields.io/codacy/grade/{{package_codacy_id}}?logo=codacy)](https://www.codacy.com/app/fabiocaccamo/python-fsutil)
[![](https://img.shields.io/scrutinizer/quality/g/fabiocaccamo/python-fsutil?logo=scrutinizer)](https://scrutinizer-ci.com/g/fabiocaccamo/python-fsutil/?branch=master)
[![](https://img.shields.io/codeclimate/maintainability/fabiocaccamo/python-fsutil?logo=code-climate)](https://codeclimate.com/github/fabiocaccamo/python-fsutil/)
[![](https://requires.io/github/fabiocaccamo/python-fsutil/requirements.svg?branch=master)](https://requires.io/github/fabiocaccamo/python-fsutil/requirements/?branch=master)

# python-fsutil
file-system utilities for lazy devs.

## Features
-   **Simple** and intuitive.
-   Supports both **python 2** and **python 3**.
-   Zero dependencies.
-   Well **tested**.

## Index
-   [Installation](#installation)
-   [Usage](#usage)
    -   [Methods](#methods)
-   [Testing](#testing)
-   [License](#license)

## Installation
-   Run `pip install python-fsutil`

## Usage

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
-   [`get_file_basename`](#get_file_basename)
-   [`get_file_extension`](#get_file_extension)
-   [`get_filename`](#get_filename)
-   [`get_hash`](#get_hash)
-   [`get_path`](#get_path)
-   [`is_dir`](#is_dir)
-   [`is_empty`](#is_empty)
-   [`is_empty_dir`](#is_empty_dir)
-   [`is_empty_file`](#is_empty_file)
-   [`is_file`](#is_file)
-   [`join_filename`](#join_filename)
-   [`join_filepath`](#join_filepath)
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
-   [`write_file`](#write_file)

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
