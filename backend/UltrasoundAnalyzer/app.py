import os
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from predict import predict_img

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/ultrasound_analyzer/predict', methods=['POST'])
def predict_pcos():
    # Check if the request contains the 'image' file
    if 'image' not in request.files:
        return jsonify({'error': 'No image file in request'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    # Save the uploaded file to a temporary directory
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, file.filename)
    file.save(temp_path)

    try:
        # Call predict_img (defined in predict.py) to get the PCOS likelihood percentage
        pcos_likelihood_percentage = predict_img(temp_path)
        # Remove the temporary file after prediction
        os.remove(temp_path)
        return jsonify({'PCOS Likelihood': f"{pcos_likelihood_percentage:.2f}%"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
