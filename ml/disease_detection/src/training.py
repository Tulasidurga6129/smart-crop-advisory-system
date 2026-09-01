from pathlib import Path

import tensorflow as tf

from src.class_weights import calculate_class_weights
from src.data_loader import create_train_val_test_datasets
from src.model import create_model


LEARNING_RATE = 0.001
EPOCHS = 20


def compile_model(model):
    optimizer = tf.keras.optimizers.Adam(
        learning_rate=LEARNING_RATE
    )

    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


def main():
    print("\n===== STEP 22: MODEL TRAINING =====\n")

    # Create output directory
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)

    # Load datasets
    print("Loading datasets...")

    (
        train_dataset,
        validation_dataset,
        test_dataset,
        class_names,
        class_to_index,
    ) = create_train_val_test_datasets()

    print(f"Classes: {len(class_names)}")
    print(f"Class names: {class_names}")

    # Calculate class weights from training split
    print("\nCalculating class weights...")

    _, class_weights, _ = calculate_class_weights()

    print("Class weights:")
    for class_index, weight in class_weights.items():
        print(
            f"{class_index:2d} -> "
            f"{class_names[class_index]:<55} "
            f"{weight:.4f}"
        )

    # Create model
    print("\nCreating MobileNetV2 model...")

    model = create_model()

    # Compile model
    model = compile_model(model)

    print("\nModel compiled successfully.")

    # Callbacks
    checkpoint_path = model_dir / "best_model.keras"

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(checkpoint_path),
            monitor="val_accuracy",
            mode="max",
            save_best_only=True,
            verbose=1,
        ),

        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            mode="max",
            patience=5,
            restore_best_weights=True,
            verbose=1,
        ),

        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2,
            min_lr=1e-6,
            verbose=1,
        ),
    ]

    print("\n===== STARTING TRAINING =====\n")

    history = model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=EPOCHS,
        class_weight=class_weights,
        callbacks=callbacks,
    )

    print("\n===== TRAINING COMPLETE =====")

    print(f"Best model saved to: {checkpoint_path}")

    # Evaluate on test data
    print("\n===== TEST EVALUATION =====\n")

    test_loss, test_accuracy = model.evaluate(
        test_dataset,
        verbose=1,
    )

    print(f"\nTest loss     : {test_loss:.4f}")
    print(f"Test accuracy : {test_accuracy:.4f}")

    print("\n================================")


if __name__ == "__main__":
    main()