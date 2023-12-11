import re
import threading
import time
import unittest
from datetime import datetime, timedelta
from decimal import Decimal

import fsutil


class fsutil_test_case(unittest.TestCase):
    def setUp(self):
        fsutil.remove_dir(self.temp_path())

    def tearDown(self):
        fsutil.remove_dir(self.temp_path())

    @staticmethod
    def temp_path(filepath=""):
        return fsutil.join_path(__file__, f"temp/{filepath}")

    @staticmethod
    def temp_file_of_size(path, size):
        fsutil.create_file(path)
        size_bytes = fsutil.convert_size_string_to_bytes(size)
        with open(path, "wb") as file:
            file.seek(size_bytes - 1)
            file.write(b"\0")

    def test_assert_dir(self):
        path = self.temp_path("a/b/")
        with self.assertRaises(OSError):
            fsutil.assert_dir(path)
        fsutil.create_dir(path)
        fsutil.assert_dir(path)

    def test_assert_dir_with_file(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path)
        with self.assertRaises(OSError):
            fsutil.assert_dir(path)

    def test_assert_exists_with_directory(self):
        path = self.temp_path("a/b/")
        with self.assertRaises(OSError):
            fsutil.assert_exists(path)
        fsutil.create_dir(path)
        fsutil.assert_exists(path)

    def test_assert_exists_with_file(self):
        path = self.temp_path("a/b/c.txt")
        with self.assertRaises(OSError):
            fsutil.assert_exists(path)
        fsutil.create_file(path)
        fsutil.assert_exists(path)

    def test_assert_file(self):
        path = self.temp_path("a/b/c.txt")
        with self.assertRaises(OSError):
            fsutil.assert_file(path)
        fsutil.create_file(path)
        fsutil.assert_file(path)

    def test_assert_file_with_directory(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_dir(path)
        with self.assertRaises(OSError):
            fsutil.assert_file(path)

    def test_clean_dir_only_dirs(self):
        fsutil.create_dir(self.temp_path("x/y/z/a"))
        fsutil.create_dir(self.temp_path("x/y/z/b"))
        fsutil.create_dir(self.temp_path("x/y/z/c"))
        fsutil.create_dir(self.temp_path("x/y/z/d"))
        fsutil.create_dir(self.temp_path("x/y/z/e"))
        fsutil.create_file(self.temp_path("x/y/z/b/f.txt"), content="hello world")
        fsutil.create_file(self.temp_path("x/y/z/d/f.txt"), content="hello world")
        fsutil.clean_dir(self.temp_path("x/y"), dirs=False, files=True)
        self.assertTrue(fsutil.exists(self.temp_path("x/y/z/a")))
        self.assertTrue(fsutil.exists(self.temp_path("x/y/z/b")))
        self.assertTrue(fsutil.exists(self.temp_path("x/y/z/c")))
        self.assertTrue(fsutil.exists(self.temp_path("x/y/z/d")))
        self.assertTrue(fsutil.exists(self.temp_path("x/y/z/e")))
        fsutil.clean_dir(self.temp_path("x/y"), dirs=True, files=True)
        self.assertFalse(fsutil.exists(self.temp_path("x/y/z/a")))
        self.assertTrue(fsutil.exists(self.temp_path("x/y/z/b")))
        self.assertFalse(fsutil.exists(self.temp_path("x/y/z/c")))
        self.assertTrue(fsutil.exists(self.temp_path("x/y/z/d")))
        self.assertFalse(fsutil.exists(self.temp_path("x/y/z/e")))

    def test_clean_dir_only_files(self):
        fsutil.create_file(self.temp_path("a/b/c/f1.txt"), content="hello world")
        fsutil.create_file(self.temp_path("a/b/c/f2.txt"))
        fsutil.create_file(self.temp_path("a/b/c/f3.txt"), content="hello world")
        fsutil.create_file(self.temp_path("a/b/c/f4.txt"))
        fsutil.create_file(self.temp_path("a/b/c/f5.txt"), content="hello world")
        fsutil.clean_dir(self.temp_path("a"), dirs=False, files=False)
        self.assertTrue(fsutil.exists(self.temp_path("a/b/c/f1.txt")))
        self.assertTrue(fsutil.exists(self.temp_path("a/b/c/f2.txt")))
        self.assertTrue(fsutil.exists(self.temp_path("a/b/c/f3.txt")))
        self.assertTrue(fsutil.exists(self.temp_path("a/b/c/f4.txt")))
        self.assertTrue(fsutil.exists(self.temp_path("a/b/c/f5.txt")))
        fsutil.clean_dir(self.temp_path("a"), dirs=False, files=True)
        self.assertTrue(fsutil.exists(self.temp_path("a/b/c/f1.txt")))
        self.assertFalse(fsutil.exists(self.temp_path("a/b/c/f2.txt")))
        self.assertTrue(fsutil.exists(self.temp_path("a/b/c/f3.txt")))
        self.assertFalse(fsutil.exists(self.temp_path("a/b/c/f4.txt")))
        self.assertTrue(fsutil.exists(self.temp_path("a/b/c/f5.txt")))

    def test_clean_dir_dirs_and_files(self):
        fsutil.create_file(self.temp_path("a/b/c/f1.txt"))
        fsutil.create_file(self.temp_path("a/b/c/f2.txt"))
        fsutil.create_file(self.temp_path("a/b/c/f3.txt"))
        fsutil.create_file(self.temp_path("a/b/c/d/f4.txt"))
        fsutil.create_file(self.temp_path("a/b/c/d/f5.txt"))
        fsutil.clean_dir(self.temp_path("a"), dirs=True, files=True)
        self.assertFalse(fsutil.exists(self.temp_path("a/b/c/d/f5.txt")))
        self.assertFalse(fsutil.exists(self.temp_path("a/b/c/d/f4.txt")))
        self.assertFalse(fsutil.exists(self.temp_path("a/b/c/f3.txt")))
        self.assertFalse(fsutil.exists(self.temp_path("a/b/c/f2.txt")))
        self.assertFalse(fsutil.exists(self.temp_path("a/b/c/f1.txt")))
        self.assertFalse(fsutil.exists(self.temp_path("a/b/c")))
        self.assertFalse(fsutil.exists(self.temp_path("a/b")))
        self.assertTrue(fsutil.exists(self.temp_path("a")))

    def test_convert_size_bytes_to_string(self):
        self.assertEqual(fsutil.convert_size_bytes_to_string(1023), "1023 bytes")
        self.assertEqual(fsutil.convert_size_bytes_to_string(1024), "1 KB")
        self.assertEqual(fsutil.convert_size_bytes_to_string(1048576), "1.00 MB")
        self.assertEqual(fsutil.convert_size_bytes_to_string(1572864), "1.50 MB")
        self.assertEqual(fsutil.convert_size_bytes_to_string(1073741824), "1.00 GB")
        self.assertEqual(fsutil.convert_size_bytes_to_string(1879048192), "1.75 GB")
        self.assertEqual(fsutil.convert_size_bytes_to_string(1099511627776), "1.00 TB")

    def test_convert_size_bytes_to_string_and_convert_size_string_to_bytes(self):
        self.assertEqual(
            fsutil.convert_size_bytes_to_string(
                fsutil.convert_size_string_to_bytes("1023 bytes")
            ),
            "1023 bytes",
        )
        self.assertEqual(
            fsutil.convert_size_bytes_to_string(
                fsutil.convert_size_string_to_bytes("1 KB")
            ),
            "1 KB",
        )
        self.assertEqual(
            fsutil.convert_size_bytes_to_string(
                fsutil.convert_size_string_to_bytes("1.00 MB")
            ),
            "1.00 MB",
        )
        self.assertEqual(
            fsutil.convert_size_bytes_to_string(
                fsutil.convert_size_string_to_bytes("1.25 MB")
            ),
            "1.25 MB",
        )
        self.assertEqual(
            fsutil.convert_size_bytes_to_string(
                fsutil.convert_size_string_to_bytes("2.50 MB")
            ),
            "2.50 MB",
        )
        self.assertEqual(
            fsutil.convert_size_bytes_to_string(
                fsutil.convert_size_string_to_bytes("1.00 GB")
            ),
            "1.00 GB",
        )
        self.assertEqual(
            fsutil.convert_size_bytes_to_string(
                fsutil.convert_size_string_to_bytes("1.09 GB")
            ),
            "1.09 GB",
        )
        self.assertEqual(
            fsutil.convert_size_bytes_to_string(
                fsutil.convert_size_string_to_bytes("1.99 GB")
            ),
            "1.99 GB",
        )
        self.assertEqual(
            fsutil.convert_size_bytes_to_string(
                fsutil.convert_size_string_to_bytes("1.00 TB")
            ),
            "1.00 TB",
        )

    def test_convert_size_string_to_bytes(self):
        self.assertEqual(fsutil.convert_size_string_to_bytes("1 KB"), 1024)
        self.assertEqual(fsutil.convert_size_string_to_bytes("1.00 MB"), 1048576)
        self.assertEqual(fsutil.convert_size_string_to_bytes("1.00 GB"), 1073741824)
        self.assertEqual(fsutil.convert_size_string_to_bytes("1.00 TB"), 1099511627776)

    def test_convert_size_string_to_bytes_and_convert_size_bytes_to_string(self):
        self.assertEqual(
            fsutil.convert_size_string_to_bytes(
                fsutil.convert_size_bytes_to_string(1023)
            ),
            1023,
        )
        self.assertEqual(
            fsutil.convert_size_string_to_bytes(
                fsutil.convert_size_bytes_to_string(1024)
            ),
            1024,
        )
        self.assertEqual(
            fsutil.convert_size_string_to_bytes(
                fsutil.convert_size_bytes_to_string(1048576)
            ),
            1048576,
        )
        self.assertEqual(
            fsutil.convert_size_string_to_bytes(
                fsutil.convert_size_bytes_to_string(1310720)
            ),
            1310720,
        )
        self.assertEqual(
            fsutil.convert_size_string_to_bytes(
                fsutil.convert_size_bytes_to_string(2621440)
            ),
            2621440,
        )
        self.assertEqual(
            fsutil.convert_size_string_to_bytes(
                fsutil.convert_size_bytes_to_string(1073741824)
            ),
            1073741824,
        )
        self.assertEqual(
            fsutil.convert_size_string_to_bytes(
                fsutil.convert_size_bytes_to_string(1170378588)
            ),
            1170378588,
        )
        self.assertEqual(
            fsutil.convert_size_string_to_bytes(
                fsutil.convert_size_bytes_to_string(2136746229)
            ),
            2136746229,
        )
        self.assertEqual(
            fsutil.convert_size_string_to_bytes(
                fsutil.convert_size_bytes_to_string(1099511627776)
            ),
            1099511627776,
        )

    def test_copy_file(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path, content="hello world")
        dest = self.temp_path("x/y/z.txt")
        fsutil.copy_file(path, dest)
        self.assertTrue(fsutil.is_file(path))
        self.assertTrue(fsutil.is_file(dest))
        self.assertEqual(fsutil.get_file_hash(path), fsutil.get_file_hash(dest))

    def test_copy_dir(self):
        fsutil.create_file(self.temp_path("a/b/f-1.txt"))
        fsutil.create_file(self.temp_path("a/b/f-2.txt"))
        fsutil.create_file(self.temp_path("a/b/f-3.txt"))
        fsutil.copy_dir(self.temp_path("a/b"), self.temp_path("x/y/z"))
        filepaths = fsutil.list_files(self.temp_path("a/b"))
        filenames = [fsutil.get_filename(filepath) for filepath in filepaths]
        self.assertEqual(len(filepaths), 3)
        self.assertEqual(filenames, ["f-1.txt", "f-2.txt", "f-3.txt"])
        filepaths = fsutil.list_files(self.temp_path("x/y/z/b/"))
        filenames = [fsutil.get_filename(filepath) for filepath in filepaths]
        self.assertEqual(len(filepaths), 3)
        self.assertEqual(filenames, ["f-1.txt", "f-2.txt", "f-3.txt"])

    def test_copy_dir_with_overwrite(self):
        fsutil.create_file(self.temp_path("a/b/f-1.txt"))
        fsutil.create_file(self.temp_path("a/b/f-2.txt"))
        fsutil.create_file(self.temp_path("a/b/f-3.txt"))
        fsutil.create_file(self.temp_path("x/y/z/f-0.txt"))
        fsutil.copy_dir(self.temp_path("a/b"), self.temp_path("x/y/z"), overwrite=False)
        with self.assertRaises(OSError):
            fsutil.copy_dir(
                self.temp_path("a/b"), self.temp_path("x/y/z"), overwrite=False
            )
        fsutil.copy_dir(self.temp_path("a/b"), self.temp_path("x/y/z"), overwrite=True)

    def test_copy_dir_content(self):
        fsutil.create_file(self.temp_path("a/b/f-1.txt"))
        fsutil.create_file(self.temp_path("a/b/f-2.txt"))
        fsutil.create_file(self.temp_path("a/b/f-3.txt"))
        fsutil.copy_dir_content(self.temp_path("a/b"), self.temp_path("z"))
        filepaths = fsutil.list_files(self.temp_path("z"))
        filenames = [fsutil.get_filename(filepath) for filepath in filepaths]
        self.assertEqual(len(filepaths), 3)
        self.assertEqual(filenames, ["f-1.txt", "f-2.txt", "f-3.txt"])

    def test_create_file(self):
        path = self.temp_path("a/b/c.txt")
        self.assertFalse(fsutil.exists(path))
        fsutil.create_file(path, content="hello world")
        self.assertTrue(fsutil.exists(path))
        self.assertTrue(fsutil.is_file(path))
        self.assertEqual(fsutil.read_file(path), "hello world")

    def test_create_file_with_overwrite(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path, content="hello world")
        with self.assertRaises(OSError):
            fsutil.create_file(path, content="hello world")
        fsutil.create_file(path, content="hello moon", overwrite=True)
        self.assertEqual(fsutil.read_file(path), "hello moon")

    def test_create_zip_file(self):
        zip_path = self.temp_path("archive.zip")
        f1_path = self.temp_path("a/b/f1.txt")
        f2_path = self.temp_path("a/b/f2.txt")
        f3_path = self.temp_path("x/y/f3.txt")
        f4_path = self.temp_path("x/y/f4.txt")
        fsutil.create_file(f1_path, content="hello world 1")
        fsutil.create_file(f2_path, content="hello world 2")
        fsutil.create_file(f3_path, content="hello world 3")
        fsutil.create_file(f4_path, content="hello world 4")
        fsutil.create_zip_file(zip_path, [f1_path, f2_path, f3_path, f4_path])
        with self.assertRaises(OSError):
            fsutil.create_zip_file(
                zip_path, [f1_path, f2_path, f3_path, f4_path], overwrite=False
            )
        self.assertTrue(fsutil.is_file(f1_path))
        self.assertTrue(fsutil.is_file(f2_path))
        self.assertTrue(fsutil.is_file(f3_path))
        self.assertTrue(fsutil.is_file(f4_path))
        self.assertTrue(fsutil.is_file(zip_path))
        self.assertTrue(fsutil.get_file_size(zip_path) > 0)

    def test_create_tar_file(self):
        tar_path = self.temp_path("archive.zip")
        f1_path = self.temp_path("a/b/f1.txt")
        f2_path = self.temp_path("a/b/f2.txt")
        f3_path = self.temp_path("x/y/f3.txt")
        f4_path = self.temp_path("x/y/f4.txt")
        fsutil.create_file(f1_path, content="hello world 1")
        fsutil.create_file(f2_path, content="hello world 2")
        fsutil.create_file(f3_path, content="hello world 3")
        fsutil.create_file(f4_path, content="hello world 4")
        fsutil.create_tar_file(tar_path, [f1_path, f2_path, f3_path, f4_path])
        with self.assertRaises(OSError):
            fsutil.create_tar_file(
                tar_path, [f1_path, f2_path, f3_path, f4_path], overwrite=False
            )
        self.assertTrue(fsutil.is_file(f1_path))
        self.assertTrue(fsutil.is_file(f2_path))
        self.assertTrue(fsutil.is_file(f3_path))
        self.assertTrue(fsutil.is_file(f4_path))
        self.assertTrue(fsutil.is_file(tar_path))
        self.assertTrue(fsutil.get_file_size(tar_path) > 0)

    def test_delete_dir(self):
        fsutil.create_file(self.temp_path("a/b/c/d.txt"))
        fsutil.create_file(self.temp_path("a/b/c/e.txt"))
        fsutil.create_file(self.temp_path("a/b/c/f.txt"))
        deleted = fsutil.delete_dir(self.temp_path("a/c/"))
        self.assertFalse(deleted)
        deleted = fsutil.delete_dir(self.temp_path("a/b/"))
        self.assertTrue(deleted)
        self.assertTrue(fsutil.exists(self.temp_path("a")))
        self.assertFalse(fsutil.exists(self.temp_path("a/b")))

    def test_delete_dir_content(self):
        fsutil.create_file(self.temp_path("a/b/c/d.txt"))
        fsutil.create_file(self.temp_path("a/b/e.txt"))
        fsutil.create_file(self.temp_path("a/b/f.txt"))
        path = self.temp_path("a/b/")
        fsutil.delete_dir_content(path)
        self.assertTrue(fsutil.is_empty_dir(path))

    def test_delete_dirs(self):
        fsutil.create_file(self.temp_path("a/b/c/document.txt"))
        fsutil.create_file(self.temp_path("a/b/d/document.txt"))
        fsutil.create_file(self.temp_path("a/b/e/document.txt"))
        fsutil.create_file(self.temp_path("a/b/f/document.txt"))
        path1 = self.temp_path("a/b/c/")
        path2 = self.temp_path("a/b/d/")
        path3 = self.temp_path("a/b/e/")
        path4 = self.temp_path("a/b/f/")
        self.assertTrue(fsutil.exists(path1))
        self.assertTrue(fsutil.exists(path2))
        self.assertTrue(fsutil.exists(path3))
        self.assertTrue(fsutil.exists(path4))
        fsutil.delete_dirs(path1, path2, path3, path4)
        self.assertFalse(fsutil.exists(path1))
        self.assertFalse(fsutil.exists(path2))
        self.assertFalse(fsutil.exists(path3))
        self.assertFalse(fsutil.exists(path4))

    def test_delete_file(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(self.temp_path("a/b/c.txt"))
        self.assertTrue(fsutil.exists(path))
        deleted = fsutil.delete_file(self.temp_path("a/b/d.txt"))
        self.assertFalse(deleted)
        deleted = fsutil.delete_file(path)
        self.assertTrue(deleted)
        self.assertFalse(fsutil.exists(path))

    def test_delete_files(self):
        path1 = self.temp_path("a/b/c/document.txt")
        path2 = self.temp_path("a/b/d/document.txt")
        path3 = self.temp_path("a/b/e/document.txt")
        path4 = self.temp_path("a/b/f/document.txt")
        fsutil.create_file(path1)
        fsutil.create_file(path2)
        fsutil.create_file(path3)
        fsutil.create_file(path4)
        self.assertTrue(fsutil.exists(path1))
        self.assertTrue(fsutil.exists(path2))
        self.assertTrue(fsutil.exists(path3))
        self.assertTrue(fsutil.exists(path4))
        fsutil.delete_files(path1, path2, path3, path4)
        self.assertFalse(fsutil.exists(path1))
        self.assertFalse(fsutil.exists(path2))
        self.assertFalse(fsutil.exists(path3))
        self.assertFalse(fsutil.exists(path4))

    def test_download_file(self):
        url = "https://raw.githubusercontent.com/fabiocaccamo/python-fsutil/main/README.md"
        path = fsutil.download_file(url, dirpath=__file__)
        self.assertTrue(fsutil.exists(path))
        lines = fsutil.read_file_lines(path, skip_empty=False)
        lines_count = len(lines)
        self.assertTrue(lines_count > 500 and lines_count < 1000)
        fsutil.remove_file(path)
        self.assertFalse(fsutil.exists(path))

    def test_download_file_multiple_to_temp_dir(self):
        for _ in range(3):
            url = "https://raw.githubusercontent.com/fabiocaccamo/python-fsutil/main/README.md"
            path = fsutil.download_file(url)
            self.assertTrue(fsutil.exists(path))
            lines = fsutil.read_file_lines(path, skip_empty=False)
            lines_count = len(lines)
            self.assertTrue(lines_count > 500 and lines_count < 1000)
            fsutil.remove_file(path)
            self.assertFalse(fsutil.exists(path))

    def test_download_file_without_requests_installed(self):
        requests_installed = fsutil.requests_installed
        fsutil.requests_installed = False
        url = "https://raw.githubusercontent.com/fabiocaccamo/python-fsutil/main/README.md"
        with self.assertRaises(ModuleNotFoundError):
            fsutil.download_file(url, dirpath=__file__)
        fsutil.requests_installed = requests_installed

    def test_exists(self):
        path = self.temp_path("a/b/")
        self.assertFalse(fsutil.exists(path))
        fsutil.create_dir(path)
        self.assertTrue(fsutil.exists(path))
        path = self.temp_path("a/b/c.txt")
        self.assertFalse(fsutil.exists(path))
        fsutil.create_file(path)
        self.assertTrue(fsutil.exists(path))

    def test_extract_zip_file(self):
        zip_path = self.temp_path("archive.zip")
        unzip_path = self.temp_path("unarchive/")
        f1_path = self.temp_path("a/b/f1.txt")
        f2_path = self.temp_path("a/b/f2.txt")
        f3_path = self.temp_path("j/k/f3.txt")
        f4_path = self.temp_path("j/k/f4.txt")
        f5_path = self.temp_path("x/y/z/f5.txt")
        f6_path = self.temp_path("x/y/z/f6.txt")
        f5_f6_dir = self.temp_path("x")
        fsutil.create_file(f1_path, content="hello world 1")
        fsutil.create_file(f2_path, content="hello world 2")
        fsutil.create_file(f3_path, content="hello world 3")
        fsutil.create_file(f4_path, content="hello world 4")
        fsutil.create_file(f5_path, content="hello world 5")
        fsutil.create_file(f6_path, content="hello world 6")
        fsutil.create_zip_file(
            zip_path, [f1_path, f2_path, f3_path, f4_path, f5_f6_dir]
        )
        fsutil.extract_zip_file(zip_path, unzip_path)
        self.assertTrue(fsutil.is_dir(unzip_path))
        self.assertTrue(fsutil.is_file(self.temp_path("unarchive/f1.txt")))
        self.assertTrue(fsutil.is_file(self.temp_path("unarchive/f2.txt")))
        self.assertTrue(fsutil.is_file(self.temp_path("unarchive/f3.txt")))
        self.assertTrue(fsutil.is_file(self.temp_path("unarchive/f4.txt")))
        self.assertTrue(fsutil.is_file(self.temp_path("unarchive/y/z/f5.txt")))
        self.assertTrue(fsutil.is_file(self.temp_path("unarchive/y/z/f6.txt")))
        self.assertTrue(fsutil.is_file(zip_path))

    def test_extract_zip_file_with_autodelete(self):
        zip_path = self.temp_path("archive.zip")
        unzip_path = self.temp_path("unarchive/")
        path = self.temp_path("f1.txt")
        fsutil.create_file(path, content="hello world 1")
        fsutil.create_zip_file(zip_path, [path])
        fsutil.extract_zip_file(zip_path, unzip_path, autodelete=True)
        self.assertTrue(fsutil.is_dir(unzip_path))
        self.assertTrue(fsutil.is_file(self.temp_path("unarchive/f1.txt")))
        self.assertFalse(fsutil.is_file(zip_path))

    def test_extract_tar_file(self):
        tar_path = self.temp_path("archive.tar")
        untar_path = self.temp_path("unarchive/")
        f1_path = self.temp_path("a/b/f1.txt")
        f2_path = self.temp_path("a/b/f2.txt")
        f3_path = self.temp_path("j/k/f3.txt")
        f4_path = self.temp_path("j/k/f4.txt")
        f5_path = self.temp_path("x/y/z/f5.txt")
        f6_path = self.temp_path("x/y/z/f6.txt")
        f5_f6_dir = self.temp_path("x")
        fsutil.create_file(f1_path, content="hello world 1")
        fsutil.create_file(f2_path, content="hello world 2")
        fsutil.create_file(f3_path, content="hello world 3")
        fsutil.create_file(f4_path, content="hello world 4")
        fsutil.create_file(f5_path, content="hello world 5")
        fsutil.create_file(f6_path, content="hello world 6")
        fsutil.create_tar_file(
            tar_path, [f1_path, f2_path, f3_path, f4_path, f5_f6_dir]
        )
        fsutil.extract_tar_file(tar_path, untar_path)
        self.assertTrue(fsutil.is_dir(untar_path))
        self.assertTrue(fsutil.is_file(self.temp_path("unarchive/f1.txt")))
        self.assertTrue(fsutil.is_file(self.temp_path("unarchive/f2.txt")))
        self.assertTrue(fsutil.is_file(self.temp_path("unarchive/f3.txt")))
        self.assertTrue(fsutil.is_file(self.temp_path("unarchive/f4.txt")))
        self.assertTrue(fsutil.is_file(self.temp_path("unarchive/y/z/f5.txt")))
        self.assertTrue(fsutil.is_file(self.temp_path("unarchive/y/z/f6.txt")))
        self.assertTrue(fsutil.is_file(tar_path))

    def test_extract_tar_file_with_autodelete(self):
        tar_path = self.temp_path("archive.tar")
        untar_path = self.temp_path("unarchive/")
        path = self.temp_path("f1.txt")
        fsutil.create_file(path, content="hello world 1")
        fsutil.create_tar_file(tar_path, [path])
        fsutil.extract_tar_file(tar_path, untar_path, autodelete=True)
        self.assertTrue(fsutil.is_dir(untar_path))
        self.assertTrue(fsutil.is_file(self.temp_path("unarchive/f1.txt")))
        self.assertFalse(fsutil.is_file(tar_path))

    def test_get_dir_creation_date(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path, content="Hello World")
        creation_date = fsutil.get_dir_creation_date(self.temp_path("a/b"))
        now = datetime.now()
        self.assertTrue((now - creation_date) < timedelta(seconds=0.1))
        time.sleep(0.2)
        creation_date = fsutil.get_dir_creation_date(self.temp_path("a/b"))
        now = datetime.now()
        self.assertFalse((now - creation_date) < timedelta(seconds=0.1))

    def test_get_dir_creation_date_formatted(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path, content="Hello World")
        creation_date_str = fsutil.get_dir_creation_date_formatted(
            self.temp_path("a/b"), format="%Y/%m/%d"
        )
        creation_date_re = re.compile(r"^[\d]{4}\/[\d]{2}\/[\d]{2}$")
        self.assertTrue(creation_date_re.match(creation_date_str))

    def test_get_dir_hash(self):
        f1_path = self.temp_path("x/a/b/f1.txt")
        f2_path = self.temp_path("x/a/b/f2.txt")
        f3_path = self.temp_path("x/j/k/f3.txt")
        f4_path = self.temp_path("x/j/k/f4.txt")
        f5_path = self.temp_path("x/y/z/f5.txt")
        f6_path = self.temp_path("x/y/z/f6.txt")
        fsutil.create_file(f1_path, content="hello world 1")
        fsutil.create_file(f2_path, content="hello world 2")
        fsutil.create_file(f3_path, content="hello world 3")
        fsutil.create_file(f4_path, content="hello world 4")
        fsutil.create_file(f5_path, content="hello world 5")
        fsutil.create_file(f6_path, content="hello world 6")
        hash = fsutil.get_dir_hash(self.temp_path("x/"))
        self.assertEqual(hash, "eabe619c41f0c4611b7b9746bededfcb")

    def test_get_dir_last_modified_date(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path, content="Hello")
        creation_date = fsutil.get_dir_creation_date(self.temp_path("a"))
        time.sleep(0.2)
        fsutil.write_file(path, content="Goodbye", append=True)
        now = datetime.now()
        lastmod_date = fsutil.get_dir_last_modified_date(self.temp_path("a"))
        self.assertTrue((now - lastmod_date) < timedelta(seconds=0.1))
        self.assertTrue((lastmod_date - creation_date) > timedelta(seconds=0.15))

    def test_get_dir_last_modified_date_formatted(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path, content="Hello World")
        lastmod_date_str = fsutil.get_dir_last_modified_date_formatted(
            self.temp_path("a")
        )
        lastmod_date_re = re.compile(
            r"^[\d]{4}\-[\d]{2}\-[\d]{2}[\s]{1}[\d]{2}\:[\d]{2}\:[\d]{2}$"
        )
        self.assertTrue(lastmod_date_re.match(lastmod_date_str))

    def test_get_dir_size(self):
        self.temp_file_of_size(self.temp_path("a/a-1.txt"), "1.05 MB")  # 1101004
        self.temp_file_of_size(self.temp_path("a/b/b-1.txt"), "2 MB")  # 2097152
        self.temp_file_of_size(self.temp_path("a/b/b-2.txt"), "2.25 MB")  # 2359296
        self.temp_file_of_size(self.temp_path("a/b/c/c-1.txt"), "3.75 MB")  # 3932160
        self.temp_file_of_size(self.temp_path("a/b/c/c-2.txt"), "500 KB")  # 512000
        self.temp_file_of_size(self.temp_path("a/b/c/c-3.txt"), "200 KB")  # 204800
        self.assertEqual(fsutil.get_dir_size(self.temp_path("a")), 10206412)
        self.assertEqual(fsutil.get_dir_size(self.temp_path("a/b")), 9105408)
        self.assertEqual(fsutil.get_dir_size(self.temp_path("a/b/c")), 4648960)

    def test_get_dir_size_formatted(self):
        self.temp_file_of_size(self.temp_path("a/a-1.txt"), "1.05 MB")  # 1101004
        self.temp_file_of_size(self.temp_path("a/b/b-1.txt"), "2 MB")  # 2097152
        self.temp_file_of_size(self.temp_path("a/b/b-2.txt"), "2.25 MB")  # 2359296
        self.temp_file_of_size(self.temp_path("a/b/c/c-1.txt"), "3.75 MB")  # 3932160
        self.temp_file_of_size(self.temp_path("a/b/c/c-2.txt"), "500 KB")  # 512000
        self.temp_file_of_size(self.temp_path("a/b/c/c-3.txt"), "200 KB")  # 204800
        self.assertEqual(fsutil.get_dir_size_formatted(self.temp_path("a")), "9.73 MB")
        self.assertEqual(
            fsutil.get_dir_size_formatted(self.temp_path("a/b")), "8.68 MB"
        )
        self.assertEqual(
            fsutil.get_dir_size_formatted(self.temp_path("a/b/c")), "4.43 MB"
        )

    def test_get_file_basename(self):
        s = "Document"
        self.assertEqual(fsutil.get_file_basename(s), "Document")
        s = "Document.txt"
        self.assertEqual(fsutil.get_file_basename(s), "Document")
        s = ".Document.txt"
        self.assertEqual(fsutil.get_file_basename(s), ".Document")
        s = "/root/a/b/c/Document.txt"
        self.assertEqual(fsutil.get_file_basename(s), "Document")
        s = "https://domain-name.com/Document.txt?p=1"
        self.assertEqual(fsutil.get_file_basename(s), "Document")

    def test_get_file_creation_date(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path, content="Hello World")
        creation_date = fsutil.get_file_creation_date(path)
        now = datetime.now()
        self.assertTrue((now - creation_date) < timedelta(seconds=0.1))
        time.sleep(0.2)
        creation_date = fsutil.get_file_creation_date(path)
        now = datetime.now()
        self.assertFalse((now - creation_date) < timedelta(seconds=0.1))

    def test_get_file_creation_date_formatted(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path, content="Hello World")
        creation_date_str = fsutil.get_file_creation_date_formatted(
            path, format="%Y/%m/%d"
        )
        creation_date_re = re.compile(r"^[\d]{4}\/[\d]{2}\/[\d]{2}$")
        self.assertTrue(creation_date_re.match(creation_date_str))

    def test_get_file_extension(self):
        s = "Document"
        self.assertEqual(fsutil.get_file_extension(s), "")
        s = "Document.txt"
        self.assertEqual(fsutil.get_file_extension(s), "txt")
        s = ".Document.txt"
        self.assertEqual(fsutil.get_file_extension(s), "txt")
        s = "/root/a/b/c/Document.txt"
        self.assertEqual(fsutil.get_file_extension(s), "txt")
        s = "https://domain-name.com/Document.txt?p=1"
        self.assertEqual(fsutil.get_file_extension(s), "txt")

    def test_get_file_hash(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path, content="Hello World")
        hash = fsutil.get_file_hash(path)
        self.assertEqual(hash, "b10a8db164e0754105b7a99be72e3fe5")

    def test_get_file_last_modified_date(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path, content="Hello")
        creation_date = fsutil.get_file_creation_date(path)
        time.sleep(0.2)
        fsutil.write_file(path, content="Goodbye", append=True)
        now = datetime.now()
        lastmod_date = fsutil.get_file_last_modified_date(path)
        self.assertTrue((now - lastmod_date) < timedelta(seconds=0.1))
        self.assertTrue((lastmod_date - creation_date) > timedelta(seconds=0.15))

    def test_get_file_last_modified_date_formatted(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path, content="Hello World")
        lastmod_date_str = fsutil.get_file_last_modified_date_formatted(path)
        lastmod_date_re = re.compile(
            r"^[\d]{4}\-[\d]{2}\-[\d]{2}[\s]{1}[\d]{2}\:[\d]{2}\:[\d]{2}$"
        )
        self.assertTrue(lastmod_date_re.match(lastmod_date_str))

    def test_get_file_size(self):
        path = self.temp_path("a/b/c.txt")
        self.temp_file_of_size(path, "1.75 MB")
        size = fsutil.get_file_size(path)
        self.assertEqual(size, fsutil.convert_size_string_to_bytes("1.75 MB"))

    def test_get_file_size_formatted(self):
        path = self.temp_path("a/b/c.txt")
        self.temp_file_of_size(path, "1.75 MB")
        size = fsutil.get_file_size_formatted(path)
        self.assertEqual(size, "1.75 MB")

    def test_get_filename(self):
        s = "Document"
        self.assertEqual(fsutil.get_filename(s), "Document")
        s = "Document.txt"
        self.assertEqual(fsutil.get_filename(s), "Document.txt")
        s = ".Document.txt"
        self.assertEqual(fsutil.get_filename(s), ".Document.txt")
        s = "/root/a/b/c/Document.txt"
        self.assertEqual(fsutil.get_filename(s), "Document.txt")
        s = "https://domain-name.com/Document.txt?p=1"
        self.assertEqual(fsutil.get_filename(s), "Document.txt")

    def test_get_parent_dir(self):
        s = "/root/a/b/c/Document.txt"
        self.assertEqual(fsutil.get_parent_dir(s), "/root/a/b/c")
        s = "/root/a/b/c/Document.txt"
        self.assertEqual(fsutil.get_parent_dir(s, levels=0), "/root/a/b/c")
        s = "/root/a/b/c/Document.txt"
        self.assertEqual(fsutil.get_parent_dir(s, levels=1), "/root/a/b/c")
        s = "/root/a/b/c/Document.txt"
        self.assertEqual(fsutil.get_parent_dir(s, levels=2), "/root/a/b")
        s = "/root/a/b/c/Document.txt"
        self.assertEqual(fsutil.get_parent_dir(s, levels=3), "/root/a")
        s = "/root/a/b/c/Document.txt"
        self.assertEqual(fsutil.get_parent_dir(s, levels=4), "/root")
        s = "/root/a/b/c/Document.txt"
        self.assertEqual(fsutil.get_parent_dir(s, levels=5), "/")
        s = "/root/a/b/c/Document.txt"
        self.assertEqual(fsutil.get_parent_dir(s, levels=6), "/")

    def test_get_unique_name(self):
        path = self.temp_path("a/b/c")
        fsutil.create_dir(path)
        name = fsutil.get_unique_name(
            path,
            prefix="custom-prefix",
            suffix="custom-suffix",
            extension="txt",
            separator="_",
        )
        basename, extension = fsutil.split_filename(name)
        self.assertTrue(basename.startswith("custom-prefix_"))
        self.assertTrue(basename.endswith("_custom-suffix"))
        self.assertEqual(extension, "txt")

    def test_is_dir(self):
        path = self.temp_path("a/b/")
        self.assertFalse(fsutil.is_dir(path))
        fsutil.create_dir(path)
        self.assertTrue(fsutil.is_dir(path))
        path = self.temp_path("a/b/c.txt")
        self.assertFalse(fsutil.is_dir(path))
        fsutil.create_file(path)
        self.assertFalse(fsutil.is_dir(path))

    def test_is_empty(self):
        fsutil.create_file(self.temp_path("a/b/c.txt"))
        fsutil.create_file(self.temp_path("a/b/d.txt"), content="1")
        fsutil.create_dir(self.temp_path("a/b/e"))
        self.assertTrue(fsutil.is_empty(self.temp_path("a/b/c.txt")))
        self.assertFalse(fsutil.is_empty(self.temp_path("a/b/d.txt")))
        self.assertTrue(fsutil.is_empty(self.temp_path("a/b/e")))
        self.assertFalse(fsutil.is_empty(self.temp_path("a/b")))

    def test_is_empty_dir(self):
        path = self.temp_path("a/b/")
        fsutil.create_dir(path)
        self.assertTrue(fsutil.is_empty_dir(path))
        filepath = self.temp_path("a/b/c.txt")
        fsutil.create_file(filepath)
        self.assertTrue(fsutil.is_file(filepath))
        self.assertFalse(fsutil.is_empty_dir(path))

    def test_is_empty_file(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path)
        self.assertTrue(fsutil.is_empty_file(path))
        path = self.temp_path("a/b/d.txt")
        fsutil.create_file(path, content="hello world")
        self.assertFalse(fsutil.is_empty_file(path))

    def test_is_file(self):
        path = self.temp_path("a/b/c.txt")
        self.assertFalse(fsutil.is_file(path))
        fsutil.create_file(path)
        self.assertTrue(fsutil.is_file(path))

    def test_join_filename(self):
        self.assertEqual(fsutil.join_filename("Document", "txt"), "Document.txt")
        self.assertEqual(fsutil.join_filename("Document", ".txt"), "Document.txt")
        self.assertEqual(fsutil.join_filename(" Document ", " txt "), "Document.txt")
        self.assertEqual(fsutil.join_filename("Document", " .txt "), "Document.txt")

    def test_join_filepath(self):
        self.assertEqual(
            fsutil.join_filepath("a/b/c", "Document.txt"), "a/b/c/Document.txt"
        )

    def test_join_path_with_absolute_path(self):
        self.assertEqual(
            fsutil.join_path("/a/b/c/", "/document.txt"), "/a/b/c/document.txt"
        )

    def test_join_path_with_parent_dirs(self):
        self.assertEqual(
            fsutil.join_path("/a/b/c/", "../../document.txt"), "/a/document.txt"
        )

    def test_list_dirs(self):
        for i in range(0, 5):
            fsutil.create_dir(self.temp_path(f"a/b/c/d-{i}"))
            fsutil.create_file(self.temp_path(f"a/b/c/f-{i}"), content=f"{i}")
        dirpaths = fsutil.list_dirs(self.temp_path("a/b/c"))
        dirnames = [fsutil.split_path(dirpath)[-1] for dirpath in dirpaths]
        self.assertEqual(len(dirpaths), 5)
        self.assertEqual(dirnames, ["d-0", "d-1", "d-2", "d-3", "d-4"])

    def test_list_files(self):
        for i in range(0, 5):
            fsutil.create_dir(self.temp_path(f"a/b/c/d-{i}"))
            fsutil.create_file(self.temp_path(f"a/b/c/f-{i}.txt"), content=f"{i}")
        filepaths = fsutil.list_files(self.temp_path("a/b/c"))
        filenames = [fsutil.get_filename(filepath) for filepath in filepaths]
        self.assertEqual(len(filepaths), 5)
        self.assertEqual(
            filenames, ["f-0.txt", "f-1.txt", "f-2.txt", "f-3.txt", "f-4.txt"]
        )

    def test_make_dirs(self):
        path = self.temp_path("a/b/c/")
        fsutil.make_dirs(path)
        self.assertTrue(fsutil.is_dir(path))

    def test_make_dirs_race_condition(self):
        path = self.temp_path("a/b/c/")
        for _ in range(0, 20):
            t = threading.Thread(target=fsutil.make_dirs, args=[path], kwargs={})
            t.start()
        t.join()
        self.assertTrue(fsutil.is_dir(path))

    def test_make_dirs_with_existing_dir(self):
        path = self.temp_path("a/b/c/")
        fsutil.create_dir(path)
        fsutil.make_dirs(path)
        self.assertTrue(fsutil.is_dir(path))

    def test_make_dirs_with_existing_file(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path)
        with self.assertRaises(OSError):
            fsutil.make_dirs(path)

    def test_make_dirs_for_file(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.make_dirs_for_file(path)
        self.assertTrue(fsutil.is_dir(self.temp_path("a/b/")))
        self.assertFalse(fsutil.is_dir(path))
        self.assertFalse(fsutil.is_file(path))

    def test_make_dirs_for_file_with_existing_file(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path)
        fsutil.make_dirs_for_file(path)
        self.assertTrue(fsutil.is_dir(self.temp_path("a/b/")))
        self.assertFalse(fsutil.is_dir(path))
        self.assertTrue(fsutil.is_file(path))

    def test_make_dirs_for_file_with_existing_dir(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_dir(path)
        with self.assertRaises(OSError):
            fsutil.make_dirs_for_file(path)

    def test_make_dirs_for_file_with_filename_only(self):
        path = "document.txt"
        fsutil.make_dirs_for_file(path)
        self.assertFalse(fsutil.is_file(path))

    def test_move_dir(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path, content="Hello World")
        fsutil.move_dir(self.temp_path("a/b"), self.temp_path("x/y"))
        self.assertFalse(fsutil.exists(path))
        self.assertTrue(fsutil.is_file(self.temp_path("x/y/b/c.txt")))

    def test_move_file(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path, content="Hello World")
        dest = self.temp_path("a")
        fsutil.move_file(path, dest)
        self.assertFalse(fsutil.exists(path))
        self.assertTrue(fsutil.is_file(self.temp_path("a/c.txt")))

    def test_read_file(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.write_file(path, content="Hello World")
        self.assertEqual(fsutil.read_file(path), "Hello World")

    def test_read_file_from_url(self):
        url = "https://raw.githubusercontent.com/fabiocaccamo/python-fsutil/main/README.md"
        content = fsutil.read_file_from_url(url)
        self.assertTrue("python-fsutil" in content)

    def test_read_file_json(self):
        path = self.temp_path("a/b/c.json")
        now = datetime.now()
        data = {
            "test": "Hello World",
            "test_datetime": now,
            "test_set": {1, 2, 3},
        }
        fsutil.write_file_json(self.temp_path("a/b/c.json"), data=data)
        expected_data = data.copy()
        expected_data["test_datetime"] = now.isoformat()
        expected_data["test_set"] = list(expected_data["test_set"])
        self.assertEqual(fsutil.read_file_json(path), expected_data)

    def test_read_file_lines(self):
        path = self.temp_path("a/b/c.txt")
        lines = ["", "1 ", " 2", "", "", " 3 ", "  4  ", "", "", "5"]
        fsutil.write_file(path, content="\n".join(lines))

        expected_lines = list(lines)
        lines = fsutil.read_file_lines(path, strip_white=False, skip_empty=False)
        self.assertEqual(lines, expected_lines)

        expected_lines = ["", "1", "2", "", "", "3", "4", "", "", "5"]
        lines = fsutil.read_file_lines(path, strip_white=True, skip_empty=False)
        self.assertEqual(lines, expected_lines)

        expected_lines = ["1 ", " 2", " 3 ", "  4  ", "5"]
        lines = fsutil.read_file_lines(path, strip_white=False, skip_empty=True)
        self.assertEqual(lines, expected_lines)

        expected_lines = ["1", "2", "3", "4", "5"]
        lines = fsutil.read_file_lines(path, strip_white=True, skip_empty=True)
        self.assertEqual(lines, expected_lines)

    def test_read_file_lines_with_lines_range(self):
        path = self.temp_path("a/b/c.txt")
        lines = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        fsutil.write_file(path, content="\n".join(lines))

        # single line
        expected_lines = ["1"]
        lines = fsutil.read_file_lines(path, line_start=1, line_end=1)
        self.assertEqual(lines, expected_lines)

        # multiple lines
        expected_lines = ["1", "2", "3"]
        lines = fsutil.read_file_lines(path, line_start=1, line_end=3)
        self.assertEqual(lines, expected_lines)

        # multiple lines not stripped
        expected_lines = ["1\n", "2\n", "3\n"]
        lines = fsutil.read_file_lines(
            path, line_start=1, line_end=3, strip_white=False, skip_empty=False
        )
        self.assertEqual(lines, expected_lines)

        # last line
        expected_lines = ["9"]
        lines = fsutil.read_file_lines(path, line_start=-1)
        self.assertEqual(lines, expected_lines)

        # last 3 lines
        expected_lines = ["7", "8", "9"]
        lines = fsutil.read_file_lines(path, line_start=-3)
        self.assertEqual(lines, expected_lines)

        # empty file
        fsutil.write_file(path, content="")
        expected_lines = []
        lines = fsutil.read_file_lines(path, line_start=-2)
        self.assertEqual(lines, expected_lines)

    def test_read_file_lines_count(self):
        path = self.temp_path("a/b/c.txt")
        lines = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        fsutil.write_file(path, content="\n".join(lines))

        lines_count = fsutil.read_file_lines_count(path)
        self.assertEqual(lines_count, 10)

    def test_rename_dir(self):
        path = self.temp_path("a/b/c")
        fsutil.make_dirs(path)
        fsutil.rename_dir(path, "d")
        self.assertFalse(fsutil.exists(path))
        path = self.temp_path("a/b/d")
        self.assertTrue(fsutil.exists(path))

    def test_rename_dir_with_existing_name(self):
        path = self.temp_path("a/b/c")
        fsutil.make_dirs(path)
        fsutil.make_dirs(self.temp_path("a/b/d"))
        with self.assertRaises(OSError):
            fsutil.rename_dir(path, "d")

    def test_rename_file(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path)
        fsutil.rename_file(path, "d.txt.backup")
        self.assertFalse(fsutil.exists(path))
        path = self.temp_path("a/b/d.txt.backup")
        self.assertTrue(fsutil.exists(path))

    def test_rename_file_with_existing_name(self):
        path = self.temp_path("a/b/c")
        fsutil.create_file(path)
        path = self.temp_path("a/b/d")
        fsutil.create_file(path)
        with self.assertRaises(OSError):
            fsutil.rename_file(path, "c")

    def test_rename_file_basename(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path)
        fsutil.rename_file_basename(path, "d")
        self.assertFalse(fsutil.exists(path))
        path = self.temp_path("a/b/d.txt")
        self.assertTrue(fsutil.exists(path))

    def test_rename_file_extension(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(path)
        fsutil.rename_file_extension(path, "json")
        self.assertFalse(fsutil.exists(path))
        path = self.temp_path("a/b/c.json")
        self.assertTrue(fsutil.exists(path))

    def test_remove_dir(self):
        fsutil.create_file(self.temp_path("a/b/c/d.txt"))
        fsutil.create_file(self.temp_path("a/b/c/e.txt"))
        fsutil.create_file(self.temp_path("a/b/c/f.txt"))
        removed = fsutil.remove_dir(self.temp_path("a/c/"))
        self.assertFalse(removed)
        removed = fsutil.remove_dir(self.temp_path("a/b/"))
        self.assertTrue(removed)
        self.assertTrue(fsutil.exists(self.temp_path("a")))
        self.assertFalse(fsutil.exists(self.temp_path("a/b")))

    def test_remove_dir_content(self):
        fsutil.create_file(self.temp_path("a/b/c/d.txt"))
        fsutil.create_file(self.temp_path("a/b/e.txt"))
        fsutil.create_file(self.temp_path("a/b/f.txt"))
        path = self.temp_path("a/b/")
        fsutil.remove_dir_content(path)
        self.assertTrue(fsutil.is_empty_dir(path))

    def test_remove_dirs(self):
        fsutil.create_file(self.temp_path("a/b/c/document.txt"))
        fsutil.create_file(self.temp_path("a/b/d/document.txt"))
        fsutil.create_file(self.temp_path("a/b/e/document.txt"))
        fsutil.create_file(self.temp_path("a/b/f/document.txt"))
        path1 = self.temp_path("a/b/c/")
        path2 = self.temp_path("a/b/d/")
        path3 = self.temp_path("a/b/e/")
        path4 = self.temp_path("a/b/f/")
        self.assertTrue(fsutil.exists(path1))
        self.assertTrue(fsutil.exists(path2))
        self.assertTrue(fsutil.exists(path3))
        self.assertTrue(fsutil.exists(path4))
        fsutil.remove_dirs(path1, path2, path3, path4)
        self.assertFalse(fsutil.exists(path1))
        self.assertFalse(fsutil.exists(path2))
        self.assertFalse(fsutil.exists(path3))
        self.assertFalse(fsutil.exists(path4))

    def test_remove_file(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.create_file(self.temp_path("a/b/c.txt"))
        self.assertTrue(fsutil.exists(path))
        removed = fsutil.remove_file(self.temp_path("a/b/d.txt"))
        self.assertFalse(removed)
        removed = fsutil.remove_file(path)
        self.assertTrue(removed)
        self.assertFalse(fsutil.exists(path))

    def test_remove_files(self):
        path1 = self.temp_path("a/b/c/document.txt")
        path2 = self.temp_path("a/b/d/document.txt")
        path3 = self.temp_path("a/b/e/document.txt")
        path4 = self.temp_path("a/b/f/document.txt")
        fsutil.create_file(path1)
        fsutil.create_file(path2)
        fsutil.create_file(path3)
        fsutil.create_file(path4)
        self.assertTrue(fsutil.exists(path1))
        self.assertTrue(fsutil.exists(path2))
        self.assertTrue(fsutil.exists(path3))
        self.assertTrue(fsutil.exists(path4))
        fsutil.remove_files(path1, path2, path3, path4)
        self.assertFalse(fsutil.exists(path1))
        self.assertFalse(fsutil.exists(path2))
        self.assertFalse(fsutil.exists(path3))
        self.assertFalse(fsutil.exists(path4))

    def test_replace_file(self):
        dest = self.temp_path("a/b/c.txt")
        src = self.temp_path("d/e/f.txt")
        fsutil.create_file(dest, "old")
        fsutil.create_file(src, "new")
        fsutil.replace_file(dest, src)
        content = fsutil.read_file(dest)
        self.assertEqual(content, "new")
        self.assertTrue(fsutil.exists(src))

    def test_replace_file_with_autodelete(self):
        dest_file = self.temp_path("a/b/c.txt")
        src_file = self.temp_path("d/e/f.txt")
        fsutil.create_file(dest_file, "old")
        fsutil.create_file(src_file, "new")
        fsutil.replace_file(dest_file, src_file, autodelete=True)
        content = fsutil.read_file(dest_file)
        self.assertEqual(content, "new")
        self.assertFalse(fsutil.exists(src_file))

    def test_replace_dir(self):
        dest_dir = self.temp_path("a/b/")
        dest_file = self.temp_path("a/b/c.txt")
        src_dir = self.temp_path("d/e/")
        src_file = self.temp_path("d/e/f.txt")
        fsutil.create_file(dest_file, "old")
        fsutil.create_file(src_file, "new")
        fsutil.replace_dir(dest_dir, src_dir)
        content = fsutil.read_file(self.temp_path("a/b/f.txt"))
        self.assertEqual(content, "new")
        self.assertTrue(fsutil.exists(src_dir))

    def test_replace_dir_with_autodelete(self):
        dest_dir = self.temp_path("a/b/")
        dest_file = self.temp_path("a/b/c.txt")
        src_dir = self.temp_path("d/e/")
        src_file = self.temp_path("d/e/f.txt")
        fsutil.create_file(dest_file, "old")
        fsutil.create_file(src_file, "new")
        fsutil.replace_dir(dest_dir, src_dir, autodelete=True)
        content = fsutil.read_file(self.temp_path("a/b/f.txt"))
        self.assertEqual(content, "new")
        self.assertFalse(fsutil.exists(src_dir))

    def test_search_files(self):
        fsutil.create_file(self.temp_path("a/b/c/IMG_1000.jpg"))
        fsutil.create_file(self.temp_path("a/b/c/IMG_1001.jpg"))
        fsutil.create_file(self.temp_path("a/b/c/IMG_1002.png"))
        fsutil.create_file(self.temp_path("a/b/c/IMG_1003.jpg"))
        fsutil.create_file(self.temp_path("a/b/c/IMG_1004.jpg"))
        fsutil.create_file(self.temp_path("a/x/c/IMG_1005.png"))
        fsutil.create_file(self.temp_path("x/b/c/IMG_1006.png"))
        fsutil.create_file(self.temp_path("a/b/c/DOC_1007.png"))
        results = fsutil.search_files(self.temp_path("a/"), "**/c/IMG_*.png")
        expected_results = [
            self.temp_path("a/b/c/IMG_1002.png"),
            self.temp_path("a/x/c/IMG_1005.png"),
        ]
        self.assertEqual(results, expected_results)

    def test_search_dirs(self):
        fsutil.create_file(self.temp_path("a/b/c/IMG_1000.jpg"))
        fsutil.create_file(self.temp_path("x/y/z/c/IMG_1001.jpg"))
        fsutil.create_file(self.temp_path("a/c/IMG_1002.png"))
        fsutil.create_file(self.temp_path("c/b/c/IMG_1003.jpg"))
        results = fsutil.search_dirs(self.temp_path(""), "**/c")
        expected_results = [
            self.temp_path("a/b/c"),
            self.temp_path("a/c"),
            self.temp_path("c"),
            self.temp_path("c/b/c"),
            self.temp_path("x/y/z/c"),
        ]
        self.assertEqual(results, expected_results)

    def test_split_filename(self):
        s = "Document"
        self.assertEqual(fsutil.split_filename(s), ("Document", ""))
        s = ".Document"
        self.assertEqual(fsutil.split_filename(s), (".Document", ""))
        s = "Document.txt"
        self.assertEqual(fsutil.split_filename(s), ("Document", "txt"))
        s = ".Document.txt"
        self.assertEqual(fsutil.split_filename(s), (".Document", "txt"))
        s = "/root/a/b/c/Document.txt"
        self.assertEqual(fsutil.split_filename(s), ("Document", "txt"))
        s = "https://domain-name.com/Document.txt?p=1"
        self.assertEqual(fsutil.split_filename(s), ("Document", "txt"))

    def test_split_filepath(self):
        s = "/root/a/b/c/Document.txt"
        self.assertEqual(fsutil.split_filepath(s), ("/root/a/b/c", "Document.txt"))

    def test_split_filepath_with_filename_only(self):
        s = "Document.txt"
        self.assertEqual(fsutil.split_filepath(s), ("", "Document.txt"))

    def test_split_path(self):
        s = "/root/a/b/c/Document.txt"
        self.assertEqual(fsutil.split_path(s), ["root", "a", "b", "c", "Document.txt"])

    def test_write_file(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.write_file(self.temp_path("a/b/c.txt"), content="Hello World")
        self.assertEqual(fsutil.read_file(path), "Hello World")
        fsutil.write_file(self.temp_path("a/b/c.txt"), content="Hello Jupiter")
        self.assertEqual(fsutil.read_file(path), "Hello Jupiter")

    def test_write_file_atomic(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.write_file(
            self.temp_path("a/b/c.txt"), content="Hello World", atomic=True
        )
        self.assertEqual(fsutil.read_file(path), "Hello World")
        fsutil.write_file(
            self.temp_path("a/b/c.txt"), content="Hello Jupiter", atomic=True
        )
        self.assertEqual(fsutil.read_file(path), "Hello Jupiter")

    def test_write_file_with_filename_only(self):
        path = "document.txt"
        fsutil.write_file(path, content="Hello World")
        self.assertTrue(fsutil.is_file(path))
        # cleanup
        fsutil.remove_file(path)

    def test_write_file_json(self):
        path = self.temp_path("a/b/c.json")
        now = datetime.now()
        dec = Decimal("3.33")
        data = {
            "test": "Hello World",
            "test_datetime": now,
            "test_decimal": dec,
        }
        fsutil.write_file_json(self.temp_path("a/b/c.json"), data=data)
        self.assertEqual(
            fsutil.read_file(path),
            (
                "{"
                f'"test": "Hello World", '
                f'"test_datetime": "{now.isoformat()}", '
                f'"test_decimal": "{dec}"'
                "}"
            ),
        )

    def test_write_file_json_atomic(self):
        path = self.temp_path("a/b/c.json")
        now = datetime.now()
        dec = Decimal("3.33")
        data = {
            "test": "Hello World",
            "test_datetime": now,
            "test_decimal": dec,
        }
        fsutil.write_file_json(self.temp_path("a/b/c.json"), data=data, atomic=True)
        self.assertEqual(
            fsutil.read_file(path),
            (
                "{"
                f'"test": "Hello World", '
                f'"test_datetime": "{now.isoformat()}", '
                f'"test_decimal": "{dec}"'
                "}"
            ),
        )

    def test_write_file_with_append(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.write_file(self.temp_path("a/b/c.txt"), content="Hello World")
        self.assertEqual(fsutil.read_file(path), "Hello World")
        fsutil.write_file(
            self.temp_path("a/b/c.txt"), content=" - Hello Sun", append=True
        )
        self.assertEqual(fsutil.read_file(path), "Hello World - Hello Sun")

    def test_write_file_with_append_atomic(self):
        path = self.temp_path("a/b/c.txt")
        fsutil.write_file(
            self.temp_path("a/b/c.txt"), content="Hello World", atomic=True
        )
        self.assertEqual(fsutil.read_file(path), "Hello World")
        fsutil.write_file(
            self.temp_path("a/b/c.txt"),
            content=" - Hello Sun",
            append=True,
            atomic=True,
        )
        self.assertEqual(fsutil.read_file(path), "Hello World - Hello Sun")


if __name__ == "__main__":
    unittest.main()
