import mock

from django.test import TestCase
from model_bakery import baker

from urls.models import Url


class FakeUUID:
    hex = "abcd"


class UrlModelsTestCase(TestCase):
    @mock.patch("uuid.uuid4", return_value=FakeUUID)
    def test_create_urls_should_generate_a_url_identifier(
        self, url_identifier_generator
    ):
        url = baker.make(Url)
        self.assertEqual(url.url_identifier, "abcd")

    @mock.patch("urls.models.extract_title_from_url.delay", side_effect=None)
    def test_save_method_should_call_a_celery_task(self, mocked_extract_title_from_url):
        url = Url(original_url="http://example.com")
        url.save()

        self.assertEqual(mocked_extract_title_from_url.call_count, 1)

    @mock.patch("urls.models.extract_title_from_url.delay", side_effect=None)
    def test_save_method_should_not_if_the_url_has_a_title_call_a_celery_task(
        self, mocked_extract_title_from_url
    ):
        url = Url(original_url="http://example.com", title="Example Domain")
        url.save()

        self.assertEqual(mocked_extract_title_from_url.call_count, 0)

    def test_assert_get_absolute_url(self):
        url = baker.make(Url, url_identifier="abcd")

        self.assertEqual(url.get_absolute_url(), "/urls/abcd/")

    def test_increment_access_count(self):
        url = baker.make(Url, url_identifier="abcd")
        self.assertEqual(url.access_count, 0)

        url.increment_access_count()

        url.refresh_from_db()
        self.assertEqual(url.access_count, 1)
