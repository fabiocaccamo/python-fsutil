# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.0](https://github.com/fabiocaccamo/python-fsutil/releases/tag/0.6.0) - 2023-01-25
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
