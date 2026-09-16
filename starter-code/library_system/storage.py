"""
Storage Module (Module 2)
Handles reading from and writing to JSON storage files with proper UTF-8 encoding and schema validation.
"""

import json
import os
from typing import List, Dict, Any


def load_books(filepath: str) -> List[Dict[str, Any]]:
    """
    Load a list of book dictionaries from a JSON file.

    Args:
        filepath: Path to the JSON file.

    Returns:
        List of book dictionaries.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If file content is not valid JSON.
        ValueError: If the top-level data in JSON is not a list.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Database file not found: '{filepath}'")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(f"Catalog data must be a list of book dictionaries, got {type(data).__name__}")

    return data


def save_books(filepath: str, books: List[Dict[str, Any]], indent: int = 2) -> None:
    """
    Save a list of book dictionaries to a JSON file.

    Args:
        filepath: Path to the destination JSON file.
        books: List of book dictionaries to write.
        indent: Indentation level for pretty-printing JSON.

    Raises:
        TypeError: If books is not a list.
    """
    if not isinstance(books, list):
        raise TypeError(f"Books data must be a list, got {type(books).__name__}")

    # Ensure target directory exists if specified
    dir_path = os.path.dirname(filepath)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=indent, ensure_ascii=False)

