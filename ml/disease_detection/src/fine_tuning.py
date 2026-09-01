from pathlib import Path

import tensorflow as tf

from src.class_weights import calculate_class_weights
from src.data_loader import create_train_val_test_datasets


BASE_MODEL_PATH = "models/best_model.keras"
FINETUNED_MODEL_PATH = "models/best_finetuned_model.keras"

LEARNING_RATE = 0.00001
EPOCHS = 10
FINE_TUNE_LAYERS = 30


def main():
    print("\n===== STEP 24: MOBILE NET V2 FINE-TUNING =====\n")

    # --------------------------------------------------
    # Load datasets
    # --------------------------------------------------
    print("Loading datasets...")

    (
        train_dataset,
        validation_dataset,
        test_dataset,
        class_names,
        _,
    ) = create_train_val_test_datasets()

    print(f"Classes: {len(class_names)}")

    # --------------------------------------------------
    # Load the baseline model
    # --------------------------------------------------
    print("\nLoading baseline model...")

    model = tf.keras.models.load_model(
        BASE_MODEL_PATH
    )

    print("Baseline model loaded successfully! ✅")

    # --------------------------------------------------
    # Find MobileNetV2 backbone
    # --------------------------------------------------
    base_model = None

    for layer in model.layers:
        if (
            isinstance(layer, tf.keras.Model)
            and "mobilenetv2" in layer.name.lower()
        ):
            base_model = layer
            break

    if base_model is None:
        raise RuntimeError(
            "MobileNetV2 backbone could not be found."
        )

    print(f"Backbone found: {base_model.name}")
    print(f"Backbone layers: {len(base_model.layers)}")

    # --------------------------------------------------
    # Freeze the entire backbone first
    # --------------------------------------------------
    base_model.trainable = True

    for layer in base_model.layers:
        layer.trainable = False

    # --------------------------------------------------
    # Unfreeze only the last 30 layers
    # --------------------------------------------------
    trainable_count = 0

    for layer in base_model.layers[-FINE_TUNE_LAYERS:]:
        # Keep BatchNormalization layers frozen.
        if not isinstance(
            layer,
            tf.keras.layers.BatchNormalization,
        ):
            layer.trainable = True
            trainable_count += 1

    print(
        f"\nUnfrozen MobileNetV2 layers: "
        f"{trainable_count}"
    )

    # --------------------------------------------------
    # Class weights
    # --------------------------------------------------
    print("\nCalculating class weights...")

    _, class_weights, _ = calculate_class_weights()

    # --------------------------------------------------
    # Recompile with very small learning rate
    # --------------------------------------------------
    optimizer = tf.keras.optimizers.Adam(
        learning_rate=LEARNING_RATE
    )

    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    print("\nModel recompiled for fine-tuning.")
    print(f"Learning rate: {LEARNING_RATE}")

    # --------------------------------------------------
    # Callbacks
    # --------------------------------------------------
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            filepath=FINETUNED_MODEL_PATH,
            monitor="val_accuracy",
            mode="max",
            save_best_only=True,
            verbose=1,
        ),

        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            mode="max",
            patience=3,
            restore_best_weights=True,
            verbose=1,
        ),

        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=1,
            min_lr=1e-7,
            verbose=1,
        ),
    ]

    # --------------------------------------------------
    # Fine-tuning
    # --------------------------------------------------
    print("\n===== STARTING FINE-TUNING =====\n")

    model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=EPOCHS,
        class_weight=class_weights,
        callbacks=callbacks,
    )

    print("\n===== FINE-TUNING COMPLETE =====")

    # --------------------------------------------------
    # Test evaluation
    # --------------------------------------------------
    print("\n===== FINE-TUNED TEST EVALUATION =====\n")

    test_loss, test_accuracy = model.evaluate(
        test_dataset,
        verbose=1,
    )

    print(f"\nFine-tuned test loss     : {test_loss:.4f}")
    print(
        f"Fine-tuned test accuracy : "
        f"{test_accuracy:.4f}"
    )
    print(
        f"Fine-tuned test accuracy : "
        f"{test_accuracy * 100:.2f}%"
    )

    print(
        f"\nFine-tuned model saved to: "
        f"{FINETUNED_MODEL_PATH}"
    )

    print("\n========================================")


if __name__ == "__main__":
    main()