from db_patient import Patient
import sendgrid
import os
from sendgrid.helpers.mail import *


def email_alert(patient_id):
    for user in Patient.objects.raw({"_id": patient_id})
        patient = user

    attendant_email = patient.attending_email

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("tachycardic_alert@gmail.com")
    to_email = Email(attendant_email)
    subject = "Patient Tachycardic Alert"
    content = Content("text/plain", "Patient {0}is tachycardic".format(patient_id))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


def is_tachycardic(patient_id):
    for user in Patient.objects.raw({"_id": patient_id})
        patient = user

    age = patient.user_age
    heart_rate = patient.herat_rate
    if age < 1:
        except 
    elif age < 3:
        if heart_rate > 151:
            return True
    elif age < 5:
        if heart_rate > 137:
            return True
    elif age < 8:
        if heart_rate > 133:
            return True
    elif age < 12:
        if heart_rate > 130:
            return True
    elif age < 15:
        if heart_rate > 119:
            return True
    else:
        if heart_rate > 100:
            return True
    
    return False
