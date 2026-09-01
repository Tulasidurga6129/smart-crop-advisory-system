from collections import Counter
from src.config import DATASET_DIR


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def get_class_distribution():
    distribution = {}

    for class_dir in sorted(DATASET_DIR.iterdir()):
        if not class_dir.is_dir():
            continue

        count = sum(
            1
            for file in class_dir.iterdir()
            if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
        )

        distribution[class_dir.name] = count

    return distribution


if __name__ == "__main__":
    distribution = get_class_distribution()

    total = sum(distribution.values())

    print("\n===== DATASET CLASS DISTRIBUTION =====\n")

    for index, (class_name, count) in enumerate(distribution.items()):
        percentage = (count / total) * 100

        print(
            f"{index:2d}. {class_name:<55} "
            f"{count:5d} images ({percentage:5.2f}%)"
        )

    print("\n======================================")
    print(f"Total classes : {len(distribution)}")
    print(f"Total images  : {total}")