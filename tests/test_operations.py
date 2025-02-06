import threading
from unittest.mock import patch

import pytest

import fsutil


def test_clean_dir_only_dirs(temp_path):
    fsutil.create_dir(temp_path("x/y/z/a"))
    fsutil.create_dir(temp_path("x/y/z/b"))
    fsutil.create_dir(temp_path("x/y/z/c"))
    fsutil.create_dir(temp_path("x/y/z/d"))
    fsutil.create_dir(temp_path("x/y/z/e"))
    fsutil.create_file(temp_path("x/y/z/b/f.txt"), content="hello world")
    fsutil.create_file(temp_path("x/y/z/d/f.txt"), content="hello world")
    fsutil.clean_dir(temp_path("x/y"), dirs=False, files=True)
    assert fsutil.exists(temp_path("x/y/z/a"))
    assert fsutil.exists(temp_path("x/y/z/b"))
    assert fsutil.exists(temp_path("x/y/z/c"))
    assert fsutil.exists(temp_path("x/y/z/d"))
    assert fsutil.exists(temp_path("x/y/z/e"))
    fsutil.clean_dir(temp_path("x/y"), dirs=True, files=True)
    assert not fsutil.exists(temp_path("x/y/z/a"))
    assert fsutil.exists(temp_path("x/y/z/b"))
    assert not fsutil.exists(temp_path("x/y/z/c"))
    assert fsutil.exists(temp_path("x/y/z/d"))
    assert not fsutil.exists(temp_path("x/y/z/e"))


def test_clean_dir_only_files(temp_path):
    fsutil.create_file(temp_path("a/b/c/f1.txt"), content="hello world")
    fsutil.create_file(temp_path("a/b/c/f2.txt"))
    fsutil.create_file(temp_path("a/b/c/f3.txt"), content="hello world")
    fsutil.create_file(temp_path("a/b/c/f4.txt"))
    fsutil.create_file(temp_path("a/b/c/f5.txt"), content="hello world")
    fsutil.clean_dir(temp_path("a"), dirs=False, files=False)
    assert fsutil.exists(temp_path("a/b/c/f1.txt"))
    assert fsutil.exists(temp_path("a/b/c/f2.txt"))
    assert fsutil.exists(temp_path("a/b/c/f3.txt"))
    assert fsutil.exists(temp_path("a/b/c/f4.txt"))
    assert fsutil.exists(temp_path("a/b/c/f5.txt"))
    fsutil.clean_dir(temp_path("a"), dirs=False, files=True)
    assert fsutil.exists(temp_path("a/b/c/f1.txt"))
    assert not fsutil.exists(temp_path("a/b/c/f2.txt"))
    assert fsutil.exists(temp_path("a/b/c/f3.txt"))
    assert not fsutil.exists(temp_path("a/b/c/f4.txt"))
    assert fsutil.exists(temp_path("a/b/c/f5.txt"))


def test_clean_dir_dirs_and_files(temp_path):
    fsutil.create_file(temp_path("a/b/c/f1.txt"))
    fsutil.create_file(temp_path("a/b/c/f2.txt"))
    fsutil.create_file(temp_path("a/b/c/f3.txt"))
    fsutil.create_file(temp_path("a/b/c/d/f4.txt"))
    fsutil.create_file(temp_path("a/b/c/d/f5.txt"))
    fsutil.clean_dir(temp_path("a"), dirs=True, files=True)
    assert not fsutil.exists(temp_path("a/b/c/d/f5.txt"))
    assert not fsutil.exists(temp_path("a/b/c/d/f4.txt"))
    assert not fsutil.exists(temp_path("a/b/c/f3.txt"))
    assert not fsutil.exists(temp_path("a/b/c/f2.txt"))
    assert not fsutil.exists(temp_path("a/b/c/f1.txt"))
    assert not fsutil.exists(temp_path("a/b/c"))
    assert not fsutil.exists(temp_path("a/b"))
    assert fsutil.exists(temp_path("a"))


def test_copy_file(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path, content="hello world")
    dest = temp_path("x/y/z.txt")
    fsutil.copy_file(path, dest)
    assert fsutil.is_file(path)
    assert fsutil.is_file(dest)
    assert fsutil.get_file_hash(path) == fsutil.get_file_hash(dest)


