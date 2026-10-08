from datetime import datetime
from decimal import Decimal

import pytest

import fsutil


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


if __name__ == "__main__":
    pytest.main()
