# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.9.3](https://github.com/fabiocaccamo/python-fsutil/releases/tag/0.9.3) - 2023-01-12
-   Remove `tests/` from dist.

## [0.9.2](https://github.com/fabiocaccamo/python-fsutil/releases/tag/0.9.2) - 2023-01-11
-   Fix `FileNotFoundError` when calling `make_dirs_for_file` with filename only.
-   Pin test requirements.
-   Bump test requirements.

## [0.9.1](https://github.com/fabiocaccamo/python-fsutil/releases/tag/0.9.1) - 2023-01-02
-   Fix `OSError` when downloading multiple files to the same temp dir.

## [0.9.0](https://github.com/fabiocaccamo/python-fsutil/releases/tag/0.9.0) - 2023-01-02
-   Drop old code targeting `Python < 3.8`.
-   Add `get_unique_name` method.
-   Add `replace_file` method.
-   Add `replace_dir` method.
-   Add `get_dir_hash` method. #10
-   Add support to `pathlib.Path` path arguments. #14
-   Add default value for `pattern` argument in `search_dirs` and `search_files` methods.
-   Add more assertions on path args.
-   Increase tests coverage.
-   Add `setup.cfg` (`setuptools` declarative syntax) generated using `setuptools-py2cfg`.
-   Add `pyupgrade` to `pre-commit` config.
-   Fix duplicated test name.
-   Remove unused variable in tests.

## [0.8.0](https://github.com/fabiocaccamo/python-fsutil/releases/tag/0.8.0) - 2022-12-09
-   Add `Python 3.11` support.
-   Drop `Python < 3.8` support. #17
-   Add `pypy` to CI.
-   Add `pre-commit`.
-   Add default json encoder to `write_file_json` for encoding also `datetime` and `set` objects by default.
-   Replace `str.format` with `f-strings`.
-   Make `dirpath` argument optional in `download_file` method.
-   Fix `download_file` `NameError` when `requests` is not installed.
-   Increase tests coverage.
-   Bump requirements and GitHub actions versions.

## [0.7.0](https://github.com/fabiocaccamo/python-fsutil/releases/tag/0.7.0) - 2022-09-13
-   Add `read_file_lines_count` method.
-   Update `read_file_lines` method with two new arguments: `line_start` and `line_end` *(for specifying the lines-range to read)*.

## [0.6.1](https://github.com/fabiocaccamo/python-fsutil/releases/tag/0.6.1) - 2022-05-20
-   Fixed `create_zip_file` content directory structure.

## [0.6.0](https://github.com/fabiocaccamo/python-fsutil/releases/tag/0.6.0) - 2022-01-25
-   Added `read_file_json` and `write_file_json` methods.
-   Removed `requests` requirement *(it's optional now)*.

## [0.5.0](https://github.com/fabiocaccamo/python-fsutil/releases/tag/0.5.0) - 2021-05-03
-   Added `get_parent_dir` method.
-   Updated `join_path` to force concatenation even with absolute paths.
-   Updated `join_path` to return a normalized path.
-   Updated `join_filepath` method to use `join_path`.

## [0.4.0](https://github.com/fabiocaccamo/python-fsutil/releases/tag/0.4.0) - 2020-12-23
-   Added `delete_dir_content` method (alias for `remove_dir_content` method).
-   Added `download_file` method.
-   Added `read_file_from_url` method.
-   Added `remove_dir_content` and method.

## [0.3.0](https://github.com/fabiocaccamo/python-fsutil/releases/tag/0.3.0) - 2020-11-04
-   Added `create_zip_file` method.
-   Added `extract_zip_file` method.
-   Added `get_dir_creation_date` method.
-   Added `get_dir_creation_date_formatted` method.
-   Added `get_dir_last_modified_date` method.
-   Added `get_dir_last_modified_date_formatted` method.
-   Added `get_file_creation_date` method.
-   Added `get_file_creation_date_formatted` method.
-   Added `get_file_last_modified_date` method.
-   Added `get_file_last_modified_date_formatted` method.
-   Added `read_file_lines` method.
-   Refactored tests.

## [0.2.0](https://github.com/fabiocaccamo/python-fsutil/releases/tag/0.2.0) - 2020-10-29
-   Added `convert_size_bytes_to_string` method.
-   Added `convert_size_string_to_bytes` method.
-   Added `get_dir_size` method.
-   Added `get_dir_size_formatted` method.
-   Added `get_file_size` method.
-   Added `get_file_size_formatted`.
-   Renamed `get_path` to `join_path`.
-   Renamed `get_hash` to `get_file_hash`.
-   Fixed `clean_dir` method and added relative tests.
-   Improved code quality and tests coverage.

## [0.1.0](https://github.com/fabiocaccamo/python-fsutil/releases/tag/0.1.0) - 2020-10-27
-   Released `python-fsutil`
