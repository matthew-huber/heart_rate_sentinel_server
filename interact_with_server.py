import requests


def add_patient():
    """
    Add a new patient to the database

    :return: None
    """
    r = requests.post("http://127.0.0.1:5000/api/new_patient",
                      json={"patient_id": 9,
                            "attending_email": "mth37@duke.edu",
                            "user_age": 50})
    post_result = r.json()
    print(post_result)


def add_hr():
    """
    Add a new heart rate to the database for a given patient

    :return: None
    """
    r = requests.post("http://127.0.0.1:5000/api/heart_rate",
                      json={"patient_id": 8,
                            "heart_rate": 200})
    post_result = r.json()
    print(post_result)


def get_last_hr():
    """
    find the last heart rate stored in database for a patient

    :return: None
    """
    r = requests.get("http://127.0.0.1:5000/api/heart_rate/10")
    result = r.json()
    print(result)


def get_avg_hr():
    """
    Find average heart rate for a patient through all time

    :return: None
    """
    r = requests.get("http://127.0.0.1:5000/api/heart_rate/average/10")
    result = r.json()
    print(result)


def get_avg_hr_since():
    """
    Find average heart for a patient since given time

    :return: None
    """
    r = requests.post("http://127.0.0.1:5000/api/heart_rate/interval_average",
                      json={"patient_id": 8,
                            "heart_rate_average_since":
                            "2018-03-09 11:00:36.372339"})
    post_result = r.json()
    print(post_result)


if __name__ == "__main__":
    add_patient()
