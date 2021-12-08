from sanic import Sanic
from sanic.response import json
import requests

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
    studentId = jsonResponse["data"]["id"]
    sessionId = jsonResponse["meta"]["session_id"]
    headers = {
        "authorization": f"Basic {sessionId}"
    }
    resp2 = session.get(f"https://www.classcharts.com/apiv2student/homeworks/{studentId}?", headers = {
      "authorization": f"Basic {sessionId}"
    })
    homeworks = []
    jsonResponse2 = resp2.json()
    print(f"Class: {jsonResponse2['data'][2]['lesson']}\nLesson: {jsonResponse2['data'][2]['subject']}")
    if jsonResponse["success"] == 0:
        print("Error while logging in - Your date of birth or your login code is incorrect!")
        return(0, "ERROR - DOB OR CODE", jsonResponse, session)
    else:
        name = jsonResponse["data"]["name"]
        return(1, name, jsonResponse, session)



app = Sanic("The backend for my BetterClasscharts Project!")

@app.route("/login")
def signin(request):
    req = request.json
    code = req["code"]
    dob = req["dob"]
    success, name, resp, session = login(code, dob)
    if success == 0:
        return json({ "success": 0, "message": "Your Date of birth or your login code is incorrect. Please try again!"})

    else:
        student_id = resp["data"]["id"]
        return json({})



if __name__ == '__main__':
    app.run("0.0.0.0")