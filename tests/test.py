# -*- coding: utf-8 -*-

import fsutil
import functools
import unittest


def temp_path(filepath=''):
    return fsutil.get_path(__file__, 'temp/{}'.format(filepath))


def temp_context(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        fsutil.remove_dir(temp_path())
        func(*args, **kwargs)
        fsutil.remove_dir(temp_path())
    return wrapper


class fsutil_test_case(unittest.TestCase):

    @temp_context
    def test_assert_dir(self):
        path = temp_path('a/b/')
        with self.assertRaises(OSError):
            fsutil.assert_dir(path)
        fsutil.create_dir(path)
        fsutil.assert_dir(path)

    @temp_context
    def test_assert_dir_with_file(self):
        path = temp_path('a/b/c.txt')
        fsutil.create_file(path)
        with self.assertRaises(OSError):
            fsutil.assert_dir(path)

    @temp_context
    def test_assert_exists_with_directory(self):
        path = temp_path('a/b/')
        with self.assertRaises(OSError):
            fsutil.assert_exists(path)
        fsutil.create_dir(path)
        fsutil.assert_exists(path)

    @temp_context
    def test_assert_exists_with_file(self):
        path = temp_path('a/b/c.txt')
        with self.assertRaises(OSError):
            fsutil.assert_exists(path)
        fsutil.create_file(path)
        fsutil.assert_exists(path)

    @temp_context
    def test_assert_file(self):
        path = temp_path('a/b/c.txt')
        with self.assertRaises(OSError):
            fsutil.assert_file(path)
        fsutil.create_file(path)
        fsutil.assert_file(path)

    @temp_context
    def test_assert_file_with_directory(self):
        path = temp_path('a/b/c.txt')
        fsutil.create_dir(path)
        with self.assertRaises(OSError):
            fsutil.assert_file(path)

    @temp_context
    def test_copy_file(self):
        path = temp_path('a/b/c.txt')
        fsutil.create_file(path, content='hello world')
        dest = temp_path('x/y/z.txt')
        fsutil.copy_file(path, dest)
        self.assertTrue(fsutil.is_file(path))
        self.assertTrue(fsutil.is_file(dest))
        self.assertEqual(fsutil.get_hash(path), fsutil.get_hash(dest))

    @temp_context
    def test_copy_dir(self):
        fsutil.create_file(temp_path('a/b/f-1.txt'))
        fsutil.create_file(temp_path('a/b/f-2.txt'))
        fsutil.create_file(temp_path('a/b/f-3.txt'))
        fsutil.copy_dir(temp_path('a/b'), temp_path('x/y/z'))
        files = fsutil.list_files(temp_path('a/b'))
        files_names = [file[0] for file in files]
        self.assertEqual(len(files), 3)
        self.assertEqual(files_names, ['f-1.txt', 'f-2.txt', 'f-3.txt'])
        files = fsutil.list_files(temp_path('x/y/z/b/'))
        files_names = [file[0] for file in files]
        self.assertEqual(len(files), 3)
        self.assertEqual(files_names, ['f-1.txt', 'f-2.txt', 'f-3.txt'])

    @temp_context
    def test_copy_dir_with_overwrite(self):
        fsutil.create_file(temp_path('a/b/f-1.txt'))
        fsutil.create_file(temp_path('a/b/f-2.txt'))
        fsutil.create_file(temp_path('a/b/f-3.txt'))
        fsutil.create_file(temp_path('x/y/z/f-0.txt'))
        fsutil.copy_dir(temp_path('a/b'), temp_path('x/y/z'), overwrite=False)
        with self.assertRaises(OSError):
            fsutil.copy_dir(temp_path('a/b'), temp_path('x/y/z'), overwrite=False)
        fsutil.copy_dir(temp_path('a/b'), temp_path('x/y/z'), overwrite=True)

    @temp_context
    def test_copy_dir_content(self):
        fsutil.create_file(temp_path('a/b/f-1.txt'))
        fsutil.create_file(temp_path('a/b/f-2.txt'))
        fsutil.create_file(temp_path('a/b/f-3.txt'))
        fsutil.copy_dir_content(temp_path('a/b'), temp_path('z'))
        files = fsutil.list_files(temp_path('z'))
        files_names = [file[0] for file in files]
        self.assertEqual(len(files), 3)
        self.assertEqual(files_names, ['f-1.txt', 'f-2.txt', 'f-3.txt'])

    @temp_context
    def test_create_file(self):
        path = temp_path('a/b/c.txt')
        self.assertFalse(fsutil.exists(path))
        fsutil.create_file(path, content='hello world')
        self.assertTrue(fsutil.exists(path))
        self.assertTrue(fsutil.is_file(path))
        self.assertEqual(fsutil.read_file(path), 'hello world')

    @temp_context
    def test_create_file_with_overwrite(self):
        path = temp_path('a/b/c.txt')
        fsutil.create_file(path, content='hello world')
        with self.assertRaises(OSError):
            fsutil.create_file(path, content='hello world')
        fsutil.create_file(path, content='hello moon', overwrite=True)
        self.assertEqual(fsutil.read_file(path), 'hello moon')

    @temp_context
    def test_delete_dir(self):
        fsutil.create_file(temp_path('a/b/c/d.txt'))
        fsutil.create_file(temp_path('a/b/c/e.txt'))
        fsutil.create_file(temp_path('a/b/c/f.txt'))
        deleted = fsutil.delete_dir(temp_path('a/c/'))
        self.assertFalse(deleted)
        deleted = fsutil.delete_dir(temp_path('a/b/'))
        self.assertTrue(deleted)
        self.assertTrue(fsutil.exists(temp_path('a')))
        self.assertFalse(fsutil.exists(temp_path('a/b')))

    @temp_context
    def test_delete_dirs(self):
        fsutil.create_file(temp_path('a/b/c/document.txt'))
        fsutil.create_file(temp_path('a/b/d/document.txt'))
        fsutil.create_file(temp_path('a/b/e/document.txt'))
        fsutil.create_file(temp_path('a/b/f/document.txt'))
        path1 = temp_path('a/b/c/')
        path2 = temp_path('a/b/d/')
        path3 = temp_path('a/b/e/')
        path4 = temp_path('a/b/f/')
        self.assertTrue(fsutil.exists(path1))
        self.assertTrue(fsutil.exists(path2))
        self.assertTrue(fsutil.exists(path3))
        self.assertTrue(fsutil.exists(path4))
        fsutil.delete_dirs(path1, path2, path3, path4)
        self.assertFalse(fsutil.exists(path1))
        self.assertFalse(fsutil.exists(path2))
        self.assertFalse(fsutil.exists(path3))
        self.assertFalse(fsutil.exists(path4))

    @temp_context
    def test_delete_file(self):
        path = temp_path('a/b/c.txt')
        fsutil.create_file(temp_path('a/b/c.txt'))
        self.assertTrue(fsutil.exists(path))
        deleted = fsutil.delete_file(temp_path('a/b/d.txt'))
        self.assertFalse(deleted)
        deleted = fsutil.delete_file(path)
        self.assertTrue(deleted)
        self.assertFalse(fsutil.exists(path))

    @temp_context
    def test_delete_files(self):
        path1 = temp_path('a/b/c/document.txt')
        path2 = temp_path('a/b/d/document.txt')
        path3 = temp_path('a/b/e/document.txt')
        path4 = temp_path('a/b/f/document.txt')
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

    @temp_context
    def test_exists(self):
        path = temp_path('a/b/')
        self.assertFalse(fsutil.exists(path))
        fsutil.create_dir(path)
        self.assertTrue(fsutil.exists(path))
        path = temp_path('a/b/c.txt')
        self.assertFalse(fsutil.exists(path))
        fsutil.create_file(path)
        self.assertTrue(fsutil.exists(path))

    def test_get_file_basename(self):
        s = 'Document'
        self.assertEqual(fsutil.get_file_basename(s), 'Document')
        s = 'Document.txt'
        self.assertEqual(fsutil.get_file_basename(s), 'Document')
        s = '.Document.txt'
        self.assertEqual(fsutil.get_file_basename(s), '.Document')
        s = '/root/a/b/c/Document.txt'
        self.assertEqual(fsutil.get_file_basename(s), 'Document')
        s = 'https://domain-name.com/Document.txt?p=1'
        self.assertEqual(fsutil.get_file_basename(s), 'Document')

    def test_get_file_extension(self):
        s = 'Document'
        self.assertEqual(fsutil.get_file_extension(s), '')
        s = 'Document.txt'
        self.assertEqual(fsutil.get_file_extension(s), 'txt')
        s = '.Document.txt'
        self.assertEqual(fsutil.get_file_extension(s), 'txt')
        s = '/root/a/b/c/Document.txt'
        self.assertEqual(fsutil.get_file_extension(s), 'txt')
        s = 'https://domain-name.com/Document.txt?p=1'
        self.assertEqual(fsutil.get_file_extension(s), 'txt')

    def test_get_filename(self):
        s = 'Document'
        self.assertEqual(fsutil.get_filename(s), 'Document')
        s = 'Document.txt'
        self.assertEqual(fsutil.get_filename(s), 'Document.txt')
        s = '.Document.txt'
        self.assertEqual(fsutil.get_filename(s), '.Document.txt')
        s = '/root/a/b/c/Document.txt'
        self.assertEqual(fsutil.get_filename(s), 'Document.txt')
        s = 'https://domain-name.com/Document.txt?p=1'
        self.assertEqual(fsutil.get_filename(s), 'Document.txt')

    @temp_context
    def test_get_hash(self):
        path = temp_path('a/b/c.txt')
        fsutil.create_file(path, content='Hello World')
        hash = fsutil.get_hash(path)
        self.assertEqual(hash, 'b10a8db164e0754105b7a99be72e3fe5')

    @temp_context
    def test_is_dir(self):
        path = temp_path('a/b/')
        self.assertFalse(fsutil.is_dir(path))
        fsutil.create_dir(path)
        self.assertTrue(fsutil.is_dir(path))
        path = temp_path('a/b/c.txt')
        self.assertFalse(fsutil.is_dir(path))
        fsutil.create_file(path)
        self.assertFalse(fsutil.is_dir(path))

    @temp_context
    def test_is_empty(self):
        fsutil.create_file(temp_path('a/b/c.txt'))
        fsutil.create_file(temp_path('a/b/d.txt'), content='1')
        fsutil.create_dir(temp_path('a/b/e'))
        self.assertTrue(fsutil.is_empty(temp_path('a/b/c.txt')))
        self.assertFalse(fsutil.is_empty(temp_path('a/b/d.txt')))
        self.assertTrue(fsutil.is_empty(temp_path('a/b/e')))
        self.assertFalse(fsutil.is_empty(temp_path('a/b')))

    @temp_context
    def test_is_empty_dir(self):
        path = temp_path('a/b/')
        fsutil.create_dir(path)
        self.assertTrue(fsutil.is_empty_dir(path))
        filepath = temp_path('a/b/c.txt')
        fsutil.create_file(filepath)
        self.assertTrue(fsutil.is_file(filepath))
        self.assertFalse(fsutil.is_empty_dir(path))

    @temp_context
    def test_is_empty_file(self):
        path = temp_path('a/b/c.txt')
        fsutil.create_file(path)
        self.assertTrue(fsutil.is_empty_file(path))
        path = temp_path('a/b/d.txt')
        fsutil.create_file(path, content='hello world')
        self.assertFalse(fsutil.is_empty_file(path))

    @temp_context
    def test_is_file(self):
        path = temp_path('a/b/c.txt')
        self.assertFalse(fsutil.is_file(path))
        fsutil.create_file(path)
        self.assertTrue(fsutil.is_file(path))

    def test_join_filename(self):
        self.assertEqual(
            fsutil.join_filename('Document', 'txt'), 'Document.txt')
        self.assertEqual(
            fsutil.join_filename('Document', '.txt'), 'Document.txt')
        self.assertEqual(
            fsutil.join_filename(' Document ', ' txt '), 'Document.txt')
        self.assertEqual(
            fsutil.join_filename('Document', ' .txt '), 'Document.txt')

    def test_join_filepath(self):
        self.assertEqual(fsutil.join_filepath('a/b/c', 'Document.txt'), 'a/b/c/Document.txt')

    @temp_context
    def test_list_dirs(self):
        for i in range(0, 5):
            fsutil.create_dir(temp_path('a/b/c/d-{}'.format(i)))
            fsutil.create_file(temp_path('a/b/c/f-{}'.format(i)), content='{}'.format(i))
        dirs = fsutil.list_dirs(temp_path('a/b/c'))
        dirs_names = [dir[0] for dir in dirs]
        self.assertEqual(len(dirs), 5)
        self.assertEqual(dirs_names, ['d-0', 'd-1', 'd-2', 'd-3', 'd-4'])

    @temp_context
    def test_list_files(self):
        for i in range(0, 5):
            fsutil.create_dir(temp_path('a/b/c/d-{}'.format(i)))
            fsutil.create_file(temp_path('a/b/c/f-{}.txt'.format(i)), content='{}'.format(i))
        files = fsutil.list_files(temp_path('a/b/c'))
        files_names = [file[0] for file in files]
        self.assertEqual(len(files), 5)
        self.assertEqual(files_names, ['f-0.txt', 'f-1.txt', 'f-2.txt', 'f-3.txt', 'f-4.txt'])

    @temp_context
    def test_make_dirs(self):
        path = temp_path('a/b/c/')
        fsutil.make_dirs(path)
        self.assertTrue(fsutil.is_dir(path))

    @temp_context
    def test_make_dirs_with_existing_dir(self):
        path = temp_path('a/b/c/')
        fsutil.create_dir(path)
        fsutil.make_dirs(path)
        self.assertTrue(fsutil.is_dir(path))

    @temp_context
    def test_make_dirs_with_existing_file(self):
        path = temp_path('a/b/c.txt')
        fsutil.create_file(path)
        with self.assertRaises(OSError):
            fsutil.make_dirs(path)

    @temp_context
    def test_make_dirs_for_file(self):
        path = temp_path('a/b/c.txt')
        fsutil.make_dirs_for_file(path)
        self.assertTrue(fsutil.is_dir(temp_path('a/b/')))
        self.assertFalse(fsutil.is_dir(path))
        self.assertFalse(fsutil.is_file(path))

    @temp_context
    def test_make_dirs_for_file_with_existing_file(self):
        path = temp_path('a/b/c.txt')
        fsutil.create_file(path)
        fsutil.make_dirs_for_file(path)
        self.assertTrue(fsutil.is_dir(temp_path('a/b/')))
        self.assertFalse(fsutil.is_dir(path))
        self.assertTrue(fsutil.is_file(path))

    @temp_context
    def test_make_dirs_for_file_with_existing_file(self):
        path = temp_path('a/b/c.txt')
        fsutil.create_dir(path)
        with self.assertRaises(OSError):
            fsutil.make_dirs_for_file(path)

    @temp_context
    def test_move_dir(self):
        path = temp_path('a/b/c.txt')
        fsutil.create_file(path, content='Hello World')
        fsutil.move_dir(temp_path('a/b'), temp_path('x/y'))
        self.assertFalse(fsutil.exists(path))
        self.assertTrue(fsutil.is_file(temp_path('x/y/b/c.txt')))

    @temp_context
    def test_move_file(self):
        path = temp_path('a/b/c.txt')
        fsutil.create_file(path, content='Hello World')
        dest = temp_path('a')
        fsutil.move_file(path, dest)
        self.assertFalse(fsutil.exists(path))
        self.assertTrue(fsutil.is_file(temp_path('a/c.txt')))

    @temp_context
    def test_read_file(self):
        path = temp_path('a/b/c.txt')
        fsutil.write_file(path, content='Hello World')
        self.assertEqual(fsutil.read_file(path), 'Hello World')

    @temp_context
    def test_rename_dir(self):
        path = temp_path('a/b/c')
        fsutil.make_dirs(path)
        fsutil.rename_dir(path, 'd')
        self.assertFalse(fsutil.exists(path))
        path = temp_path('a/b/d')
        self.assertTrue(fsutil.exists(path))

    @temp_context
    def test_rename_dir_with_existing_name(self):
        path = temp_path('a/b/c')
        fsutil.make_dirs(path)
        fsutil.make_dirs(temp_path('a/b/d'))
        with self.assertRaises(OSError):
            fsutil.rename_dir(path, 'd')

    @temp_context
    def test_rename_file(self):
        path = temp_path('a/b/c.txt')
        fsutil.create_file(path)
        fsutil.rename_file(path, 'd.txt.backup')
        self.assertFalse(fsutil.exists(path))
        path = temp_path('a/b/d.txt.backup')
        self.assertTrue(fsutil.exists(path))

    @temp_context
    def test_rename_file_with_existing_name(self):
        path = temp_path('a/b/c')
        fsutil.create_file(path)
        path = temp_path('a/b/d')
        fsutil.create_file(path)
        with self.assertRaises(OSError):
            fsutil.rename_file(path, 'c')

    @temp_context
    def test_rename_file_basename(self):
        path = temp_path('a/b/c.txt')
        fsutil.create_file(path)
        fsutil.rename_file_basename(path, 'd')
        self.assertFalse(fsutil.exists(path))
        path = temp_path('a/b/d.txt')
        self.assertTrue(fsutil.exists(path))

    @temp_context
    def test_rename_file_extension(self):
        path = temp_path('a/b/c.txt')
        fsutil.create_file(path)
        fsutil.rename_file_extension(path, 'json')
        self.assertFalse(fsutil.exists(path))
        path = temp_path('a/b/c.json')
        self.assertTrue(fsutil.exists(path))

    @temp_context
    def test_remove_dir(self):
        fsutil.create_file(temp_path('a/b/c/d.txt'))
        fsutil.create_file(temp_path('a/b/c/e.txt'))
        fsutil.create_file(temp_path('a/b/c/f.txt'))
        removed = fsutil.remove_dir(temp_path('a/c/'))
        self.assertFalse(removed)
        removed = fsutil.remove_dir(temp_path('a/b/'))
        self.assertTrue(removed)
        self.assertTrue(fsutil.exists(temp_path('a')))
        self.assertFalse(fsutil.exists(temp_path('a/b')))

    @temp_context
    def test_remove_dirs(self):
        fsutil.create_file(temp_path('a/b/c/document.txt'))
        fsutil.create_file(temp_path('a/b/d/document.txt'))
        fsutil.create_file(temp_path('a/b/e/document.txt'))
        fsutil.create_file(temp_path('a/b/f/document.txt'))
        path1 = temp_path('a/b/c/')
        path2 = temp_path('a/b/d/')
        path3 = temp_path('a/b/e/')
        path4 = temp_path('a/b/f/')
        self.assertTrue(fsutil.exists(path1))
        self.assertTrue(fsutil.exists(path2))
        self.assertTrue(fsutil.exists(path3))
        self.assertTrue(fsutil.exists(path4))
        fsutil.remove_dirs(path1, path2, path3, path4)
        self.assertFalse(fsutil.exists(path1))
        self.assertFalse(fsutil.exists(path2))
        self.assertFalse(fsutil.exists(path3))
        self.assertFalse(fsutil.exists(path4))

    @temp_context
    def test_remove_file(self):
        path = temp_path('a/b/c.txt')
        fsutil.create_file(temp_path('a/b/c.txt'))
        self.assertTrue(fsutil.exists(path))
        removed = fsutil.remove_file(temp_path('a/b/d.txt'))
        self.assertFalse(removed)
        removed = fsutil.remove_file(path)
        self.assertTrue(removed)
        self.assertFalse(fsutil.exists(path))

    @temp_context
    def test_remove_files(self):
        path1 = temp_path('a/b/c/document.txt')
        path2 = temp_path('a/b/d/document.txt')
        path3 = temp_path('a/b/e/document.txt')
        path4 = temp_path('a/b/f/document.txt')
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

    @temp_context
    def test_search_files(self):
        fsutil.create_file(temp_path('a/b/c/IMG_1000.jpg'))
        fsutil.create_file(temp_path('a/b/c/IMG_1001.jpg'))
        fsutil.create_file(temp_path('a/b/c/IMG_1002.png'))
        fsutil.create_file(temp_path('a/b/c/IMG_1003.jpg'))
        fsutil.create_file(temp_path('a/b/c/IMG_1004.jpg'))
        fsutil.create_file(temp_path('a/x/c/IMG_1005.png'))
        fsutil.create_file(temp_path('x/b/c/IMG_1006.png'))
        fsutil.create_file(temp_path('a/b/c/DOC_1007.png'))
        results_raw = fsutil.search_files(temp_path('a/'), '**/c/IMG_*.png')
        results = [result[0] for result in results_raw]
        expected_results = [
            temp_path('a/b/c/IMG_1002.png'),
            temp_path('a/x/c/IMG_1005.png'),
        ]
        self.assertEqual(results, expected_results)

    @unittest.skipIf(fsutil.PY2, 'In python 2 glob recursive pattern ** was not supported yet.')
    @temp_context
    def test_search_dirs(self):
        fsutil.create_file(temp_path('a/b/c/IMG_1000.jpg'))
        fsutil.create_file(temp_path('x/y/z/c/IMG_1001.jpg'))
        fsutil.create_file(temp_path('a/c/IMG_1002.png'))
        fsutil.create_file(temp_path('c/b/c/IMG_1003.jpg'))
        results = [result[0] for result in fsutil.search_dirs(temp_path(''), '**/c')]
        expected_results = [
            temp_path('a/b/c'),
            temp_path('a/c'),
            temp_path('c'),
            temp_path('c/b/c'),
            temp_path('x/y/z/c'),
        ]
        self.assertEqual(results, expected_results)

    def test_split_filename(self):
        s = 'Document'
        self.assertEqual(fsutil.split_filename(s), ('Document', '', ))
        s = '.Document'
        self.assertEqual(fsutil.split_filename(s), ('.Document', '', ))
        s = 'Document.txt'
        self.assertEqual(fsutil.split_filename(s), ('Document', 'txt', ))
        s = '.Document.txt'
        self.assertEqual(fsutil.split_filename(s), ('.Document', 'txt', ))
        s = '/root/a/b/c/Document.txt'
        self.assertEqual(fsutil.split_filename(s), ('Document', 'txt', ))
        s = 'https://domain-name.com/Document.txt?p=1'
        self.assertEqual(fsutil.split_filename(s), ('Document', 'txt', ))

    def test_split_filepath(self):
        s = '/root/a/b/c/Document.txt'
        self.assertEqual(fsutil.split_filepath(
            s), ('/root/a/b/c', 'Document.txt', ))

    @temp_context
    def test_write_file(self):
        path = temp_path('a/b/c.txt')
        fsutil.write_file(temp_path('a/b/c.txt'), content='Hello World')
        self.assertEqual(fsutil.read_file(path), 'Hello World')
        fsutil.write_file(temp_path('a/b/c.txt'), content='Hello Jupiter')
        self.assertEqual(fsutil.read_file(path), 'Hello Jupiter')

    @temp_context
    def test_write_file_with_append(self):
        path = temp_path('a/b/c.txt')
        fsutil.write_file(temp_path('a/b/c.txt'), content='Hello World')
        self.assertEqual(fsutil.read_file(path), 'Hello World')
        fsutil.write_file(temp_path('a/b/c.txt'), content=' - Hello Sun', append=True)
        self.assertEqual(fsutil.read_file(path), 'Hello World - Hello Sun')


if __name__ == '__main__':
    unittest.main()
