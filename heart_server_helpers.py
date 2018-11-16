from db_patient import Patient
import sendgrid
import os
import datetime
from sendgrid.helpers.mail import *


def existing_beats(patient_id):
    """
    checks whether there are existing heart beats for a patient

    :param patient_id: integer ID of patient to check if there is beat data
    :return: True if patient has recorded heart rates, False if not
    """
    for user in Patient.objects.raw({"_id": patient_id}):
        patient = user

    hr_list = patient.heart_rate

    if hr_list == []:
        return False
    else:
        return True


def validate_patient(patient_id):
    """
    check whether patient exists in database

    :param patient_id: integer ID to look for in database
    :return: True if patient exists in database, False if not
    """
    for user in Patient.objects.raw({"_id": patient_id}):
        patient = user

    try:
        patient
        return True
    except NameError:
        return False


def email_alert(patient_id):
    """
    Send an email to the attending physician of tachycardic patient

    :param patient_id: integer ID of tachycardic patient
    :return: None
    """
    for user in Patient.objects.raw({"_id": patient_id}):
        patient = user

    attendant_email = patient.attending_email

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("tachycardic_alert@gmail.com")
    to_email = Email(attendant_email)
    subject = "Patient Tachycardic Alert"
    content = Content("text/plain", "Patient {0}".format(patient_id))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return True


def is_tachycardic(patient_id):
    """
    check whether a patient is tachycardic

    :param patient_id: integer ID of patient to check tachycardia status
    :return: True if patient is tachycardic, False if patient is not
    """
    for user in Patient.objects.raw({"_id": patient_id}):
        patient = user

    age = patient.user_age
    heart_rate_list = patient.heart_rate
    heart_rate = heart_rate_list[-1]
    tachycardic = False

    if age < 1:
        return False
    elif age < 3:
        if heart_rate > 151:
            tachycardic = True
    elif age < 5:
        if heart_rate > 137:
            tachycardic = True
    elif age < 8:
        if heart_rate > 133:
            tachycardic = True
    elif age < 12:
        if heart_rate > 130:
            tachycardic = True
    elif age < 15:
        if heart_rate > 119:
            tachycardic = True
    else:
        if heart_rate > 100:
            tachycardic = True

    if tachycardic is True:
        email_alert(patient_id)
        return True

    return False


def hr_avg_since(pat_id, start_time):
    """
    find the heart rate for a given patient since a certain time

    :param pat_id: integer ID of patient to find average heart rate of
    :param start_time: date time string to find heart rate since
    :return: average heart rate since time given by datetime string
    """
    for user in Patient.objects.raw({"_id": pat_id}):
        patient = user

    heart_rate_list = patient.heart_rate
    hr_times_list = patient.h_r_times

    hr_to_average = []
    parse_date = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")

    index = 0

    for date in hr_times_list:
        if date > parse_date:
            hr_to_average.append(heart_rate_list[index])
        index = index + 1

    if len(hr_to_average) == 0:
        return 0
    avg_hr = sum(hr_to_average)/len(hr_to_average)
    return avg_hr
