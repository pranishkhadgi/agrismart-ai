from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from admin import admin_bp


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin_dashboard.html')