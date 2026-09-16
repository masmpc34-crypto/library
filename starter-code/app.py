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
summary = generate_library_summary(books)

m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.metric(label="Total de Livros", value=summary.get("total_books", 0))
with m_col2:
    st.metric(
        label="Disponíveis na Estante",
        value=summary.get("available_books", 0),
        delta=f"{summary.get('available_books', 0)} prontos",
    )
with m_col3:
    st.metric(
        label="Emprestados",
        value=summary.get("borrowed_books", 0),
        delta=f"-{summary.get('borrowed_books', 0)} fora" if summary.get("borrowed_books", 0) > 0 else "Nenhum",
        delta_color="inverse",
    )
with m_col4:
    avg_yr = summary.get("average_year", 0.0)
    st.metric(label="Ano Médio de Lançamento", value=f"{avg_yr:.1f}" if avg_yr > 0 else "N/A")

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

    f_col1, f_col2 = st.columns([1, 2])
    with f_col1:
        genres = ["Todos os Gêneros"] + summary.get("unique_genres", [])
        selected_genre = st.selectbox("Filtrar por Gênero", options=genres)
    with f_col2:
        search_query = st.text_input("Buscar por Autor ou Título", placeholder="Digite termos de busca...")

    filtered = books
    if selected_genre != "Todos os Gêneros":
        filtered = find_books_by_genre(filtered, selected_genre)
    if search_query.strip():
        q = search_query.strip().lower()
        filtered = [b for b in filtered if q in b.get("title", "").lower() or q in b.get("author", "").lower()]

    df = pd.DataFrame(filtered)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.info("👉 Complete TODO 2 in app.py to display the searchable book catalog.")


# ===================================================================
# TODO 3: Register New Book with Form (Lab Step 5)
# ===================================================================
with tab_add:
    st.subheader("Register a New Book into the Catalog")
    with st.form("form_cadastro_livro", clear_on_submit=True):
        new_title = st.text_input("Título da Obra *")
        new_author = st.text_input("Autor(es) *")
        new_year = st.number_input("Ano de Publicação *", min_value=1500, max_value=2050, value=2024)
        new_genres = st.text_input("Gêneros (separados por vírgula) *")
        if st.form_submit_button("Cadastrar Livro", type="primary"):
            next_id = max([b.get("id", 0) for b in books], default=0) + 1
            candidate = {"id": next_id, "title": new_title.strip(), "author": new_author.strip(),
                         "year": int(new_year), "genres": [g.strip() for g in new_genres.split(",") if g.strip()],
                         "is_available": True}
            try:
                validate_book(candidate)  # Validação no backend!
                books.append(candidate)
                save_books(DATA_FILE, books)
                st.success(f"Registrado com sucesso #{next_id}: {candidate['title']}!")
                st.rerun()
            except ValueError as e:
                st.error(f"Erro de Validação: {e}")

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
