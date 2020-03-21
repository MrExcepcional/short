from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase



class FunctionalTest(StaticLiveServerTestCase):
    """docstring for FunctionalTest"""

    def setUp(self):
        self.browser=webdriver.Firefox()
        # self.staging_server = os.environ.get('STAGING_SERVER')
        # if self.staging_server:
        #     self.live_server_url = 'http://' + self.staging_server

    def tearDown(self):
        self.browser.quit()

    def test_can_get_shortened_url(self):
        # Susan goes to th awesome url-shortener site
        self.browser.get('http:localhost:8000')

        # She notices the page title mention shortner
        self.assertIn('Shortner', self.browser.title)

        self.fail('finish the test!!!')
        # and header mention New URL lists

        # She is invited to enter a link to shorten straight away

        # She enters a long link

        # She waits for the page to update and sees her shortened url

        # Satisfied with her new url she goes back to sleep
        # (but tomorrow she will use the shortened link to see if 
        # redirects to the original website... story continues)