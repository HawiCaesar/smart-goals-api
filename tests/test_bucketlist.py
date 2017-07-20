from bucketlist import create_application, database
import unittest
import os, sys
import json


class BucketlistTestCases(unittest.TestCase):
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

        """ Token Authentication implemented so register_user and login_user must be done in each function """

        def register_user(email="user@test.com", password="testabcd"):
            user_data = {
                'email': email,
                'password': password
            }
            return self.client().post('/v1/api/auth/register', data=json.dumps(user_data), headers=self.headers)

        def login_user(email="user@test.com", password="testabcd"):
            user_data = {
                'email': email,
                'password': password
            }
            return self.client().post('/v1/api/auth/login', data=json.dumps(user_data), headers=self.headers)

            # binds app to current context
        with self.app.app_context():
            # create tables
            database.create_all()

        register_user()
        result = login_user()
        self.access_token = json.loads(result.data.decode())



    def test_bucketlist_creation(self):
        """ User can create a bucketlist """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertIn('Bucketlist Created', data['message'], "Bucketlist not created")


    def test_api_can_get_bucketlist_by_id(self):
        """ Test API can get a specific bucketlist by id """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist4),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})
        self.assertEqual(response.status_code, 201)

        result = self.client().get('/v1/api/bucketlists/1',
                                   headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                            "Content-Type": "application/json"})

        self.assertEqual(result.status_code, 200)

        data = json.loads(result.data.decode('utf-8'))
        self.assertIn("2018", data['name'])

    def test_api_fetch_all_bucketlists(self):
        """ Test API can fetch all bucketlists GET request """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        response2 = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist3),
                                       headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                "Content-Type": "application/json"})

        self.assertEqual(response2.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 200)

    def test_api_bucketlist_can_be_updated(self):
        """ Update bucketlist PUT request"""

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist4),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        put_response = self.client().put('/v1/api/bucketlists/1', data=json.dumps(self.updated_bucketlist),
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(put_response.status_code, 200)

        get_response = self.client().get('/v1/api/bucketlists/1',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})
        self.assertEqual(get_response.status_code, 200)

        data = json.loads(get_response.data.decode('utf-8'))
        self.assertIn("2018 Milestones", data['name'])

    def test_api_bucketlist_can_be_deleted(self):
        """ Delete bucketlist DELETE request """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        response2 = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist3),
                                       headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                "Content-Type": "application/json"})

        self.assertEqual(response2.status_code, 201)

        delete_response = self.client().delete('/v1/api/bucketlists/2',
                                               headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                        "Content-Type": "application/json"})

        self.assertEqual(delete_response.status_code, 200)

        # Check if bucketlist has been deleted
        get_response = self.client().get('/v1/api/bucketlists/2',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 404)

    def test_api_delete_non_existing_bucketlist(self):
        """ Test Case: Delete non existing bucketlist """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        response2 = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist3),
                                       headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                "Content-Type": "application/json"})

        self.assertEqual(response2.status_code, 201)

        delete_response = self.client().delete('/v1/api/bucketlists/9',
                                               headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                        "Content-Type": "application/json"})
        self.assertEqual(delete_response.status_code, 404)

    def test_api_delete_bucketlist_without_id(self):
        """ Test Case: delete bucketlist without id """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        response2 = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist3),
                                       headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                "Content-Type": "application/json"})

        self.assertEqual(response2.status_code, 201)

        delete_response = self.client().delete('/v1/api/bucketlists/',
                                               headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                        "Content-Type": "application/json"})
        self.assertEqual(delete_response.status_code, 405)

    def test_api_update_non_exisiting_bucketlist(self):
        """ Test Case: Update non exisiting bucketlist """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist4),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        put_response = self.client().put('/v1/api/bucketlists/3', data=json.dumps(self.updated_bucketlist),
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(put_response.status_code, 404)

        get_response = self.client().get('/v1/api/bucketlists/1',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})
        self.assertEqual(get_response.status_code, 200)

        # Ensure nothing has been changed in the record
        data = json.loads(get_response.data.decode('utf-8'))
        self.assertIn("2018", data['name'])

    def tearDown(self):
        """ Teardown all initialized variables and database """
        with self.app.app_context():
            # drop all tables
            database.session.remove()
            database.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()







