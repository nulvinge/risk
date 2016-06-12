from flask import Flask, request
app = Flask(__name__)

#simulate db index
class UserData:
    def __init__():
        self.lastSuccessfull = 0
        self.lastFailed = 0

userData = {}

def successfullLogin(userid, time):
    if not userid in userData:
        userData[userid] = UserData()
    userData[userid].lastSuccessfull = time

def failedLogin(userid, time):
    if not userid in userData:
        userData[userid] = UserData()
    userData[userid].lastFailed = time

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
            successfullLogin(s[8], time)
        elif s[5] == "Failed":
            failedLogin(s[10], time)

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

    if userid in userData:
        return "true"
    else:
        return "false"

if __name__ == "__main__":
    app.run()

