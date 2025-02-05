import sys

import pytest

import fsutil


@pytest.mark.skipif(sys.platform.startswith("win"), reason="Test skipped on Windows")
def test_get_permissions(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.write_file(path, content="Hello World")
    permissions = fsutil.get_permissions(path)
    assert permissions == 644


@pytest.mark.skipif(sys.platform.startswith("win"), reason="Test skipped on Windows")
def test_set_permissions(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.write_file(path, content="Hello World")
    fsutil.set_permissions(path, 777)
    permissions = fsutil.get_permissions(path)
    assert permissions == 777


if __name__ == "__main__":
    pytest.main()
