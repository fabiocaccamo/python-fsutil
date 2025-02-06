from __future__ import annotations

from fsutil.archives import (
    create_tar_file,
    create_zip_file,
    extract_tar_file,
    extract_zip_file,
)
from fsutil.checks import (
    assert_dir,
    assert_exists,
    assert_file,
    assert_not_dir,
    assert_not_exists,
    assert_not_file,
    exists,
    is_dir,
    is_empty,
    is_empty_dir,
    is_empty_file,
    is_file,
)
from fsutil.converters import convert_size_bytes_to_string, convert_size_string_to_bytes
from fsutil.info import (
    get_dir_creation_date,
    get_dir_creation_date_formatted,
    get_dir_hash,
    get_dir_last_modified_date,
    get_dir_last_modified_date_formatted,
    get_dir_size,
    get_dir_size_formatted,
    get_file_creation_date,
    get_file_creation_date_formatted,
    get_file_hash,
    get_file_last_modified_date,
    get_file_last_modified_date_formatted,
    get_file_size,
    get_file_size_formatted,
)
from fsutil.io import (
    read_file,
    read_file_from_url,
    read_file_json,
    read_file_lines,
    read_file_lines_count,
    write_file,
    write_file_json,
)
from fsutil.metadata import (
    __author__,
    __copyright__,
    __description__,
    __email__,
    __license__,
    __title__,
    __version__,
)
from fsutil.operations import (
    clean_dir,
    copy_dir,
    copy_dir_content,
    copy_file,
    create_dir,
    create_file,
    delete_dir,
    delete_dir_content,
    delete_dirs,
    delete_file,
    delete_files,
    download_file,
    list_dirs,
    list_files,
    make_dirs,
    make_dirs_for_file,
    move_dir,
    move_file,
    remove_dir,
    remove_dir_content,
    remove_dirs,
    remove_file,
    remove_files,
    rename_dir,
    rename_file,
    rename_file_basename,
    rename_file_extension,
    replace_dir,
    replace_file,
    search_dirs,
    search_files,
)
from fsutil.paths import (
    get_file_basename,
    get_file_extension,
    get_filename,
    get_parent_dir,
    get_unique_name,
    join_filename,
    join_filepath,
    join_path,
    split_filename,
    split_filepath,
    split_path,
    transform_filepath,
)
from fsutil.perms import get_permissions, set_permissions

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
    "create_tar_file",
    "create_zip_file",
    "delete_dir",
    "delete_dir_content",
    "delete_dirs",
    "delete_file",
    "delete_files",
    "download_file",
    "exists",
    "extract_tar_file",
    "extract_zip_file",
    "get_dir_creation_date",
    "get_dir_creation_date_formatted",
    "get_dir_hash",
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
    "get_permissions",
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
    "set_permissions",
    "split_filename",
    "split_filepath",
    "split_path",
    "transform_filepath",
    "write_file",
    "write_file_json",
]
