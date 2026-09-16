"""
Unit Tests for Storage Module (Module 2)
"""

import json
import os
import tempfile
import unittest
from library_system.storage import load_books, save_books


class TestStorageModule(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "test_catalog.json")
        self.sample_books = [
            {
                "id": 1,
                "title": "The Pragmatic Programmer",
                "author": "Andrew Hunt, David Thomas",
                "year": 1999,
                "genres": ["Software Engineering"],
                "is_available": True,
            }
        ]

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_books_success(self):
        save_books(self.test_file, self.sample_books)
        loaded = load_books(self.test_file)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["title"], "The Pragmatic Programmer")

    def test_load_books_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_books(os.path.join(self.temp_dir.name, "non_existent.json"))

    def test_load_books_invalid_schema_raises_value_error(self):
        # A dictionary rather than a list should be rejected
        bad_json = os.path.join(self.temp_dir.name, "bad_schema.json")
        with open(bad_json, "w", encoding="utf-8") as f:
            f.write('{"catalog": []}')

        with self.assertRaises(ValueError):
            load_books(bad_json)

    def test_save_books_and_load_roundtrip(self):
        save_books(self.test_file, self.sample_books)
        self.assertTrue(os.path.exists(self.test_file))
        loaded = load_books(self.test_file)
        self.assertEqual(loaded, self.sample_books)

    def test_storage_utf8_encoding(self):
        unicode_books = [
            {
                "id": 10,
                "title": "Le Petit Prince — Édition Spéciale",
                "author": "Antoine de Saint-Exupéry & René",
                "year": 1943,
                "genres": ["Littérature", "Philosophie"],
                "is_available": True,
            }
        ]
        utf8_file = os.path.join(self.temp_dir.name, "utf8_test.json")
        save_books(utf8_file, unicode_books)
        loaded = load_books(utf8_file)
        self.assertEqual(loaded[0]["author"], "Antoine de Saint-Exupéry & René")
        self.assertEqual(loaded[0]["title"], "Le Petit Prince — Édition Spéciale")


if __name__ == "__main__":
    unittest.main()

