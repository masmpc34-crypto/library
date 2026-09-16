"""
Reporting Module (Module 4)
Generates library analytics, inventory statistics, and formatted reports.
"""

from typing import List, Dict, Any


def generate_library_summary(books: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate comprehensive statistical summary of the library catalog.

    Args:
        books: List of book dictionaries.

    Returns:
        Dictionary with keys:
            - total_books: Total count of books
            - available_books: Count of books currently available for checkout
            - borrowed_books: Count of books currently on loan
            - average_year: Average publication year (float)
            - unique_genres: Sorted list of distinct genres present
    """
    total = len(books)
    available = sum(1 for b in books if b.get("is_available", False) is True)
    borrowed = sum(1 for b in books if b.get("is_available", False) is False)

    total_years = sum(book.get("year", 0) for book in books)
    avg_year = float(total_years / total) if total > 0 else 0.0

    all_genres = set()
    for book in books:
        for genre in book.get("genres", []):
            if isinstance(genre, str) and genre.strip():
                all_genres.add(genre.strip())

    return {
        "total_books": total,
        "available_books": available,
        "borrowed_books": borrowed,
        "average_year": avg_year,
        "unique_genres": sorted(list(all_genres))
    }


def format_summary_report(summary: Dict[str, Any]) -> str:
    """
    Format the summary dictionary into a clean, human-readable text report.

    Args:
        summary: Dictionary returned by generate_library_summary.

    Returns:
        Formatted multi-line string.
    """
    lines = [
        "========================================",
        "        LIBRARY STATUS REPORT           ",
        "========================================",
        f"Total Books Cataloged : {summary.get('total_books', 0)}",
        f"Available on Shelf    : {summary.get('available_books', 0)}",
        f"Currently Borrowed    : {summary.get('borrowed_books', 0)}",
        f"Average Release Year  : {summary.get('average_year', 0.0):.1f}",
        f"Unique Genres ({len(summary.get('unique_genres', []))}) : {', '.join(summary.get('unique_genres', []))}",
        "========================================"
    ]
    return "\n".join(lines)

