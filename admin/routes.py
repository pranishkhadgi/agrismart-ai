from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from werkzeug.utils import secure_filename
from extensions import db
from database.models import User, Prediction, CropData, MLModelRecord
from admin import admin_bp
import os
import joblib

ALLOWED_EXTENSIONS = {'pkl'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    total_crops       = CropData.query.count()
    recent_users      = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_preds      = Prediction.query.order_by(Prediction.created_at.desc()).limit(5).all()
    return render_template('admin/admin_dashboard.html',
                           total_users=total_users,
                           total_predictions=total_predictions,
                           total_crops=total_crops,
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


# --- CROP DATA ---

@admin_bp.route('/admin/crops')
@login_required
@admin_required
def crops():
    all_crops = CropData.query.order_by(CropData.crop_name).all()
    return render_template('admin/crops.html', crops=all_crops)


@admin_bp.route('/admin/crops/add', methods=['POST'])
@login_required
@admin_required
def add_crop():
    crop_name   = request.form.get('crop_name', '').strip()
    description = request.form.get('description', '').strip()
    season      = request.form.get('season', '').strip()

    if not crop_name:
        flash('Crop name is required.', 'danger')
        return redirect(url_for('admin.crops'))

    existing = CropData.query.filter_by(crop_name=crop_name.lower()).first()
    if existing:
        flash('Crop already exists.', 'warning')
        return redirect(url_for('admin.crops'))

    crop = CropData(
        crop_name=crop_name.lower(),
        description=description,
        season=season,
        uploaded_by=current_user.id
    )
    db.session.add(crop)
    db.session.commit()
    flash(f'{crop_name} added successfully.', 'success')
    return redirect(url_for('admin.crops'))


@admin_bp.route('/admin/crops/delete/<int:crop_id>', methods=['POST'])
@login_required
@admin_required
def delete_crop(crop_id):
    crop = CropData.query.get_or_404(crop_id)
    db.session.delete(crop)
    db.session.commit()
    flash(f'{crop.crop_name} deleted.', 'success')
    return redirect(url_for('admin.crops'))


@admin_bp.route('/admin/crops/edit/<int:crop_id>', methods=['POST'])
@login_required
@admin_required
def edit_crop(crop_id):
    crop = CropData.query.get_or_404(crop_id)
    crop.description = request.form.get('description', '').strip()
    crop.season      = request.form.get('season', '').strip()
    db.session.commit()
    flash(f'{crop.crop_name} updated.', 'success')
    return redirect(url_for('admin.crops'))


# --- ML MODELS ---

@admin_bp.route('/admin/models')
@login_required
@admin_required
def models():
    all_models = MLModelRecord.query.order_by(MLModelRecord.updated_at.desc()).all()
    return render_template('admin/models.html', models=all_models)


@admin_bp.route('/admin/models/upload', methods=['POST'])
@login_required
@admin_required
def upload_model():
    model_name = request.form.get('model_name', '').strip()
    accuracy   = request.form.get('accuracy', '').strip()
    file       = request.files.get('model_file')

    if not model_name or not file:
        flash('Model name and file are required.', 'danger')
        return redirect(url_for('admin.models'))

    if not allowed_file(file.filename):
        flash('Only .pkl files are allowed.', 'danger')
        return redirect(url_for('admin.models'))

    filename = secure_filename(file.filename)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_path = os.path.join(base_dir, 'data', 'models', filename)
    file.save(save_path)

    existing = MLModelRecord.query.filter_by(filename=filename).first()
    if existing:
        existing.model_name  = model_name
        existing.accuracy    = float(accuracy) if accuracy else None
        existing.uploaded_by = current_user.id
        from datetime import datetime
        existing.updated_at  = datetime.utcnow()
    else:
        record = MLModelRecord(
            model_name=model_name,
            filename=filename,
            accuracy=float(accuracy) if accuracy else None,
            uploaded_by=current_user.id
        )
        db.session.add(record)

    db.session.commit()
    flash(f'{filename} uploaded successfully. Restart the server to apply.', 'success')
    return redirect(url_for('admin.models'))


@admin_bp.route('/admin/models/delete/<int:model_id>', methods=['POST'])
@login_required
@admin_required
def delete_model(model_id):
    model = MLModelRecord.query.get_or_404(model_id)
    db.session.delete(model)
    db.session.commit()
    flash(f'{model.filename} record deleted.', 'success')
    return redirect(url_for('admin.models'))


# --- ALL PREDICTIONS ---

@admin_bp.route('/admin/predictions')
@login_required
@admin_required
def predictions():
    page  = request.args.get('page', 1, type=int)
    preds = Prediction.query.order_by(Prediction.created_at.desc())\
            .paginate(page=page, per_page=15, error_out=False)
    return render_template('admin/predictions.html', predictions=preds)