from flask import Flask, jsonify, request
from db_patient import Patient
import heart_server_helpers
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

    try:
        existing_hr = patient.heart_rate
        existing_hr.append(rate)
        patient.heart_rate = existing_hr

        existing_hr_times = patient.h_r_times
        existing_hr_times.append(datetime.datetime.now())
        patient.h_r_times = existing_hr_times
    except:
        print('exception handled')
        patient.heart_rate = [rate]
        patient.h_r_times = [datetime.datetime.now()]

#    tachycardia = heart_server_helpers.is_tachycardic(pat_id)
#    if tachycardia == False:
#        heart_server_helpers.email_alert(pat_id, rate)

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


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def return_avg_rate(patient_id):
    patient_id = int(patient_id)
    for user in Patient.objects.raw({"_id": patient_id}):
        patient = user

    heartrate_list = patient.heart_rate
    num_rates = len(heartrate_list)

    avg_rate = {"rate_avg": sum(heartrate_list)/num_rates}
    return jsonify(avg_rate)


@app.route("/api/status/<patient_id>", methods=["GET"])
def patient_status(patient_id):
    patient_id = int(patient_id)
    tachycardia = heart_server_helpers.is_tachycardic(patient_id)

    status = {"patient_tachycardic": tachycardia}
    return jsonify(status)


if __name__ == "__main__":
    app.run(host="127.0.0.1")
