"""
Unit Tests for Reporting Module (Module 4)
"""

import unittest
from library_system.reporting import generate_library_summary, format_summary_report


class TestReportingModule(unittest.TestCase):

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
                "genres": ["Software Engineering"],
                "is_available": False,
            },
            {
                "id": 3,
                "title": "Fluent Python",
                "author": "Luciano Ramalho",
                "year": 2021,
                "genres": ["Python"],
                "is_available": True,
            },
            {
                "id": 4,
                "title": "Refactoring",
                "author": "Martin Fowler",
                "year": 1999,
                "genres": ["Software Engineering"],
                "is_available": True,
            },
        ]

    def test_generate_library_summary_counts(self):
        summary = generate_library_summary(self.sample_books)
        self.assertEqual(summary["total_books"], 4)
        # Out of 4 books, 3 are available (id 1, 3, 4) and 1 is borrowed (id 2)
        self.assertEqual(summary["available_books"], 3, "Expected 3 available books")
        self.assertEqual(summary["borrowed_books"], 1, "Expected 1 borrowed book")
        self.assertAlmostEqual(summary["average_year"], 2006.75, places=2)
        self.assertIn("Career", summary["unique_genres"])
        self.assertIn("Python", summary["unique_genres"])
        self.assertIn("Software Engineering", summary["unique_genres"])

    def test_generate_library_summary_empty(self):
        summary = generate_library_summary([])
        self.assertEqual(summary["total_books"], 0)
        self.assertEqual(summary["available_books"], 0)
        self.assertEqual(summary["borrowed_books"], 0)
        self.assertEqual(summary["average_year"], 0.0)
        self.assertEqual(summary["unique_genres"], [])

    def test_format_summary_report(self):
        summary = generate_library_summary(self.sample_books)
        report_text = format_summary_report(summary)
        self.assertIn("LIBRARY STATUS REPORT", report_text)
        self.assertIn("Total Books Cataloged : 4", report_text)
        self.assertIn("Available on Shelf    : 3", report_text)
        self.assertIn("Currently Borrowed    : 1", report_text)


if __name__ == "__main__":
    unittest.main()

