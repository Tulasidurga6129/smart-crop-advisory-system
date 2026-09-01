from pathlib import Path

import tensorflow as tf

from src.config import DATASET_DIR
from src.data_loader import load_datasets
from src.model import build_model
from src.class_weights import calculate_class_weights


EPOCHS = 20

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

BEST_MODEL_PATH = MODEL_DIR / "best_model.keras"


def train():

    print("\n===== LOADING DATASETS =====\n")

    (
        train_dataset,
        validation_dataset,
        test_dataset,
        class_names
    ) = load_datasets()

    print("\n===== CALCULATING CLASS WEIGHTS =====\n")

    class_weights = calculate_class_weights()

    print("\n===== BUILDING MODEL =====\n")

    model = build_model(
        num_classes=len(class_names)
    )

    model.summary()

    print("\n===== CONFIGURING CALLBACKS =====\n")

    callbacks = [

        tf.keras.callbacks.ModelCheckpoint(
            filepath=BEST_MODEL_PATH,
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
            verbose=1
        ),

        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),

        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.2,
            patience=2,
            min_lr=1e-7,
            verbose=1
        )
    ]

    print("\n===== STARTING TRAINING =====\n")

    history = model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=EPOCHS,
        class_weight=class_weights,
        callbacks=callbacks
    )

    print("\n===== TRAINING COMPLETE =====\n")

    print(f"Best model saved to: {BEST_MODEL_PATH}")

    print("\n===== EVALUATING ON TEST DATA =====\n")

    test_loss, test_accuracy = model.evaluate(
        test_dataset,
        verbose=1
    )

    print("\n===== TEST RESULTS =====")
    print(f"Test Loss     : {test_loss:.4f}")
    print(f"Test Accuracy : {test_accuracy:.4f}")
    print("========================\n")

    return history


if __name__ == "__main__":
    train()