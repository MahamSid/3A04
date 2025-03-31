import os
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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