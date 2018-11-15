from db_patient import Patient


def email_alert(patient_id):
    for user in Patient.objects.raw({"_id": patient_id})
        patient = user

    email = patient.attending_email


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
