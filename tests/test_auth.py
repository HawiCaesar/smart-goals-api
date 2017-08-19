import unittest
import json
from app import create_application, database

class AuthTestCases(unittest.TestCase):
    """Test case for the authentication blueprint."""

    def setUp(self):
        """Set up test variables."""
        self.app = create_application(config_name="testing")
        # initialize the test client
        self.client = self.app.test_client
        # This is the user test json data with a predefined email and password
        self.user_data = {
            'email': 'test@example.com',
            'password': 'test_password'
        }

        # Unregistered User
        self.non_user = {
            'email': 'non_user@example.com',
            'password': 'nope'
        }
        self.headers = {'Content-Type': 'application/json'}

        with self.app.app_context():
            # create all tables
            database.session.close()
            database.drop_all()
            database.create_all()

    def test_can_register_successfully(self):
        """ Allow user to register """

        response = self.client().post('/v1/api/auth/register', data=json.dumps(self.user_data),
                                      headers=self.headers)

        result = json.loads(response.data.decode())

        self.assertIn(result['message'], "User registered successfully.")
        self.assertEqual(response.status_code, 201)

    def test_registered_user_cannot_register_twice(self):
        """ A user cannot enter be allowed to register twice """

        response = self.client().post('/v1/api/auth/register', data=json.dumps(self.user_data), headers=self.headers)
        response2 = self.client().post('/v1/api/auth/register', data=json.dumps(self.user_data), headers=self.headers)

        self.assertEqual(response.status_code, 201)

        self.assertEqual(response2.status_code, 409)

        result = json.loads(response2.data.decode())
        self.assertIn(result['message'], "User already registered. Kindly Login")

    def test_user_login(self):
        """ Allow the user to login """

        response = self.client().post('/v1/api/auth/register', data=json.dumps(self.user_data), headers=self.headers)

        login_response = self.client().post('/v1/api/auth/login', data=json.dumps(self.user_data),
                                            headers=self.headers)

        result = json.loads(login_response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertIn(result['message'], "User has logged in!")
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue('access_token' in result)

    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""

        response = self.client().post('/v1/api/auth/login', data=json.dumps(self.non_user), headers=self.headers)

        result = json.loads(response.data.decode())

        # 401(Unauthorized User)
        self.assertEqual(response.status_code, 401)
        self.assertIn(result['message'], "Invalid email or password, Please try again")

    def tearDown(self):
        """ Teardown all initialized variables """
        with self.app.app_context():
            # drop all tables
            database.session.remove()
            database.drop_all()



