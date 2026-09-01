import random
import shutil

from pathlib import Path

from src.config import DATASET_DIR


SEED = 42

TRAIN_RATIO = 0.80
VAL_RATIO = 0.10
TEST_RATIO = 0.10

SPLIT_DIR = DATASET_DIR.parent / "split_dataset"


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def split_dataset():
    random.seed(SEED)

    if abs(TRAIN_RATIO + VAL_RATIO + TEST_RATIO - 1.0) > 1e-6:
        raise ValueError("Train, validation and test ratios must add up to 1.")

    if SPLIT_DIR.exists():
        print(f"Removing existing split directory: {SPLIT_DIR}")
        shutil.rmtree(SPLIT_DIR)

    train_dir = SPLIT_DIR / "train"
    val_dir = SPLIT_DIR / "val"
    test_dir = SPLIT_DIR / "test"

    total_images = 0

    print("\n===== DATASET SPLIT =====\n")

    for class_dir in sorted(DATASET_DIR.iterdir()):

        if not class_dir.is_dir():
            continue

        images = [
            image
            for image in class_dir.iterdir()
            if image.is_file()
            and image.suffix.lower() in IMAGE_EXTENSIONS
        ]

        if not images:
            continue

        random.shuffle(images)

        total = len(images)

        train_count = int(total * TRAIN_RATIO)
        val_count = int(total * VAL_RATIO)

        train_images = images[:train_count]
        val_images = images[train_count:train_count + val_count]
        test_images = images[train_count + val_count:]

        for split_name, split_images in [
            ("train", train_images),
            ("val", val_images),
            ("test", test_images),
        ]:

            destination = SPLIT_DIR / split_name / class_dir.name
            destination.mkdir(parents=True, exist_ok=True)

            for image in split_images:
                shutil.copy2(image, destination / image.name)

        total_images += total

        print(
            f"{class_dir.name:<55} "
            f"Train: {len(train_images):4d} | "
            f"Val: {len(val_images):4d} | "
            f"Test: {len(test_images):4d}"
        )

    print("\n========================")
    print(f"Total images : {total_images}")
    print(f"Split folder : {SPLIT_DIR}")
    print("========================\n")


if __name__ == "__main__":
    split_dataset()
    