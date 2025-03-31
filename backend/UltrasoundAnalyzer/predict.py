import os
import sys
import csv
import base64
import tempfile
import numpy as np
import tensorflow as tf
from PIL import Image

class ultrasoundCalculator:
    def __init__(self, target_size=(224, 224)):
        """
        Initialize the calculator by setting the target image size and loading the model.
        The model file 'ultrasound_pcos_model.h5' must be in the same directory as this script.
        """
        self.target_size = target_size
        self.model_path = os.path.join(os.path.dirname(__file__), "ultrasound_pcos_model.h5")
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at: {self.model_path}")
        self.model = tf.keras.models.load_model(self.model_path)

    def load_and_preprocess_image(self, image_path):
        """
        Loads an image from the given path, converts it to RGB, resizes it,
        and scales pixel values to [0, 1]. Returns an array with shape (1, height, width, 3).
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        try:
            img = Image.open(image_path).convert('RGB')
        except Exception as e:
            raise RuntimeError(f"Error loading image: {e}") from e

        img = img.resize(self.target_size)
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    def predict_img(self, image_path):
        """
        Preprocesses the image and runs the model prediction.
        Returns the PCOS likelihood percentage (float).
        Assumes the model's output is a softmax vector [PCOS_prob, NotPCOS_prob]
        and that the first index corresponds to the "infected" (PCOS) probability.
        """
        img_array = self.load_and_preprocess_image(image_path)
        predictions = self.model.predict(img_array)
        pcos_likelihood_percentage = predictions[0][0] * 100.0
        return pcos_likelihood_percentage

    def predict(self):
        """
        Opens a hardcoded CSV file (named 'hardcoded.csv' in the same directory),
        reads the first row's 'ultrasound_image' column (which should contain a base64
        encoded image), decodes it into a JPG, saves it temporarily, and then runs
        predict_img on the saved file.
        Returns the PCOS likelihood percentage.
        """
        csv_file = os.path.join(os.path.dirname(__file__), "hardcoded.csv")
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")

        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            row = next(reader)  # Read the first row

        if "ultrasound_image" not in row:
            raise ValueError("CSV file does not contain 'ultrasound_image' column")

        base64_str = row["ultrasound_image"]
        try:
            img_data = base64.b64decode(base64_str)
        except Exception as e:
            raise ValueError(f"Error decoding base64 image data: {e}") from e

        # Save the decoded image to a temporary file
        temp_path = os.path.join(tempfile.gettempdir(), "temp_ultrasound.jpg")
        with open(temp_path, "wb") as temp_file:
            temp_file.write(img_data)

        # Run prediction on the temporary file
        result = self.predict_img(temp_path)
        os.remove(temp_path)
        return result

def main():
    try:
        calculator = ultrasoundCalculator()
        pcos_likelihood = calculator.predict()
        print(f"PCOS Likelihood: {pcos_likelihood:.2f}%")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
