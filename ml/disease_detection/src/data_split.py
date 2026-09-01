import random
from pathlib import Path

from src.config import DATASET_DIR


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

SEED = 42


def collect_images():
    data = {}

    for class_dir in sorted(DATASET_DIR.iterdir()):
        if not class_dir.is_dir():
            continue

        images = [
            file
            for file in class_dir.iterdir()
            if file.is_file()
            and file.suffix.lower() in IMAGE_EXTENSIONS
        ]

        if images:
            data[class_dir.name] = images

    return data


def create_split(data):
    random.seed(SEED)

    train_files = []
    val_files = []
    test_files = []

    for class_name, images in data.items():
        images = images.copy()
        random.shuffle(images)

        total = len(images)

        train_end = int(total * TRAIN_RATIO)
        val_end = train_end + int(total * VAL_RATIO)

        train = images[:train_end]
        val = images[train_end:val_end]
        test = images[val_end:]

        train_files.extend((str(path), class_name) for path in train)
        val_files.extend((str(path), class_name) for path in val)
        test_files.extend((str(path), class_name) for path in test)

    random.shuffle(train_files)
    random.shuffle(val_files)
    random.shuffle(test_files)

    return train_files, val_files, test_files


def save_split(files, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for image_path, class_name in files:
            f.write(f"{image_path}\t{class_name}\n")


if __name__ == "__main__":
    data = collect_images()

    train_files, val_files, test_files = create_split(data)

    output_dir = Path("data_splits")
    output_dir.mkdir(exist_ok=True)

    save_split(train_files, output_dir / "train.txt")
    save_split(val_files, output_dir / "validation.txt")
    save_split(test_files, output_dir / "test.txt")

    print("\n===== DATASET SPLIT =====\n")

    print(f"Classes            : {len(data)}")
    print(f"Training images    : {len(train_files)}")
    print(f"Validation images  : {len(val_files)}")
    print(f"Test images        : {len(test_files)}")
    print(
        f"Total images       : "
        f"{len(train_files) + len(val_files) + len(test_files)}"
    )

    print("\nSplit ratio:")
    print("Training   : 70%")
    print("Validation : 15%")
    print("Test       : 15%")

    print("\nFiles created:")
    print("data_splits/train.txt")
    print("data_splits/validation.txt")
    print("data_splits/test.txt")

    print("\n========================")