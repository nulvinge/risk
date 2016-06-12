import os
import unittest
import risk
import tempfile

class RiskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = risk.app.test_client()

    def tearDown(self):
        pass


    def successfull(self, username):
        return self.app.post('/log', data=dict(
            msg="20140616 09:08:11 vm5 [4f8a7f94:533e22a7] sshd Accepted password for %s from 112.196.12.67 port 57912 ssh2" % username
        ), follow_redirects=True)

    def failed(self, username):
        return self.app.post('/log', data=dict(
            msg="20140616 09:02:46 vm5 [4f8a7f94:533e229c] sshd Failed none for invalid user %s from 116.10.191.235 port 52753 ssh2" % username
        ), follow_redirects=True)

    def isuserknown_fail(self):
        return self.app.get('/isuserknown', follow_redirects=True)

    def isuserknown(self, username):
        return self.app.get('/isuserknown?username=' + username, follow_redirects=True)

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

if __name__ == '__main__':
    unittest.main()

