import os
import unittest
import risk
import tempfile

class RiskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = risk.app.test_client()

    def tearDown(self):
        pass


    def successfull(self, username="test", ip="123.123.123.123"):
        return self.app.post('/log', data=dict(
            msg="20140616 09:08:11 vm5 [4f8a7f94:533e22a7] sshd Accepted password for %s from %s port 57912 ssh2"
                % (username, ip)
        ), follow_redirects=True)

    def failed(self, username="test", ip="123.123.123.123"):
        return self.app.post('/log', data=dict(
            msg="20140616 09:02:46 vm5 [4f8a7f94:533e229c] sshd Failed none for invalid user %s from %s port 52753 ssh2"
                % (username, ip)
        ), follow_redirects=True)

    def isuserknown_fail(self):
        return self.app.get('/isuserknown', follow_redirects=True)

    def isuserknown(self, username):
        return self.app.get('/isuserknown?username=' + username, follow_redirects=True)

    def isipknown_fail(self):
        return self.app.get('/isipknown', follow_redirects=True)

    def isipknown(self, ip):
        return self.app.get('/isipknown?ip=' + ip, follow_redirects=True)

    def test_isuserknown(self):
        rv = self.isuserknown_fail()
        assert rv.status_code == 400
        rv = self.isuserknown("nouser")
        assert 'false' in rv.data
        rv = self.isuserknown("gooduser")
        assert 'false' in rv.data
        rv = self.successfull("gooduser")
        rv = self.isuserknown("gooduser")
        assert 'true' in rv.data
        rv = self.failed("baduser")
        rv = self.isuserknown("baduser")
        assert 'false' in rv.data
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
        rv = self.successfull(ip=goodip)
        rv = self.isipknown(goodip)
        assert 'true' in rv.data
        rv = self.failed(ip=badip)
        rv = self.isipknown(badip)
        assert 'true' in rv.data
        rv = self.isipknown(noip)
        assert 'false' in rv.data
        rv = self.isipknown(goodip)
        assert 'true' in rv.data

if __name__ == '__main__':
    unittest.main()

