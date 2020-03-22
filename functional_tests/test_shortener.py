import os
import time
import re

from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


MAX_WAIT = 10


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    """docstring for FunctionalTest"""

    def setUp(self):
        self.browser = webdriver.Firefox()
        # self.staging_server = os.environ.get('STAGING_SERVER')
        # if self.staging_server:
        #     self.live_server_url = 'http://' + self.staging_server

    def tearDown(self):
        self.browser.quit()

    def get_shortner_input_box(self):
        return self.browser.find_element_by_id("id_original_url")

    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def wait_for_shortened_link(self):
        url_result = self.browser.find_element_by_id("shortner-url").get_attribute(
            "value"
        )
        url_search = re.search(r"http://.+$", url_result)
        if not url_search:
            self.fail(f"Coulf not find url in:\n{url_result}")
        url = url_search.group(0)
        # TODO: change hardcoded localhost to self.live_server_url
        self.assertIn("localhost", url)

    def test_can_get_shortened_url(self):
        # Susan goes to th awesome url-shortener site
        self.browser.get(self.live_server_url)

        # She notices the page title mention shortner
        self.assertIn("Shortner", self.browser.title)
        # and header mention New URL lists
        header_text = self.browser.find_element_by_tag_name("h2").text
        self.assertIn("New URL", header_text)

        # She is invited to enter a link to shorten straight away
        inputbox = self.get_shortner_input_box()
        self.assertEqual(inputbox.get_attribute("placeholder"), "URL")

        # She enters a long link
        inputbox.send_keys("https://www.youtube.com/watch?v=_sldz7NZsOg")
        inputbox.send_keys(Keys.ENTER)

        # She waits for the page to update and sees her shortened url
        self.wait_for_shortened_link()

        # Satisfied with her new url she goes back to sleep,
        # but tomorrow she will use the shortened link to see if
        # redirects to the original website... story continues.
