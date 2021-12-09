from sanic import Sanic
from sanic.response import json
import requests

# Storing key info
homework_url = "https://www.classcharts.com/apipublic/homework/0"
login_url = "https://www.classcharts.com/apiv2student/login"

# Homework System: 
def GetHomework(code, dob):
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

# Behaviour System: 
def GetBehaviour(code, dob):
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
    #https://www.classcharts.com/apiv2student/activity/5939358?from=2021-08-01&to=2021-12-09
    resp2 = session.get(f"https://www.classcharts.com/apiv2student/activity/{studentId}", headers = {
      "authorization": f"Basic {sessionId}"
    })
    points = {}
    jsonResponse2 = resp2.json()
    # print(jsonResponse2)
    Count = 0
    PosCount = 0
    NegCount = 0
    for i in jsonResponse2["data"]:
      Count+=1
      if i["polarity"] == "positive":
        PosCount+=1
      elif i["polarity"] == "positive":
        NegCount+=1
      data = {
          Count: {
            "type": i["polarity"],
            "teacher": i["teacher_name"],
            "note": i["note"]
          }
      }
      points.update(data)
    if jsonResponse["success"] == 0:
        print("Error while logging in - Your date of birth or your login code is incorrect!")
        return(0, "ERROR - DOB OR CODE", jsonResponse["data"], session)
    elif jsonResponse2["success"] == 0:
      return(0, "Unexpected Error", jsonResponse2["data"], session)
    else:
        name = jsonResponse["data"]["name"]
        return(1, name, points)

app = Sanic("The backend for my BetterClasscharts Project!")

@app.route("/homework")
def HomeworkEndpoint(request):
    req = request.json
    code = req["code"]
    dob = req["dob"]
    success, name, homeworks = GetHomework(code, dob)
    if success == 0:
        return json({ "success": 0, "message": "Your Date of birth or your login code is incorrect. Please try again!"})

    else:
        return json({ "success": 1, "message": homeworks })

@app.route("/behaviour")
def BehaviourEndpoint(request):
    req = request.json
    code = req["code"]
    dob = req["dob"]
    success, name, points = GetBehaviour(code, dob)
    if success == 0:
        return json({ "success": 0, "message": "Your Date of birth or your login code is incorrect. Please try again!"})

    else:
        return json({ "success": 1, "message": points })


if __name__ == '__main__':
    app.run("0.0.0.0")