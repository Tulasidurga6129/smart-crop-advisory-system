import os

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset.csv",
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "yield_model.pkl",
)


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

df = pd.read_csv(DATASET_PATH)


# --------------------------------------------------
# Features
# --------------------------------------------------

FEATURES = [
    "Crop",
    "Crop_Year",
    "Season",
    "State",
    "Area",
    "Annual_Rainfall",
    "Avg_Temperature",
    "Max_Temperature",
    "Min_Temperature",
]

TARGET = "Yield"


X = df[FEATURES]
y = df[TARGET]


# --------------------------------------------------
# Categorical and numerical features
# --------------------------------------------------

CATEGORICAL_FEATURES = [
    "Crop",
    "Season",
    "State",
]

NUMERICAL_FEATURES = [
    "Crop_Year",
    "Area",
    "Annual_Rainfall",
    "Avg_Temperature",
    "Max_Temperature",
    "Min_Temperature",
]


# --------------------------------------------------
# Preprocessing
# --------------------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            CATEGORICAL_FEATURES,
        ),
        (
            "numerical",
            "passthrough",
            NUMERICAL_FEATURES,
        ),
    ]
)


# --------------------------------------------------
# Model
# --------------------------------------------------

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
)


pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor,
        ),
        (
            "model",
            model,
        ),
    ]
)


# --------------------------------------------------
# Train/Test Split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)


print("=" * 60)
print("Crop Yield Prediction Model Training")
print("=" * 60)

print(f"Dataset rows      : {len(df)}")
print(f"Training rows     : {len(X_train)}")
print(f"Testing rows      : {len(X_test)}")
print(f"Features          : {len(FEATURES)}")
print(f"Target            : {TARGET}")

print()
print("Features used:")
for feature in FEATURES:
    print(f"  - {feature}")


# --------------------------------------------------
# Train
# --------------------------------------------------

print()
print("Training Random Forest model...")

pipeline.fit(
    X_train,
    y_train,
)

print("Training completed.")


# --------------------------------------------------
# Evaluate
# --------------------------------------------------

predictions = pipeline.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions,
)

rmse = mean_squared_error(
    y_test,
    predictions,
) ** 0.5

r2 = r2_score(
    y_test,
    predictions,
)


print()
print("=" * 60)
print("Model Evaluation")
print("=" * 60)

print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")


# --------------------------------------------------
# Save model
# --------------------------------------------------

joblib.dump(
    pipeline,
    MODEL_PATH,
)

print()
print("=" * 60)
print("Model saved successfully")
print("=" * 60)
print(f"Path: {MODEL_PATH}")