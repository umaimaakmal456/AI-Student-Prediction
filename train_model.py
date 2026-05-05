import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "student_data.csv"
MODEL_PATH = BASE_DIR / "models" / "student_performance_model.pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"

df = pd.read_csv(DATA_PATH)

X = df[
    [
        "study_hours",
        "attendance",
        "previous_score",
        "sleep_hours",
        "assignments_completed",
        "participation",
        "internet_access",
        "parental_support",
        "extra_classes"
    ]
]

y = df["final_score"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Apply StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Setup GridSearchCV for RandomForest
param_grid = {
    'n_estimators': [100, 150, 200],
    'max_depth': [5, 8, 12, None]
}

rf = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, scoring='neg_mean_absolute_error', n_jobs=-1)

print("Training model with GridSearchCV (5-fold CV)... This may take a few seconds.")
grid_search.fit(X_train_scaled, y_train)

best_model = grid_search.best_estimator_

predictions = best_model.predict(X_test_scaled)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

MODEL_PATH.parent.mkdir(exist_ok=True)
joblib.dump(best_model, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)

print("Model trained successfully!")
print(f"Best Parameters: {grid_search.best_params_}")
print(f"Model saved at: {MODEL_PATH}")
print(f"Scaler saved at: {SCALER_PATH}")
print(f"Mean Absolute Error: {mae:.2f}")
print(f"R2 Score: {r2:.2f}")
