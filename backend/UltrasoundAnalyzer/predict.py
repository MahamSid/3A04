import os
import sys
import numpy as np
import tensorflow as tf
from PIL import Image

def load_and_preprocess_image(image_path, target_size=(224, 224)):
    """
    Loads an image from the given path, converts it to RGB, resizes it,
    and scales pixel values to [0, 1].
    """
    try:
        img = Image.open(image_path).convert('RGB')
    except Exception as e:
        print(f"Error loading image: {e}")
        sys.exit(1)
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0
    # Expand dims to create a batch of size 1.
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def main():
    # Hardcoded image path; update this to the path of your test image.
    image_path = r"dataset/test/notinfected/img4.jpg"  # <-- Update this path

    if not os.path.exists(image_path):
        print(f"Error: The file {image_path} does not exist.")
        sys.exit(1)

    # Load the saved model
    model = tf.keras.models.load_model("ultrasound_pcos_model.h5")

    # Preprocess the image
    img_array = load_and_preprocess_image(image_path, target_size=(224, 224))

    # Make a prediction (output is a 2-element softmax vector)
    predictions = model.predict(img_array)

    # Assuming index 0 is the "infected" (PCOS) probability
    pcos_likelihood_percentage = predictions[0][0] * 100.0

    # Print the PCOS likelihood as a percentage (double)
    print(f"PCOS Likelihood: {pcos_likelihood_percentage:.2f}%")

if __name__ == "__main__":
    main()
