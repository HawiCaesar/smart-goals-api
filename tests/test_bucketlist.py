from bucketlist import create_application, database
from unittest import TestCase
import os
import json


class BucketlistTestCases(TestCase):
    """Bucketlist Test Cases"""

    def setUp(self):
        self.app = create_application(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist1 = {"name": "Travel Manenos"}
        self.bucketlist2 = {"name": "Draw caricatures"}
        self.bucketlist3 = {"name": "Career Things"}
        self.bucketlist4 = {"name": "2018"}

        # binds app to current context
        with self.app.app_context():
            # create tables
            database.create_all()

    def test_bucketlist_creation(self):
        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                                      headers={'Content-Type': 'application/json'})

        data = json.loads(response.data.decode())


        self.assertEqual(response.status_code, 201)
        self.assertIn('Travel Manenos', data['name'], "Bucketlist not created")

    def test_api_fetch_all_bucketlists(self):
        """ Test API can fetch all bucketlists GET request """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                      headers={'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 201)

        response2 = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist3),
                                       headers={'Content-Type': 'application/json'})

        self.assertEqual(response2.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/')
        self.assertEqual(get_response.status_code, 200)

        data = json.loads(response.data.decode('utf-8'))

        self.assertIn('Draw caricatures', data['name'])


    def test_api_can_get_bucketlist_by_id(self):
        """ Test API can get a specific bucketlist by id """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist4),
                                      headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 201)

        json_response = json.loads(response.data.decode('utf-8').replace("'", "\""))

        result = self.client().get('/v1/api/bucketlists/{}'.format(json_response['id']))
        self.assertEqual(result.status_code, 200)

        data = json.loads(result.data.decode('utf-8'))
        self.assertIn("2018", data['name'])



    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            database.session.remove()
            database.drop_all()


# Make the tests conveniently executable
# if __name__ == "__main__":
#     unittest.main()








