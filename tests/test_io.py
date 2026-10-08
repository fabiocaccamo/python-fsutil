import sys
from datetime import date, datetime
from decimal import Decimal

import pytest
import yaml

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


@pytest.mark.parametrize(
    "encoding", ["utf-8", "utf-8-sig", "utf-16", "utf-16-be", "utf-32", "utf-32-be"]
)
@pytest.mark.parametrize(
    ("line_start", "line_end", "expected"),
    [
        (0, 1, ["甲", "乙"]),
        (1, 1, ["乙"]),
        (-1, -1, ["丙"]),
        (0, -2, ["甲", "乙"]),
        (-2, -1, ["乙", "丙"]),
        (-9, 1, ["甲", "乙"]),
        (6, 8, []),
    ],
)
@pytest.mark.parametrize("trailing_newline", [False, True])
def test_read_file_lines_range_encoding(
    tmp_path, encoding, line_start, line_end, expected, trailing_newline
):
    path = tmp_path / "encoded.txt"
    content = "甲\n乙\n丙" + ("\n" if trailing_newline else "")
    path.write_bytes(content.encode(encoding))

    assert (
        fsutil.read_file_lines(
            path, line_start=line_start, line_end=line_end, encoding=encoding
        )
        == expected
    )


@pytest.mark.parametrize("encoding", ["utf-8", "utf-16", "utf-32"])
@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_read_file_lines_range_preserves_line_endings(tmp_path, encoding, newline):
    path = tmp_path / "encoded.txt"
    path.write_bytes(f"甲{newline} 乙\r丙 {newline}丁".encode(encoding))

    assert fsutil.read_file_lines(
        path,
        line_start=1,
        line_end=-2,
        strip_white=False,
        encoding=encoding,
    ) == [f" 乙\r丙 {newline}"]


@pytest.mark.parametrize("encoding", ["utf-8", "utf-16", "utf-32"])
def test_read_file_lines_range_empty_encoded_file(tmp_path, encoding):
    path = tmp_path / "encoded.txt"
    path.write_bytes("".encode(encoding))

    assert fsutil.read_file_lines(path, line_start=-2, encoding=encoding) == []


def test_read_file_lines_count(temp_path):
    path = temp_path("a/b/c.txt")
    lines = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    fsutil.write_file(path, content="\n".join(lines))

    lines_count = fsutil.read_file_lines_count(path)
    assert lines_count == 10


@pytest.mark.parametrize("atomic", [False, True])
@pytest.mark.parametrize("encoding", ["utf-8", "utf-16"])
@pytest.mark.parametrize(
    "data",
    [
        {"name": "caf\u00e9", "items": [1, True, None]},
        ["a", 2],
        "text",
        None,
        {"date": date(2026, 1, 2)},
    ],
)
def test_read_file_yaml(temp_path, atomic, encoding, data):
    path = temp_path("a/b/c.yaml")
    fsutil.write_file_yaml(path, data, encoding=encoding, atomic=atomic)
    assert fsutil.read_file_yaml(path, encoding=encoding) == data


def test_read_file_yaml_with_empty_file(temp_path):
    path = temp_path("a/b/c.yaml")
    fsutil.write_file(path, content="")
    assert fsutil.read_file_yaml(path) is None


@pytest.mark.parametrize(
    "content",
    [
        "items: [",
        "---\na: 1\n---\nb: 2",
        "!!python/tuple [1, 2]",
    ],
)
def test_read_file_yaml_with_invalid_or_unsafe_content(temp_path, content):
    path = temp_path("a/b/c.yaml")
    fsutil.write_file(path, content=content)
    with pytest.raises(yaml.YAMLError):
        fsutil.read_file_yaml(path)


def test_read_file_yaml_with_missing_file(temp_path):
    path = temp_path("a/b/c.yaml")
    with pytest.raises(OSError):
        fsutil.read_file_yaml(path)


def test_read_file_yaml_without_yaml_installed(temp_path, monkeypatch):
    path = temp_path("a/b/c.yaml")
    fsutil.write_file(path, content="key: value")
    monkeypatch.setitem(sys.modules, "yaml", None)
    with pytest.raises(ModuleNotFoundError, match="PyYAML"):
        fsutil.read_file_yaml(path)


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


def test_write_file_yaml(temp_path):
    path = temp_path("a/b/c.yaml")
    data = {"z": 1, "a": 2, "name": "caf\u00e9"}
    fsutil.write_file_yaml(path, data)
    assert fsutil.read_file(path) == "z: 1\na: 2\nname: caf\u00e9\n"


def test_write_file_yaml_with_options(temp_path):
    path = temp_path("a/b/c.yaml")
    data = {"z": [1, 2], "a": "caf\u00e9"}
    fsutil.write_file_yaml(path, data, sort_keys=True, allow_unicode=False, indent=4)
    assert fsutil.read_file(path) == 'a: "caf\\xE9"\nz:\n- 1\n- 2\n'
    assert fsutil.read_file_yaml(path) == data


@pytest.mark.parametrize("atomic", [False, True])
def test_write_file_yaml_with_unsupported_data(temp_path, atomic):
    path = temp_path("a/b/c.yaml")
    fsutil.write_file(path, content="original")
    with pytest.raises(yaml.representer.RepresenterError):
        fsutil.write_file_yaml(path, object(), atomic=atomic)
    assert fsutil.read_file(path) == "original"
    assert fsutil.list_files(temp_path("a/b")) == [path]


def test_write_file_yaml_with_stream(temp_path):
    path = temp_path("a/b/c.yaml")
    with pytest.raises(TypeError, match="stream"):
        fsutil.write_file_yaml(path, {"key": "value"}, stream=None)
    assert not fsutil.exists(path)


def test_write_file_yaml_without_yaml_installed(temp_path, monkeypatch):
    path = temp_path("a/b/c.yaml")
    monkeypatch.setitem(sys.modules, "yaml", None)
    with pytest.raises(ModuleNotFoundError, match="PyYAML"):
        fsutil.write_file_yaml(path, {"key": "value"})
    assert not fsutil.exists(path)


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
