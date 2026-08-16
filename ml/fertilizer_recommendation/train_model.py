import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# 1. Load Dataset
df = pd.read_csv("fertilizer_prediction.csv")

print("Dataset Shape:", df.shape)


# 2. Clean Column Names
df.columns = df.columns.str.strip()

df = df.rename(columns={
    "Temparature": "Temperature",
    "Phosphorous": "Phosphorus"
})


# 3. Separate Features and Target
X = df.drop("Fertilizer Name", axis=1)
y = df["Fertilizer Name"]


# 4. Define Features
categorical_features = [
    "Soil Type",
    "Crop Type"
]

numeric_features = [
    "Temperature",
    "Humidity",
    "Moisture",
    "Nitrogen",
    "Potassium",
    "Phosphorus"
]


# 5. Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# 6. Create Random Forest Model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)


# 7. Create Pipeline
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# 8. Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# 9. Train Model
print("\nTraining Fertilizer Recommendation Model...")

pipeline.fit(X_train, y_train)


# 10. Evaluate Model
y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Evaluation")
print("------------------------")
print("Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# 11. Save Model
joblib.dump(
    pipeline,
    "fertilizer_model.pkl"
)

print("\nModel saved successfully as fertilizer_model.pkl")