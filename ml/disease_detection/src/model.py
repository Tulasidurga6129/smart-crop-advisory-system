import tensorflow as tf


IMG_SIZE = (224, 224)
NUM_CLASSES = 15


def create_model():
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(*IMG_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )

    # Freeze the pretrained feature extractor
    base_model.trainable = False

    inputs = tf.keras.Input(
        shape=(*IMG_SIZE, 3),
        name="image",
    )
    x=tf.keras.layers.Rescaling(
        scale=2.0,offset=1.0,
    )(inputs)

    x = base_model(
        inputs,
        training=False,
    )

    x = tf.keras.layers.GlobalAveragePooling2D()(x)

    x = tf.keras.layers.Dropout(0.30)(x)

    outputs = tf.keras.layers.Dense(
        NUM_CLASSES,
        activation="softmax",
        name="predictions",
    )(x)

    model = tf.keras.Model(
        inputs=inputs,
        outputs=outputs,
        name="plant_disease_mobilenetv2",
    )

    return model


if __name__ == "__main__":
    model = create_model()

    print("\n===== MODEL SUMMARY =====\n")

    model.summary()

    print("\nTrainable parameters:")
    print(model.count_params())

    print("\nModel created successfully! ✅")