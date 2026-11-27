import os
import uuid
from pathlib import Path
from unittest.mock import patch

import pytest

import fsutil


def test_get_file_basename():
    assert fsutil.get_file_basename("Document") == "Document"
    assert fsutil.get_file_basename("Document.txt") == "Document"
    assert fsutil.get_file_basename(".Document.txt") == ".Document"
    assert fsutil.get_file_basename("/root/a/b/c/Document.txt") == "Document"
    assert (
        fsutil.get_file_basename("https://domain-name.com/Document.txt?p=1")
        == "Document"
    )


def test_get_file_extension():
    assert fsutil.get_file_extension("Document") == ""
    assert fsutil.get_file_extension("Document.txt") == "txt"
    assert fsutil.get_file_extension(".Document.txt") == "txt"
    assert fsutil.get_file_extension("/root/a/b/c/Document.txt") == "txt"
    assert (
        fsutil.get_file_extension("https://domain-name.com/Document.txt?p=1") == "txt"
    )


def test_get_filename():
    assert fsutil.get_filename("Document") == "Document"
    assert fsutil.get_filename("Document.txt") == "Document.txt"
    assert fsutil.get_filename(".Document.txt") == ".Document.txt"
    assert fsutil.get_filename("/root/a/b/c/Document.txt") == "Document.txt"
    assert (
        fsutil.get_filename("https://domain-name.com/Document.txt?p=1")
        == "Document.txt"
    )


@pytest.mark.parametrize("basename", ["Document#1", "Document?1"])
def test_get_filename_with_url_characters_in_local_path(basename):
    filename = f"{basename}.txt"
    path = f"/root/a/b/c/{filename}"
    dirpath = os.path.normpath("/root/a/b/c")
    assert fsutil.get_filename(path) == filename
    assert fsutil.get_filename(Path(path)) == filename
    assert fsutil.get_filename(f"C:/a/b/c/{filename}") == filename
    assert fsutil.get_file_basename(path) == basename
    assert fsutil.get_file_extension(path) == "txt"
    assert fsutil.split_filename(path) == (basename, "txt")
    assert fsutil.split_filepath(path) == (dirpath, filename)


def test_get_filename_with_url_query_and_fragment():
    url = "https://domain-name.com/a/Document.txt?version=1.2#section"
    assert fsutil.get_filename(url) == "Document.txt"
    assert fsutil.get_file_basename(url) == "Document"
    assert fsutil.get_file_extension(url) == "txt"
    assert fsutil.split_filename(url) == ("Document", "txt")
    assert fsutil.split_filepath(url)[1] == "Document.txt"


def test_get_parent_dir():
    s = "/root/a/b/c/Document.txt"
    assert fsutil.get_parent_dir(s) == os.path.normpath("/root/a/b/c")
    assert fsutil.get_parent_dir(s, levels=0) == os.path.normpath("/root/a/b/c")
    assert fsutil.get_parent_dir(s, levels=1) == os.path.normpath("/root/a/b/c")
    assert fsutil.get_parent_dir(s, levels=2) == os.path.normpath("/root/a/b")
    assert fsutil.get_parent_dir(s, levels=3) == os.path.normpath("/root/a")
    assert fsutil.get_parent_dir(s, levels=4) == os.path.normpath("/root")
    assert fsutil.get_parent_dir(s, levels=5) == os.path.normpath("/")
    assert fsutil.get_parent_dir(s, levels=6) == os.path.normpath("/")


def test_get_unique_name(temp_path):
    path = temp_path("a/b/c")
    fsutil.create_dir(path)
    name = fsutil.get_unique_name(
        path,
        prefix="custom-prefix",
        suffix="custom-suffix",
        extension="txt",
        separator="_",
    )
    basename, extension = fsutil.split_filename(name)
    assert basename.startswith("custom-prefix_")
    assert basename.endswith("_custom-suffix")
    assert extension == "txt"


def test_get_unique_name_with_collision(temp_path):
    path = temp_path("a/b/c")
    uids = [uuid.uuid4(), uuid.uuid4()]
    fsutil.create_file(fsutil.join_path(path, f"prefix_{uids[0]}_suffix.txt"))
    with patch("uuid.uuid4", side_effect=uids):
        name = fsutil.get_unique_name(
            path, prefix="prefix", suffix="suffix", extension="TXT", separator="_"
        )
    assert name == f"prefix_{uids[1]}_suffix.txt"


def test_join_filename():
    assert fsutil.join_filename("Document", "txt") == "Document.txt"
    assert fsutil.join_filename("Document", ".txt") == "Document.txt"
    assert fsutil.join_filename(" Document ", " txt ") == "Document.txt"
    assert fsutil.join_filename("Document", " .txt ") == "Document.txt"
    assert fsutil.join_filename("Document", "txt.") == "Document.txt"
    assert fsutil.join_filename("Document", "") == "Document"
    assert fsutil.join_filename("", "txt") == "txt"


