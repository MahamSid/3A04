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
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Open and convert to RGB
    try:
        img = Image.open(image_path).convert('RGB')
    except Exception as e:
        raise RuntimeError(f"Error loading image: {e}") from e

    # Resize and normalize
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0

    # Add a batch dimension: (1, height, width, 3)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_img(image_path):
    """
    Loads the local model file 'ultrasound_pcos_model.h5' from the same directory,
    preprocesses the input image, and returns the PCOS likelihood percentage.

    Assumes the model's output layer is [PCOS_prob, NotPCOS_prob] via softmax.
    """
    # Build the model path relative to the current file's directory
    model_path = os.path.join(os.path.dirname(__file__), "ultrasound_pcos_model.h5")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")

    # Load the model
    model = tf.keras.models.load_model(model_path)

    # Preprocess the image
    img_array = load_and_preprocess_image(image_path, target_size=(224, 224))

    # Make a prediction (index 0 is "infected" (PCOS) probability)
    predictions = model.predict(img_array)
    pcos_likelihood_percentage = predictions[0][0] * 100.0
    return pcos_likelihood_percentage

def main():
    """
    Example usage of predict_img with a hardcoded image path.
    Modify the path or remove this function if not needed.
    """
    image_path = ""  # <-- Replace with a real file path

    if not os.path.exists(image_path):
        print(f"Error: The file {image_path} does not exist.")
        sys.exit(1)

    try:
        pcos_likelihood_percentage = predict_img(image_path)
        print(f"PCOS Likelihood: {pcos_likelihood_percentage:.2f}%")
    except Exception as e:
        print(f"Prediction error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
