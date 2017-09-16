from django.test import TestCase
from homepage.api_calls import get_data, insert_prices
from homepage.models import Tick

class ApiCalls(TestCase):

    test_url = 'http://www.github.com'

    def test_get_data_timeout(self):
        timeout = (0.01, 0.1)  # connect, read
        response = get_data(self.test_url, timeout)
        self.assertEqual(response, -1)

    def test_insert_prices(self):
        usd_zar, xbt_zar, xbt_usd = 1.123, 2.234, 3.345
        insert_prices(usd_zar, xbt_zar, xbt_usd)
