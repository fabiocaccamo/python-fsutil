import sys
from datetime import datetime
from decimal import Decimal

import pytest

import fsutil


def test_read_file(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.write_file(path, content="Hello World")
    assert fsutil.read_file(path) == "Hello World"


def test_read_file_from_url():
    url = "https://raw.githubusercontent.com/fabiocaccamo/python-fsutil/main/README.md"
    content = fsutil.read_file_from_url(url)
    assert "python-fsutil" in content


def test_read_file_json(temp_path):
    path = temp_path("a/b/c.json")
    now = datetime.now()
    data = {
        "test": "Hello World",
        "test_datetime": now,
        "test_set": {1, 2, 3},
    }
    fsutil.write_file_json(path, data=data)
    expected_data = data.copy()
    expected_data["test_datetime"] = now.isoformat()
    expected_data["test_set"] = list(expected_data["test_set"])
    assert fsutil.read_file_json(path) == expected_data


def test_read_file_lines(temp_path):
    path = temp_path("a/b/c.txt")
    lines = ["", "1 ", " 2", "", "", " 3 ", "  4  ", "", "", "5"]
    fsutil.write_file(path, content="\n".join(lines))

    expected_lines = list(lines)
    lines = fsutil.read_file_lines(path, strip_white=False, skip_empty=False)
    assert lines == expected_lines

    expected_lines = ["", "1", "2", "", "", "3", "4", "", "", "5"]
    lines = fsutil.read_file_lines(path, strip_white=True, skip_empty=False)
    assert lines == expected_lines

    expected_lines = ["1 ", " 2", " 3 ", "  4  ", "5"]
    lines = fsutil.read_file_lines(path, strip_white=False, skip_empty=True)
    assert lines == expected_lines

    expected_lines = ["1", "2", "3", "4", "5"]
    lines = fsutil.read_file_lines(path, strip_white=True, skip_empty=True)
    assert lines == expected_lines


def test_read_file_lines_with_lines_range(temp_path):
    path = temp_path("a/b/c.txt")
    lines = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    fsutil.write_file(path, content="\n".join(lines))

    # single line
    expected_lines = ["1"]
    lines = fsutil.read_file_lines(path, line_start=1, line_end=1)
    assert lines == expected_lines

    # multiple lines
    expected_lines = ["1", "2", "3"]
    lines = fsutil.read_file_lines(path, line_start=1, line_end=3)
    assert lines == expected_lines

    # multiple lines not stripped
    newline = "\r\n" if sys.platform == "win32" else "\n"
    expected_lines = [f"1{newline}", f"2{newline}", f"3{newline}"]
    lines = fsutil.read_file_lines(
        path, line_start=1, line_end=3, strip_white=False, skip_empty=False
    )
    assert lines == expected_lines

    # last line
    expected_lines = ["9"]
    lines = fsutil.read_file_lines(path, line_start=-1)
    assert lines == expected_lines

    # last 3 lines
    expected_lines = ["7", "8", "9"]
    lines = fsutil.read_file_lines(path, line_start=-3)
    assert lines == expected_lines

    # empty file
    fsutil.write_file(path, content="")
    expected_lines = []
    lines = fsutil.read_file_lines(path, line_start=-2)
    assert lines == expected_lines


def test_read_file_lines_count(temp_path):
    path = temp_path("a/b/c.txt")
    lines = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    fsutil.write_file(path, content="\n".join(lines))

    lines_count = fsutil.read_file_lines_count(path)
    assert lines_count == 10


def test_write_file(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.write_file(path, content="Hello World")
    assert fsutil.read_file(path) == "Hello World"
    fsutil.write_file(path, content="Hello Jupiter")
    assert fsutil.read_file(path) == "Hello Jupiter"


def test_write_file_atomic(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.write_file(path, content="Hello World", atomic=True)
    assert fsutil.read_file(path) == "Hello World"
    fsutil.write_file(path, content="Hello Jupiter", atomic=True)
    assert fsutil.read_file(path) == "Hello Jupiter"


def test_write_file_atomic_no_temp_files_left(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.write_file(path, content="Hello World", atomic=True)
    fsutil.write_file(path, content="Hello Jupiter", atomic=True)
    assert fsutil.list_files(temp_path("a/b/")) == [path]


@pytest.mark.skipif(sys.platform.startswith("win"), reason="Test skipped on Windows")
def test_write_file_atomic_permissions_inheritance(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.write_file(path, content="Hello World", atomic=False)
    assert fsutil.get_permissions(path) == 644
    fsutil.set_permissions(path, 777)
    fsutil.write_file(path, content="Hello Jupiter", atomic=True)
    assert fsutil.get_permissions(path) == 777


def test_write_file_with_filename_only():
    path = "document.txt"
    fsutil.write_file(path, content="Hello World")
    assert fsutil.is_file(path)
    # cleanup
    fsutil.remove_file(path)


def test_write_file_json(temp_path):
    path = temp_path("a/b/c.json")
    now = datetime.now()
    dec = Decimal("3.33")
    data = {
        "test": "Hello World",
        "test_datetime": now,
        "test_decimal": dec,
    }
    fsutil.write_file_json(path, data=data)
    assert fsutil.read_file(path) == (
        "{"
        f'"test": "Hello World", '
        f'"test_datetime": "{now.isoformat()}", '
        f'"test_decimal": "{dec}"'
        "}"
    )


def test_write_file_json_atomic(temp_path):
    path = temp_path("a/b/c.json")
    now = datetime.now()
    dec = Decimal("3.33")
    data = {
        "test": "Hello World",
        "test_datetime": now,
        "test_decimal": dec,
    }
    fsutil.write_file_json(path, data=data, atomic=True)
    assert fsutil.read_file(path) == (
        "{"
        f'"test": "Hello World", '
        f'"test_datetime": "{now.isoformat()}", '
        f'"test_decimal": "{dec}"'
        "}"
    )


def test_write_file_with_append(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.write_file(path, content="Hello World")
    assert fsutil.read_file(path) == "Hello World"
    fsutil.write_file(path, content=" - Hello Sun", append=True)
    assert fsutil.read_file(path) == "Hello World - Hello Sun"


def test_write_file_with_append_atomic(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.write_file(path, content="Hello World", atomic=True)
    assert fsutil.read_file(path) == "Hello World"
    fsutil.write_file(path, content=" - Hello Sun", append=True, atomic=True)
    assert fsutil.read_file(path) == "Hello World - Hello Sun"


if __name__ == "__main__":
    pytest.main()
