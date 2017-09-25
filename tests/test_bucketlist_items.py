from app import create_application, database
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
        self.bucketlist_item7 = {"item_name": "Travel to Seychelles", "complete_by": "2018-04-03"}
        self.bucketlist_item8 = {"item_name": "Travel to Austraila", "complete_by": "2018-05-03"}
        self.bucketlist_item9 = {"item_name": "Travel to Japan", "complete_by": "2018-03-03"}
        self.bucketlist_item10 = {"item_name": "Travel to Rio", "complete_by": "2019-03-03"}
        self.bucketlist_item11 = {"item_name": "Travel to New Zealand, USA", "complete_by": "2018-03-03"}
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

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        response_item = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item1),
                                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                    "Content-Type": "application/json"})

        self.assertEqual(response_item.status_code, 201)
        self.assertIn("Bucketlist Item Created", json.loads(response_item.data)['message'])

    def test_api_user_cannot_create_existing_bucketlist_item(self):

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        response_item = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                    "Content-Type": "application/json"})

        self.assertEqual(response_item.status_code, 409)
        self.assertIn("Bucketlist Item Already Exists", json.loads(response_item.data)['message'],
                      "Existing bucketlist item should not be created")

    def test_api_get_bucketlist_item(self):
        """ Get all Bucketlist items that has been saved to database """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        get_response_item = self.client().get('/v1/api/bucketlists/1/items/',
                                              headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                       "Content-Type": "application/json"})

        get_response_item2 = self.client().get('/v1/api/bucketlists/',
                                               headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                        "Content-Type": "application/json"})

        data_item = json.loads(get_response_item.data)
        data_item2 = json.loads(get_response_item2.data)

        self.assertEqual(get_response_item.status_code, 200)
        self.assertEqual(get_response_item2.status_code, 200)
        self.assertIn("Travel to NYC, USA", data_item['results'][0]['item_name'])
        self.assertIn("Travel to NYC, USA", data_item2['results'][0]['items'][0]['item_name'])

    def test_api_get_bucketlist_item_by_id(self):
        """ Get bucketlist item by id from database """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        get_response_item = self.client().get('/v1/api/bucketlists/1/items/1',
                                              headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                       "Content-Type": "application/json"})

        data_item = json.loads(get_response_item.data)

        self.assertEqual(get_response_item.status_code, 200)
        self.assertIn("Travel to NYC, USA", data_item['item_name'], "Cannot fetch bucketlist Item")

    def test_api_no_buckelist_item_response_message(self):
        """ Test if the response message is returned when no bucketlist item is created """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        get_response_item = self.client().get('/v1/api/bucketlists/1/items/',
                                              headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                       "Content-Type": "application/json"})

        data_item = json.loads(get_response_item.data)

        self.assertEqual(get_response_item.status_code, 200)
        self.assertEqual(len(data_item['results']), 0)
        self.assertIn("No Bucketlist Items in this Bucketlist", data_item['message'])

    def test_api_test_response_message(self):
        """ Test response message is returned if no parameter passed in GET request for bucketlist items """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        get_response_item = self.client().get('/v1/api/bucketlists//items/',
                                              headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                       "Content-Type": "application/json"})

        self.assertEqual(get_response_item.status_code, 404)
        self.assertIn(b"The requested URL was not found on the server", get_response_item.data,
                      "Bucketlist has no items")

    def test_api_user_can_update_bucketlist_item(self):
        """ Test Case User can update a bucket list item PUT request"""

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        update_item = self.client().put('/v1/api/bucketlists/1/items/1', data=json.dumps(self.bucketlist_item_update),
                                        headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                 "Content-Type": "application/json"})

        get_response_item = self.client().get('/v1/api/bucketlists/1/items/1',
                                              headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                       "Content-Type": "application/json"})

        data_item = json.loads(get_response_item.data)

        self.assertEqual(update_item.status_code, 200)
        self.assertIn("Draw Ed, Edd, Eddy", data_item['item_name'], "Bucketlist item cannot be updated")

    def test_api_user_cannot_update_bucketlist_item_without_id(self):
        """ Test Case User cannot update a bucket list item without id PUT request"""

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        update_item = self.client().put('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item_update),
                                        headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                 "Content-Type": "application/json"})

        self.assertEqual(update_item.status_code, 405)
        self.assertIn(b"405 Method Not Allowed", update_item.data)

    def test_api_user_cannot_update_non_existing_bucketlist_item(self):
        """ Test Case User cannot update a non-existing bucketlist item"""

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        update_item = self.client().put('/v1/api/bucketlists/1/items/5', data=json.dumps(self.bucketlist_item_update),
                                        headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                 "Content-Type": "application/json"})

        data_item = json.loads(update_item.data)

        self.assertEqual(update_item.status_code, 404)
        self.assertIn("Bucketlist item does not exist", data_item['message'],
                      "Bucketlist item cannot be updated because it is non-existed")

    def test_api_user_cannot_update_bucketlist_item_of_different_bucketlist(self):
        """ Test Case User should not be allowed to update bucketlist item of a non-existing or different bucketlist """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item4),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        update_item = self.client().put('/v1/api/bucketlists/4/items/2', data=json.dumps(self.bucketlist_item_update),
                                        headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                 "Content-Type": "application/json"})

        data_item = json.loads(update_item.data.decode())

        self.assertEqual(update_item.status_code, 404)
        self.assertIn("Bucketlist item does not exist", data_item['message'],
                      "Cannot update bucketlist item that does not belong to bucketlist")

    def test_user_can_delete_bucketlist_item(self):
        """Test Case User can delete bucketlist item """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        delete_response = self.client().delete('/v1/api/bucketlists/1/items/1',
                                               headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                        "Content-Type": "application/json"})

        self.assertEqual(delete_response.status_code, 204)

    def test_user_cannot_delete_bucketlist_item_without_id(self):
        """Test Case User can delete bucketlist item """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        delete_response = self.client().delete('/v1/api/bucketlists/1/items/',
                                               headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                        "Content-Type": "application/json"})

        self.assertEqual(delete_response.status_code, 405)
        self.assertIn(b"405 Method Not Allowed", delete_response.data)

    def test_user_cannot_delete_non_existing_bucketlist(self):
        """ Test Case User cannot delete non-existing bucketlist """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        delete_response = self.client().delete('/v1/api/bucketlists/1/items/4',
                                               headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                        "Content-Type": "application/json"})

        self.assertEqual(delete_response.status_code, 404)
        self.assertIn(json.loads(delete_response.data)['message'],
                      "Bucketlist item cannot be deleted as it does not exist")

    def test_user_cannot_delete_bucketlist_item_of_different_bucketlist(self):
        """ Test Case User should not be allowed to delete bucketlist item of a non-existing or different bucketlist """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        delete_response = self.client().delete('/v1/api/bucketlists/4/items/2',
                                               headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                        "Content-Type": "application/json"})

        data_item = json.loads(delete_response.data)

        self.assertEqual(delete_response.status_code, 404)
        self.assertIn("Bucketlist item cannot be deleted as it does not exist", data_item['message'],
                      "Cannot delete bucketlist item that does not belong to bucketlist")

    def test_api_search_bucketlist_items_in_bucketlist_works(self):
        """ Test Case: User can pass query to search for bucketlist items """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item4),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        get_response = self.client().get('/v1/api/bucketlists/1/items/?q=Dr',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data)

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(len(data['results']), 2, "2 results should be returned for search term 'Dr' ")

    def test_api_returns_correct_message_bucketlist_item_non_existent(self):
        """Test Case: User should be given correct error message when fetching non-existing bucketlist item """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        get_response = self.client().get('/v1/api/bucketlists/5/items/6',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data)

        self.assertEqual(get_response.status_code, 404)
        self.assertEqual(data['message'], "That bucketlist item does not exist in bucketlist",
                         "No results non existing bucketlist item")

    def test_api_return_correct_message_if_no_parameters_passed(self):
        """ Test Case: User should be given correct error message when not passing parameters to get bucketlist item """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        get_response = self.client().get('/v1/api/bucketlists/{}/items/{}',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        self.assertEqual(get_response.status_code, 404)
        self.assertIn(b'404 Not Found', get_response.data, "No results non existing bucketlist item")

    def test_api_show_previous_and_next_link(self):
        """ Previous and Next links are shown """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item1),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item7),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item8),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item9),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item10),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item11),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        get_response = self.client().get('/v1/api/bucketlists/1/items/?start=3&limit=3',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data)

        self.assertEqual(get_response.status_code, 200)
        self.assertIn(data['previous'], "/v1/api/bucketlists/1/items/?start=1&limit=2")
        self.assertIn(data['next'], "/v1/api/bucketlists/1/items/?start=6&limit=3")

    def test_api_basic_pagination_for_bucketlist_items(self):
        """ Using a simple GET request on bucketlist items returns a paginated list of 5 items """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item1),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item6),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item7),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item8),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item9),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item10),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item11),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        get_response = self.client().get('/v1/api/bucketlists/1/items/',
                                         headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                  "Content-Type": "application/json"})

        data = json.loads(get_response.data)

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(len(data['results']), 5, "5 results should be returned for simple GET")

    def test_api_cannot_get_bucketlist_item_without_token(self):
        """ Test Case: User cannot GET bucketlist items without auth token """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Content-Type": "application/json"})

        get_response = self.client().get('/v1/api/bucketlists/1/items/', headers={"Content-Type": "application/json"})

        data = json.loads(get_response.data)

        self.assertEqual(get_response.status_code, 401)
        self.assertEqual("Missing Authorization Header", data['msg'])

    def test_api_cannot_post_bucketlist_item_without_token(self):
        """ Test Case: User cannot POST bucketlist items without auth token """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist1),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        response_item1 = self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                                            headers={"Content-Type": "application/json"})

        data = json.loads(response_item1.data)

        self.assertEqual(response_item1.status_code, 401)
        self.assertEqual("Missing Authorization Header", data['msg'])

    def test_api_cannot_put_bucketlist_item_without_token(self):
        """ Test Case: User cannot PUT bucketlist items without auth token """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        update_item = self.client().put('/v1/api/bucketlists/1/items/1', data=json.dumps(self.bucketlist_item_update),
                                        headers={"Content-Type": "application/json"})

        data = json.loads(update_item.data)
        self.assertEqual(update_item.status_code, 401)
        self.assertEqual("Missing Authorization Header", data['msg'])

    def test_api_cannot_delete_bucketlist_item_without_token(self):
        """ Test Case: User cannot DELETE bucketlist items without auth token """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        delete_item = self.client().delete('/v1/api/bucketlists/1/items/1',
                                           headers={"Content-Type": "application/json"})

        data = json.loads(delete_item.data)

        self.assertEqual(delete_item.status_code, 401)
        self.assertEqual("Missing Authorization Header", data['msg'])

    def test_api_cannot_allow_post_request_without_data(self):
        """ User cannot add a bucketlist item without data """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        response_item = self.client().post('/v1/api/bucketlists/1/items/',
                                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                    "Content-Type": "application/json"})

        self.assertEqual(response_item.status_code, 400)
        self.assertIn(b"400 Bad Request", response_item.data)

    def test_api_cannot_allow_put_request_without_data(self):
        """ User cannot update a bucketlist item without data """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})
        response_item1 = self.client().put('/v1/api/bucketlists/1/items/1',
                                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                    "Content-Type": "application/json"})

        self.assertEqual(response_item1.status_code, 400)
        self.assertIn(b"400 Bad Request", response_item1.data)

    def test_api_error_start_and_limit_parameters_are_non_numbers(self):
        """ Server returns an error message when start page and limit is not a number """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item1),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        # Start parameter
        start_response = self.client().get('/v1/api/bucketlists/1/items/?start=r',
                                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                    "Content-Type": "application/json"})
        # Limit parameter
        limit_response = self.client().get('/v1/api/bucketlists/1/items/?limit=e',
                                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                    "Content-Type": "application/json"})
        # Both parameters
        both_response = self.client().get('/v1/api/bucketlists/1/items/?start=r&limit=e',
                                          headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                   "Content-Type": "application/json"})

        data_start_param = json.loads(start_response.data)
        data_limit_param = json.loads(limit_response.data)
        data_both_param = json.loads(both_response.data)

        self.assertEqual(start_response.status_code, 500)
        self.assertEqual(data_start_param['message'], "Start Page and Limits should be numbers only")

        self.assertEqual(limit_response.status_code, 500)
        self.assertEqual(data_limit_param['message'], "Start Page and Limits should be numbers only")

        self.assertEqual(both_response.status_code, 500)
        self.assertEqual(data_both_param['message'], "Start Page and Limits should be numbers only")

    def test_api_correct_message_for_no_items(self):
        """ Trying to get items of non-existent bucketlist """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        get_response_item = self.client().get('/v1/api/bucketlists/5/items/',
                                              headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                       "Content-Type": "application/json"})

        data = json.loads(get_response_item.data)
        self.assertEqual(get_response_item.status_code, 404)
        self.assertIn("No Bucketlist Items Because Bucketlist", data['message'])

    def test_api_search_none_existent_bucketlist_item(self):
        """ Correct message is returned when search returns no result """

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item1),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        get_response_item = self.client().get('/v1/api/bucketlists/1/items/?q=observe',
                                              headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                       "Content-Type": "application/json"})

        data = json.loads(get_response_item.data)

        self.assertEqual(get_response_item.status_code, 404)
        self.assertIn("Bucketlist Item does not exist", data['message'])

    def test_error_message_if_no_update_data(self):

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        update_item = self.client().put('/v1/api/bucketlists/1/items/1', data=json.dumps({"item_name": "",
                                                                                          "complete_by": ""}),
                                        headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                 "Content-Type": "application/json"})

        data = json.loads(update_item.data)

        self.assertEqual(update_item.status_code, 400)
        self.assertIn("Item Name must be provided", data['message'])

    def test_error_message_if_existing_name_given_on_update(self):

        self.client().post('/v1/api/bucketlists/', data=json.dumps(self.bucketlist2),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item3),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        self.client().post('/v1/api/bucketlists/1/items/', data=json.dumps(self.bucketlist_item4),
                           headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                    "Content-Type": "application/json"})

        update_item = self.client().put('/v1/api/bucketlists/1/items/1', data=json.dumps(self.bucketlist_item4),
                                        headers={"Authorization": "Bearer " + self.access_token['access_token'],
                                                 "Content-Type": "application/json"})

        data = json.loads(update_item.data)

        self.assertEqual(update_item.status_code, 400)
        self.assertIn("Cannot update bucketlist item with existing name", data['message'])

    def tearDown(self):
        """ Teardown all initialized variables and database """
        with self.app.app_context():
            # drop all tables
            database.session.remove()
            database.drop_all()
