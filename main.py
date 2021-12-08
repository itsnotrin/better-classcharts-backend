from sanic import Sanic
from sanic.response import json
import requests

# Storing key info
homework_url = "https://www.classcharts.com/apipublic/homework/0"
login_url = "https://www.classcharts.com/apiv2student/login"

# Homework System: 
def homework(code, dob):
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
    homeworks = {}
    jsonResponse2 = resp2.json()
    num = 0
    for i in jsonResponse2["data"]:
        num+=1
        data = {
            num:{
                "Class": i["lesson"],
                "Subject": i["subject"],
                "Title": i["title"],
                "Description": i["description"],
                "Done": i["status"]["ticked"]
            }
        }
        homeworks.update(data)
    if jsonResponse["success"] == 0:
        print("Error while logging in - Your date of birth or your login code is incorrect!")
        return(0, "ERROR - DOB OR CODE", jsonResponse, session)
    else:
        name = jsonResponse["data"]["name"]
        return(1, name, homeworks)



app = Sanic("The backend for my BetterClasscharts Project!")

@app.route("/homework")
def HomeworkEndpoint(request):
    req = request.json
    code = req["code"]
    dob = req["dob"]
    success, name, homeworks = homework(code, dob)
    if success == 0:
        return json({ "success": 0, "message": "Your Date of birth or your login code is incorrect. Please try again!"})

    else:
        return json({ "success": 1, "message": homeworks })



if __name__ == '__main__':
    app.run("0.0.0.0")