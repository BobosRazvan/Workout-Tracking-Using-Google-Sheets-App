import requests
import json
import datetime
import os

APP_ID = os.environ.get('APP_ID')
API_KEY = os.environ.get('API_KEY')
AUTHORIZATION_BEARER_TOKEN = os.environ.get('AUTHORIZATION_BEARER_TOKEN')
SHEET_ENDPOINT = os.environ.get('SHEET_ENDPOINT')


def get_exercise_data(query):
    url = "https://trackapi.nutritionix.com/v2/natural/exercise"

    headers = {
        "x-app-id": APP_ID,
        "x-app-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "query": query
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return None


exercises = input("Tell me what exercises you did: ")
print("\n\n")

exercise_data = get_exercise_data(exercises)
print(json.dumps(exercise_data, indent=4))

exercise_name = ""
exercise_duration = 0.0
exercise_calories = 0.0
for exercise in exercise_data['exercises']:
    exercise_name = exercise['name']
    exercise_duration = exercise['duration_min']
    exercise_calories = exercise['nf_calories']

now = datetime.datetime.now()
date = now.strftime("%Y/%m/%d")
time = now.strftime("%H:%M:%S")


def add_row(date, time, exercise_name, exercise_duration, exercise_calories):
    url = SHEET_ENDPOINT

    headers = {
        "Authorization": AUTHORIZATION_BEARER_TOKEN,
    }

    data = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise_name.title(),
            "duration": exercise_duration,
            "calories": exercise_calories
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return None


# Use the function
sheet_response = add_row(date, time, exercise_name, exercise_duration, exercise_calories)
print(json.dumps(sheet_response, indent=4))
