from flask import Flask, request
app = Flask(__name__)

class UserData:
    """simulate db index for user logins"""
    def __init__(self):
        self.lastSuccessfull = ""
        self.lastFailed = ""

userData = {}
ips = {}

def successfullLogin(time, userid, ip):
    if userid not in userData:
        userData[userid] = UserData()
    userData[userid].lastSuccessfull = time

    if ip not in ips:
        ips[ip] = True #dummy value for set

def failedLogin(time, userid, ip):
    if userid not in userData:
        userData[userid] = UserData()
    userData[userid].lastFailed = time

    if ip not in ips:
        ips[ip] = False #dummy value for set

def parseMsg(msg):
    """Parses a log message and stores it

    Example parses of what we are looking for
    Successfull
    20140616 09:08:11 vm5 [4f8a7f94:533e22a7] sshd Accepted password for cryptzone from 112.196.12.67 port 57912 ssh2
    Failed
    20140616 09:02:46 vm5 [4f8a7f94:533e229c] sshd Failed none for invalid user root from 116.10.191.235 port 52753 ssh2

    Use naive parsing for now
    """

    s = msg.split(' ')
    time = s[0] + ' ' + s[1]
    if s[4] == "sshd":
        if s[5] == "Accepted":
            successfullLogin(time, s[8], s[10])
        elif s[5] == "Failed":
            failedLogin(time, s[10], s[12])

@app.route("/log", methods=['POST'])
def log():
    msg = request.form['msg']
    parseMsg(msg)
    return ""

@app.route("/isuserknown")
def isUserKnown():
    userid = request.args.get('username', '')

    if not userid:
        return "Invalid userid", 400

    if userid in userData and userData[userid].lastSuccessfull:
        return "true"
    else:
        return "false"

@app.route("/isipknown")
def isIpKnown():
    ip = request.args.get('ip', '')

    if not ip:
        return "Invalid ip", 400

    if ip in ips:
        return "true"
    else:
        return "false"

if __name__ == "__main__":
    app.run()

