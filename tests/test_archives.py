import pytest

import fsutil


def test_create_zip_file(temp_path):
    zip_path = temp_path("archive.zip")
    f1_path = temp_path("a/b/f1.txt")
    f2_path = temp_path("a/b/f2.txt")
    f3_path = temp_path("x/y/f3.txt")
    f4_path = temp_path("x/y/f4.txt")
    fsutil.create_file(f1_path, content="hello world 1")
    fsutil.create_file(f2_path, content="hello world 2")
    fsutil.create_file(f3_path, content="hello world 3")
    fsutil.create_file(f4_path, content="hello world 4")
    fsutil.create_zip_file(zip_path, [f1_path, f2_path, f3_path, f4_path])
    with pytest.raises(OSError):
        fsutil.create_zip_file(
            zip_path, [f1_path, f2_path, f3_path, f4_path], overwrite=False
        )
    assert fsutil.is_file(f1_path)
    assert fsutil.is_file(f2_path)
    assert fsutil.is_file(f3_path)
    assert fsutil.is_file(f4_path)
    assert fsutil.is_file(zip_path)
    assert fsutil.get_file_size(zip_path) > 0


def test_create_tar_file(temp_path):
    tar_path = temp_path("archive.tar")
    f1_path = temp_path("a/b/f1.txt")
    f2_path = temp_path("a/b/f2.txt")
    f3_path = temp_path("x/y/f3.txt")
    f4_path = temp_path("x/y/f4.txt")
    fsutil.create_file(f1_path, content="hello world 1")
    fsutil.create_file(f2_path, content="hello world 2")
    fsutil.create_file(f3_path, content="hello world 3")
    fsutil.create_file(f4_path, content="hello world 4")
    fsutil.create_tar_file(tar_path, [f1_path, f2_path, f3_path, f4_path])
    with pytest.raises(OSError):
        fsutil.create_tar_file(
            tar_path, [f1_path, f2_path, f3_path, f4_path], overwrite=False
        )
    assert fsutil.is_file(f1_path)
    assert fsutil.is_file(f2_path)
    assert fsutil.is_file(f3_path)
    assert fsutil.is_file(f4_path)
    assert fsutil.is_file(tar_path)
    assert fsutil.get_file_size(tar_path) > 0


def test_extract_zip_file(temp_path):
    zip_path = temp_path("archive.zip")
    unzip_path = temp_path("unarchive/")
    f1_path = temp_path("a/b/f1.txt")
    f2_path = temp_path("a/b/f2.txt")
    f3_path = temp_path("j/k/f3.txt")
    f4_path = temp_path("j/k/f4.txt")
    f5_path = temp_path("x/y/z/f5.txt")
    f6_path = temp_path("x/y/z/f6.txt")
    f5_f6_dir = temp_path("x")
    fsutil.create_file(f1_path, content="hello world 1")
    fsutil.create_file(f2_path, content="hello world 2")
    fsutil.create_file(f3_path, content="hello world 3")
    fsutil.create_file(f4_path, content="hello world 4")
    fsutil.create_file(f5_path, content="hello world 5")
    fsutil.create_file(f6_path, content="hello world 6")
    fsutil.create_zip_file(zip_path, [f1_path, f2_path, f3_path, f4_path, f5_f6_dir])
    fsutil.extract_zip_file(zip_path, unzip_path)
    assert fsutil.is_dir(unzip_path)
    assert fsutil.is_file(temp_path("unarchive/f1.txt"))
    assert fsutil.is_file(temp_path("unarchive/f2.txt"))
    assert fsutil.is_file(temp_path("unarchive/f3.txt"))
    assert fsutil.is_file(temp_path("unarchive/f4.txt"))
    assert fsutil.is_file(temp_path("unarchive/y/z/f5.txt"))
    assert fsutil.is_file(temp_path("unarchive/y/z/f6.txt"))
    assert fsutil.is_file(zip_path)


def test_extract_zip_file_with_autodelete(temp_path):
    zip_path = temp_path("archive.zip")
    unzip_path = temp_path("unarchive/")
    path = temp_path("f1.txt")
    fsutil.create_file(path, content="hello world 1")
    fsutil.create_zip_file(zip_path, [path])
    fsutil.extract_zip_file(zip_path, unzip_path, autodelete=True)
    assert fsutil.is_dir(unzip_path)
    assert fsutil.is_file(temp_path("unarchive/f1.txt"))
    assert not fsutil.is_file(zip_path)


def test_extract_tar_file(temp_path):
    tar_path = temp_path("archive.tar")
    untar_path = temp_path("unarchive/")
    f1_path = temp_path("a/b/f1.txt")
    f2_path = temp_path("a/b/f2.txt")
    f3_path = temp_path("j/k/f3.txt")
    f4_path = temp_path("j/k/f4.txt")
    f5_path = temp_path("x/y/z/f5.txt")
    f6_path = temp_path("x/y/z/f6.txt")
    f5_f6_dir = temp_path("x")
    fsutil.create_file(f1_path, content="hello world 1")
    fsutil.create_file(f2_path, content="hello world 2")
    fsutil.create_file(f3_path, content="hello world 3")
    fsutil.create_file(f4_path, content="hello world 4")
    fsutil.create_file(f5_path, content="hello world 5")
    fsutil.create_file(f6_path, content="hello world 6")
    fsutil.create_tar_file(tar_path, [f1_path, f2_path, f3_path, f4_path, f5_f6_dir])
    fsutil.extract_tar_file(tar_path, untar_path)
    assert fsutil.is_dir(untar_path)
    assert fsutil.is_file(temp_path("unarchive/f1.txt"))
    assert fsutil.is_file(temp_path("unarchive/f2.txt"))
    assert fsutil.is_file(temp_path("unarchive/f3.txt"))
    assert fsutil.is_file(temp_path("unarchive/f4.txt"))
    assert fsutil.is_file(temp_path("unarchive/y/z/f5.txt"))
    assert fsutil.is_file(temp_path("unarchive/y/z/f6.txt"))
    assert fsutil.is_file(tar_path)


def test_extract_tar_file_with_autodelete(temp_path):
    tar_path = temp_path("archive.tar")
    untar_path = temp_path("unarchive/")
    path = temp_path("f1.txt")
    fsutil.create_file(path, content="hello world 1")
    fsutil.create_tar_file(tar_path, [path])
    fsutil.extract_tar_file(tar_path, untar_path, autodelete=True)
    assert fsutil.is_dir(untar_path)
    assert fsutil.is_file(temp_path("unarchive/f1.txt"))
    assert not fsutil.is_file(tar_path)


if __name__ == "__main__":
    pytest.main()
