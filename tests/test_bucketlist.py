from bucketlist import create_application, database
import unittest
import json
import sys


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

    def test_api_fetches_user_specific_bucketlists(self):
        """ User should only access their bucketlists """

        # Register different user
        user_data = {
            'email': 'test2@example.com',
            'password': 'test2_password'
        }

        register_response = self.client().post('/v1/api/auth/register', data=json.dumps(user_data),
                                               headers=self.headers)

        register_result = json.loads(register_response.data.decode())

        self.assertEqual(register_result['message'], "User registered successfully.")
        self.assertEqual(register_response.status_code, 201)

        # Login diferent user

        login_response = self.client().post('/v1/api/auth/login', data=json.dumps(user_data),
                                            headers=self.headers)

        login_result = json.loads(login_response.data.decode())

        self.assertEqual(login_result['message'], "User has logged in!")
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(login_result['access_token'])  # New User Access Token

        # User 1 posts bucketlist
        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist4),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        # User 2 posts bucketlist
        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                                      headers={"Authorization": "Bearer " + login_result['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        # User 1's bucketlist
        get_response = self.client().get('/v1/api/bucketlists/',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data.decode('utf-8'))
        self.assertIn("2018", data['results'][0]['name'])

        # User 2's bucketlist
        get_response = self.client().get('/v1/api/bucketlists/',
                                         headers={"Authorization": "Bearer " + login_result['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data.decode('utf-8'))
        self.assertIn("Travel Manenos", data['results'][0]['name'])


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

    def test_api_get_paginated_bucketlists(self):
        """ Test Case User can fetch bucketlists in paginated form", 4 inserted but 3 returned"""

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        response2 = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response2.status_code, 201)

        response3 = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist3),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response3.status_code, 201)

        response4 = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist4),
                                       headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                "Content-Type": "application/json"})

        self.assertEqual(response4.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 200)

        data = json.loads(get_response.data.decode('utf-8'))

        # 4 bucketlists inserted but results are paginated
        self.assertEqual(3, len(data['results']), "Fetched bucketlists cannot be paginated")


    def test_api_bucketlist_next_and_previous_page_links(self):
        """ The bucketlist api provide next and previous url links when pagination is done """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        response2 = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                       headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                "Content-Type": "application/json"})

        self.assertEqual(response2.status_code, 201)

        response3 = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist3),
                                       headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                "Content-Type": "application/json"})

        self.assertEqual(response3.status_code, 201)

        response4 = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist4),
                                       headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                "Content-Type": "application/json"})

        self.assertEqual(response4.status_code, 201)

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps({"name":"Learn Piano"}),
                                       headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Learn Guitar"}),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 200)

        data = json.loads(get_response.data.decode('utf-8'))

        self.assertEqual(3, len(data['results']), "Fetched bucketlists cannot be paginated")

        get_response = self.client().get('/v1/api/bucketlists/?start=1&limit=3',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data.decode('utf-8'))

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(data['next'], '/v1/api/bucketlists/?start=2&limit=3', "Next page link not provided")
        self.assertEqual(data['previous'], '', 'Previous link should be empty for start of 1')

    def test_api_search_bucketlist_works(self):
        """ Test Case: User can pass query to search for bucketlist """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Draw Caricatures"}),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Draw Business Logos"}),
                                       headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Play Drums"}),
                                       headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "2018 Milestones"}),
                                       headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/?q=Dr',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data.decode('utf-8'))

        self.assertEqual(get_response.status_code, 200)

        self.assertEqual(len(data['results']), 3, "3 results should be returned for search term 'Dr' ")

    def test_api_search_bucketlist_returns_correct_message_for_no_bucketlist_found(self):
        """ Test Case: The API should return a 'no such bucketlist is found' message when no result is found """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Draw Caricatures"}),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Draw Business Logos"}),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Play Drums"}),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/?q=zx',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data.decode('utf-8'))

        self.assertEqual(get_response.status_code, 404)

        self.assertEqual('No Bucketlist matching your query was found', data['message'], "Wrong message returned")


    def tearDown(self):
        """ Teardown all initialized variables and database """
        with self.app.app_context():
            # drop all tables
            database.session.remove()
            database.drop_all()


# # Make the tests conveniently executable
# if __name__ == "__main__":
#     unittest.main()







