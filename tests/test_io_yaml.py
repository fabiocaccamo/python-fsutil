import sys
from datetime import date

import pytest
import yaml

import fsutil


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


if __name__ == "__main__":
    pytest.main()
