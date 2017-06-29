import unittest

from bucketlist import app, classes

class BucketlistActivitySmartGoalsTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        self.user1 = classes.User()
        self.user1_bucketlist = classes.Bucketlist()
        self.user1_bucketlist_activity = classes.Bucketlist_Activities()

        classes.all_users = {} #master user list
        classes.all_bucketlists = {} #master bucketlist list
        classes.all_bucketlists_activities = {} #master bucketlist activity

    def test_user_can_create_bucketlist_activity(self):
        self.user1.create_user("Zach Reed", "zreed@email.com", "qaz12#@")

        self.user1_bucketlist.create_bucketlist(classes.all_users['zreed@email.com'][1],
                                                'Career Things',
                                                'Goals to achieve in my career')

        self.user1_bucketlist_activity.create_bucketlist_activity(
            classes.all_users['zreed@email.com'][1],
            'Career Things',
            'Achieve A', '01/01/2018', False)

        self.assertEqual(classes.all_bucketlists_activities['zreed@email.com'][0],
                         {'Achieve A':[False, '01/01/2018', 'Career Things']},
                         "User cannot create bucketlist activity")

    def test_user_can_create_more_than_one_bucketlist_activity(self):
        self.user1.create_user("Zach Reed", "zreed@email.com", "qaz12#@")

        self.user1_bucketlist.create_bucketlist(classes.all_users['zreed@email.com'][1],
                                                'Career Things',
                                                'Goals to achieve in my career')

        self.user1_bucketlist_activity.create_bucketlist_activity(
            classes.all_users['zreed@email.com'][1],
            'Career Things',
            'Achieve A', '01/01/2018', False)

        self.user1_bucketlist_activity.create_bucketlist_activity(
            classes.all_users['zreed@email.com'][1],
            'Career Things',
            'Achieve XYZ', '01/01/2018', False)

        count = len(classes.all_bucketlists_activities['zreed@email.com'])

        self.assertEqual(count, 2, "User cannot create multiple bucketlist activities")

    def test_user_can_update_bucketlist_activity(self):
        self.user1.create_user("Zach Reed", "zreed@email.com", "qaz12#@")

        self.user1_bucketlist.create_bucketlist(classes.all_users['zreed@email.com'][1],
                                                'Career Things',
                                                'Goals to achieve in my career')

        self.user1_bucketlist_activity.create_bucketlist_activity(
            classes.all_users['zreed@email.com'][1],
            'Career Things',
            'Achieve A', '01/01/2018', False)

        self.user1_bucketlist_activity.create_bucketlist_activity(
            classes.all_users['zreed@email.com'][1],
            'Career Things',
            'Achieve XYZ', '01/01/2018', False)

        self.user1_bucketlist_activity.update_bucketlist_activity(
            classes.all_users['zreed@email.com'][1], 0, 'Career Things', '01/02/2018',
            'Achieve Promotion', False)


        self.assertEqual(classes.all_bucketlists_activities['zreed@email.com'][0],
                         {'Achieve Promotion':[False, '01/02/2018', 'Career Things']},
                         "User cannot update bucketlist activity")



    def test_user_cannot_make_bucketlist_activity_without_bucketlist(self):
        self.user1.create_user("Jane Zeed", "jzeed@email.com", "qaz12#@")

        self.user1_bucketlist.create_bucketlist(classes.all_users['jzeed@email.com'][1],
                                                'Career Things',
                                                'Goals to achieve in my career')

        self.user1_bucketlist_activity.create_bucketlist_activity(
            classes.all_users['jzeed@email.com'][1],
            'Career Things',
            'Achieve Milestone', '01/01/2018', False)

        self.user1_bucketlist_activity.create_bucketlist_activity(
            classes.all_users['jzeed@email.com'][1],
            'Career Things',
            'Achieve Promotion', '05/06/2018', False)

        self.user1_bucketlist_activity.delete_bucketlist_activity(
            classes.all_users['jzeed@email.com'][1], 1)

        count = len(classes.all_bucketlists_activities['jzeed@email.com'])

        self.assertEqual(count, 1, "User cannot delete bucketlist activities")
