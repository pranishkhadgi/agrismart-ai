"""
Computes the real evaluation numbers for Table 4.7 (Linear Regression) and the
K-Means Clustering Evaluation section of the report.

This mirrors data/training.ipynb exactly (same features, same random_state=42
train/test split, same k=4 for KMeans), but adds a fixed seed to the synthetic
yield-noise step so the numbers are reproducible run-to-run.
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score, silhouette_score
)

df = pd.read_csv(r"D:\Not Backed up\Study Materials\BCA\8th Semester\Project\agrismart-ai\data\Crop_recommendation.csv")

# ---- Linear Regression (yield prediction) ----
np.random.seed(42)  # fixed so results are reproducible for the report
df['yield_kg'] = (
    df['N'] * 2.1 +
    df['P'] * 1.8 +
    df['K'] * 1.5 +
    df['rainfall'] * 0.9 +
    np.random.normal(0, 50, len(df))
).round(1)

X_yield = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y_yield = df['yield_kg']

X_train_y, X_test_y, y_train_y, y_test_y = train_test_split(
    X_yield, y_yield, test_size=0.2, random_state=42
)

lr_model = LinearRegression()
lr_model.fit(X_train_y, y_train_y)
y_pred_y = lr_model.predict(X_test_y)

mae = mean_absolute_error(y_test_y, y_pred_y)
mse = mean_squared_error(y_test_y, y_pred_y)
rmse = np.sqrt(mse)
r2 = r2_score(y_test_y, y_pred_y)

print("=== Table 4.7 — Linear Regression Evaluation ===")
print(f"Train samples: {X_train_y.shape[0]}")
print(f"Test samples:  {X_test_y.shape[0]}")
print(f"MAE:  {mae:.4f}")
print(f"MSE:  {mse:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R2 score: {r2:.4f}")

# ---- K-Means Clustering ----
X = df.drop(columns=['label', 'yield_kg'])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

k = 4
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)
sil = silhouette_score(X_scaled, labels)
inertia = kmeans.inertia_

print("\n=== K-Means Clustering Evaluation ===")
print(f"Chosen k: {k}")
print(f"Silhouette Score: {sil:.4f}")
print(f"Inertia: {inertia:.4f}")
