from flask import Flask, jsonify, request
from db_patient import Patient
import heart_server_helpers
import datetime
from email.utils import parseaddr
app = Flask(__name__)


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    """
    add a new patient to the patient database via post

    :return: json indicating success adding patient, or error message
    """
    patient_data = request.get_json()
    pat_id = patient_data["patient_id"]
    email = patient_data["attending_email"]
    age = patient_data["user_age"]

    if not isinstance(pat_id, int):
        return jsonify({"Error": "non-integer entered for patient ID"})
    if not isinstance(age, int):
        return jsonify({"Error": "non-integer entered for age"})
    if age < 1:
        return jsonify({"Error": "age can not be less than 1"})
    valid_email = '@' in parseaddr(email)[1]
    if not valid_email:
        return jsonify({"Error": "invalid email address entered"})

    pat_add = Patient(patient_id=pat_id, attending_email=email, user_age=age)
    pat_add.save()

    return_val = {"status": "true"}
    return jsonify(return_val)


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def interval_average():
    """
    calculate the average heartrate since a given time via post

    :return: json containing the average, or error message
    """
    interval_request = request.get_json()
    pat_id = interval_request["patient_id"]

    if heart_server_helpers.validate_patient(pat_id) is False:
        return jsonify({"Error": "invalid patient ID"})

    if heart_server_helpers.exisiting_beats(pat_id) is False:
        return jsonify({"Error": "no heartbeats recorded for patient"})

    start_time = interval_request["heart_rate_average_since"]

    try:
        datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        return jsonify({"Error": "Enter date a YYYY-mm-dd HH:MM:SS.ffffff"})

    interval_average = heart_server_helpers.hr_avg_since(pat_id, start_time)

    return jsonify({"interval_average": interval_average})


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    """
    Add a heart rate to the database for a given patient via post

    :return: json indicating success adding heart rate, or error message
    """
    heart_data = request.get_json()
    pat_id = heart_data["patient_id"]
    rate = heart_data["heart_rate"]

    if not isinstance(rate, int):
        return jsonify({"Error": "non-integer value for heart rate"})

    if heart_server_helpers.validate_patient(pat_id) is False:
        return jsonify({"Error": "invalid patient ID"})

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

    patient.save()

    tachycardia = heart_server_helpers.is_tachycardic(pat_id)

    return jsonify({"status": "true"})


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def return_heartrates(patient_id):
    """
    access database to get heart rate history for a patient

    :param patient_id: integer ID of patient to get heart rates of
    :return: json with the heart rate list for patient, or error message
    """
    patient_id = int(patient_id)

    if heart_server_helpers.validate_patient(pat_id) is False:
        return jsonify({"Error": "invalid patient ID"})

    if heart_server_helpers.existing_beats(pat_id) is False:
        return jsonify({"Error": "no heartbeats recorded for patient"})

    for user in Patient.objects.raw({"_id": patient_id}):
        patient = user

    heartrate_list = patient.heart_rate
    print(heartrate_list)
    heart_list = {"heat_rates": heartrate_list}
    return jsonify(heart_list)


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def return_avg_rate(patient_id):
    """
    access database to get last heart rate recorded for patient

    :param patient_id: integer ID of patient to get heart rates from
    :return: json with the last heart rate for patient, or error message

    """
    patient_id = int(patient_id)

    if heart_server_helpers.validate_patient(pat_id) is False:
        return jsonify({"Error": "invalid patient ID"})

    if heart_server_helpers.existing_beats(pat_id) is False:
        return jsonify({"Error": "no heartbeats recorded for patient"})

    for user in Patient.objects.raw({"_id": patient_id}):
        patient = user

    heartrate_list = patient.heart_rate
    num_rates = len(heartrate_list)

    avg_rate = {"rate_avg": sum(heartrate_list)/num_rates}
    return jsonify(avg_rate)


@app.route("/api/status/<patient_id>", methods=["GET"])
def patient_status(patient_id):
    """
    check whether a given patient is tachycardic

    :param patient_id: integer ID of patient to check tachycardic status
    :return: json indicating whether patient is tachycardic, or error message
    """
    patient_id = int(patient_id)

    if heart_server_helpers.validate_patient(pat_id) is False:
        return jsonify({"Error": "invalid patient ID"})

    if heart_server_helpers.existing_beats(pat_id) is False:
        return jsonify({"Error": "no heartbeats recorded for patient"})

    tachycardia = heart_server_helpers.is_tachycardic(patient_id)

    status = {"patient_tachycardic": tachycardia}
    return jsonify(status)


if __name__ == "__main__":
    app.run(host="127.0.0.1")
