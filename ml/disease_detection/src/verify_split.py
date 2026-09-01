from pathlib import Path

from src.config import DATASET_DIR


SPLIT_DIR = DATASET_DIR.parent / "split_dataset"


def count_images(folder):
    extensions = {".jpg", ".jpeg", ".png"}

    return sum(
        1
        for file in folder.rglob("*")
        if file.is_file() and file.suffix.lower() in extensions
    )


if __name__ == "__main__":

    print("\n===== SPLIT VERIFICATION =====\n")

    for split in ["train", "val", "test"]:

        split_path = SPLIT_DIR / split

        if not split_path.exists():
            print(f"{split}: NOT FOUND")
            continue

        classes = [
            directory
            for directory in split_path.iterdir()
            if directory.is_dir()
        ]

        image_count = count_images(split_path)

        print(
            f"{split.upper():5s} | "
            f"Classes: {len(classes):2d} | "
            f"Images: {image_count:5d}"
        )

    print("\n==============================")