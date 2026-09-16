"""
Borrowing Module (Module 3)
Manages library circulation: book checkouts, returns, loan tracking, and late fee calculation.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional


def checkout_book(
    books: List[Dict[str, Any]],
    book_id: int,
    borrower_name: str
) -> Dict[str, Any]:
    """
    Check out a book to a borrower.
    Updates the book's availability status and returns a checkout record.

    Args:
        books: List of book dictionaries in the catalog.
        book_id: Integer ID of the book to checkout.
        borrower_name: Name of the student or patron.

    Returns:
        Dictionary representing the checkout transaction receipt.

    Raises:
        ValueError: If borrower_name is empty, book_id is not found, or book is already checked out.
    """
    if not borrower_name or not borrower_name.strip():
        raise ValueError("Borrower name cannot be empty")

    target_book = None
    for book in books:
        if book.get("id") == book_id:
            target_book = book
            break

    if target_book is None:
        raise ValueError(f"Book with ID {book_id} not found in catalog")

    if not target_book.get("is_available", False):
        raise ValueError(f"Book '{target_book.get('title')}' (ID: {book_id}) is currently unavailable")

    # Update availability
    target_book["is_available"] = False
    target_book["borrower"] = borrower_name.strip()

    return {
        "book_id": book_id,
        "title": target_book.get("title"),
        "borrower": borrower_name.strip(),
        "status": "CHECKED_OUT"
    }


def return_book(books: List[Dict[str, Any]], book_id: int) -> Dict[str, Any]:
    """
    Return a currently borrowed book back to the library catalog.

    Args:
        books: List of book dictionaries in the catalog.
        book_id: Integer ID of the book being returned.

    Returns:
        Dictionary representing the return transaction receipt.

    Raises:
        ValueError: If book is not found or is not currently checked out.
    """
    target_book = None
    for book in books:
        if book.get("id") == book_id:
            target_book = book
            break

    if target_book is None:
        raise ValueError(f"Book with ID {book_id} not found in catalog")

    if target_book.get("is_available", False) is True:
        raise ValueError(f"Book '{target_book.get('title')}' (ID: {book_id}) is already in library (not checked out)")

    former_borrower = target_book.pop("borrower", "Unknown")
    target_book["is_available"] = True

    return {
        "book_id": book_id,
        "title": target_book.get("title"),
        "former_borrower": former_borrower,
        "status": "RETURNED"
    }


def calculate_late_fee(days_overdue: int, daily_rate: float = 0.50) -> float:
    """
    Calculate late fee penalty based on overdue days.

    Args:
        days_overdue: Number of days past the due date.
        daily_rate: Fee charged per overdue day (default $0.50).

    Returns:
        Total fee as a float. Returns 0.0 if not overdue.
    """
    if days_overdue <= 0:
        return 0.0
    return round(float(days_overdue * daily_rate), 2)

