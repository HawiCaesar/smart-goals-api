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
        self.bucketlist_item1 = {"item_name": "Travel to Dusseldorf, Germany", "complete_by": "2018-01-03"}
        self.bucketlist_item2 = {"item_name": "Travel to NYC, USA", "complete_by": "2018-03-03"}
        self.bucketlist_item3 = {"item_name": "Draw Batman", "complete_by": "2018-05-01"}
        self.bucketlist_item4 = {"item_name": "Draw Spiderman", "complete_by": "2018-02-01"}
        self.bucketlist_item5 = {"item_name": "Draw Ironman", "complete_by": "2018-02-01"}
        self.bucketlist_item6 = {"item_name": "Draw Hulk", "complete_by": "2018-02-01"}
        self.bucketlist_item_update = {"item_name": "Draw Ed, Edd, Eddy", "done": "true", "complete_by":"2018-05-02"}
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

        self.assertIn("Travel to NYC, USA", data_item['results'][0]['item_name'], "Cannot fetch bucketlist Item")

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

        self.assertIn("No bucketlist item matching your query in exists", data_item['message'],
                      "Bucketlist has no items")

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

    def test_api_user_can_update_bucketlist_item(self):
        """ Test Case User can update a bucket list item PUT request"""

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/1',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 200)

        response_item1 = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                                            headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                     "Content-Type": "application/json"})

        self.assertEqual(response_item1.status_code, 201)

        update_item = self.client().put('/v1/api/bucketlists/1/items/1', data=json.dumps(self.bucketlist_item_update),
                                        headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                 "Content-Type": "application/json"})

        self.assertEqual(update_item.status_code, 200)

        get_response_item = self.client().get('/v1/api/bucketlists/1/items/1',
                                              headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                       "Content-Type": "application/json"})

        self.assertEqual(get_response_item.status_code, 200)
        data_item = json.loads(get_response_item.data.decode())

        self.assertIn("Draw Ed, Edd, Eddy", data_item['item_name'], "Bucketlist item cannot be updated")

    def test_api_user_cannot_update_non_existing_bucketlist_item(self):
        """ Test Case User cannot update a non-existing bucketlist item"""

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/1',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 200)

        response_item1 = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                                            headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                     "Content-Type": "application/json"})

        self.assertEqual(response_item1.status_code, 201)

        update_item = self.client().put('/v1/api/bucketlists/1/items/5', data=json.dumps(self.bucketlist_item_update),
                                        headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                 "Content-Type": "application/json"})

        self.assertEqual(update_item.status_code, 404)

        data_item = json.loads(update_item.data.decode())

        self.assertIn("Bucketlist item does not exist", data_item['message'],
                      "Bucketlist item cannot be updated because it is non-existed")

    def test_api_user_cannot_update_bucketlist_item_of_different_bucketlist(self):
        """ Test Case User should not be allowed to update bucketlist item of a non-existing or different bucketlist """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/1',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 200)

        response_item1 = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                                            headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                     "Content-Type": "application/json"})

        self.assertEqual(response_item1.status_code, 201)

        response_item1 = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item4),
                                            headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                     "Content-Type": "application/json"})

        self.assertEqual(response_item1.status_code, 201)

        update_item = self.client().put('/v1/api/bucketlists/4/items/2', data=json.dumps(self.bucketlist_item_update),
                                        headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                 "Content-Type": "application/json"})

        self.assertEqual(update_item.status_code, 404)

        data_item = json.loads(update_item.data.decode())

        self.assertIn("Bucketlist item does not exist", data_item['message'],
                      "Cannot update bucketlist item that does not belong to bucketlist")



    def test_user_can_delete_bucketlist(self):
        """Test Case User can delete bucketlist item """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/1',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 200)

        response_item1 = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                                            headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                     "Content-Type": "application/json"})

        self.assertEqual(response_item1.status_code, 201)

        delete_response = self.client().delete('/v1/api/bucketlists/1/items/1',
                                               headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                        "Content-Type": "application/json"})

        self.assertEqual(delete_response.status_code, 204)



    def test_user_cannot_delete_non_existing_bucketlist(self):
        """ Test Case User cannot delete non-existing bucketlist """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/1',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 200)

        response_item1 = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                                            headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                     "Content-Type": "application/json"})

        self.assertEqual(response_item1.status_code, 201)

        delete_response = self.client().delete('/v1/api/bucketlists/1/items/4',
                                               headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                        "Content-Type": "application/json"})

        self.assertEqual(delete_response.status_code, 404)

    def test_user_cannot_delete_bucketlist_item_of_different_bucketlist(self):
        """ Test Case User should not be allowed to delete bucketlist item of a non-existing or different bucketlist """

        response = self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                                      headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                               "Content-Type": "application/json"})

        self.assertEqual(response.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/1',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 200)

        response_item1 = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                                            headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                     "Content-Type": "application/json"})

        self.assertEqual(response_item1.status_code, 201)

        response_item1 = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item4),
                                            headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                     "Content-Type": "application/json"})

        self.assertEqual(response_item1.status_code, 201)

        delete_response = self.client().delete('/v1/api/bucketlists/4/items/2',
                                               headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                        "Content-Type": "application/json"})

        self.assertEqual(delete_response.status_code, 404)

        data_item = json.loads(delete_response.data.decode())

        self.assertIn("Bucketlist item cannot be deleted as it does not exist", data_item['message'],
                      "Cannot delete bucketlist item that does not belong to bucketlist")

    def test_api_search_term_for_bucketlist_items_in_bucketlist_works(self):
        """ Test Case: User can pass query to search for bucketlist items """

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

        response_item = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item4),
                                            headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                     "Content-Type": "application/json"})

        self.assertEqual(response_item.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/1/items/?q=Dr',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data.decode('utf-8'))

        self.assertEqual(get_response.status_code, 200)

        self.assertEqual(len(data['results']), 2, "2 results should be returned for search term 'Dr' ")

    def test_api_returns_correct_message_if_bucketlist_item_non_existent(self):
        """Test Case: User should be given correct error message when fetching non-existing bucketlist item """

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

        get_response = self.client().get('/v1/api/bucketlists/5/items/6',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data.decode('utf-8'))

        self.assertEqual(get_response.status_code, 404)

        self.assertEqual(data['message'], "That bucketlist item does not exist in bucketlist",
                         "No results non existing bucketlist item")

    def test_api_return_correct_message_if_no_parameters_passed_to_search_bucketlist_item(self):
        """ Test Case: User should be given correct error message when not passing parameters to get bucketlist item """

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

        get_response = self.client().get('/v1/api/bucketlists/{}/items/{}',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 404)

        self.assertIn(b'404 Not Found', get_response.data, "No results non existing bucketlist item")

    def test_api_show_previous_and_next_link_for_many_bucketlist_items(self):
        """ Previous and Next links are shown """

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

        response_item = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item4),
                                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                    "Content-Type": "application/json"})

        self.assertEqual(response_item.status_code, 201)

        response_item = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item5),
                                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                    "Content-Type": "application/json"})

        self.assertEqual(response_item.status_code, 201)

        response_item = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item6),
                                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                    "Content-Type": "application/json"})

        self.assertEqual(response_item.status_code, 201)

        get_response = self.client().get('/v1/api/bucketlists/1/items/?start=2&limit=2',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data.decode('utf-8'))

        self.assertEqual(get_response.status_code, 200)

        self.assertEqual(data['previous'], "/v1/api/bucketlists/1/items/?start=1&limit=2", "Test has no previous link")


    def tearDown(self):
        """ Teardown all initialized variables and database """
        with self.app.app_context():
            # drop all tables
            database.session.remove()
            database.drop_all()
