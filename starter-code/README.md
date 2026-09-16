# Day 3 Lab: Streamlit Web Dashboard & Capstone Kickoff 🚀

Welcome to Day 3 of the Python Bootcamp!

Today, we take our fully tested, modular Python backend from Day 2 and connect it to a modern, pure-Python web interface using **Streamlit** and the ultra-fast Python package manager **uv**. In the second half of the afternoon, you will form your **Capstone Project Teams**, select a project topic, set up a shared GitHub repository, and establish your project architecture.

---

## 🎯 Lab Objectives

1. **Modern Python Tooling (`uv`)**: Install and use `uv` to manage dependencies and execute commands seamlessly without manual virtual environment headaches.
2. **Build a Pure-Python Web UI**: Connect `library_system/` to an interactive browser application (`app.py`) using `st.title`, `st.metric`, `st.dataframe`, `st.selectbox`, `st.text_input`, and `st.form`.
3. **Preserve Separation of Concerns**: Keep frontend code decoupled from backend business logic so unit tests continue to pass with 100% confidence.
4. **Master Live Reload**: Experience Streamlit's rapid-feedback developer loop ("Always rerun").
5. **Capstone Project Kickoff**: Form teams of 2–3, select a topic, create a shared GitHub repository, set up standard folders (including `/tests`), and draft requirements in `README.md`.

---

## 📁 Project Directory Structure

```text
starter-code/
├── pyproject.toml           # Project metadata & dependencies for uv
├── .gitignore               # Ignores .venv, cache files, etc.
├── sample_data.json         # JSON catalog database
├── app.py                   # Streamlit web application scaffold (MODIFY THIS FILE)
├── library_system/          # Tested Day 2 backend package
│   ├── __init__.py
│   ├── catalog.py           # Book validation & genre/author search
│   ├── storage.py           # Robust JSON load/save operations
│   ├── borrowing.py         # Book checkout and return circulation
│   └── reporting.py         # Summary metrics calculations
├── test_catalog.py          # Unit tests for catalog.py
├── test_storage.py          # Unit tests for storage.py
├── test_borrowing.py        # Unit tests for borrowing.py
├── test_reporting.py        # Unit tests for reporting.py
└── test_integration.py      # End-to-end integration workflow tests
```

---

## 🛠️ Step-by-Step Instructions: Streamlit Dashboard

### Step 1: Install `uv` (Your Fast Python Toolchain)

`uv` is an extremely fast, modern Python package installer and environment manager written in Rust.

#### On Windows (PowerShell):
Open PowerShell (as Administrator or regular user) and run:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
*Alternative via Winget:*
```powershell
winget install astral-sh.uv
```

#### On macOS & Linux (Terminal):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Verify Installation:
Close and reopen your terminal, then verify:
```bash
uv --version
```
*(You should see `uv 0.4.x` or newer).*

---

### Step 2: Verify Existing Tests

Before touching any code, verify that all 20 backend unit tests from Day 2 pass:

```bash
# Using uv (automatically installs Python dependencies in an isolated sandbox)
uv run python -m unittest discover -v

# Or using standard python
python3 -m unittest discover -v
```

**Expected Result:**
```text
Ran 20 tests in 0.002s

OK
```

---

### Step 3: Launch Streamlit & Enable Live Auto-Reload

Run the starter application using `uv`:

```bash
uv run streamlit run app.py
```

1. Streamlit will install `streamlit` and `pandas` automatically into a cached environment (no manual `venv` activation needed!).
2. Your default web browser will automatically open to `http://localhost:8501`.
3. **Configure Live Auto-Reload**:
   - In your browser, look at the top right corner.
   - When you make a change in `app.py` and save, Streamlit displays a prompt: **"Source file changed. [Rerun] [Always rerun]"**.
   - Click **"Always rerun"**. Now, every time you press `Ctrl + S` (or `Cmd + S`) in VS Code / your editor, your browser will instantly reload with your newest changes!

---

### Step 4: Implement `app.py` Step-by-Step

Open `app.py` in your code editor. You will complete four guided checkpoints (`TODO 1` through `TODO 4`).

#### 📍 Checkpoint 1: Render Library Status Metrics (`TODO 1`)
Find `TODO 1` in `app.py`. Replace the placeholder `st.info(...)` banner with:

```python
# Call backend reporting module
summary = generate_library_summary(books)

# Create 4 columns for metric cards
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.metric(label="Total Books", value=summary.get("total_books", 0))
with m_col2:
    st.metric(
        label="Available on Shelf",
        value=summary.get("available_books", 0),
        delta=f"{summary.get('available_books', 0)} ready",
    )
with m_col3:
    st.metric(
        label="Currently Borrowed",
        value=summary.get("borrowed_books", 0),
        delta=f"-{summary.get('borrowed_books', 0)} out" if summary.get("borrowed_books", 0) > 0 else "None",
        delta_color="inverse",
    )
with m_col4:
    avg_yr = summary.get("average_year", 0.0)
    st.metric(label="Average Release Year", value=f"{avg_yr:.1f}" if avg_yr > 0 else "N/A")
```
👉 **Save `app.py`**: Switch to your browser. You should now see four status cards at the top of your dashboard!

