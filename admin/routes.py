from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from extensions import db
from database.models import User, Prediction
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
    total_users       = User.query.count()
    total_predictions = Prediction.query.count()
    recent_users      = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_preds      = Prediction.query.order_by(Prediction.created_at.desc()).limit(5).all()
    return render_template('admin/admin_dashboard.html',
                           total_users=total_users,
                           total_predictions=total_predictions,
                           recent_users=recent_users,
                           recent_preds=recent_preds)


@admin_bp.route('/admin/users')
@login_required
@admin_required
def users():
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=all_users)


@admin_bp.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    if user_id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.users'))
    user = User.query.get_or_404(user_id)
    Prediction.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.email} deleted.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/admin/users/toggle-role/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_role(user_id):
    if user_id == current_user.id:
        flash('You cannot change your own role.', 'danger')
        return redirect(url_for('admin.users'))
    user = User.query.get_or_404(user_id)
    user.role = 'admin' if user.role == 'user' else 'user'
    db.session.commit()
    flash(f'{user.email} is now {user.role}.', 'success')
    return redirect(url_for('admin.users'))