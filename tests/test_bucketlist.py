import unittest

from bucketlist import app, classes

class BucketlistSmartGoalsTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        self.user1 = classes.User()
        self.user1_bucketlist = classes.Bucketlist()
        classes.all_users = {} #master user list
        classes.all_bucketlists = {} #master bucketlist list

    def test_user_can_make_bucketlist(self):

        self.user1.create_user("Zach Reed", "zreed@email.com", "qaz12#@")

        self.user1_bucketlist.create_bucketlist(classes.all_users['zreed@email.com'][1],
                                                'Career Things',
                                                'Goals to achieve in my career')

        self.assertEqual(classes.all_bucketlists['zreed@email.com'],
                         [{"Career Things":"Goals to achieve in my career"}],
                         "Cannot create bucketlist")

    def test_user_can_make_more_than_one_bucketlist(self):

        self.user1.create_user("John Ist", "jist@email.com", "qaz12#@")

        self.user1_bucketlist.create_bucketlist(classes.all_users['jist@email.com'][1],
                                                'Career Things',
                                                'Goals to achieve in my career')
        self.user1_bucketlist.create_bucketlist(classes.all_users['jist@email.com'][1],
                                                'Travel Manenos',
                                                'Places to travel')

        count = len(classes.all_bucketlists["jist@email.com"])

        self.assertEqual(count, 2, "User cannot make more than one bucketlist")


    def test_user_can_update_bucket_their_bucketlist(self):
        self.user1.create_user("John Brown", "jbrown@email.com", "qaz12#@")

        self.user1_bucketlist.create_bucketlist(classes.all_users['jbrown@email.com'][1],
                                                'Career Things',
                                                'Goals to achieve in my career')

        self.user1_bucketlist.update_bucketlist(classes.all_users['jbrown@email.com'][1], 0,
                                                'Career Targets',
                                                'Target to aim for in my career')

        self.assertEqual(classes.all_bucketlists['jbrown@email.com'][0],
                         {'Career Targets':'Target to aim for in my career'},
                         'User cannot update their bucketlist')

    def test_user_can_delete_their_bucketlist(self):
        self.user1.create_user("Brian Hawi", "bhawi@gmail.com", "qaz12#@")

        self.user1_bucketlist.create_bucketlist(classes.all_users['bhawi@gmail.com'][1],
                                                'Career Things',
                                                'Goals to achieve in my career')
        self.user1_bucketlist.create_bucketlist(classes.all_users['bhawi@gmail.com'][1],
                                                'Travel Manenos',
                                                'Places to travel')

        self.user1_bucketlist.delete_bucketlist(classes.all_users['bhawi@gmail.com'][1], 0)

        self.assertEqual(classes.all_bucketlists['bhawi@gmail.com'][0],
                         {'Travel Manenos':'Places to travel'},
                         "User cannot delete a bucketlist")

    def test_user_can_delete_non_existing_bucketlist(self):
        pass

    def test_user_can_update_non_existing_bucketlist(self):
        pass

