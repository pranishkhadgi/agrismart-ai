# 🌾 AgriSmart AI

A machine learning-powered crop recommendation and yield prediction system built as a BCA Final Year Project.

## Live Demo
[agrismart-ai.onrender.com](https://agrismart-ai.onrender.com)

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

agrismart-ai/
├── app.py # Main Flask app
├── config.py # Configuration
├── extensions.py # DB and login manager
├── auth/ # Authentication blueprint
├── user/ # User routes blueprint
├── admin/ # Admin routes blueprint
├── database/ # SQLAlchemy models
├── data/models/ # Trained .pkl model files
├── templates/ # HTML templates
└── static/ # CSS and JS

## Local Setup
```bash
git clone https://github.com/YOUR_USERNAME/agrismart-ai
cd agrismart-ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`

## Set Admin Account
```bash
python make_admin.py
```

## Dataset
Crop Recommendation Dataset — Kaggle (2,200 samples, 22 crop types, 7 features)

## Project By
BCA Final Year Project — Pranish Khadgi, Padmashree International College, 2026