def test_copy_dir(temp_path):
    fsutil.create_file(temp_path("a/b/f-1.txt"))
    fsutil.create_file(temp_path("a/b/f-2.txt"))
    fsutil.create_file(temp_path("a/b/f-3.txt"))
    fsutil.copy_dir(temp_path("a/b"), temp_path("x/y/z"))
    filepaths = fsutil.list_files(temp_path("a/b"))
    filenames = [fsutil.get_filename(filepath) for filepath in filepaths]
    assert len(filepaths) == 3
    assert filenames == ["f-1.txt", "f-2.txt", "f-3.txt"]
    filepaths = fsutil.list_files(temp_path("x/y/z/b/"))
    filenames = [fsutil.get_filename(filepath) for filepath in filepaths]
    assert len(filepaths) == 3
    assert filenames == ["f-1.txt", "f-2.txt", "f-3.txt"]


def test_copy_dir_with_overwrite(temp_path):
    fsutil.create_file(temp_path("a/b/f-1.txt"))
    fsutil.create_file(temp_path("a/b/f-2.txt"))
    fsutil.create_file(temp_path("a/b/f-3.txt"))
    fsutil.create_file(temp_path("x/y/z/f-0.txt"))
    fsutil.copy_dir(temp_path("a/b"), temp_path("x/y/z"), overwrite=False)
    with pytest.raises(OSError):
        fsutil.copy_dir(temp_path("a/b"), temp_path("x/y/z"), overwrite=False)
    fsutil.copy_dir(temp_path("a/b"), temp_path("x/y/z"), overwrite=True)


def test_copy_dir_content(temp_path):
    fsutil.create_file(temp_path("a/b/f-1.txt"))
    fsutil.create_file(temp_path("a/b/f-2.txt"))
    fsutil.create_file(temp_path("a/b/f-3.txt"))
    fsutil.copy_dir_content(temp_path("a/b"), temp_path("z"))
    filepaths = fsutil.list_files(temp_path("z"))
    filenames = [fsutil.get_filename(filepath) for filepath in filepaths]
    assert len(filepaths) == 3
    assert filenames == ["f-1.txt", "f-2.txt", "f-3.txt"]


def test_create_file(temp_path):
    path = temp_path("a/b/c.txt")
    assert not fsutil.exists(path)
    fsutil.create_file(path, content="hello world")
    assert fsutil.exists(path)
    assert fsutil.is_file(path)
    assert fsutil.read_file(path) == "hello world"


def test_create_file_with_overwrite(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path, content="hello world")
    with pytest.raises(OSError):
        fsutil.create_file(path, content="hello world")
    fsutil.create_file(path, content="hello moon", overwrite=True)
    assert fsutil.read_file(path) == "hello moon"


def test_delete_dir(temp_path):
    fsutil.create_file(temp_path("a/b/c/d.txt"))
    fsutil.create_file(temp_path("a/b/c/e.txt"))
    fsutil.create_file(temp_path("a/b/c/f.txt"))
    deleted = fsutil.delete_dir(temp_path("a/c/"))
    assert not deleted
    deleted = fsutil.delete_dir(temp_path("a/b/"))
    assert deleted
    assert fsutil.exists(temp_path("a"))
    assert not fsutil.exists(temp_path("a/b"))


def test_delete_dir_content(temp_path):
    fsutil.create_file(temp_path("a/b/c/d.txt"))
    fsutil.create_file(temp_path("a/b/e.txt"))
    fsutil.create_file(temp_path("a/b/f.txt"))
    path = temp_path("a/b/")
    fsutil.delete_dir_content(path)
    assert fsutil.is_empty_dir(path)


def test_delete_dirs(temp_path):
    fsutil.create_file(temp_path("a/b/c/document.txt"))
    fsutil.create_file(temp_path("a/b/d/document.txt"))
    fsutil.create_file(temp_path("a/b/e/document.txt"))
    fsutil.create_file(temp_path("a/b/f/document.txt"))
    path1 = temp_path("a/b/c/")
    path2 = temp_path("a/b/d/")
    path3 = temp_path("a/b/e/")
    path4 = temp_path("a/b/f/")
    assert fsutil.exists(path1)
    assert fsutil.exists(path2)
    assert fsutil.exists(path3)
    assert fsutil.exists(path4)
    fsutil.delete_dirs(path1, path2, path3, path4)
    assert not fsutil.exists(path1)
    assert not fsutil.exists(path2)
    assert not fsutil.exists(path3)
    assert not fsutil.exists(path4)


