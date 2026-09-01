from pathlib import Path

import numpy as np
import tensorflow as tf

from src.data_loader import create_train_val_test_datasets


MODEL_PATH = "models/best_model.keras"


def main():
    print("\n===== STEP 23: MODEL EVALUATION =====\n")

    # Load datasets
    (
        _,
        _,
        test_dataset,
        class_names,
        _,
    ) = create_train_val_test_datasets()

    print(f"Classes: {len(class_names)}")

    # Load trained model
    print("\nLoading trained model...")

    model = tf.keras.models.load_model(MODEL_PATH)

    print("Model loaded successfully! ✅")

    # Generate predictions
    print("\nGenerating predictions on test set...")

    predictions = model.predict(
        test_dataset,
        verbose=1,
    )

    predicted_labels = np.argmax(
        predictions,
        axis=1,
    )

    # Get true labels
    true_labels = []

    for _, labels in test_dataset:
        true_labels.extend(labels.numpy())

    true_labels = np.array(true_labels)

    print("\nPredictions generated successfully! ✅")

    # Accuracy
    accuracy = np.mean(
        predicted_labels == true_labels
    )

    print(f"\nTest accuracy: {accuracy:.4f}")
    print(f"Test accuracy: {accuracy * 100:.2f}%")

    # Confusion matrix
    confusion_matrix = tf.math.confusion_matrix(
        true_labels,
        predicted_labels,
        num_classes=len(class_names),
    ).numpy()

    print("\n===== CONFUSION MATRIX =====\n")

    print("Rows = Actual class")
    print("Columns = Predicted class\n")

    print("     ", end="")

    for index in range(len(class_names)):
        print(f"{index:4d}", end="")

    print()

    for index, row in enumerate(confusion_matrix):
        print(f"{index:2d}: ", end="")

        for value in row:
            print(f"{value:4d}", end="")

        print()

    # Per-class metrics
    print("\n===== PER-CLASS METRICS =====\n")

    print(
        f"{'Class':<5}"
        f"{'Name':<55}"
        f"{'Precision':>10}"
        f"{'Recall':>10}"
        f"{'F1':>10}"
    )

    for index, class_name in enumerate(class_names):

        true_positive = confusion_matrix[index, index]

        predicted_positive = confusion_matrix[:, index].sum()

        actual_positive = confusion_matrix[index, :].sum()

        precision = (
            true_positive / predicted_positive
            if predicted_positive > 0
            else 0.0
        )

        recall = (
            true_positive / actual_positive
            if actual_positive > 0
            else 0.0
        )

        if precision + recall > 0:
            f1 = (
                2 * precision * recall
                / (precision + recall)
            )
        else:
            f1 = 0.0

        print(
            f"{index:<5}"
            f"{class_name:<55}"
            f"{precision:>10.4f}"
            f"{recall:>10.4f}"
            f"{f1:>10.4f}"
        )

    # Save confusion matrix
    output_dir = Path("evaluation")
    output_dir.mkdir(exist_ok=True)

    np.savetxt(
        output_dir / "confusion_matrix.csv",
        confusion_matrix,
        delimiter=",",
        fmt="%d",
    )

    print("\nSaved:")
    print("evaluation/confusion_matrix.csv")

    print("\n===== EVALUATION COMPLETE =====")


if __name__ == "__main__":
    main()