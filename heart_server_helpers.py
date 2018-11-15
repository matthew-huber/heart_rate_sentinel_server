from db_patient import Patient
import sendgrid
import os
import datetime
from sendgrid.helpers.mail import *


def email_alert(patient_id):
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
    print(response.status_code)
    print(response.body)
    print(response.headers)


def is_tachycardic(patient_id):
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

    avg_hr = sum(hr_to_average)/len(hr_to_average)
    return avg_hr
