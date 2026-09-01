from pathlib import Path

import numpy as np
import tensorflow as tf
from app.services.disease_recommendations import get_recommendation

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "disease_detection"
    / "models"
    / "final_model.keras"
)

IMAGE_SIZE = (224, 224)


# IMPORTANT:
# This order must match the class ordering used during training.
CLASS_NAMES = [
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato__Tomato_YellowLeaf__Curl_Virus",
    "Tomato__Tomato_mosaic_virus",
    "Tomato___Target_Spot",
    "Tomato_healthy",
]

_model = None


# ---------------------------------------------------------
# Model loading
# ---------------------------------------------------------

def get_model():
    global _model

    if _model is None:

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Disease detection model not found: {MODEL_PATH}"
            )

        _model = tf.keras.models.load_model(
            MODEL_PATH,
            compile=False,
        )

    return _model


# ---------------------------------------------------------
# Image preprocessing
# ---------------------------------------------------------

def preprocess_image(image_bytes: bytes) -> tf.Tensor:

    image = tf.io.decode_image(
        image_bytes,
        channels=3,
        expand_animations=False,
    )

    image = tf.image.resize(
        image,
        IMAGE_SIZE,
    )

    image = tf.cast(
        image,
        tf.float32,
    ) / 255.0

    image = tf.expand_dims(
        image,
        axis=0,
    )

    return image


# ---------------------------------------------------------
# Disease name formatting
# ---------------------------------------------------------

def format_disease_name(class_name: str):

    if "__" in class_name:
        plant, disease = class_name.split(
            "__",
            1,
        )

    elif "_healthy" in class_name:
        plant = class_name.replace(
            "_healthy",
            "",
        )

        disease = "healthy"

    else:
        parts = class_name.split(
            "_",
            1,
        )

        if len(parts) == 2:
            plant, disease = parts

        else:
            plant = class_name
            disease = "Unknown"

    plant = plant.replace(
        "_",
        " ",
    ).strip()

    disease = disease.replace(
        "_",
        " ",
    ).strip()

    return plant, disease


# ---------------------------------------------------------
# Prediction
# ---------------------------------------------------------

def predict_disease(image_bytes: bytes):

    model = get_model()

    image = preprocess_image(image_bytes)

    predictions = model.predict(
        image,
        verbose=0,
    )

    predicted_index = int(
        np.argmax(predictions[0])
    )

    confidence = float(
        predictions[0][predicted_index]
    )

    predicted_class = CLASS_NAMES[
        predicted_index
    ]

    recommendation = get_recommendation(
        predicted_class
    )

    return {
        "class_name": predicted_class,
        "plant": recommendation["plant"],
        "disease": recommendation["disease"],
        "confidence": confidence,
        "description": recommendation["description"],
        "treatment": recommendation["treatment"],
        "fertilizer": recommendation["fertilizer"],
        "prevention": recommendation["prevention"],
    }