import os
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from predict import predict_img

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/ultrasound_analyzer/predict', methods=['GET'])
def predict_pcos():
    temp_path = 'last_upload_img.jpg'
    try:
        # Call predict_img (defined in predict.py) to get the PCOS likelihood percentage
        pcos_likelihood_percentage = predict_img(temp_path)
        return jsonify({'PCOS Likelihood': f"{pcos_likelihood_percentage:.2f}%"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ultrasound_analyzer/uploadImage', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No file part'
    file = request.files['image']
    #save in a temp directory with name last_upload_img.jpg
    file.save('last_upload_img.jpg')
    return jsonify(200,{'success': 'Image uploaded successfully'})

if __name__ == '__main__':
    app.run(debug=True)


#TODO: Save image locally and have predict look at that image

#80% of course evals for 3s03