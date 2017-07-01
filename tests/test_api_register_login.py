from bucketlist import app, classes
from flask import jsonify, request
from unittest import TestCase
import sys
import json


class RegisterLoginAPI_TestCases(TestCase):

    def setUp(self):
        self.tester = app.test_client(self)
        classes.all_users = {}


    def test_user_can_register(self):

        data = {
            'fullname':'James Brown',
            'email':'jb@gmail.com',
            'password':'ABC'
        }
        response = self.tester.post('/v1/api/auth/register',
                                    data=json.dumps(data),
                                    content_type='application/json')


        self.assertEqual(response.status_code, 201)

    def test_correct_response_when_user_registered(self):
        data = {
            'fullname':'Albert Brown',
            'email':'ab@gmail.com',
            'password':'XT'
        }

        response = self.tester.post('/v1/api/auth/register',
                                    data=json.dumps(data),
                                    content_type='application/json')


        assert b'User has been registered' in response.data



