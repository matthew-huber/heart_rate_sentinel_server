from flask import Flask, jsonify, request
from db_patient import Patient
app = Flask(__name__)

@app.route("/api/new_patient", methods = ["POST"])
def new_patient():
    patient_data = request.get_json()
    pat_id = patient_data["patient_id"]
    email = patient_data["attending_email"]
    age = patient_data["user_age"]
    pat_to_add = Patient(patient_id = pat_id, attending_email = email, user_age = age)
    pat_to_add.save()
    
    return 0
