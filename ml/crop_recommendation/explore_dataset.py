import pandas as pd

# Load the dataset
df = pd.read_csv("data/crop_recommendation.csv")

# Show basic information
print("Dataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nCrop Count:")
print(df["label"].value_counts())