"""Logged-in page routes."""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, logout_user


# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@home_bp.route('/', methods=['GET', 'POST'])
def home():
    """Home"""
   
    return render_template('home.html')


@home_bp.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    """Feedback"""

    return render_template('feedback.html')


@home_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))