import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# Load dataset
df = pd.read_csv("data/crop_recommendation.csv")


# Separate input features and target
X = df.drop("label", axis=1)
y = df["label"]


print("Input features:")
print(X.columns.tolist())

print("\nTarget:")
print(y.name)

print("\nInput shape:")
print(X.shape)

print("\nTarget shape:")
print(y.shape)


# Split the dataset into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print("\nTraining data:")
print(X_train.shape)

print("\nTesting data:")
print(X_test.shape)


# Create the Random Forest model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)


# Train the model
model.fit(X_train, y_train)

print("\nModel training completed!")


# Make predictions on the test data
y_pred = model.predict(X_test)


# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:")
print(accuracy)

print("\nModel Accuracy Percentage:")
print(f"{accuracy * 100:.2f}%")


# Show detailed classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
# Save the trained model
joblib.dump(model, "models/crop_model.pkl")

print("\nModel saved successfully!")