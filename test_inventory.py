import unittest
import tempfile
import os

from library_manager.inventory import LibraryInventory
from library_manager.book import Book

class TestInventory(unittest.TestCase):
    def setUp(self):
        # temp file to avoid polluting project
        fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        # start with empty file
        self.inv = LibraryInventory(storage_path=self.path)

    def tearDown(self):
        try:
            os.remove(self.path)
        except OSError:
            pass

    def test_add_and_search(self):
        b = Book(title="Test Game", author="R. Dev", isbn="12345")
        self.inv.add_book(b)
        found = self.inv.search_by_isbn("12345")
        self.assertIsNotNone(found)
        self.assertEqual(found.title, "Test Game")

    def test_issue_and_return(self):
        b = Book(title="Another", author="Author", isbn="54321")
        self.inv.add_book(b)
        book = self.inv.search_by_isbn("54321")
        self.assertTrue(book.is_available())
        self.assertTrue(book.issue())
        self.assertFalse(book.is_available())
        self.assertTrue(book.return_book())
        self.assertTrue(book.is_available())

if __name__ == '__main__':
    unittest.main()