---

#### 📍 Checkpoint 2: Display & Filter the Catalog Table (`TODO 2`)
Under `with tab_browse:`, replace the `TODO 2` placeholder with:

```python
st.subheader("Filter & Search Catalog")

# Filter controls
f_col1, f_col2 = st.columns([1, 2])
with f_col1:
    genres = ["All Genres"] + summary.get("unique_genres", [])
    selected_genre = st.selectbox("Filter by Genre", options=genres)

with f_col2:
    search_query = st.text_input("Search by Author or Title", placeholder="Type search keywords...")

# Apply backend filters
filtered = books
if selected_genre != "All Genres":
    filtered = find_books_by_genre(filtered, selected_genre)

if search_query.strip():
    query = search_query.strip().lower()
    filtered = [
        b for b in filtered
        if query in b.get("title", "").lower() or query in b.get("author", "").lower()
    ]

st.write(f"Showing **{len(filtered)}** of **{len(books)}** book(s)")

if filtered:
    table_rows = []
    for b in filtered:
        table_rows.append({
            "ID": b.get("id"),
            "Title": b.get("title"),
            "Author": b.get("author"),
            "Year": b.get("year"),
            "Genres": ", ".join(b.get("genres", [])),
            "Status": "Available" if b.get("is_available") else "Borrowed",
            "Borrower": b.get("borrower", "—"),
        })
    df = pd.DataFrame(table_rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No books match the selected filters.")
```
👉 **Save `app.py`**: Switch to your browser. Test selecting genres like "Python" or typing "Martin" into the search bar. The table updates instantly!

---

#### 📍 Checkpoint 3: Register a New Book Form (`TODO 3`)
Under `with tab_add:`, replace the `TODO 3` placeholder with:

```python
st.subheader("Register a New Book into the Catalog")

with st.form("add_book_form", clear_on_submit=True):
    col_title, col_author = st.columns(2)
    with col_title:
        new_title = st.text_input("Book Title *", placeholder="e.g., Designing Data-Intensive Applications")
    with col_author:
        new_author = st.text_input("Author(s) *", placeholder="e.g., Martin Kleppmann")

    col_year, col_genres = st.columns(2)
    with col_year:
        new_year = st.number_input("Publication Year *", min_value=1500, max_value=2050, value=2020, step=1)
    with col_genres:
        new_genres_raw = st.text_input("Genres (comma-separated) *", placeholder="e.g., Distributed Systems, Databases")

    submit_btn = st.form_submit_button("Register Book", type="primary")

    if submit_btn:
        genres_list = [g.strip() for g in new_genres_raw.split(",") if g.strip()]
        existing_ids = [b.get("id", 0) for b in books if isinstance(b.get("id"), int)]
        next_id = max(existing_ids, default=0) + 1

        candidate_book = {
            "id": next_id,
            "title": new_title.strip(),
            "author": new_author.strip(),
            "year": int(new_year),
            "genres": genres_list,
            "is_available": True,
        }

        try:
            # 1. Validate using Day 2 backend
            validate_book(candidate_book)

            # 2. Persist using Day 2 storage
            books.append(candidate_book)
            save_books(DATA_FILE, books)

            st.success(f"Successfully registered: #{next_id} — **{candidate_book['title']}**!")
            st.rerun()
        except ValueError as val_err:
            st.error(f"Validation Failed: {val_err}")
```
👉 **Save `app.py`**:
1. Try clicking "Register Book" with empty fields: notice how `validate_book()` raises a `ValueError` that is caught and displayed gracefully with `st.error`!
2. Now enter a valid title, author, and genres, and click submit. Watch the book appear in `sample_data.json` and in the browse table immediately!

---

#### 📍 Checkpoint 4: Circulation Desk (Check Out & Return) (`TODO 4`)
Under `with tab_circulation:`, replace the `TODO 4` placeholder with:

```python
st.subheader("Circulation Operations")

col_checkout, col_return = st.columns(2)

# Check Out Section
with col_checkout:
    st.markdown("### 📤 Check Out a Book")
    available_books = [b for b in books if b.get("is_available", False)]

    if not available_books:
        st.info("No books are currently available on the shelf.")
    else:
        book_options = {f"#{b['id']}: {b['title']}": b["id"] for b in available_books}
        selected_label = st.selectbox("Choose Book to Check Out", options=list(book_options.keys()))
        borrower = st.text_input("Borrower Name *", placeholder="Student / Patron name")

        if st.button("Complete Checkout", type="primary"):
            if not borrower.strip():
                st.warning("Please provide a borrower name.")
            else:
                target_id = book_options[selected_label]
                try:
                    receipt = checkout_book(books, target_id, borrower.strip())
                    save_books(DATA_FILE, books)
                    st.success(f"Checked out '{receipt['title']}' to **{receipt['borrower']}**!")
                    st.rerun()
                except ValueError as err:
                    st.error(f"Checkout Error: {err}")

# Return Section
with col_return:
    st.markdown("### 📥 Return a Book")
    borrowed_books = [b for b in books if not b.get("is_available", False)]

    if not borrowed_books:
        st.info("No books are currently checked out.")
    else:
        borrowed_options = {f"#{b['id']}: {b['title']} (Borrower: {b.get('borrower', 'Unknown')})": b["id"] for b in borrowed_books}
        return_label = st.selectbox("Choose Book to Return", options=list(borrowed_options.keys()))

        if st.button("Complete Return"):
            target_return_id = borrowed_options[return_label]
            try:
                receipt = return_book(books, target_return_id)
                save_books(DATA_FILE, books)
                st.success(f"Returned '{receipt['title']}'!")
                st.rerun()
            except ValueError as err:
                st.error(f"Return Error: {err}")
```
👉 **Save `app.py`**: Try checking out a book to your name, then head to the Browse Catalog tab or check the Top Metrics cards to see the status update in real time!

