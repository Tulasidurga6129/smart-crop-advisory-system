# 🌾 Crop Yield Prediction Module

## Team Member 4 – Smart Crop Advisory System

This module predicts crop yield using machine learning based on crop, location, weather, and agricultural input data.

---

## 🎯 Objective

The objective of this module is to predict the expected crop yield using historical agricultural and environmental data.

The prediction model can be integrated with the Smart Crop Advisory System so that farmers can enter crop and field information and receive an estimated yield.

---

## 📊 Dataset

The dataset contains 19,689 records and 13 columns.

### Input Features

- Crop
- Crop Year
- Season
- State
- Area
- Annual Rainfall
- Fertilizer
- Pesticide
- Average Temperature
- Maximum Temperature
- Minimum Temperature

### Target Variable

- Yield

---

## 🤖 Machine Learning Model

### Algorithm

Random Forest Regressor

### Preprocessing

Categorical features:

- Crop
- Season
- State

These features are converted into numerical features using One-Hot Encoding.

Numerical features are passed directly to the model.

---

## 🔄 Model Workflow

```text
Agricultural Dataset
        ↓
Data Preparation
        ↓
Feature Selection
        ↓
One-Hot Encoding
        ↓
Train/Test Split
        ↓
Random Forest Regressor
        ↓
Model Training
        ↓
Yield Prediction