def test_join_filename_with_multi_dot_extension():
    assert fsutil.join_filename("archive", "tar.gz") == "archive.tar.gz"
    assert fsutil.join_filename("archive", ".tar.gz") == "archive.tar.gz"
    assert fsutil.join_filename("archive", " .tar.gz ") == "archive.tar.gz"
    assert fsutil.join_filename("archive", "tar.gz.") == "archive.tar.gz"


def test_join_filepath():
    assert fsutil.join_filepath("a/b/c", "Document.txt") == os.path.normpath(
        "a/b/c/Document.txt"
    )


def test_join_path_with_absolute_path():
    assert fsutil.join_path("/a/b/c/", "/document.txt") == os.path.normpath(
        "/a/b/c/document.txt"
    )


@patch("os.sep", "\\")
def test_join_path_with_absolute_path_on_windows():
    assert fsutil.join_path("/a/b/c/", "/document.txt") == os.path.normpath(
        "/a/b/c/document.txt"
    )


def test_join_path_with_parent_dirs():
    assert fsutil.join_path("/a/b/c/", "../../document.txt") == os.path.normpath(
        "/a/document.txt"
    )


def test_split_filename():
    assert fsutil.split_filename("Document") == ("Document", "")
    assert fsutil.split_filename(".Document") == (".Document", "")
    assert fsutil.split_filename("Document.txt") == ("Document", "txt")
    assert fsutil.split_filename(".Document.txt") == (".Document", "txt")
    assert fsutil.split_filename("/root/a/b/c/Document.txt") == ("Document", "txt")
    assert fsutil.split_filename("https://domain-name.com/Document.txt?p=1") == (
        "Document",
        "txt",
    )


def test_split_filepath():
    s = os.path.normpath("/root/a/b/c/Document.txt")
    assert fsutil.split_filepath(s) == (os.path.normpath("/root/a/b/c"), "Document.txt")


def test_split_filepath_with_filename_only():
    s = os.path.normpath("Document.txt")
    assert fsutil.split_filepath(s) == ("", "Document.txt")


def test_split_path():
    s = os.path.normpath("/root/a/b/c/Document.txt")
    assert fsutil.split_path(s) == ["root", "a", "b", "c", "Document.txt"]


def test_transform_filepath_without_args():
    s = "/root/a/b/c/Document.txt"
    with pytest.raises(ValueError):
        fsutil.transform_filepath(s)


def test_transform_filepath_with_empty_str_args():
    s = "/root/a/b/c/Document.txt"
    assert fsutil.transform_filepath(s, dirpath="") == os.path.normpath("Document.txt")
    assert fsutil.transform_filepath(s, basename="") == os.path.normpath(
        "/root/a/b/c/txt"
    )
    assert fsutil.transform_filepath(s, extension="") == os.path.normpath(
        "/root/a/b/c/Document"
    )
    assert fsutil.transform_filepath(
        s, dirpath="/root/x/y/z/", basename="NewDocument", extension="xls"
    ) == os.path.normpath("/root/x/y/z/NewDocument.xls")
    with pytest.raises(ValueError):
        fsutil.transform_filepath(s, dirpath="", basename="", extension="")


def test_transform_filepath_with_str_args():
    s = "/root/a/b/c/Document.txt"
    assert fsutil.transform_filepath(s, dirpath="/root/x/y/z/") == os.path.normpath(
        "/root/x/y/z/Document.txt"
    )
    assert fsutil.transform_filepath(s, basename="NewDocument") == os.path.normpath(
        "/root/a/b/c/NewDocument.txt"
    )
    assert fsutil.transform_filepath(s, extension="xls") == os.path.normpath(
        "/root/a/b/c/Document.xls"
    )
    assert fsutil.transform_filepath(s, extension=".xls") == os.path.normpath(
        "/root/a/b/c/Document.xls"
    )
    assert fsutil.transform_filepath(
        s, dirpath="/root/x/y/z/", basename="NewDocument", extension="xls"
    ) == os.path.normpath("/root/x/y/z/NewDocument.xls")


def test_transform_filepath_with_callable_args():
    s = "/root/a/b/c/Document.txt"
    assert fsutil.transform_filepath(
        s, dirpath=lambda d: f"{d}/x/y/z/"
    ) == os.path.normpath("/root/a/b/c/x/y/z/Document.txt")
    assert fsutil.transform_filepath(
        s, basename=lambda b: b.lower()
    ) == os.path.normpath("/root/a/b/c/document.txt")
    assert fsutil.transform_filepath(s, extension=lambda e: "xls") == os.path.normpath(
        "/root/a/b/c/Document.xls"
    )
    assert fsutil.transform_filepath(
        s,
        dirpath=lambda d: f"{d}/x/y/z/",
        basename=lambda b: b.lower(),
        extension=lambda e: "xls",
    ) == os.path.normpath("/root/a/b/c/x/y/z/document.xls")


if __name__ == "__main__":
    pytest.main()
