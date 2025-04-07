from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from account_system.account_system.account_login import AccountLogin
from uploadResults.discussUltrasound import discussUltrasound
from uploadResults.discussSymptoms import discussSymptoms
from uploadResults.discussBloodTest import discussBloodTest

app = Flask(__name__)

# Enable CORS globally. If you know the exact origin (e.g. http://localhost:3000),
# replace '*' with that specific origin for better security:
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def index():
    users = [{'id': 1, 'username': 'test1'}]
    return jsonify({'response': users})

@app.route('/SymptomUploadResults', methods=['POST'])
def SymptomUploadResults():
    incomingReq = request.get_json()
    result = discussSymptoms(incomingReq).uploadUserSymptom()
    response = make_response(result)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/UltrasoundAnalyzer/UploadResults', methods=['POST'])
def UltrasoundUploadResults():
    result = discussUltrasound(request).uploadUltrasound()
    response = make_response(result)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/BloodTestUploadResults', methods=['POST'])
def BloodTestUploadResults():
    incomingReq = request.get_json()
    uploadblood = discussBloodTest(incomingReq).uploadUserBloodTest()
    return uploadblood

@app.route('/api/calculateLikelihood', methods=['POST'])
def calculate_likelihood():
    from calculateResults.likelihood_calculation_service import LikelihoodCalculationService
    
    lcs = LikelihoodCalculationService()
    symp_score = lcs.get_symptoms_score()
    bt_score = lcs.get_blood_test_score()
    us_score = lcs.get_ultrasound_score()
    overall_score = lcs.receive_overall_score(symp_score, bt_score, us_score)
    lcs.sendToDB(overall_score, symp_score, bt_score, us_score)
    
    return jsonify({"success": True, "message": "Likelihood calculated and stored."})

@app.route("/api/getResults", methods=["GET"])
def get_results():
    from results_viewer_service import ResultsViewerService
    rvs = ResultsViewerService()
    results_data = rvs.get_results_and_recommendation()
    return jsonify(results_data)

@app.route('/LoginAttempt', methods=['POST'])
def LoginAttempt():
    # Example static credentials for testing
    user = AccountLogin('Sfwre12', '3rdYear!')
    result = user.login()
    return {"Test": result}

if __name__ == "__main__":
    app.run(debug=True)
