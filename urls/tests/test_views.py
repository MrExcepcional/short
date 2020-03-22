
from django.test import TestCase
from django.urls import reverse_lazy
from model_bakery import baker

from urls.models import Url


class TestUrlCreateView(TestCase):
    def test_create_url(self):
        data = {
            'original_url': 'http://www.example.com',
        }

        response = self.client.post(
            reverse_lazy('urls:create'),
            data,
        )

        url = Url.objects.get(original_url='http://www.example.com')

        self.assertEqual(Url.objects.count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse_lazy('urls:detail', kwargs={'url_identifier': url.url_identifier})
        )

    def test_create_url_with_invalid_form(self):
        data = {}

        response = self.client.post(
            reverse_lazy('urls:create'),
            data,
        )

        form = response.context_data['form']

        self.assertEqual(Url.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.is_valid(), False)


class TestUrlDetailView(TestCase):
    def setUp(self):
        self.url = baker.make(Url)

    def test_detail_url(self):        
        response = self.client.get(
            reverse_lazy('urls:detail', kwargs={'url_identifier': self.url.url_identifier}),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object'], self.url)

    def test_detail_url_should_return_a_404_for_invalid_url_identifiers(self):        
        response = self.client.get(
            reverse_lazy('urls:detail', kwargs={'url_identifier': 'abcd'}),
        )

        self.assertEqual(response.status_code, 404)


class TestUrlRedirectView(TestCase):
    def setUp(self):
        self.url = baker.make(Url, original_url='http://www.example.com')

    def test_redirect_url(self):
        response = self.client.get(
            reverse_lazy('redirect', kwargs={'url_identifier': self.url.url_identifier}),
        )
        self.url.refresh_from_db()

        self.assertEqual(self.url.access_count, 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url.original_url)

    def test_redirect_url_should_return_a_404_for_invalid_url_identifiers(self):
        response = self.client.get(
            reverse_lazy('redirect', kwargs={'url_identifier': 'abcd'}),
        )

        self.assertEqual(response.status_code, 404)


class TestTopUrlsListView(TestCase):
    def setUp(self):
        baker.make(Url, _quantity=101)

    def test_top_urls(self):
        response = self.client.get(
            reverse_lazy('urls:top-urls'),
        )

        self.assertEqual(response.context_data['urls'].count(), 100)
