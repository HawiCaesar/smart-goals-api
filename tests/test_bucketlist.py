from bucketlist import create_application, database
from unittest import TestCase
import os
import json


class BucketlistTestCases(TestCase):
    """Bucketlist Test Cases"""

    def setUp(self):
        self.app = create_application(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist1 = {"fullname": "Travel Manenos"}
        self.bucketlist2 = {"fullname": "Draw caricatures"}

        # binds app to current context
        with self.app.app_context():
            # create tables
            database.create_all()

    def test_bucketlist_creation(self):
        response = self.client().post('/create-bucketlist/', data=self.bucketlist1)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Travel Manenos', str(response.data))

    def test_api_fetch_all_bucketlist(self):
        """ Test API can fetch all bucketlists GET request """

        response = self.client().post('/create-bucketlist/', data=self.bucketlist1)
        self.assertEqual(response.status_code, 201)

        response2 = self.client().post('/create-bucketlist/', data=self.bucketlist2)
        self.assertEqual(response2.status_code, 201)

        get_response = self.client().get('/bucketlists/')
        self.assertEqual(get_response.status_code, 200)

        self.assertIn('Travel Manenos', str(get_response))
        self.assertIn('Draw caricatures', str(get_response))

    def test_api_can_get_bucketlist_by_id(self):
        """ Test API can get a specific bucketlist by id """

        response = self.client().post('/create-bucketlist', data=self.bucketlist1)
        self.assertEqual(response.status_code, 201)

        json_response = json.loads(response.data.decode('utf-8').replace("'", "\""))

        result = self.client().get('/bucketlists/{}'.format(json_response['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn("Travel Manenos", str(result.data))








