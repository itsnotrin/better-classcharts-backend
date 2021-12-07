from sanic import Sanic
from sanic.response import json
import requests

# Storing key info
homework_url = "https://www.classcharts.com/apipublic/homework"
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
        return(1, "ERROR - DOB OR CODE", session)
    else:
        name = jsonResponse["data"]["name"]
        return(0, name, session)

app = Sanic("The backend for my BetterClasscharts Project!")

@app.route("/login")
def post_json(request):
    return json({ "received": True, "message": request.json })

if __name__ == '__main__':
    app.run()