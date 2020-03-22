import responses

from django.test import override_settings
from django.test import TestCase
from model_bakery import baker

from url_shortner.models import Url
from url_shortner.tasks import extract_title_from_url


class TasksTestCase(TestCase):
    def setUp(self):
        self.url = baker.make(Url, original_url="http://example.com")

    @responses.activate
    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_extract_title_from_url(self):
        responses.add(
            responses.GET,
            url="http://example.com",
            body="<html><title>Example Domain</title></html>",
        )

        extract_title_from_url.delay(self.url.id)

        self.url.refresh_from_db()
        self.assertEqual(self.url.title, "Example Domain")
