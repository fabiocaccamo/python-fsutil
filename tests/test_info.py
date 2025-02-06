import re
import time
from datetime import datetime, timedelta

import pytest

import fsutil


def create_file_of_size(path, size):
    fsutil.create_file(path)
    size_bytes = fsutil.convert_size_string_to_bytes(size)
    with open(path, "wb") as file:
        file.seek(size_bytes - 1)
        file.write(b"\0")


def test_get_dir_creation_date(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path, content="Hello World")
    creation_date = fsutil.get_dir_creation_date(temp_path("a/b"))
    now = datetime.now()
    assert (now - creation_date) < timedelta(seconds=0.1)
    time.sleep(0.2)
    creation_date = fsutil.get_dir_creation_date(temp_path("a/b"))
    now = datetime.now()
    assert not (now - creation_date) < timedelta(seconds=0.1)


def test_get_dir_creation_date_formatted(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path, content="Hello World")
    creation_date_str = fsutil.get_dir_creation_date_formatted(
        temp_path("a/b"), format="%Y/%m/%d"
    )
    creation_date_re = re.compile(r"^[\d]{4}\/[\d]{2}\/[\d]{2}$")
    assert creation_date_re.match(creation_date_str) is not None


def test_get_dir_hash(temp_path):
    f1_path = temp_path("x/a/b/f1.txt")
    f2_path = temp_path("x/a/b/f2.txt")
    f3_path = temp_path("x/j/k/f3.txt")
    f4_path = temp_path("x/j/k/f4.txt")
    f5_path = temp_path("x/y/z/f5.txt")
    f6_path = temp_path("x/y/z/f6.txt")
    fsutil.create_file(f1_path, content="hello world 1")
    fsutil.create_file(f2_path, content="hello world 2")
    fsutil.create_file(f3_path, content="hello world 3")
    fsutil.create_file(f4_path, content="hello world 4")
    fsutil.create_file(f5_path, content="hello world 5")
    fsutil.create_file(f6_path, content="hello world 6")
    dir_hash = fsutil.get_dir_hash(temp_path("x/"))
    assert dir_hash == "eabe619c41f0c4611b7b9746bededfcb"


def test_get_dir_last_modified_date(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path, content="Hello")
    creation_date = fsutil.get_dir_creation_date(temp_path("a"))
    time.sleep(0.2)
    fsutil.write_file(path, content="Goodbye", append=True)
    now = datetime.now()
    lastmod_date = fsutil.get_dir_last_modified_date(temp_path("a"))
    assert (now - lastmod_date) < timedelta(seconds=0.1)
    assert (lastmod_date - creation_date) > timedelta(seconds=0.15)


def test_get_dir_last_modified_date_formatted(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path, content="Hello World")
    lastmod_date_str = fsutil.get_dir_last_modified_date_formatted(temp_path("a"))
    lastmod_date_re = re.compile(
        r"^[\d]{4}\-[\d]{2}\-[\d]{2}[\s]{1}[\d]{2}\:[\d]{2}\:[\d]{2}$"
    )
    assert lastmod_date_re.match(lastmod_date_str) is not None


def test_get_dir_size(temp_path):
    create_file_of_size(temp_path("a/a-1.txt"), "1.05 MB")  # 1101004
    create_file_of_size(temp_path("a/b/b-1.txt"), "2 MB")  # 2097152
    create_file_of_size(temp_path("a/b/b-2.txt"), "2.25 MB")  # 2359296
    create_file_of_size(temp_path("a/b/c/c-1.txt"), "3.75 MB")  # 3932160
    create_file_of_size(temp_path("a/b/c/c-2.txt"), "500 KB")  # 512000
    create_file_of_size(temp_path("a/b/c/c-3.txt"), "200 KB")  # 204800
    assert fsutil.get_dir_size(temp_path("a")) == 10206412
    assert fsutil.get_dir_size(temp_path("a/b")) == 9105408
    assert fsutil.get_dir_size(temp_path("a/b/c")) == 4648960


def test_get_dir_size_formatted(temp_path):
    create_file_of_size(temp_path("a/a-1.txt"), "1.05 MB")  # 1101004
    create_file_of_size(temp_path("a/b/b-1.txt"), "2 MB")  # 2097152
    create_file_of_size(temp_path("a/b/b-2.txt"), "2.25 MB")  # 2359296
    create_file_of_size(temp_path("a/b/c/c-1.txt"), "3.75 MB")  # 3932160
    create_file_of_size(temp_path("a/b/c/c-2.txt"), "500 KB")  # 512000
    create_file_of_size(temp_path("a/b/c/c-3.txt"), "200 KB")  # 204800
    assert fsutil.get_dir_size_formatted(temp_path("a")) == "9.73 MB"
    assert fsutil.get_dir_size_formatted(temp_path("a/b")) == "8.68 MB"
    assert fsutil.get_dir_size_formatted(temp_path("a/b/c")) == "4.43 MB"


def test_get_file_creation_date(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path, content="Hello World")
    creation_date = fsutil.get_file_creation_date(path)
    now = datetime.now()
    assert (now - creation_date) < timedelta(seconds=0.1)
    time.sleep(0.2)
    creation_date = fsutil.get_file_creation_date(path)
    now = datetime.now()
    assert not (now - creation_date) < timedelta(seconds=0.1)


def test_get_file_creation_date_formatted(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path, content="Hello World")
    creation_date_str = fsutil.get_file_creation_date_formatted(path, format="%Y/%m/%d")
    creation_date_re = re.compile(r"^[\d]{4}\/[\d]{2}\/[\d]{2}$")
    assert creation_date_re.match(creation_date_str) is not None


def test_get_file_hash(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path, content="Hello World")
    file_hash = fsutil.get_file_hash(path)
    assert file_hash == "b10a8db164e0754105b7a99be72e3fe5"


def test_get_file_last_modified_date(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path, content="Hello")
    creation_date = fsutil.get_file_creation_date(path)
    time.sleep(0.2)
    fsutil.write_file(path, content="Goodbye", append=True)
    now = datetime.now()
    lastmod_date = fsutil.get_file_last_modified_date(path)
    assert (now - lastmod_date) < timedelta(seconds=0.1)
    assert (lastmod_date - creation_date) > timedelta(seconds=0.15)


def test_get_file_last_modified_date_formatted(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path, content="Hello World")
    lastmod_date_str = fsutil.get_file_last_modified_date_formatted(path)
    lastmod_date_re = re.compile(
        r"^[\d]{4}\-[\d]{2}\-[\d]{2}[\s]{1}[\d]{2}\:[\d]{2}\:[\d]{2}$"
    )
    assert lastmod_date_re.match(lastmod_date_str) is not None


def test_get_file_size(temp_path):
    path = temp_path("a/b/c.txt")
    create_file_of_size(path, "1.75 MB")
    size = fsutil.get_file_size(path)
    assert size == fsutil.convert_size_string_to_bytes("1.75 MB")


def test_get_file_size_formatted(temp_path):
    path = temp_path("a/b/c.txt")
    create_file_of_size(path, "1.75 MB")
    size = fsutil.get_file_size_formatted(path)
    assert size == "1.75 MB"


if __name__ == "__main__":
    pytest.main()
