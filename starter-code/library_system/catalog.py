"""
Catalog Module (Module 1)
Handles book record validation, searching by genre and author, and publication metrics.
"""

from typing import List, Dict, Any, Optional


def validate_book(book: Dict[str, Any]) -> bool:
    """
    Validate that a book dictionary has the required structure and non-empty values.

    Args:
        book: Dictionary representing a book.

    Returns:
        True if valid.

    Raises:
        ValueError: If any validation rule is violated.
    """
    if not isinstance(book, dict):
        raise ValueError("Book entry must be a dictionary")

    required_fields = ["id", "title", "author", "year", "genres"]
    for field in required_fields:
        if field not in book:
            raise ValueError(f"Missing required field: '{field}'")

    if not isinstance(book["id"], int) or book["id"] <= 0:
        raise ValueError("Field 'id' must be a positive integer")

    if not isinstance(book["title"], str) or not book["title"].strip():
        raise ValueError("Field 'title' cannot be empty")

    if not isinstance(book["author"], str) or not book["author"].strip():
        raise ValueError("Field 'author' cannot be empty")

    if not isinstance(book["year"], int) or book["year"] <= 0:
        raise ValueError("Field 'year' must be a positive integer")

    if not isinstance(book["genres"], list) or len(book["genres"]) == 0:
        raise ValueError("Field 'genres' must be a non-empty list of strings")

    return True


def find_books_by_genre(books: List[Dict[str, Any]], genre: str) -> List[Dict[str, Any]]:
    """
    Find all books that belong to a specific genre using case-insensitive matching.

    Args:
        books: List of book dictionaries.
        genre: Genre string to search for.

    Returns:
        List of matching book dictionaries.
    """
    if not genre or not genre.strip():
        return []

    target = genre.strip().lower()
    return [
        book for book in books
        if any(g.strip().lower() == target for g in book.get("genres", []))
    ]


def find_books_by_author(books: List[Dict[str, Any]], author_query: str) -> List[Dict[str, Any]]:
    """
    Find all books whose author contains the query string (case-insensitive substring match).

    Args:
        books: List of book dictionaries.
        author_query: Author name or substring to search for.

    Returns:
        List of matching book dictionaries.
    """
    if not author_query or not author_query.strip():
        return []

    target = author_query.strip().lower()
    return [
        book for book in books
        if target in book.get("author", "").lower()
    ]


def calculate_average_year(books: List[Dict[str, Any]]) -> float:
    """
    Calculate the average publication year of books in the catalog.

    Args:
        books: List of book dictionaries.

    Returns:
        Average year as a float. Returns 0.0 if the list is empty.
    """
    if not books:
        return 0.0

    total_years = sum(book.get("year", 0) for book in books)
    return float(total_years / len(books))

