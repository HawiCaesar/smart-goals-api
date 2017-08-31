from app import create_application, database
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

        # new user
        user_data2 = {
            'email': 'test2@example.com',
            'password': 'test2_password'
        }

        register_response = self.client().post('/v1/api/auth/register', data=json.dumps(user_data2),
                                               headers=self.headers)

        register_result = json.loads(register_response.data.decode())

        login_response = self.client().post('/v1/api/auth/login', data=json.dumps(user_data2),
                                            headers=self.headers)

        self.login_result2 = json.loads(login_response.data.decode())

        # Register Asserts
        self.assertIn(register_result['message'], "User registered successfully.")
        self.assertEqual(register_response.status_code, 201)

        # Login Asserts
        self.assertIn(self.login_result2['message'], "User has logged in!")
        self.assertEqual(login_response.status_code, 200)

    def test_bucketlist_creation(self):
        """ User can create a bucketlist """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertIn('Bucketlist Created', data['message'])

    def test_api_can_get_bucketlist_by_id(self):
        """ Test API can get a specific bucketlist by id """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist4),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        result = self.client().get('/v1/api/bucketlists/1',
                                   headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                            "Content-Type": "application/json"})
        data = json.loads(result.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result.status_code, 200)
        self.assertIn("2018", data['name'])

    def test_api_fetch_all_bucketlists(self):
        """ Test API can fetch all bucketlists GET request """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        response2 = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist3),
                                       headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                "Content-Type": "application/json"})

        get_response = self.client().get('/v1/api/bucketlists/',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response2.status_code, 201)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(len(data['results']), 2)

    def test_api_access_protected_page_without_token(self):
        """ Test API can fetch all bucketlists GET request without token"""

        get_response = self.client().get('/v1/api/bucketlists/',
                                         headers={"Content-Type": "application/json"})

        data = json.loads(get_response.data)

        self.assertEqual(get_response.status_code, 401)
        self.assertIn("Missing Authorization Header", data['msg'])

    def test_api_fetches_user_specific_bucketlists(self):
        """ User should only access their bucketlists """

        # User 1 posts bucketlist
        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist4),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        # User 2 posts bucketlist
        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                           headers={"Authorization": "Bearer " + self.login_result2['access_token'],
                                    "Content-Type": "application/json"})

        # User 1's bucketlist
        get_response1 = self.client().get('/v1/api/bucketlists/',
                                          headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                   "Content-Type": "application/json"})

        data1 = json.loads(get_response1.data)

        # User 2's bucketlist
        get_response2 = self.client().get('/v1/api/bucketlists/',
                                          headers={"Authorization": "Bearer " + self.login_result2['access_token'],
                                                   "Content-Type": "application/json"})

        data2 = json.loads(get_response2.data)

        self.assertIn("2018", data1['results'][0]['name'])
        self.assertIn("Travel Manenos", data2['results'][0]['name'])

    def test_api_bucketlist_can_be_updated(self):
        """ Update bucketlist PUT request"""

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist4),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        put_response = self.client().put('/v1/api/bucketlists/1', data=json.dumps(self.updated_bucketlist),
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(put_response.status_code, 200)

        get_response = self.client().get('/v1/api/bucketlists/1',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data)
        put_data = json.loads(put_response.data)

        self.assertIn("2018 Milestones", data['name'])
        self.assertIn("Bucketlist successfully updated", put_data["message"])

    def test_api_bucketlist_cannot_be_updated_without_id(self):
        """ Cannot Update bucketlist without id PUT request"""

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist4),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        put_response = self.client().put('/v1/api/bucketlists/', data=json.dumps(self.updated_bucketlist),
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(put_response.status_code, 405)
        self.assertIn(b"405 Method Not Allowed", put_response.data)

    def test_api_bucketlist_can_be_deleted(self):
        """ Delete bucketlist DELETE request """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        delete_response = self.client().delete('/v1/api/bucketlists/1',
                                               headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                        "Content-Type": "application/json"})

        # Check if bucketlist has been deleted
        get_response = self.client().get('/v1/api/bucketlists/1',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 404)
        self.assertEqual(delete_response.status_code, 200)

        self.assertIn('deleted', json.loads(delete_response.data)['message'])
        self.assertIn('Bucketlist Does Not Exist', json.loads(get_response.data)['message'])

    def test_api_delete_non_existing_bucketlist(self):
        """ Test Case: Delete non existing bucketlist """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        delete_response = self.client().delete('/v1/api/bucketlists/9',
                                               headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                        "Content-Type": "application/json"})

        self.assertEqual(delete_response.status_code, 404)
        self.assertIn('Bucketlist does not exist', json.loads(delete_response.data)['message'])

    def test_api_delete_bucketlist_without_id(self):
        """ Test Case: delete bucketlist without id """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        delete_response = self.client().delete('/v1/api/bucketlists/',
                                               headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                        "Content-Type": "application/json"})

        self.assertEqual(delete_response.status_code, 405)
        self.assertIn(b"405 Method Not Allowed", delete_response.data)

    def test_api_update_non_exisiting_bucketlist(self):
        """ Test Case: Update non exisiting bucketlist """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist4),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        put_response = self.client().put('/v1/api/bucketlists/3', data=json.dumps(self.updated_bucketlist),
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        get_response = self.client().get('/v1/api/bucketlists/1',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(put_response.status_code, 404)

        # Ensure nothing has been changed in the record
        data = json.loads(get_response.data.decode('utf-8'))
        self.assertIn("2018", data['name'])

    def test_api_get_paginated_bucketlists(self):
        """ Test Case User can fetch bucketlists in paginated form", 7 inserted but 5 returned"""

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist4),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Things to manually make"}),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Cars to drive"}),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Learn Guitar"}),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        get_response = self.client().get('/v1/api/bucketlists/',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data.decode('utf-8'))

        # 7 bucketlists inserted but results are paginated
        self.assertEqual(5, len(data['results']), "Fetched bucketlists cannot be paginated")

    def test_api_bucketlist_next_and_previous_page_links(self):
        """ The bucketlist api provide next and previous url links when pagination is done """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist4),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/', data=json.dumps({"name":"Learn Piano"}),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Learn Guitar"}),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        get_response = self.client().get('/v1/api/bucketlists/?start=1&limit=3',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data)

        self.assertEqual(get_response.status_code, 200)
        self.assertIn(data['next'], '/v1/api/bucketlists/?start=4&limit=3', "Next page link not provided")
        self.assertIn(data['previous'], '', 'Previous link should be empty for start of 1')

    def test_api_search_bucketlist_works(self):
        """ Test Case: User can pass query to search for bucketlist """

        self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Draw Caricatures"}),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Draw Business Logos"}),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Play Drums"}),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "2018 Milestones"}),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        get_response = self.client().get('/v1/api/bucketlists/?q=Dr',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data)

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(len(data['results']), 3, "3 results should be returned for search term 'Dr' ")

    def test_api_returns_correct_message_for_no_bucketlist_found(self):
        """ Test Case: The API should return a 'no such bucketlist is found' message when no result is found """

        self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Draw Caricatures"}),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Draw Business Logos"}),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Play Drums"}),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        get_response = self.client().get('/v1/api/bucketlists/?q=zx',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data)

        self.assertEqual(get_response.status_code, 404)
        self.assertIn('Bucketlists Do Not Exist', data['message'])
        self.assertEqual(0, len(data['results']))

    def test_api_user_cannot_create_existing_bucketlist(self):
        """ Test Case: The API should refuse the user from recreating an existing bucketlist """

        self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Draw Caricatures"}),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps({"name": "Draw Caricatures"}),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 409)
        self.assertEqual("Bucketlist already exists", data['message'], "Cannot recreate existing bucketlist")

    def test_api_cannot_post_bucketlist_without_token(self):
        """ Test Case: User cannot POST without auth token """

        post_response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                           headers={"Content-Type": "application/json"})

        data = json.loads(post_response.data)

        self.assertEqual(post_response.status_code, 401)
        self.assertIn("Missing Authorization Header", data['msg'])

    def test_api_cannot_put_bucketlist_without_token(self):
        """ Test Case: User cannot PUT without auth token """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        put_response = self.client().put('/v1/api/bucketlists/1', data=json.dumps({"name":"Draw Caricature"}),
                                         headers={"Content-Type": "application/json"})

        data = json.loads(put_response.data)

        self.assertEqual(put_response.status_code, 401)
        self.assertIn("Missing Authorization Header", data['msg'])

    def test_api_cannot_delete_bucketlist_without_token(self):
        """ Test Case: User cannot DELETE without auth token """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        delete_response = self.client().delete('/v1/api/bucketlists/1',
                                               headers={"Content-Type": "application/json"})

        data = json.loads(delete_response.data)

        self.assertEqual(delete_response.status_code, 401)
        self.assertIn("Missing Authorization Header", data['msg'])

    def test_api_cannot_allow_post_request_without_data(self):
        """ Server returns an error when user tries to post no data """
        response = self.client().post('/v1/api/bucketlists/',
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"400 Bad Request", response.data)

    def test_api_cannot_allow_put_request_without_data(self):
        """ Server returns an error when user tries to put no data """
        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        put_response = self.client().put('/v1/api/bucketlists/1',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(put_response.status_code, 400)
        self.assertIn(b"400 Bad Request", put_response.data)

    def test_api_query_parameters_are_non_numbers(self):
        """ Server returns an error message when start page and limit is not a number """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        # Start parameter
        start_response = self.client().get('/v1/api/bucketlists/?start=e',
                                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                    "Content-Type": "application/json"})

        # Limit parameter
        limit_response = self.client().get('/v1/api/bucketlists/?limit=e',
                                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                    "Content-Type": "application/json"})

        # Both paramters
        both_response = self.client().get('/v1/api/bucketlists/?start=e&limit=e',
                                          headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                   "Content-Type": "application/json"})

        data_start_param = json.loads(start_response.data)
        data_limit_param = json.loads(limit_response.data)
        data_both_params = json.loads(both_response.data)

        self.assertEqual(start_response.status_code, 500)
        self.assertEqual(limit_response.status_code, 500)
        self.assertEqual(both_response.status_code, 500)

        self.assertIn(data_start_param['message'], "Start Page and Limits should be numbers only")

        self.assertIn(data_limit_param['message'], "Start Page and Limits should be numbers only")

        self.assertIn(data_both_params['message'], "Start Page and Limits should be numbers only")

    def tearDown(self):
        """ Teardown all initialized variables and database """
        with self.app.app_context():
            # drop all tables
            database.session.remove()
            database.drop_all()


# # Make the tests conveniently executable
# if __name__ == "__main__":
#     unittest.main()







