from sanic import Sanic
from sanic.response import json
import requests

# Storing key info
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
    #TODO: ALLOW USERS TO SET A SPECIFIC TIME FRAME TO REPORT BACK FROM.
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
          int(Count): {
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

# Timetable System: 
def GetTimetable(code, dob):
    headers = {"User-Agent": "Mozilla/5.0"}
    payload = {'code': code, 'dob':dob, 'remember_me': '1'}
    session = requests.Session()
    resp = session.post(login_url, headers=headers, data=payload)
    jsonResponse = resp.json()
    studentId = jsonResponse["data"]["id"]
    sessionId = jsonResponse["meta"]["session_id"]
    resp2 = session.get(f"https://www.classcharts.com/apiv2student/timetable/{studentId}", headers = {
      "authorization": f"Basic {sessionId}"
    })
    jsonResponse2 = resp2.json()
    print(jsonResponse2["data"])
    if jsonResponse["success"] == 0:
        print("Error while logging in - Your date of birth or your login code is incorrect!")
        return(0, "ERROR - DOB OR CODE", jsonResponse, session)
    else:
        name = jsonResponse["data"]["name"]
        return(1, name, jsonResponse2)

app = Sanic("The backend for my BetterClasscharts Project!")

@app.route("/homework")
def HomeworkEndpoint(request):
    req = request.json
    try:
      code = req["code"]
      dob = req["dob"]
    except:
      return json({ "success": 0, "message": "Code or Date of Birth is missing." })
    success, name, homeworks = GetHomework(code, dob)
    if success == 0:
        return json({ "success": 0, "message": "Your Date of birth or your login code is incorrect. Please try again!"})

    else:
        return json({ "success": 1, "message": homeworks })

@app.route("/behaviour")
def BehaviourEndpoint(request):
    req = request.json
    try:
      code = req["code"]
      dob = req["dob"]
    except:
      return json({ "success": 0, "message": "Code or Date of Birth is missing." })
    success, name, points = GetBehaviour(code, dob)
    if success == 0:
        return json({ "success": 0, "message": "Your Date of birth or your login code is incorrect. Please try again!"})

    else:
        return json({ "success": 1, "message": points })

@app.route("/timetable")
def TimetableEndpoint(request):
    req = request.json
    try:
      code = req["code"]
      dob = req["dob"]
    except:
      return json({ "success": 0, "message": "Code or Date of Birth is missing." })
    GetTimetable(code, dob)
    return json({})
    # success, name, points = GetBehaviour(code, dob)
    # if success == 0:
    #     return json({ "success": 0, "message": "Your Date of birth or your login code is incorrect. Please try again!"})

    # else:
    #     return json({ "success": 1, "message": points })

if __name__ == '__main__':
    app.run("0.0.0.0")