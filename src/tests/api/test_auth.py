import unittest
import json
from flask_restful import request
from tests.test_utils import *
from db.__init__ import exec_get_one

def getHeaders(test, username, password):
    authInfo = {
        'username': username,
        'password': password
    }
    headers = post_rest_call(test, 'http://localhost:5000/auth', params=json.dumps(authInfo), post_header={'Content-Type': 'application/json'})
    headers['Content-Type'] = 'application/json'
    return headers

class TestAuth(unittest.TestCase):

    def setUp(self):
        post_rest_call(self, 'http://localhost:5000/manage/test')

    def testAuthenticate(self):
        authInfo = {
            'username': 'xX_EldenLord_Xx',
            'password': 'thefallenleaves'
        }
        result = post_rest_call(self, 'http://localhost:5000/auth', params=json.dumps(authInfo), post_header={'Content-Type': 'application/json'})
        self.assertEqual(result['user-id'], '1')

    def testAuthHeaders(self):
        authInfo = {
            'username': 'xX_EldenLord_Xx',
            'password': 'thefallenleaves'
        }
        headers = post_rest_call(self, 'http://localhost:5000/auth', params=json.dumps(authInfo), post_header={'Content-Type': 'application/json'})
        # Mockup of auth_headers()
        user_id = headers.get('user-id')    
        session_key = headers.get('session-key')
        if session_key is None or user_id is None:
            self.fail()

