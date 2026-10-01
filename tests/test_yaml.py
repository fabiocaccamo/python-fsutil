import subprocess
import sys
from datetime import date
from io import StringIO

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
def test_yaml_roundtrip(tmp_path, atomic, encoding, data):
    path = tmp_path / "nested" / "data.yaml"
    fsutil.write_file_yaml(path, data, encoding=encoding, atomic=atomic)
    assert fsutil.read_file_yaml(path, encoding=encoding) == data


def test_yaml_dump_options(tmp_path):
    path = tmp_path / "options.yaml"
    fsutil.write_file_yaml(path, {"z": [1, 2], "a": 3}, sort_keys=False, indent=4)
    assert path.read_text(encoding="utf-8").startswith("z:")
    assert fsutil.read_file_yaml(path) == {"z": [1, 2], "a": 3}


def test_yaml_empty_file(tmp_path):
    path = tmp_path / "empty.yaml"
    path.write_text("", encoding="utf-8")
    assert fsutil.read_file_yaml(path) is None


@pytest.mark.parametrize(
    "content", ["items: [", "---\na: 1\n---\nb: 2", "!!python/tuple [1, 2]"]
)
def test_yaml_rejects_invalid_or_unsafe_documents(tmp_path, content):
    path = tmp_path / "invalid.yaml"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(yaml.YAMLError):
        fsutil.read_file_yaml(path)


@pytest.mark.parametrize("atomic", [False, True])
def test_yaml_dump_failure_preserves_file(tmp_path, atomic):
    path = tmp_path / "original.yaml"
    path.write_bytes(b"original")
    with pytest.raises(yaml.representer.RepresenterError):
        fsutil.write_file_yaml(path, object(), atomic=atomic)
    assert path.read_bytes() == b"original"
    assert list(tmp_path.iterdir()) == [path]


def test_yaml_missing_file(tmp_path):
    with pytest.raises(OSError):
        fsutil.read_file_yaml(tmp_path / "missing.yaml")


@pytest.mark.parametrize("operation", ["read_file_yaml", "write_file_yaml"])
def test_yaml_missing_dependency(tmp_path, monkeypatch, operation):
    monkeypatch.setitem(sys.modules, "yaml", None)
    args = [tmp_path / "data.yaml"]
    if operation == "write_file_yaml":
        args.append({"key": "value"})
    with pytest.raises(ModuleNotFoundError, match="PyYAML"):
        getattr(fsutil, operation)(*args)
    assert not list(tmp_path.iterdir())


def test_import_without_yaml():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; sys.modules['yaml'] = None; import fsutil; "
            "assert callable(fsutil.read_file_yaml); "
            "assert callable(fsutil.write_file_yaml)",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_yaml_rejects_output_stream_without_modifying_file(tmp_path):
    path = tmp_path / "original.yaml"
    path.write_bytes(b"original")
    stream = StringIO()
    with pytest.raises(TypeError):
        fsutil.write_file_yaml(path, {"key": "value"}, stream=stream)
    assert path.read_bytes() == b"original"
    assert stream.getvalue() == ""
