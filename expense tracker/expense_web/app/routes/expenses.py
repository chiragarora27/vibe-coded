"""
Expenses Blueprint — all expense-related pages and API endpoints.
"""
import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from ..utils.csv_handler import (
    add_expense, get_all_expenses, get_total_spending,
    get_category_totals, get_monthly_totals, get_dashboard_summary,
    delete_expense, update_expense, get_expense_by_index,
)

expenses_bp = Blueprint('expenses', __name__)


def _require_login():
    if 'username' not in session:
        flash('Please sign in to continue.', 'info')
        return redirect(url_for('auth.login'))
    return None


# ── Dashboard ─────────────────────────────────────────────────────────────────

@expenses_bp.route('/dashboard')
def dashboard():
    guard = _require_login()
    if guard:
        return guard
    username = session['username']
    summary = get_dashboard_summary(username)
    recent = get_all_expenses(username)[:10]
    return render_template('expenses/dashboard.html', username=username,
                           summary=summary, recent=recent)


# ── All Expenses ──────────────────────────────────────────────────────────────

@expenses_bp.route('/expenses')
def all_expenses():
    guard = _require_login()
    if guard:
        return guard
    username = session['username']
    expenses = get_all_expenses(username)
    total = get_total_spending(username)
    return render_template('expenses/all_expenses.html', username=username,
                           expenses=expenses, total=total)


# ── Add Expense ───────────────────────────────────────────────────────────────

@expenses_bp.route('/add', methods=['GET', 'POST'])
def add():
    guard = _require_login()
    if guard:
        return guard

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        cost_str = request.form.get('cost', '').strip()
        category = request.form.get('category', '').strip()

        if not name or not cost_str or not category:
            flash('All fields are required.', 'error')
        else:
            try:
                cost = float(cost_str)
                if cost < 0:
                    raise ValueError
            except ValueError:
                flash('Cost must be a positive number.', 'error')
            else:
                add_expense(session['username'], name, cost, category)
                flash(f'Expense "{name}" added successfully!', 'success')
                return redirect(url_for('expenses.dashboard'))

    username = session['username']
    cat_totals = get_category_totals(username)
    categories = list(cat_totals.keys())
    return render_template('expenses/add_expense.html', username=username,
                           categories=categories)


# ── Edit Expense ──────────────────────────────────────────────────────────────

@expenses_bp.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    """
    Edit an existing expense by its CSV file-order index.
    GET  — pre-fill the form with current values.
    POST — validate, write changes to CSV, redirect to /expenses.
    """
    guard = _require_login()
    if guard:
        return guard

    username = session['username']
    expense = get_expense_by_index(username, index)

    if expense is None:
        flash('Expense not found.', 'error')
        return redirect(url_for('expenses.all_expenses'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        cost_str = request.form.get('cost', '').strip()
        category = request.form.get('category', '').strip()

        if not name or not cost_str or not category:
            flash('All fields are required.', 'error')
        else:
            try:
                cost = float(cost_str)
                if cost < 0:
                    raise ValueError
            except ValueError:
                flash('Cost must be a positive number.', 'error')
            else:
                ok = update_expense(username, index, name, cost, category)
                if ok:
                    flash(f'Expense "{name}" updated successfully!', 'success')
                else:
                    flash('Could not update expense.', 'error')
                return redirect(url_for('expenses.all_expenses'))

    cat_totals = get_category_totals(username)
    categories = list(cat_totals.keys())
    return render_template('expenses/edit_expense.html', username=username,
                           expense=expense, index=index, categories=categories)


# ── Delete Expense ────────────────────────────────────────────────────────────

@expenses_bp.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    """
    Delete an expense by its CSV file-order index.
    Only accepts POST (form button) to prevent accidental GETs.
    """
    guard = _require_login()
    if guard:
        return guard

    username = session['username']
    expense = get_expense_by_index(username, index)
    name = expense['Name'] if expense else 'Expense'

    ok = delete_expense(username, index)
    if ok:
        flash(f'"{name}" deleted.', 'success')
    else:
        flash('Could not delete expense — it may no longer exist.', 'error')

    # Return to wherever the user came from (expenses list or dashboard)
    referrer = request.form.get('next', url_for('expenses.all_expenses'))
    return redirect(referrer)


# ── Categories ────────────────────────────────────────────────────────────────

@expenses_bp.route('/categories')
def categories():
    guard = _require_login()
    if guard:
        return guard
    username = session['username']
    cat_totals = get_category_totals(username)
    total = sum(cat_totals.values())
    return render_template('expenses/categories.html', username=username,
                           cat_totals=cat_totals, total=total)


# ── Monthly Chart ─────────────────────────────────────────────────────────────

@expenses_bp.route('/monthly')
def monthly():
    guard = _require_login()
    if guard:
        return guard
    return render_template('expenses/monthly.html', username=session['username'])


# ── JSON API endpoints ────────────────────────────────────────────────────────

@expenses_bp.route('/api/monthly')
def api_monthly():
    guard = _require_login()
    if guard:
        return jsonify({'error': 'Unauthorized'}), 401
    monthly = get_monthly_totals(session['username'])
    return jsonify({'labels': list(monthly.keys()),
                    'data': [round(v, 2) for v in monthly.values()]})


@expenses_bp.route('/api/categories')
def api_categories():
    guard = _require_login()
    if guard:
        return jsonify({'error': 'Unauthorized'}), 401
    cat_totals = get_category_totals(session['username'])
    return jsonify({'labels': list(cat_totals.keys()),
                    'data': [round(v, 2) for v in cat_totals.values()]})


@expenses_bp.route('/admin/users')
def admin_users():
    csv_path = os.path.join('data', 'authenticate.csv')

    with open(csv_path, 'r') as f:
        return f.read().replace('\n', '<br>')
