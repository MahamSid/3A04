# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import pandas as pd
# import os
# app = Flask(__name__)

# CORS(app)

# dataFile = 'blood_test_results.csv'
# @app.route('/post', methods=['POST'])
# def submitTestResults():
#     data = request.json
#     glucose = float(data.get('glucose'))
#     testosterone = float(data.get('testosterone'))
#     bileSalts = float(data.get('bileSalts'))
    
#     newUserTestResultInput = {'Glucose': glucose, 'Testosterone': testosterone, 'Bile_Salts': bileSalts}
#     newUserTestResultInputFrame = pd.DataFrame([newUserTestResultInput])
#     if os.path.exists(dataFile):
#         file = pd.read_csv(dataFile)
#         df = pd.concat([file, newUserTestResultInputFrame], ignore_index=True)
#     else:
#         df = newUserTestResultInputFrame

#     df.to_csv(dataFile, index=False)

# if __name__ == "__main__":
#     app.run(debug=True)