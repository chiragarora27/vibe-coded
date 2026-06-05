# Ledger — Personal Expense Tracker

A clean, modern web app converted from a Python CLI expense tracker.
Built with Flask, Chart.js, and pure CSS — no database required.

---

## Quick Start

### 1. Prerequisites
- Python 3.10 or newer
- pip

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python run.py
```

### 4. Open in your browser
```
http://localhost:5000
```

---

## Project Structure

```
expense_web/
├── run.py                    ← entry point
├── requirements.txt
├── data/
│   ├── authenticate.csv      ← user credentials (from original project)
│   └── <username>.csv        ← per-user expense files (auto-created on signup)
├── app/
│   ├── __init__.py           ← Flask app factory
│   ├── routes/
│   │   ├── auth.py           ← /login, /register, /logout
│   │   └── expenses.py       ← /dashboard, /expenses, /add, /categories, /monthly
│   └── utils/
│       └── csv_handler.py    ← all CSV read/write logic (ported from original)
├── templates/
│   ├── base.html             ← sidebar layout + flash messages
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── expenses/
│       ├── dashboard.html    ← 4 summary cards + recent transactions
│       ├── all_expenses.html ← full table with search + sort
│       ├── add_expense.html  ← expense form
│       ├── categories.html   ← doughnut chart + breakdown table
│       └── monthly.html      ← bar chart (replaces matplotlib)
└── static/
    ├── css/main.css
    └── js/
        ├── main.js           ← sidebar toggle, password reveal, flash auto-dismiss
        └── table.js          ← client-side search and column sort
```

---

## CLI → Web Mapping

| Original CLI function     | Web equivalent                          |
|---------------------------|-----------------------------------------|
| `sign_in()` loop          | Session-based `/login` page             |
| `add_user()`              | `/register` route + form                |
| `authenticate()`          | Same logic in `csv_handler.py`          |
| `add_expense()` + input() | `/add` form (POST)                      |
| `view_expenses()` + print | `/expenses` sortable table              |
| `total_spendings()`       | Summary card on dashboard               |
| `category_total()`        | `/categories` — all categories at once  |
| `month_expenses()` + plt  | `/monthly` — Chart.js bar chart         |

---

## Migrating Existing Data

If you already have expense data from the original CLI:

1. Copy your `authenticate.csv` into `data/authenticate.csv`
2. Copy any `<username>.csv` files into the `data/` folder

The web app will read them immediately — no migration needed.

---

## Notes

- Passwords are stored in plain text in `authenticate.csv` (same as the original CLI).
  This is fine for personal/local use. Do **not** expose this app to the internet.
- All data lives in the `data/` folder as CSV files — no external database required.
- The app uses Flask's built-in development server. For local personal use, this is sufficient.
