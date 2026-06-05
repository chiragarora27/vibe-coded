"""
CSV Handler — all read/write operations on CSV files.
Ported directly from the original expense_tracker.py CLI logic.
"""
import csv
import os
from datetime import datetime

# All CSV files live in the data/ directory at project root
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
AUTH_FILE = os.path.join(DATA_DIR, 'authenticate.csv')
EXPENSE_FIELDS = ['Name', 'Cost', 'Category', 'Date']


def _user_file(username: str) -> str:
    """Return the path to a user's expense CSV file."""
    return os.path.join(DATA_DIR, f'{username}.csv')


# ── Authentication ─────────────────────────────────────────────────────────────

def authenticate(username: str, password: str) -> bool:
    """Check username/password against authenticate.csv. Returns True on match."""
    if not os.path.exists(AUTH_FILE):
        return False
    with open(AUTH_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False


def username_exists(username: str) -> bool:
    """Return True if the username is already taken."""
    if not os.path.exists(AUTH_FILE):
        return False
    with open(AUTH_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['username'] == username:
                return True
    return False


def add_user(username: str, password: str) -> bool:
    """
    Register a new user:
    - Appends to authenticate.csv
    - Creates an empty expenses CSV for that user
    Returns False if username already taken, True on success.
    """
    if username_exists(username):
        return False

    with open(AUTH_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['username', 'password'])
        writer.writerow({'username': username, 'password': password})

    user_file = _user_file(username)
    if not os.path.exists(user_file):
        with open(user_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=EXPENSE_FIELDS)
            writer.writeheader()

    return True


# ── Expense CRUD ───────────────────────────────────────────────────────────────

def add_expense(username: str, name: str, cost: float, category: str) -> None:
    """Append a new expense row to the user's CSV file."""
    user_file = _user_file(username)
    with open(user_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=EXPENSE_FIELDS)
        writer.writerow({
            'Name': name,
            'Cost': cost,
            'Category': category,
            'Date': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
        })


def get_all_expenses(username: str) -> list:
    """
    Return all expense rows as a list of dicts, newest first.
    Each row gets an injected '_index' key = its 0-based position in the CSV
    file (original order), used as a stable ID for edit/delete operations.
    """
    user_file = _user_file(username)
    if not os.path.exists(user_file):
        return []
    with open(user_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    # Attach stable file-order index BEFORE reversing for display
    for i, row in enumerate(rows):
        row['_index'] = i
    return list(reversed(rows))


def delete_expense(username: str, index: int) -> bool:
    """
    Remove the expense at position `index` (0-based, file order).
    Rewrites the entire CSV without that row.
    Returns True on success, False if index is out of range.
    """
    user_file = _user_file(username)
    if not os.path.exists(user_file):
        return False

    with open(user_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if index < 0 or index >= len(rows):
        return False

    rows.pop(index)

    with open(user_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=EXPENSE_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    return True


def update_expense(username: str, index: int, name: str, cost: float, category: str) -> bool:
    """
    Overwrite the expense at position `index` (0-based, file order) with new
    values. The original Date is preserved. Rewrites the entire CSV.
    Returns True on success, False if index is out of range.
    """
    user_file = _user_file(username)
    if not os.path.exists(user_file):
        return False

    with open(user_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if index < 0 or index >= len(rows):
        return False

    rows[index]['Name']     = name
    rows[index]['Cost']     = cost
    rows[index]['Category'] = category
    # Date intentionally left unchanged

    with open(user_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=EXPENSE_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    return True


def get_expense_by_index(username: str, index: int):
    """Return a single expense row dict by its file-order index, or None."""
    user_file = _user_file(username)
    if not os.path.exists(user_file):
        return None
    with open(user_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if index < 0 or index >= len(rows):
        return None
    return rows[index]


def get_total_spending(username: str) -> float:
    """Sum all 'Cost' values for a user."""
    expenses = get_all_expenses(username)
    return sum(float(e['Cost']) for e in expenses if e.get('Cost'))


def get_category_totals(username: str) -> dict:
    """Return a dict of {category: total_cost} sorted by total descending."""
    expenses = get_all_expenses(username)
    totals = {}
    for e in expenses:
        cat = e.get('Category', 'Uncategorized') or 'Uncategorized'
        totals[cat] = totals.get(cat, 0.0) + float(e['Cost'] or 0)
    return dict(sorted(totals.items(), key=lambda x: x[1], reverse=True))


def get_monthly_totals(username: str) -> dict:
    """
    Return per-month totals as {YYYY-MM: total_cost}.
    Used for the bar chart — replaces matplotlib in the original.
    """
    expenses = get_all_expenses(username)
    totals = {}
    for e in expenses:
        raw_date = e.get('Date', '')
        if not raw_date:
            continue
        try:
            month_key = raw_date[:7]  # 'YYYY-MM'
            totals[month_key] = totals.get(month_key, 0.0) + float(e['Cost'] or 0)
        except (ValueError, TypeError):
            continue
    return dict(sorted(totals.items()))


def get_dashboard_summary(username: str) -> dict:
    """
    Compute the four summary cards for the dashboard:
    total_expenses, this_month, top_category, transaction_count.
    """
    expenses = get_all_expenses(username)
    current_month = datetime.today().strftime('%Y-%m')

    total = 0.0
    this_month = 0.0
    count = len(expenses)
    cat_totals = {}

    for e in expenses:
        cost = float(e.get('Cost') or 0)
        total += cost

        raw_date = e.get('Date', '')
        if raw_date and raw_date[:7] == current_month:
            this_month += cost

        cat = e.get('Category', 'Uncategorized') or 'Uncategorized'
        cat_totals[cat] = cat_totals.get(cat, 0.0) + cost

    top_cat = max(cat_totals, key=cat_totals.get) if cat_totals else '—'

    return {
        'total_expenses': round(total, 2),
        'this_month': round(this_month, 2),
        'top_category': top_cat,
        'transaction_count': count,
    }
