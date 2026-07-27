from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from database.models import Prediction
from user import user_bp


@user_bp.route('/dashboard')
@login_required
def dashboard():
    total_predictions = Prediction.query.filter_by(user_id=current_user.id).count()
    latest = Prediction.query.filter_by(user_id=current_user.id)\
             .order_by(Prediction.created_at.desc()).first()
    return render_template('user/dashboard.html',
                           user=current_user,
                           total_predictions=total_predictions,
                           latest=latest)


@user_bp.route('/history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    predictions = Prediction.query.filter_by(user_id=current_user.id)\
                  .order_by(Prediction.created_at.desc())\
                  .paginate(page=page, per_page=10, error_out=False)
    return render_template('user/history.html',
                           predictions=predictions,
                           user=current_user)


@user_bp.route('/history/delete/<int:prediction_id>', methods=['POST'])
@login_required
def delete_prediction(prediction_id):
    prediction = Prediction.query.get_or_404(prediction_id)
    if prediction.user_id != current_user.id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('user.history'))
    db.session.delete(prediction)
    db.session.commit()
    flash('Prediction deleted.', 'success')
    return redirect(url_for('user.history'))


@user_bp.route('/profile')
@login_required
def profile():
    total_predictions = Prediction.query.filter_by(user_id=current_user.id).count()
    return render_template('user/profile.html',
                           user=current_user,
                           total_predictions=total_predictions)