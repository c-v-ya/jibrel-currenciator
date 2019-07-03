import base64
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from src.apps.currenciator.models import Currency, Rate


class TestRateView(TestCase):

    def setUp(self) -> None:
        User.objects.create_user('test', 'test@test.com', 'test')
        self.auth = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(
                b'test:test').decode(),
        }

    def test_get_rate(self):
        now = timezone.now()
        currency = Currency.objects.create(name='Test')

        rates = list()
        for i in range(10):
            rate = Rate(
                currency=currency,
                date=now - timedelta(days=i),
                rate=10,
                volume=i * 2
            )
            rates.append(rate)

        Rate.objects.bulk_create(rates)
        data = {'id': currency.id}
        response = self.client.get(
            reverse('currenciator:rate'), data, **self.auth
        )

        self.assertEqual(200, response.status_code)

    def test_missing_id(self):
        response = self.client.get(reverse('currenciator:rate'), **self.auth)
        self.assertEqual(400, response.status_code)
