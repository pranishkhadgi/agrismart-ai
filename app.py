from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

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
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
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
        zone_num      = kmeans.predict(sample_scaled)[0]
        zone_name     = ZONE_LABELS[zone_num]

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
        return f"<h3>Error: {str(e)}</h3><a href='/'>Go back</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))