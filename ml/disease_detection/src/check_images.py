from PIL import Image
from src.config import DATASET_DIR

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def check_images():
    total = 0
    valid = 0
    corrupted = []

    for class_dir in sorted(DATASET_DIR.iterdir()):
        if not class_dir.is_dir():
            continue

        for file in class_dir.iterdir():
            if not file.is_file():
                continue

            if file.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            total += 1

            try:
                with Image.open(file) as img:
                    img.verify()

                valid += 1

            except Exception as e:
                corrupted.append((str(file), str(e)))

    print("\n===== IMAGE QUALITY CHECK =====\n")
    print(f"Total images checked : {total}")
    print(f"Valid images         : {valid}")
    print(f"Corrupted images     : {len(corrupted)}")

    if corrupted:
        print("\n===== CORRUPTED FILES =====\n")

        for index, (file, error) in enumerate(corrupted, start=1):
            print(f"{index}. {file}")
            print(f"   Error: {error}")

    else:
        print("\nAll images passed the quality check! ✅")

    print("\n===============================")


if __name__ == "__main__":
    check_images()