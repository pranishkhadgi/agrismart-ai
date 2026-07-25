from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from user import user_bp


@user_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)


@user_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)