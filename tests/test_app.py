import unittest

from bucketlist import app

class SmartGoalsTestCase(unittest.TestCase):
    
    def setUp(self):
        self.tester = app.test_client(self)

    # test if pages return 200 Ok message when called
    def test_index_page_works(self):

        response = self.tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_page_works(self):
        response = self.tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_signup_page_works(self):
        response = self.tester.get('/sign-up', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_about_page_works(self):
        response = self.tester.get('/about', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_contact_page_works(self):
        response = self.tester.get('/contact', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_missing_templates_status(self):
        # Testing status code response page not found"""
        response = self.tester.get('/xyz-page', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    def test_custom_message_for_page_not_found(self):
        response = self.tester.get('/xyz-page', content_type='html/text')
        self.assertTrue(b'Page Not' in response.data, msg="Custom 404 page not working")


if __name__ == "__main__":
    unittest.main()
