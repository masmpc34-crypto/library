"""
Library Management & Circulation Dashboard (Starter Code)
Follow the step-by-step TODO instructions in this file and README.md
to connect your tested Day 2 library backend to this interactive Streamlit UI!
"""

import os
import pandas as pd
import streamlit as st

# Import the tested backend functions from your library_system package
from library_system.storage import load_books, save_books
from library_system.catalog import (
    validate_book,
    find_books_by_genre,
    find_books_by_author,
)
from library_system.borrowing import checkout_book, return_book
from library_system.reporting import generate_library_summary

# -------------------------------------------------------------------
# Page Configuration & File Setup
# -------------------------------------------------------------------
st.set_page_config(
    page_title="Library Inventory & Circulation Dashboard",
    page_icon="📚",
    layout="wide",
)

DATA_FILE = os.path.join(os.path.dirname(__file__), "sample_data.json")


def get_current_books():
    """Load latest books from disk, handling missing or corrupt file gracefully."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        return load_books(DATA_FILE)
    except Exception as err:
        st.error(f"Failed to load catalog data from {DATA_FILE}: {err}")
        return []


books = get_current_books()

# -------------------------------------------------------------------
# Header
# -------------------------------------------------------------------
st.title("📚 Library Management & Circulation Dashboard")
st.caption("Day 3 Lab: Pure Python Web Frontend with Streamlit")

# ===================================================================
# TODO 1: Key Metrics Dashboard (Morning Lecture / Lab Step 3)
# ===================================================================
# 1. Call `summary = generate_library_summary(books)` from library_system.reporting.
# 2. Use `st.columns(4)` to create 4 dashboard cards.
# 3. In each column, use `st.metric()` to display:
#    - Column 1: Total Books
#    - Column 2: Available on Shelf
#    - Column 3: Currently Borrowed
#    - Column 4: Average Release Year
#
# Hint:
# summary = generate_library_summary(books)
# m1, m2, m3, m4 = st.columns(4)
# m1.metric("Total Books", summary.get("total_books", 0))
# ...

st.info("👉 Complete TODO 1 in app.py to render library status metrics cards here.")

st.divider()

# -------------------------------------------------------------------
# Navigation Tabs
# -------------------------------------------------------------------
tab_browse, tab_add, tab_circulation = st.tabs(
    ["📖 Browse Catalog", "➕ Add New Book", "🔄 Circulation Desk"]
)

# ===================================================================
# TODO 2: Browse Catalog & Filters (Lab Step 4)
# ===================================================================
with tab_browse:
    st.subheader("Filter & Search Catalog")

    # 1. Create filter controls using st.columns([1, 2]):
    #    - Left column: st.selectbox("Filter by Genre", ["All Genres"] + ...)
    #    - Right column: st.text_input("Search by Author or Title")
    #
    # 2. Filter the `books` list using your backend functions:
    #    - find_books_by_genre(books, selected_genre)
    #    - Substring search on title/author
    #
    # 3. Convert the list of dicts to a pandas DataFrame:
    #    df = pd.DataFrame(...)
    #    st.dataframe(df, use_container_width=True, hide_index=True)

    st.info("👉 Complete TODO 2 in app.py to display the searchable book catalog.")


# ===================================================================
# TODO 3: Register New Book with Form (Lab Step 5)
# ===================================================================
with tab_add:
    st.subheader("Register a New Book into the Catalog")

    # 1. Create a form with: with st.form("add_book_form", clear_on_submit=True):
    # 2. Input fields:
    #    - new_title = st.text_input("Book Title *")
    #    - new_author = st.text_input("Author(s) *")
    #    - new_year = st.number_input("Publication Year *", min_value=1500, max_value=2050, value=2024)
    #    - new_genres_raw = st.text_input("Genres (comma-separated) *")
    #    - submit_btn = st.form_submit_button("Register Book")
    #
    # 3. When submitted:
    #    - Build candidate book dictionary
    #    - Call backend validate_book(candidate_book) inside a try/except ValueError block
    #    - Append to books and call save_books(DATA_FILE, books)
    #    - Show st.success(...) and st.rerun()

    st.info("👉 Complete TODO 3 in app.py to implement book registration.")


# ===================================================================
# TODO 4: Circulation Desk (Check Out & Return) (Lab Step 6)
# ===================================================================
with tab_circulation:
    st.subheader("Circulation Operations")

    # 1. Split into two columns: Checkout (left) and Return (right)
    # 2. For Checkout:
    #    - Filter available books: [b for b in books if b.get("is_available", False)]
    #    - Use st.selectbox to pick a book and st.text_input for borrower name
    #    - On button click, call backend checkout_book(books, book_id, borrower)
    #    - Call save_books(DATA_FILE, books) and st.rerun()
    # 3. For Return:
    #    - Filter borrowed books: [b for b in books if not b.get("is_available", False)]
    #    - Use st.selectbox to pick a book
    #    - On button click, call backend return_book(books, book_id)
    #    - Call save_books(DATA_FILE, books) and st.rerun()

    st.info("👉 Complete TODO 4 in app.py to implement checkout and return workflows.")
