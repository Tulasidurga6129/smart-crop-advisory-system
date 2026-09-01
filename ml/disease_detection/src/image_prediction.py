import sys

import numpy as np
import tensorflow as tf

from src.data_loader import get_class_names
from src.recommendations import get_recommendation


MODEL_PATH = "models/final_model.keras"
IMAGE_SIZE = (224, 224)


def load_model():
    print("Loading disease detection model...")

    model = tf.keras.models.load_model(MODEL_PATH)

    print("Model loaded successfully!")

    return model


def preprocess_image(image_path):
    image = tf.io.read_file(image_path)

    image = tf.image.decode_image(
        image,
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


def format_disease_name(class_name):

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


def predict_disease(image_path):

    model = load_model()

    class_names = get_class_names()

    image = preprocess_image(
        image_path
    )

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

    predicted_class = class_names[
        predicted_index
    ]

    plant, disease = format_disease_name(
        predicted_class
    )

    recommendation = get_recommendation(
        predicted_class
    )

    return {
        "class_name": predicted_class,
        "plant": plant,
        "disease": disease,
        "confidence": confidence,
        "recommendation": recommendation,
    }


def main():

    if len(sys.argv) < 2:

        print()
        print("Usage:")
        print(
            'python -m src.image_prediction "image_path"'
        )

        return

    image_path = sys.argv[1]

    print()
    print("========================================")
    print("       SMART CROP ADVISORY")
    print("========================================")
    print()

    print(
        f"Image: {image_path}"
    )

    print()

    try:

        result = predict_disease(
            image_path
        )

        recommendation = result[
            "recommendation"
        ]

        print(
            "========== DISEASE RESULT =========="
        )

        print()

        print(
            f"Plant      : {result['plant']}"
        )

        print(
            f"Disease    : {result['disease']}"
        )

        print(
            f"Confidence : "
            f"{result['confidence'] * 100:.2f}%"
        )

        print(
            f"Class      : {result['class_name']}"
        )

        print()

        if result["confidence"] >= 0.80:

            print(
                "Confidence level: HIGH"
            )

        elif result["confidence"] >= 0.60:

            print(
                "Confidence level: MODERATE"
            )

        else:

            print(
                "Confidence level: LOW"
            )

        print()

        print(
            "========== DISEASE INFORMATION =========="
        )

        print()

        print(
            recommendation["description"]
        )

        print()

        print(
            "========== TREATMENT =========="
        )

        for item in recommendation[
            "treatment"
        ]:

            print(
                f"- {item}"
            )

        print()

        print(
            "========== FERTILIZER / NUTRIENTS =========="
        )

        print(
            recommendation["fertilizer"]
        )

        print()

        print(
            "========== PREVENTION =========="
        )

        for item in recommendation[
            "prevention"
        ]:

            print(
                f"- {item}"
            )

        print()

        print(
            "========================================"
        )

    except Exception as e:

        print()

        print(
            "Prediction failed."
        )

        print(
            f"Error: {e}"
        )


if __name__ == "__main__":

    main()