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
        self.updated_bucketlist = {"name": "2018 Milestones"}
        self.headers = {'Content-Type': 'application/json'}

        # binds app to current context
        with self.app.app_context():
            # create tables
            database.create_all()

    def test_bucketlist_creation(self):
        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                                      headers=self.headers)

        data = json.loads(response.data.decode())


        self.assertEqual(response.status_code, 201)
        self.assertIn('Bucketlist Created', data['message'], "Bucketlist not created")


    def test_api_can_get_bucketlist_by_id(self):
        """ Test API can get a specific bucketlist by id """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist4),
                                      headers=self.headers)
        self.assertEqual(response.status_code, 201)

        json_response = json.loads(response.data.decode('utf-8').replace("'", "\""))

        result = self.client().get('/v1/api/bucketlists/1')
        self.assertEqual(result.status_code, 200)

        data = json.loads(result.data.decode('utf-8'))
        self.assertIn("2018", data['name'])


    def test_api_fetch_all_bucketlists(self):
        """ Test API can fetch all bucketlists GET request """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                      headers=self.headers)

        self.assertEqual(response.status_code, 201)

        response2 = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist3),
                                       headers=self.headers)

        self.assertEqual(response2.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/')
        self.assertEqual(get_response.status_code, 200)

        # data = json.loads(get_response.data.decode('utf-8'))
        #
        # self.assertIn('Draw caricatures', data['name'])

    def test_api_bucketlist_can_be_updated(self):
        """ Update bucketlist PUT request"""

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist4),
                                      headers=self.headers)

        self.assertEqual(response.status_code, 201)

        put_response = self.client().put('/v1/api/bucketlists/1', data=json.dumps(self.updated_bucketlist),
                                         headers=self.headers)

        self.assertEqual(put_response.status_code, 200)

        get_response = self.client().get('/v1/api/bucketlists/1')
        self.assertEqual(get_response.status_code, 200)

        data = json.loads(get_response.data.decode('utf-8'))
        self.assertIn("2018 Milestones", data['name'])

    def test_api_bucketlist_can_be_deleted(self):
        """ Delete bucketlist DELETE request """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                      headers=self.headers)

        self.assertEqual(response.status_code, 201)

        response2 = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist3),
                                       headers=self.headers)

        self.assertEqual(response2.status_code, 201)

        delete_response = self.client().delete('/v1/api/bucketlists/2')
        self.assertEqual(delete_response.status_code, 200)

        # Check if bucketlist has been deleted
        get_response = self.client().get('/v1/api/bucketlists/2')
        self.assertEqual(get_response.status_code, 404)

    def test_api_delete_non_existing_bucketlist(self):
        """ Test Case: Delete non existing bucketlist """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                      headers=self.headers)

        self.assertEqual(response.status_code, 201)

        response2 = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist3),
                                       headers=self.headers)

        self.assertEqual(response2.status_code, 201)

        delete_response = self.client().delete('/v1/api/bucketlists/5')
        self.assertEqual(delete_response.status_code, 404)

    def test_api_delete_bucketlist_without_id(self):
        """ Test Case: delete bucketlist without id """
        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                     headers=self.headers)

        self.assertEqual(response.status_code, 201)

        response2 = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist3),
                                       headers=self.headers)

        self.assertEqual(response2.status_code, 201)

        self.assertEqual(response2.status_code, 201)

        delete_response = self.client().delete('/v1/api/bucketlists/')
        self.assertEqual(delete_response.status_code, 405)

    def test_api_update_non_exisiting_bucketlist(self):
        """ Test Case: Update non exisiting bucketlist """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist4),
                                      headers=self.headers)

        self.assertEqual(response.status_code, 201)

        put_response = self.client().put('/v1/api/bucketlists/3', data=json.dumps(self.updated_bucketlist),
                                         headers=self.headers)

        self.assertEqual(put_response.status_code, 404)

        get_response = self.client().get('/v1/api/bucketlists/1')
        self.assertEqual(get_response.status_code, 200)

        # Ensure nothing has been changed in the record
        data = json.loads(get_response.data.decode('utf-8'))
        self.assertIn("2018", data['name'])

    def tearDown(self):
        """ Teardown all initialized variables """
        with self.app.app_context():
            # drop all tables
            database.session.remove()
            database.drop_all()


# Make the tests conveniently executable
# if __name__ == "__main__":
#     unittest.main()








