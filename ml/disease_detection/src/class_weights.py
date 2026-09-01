from collections import Counter

from src.config import DATASET_DIR


def calculate_class_weights():
    train_file = "data_splits/train.txt"

    class_counts = Counter()

    with open(train_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            image_path, class_name = line.split("\t")
            class_counts[class_name] += 1

    total_images = sum(class_counts.values())
    num_classes = len(class_counts)

    class_names = sorted(class_counts.keys())

    class_weights = {}

    for index, class_name in enumerate(class_names):
        count = class_counts[class_name]

        weight = total_images / (num_classes * count)

        class_weights[index] = weight

    return class_counts, class_weights, class_names


if __name__ == "__main__":
    counts, class_weights, class_names = calculate_class_weights()

    print("\n===== TRAINING CLASS WEIGHTS =====\n")

    for index, class_name in enumerate(class_names):
        print(
            f"{index:2d}. "
            f"{class_name:<55} "
            f"images={counts[class_name]:5d} "
            f"weight={class_weights[index]:.4f}"
        )

    print("\n==================================")
    print(f"Training images : {sum(counts.values())}")
    print(f"Classes         : {len(class_names)}")