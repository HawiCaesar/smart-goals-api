from bucketlist import create_application, database
import unittest
import json
import sys

class BucketlistTestCases(unittest.TestCase):
    pass

    def setUp(self):
        self.app = create_application(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist1 = {"name": "Travel Manenos"}
        self.bucketlist2 = {"name": "Draw caricatures"}
        self.bucketlist_item1 = {"item_name": "Travel to Dusseldorf, Germany",
                                 "complete_by": "2018-01-03"}
        self.bucketlist_item2 = {"item_name": "Travel to NYC, USA", "complete_by": "2018-03-03"}
        self.bucketlist_item3 = {"item_name": "Draw Batman", "complete_by": "2018-05-01"}
        self.bucketlist_item4 = {"item_name": "Draw Spiderman", "complete_by": "2018-02-01"}
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


    def test_api_buckelist_item_creation(self):
        """ Test Case: Create Bucketlist Item """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/1',
                                   headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                            "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 200)

        response_item = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item1),
                                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                    "Content-Type": "application/json"})

        self.assertEqual(response_item.status_code, 201)

        data_item = json.loads(response_item.data.decode())

        self.assertIn("Bucketlist Item Created", data_item['message'], "Bucketlist Item not created")

    def test_api_user_cannot_create_existing_bucketlist_item(self):

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/1',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 200)

        response_item = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                    "Content-Type": "application/json"})

        self.assertEqual(response_item.status_code, 201)

        response_item2 = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                    "Content-Type": "application/json"})

        self.assertEqual(response_item2.status_code, 409)

        data_item = json.loads(response_item2.data.decode())

        self.assertIn("Bucketlist Item Already Exists", data_item['message'], "Existing bucketlist item should not be created")



    def test_api_get_bucketlist_item(self):
        """ Get all Bucketlist items that has been saved to database """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/1',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 200)

        response_item = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item2),
                                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                    "Content-Type": "application/json"})

        self.assertEqual(response_item.status_code, 201)

        get_response_item = self.client().get('/v1/api/bucketlists/1/items/',
                                              headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                       "Content-Type": "application/json"})

        self.assertEqual(get_response_item.status_code, 200)
        data_item = json.loads(get_response_item.data.decode())

        self.assertIn("Travel to NYC, USA", data_item[0]['item_name'], "Cannot fetch bucketlist Item")

    def test_api_get_bucketlist_item_by_id(self):
        """ Get bucketlist item by id from database """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/1',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 200)

        # One Bucketlist item
        response_item1 = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item1),
                                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                    "Content-Type": "application/json"})

        self.assertEqual(response_item1.status_code, 201)

        # Second Bucketlist item
        response_item2 = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item2),
                                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                    "Content-Type": "application/json"})

        self.assertEqual(response_item2.status_code, 201)

        get_response_item = self.client().get('/v1/api/bucketlists/1/items/2',
                                              headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                       "Content-Type": "application/json"})

        self.assertEqual(get_response_item.status_code, 200)
        data_item = json.loads(get_response_item.data.decode())

        self.assertIn("Travel to NYC, USA", data_item['item_name'], "Cannot fetch bucketlist Item")

    def test_api_no_buckelist_item_response_message(self):
        """ Test if the response message is returned when no bucketlist item is created """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/1',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 200)

        get_response_item = self.client().get('/v1/api/bucketlists/1/items/',
                                              headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                       "Content-Type": "application/json"})

        self.assertEqual(get_response_item.status_code, 404)
        data_item = json.loads(get_response_item.data.decode())

        self.assertIn("No bucketlist items in bucketlist", data_item['message'], "Bucketlist has no items")

    def test_api_test_response_message(self):
        """ Test response message is returned if no parameter passed in GET request for bucketlist items """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/1',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 200)

        get_response_item = self.client().get('/v1/api/bucketlists//items/',
                                              headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                       "Content-Type": "application/json"})

        self.assertEqual(get_response_item.status_code, 404)

        self.assertIn(b"The requested URL was not found on the server", get_response_item.data, "Bucketlist has no items")



    def tearDown(self):
        """ Teardown all initialized variables and database """
        with self.app.app_context():
            # drop all tables
            database.session.remove()
            database.drop_all()
