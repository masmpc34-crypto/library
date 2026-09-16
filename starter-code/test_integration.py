"""
Integration Tests for Library System
Simulates complete team workflow integrating all 4 modules:
1. Storage (loading JSON database)
2. Catalog (filtering and querying)
3. Borrowing (checkout / return transactions)
4. Reporting (generating status metrics)
5. Storage (saving updated state back to disk)
"""

import os
import tempfile
import unittest

from library_system.storage import load_books, save_books
from library_system.catalog import find_books_by_genre, calculate_average_year
from library_system.borrowing import checkout_book, return_book
from library_system.reporting import generate_library_summary


class TestTeamIntegrationWorkflow(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "library_db.json")
        # Start with Day 1 sample data (4 books, 3 available, 1 borrowed)
        self.initial_data = [
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
                "borrower": "Alice",
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
        save_books(self.db_path, self.initial_data)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_full_library_lifecycle_workflow(self):
        # 1. Load data from storage (Tests storage.py)
        catalog = load_books(self.db_path)
        self.assertEqual(len(catalog), 4)

        # 2. Search catalog by genre with case insensitivity (Tests catalog.py)
        se_books = find_books_by_genre(catalog, "software engineering")
        self.assertEqual(len(se_books), 3, "Catalog search must find 3 Software Engineering books")

        # 3. Perform borrowing checkout (Tests borrowing.py)
        checkout_receipt = checkout_book(catalog, 1, "Dave")
        self.assertEqual(checkout_receipt["status"], "CHECKED_OUT")
        book1 = next(b for b in catalog if b["id"] == 1)
        self.assertFalse(book1["is_available"], "Book 1 must be marked unavailable")
        self.assertEqual(book1.get("borrower"), "Dave")

        # Attempting to check out book 1 again should fail
        with self.assertRaises(ValueError):
            checkout_book(catalog, 1, "Eve")

        # 4. Return book 2 (Tests borrowing.py)
        return_receipt = return_book(catalog, 2)
        self.assertEqual(return_receipt["status"], "RETURNED")
        book2 = next(b for b in catalog if b["id"] == 2)
        self.assertTrue(book2["is_available"], "Book 2 must be marked available")

        # 5. Generate reporting analytics (Tests reporting.py)
        # At this point:
        # Book 1: unavailable (borrowed by Dave)
        # Book 2: available (returned by Alice)
        # Book 3: available
        # Book 4: available
        # Total: 4 books, 3 available, 1 borrowed
        summary = generate_library_summary(catalog)
        self.assertEqual(summary["total_books"], 4)
        self.assertEqual(summary["available_books"], 3, "Expected 3 available books after transactions")
        self.assertEqual(summary["borrowed_books"], 1, "Expected 1 borrowed book after transactions")

        # 6. Save modified state and reload (Tests storage.py)
        save_books(self.db_path, catalog)
        reloaded = load_books(self.db_path)
        self.assertEqual(len(reloaded), 4)
        reloaded_book1 = next(b for b in reloaded if b["id"] == 1)
        self.assertFalse(reloaded_book1["is_available"])
        self.assertEqual(reloaded_book1.get("borrower"), "Dave")


if __name__ == "__main__":
    unittest.main()

