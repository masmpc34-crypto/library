"""
Unit Tests for Borrowing Module (Module 3)
"""

import unittest
from library_system.borrowing import checkout_book, return_book, calculate_late_fee


class TestBorrowingModule(unittest.TestCase):

    def setUp(self):
        self.sample_books = [
            {
                "id": 1,
                "title": "The Pragmatic Programmer",
                "author": "Andrew Hunt, David Thomas",
                "year": 1999,
                "genres": ["Software Engineering"],
                "is_available": True,
            },
            {
                "id": 2,
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "year": 2008,
                "genres": ["Software Engineering"],
                "is_available": False,
                "borrower": "Alice",
            },
        ]

    def test_checkout_book_updates_availability(self):
        receipt = checkout_book(self.sample_books, 1, "Bob")
        self.assertEqual(receipt["status"], "CHECKED_OUT")
        self.assertEqual(receipt["borrower"], "Bob")

        # Crucial check: Book must be marked as NOT available
        book = next(b for b in self.sample_books if b["id"] == 1)
        self.assertFalse(book["is_available"], "Book 'is_available' should be False after checkout")
        self.assertEqual(book.get("borrower"), "Bob")

    def test_checkout_already_borrowed_raises_value_error(self):
        with self.assertRaises(ValueError):
            checkout_book(self.sample_books, 2, "Charlie")

    def test_return_book_updates_availability(self):
        receipt = return_book(self.sample_books, 2)
        self.assertEqual(receipt["status"], "RETURNED")
        self.assertEqual(receipt["former_borrower"], "Alice")

        # Crucial check: Book must be marked available again
        book = next(b for b in self.sample_books if b["id"] == 2)
        self.assertTrue(book["is_available"], "Book 'is_available' should be True after return")
        self.assertNotIn("borrower", book)

    def test_return_book_not_borrowed_raises_value_error(self):
        # Book 1 is available; returning it should raise ValueError
        with self.assertRaises(ValueError):
            return_book(self.sample_books, 1)

    def test_calculate_late_fee(self):
        self.assertEqual(calculate_late_fee(0), 0.0)
        self.assertEqual(calculate_late_fee(-3), 0.0)
        self.assertEqual(calculate_late_fee(4, daily_rate=0.50), 2.0)
        self.assertEqual(calculate_late_fee(3, daily_rate=0.75), 2.25)


if __name__ == "__main__":
    unittest.main()

