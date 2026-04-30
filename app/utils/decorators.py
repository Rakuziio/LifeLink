from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))

        if not current_user.is_admin:
            flash("Access denied")
            return redirect(url_for('home.home_page'))

        return f(*args, **kwargs)
    return wrapper