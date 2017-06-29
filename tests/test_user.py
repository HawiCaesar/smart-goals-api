import unittest
import sys, hashlib
from bucketlist import app, classes, views
from flask import request

class UserSmartGoalsTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.tester = app.test_client(self)
        self.user1 = classes.User()
        classes.all_users = {}

    ## Test if User object can be created/ Sign Up
    def test_user_class_can_be_instantiated(self):

        self.user1.create_user("James Brown", "jb@email.com", "ABC")
        self.assertIsInstance(classes.all_users["jb@email.com"], list,
                              "Master User list is not created")

    def test_more_than_one_user(self):
        self.user1.create_user("James Brown", "jb@email.com", "ABC")
        self.user2 = classes.User()
        self.user2.create_user("Fred Oroo", "foroo@email.com", "XYZ")

        count = len(classes.all_users)
        self.assertEqual(count, 2, "Cannot create more than 1 user")
    
    def test_user_can_register(self):

        response = self.tester.post('/sign-up/new-user',
                                    data=dict(fullname="James Brown",
                                              email="jb@email.com",
                                              password="ABC",
                                              confirm_password="ABC"),
                                    follow_redirects=True)

        assert b"Smart Goals | Login" in response.data


    def test_registered_user_can_login(self):
        self.user1.create_user("James Brown", "jb@email.com", "ABC")

        response1 = self.tester.post('/sign-up/new-user',
                                     data=dict(fullname="James Brown",
                                               email="jb@email.com",
                                               password="ABC",
                                               confirm_password="ABC"),
                                     follow_redirects=True)

        with app.test_request_context('/auth/',
                method="POST", data=dict(email="jb@email.com", password="ABC")):

            # User exists after just being added
            if classes.all_users['jb@email.com'][1] == request.form.get('email'):

                hash_object = hashlib.sha1(request.form.get('password').encode())
                entered_password = hash_object.hexdigest()

                self.assertEqual(classes.all_users['jb@email.com'][2],
                                 '3c01bdbb26f358bab27f267924aa2c9a03fcfdb8',
                                 "User cannot be authenticated")

            else:
                sys.stdout = "Request context not initialized well"



        assert b"Smart Goals | Login" in response1.data
        #assert b"Smart Goals | My Bucketlists" in response2.data
        # call the before funcs
        # rv = app.preprocess_request()
        # if rv != None:
        #     response = app.make_response(rv)
        # else:
        #     # do the main dispatch
        #     rv = app.dispatch_request()
        #     response = app.make_response(rv)

        #     # now do the after funcs
        #     response = app.process_response(response)


    def test_login_form_appears_if_form_not_valid(self):
        app.config['WTF_CSRF_ENABLED'] = True
        self.user1.create_user("James Brown", "jb@email.com", "ABC")
        response = self.tester.post('/auth/',
                                    data=dict(email="lj@email.com",
                                              password="ABCz"),
                                    follow_redirects=True)

        assert b"Smart Goals | Login" in response.data

    def test_current_user_can_be_set(self):
        user_details = ["James Brown",
                        "jb@email.com", "3c01bdbb26f358bab27f267924aa2c9a03fcfdb8"]

        views.set_current_user(user_details)
        self.assertEqual(views.current_user,
                         ["James Brown",
                          "jb@email.com", "3c01bdbb26f358bab27f267924aa2c9a03fcfdb8"],
                         "Current user variable cannot be set")





if __name__ == "__main__":
    unittest.main()

    