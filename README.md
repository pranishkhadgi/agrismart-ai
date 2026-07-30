# 🌾 AgriSmart AI

A machine learning-powered crop recommendation and yield prediction system built as a BCA Final Year Project.

## Live Demo
[agrismart-ai-034z.onrender.com](https://agrismart-ai-034z.onrender.com/)

## What it does
- **Recommends the best crop** based on soil nutrients and climate data
- **Predicts expected yield** in kg/hectare
- **Identifies farming zone** using unsupervised clustering
- **User accounts** with prediction history
- **Admin panel** for managing users, crop data, and ML models

## The 3 AI Algorithms

| Algorithm | Type | Role |
|---|---|---|
| Random Forest | Supervised — Classification | Crop recommendation |
| Linear Regression | Supervised — Regression | Yield prediction |
| K-Means Clustering | Unsupervised | Farming zone classification |

## Tech Stack
- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login
- **ML:** scikit-learn, pandas, numpy, joblib
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Render

## Project Structure

```text
agrismart-ai/
│
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── extensions.py               # DB and login manager
├── make_admin.py               # Script to assign admin role
├── requirements.txt            # Python dependencies
│
├── auth/                       # Authentication blueprint
│   ├── __init__.py
│   └── routes.py
│
├── user/                       # User routes blueprint
│   ├── __init__.py
│   └── routes.py
│
├── admin/                      # Admin routes blueprint
│   ├── __init__.py
│   └── routes.py
│
├── database/                   # SQLAlchemy models
│   ├── __init__.py
│   └── models.py
│
├── data/
│   ├── Crop_recommendation.csv
│   └── models/                 # Trained .pkl model files
│       ├── random_forest_model.pkl
│       ├── linear_regression_model.pkl
│       ├── kmeans_model.pkl
│       ├── scaler.pkl
│       └── label_encoder.pkl
│
├── templates/
│   ├── base.html
│   ├── landing.html
│   ├── predict.html
│   ├── result.html
│   ├── about.html
│   ├── 404.html
│   ├── auth/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── change_password.html
│   ├── user/
│   │   ├── dashboard.html
│   │   ├── history.html
│   │   └── profile.html
│   └── admin/
│       ├── admin_dashboard.html
│       ├── users.html
│       ├── crops.html
│       ├── models.html
│       └── predictions.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
└── notebooks/
    └── training.ipynb          # Model training notebook
...
```

## Local Setup

```bash
# Clone the repository
git clone https://github.com/pranishkhadgi/agrismart-ai
cd agrismart-ai

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

---

## Set Admin Account
```bash
python make_admin.py
```

## Dataset

- **Name:** Crop Recommendation Dataset
- **Source:** Kaggle
- **Size:** 2,200 samples, 22 crop types, 7 features
- **Features:** Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, Rainfall

---

## Project By
BCA Final Year Project — Pranish Khadgi, Padmashree International College, 2026