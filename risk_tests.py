import os
import unittest
import risk
import tempfile
from datetime import *
from dateutil.relativedelta import *

class RiskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = risk.app.test_client()

    def tearDown(self):
        pass


    def successful(self, username="test", ip="123.123.123.123", time="20140616 09:02:46"):
        return self.app.post('/log', data=dict(
            msg="%s vm5 [4f8a7f94:533e22a7] sshd Accepted password for %s from %s port 57912 ssh2"
                % (time, username, ip)
        ), follow_redirects=True)

    def failed(self, username="test", ip="123.123.123.123", time="20140616 09:02:46"):
        return self.app.post('/log', data=dict(
            msg="%s vm5 [4f8a7f94:533e229c] sshd Failed none for invalid user %s from %s port 52753 ssh2"
                % (time, username, ip)
        ), follow_redirects=True)

    def isuserknown_fail(self):
        return self.app.get('/isuserknown', follow_redirects=True)

    def isuserknown(self, username):
        return self.app.get('/isuserknown?username=' + username, follow_redirects=True)

    def isipknown_fail(self):
        return self.app.get('/isipknown', follow_redirects=True)

    def isipknown(self, ip):
        return self.app.get('/isipknown?ip=' + ip, follow_redirects=True)

    def isipinternal(self, ip):
        return self.app.get('/isipinternal?ip=' + ip, follow_redirects=True)

    def lastSuccessfulLoginDate(self, username):
        return self.app.get('/lastSuccessfulLoginDate?username=' + username, follow_redirects=True)

    def lastFailedLoginDate(self, username):
        return self.app.get('/lastFailedLoginDate?username=' + username, follow_redirects=True)

    def failedLoginCountLastWeek(self):
        return self.app.get('/failedLoginCountLastWeek', follow_redirects=True)

    def test_isuserknown(self):
        rv = self.isuserknown_fail()
        assert rv.status_code == 400
        rv = self.isuserknown("nouser")
        assert 'false' in rv.data
        rv = self.isuserknown("gooduser")
        assert 'false' in rv.data
        rv = self.successful("gooduser")
        rv = self.isuserknown("gooduser")
        assert 'true' in rv.data
        rv = self.failed("baduser")
        rv = self.isuserknown("baduser")
        assert 'true' in rv.data
        rv = self.isuserknown("nouser")
        assert 'false' in rv.data
        rv = self.isuserknown("gooduser")
        assert 'true' in rv.data

    def test_isipknown(self):
        goodip = "123.0.0.1"
        badip = "123.1.0.1"
        noip = "255.255.255.255"
        rv = self.isipknown_fail()
        assert rv.status_code == 400
        rv = self.isipknown(noip)
        assert 'false' in rv.data
        rv = self.isipknown(goodip)
        assert 'false' in rv.data
        rv = self.successful(ip=goodip)
        rv = self.isipknown(goodip)
        assert 'true' in rv.data
        rv = self.failed(ip=badip)
        rv = self.isipknown(badip)
        assert 'true' in rv.data
        rv = self.isipknown(noip)
        assert 'false' in rv.data
        rv = self.isipknown(goodip)
        assert 'true' in rv.data

    def test_isipinternal(self):
        internal = "192.168.1.2"
        external = "123.1.0.1"
        rv = self.isipinternal('')
        assert rv.status_code == 400
        rv = self.isipinternal(internal)
        assert 'true' in rv.data
        rv = self.isipinternal(external)
        assert 'false' in rv.data

    def test_lastSuccessfulLoginDate(self):
        time1 = "20140618 09:02:46"
        time2 = "20140619 09:02:46"
        time3 = "20140620 09:02:46"
        user = 'timetest'
        rv = self.lastSuccessfulLoginDate('')
        assert rv.status_code == 400

        rv = self.lastSuccessfulLoginDate(user)
        assert 'No login' in rv.data
        rv = self.lastFailedLoginDate(user)
        assert 'No login' in rv.data

        rv = self.failed(user, time=time1)
        rv = self.lastSuccessfulLoginDate(user)
        assert 'No login' in rv.data
        rv = self.lastFailedLoginDate(user)
        assert time1 in rv.data

        rv = self.successful(user, time=time1)
        rv = self.lastSuccessfulLoginDate(user)
        assert time1 in rv.data
        rv = self.lastFailedLoginDate(user)
        assert time1 in rv.data

        rv = self.failed(user, time=time2)
        rv = self.lastSuccessfulLoginDate(user)
        assert time1 in rv.data
        rv = self.lastFailedLoginDate(user)
        assert time2 in rv.data

        rv = self.successful(user, time=time2)
        rv = self.lastSuccessfulLoginDate(user)
        assert time2 in rv.data
        rv = self.lastFailedLoginDate(user)
        assert time2 in rv.data

        rv = self.successful(user, time=time3)
        rv = self.lastSuccessfulLoginDate(user)
        assert time3 in rv.data
        rv = self.lastFailedLoginDate(user)
        assert time2 in rv.data

        rv = self.failed(user, time=time3)
        rv = self.lastSuccessfulLoginDate(user)
        assert time3 in rv.data
        rv = self.lastFailedLoginDate(user)
        assert time3 in rv.data

    def test_failedLoginCountLastWeek(self):
        user = 'failedloginuser'
        now = datetime.now()
        time1 = now - relativedelta(day=1)
        time2 = now - relativedelta(day=2)
        time3 = now - relativedelta(day=3)
        time4 = now - relativedelta(day=4)
        time5 = now - relativedelta(day=5)
        time8 = now - relativedelta(day=8)
        time9 = now - relativedelta(day=9)

        rv = self.failedLoginCountLastWeek()
        assert "0" in rv.data
        rv = self.failed(user, time=time1)
        rv = self.failedLoginCountLastWeek()
        assert "1" in rv.data

        rv = self.failed(user, time=time8)
        rv = self.failedLoginCountLastWeek()
        assert "1" in rv.data

        rv = self.failed(user, time=time2)
        rv = self.failedLoginCountLastWeek()
        assert "2" in rv.data

        rv = self.successful(user, time=time8)
        rv = self.failedLoginCountLastWeek()
        assert "2" in rv.data

        rv = self.failed(user, time=time5)
        rv = self.failedLoginCountLastWeek()
        assert "3" in rv.data

if __name__ == '__main__':
    unittest.main()