---

### Step 5: Verify Automated Tests Still Pass!

In your terminal, run the test suite again:

```bash
uv run python -m unittest discover -v
```

Notice that all 20 tests **still pass 100%**!
> **Why?** Because we respected the **Separation of Concerns**:
> - All business logic and validation remain in `library_system/`
> - `app.py` is purely a presentation layer that gathers user input and calls backend functions.

---

## 🚀 Part 2: Capstone Project Kickoff

During the final portion of today's lab, you and your peers will kick off the **Capstone Project**.

### 1. Form Capstone Teams
- Groups of **2 to 3 students**.
- Appoint roles (e.g., Tech Lead / Release Manager, Backend Architect, Frontend / UI Specialist).

### 2. Select a Project Topic
Choose one of the four approved capstone tracks:

1. **Student Bug & Task Tracker**
   - *Scope:* Log, assign, and track software bugs during coursework.
   - *Key UI Elements:* Ticket creation form (severity, title, assignee), filterable Kanban/table view, status transitions.
   - *Unit Test Targets:* Cannot create blank tickets; invalid status transitions rejected; JSON roundtrip test.

2. **School Club Activity & Attendance Logger**
   - *Scope:* Dashboard for student club leaders to schedule meetings and log member attendance.
   - *Key UI Elements:* Event scheduler, member check-in dropdown, turnout metric cards.
   - *Unit Test Targets:* Attendance counts increment properly; no duplicate sign-ins per student per date; turnout averages calculate accurately.

3. **Homework & Study Habit Planner**
   - *Scope:* Productivity hub tracking homework deadlines and study hours.
   - *Key UI Elements:* Task submission with due dates and subject tags, completion checkboxes, progress chart.
   - *Unit Test Targets:* Reject past due dates on creation; status toggles update completion ratio; filter by subject works reliably.

4. **Classroom Flashcard & Quiz Builder**
   - *Scope:* Study aid to create question/answer decks and practice with an interactive quiz mode.
   - *Key UI Elements:* Card editor, flip/reveal flashcard view, scored quiz runner.
   - *Unit Test Targets:* Score calculation accuracy; reject blank questions/answers; deck shuffle preserves full card count.

---

### 3. Initialize Shared GitHub Repository
One team member creates the repository on GitHub:
1. Name the repository after your project (e.g., `bug-tracker-capstone`).
2. Add teammates as **Collaborators** under `Settings > Collaborators`.
3. Clone the repo to your local machine:
   ```bash
   git clone https://github.com/<team-lead-username>/<project-name>.git
   cd <project-name>
   ```

---

### 4. Create Standard Project Folder Structure
Set up your project directory structure cleanly:

```text
your-capstone-project/
├── pyproject.toml           # Define name, version, and dependencies (streamlit, pandas)
├── README.md                # Project requirements, setup guide, and team members
├── .gitignore               # Standard Python gitignore (.venv/, __pycache__/, etc.)
├── app.py                   # Streamlit entry point
├── src/                     # Core backend logic (isolated from Streamlit)
│   ├── __init__.py
│   ├── models.py            # Data classes / validation rules
│   └── storage.py           # JSON file load and save operations
└── tests/                   # Dedicated unit test suite
    ├── __init__.py
    └── test_models.py       # Initial test targets
```

Quick terminal command to initialize folders:
```bash
mkdir -p src tests
touch app.py src/__init__.py src/models.py src/storage.py tests/__init__.py tests/test_models.py
```

---

### 5. Draft Requirements in `README.md`
In your team's `README.md`, document:
- **Project Title & Team Members**
- **Problem Statement** (Who is this for and what problem does it solve?)
- **Core Features List** (Must-have features for MVP)
- **Data Schema Definition** (What does an item in JSON look like?)
- **3+ Unit Test Targets** (What specific logic will automated tests verify?)
- **How to Install & Run** (`uv run streamlit run app.py` and `uv run python -m unittest discover`)

Commit and push your initial skeleton to GitHub:
```bash
git add -A
git commit -m "Initial capstone project skeleton and requirements"
git push origin main
```

🎉 **Congratulations! You have completed Day 3!**
