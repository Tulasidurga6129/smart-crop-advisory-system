import tensorflow as tf

from src.augmentation import get_train_augmentation


IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
AUTOTUNE = tf.data.AUTOTUNE


def load_split_file(file_path):
    image_paths = []
    class_names = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            image_path, class_name = line.split("\t")

            image_paths.append(image_path)
            class_names.append(class_name)

    return image_paths, class_names


def get_class_names():
    _, class_names = load_split_file("data_splits/train.txt")

    unique_classes = sorted(set(class_names))

    return unique_classes


def create_class_mapping():
    class_names = get_class_names()

    class_to_index = {
        class_name: index
        for index, class_name in enumerate(class_names)
    }

    return class_names, class_to_index


def load_image(image_path, label):
    image = tf.io.read_file(image_path)

    image = tf.image.decode_image(
        image,
        channels=3,
        expand_animations=False,
    )

    image = tf.image.resize(image, IMAGE_SIZE)

    image = tf.cast(image, tf.float32) / 255.0

    return image, label


def create_dataset(
    split_file,
    class_to_index,
    training=False,
):
    image_paths, class_names = load_split_file(split_file)

    labels = [
        class_to_index[class_name]
        for class_name in class_names
    ]

    dataset = tf.data.Dataset.from_tensor_slices(
        (image_paths, labels)
    )

    if training:
        dataset = dataset.shuffle(
            buffer_size=len(image_paths),
            seed=42,
            reshuffle_each_iteration=True,
        )

    dataset = dataset.map(
        load_image,
        num_parallel_calls=AUTOTUNE,
    )

    if training:
        augmentation = get_train_augmentation()

        dataset = dataset.map(
            lambda image, label: (
                augmentation(image, training=True),
                label,
            ),
            num_parallel_calls=AUTOTUNE,
        )

    dataset = dataset.batch(BATCH_SIZE)

    dataset = dataset.prefetch(AUTOTUNE)

    return dataset


def create_train_val_test_datasets():
    class_names, class_to_index = create_class_mapping()

    train_dataset = create_dataset(
        "data_splits/train.txt",
        class_to_index,
        training=True,
    )

    validation_dataset = create_dataset(
        "data_splits/validation.txt",
        class_to_index,
        training=False,
    )

    test_dataset = create_dataset(
        "data_splits/test.txt",
        class_to_index,
        training=False,
    )

    return (
        train_dataset,
        validation_dataset,
        test_dataset,
        class_names,
        class_to_index,
    )


if __name__ == "__main__":
    (
        train_dataset,
        validation_dataset,
        test_dataset,
        class_names,
        class_to_index,
    ) = create_train_val_test_datasets()

    print("\n===== DATA PIPELINE CHECK =====\n")

    print(f"Number of classes : {len(class_names)}")
    print(f"Classes           : {class_names}")

    print("\nClass mapping:")
    for index, class_name in enumerate(class_names):
        print(f"{index:2d} -> {class_name}")

    print("\nChecking training batch...")

    train_images, train_labels = next(iter(train_dataset))

    print(f"Training image shape : {train_images.shape}")
    print(f"Training label shape : {train_labels.shape}")

    print(
        f"Pixel value range    : "
        f"{tf.reduce_min(train_images).numpy():.4f} - "
        f"{tf.reduce_max(train_images).numpy():.4f}"
    )

    print("\nChecking validation batch...")

    val_images, val_labels = next(iter(validation_dataset))

    print(f"Validation image shape : {val_images.shape}")
    print(f"Validation label shape : {val_labels.shape}")

    print("\nChecking test batch...")

    test_images, test_labels = next(iter(test_dataset))

    print(f"Test image shape : {test_images.shape}")
    print(f"Test label shape : {test_labels.shape}")

    print("\nPipeline check completed successfully! ✅")

    print("\n==============================")