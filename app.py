from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from config import Config
from extensions import db, login_manager
from database.models import User
import joblib
import numpy as np
import pandas as pd
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from auth import auth as auth_blueprint
    from user import user_bp as user_blueprint
    from admin import admin_bp as admin_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)

    BASE = os.path.dirname(os.path.abspath(__file__))

    rf_model = joblib.load(os.path.join(BASE, 'data/models/random_forest_model.pkl'))
    lr_model = joblib.load(os.path.join(BASE, 'data/models/linear_regression_model.pkl'))
    kmeans   = joblib.load(os.path.join(BASE, 'data/models/kmeans_model.pkl'))
    scaler   = joblib.load(os.path.join(BASE, 'data/models/scaler.pkl'))
    le       = joblib.load(os.path.join(BASE, 'data/models/label_encoder.pkl'))

    ZONE_LABELS = {
        0: "Zone 1 — Humid Fertile",
        1: "Zone 2 — Dry Arid",
        2: "Zone 3 — Moderate Temperate",
        3: "Zone 4 — High Rainfall"
    }

    CROP_INFO = {
        "rice":        {"emoji": "🌾", "tip": "Best grown in waterlogged fields with high humidity."},
        "maize":       {"emoji": "🌽", "tip": "Needs well-drained soil and moderate rainfall."},
        "chickpea":    {"emoji": "🫘", "tip": "Thrives in cool, dry climates with low humidity."},
        "kidneybeans": {"emoji": "🫘", "tip": "Requires fertile, well-drained loamy soil."},
        "pigeonpeas":  {"emoji": "🌿", "tip": "Drought-tolerant, grows well in semi-arid zones."},
        "mothbeans":   {"emoji": "🌿", "tip": "Suited for hot, arid regions with sandy soil."},
        "mungbean":    {"emoji": "🌿", "tip": "Short duration crop, good for crop rotation."},
        "blackgram":   {"emoji": "🌿", "tip": "Grows well in tropical and subtropical climates."},
        "lentil":      {"emoji": "🫘", "tip": "Prefers cool weather and well-drained soil."},
        "pomegranate": {"emoji": "🍎", "tip": "Drought-hardy, thrives in semi-arid conditions."},
        "banana":      {"emoji": "🍌", "tip": "Needs high humidity, warmth, and rich soil."},
        "mango":       {"emoji": "🥭", "tip": "Grows best in tropical climates with dry winters."},
        "grapes":      {"emoji": "🍇", "tip": "Needs well-drained soil and a long warm season."},
        "watermelon":  {"emoji": "🍉", "tip": "Loves sandy loam soil and warm temperatures."},
        "muskmelon":   {"emoji": "🍈", "tip": "Thrives in hot, dry weather with sandy soil."},
        "apple":       {"emoji": "🍏", "tip": "Requires cold winters and mild summers."},
        "orange":      {"emoji": "🍊", "tip": "Grows well in subtropical climates."},
        "papaya":      {"emoji": "🍈", "tip": "Fast-growing, needs warm humid conditions."},
        "coconut":     {"emoji": "🥥", "tip": "Thrives in coastal tropical regions."},
        "cotton":      {"emoji": "🌿", "tip": "Needs long frost-free season and moderate rain."},
        "jute":        {"emoji": "🌿", "tip": "Grows best in warm humid climates near rivers."},
        "coffee":      {"emoji": "☕", "tip": "Thrives in high-altitude tropical regions."},
    }

    @app.route('/')
    def landing():
        return render_template('landing.html')

    @app.route('/predict', methods=['GET', 'POST'])
    @login_required
    def predict():
        if request.method == 'POST':
            try:
                from database.models import Prediction

                N           = float(request.form['N'])
                P           = float(request.form['P'])
                K           = float(request.form['K'])
                temperature = float(request.form['temperature'])
                humidity    = float(request.form['humidity'])
                ph          = float(request.form['ph'])
                rainfall    = float(request.form['rainfall'])

                sample = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]],
                                       columns=['N','P','K','temperature','humidity','ph','rainfall'])

                crop_encoded = rf_model.predict(sample)[0]
                crop_name    = le.inverse_transform([crop_encoded])[0]
                crop_prob    = round(rf_model.predict_proba(sample)[0].max() * 100, 1)
                predicted_yield = round(lr_model.predict(sample)[0], 1)
                sample_scaled = scaler.transform(sample)
                zone_num      = int(kmeans.predict(sample_scaled)[0])
                zone_name     = ZONE_LABELS[zone_num]

                prediction = Prediction(
                    user_id=current_user.id,
                    N=N, P=P, K=K,
                    temperature=temperature,
                    humidity=humidity,
                    ph=ph,
                    rainfall=rainfall,
                    crop=crop_name.title(),
                    confidence=crop_prob,
                    yield_kg=predicted_yield,
                    zone=zone_name
                )
                db.session.add(prediction)
                db.session.commit()

                crop_emoji = CROP_INFO.get(crop_name, {}).get("emoji", "🌱")
                crop_tip   = CROP_INFO.get(crop_name, {}).get("tip", "")

                return render_template('result.html',
                    crop=crop_name.title(),
                    crop_emoji=crop_emoji,
                    crop_tip=crop_tip,
                    confidence=crop_prob,
                    yield_kg=predicted_yield,
                    zone=zone_name,
                    zone_num=zone_num,
                    inputs={"N": N, "P": P, "K": K, "Temp": temperature,
                            "Humidity": humidity, "pH": ph, "Rainfall": rainfall}
                )

            except Exception as e:
                flash(f'Prediction error: {str(e)}', 'danger')
                return redirect(url_for('predict'))

        return render_template('predict.html')

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)