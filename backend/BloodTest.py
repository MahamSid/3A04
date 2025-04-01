import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)

CORS(app)

dataFile = '/Users/amalhamid/Desktop/blood_test_results.csv'

def receiveUserInput():
    blood_test_results = pd.read_csv('/Users/amalhamid/Desktop/blood_test_results.csv')
    recent_input = blood_test_results.iloc[-1]
    glucose = float(recent_input['Glucose'])
    testosterone = float(recent_input['Testosterone'])
    bile_salts = float(recent_input['Bile_Salts'])
    userBloodTests = [glucose, testosterone, bile_salts]
    return userBloodTests

def getUserGlucoseBT(Glucose):
    return Glucose

def getUserTestosteroneBT(Testosterone):
    return Testosterone

def getUserBileSaltBT(Bile_Salts):
    return Bile_Salts

def calculatePCOSfromBT(userBloodTests):
    glucose = userBloodTests[0]
    testosterone = userBloodTests[1]
    bile_salts = userBloodTests[2]

    if glucose < 7:
        riskG = 0
    else:
        riskG = ((glucose - 7.0)/3.0)*33.0
    if testosterone < 70:
        riskT = 0
    else:
        riskT = ((testosterone - 70.0)/30.0)*33.0
    if bile_salts < 1181.14:
        riskBS = 0
    else:
        riskBS = ((bile_salts - 1181.14)/300.0)*34.0
    
    riskTotal = round(min((riskG + riskT + riskBS), 100), 2)
    return riskTotal



@app.route('/post', methods=['POST'])
def submitTestResults():
    print("📩 Received POST request!")
    data = request.json
    glucose = float(data.get('glucose'))
    testosterone = float(data.get('testosterone'))
    bileSalts = float(data.get('bileSalts'))
    
    newUserTestResultInput = {'Glucose': glucose, 'Testosterone': testosterone, 'Bile_Salts': bileSalts}
    newUserTestResultInputFrame = pd.DataFrame([newUserTestResultInput])
    if os.path.exists(dataFile):
        file = pd.read_csv(dataFile)
        df = pd.concat([file, newUserTestResultInputFrame], ignore_index=True)
    else:
        df = newUserTestResultInputFrame
        
    df.to_csv(dataFile, index=False)
    print("data saved to CSV!!!!!**************************************************************************************")
if __name__ == "__main__":
    userBloodTests = receiveUserInput()
    finalProbability = calculatePCOSfromBT(userBloodTests)
    print(f"\nPCOS Blood Test Probability: {finalProbability}%")
    if finalProbability < 33:
        print("Low Probability")
    elif finalProbability >= 33 and finalProbability < 66:
        print("Medium Probability")
    else:
        print("High Probability")

    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)


