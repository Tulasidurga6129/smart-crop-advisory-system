from pathlib import Path
import tensorflow as tf

from src.config import (
    DATASET_DIR,
    IMAGE_SIZE,
    BATCH_SIZE,
    RANDOM_SEED,
    VALIDATION_SPLIT,
)


def get_class_names():
    """Return sorted disease/healthy class names."""
    class_names = sorted(
        [
            directory.name
            for directory in DATASET_DIR.iterdir()
            if directory.is_dir()
        ]
    )

    return class_names


def load_datasets():
    """Load training and validation datasets from PlantVillage."""

    train_dataset = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=VALIDATION_SPLIT,
        subset="training",
        seed=RANDOM_SEED,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=True,
    )

    validation_dataset = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=VALIDATION_SPLIT,
        subset="validation",
        seed=RANDOM_SEED,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False,
    )

    return train_dataset, validation_dataset


if __name__ == "__main__":
    print("Dataset directory:")
    print(DATASET_DIR)

    print("\nDataset exists:")
    print(DATASET_DIR.exists())

    class_names = get_class_names()

    print("\nNumber of classes:")
    print(len(class_names))

    print("\nClasses:")
    for index, class_name in enumerate(class_names):
        print(f"{index}: {class_name}")

    print("\nLoading datasets...")

    train_dataset, validation_dataset = load_datasets()

    print("\nDataset loaded successfully!")

    print("Training batches:", tf.data.experimental.cardinality(train_dataset).numpy())
    print("Validation batches:", tf.data.experimental.cardinality(validation_dataset).numpy())