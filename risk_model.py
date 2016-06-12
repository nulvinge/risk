from dateutil.parser import parse

class UserData:
    """simulate db index for user logins"""
    def __init__(self):
        self.lastSuccessful = None
        self.lastFailed = None

userData = {}
ips = {}

def successfulLogin(time, userid, ip):
    if userid not in userData:
        userData[userid] = UserData()
    userData[userid].lastSuccessful = time

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
    Successful
    20140616 09:08:11 vm5 [4f8a7f94:533e22a7] sshd Accepted password for cryptzone from 112.196.12.67 port 57912 ssh2
    Failed
    20140616 09:02:46 vm5 [4f8a7f94:533e229c] sshd Failed none for invalid user root from 116.10.191.235 port 52753 ssh2

    Use naive parsing for now
    """

    s = msg.split(' ')
    time = parse(s[0] + ' ' + s[1])
    if s[4] == "sshd":
        if s[5] == "Accepted":
            successfulLogin(time, s[8], s[10])
        elif s[5] == "Failed":
            failedLogin(time, s[10], s[12])

def getUserData(userid):
    if userid in userData:
        return userData[userid]
    else:
        return None

def getIpData(ip):
    if ip in ips:
        return ips[ip]
    else:
        return None

def isIpInternal(ip):
    if ip.startswith("192.168."):
        return True
    elif ip.startswith("127."):
        return True
    elif ip.startswith("10."):
        return True
    return False

def timeToStr(datetime):
    return datetime.strftime("%Y%m%d %H:%M:%S")

