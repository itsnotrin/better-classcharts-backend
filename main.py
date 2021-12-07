from sanic import Sanic
from sanic.response import json
import requests
from datetime import datetime, timedelta

# Storing key info
homework_url = "https://www.classcharts.com/apipublic/homework/0"
login_url = "https://www.classcharts.com/apiv2student/login"

# Login System: 
def login(code, dob):
    headers = {"User-Agent": "Mozilla/5.0"}
    payload = {'code': code, 'dob':dob, 'remember_me': '1'}
    session = requests.Session()
    resp = session.post(login_url, headers=headers, data=payload)
    jsonResponse = resp.json()
    if jsonResponse["success"] == 0:
        print("Error while logging in - Your date of birth or your login code is incorrect!")
        return(0, "ERROR - DOB OR CODE", session)
    else:
        name = jsonResponse["data"]["name"]
        return(1, name, jsonResponse)

app = Sanic("The backend for my BetterClasscharts Project!")

@app.route("/login")
def signin(request):
    req = request.json
    code = req["code"]
    dob = req["dob"]
    success, name, session = login(code, dob)
    if success == 1:
        print(session)
        return json({ "success": 1, "message": f"Welcome, {name}!" })
    else:
        return json({ "success": 0, "message": "Your Date of birth or your login code is incorrect. Please try again!"})


if __name__ == '__main__':
    app.run()