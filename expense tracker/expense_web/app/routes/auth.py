"""
Auth Blueprint — handles /login, /register, /logout
Maps to: sign_in(), add_user(), authenticate() in original CLI
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..utils.csv_handler import authenticate, add_user, username_exists

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    """Redirect root to dashboard if logged in, else to login."""
    if 'username' in session:
        return redirect(url_for('expenses.dashboard'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page — authenticates against authenticate.csv."""
    if 'username' in session:
        return redirect(url_for('expenses.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if authenticate(username, password):
            session['username'] = username
            return redirect(url_for('expenses.dashboard'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page — creates new user in authenticate.csv."""
    if 'username' in session:
        return redirect(url_for('expenses.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm  = request.form.get('confirm_password', '').strip()

        if not username or not password:
            flash('Username and password are required.', 'error')
        elif password != confirm:
            flash('Passwords do not match.', 'error')
        elif username_exists(username):
            flash('That username is already taken.', 'error')
        else:
            add_user(username, password)
            flash('Account created! Please sign in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
def logout():
    """Clear session and redirect to login."""
    session.clear()
    flash('You have been signed out.', 'info')
    return redirect(url_for('auth.login'))