def test_delete_file(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path)
    assert fsutil.exists(path)
    deleted = fsutil.delete_file(temp_path("a/b/d.txt"))
    assert not deleted
    deleted = fsutil.delete_file(path)
    assert deleted
    assert not fsutil.exists(path)


def test_delete_files(temp_path):
    path1 = temp_path("a/b/c/document.txt")
    path2 = temp_path("a/b/d/document.txt")
    path3 = temp_path("a/b/e/document.txt")
    path4 = temp_path("a/b/f/document.txt")
    fsutil.create_file(path1)
    fsutil.create_file(path2)
    fsutil.create_file(path3)
    fsutil.create_file(path4)
    assert fsutil.exists(path1)
    assert fsutil.exists(path2)
    assert fsutil.exists(path3)
    assert fsutil.exists(path4)
    fsutil.delete_files(path1, path2, path3, path4)
    assert not fsutil.exists(path1)
    assert not fsutil.exists(path2)
    assert not fsutil.exists(path3)
    assert not fsutil.exists(path4)


def test_download_file(temp_path):
    url = "https://raw.githubusercontent.com/fabiocaccamo/python-fsutil/main/README.md"
    path = fsutil.download_file(url, dirpath=temp_path())
    assert fsutil.exists(path)
    lines = fsutil.read_file_lines(path, skip_empty=False)
    lines_count = len(lines)
    assert 500 < lines_count < 1000
    fsutil.remove_file(path)
    assert not fsutil.exists(path)


def test_download_file_multiple_to_temp_dir(temp_path):
    for _ in range(3):
        url = "https://raw.githubusercontent.com/fabiocaccamo/python-fsutil/main/README.md"
        path = fsutil.download_file(url)
        assert fsutil.exists(path)
        lines = fsutil.read_file_lines(path, skip_empty=False)
        lines_count = len(lines)
        assert 500 < lines_count < 1000
        fsutil.remove_file(path)
        assert not fsutil.exists(path)


def test_download_file_without_requests_installed(temp_path):
    url = "https://raw.githubusercontent.com/fabiocaccamo/python-fsutil/main/README.md"
    with patch("fsutil.operations.require_requests", side_effect=ModuleNotFoundError()):
        with pytest.raises(ModuleNotFoundError):
            fsutil.download_file(url, dirpath=temp_path())


def test_list_dirs(temp_path):
    for i in range(0, 5):
        fsutil.create_dir(temp_path(f"a/b/c/d-{i}"))
        fsutil.create_file(temp_path(f"a/b/c/f-{i}"), content=f"{i}")
    dirpaths = fsutil.list_dirs(temp_path("a/b/c"))
    dirnames = [fsutil.split_path(dirpath)[-1] for dirpath in dirpaths]
    assert len(dirpaths) == 5
    assert dirnames == ["d-0", "d-1", "d-2", "d-3", "d-4"]


def test_list_files(temp_path):
    for i in range(0, 5):
        fsutil.create_dir(temp_path(f"a/b/c/d-{i}"))
        fsutil.create_file(temp_path(f"a/b/c/f-{i}.txt"), content=f"{i}")
    filepaths = fsutil.list_files(temp_path("a/b/c"))
    filenames = [fsutil.get_filename(filepath) for filepath in filepaths]
    assert len(filepaths) == 5
    assert filenames == ["f-0.txt", "f-1.txt", "f-2.txt", "f-3.txt", "f-4.txt"]


def test_make_dirs(temp_path):
    path = temp_path("a/b/c/")
    fsutil.make_dirs(path)
    assert fsutil.is_dir(path)


def test_make_dirs_race_condition(temp_path):
    path = temp_path("a/b/c/")
    for _ in range(0, 20):
        t = threading.Thread(target=fsutil.make_dirs, args=[path], kwargs={})
        t.start()
    t.join()
    assert fsutil.is_dir(path)


def test_make_dirs_with_existing_dir(temp_path):
    path = temp_path("a/b/c/")
    fsutil.create_dir(path)
    fsutil.make_dirs(path)
    assert fsutil.is_dir(path)


def test_make_dirs_with_existing_file(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path)
    with pytest.raises(OSError):
        fsutil.make_dirs(path)


