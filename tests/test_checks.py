import pytest

import fsutil


def test_assert_dir(temp_path):
    path = temp_path("a/b/")
    with pytest.raises(OSError):
        fsutil.assert_dir(path)
    fsutil.create_dir(path)
    fsutil.assert_dir(path)


def test_assert_dir_with_file(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path)
    with pytest.raises(OSError):
        fsutil.assert_dir(path)


def test_assert_exists_with_directory(temp_path):
    path = temp_path("a/b/")
    with pytest.raises(OSError):
        fsutil.assert_exists(path)
    fsutil.create_dir(path)
    fsutil.assert_exists(path)


def test_assert_exists_with_file(temp_path):
    path = temp_path("a/b/c.txt")
    with pytest.raises(OSError):
        fsutil.assert_exists(path)
    fsutil.create_file(path)
    fsutil.assert_exists(path)


def test_assert_file(temp_path):
    path = temp_path("a/b/c.txt")
    with pytest.raises(OSError):
        fsutil.assert_file(path)
    fsutil.create_file(path)
    fsutil.assert_file(path)


def test_assert_file_with_directory(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_dir(path)
    with pytest.raises(OSError):
        fsutil.assert_file(path)


def test_exists(temp_path):
    path = temp_path("a/b/")
    assert not fsutil.exists(path)
    fsutil.create_dir(path)
    assert fsutil.exists(path)
    path = temp_path("a/b/c.txt")
    assert not fsutil.exists(path)
    fsutil.create_file(path)
    assert fsutil.exists(path)


def test_is_dir(temp_path):
    path = temp_path("a/b/")
    assert not fsutil.is_dir(path)
    fsutil.create_dir(path)
    assert fsutil.is_dir(path)
    path = temp_path("a/b/c.txt")
    assert not fsutil.is_dir(path)
    fsutil.create_file(path)
    assert not fsutil.is_dir(path)


def test_is_empty(temp_path):
    fsutil.create_file(temp_path("a/b/c.txt"))
    fsutil.create_file(temp_path("a/b/d.txt"), content="1")
    fsutil.create_dir(temp_path("a/b/e"))
    assert fsutil.is_empty(temp_path("a/b/c.txt"))
    assert not fsutil.is_empty(temp_path("a/b/d.txt"))
    assert fsutil.is_empty(temp_path("a/b/e"))
    assert not fsutil.is_empty(temp_path("a/b"))


def test_is_empty_dir(temp_path):
    path = temp_path("a/b/")
    fsutil.create_dir(path)
    assert fsutil.is_empty_dir(path)
    filepath = temp_path("a/b/c.txt")
    fsutil.create_file(filepath)
    assert fsutil.is_file(filepath)
    assert not fsutil.is_empty_dir(path)


def test_is_empty_file(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path)
    assert fsutil.is_empty_file(path)
    path = temp_path("a/b/d.txt")
    fsutil.create_file(path, content="hello world")
    assert not fsutil.is_empty_file(path)


def test_is_file(temp_path):
    path = temp_path("a/b/c.txt")
    assert not fsutil.is_file(path)
    fsutil.create_file(path)
    assert fsutil.is_file(path)


if __name__ == "__main__":
    pytest.main()
