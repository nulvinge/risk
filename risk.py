import risk_model
from flask import Flask, request
app = Flask(__name__)

@app.route("/log", methods=['POST'])
def log():
    msg = request.form['msg']
    risk_model.parseMsg(msg)
    return ""

@app.route("/isuserknown")
def isUserKnown():
    userid = request.args.get('username', '')

    if not userid:
        return "Invalid userid", 400

    data = risk_model.getUserData(userid)
    if data != None:
        return "true"
    else:
        return "false"

@app.route("/isipknown")
def isIpKnown():
    ip = request.args.get('ip', '')

    if not ip:
        return "Invalid ip", 400

    data = risk_model.getIpData(ip)
    if data != None:
        return "true"
    else:
        return "false"

@app.route("/isipinternal")
def isIpInternal():
    ip = request.args.get('ip', '')

    if not ip:
        return "Invalid ip", 400

    if risk_model.isIpInternal(ip):
        return "true"
    else:
        return "false"

@app.route("/lastSuccessfulLoginDate")
def lastSuccessfulLoginDate():
    userid = request.args.get('username', '')

    if not userid:
        return "Invalid userid", 400

    data = risk_model.getUserData(userid)
    if data != None and data.lastSuccessful != None:
        return risk_model.timeToStr(data.lastSuccessful)
    else:
        return "No login"

@app.route("/lastFailedLoginDate")
def lastFailedLoginDate():
    userid = request.args.get('username', '')

    if not userid:
        return "Invalid userid", 400

    data = risk_model.getUserData(userid)
    if data != None and data.lastFailed != None:
        return risk_model.timeToStr(data.lastFailed)
    else:
        return "No login"

if __name__ == "__main__":
    app.run(debug=True)

