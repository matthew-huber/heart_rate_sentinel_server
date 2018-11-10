import requests
import json


def main():
    r = requests.post("http://127.0.0.1:5000/api/new_patient", json= {"patient_id" : 111, "attending_email" : "mth37@duke.edu", "user_age" : 50})
    post_result = r.json()
    print(post_result)

if __name__ == "__main__":
    main()
