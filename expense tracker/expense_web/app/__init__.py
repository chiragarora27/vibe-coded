"""
Expense Tracker - Flask Application Factory
"""
from flask import Flask
from .routes.auth import auth_bp
from .routes.expenses import expenses_bp


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.secret_key = 'expense-tracker-local-secret-2024'  # Local use only

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp)

    return app
