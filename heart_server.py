from flask import Flask, jsonify, request
from db_patient import Patient
import datetime
app = Flask(__name__)


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    patient_data = request.get_json()
    pat_id = patient_data["patient_id"]
    email = patient_data["attending_email"]
    age = patient_data["user_age"]
    pat_add = Patient(patient_id=pat_id, attending_email=email, user_age=age)
    pat_add.save()

    return_val = {"status": "true"}
    return jsonify(return_val)


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    heart_data = request.get_json()
    pat_id = heart_data["patient_id"]
    rate = heart_data["heart_rate"]

    for user in Patient.objects.raw({"_id": pat_id}):
        patient = user
    print(patient)
    print(patient.user_age)
    try:
        existing_hr = patient.heart_rate
        existing_hr.append(rate)
        patient.heart_rate = existing_hr

        existing_hr_times = patient.h_r_times
        existing_hr_times.append(datetime.datetime.now())
        patient.h_r_times = existing_hr_times
    except:
        print('excception handled')
        patient.heart_rate = [rate]
        patient.h_r_times = [datetime.datetime.now()]

    print(patient.h_r_times)
    print(patient.heart_rate)

    patient.save()
    return jsonify({"status": "true"})


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def return_heartrates(patient_id):
    patient_id = int(patient_id)
    for user in Patient.objects.raw({"_id": patient_id}):
        patient = user

    heartrate_list = patient.heart_rate
    print(heartrate_list)
    heart_list = {"heat_rates": heartrate_list}
    return jsonify(heart_list)


if __name__ == "__main__":
    app.run(host="127.0.0.1")
