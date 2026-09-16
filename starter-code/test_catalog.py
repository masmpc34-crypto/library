"""
Unit Tests for Catalog Module (Module 1)
"""

import unittest
from library_system.catalog import (
    validate_book,
    find_books_by_genre,
    find_books_by_author,
    calculate_average_year,
)


class TestCatalogModule(unittest.TestCase):

    def setUp(self):
        self.sample_books = [
            {
                "id": 1,
                "title": "The Pragmatic Programmer",
                "author": "Andrew Hunt, David Thomas",
                "year": 1999,
                "genres": ["Software Engineering", "Career"],
                "is_available": True,
            },
            {
                "id": 2,
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "year": 2008,
                "genres": ["Software Engineering", "Best Practices"],
                "is_available": False,
            },
            {
                "id": 3,
                "title": "Fluent Python",
                "author": "Luciano Ramalho",
                "year": 2021,
                "genres": ["Python", "Programming"],
                "is_available": True,
            },
            {
                "id": 4,
                "title": "Refactoring",
                "author": "Martin Fowler",
                "year": 1999,
                "genres": ["Software Engineering", "Refactoring"],
                "is_available": True,
            },
        ]

    def test_validate_book_valid(self):
        self.assertTrue(validate_book(self.sample_books[0]))

    def test_validate_book_missing_field(self):
        bad_book = {"id": 1, "title": "Missing Fields"}
        with self.assertRaises(ValueError):
            validate_book(bad_book)

    def test_find_books_by_genre_case_insensitive(self):
        # Must match case-insensitively ("software engineering" matches "Software Engineering")
        matches = find_books_by_genre(self.sample_books, "software engineering")
        self.assertEqual(len(matches), 3, "Expected 3 books matching 'software engineering'")

        # Upper case search
        python_books = find_books_by_genre(self.sample_books, "PYTHON")
        self.assertEqual(len(python_books), 1)
        self.assertEqual(python_books[0]["id"], 3)

        # Non-existent genre
        empty_search = find_books_by_genre(self.sample_books, "Cooking")
        self.assertEqual(len(empty_search), 0)

    def test_find_books_by_author(self):
        fowler_books = find_books_by_author(self.sample_books, "fowler")
        self.assertEqual(len(fowler_books), 1)
        self.assertEqual(fowler_books[0]["title"], "Refactoring")

    def test_calculate_average_year(self):
        # (1999 + 2008 + 2021 + 1999) / 4 = 8027 / 4 = 2006.75
        avg = calculate_average_year(self.sample_books)
        self.assertIsInstance(avg, float)
        self.assertAlmostEqual(avg, 2006.75, places=2)

    def test_calculate_average_year_empty(self):
        self.assertEqual(calculate_average_year([]), 0.0)


if __name__ == "__main__":
    unittest.main()