def test_make_dirs_for_file(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.make_dirs_for_file(path)
    assert fsutil.is_dir(temp_path("a/b/"))
    assert not fsutil.is_dir(path)
    assert not fsutil.is_file(path)


def test_make_dirs_for_file_with_existing_file(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path)
    fsutil.make_dirs_for_file(path)
    assert fsutil.is_dir(temp_path("a/b/"))
    assert not fsutil.is_dir(path)
    assert fsutil.is_file(path)


def test_make_dirs_for_file_with_existing_dir(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_dir(path)
    with pytest.raises(OSError):
        fsutil.make_dirs_for_file(path)


def test_make_dirs_for_file_with_filename_only(temp_path):
    path = "document.txt"
    fsutil.make_dirs_for_file(path)
    assert not fsutil.is_file(path)


def test_move_dir(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path, content="Hello World")
    fsutil.move_dir(temp_path("a/b"), temp_path("x/y"))
    assert not fsutil.exists(path)
    assert fsutil.is_file(temp_path("x/y/b/c.txt"))


def test_move_file(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path, content="Hello World")
    dest = temp_path("a")
    fsutil.move_file(path, dest)
    assert not fsutil.exists(path)
    assert fsutil.is_file(temp_path("a/c.txt"))


def test_rename_dir(temp_path):
    path = temp_path("a/b/c")
    fsutil.make_dirs(path)
    fsutil.rename_dir(path, "d")
    assert not fsutil.exists(path)
    path = temp_path("a/b/d")
    assert fsutil.exists(path)


def test_rename_dir_with_existing_name(temp_path):
    path = temp_path("a/b/c")
    fsutil.make_dirs(path)
    fsutil.make_dirs(temp_path("a/b/d"))
    with pytest.raises(OSError):
        fsutil.rename_dir(path, "d")


def test_rename_file(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path)
    fsutil.rename_file(path, "d.txt.backup")
    assert not fsutil.exists(path)
    path = temp_path("a/b/d.txt.backup")
    assert fsutil.exists(path)


def test_rename_file_with_existing_name(temp_path):
    path = temp_path("a/b/c")
    fsutil.create_file(path)
    path = temp_path("a/b/d")
    fsutil.create_file(path)
    with pytest.raises(OSError):
        fsutil.rename_file(path, "c")


def test_rename_file_basename(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path)
    fsutil.rename_file_basename(path, "d")
    assert not fsutil.exists(path)
    path = temp_path("a/b/d.txt")
    assert fsutil.exists(path)


def test_rename_file_extension(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path)
    fsutil.rename_file_extension(path, "json")
    assert not fsutil.exists(path)
    path = temp_path("a/b/c.json")
    assert fsutil.exists(path)


def test_remove_dir(temp_path):
    fsutil.create_file(temp_path("a/b/c/d.txt"))
    fsutil.create_file(temp_path("a/b/c/e.txt"))
    fsutil.create_file(temp_path("a/b/c/f.txt"))
    removed = fsutil.remove_dir(temp_path("a/c/"))
    assert not removed
    removed = fsutil.remove_dir(temp_path("a/b/"))
    assert removed
    assert fsutil.exists(temp_path("a"))
    assert not fsutil.exists(temp_path("a/b"))


def test_remove_dir_content(temp_path):
    fsutil.create_file(temp_path("a/b/c/d.txt"))
    fsutil.create_file(temp_path("a/b/e.txt"))
    fsutil.create_file(temp_path("a/b/f.txt"))
    path = temp_path("a/b/")
    fsutil.remove_dir_content(path)
    assert fsutil.is_empty_dir(path)


def test_remove_dirs(temp_path):
    fsutil.create_file(temp_path("a/b/c/document.txt"))
    fsutil.create_file(temp_path("a/b/d/document.txt"))
    fsutil.create_file(temp_path("a/b/e/document.txt"))
    fsutil.create_file(temp_path("a/b/f/document.txt"))
    path1 = temp_path("a/b/c/")
    path2 = temp_path("a/b/d/")
    path3 = temp_path("a/b/e/")
    path4 = temp_path("a/b/f/")
    assert fsutil.exists(path1)
    assert fsutil.exists(path2)
    assert fsutil.exists(path3)
    assert fsutil.exists(path4)
    fsutil.remove_dirs(path1, path2, path3, path4)
    assert not fsutil.exists(path1)
    assert not fsutil.exists(path2)
    assert not fsutil.exists(path3)
    assert not fsutil.exists(path4)


def test_remove_file(temp_path):
    path = temp_path("a/b/c.txt")
    fsutil.create_file(path)
    assert fsutil.exists(path)
    removed = fsutil.remove_file(temp_path("a/b/d.txt"))
    assert not removed
    removed = fsutil.remove_file(path)
    assert removed
    assert not fsutil.exists(path)


def test_remove_files(temp_path):
    path1 = temp_path("a/b/c/document.txt")
    path2 = temp_path("a/b/d/document.txt")
    path3 = temp_path("a/b/e/document.txt")
    path4 = temp_path("a/b/f/document.txt")
    fsutil.create_file(path1)
    fsutil.create_file(path2)
    fsutil.create_file(path3)
    fsutil.create_file(path4)
    assert fsutil.exists(path1)
    assert fsutil.exists(path2)
    assert fsutil.exists(path3)
    assert fsutil.exists(path4)
    fsutil.remove_files(path1, path2, path3, path4)
    assert not fsutil.exists(path1)
    assert not fsutil.exists(path2)
    assert not fsutil.exists(path3)
    assert not fsutil.exists(path4)


def test_replace_file(temp_path):
    dest = temp_path("a/b/c.txt")
    src = temp_path("d/e/f.txt")
    fsutil.create_file(dest, "old")
    fsutil.create_file(src, "new")
    fsutil.replace_file(dest, src)
    content = fsutil.read_file(dest)
    assert content == "new"
    assert fsutil.exists(src)


def test_replace_file_with_autodelete(temp_path):
    dest_file = temp_path("a/b/c.txt")
    src_file = temp_path("d/e/f.txt")
    fsutil.create_file(dest_file, "old")
    fsutil.create_file(src_file, "new")
    fsutil.replace_file(dest_file, src_file, autodelete=True)
    content = fsutil.read_file(dest_file)
    assert content == "new"
    assert not fsutil.exists(src_file)


def test_replace_dir(temp_path):
    dest_dir = temp_path("a/b/")
    dest_file = temp_path("a/b/c.txt")
    src_dir = temp_path("d/e/")
    src_file = temp_path("d/e/f.txt")
    fsutil.create_file(dest_file, "old")
    fsutil.create_file(src_file, "new")
    fsutil.replace_dir(dest_dir, src_dir)
    content = fsutil.read_file(temp_path("a/b/f.txt"))
    assert content == "new"
    assert fsutil.exists(src_dir)


def test_replace_dir_with_autodelete(temp_path):
    dest_dir = temp_path("a/b/")
    dest_file = temp_path("a/b/c.txt")
    src_dir = temp_path("d/e/")
    src_file = temp_path("d/e/f.txt")
    fsutil.create_file(dest_file, "old")
    fsutil.create_file(src_file, "new")
    fsutil.replace_dir(dest_dir, src_dir, autodelete=True)
    content = fsutil.read_file(temp_path("a/b/f.txt"))
    assert content == "new"
    assert not fsutil.exists(src_dir)


def test_search_files(temp_path):
    fsutil.create_file(temp_path("a/b/c/IMG_1000.jpg"))
    fsutil.create_file(temp_path("a/b/c/IMG_1001.jpg"))
    fsutil.create_file(temp_path("a/b/c/IMG_1002.png"))
    fsutil.create_file(temp_path("a/b/c/IMG_1003.jpg"))
    fsutil.create_file(temp_path("a/b/c/IMG_1004.jpg"))
    fsutil.create_file(temp_path("a/x/c/IMG_1005.png"))
    fsutil.create_file(temp_path("x/b/c/IMG_1006.png"))
    fsutil.create_file(temp_path("a/b/c/DOC_1007.png"))
    results = fsutil.search_files(temp_path("a/"), "**/c/IMG_*.png")
    expected_results = [
        temp_path("a/b/c/IMG_1002.png"),
        temp_path("a/x/c/IMG_1005.png"),
    ]
    assert results == expected_results


def test_search_dirs(temp_path):
    fsutil.create_file(temp_path("a/b/c/IMG_1000.jpg"))
    fsutil.create_file(temp_path("x/y/z/c/IMG_1001.jpg"))
    fsutil.create_file(temp_path("a/c/IMG_1002.png"))
    fsutil.create_file(temp_path("c/b/c/IMG_1003.jpg"))
    results = fsutil.search_dirs(temp_path(""), "**/c")
    expected_results = [
        temp_path("a/b/c"),
        temp_path("a/c"),
        temp_path("c"),
        temp_path("c/b/c"),
        temp_path("x/y/z/c"),
    ]
    assert results == expected_results


if __name__ == "__main__":
    pytest.main()
