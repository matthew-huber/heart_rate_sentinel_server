import requests
import json


def main():
    r = requests.post("http://127.0.0.1:5000/api/new_patient",
                      json={"patient_id": 8,
                            "attending_email": "mth37@duke.edu",
                            "user_age": 50})
    post_result = r.json()
    print(post_result)


def main2():
    r = requests.post("http://127.0.0.1:5000/api/heart_rate",
                      json={"patient_id": 8,
                            "heart_rate": 200})
    post_result = r.json()
    print(post_result)


def main3():
    r = requests.get("http://127.0.0.1:5000/api/heart_rate/10")
    result = r.json()
    print(result)


def main4():
    r = requests.get("http://127.0.0.1:5000/api/heart_rate/average/10")
    result = r.json()
    print(result)


if __name__ == "__main__":
    main2()
