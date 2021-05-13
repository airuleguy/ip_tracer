from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

# Using the standard RequestFactory API to create a form POST request
factory = APIClient()


class TestApi(TestCase):
    def setUp(self) -> None:
        self.trace_url = reverse('trace-ip')
        self.statistics_url = reverse('statistics')

    def test_get_trace_uruguay(self):
        expected_result = {
            "ip": "167.62.158.169",
            "name": "Uruguay",
            "code": "UY",
            "lat": -34.8576,
            "lon": -56.1702,
            "currencies": [
                {
                    "iso": "UYU",
                    "symbol": "$U",
                    "conversion_rate": 0.023
                }, {
                    "iso": "USD",
                    "symbol": "$",
                    "conversion_rate": 1
                }
            ],
            "distance_to_uy": 0
        }

        request = factory.post(self.trace_url, {'ip': '167.62.158.169'})
        self.assertEqual(
            request.body,
            expected_result
        )

    def test_get_trace_argentina(self):
        expected_result = {
            "ip": "181.238.72.59",
            "name": "Argentina",
            "code": "AR",
            "lat": -26.816,
            "lon": -65.2154,
            "currencies": [
                    {
                        "iso": "ARS",
                        "symbol": "AR$",
                        "conversion_rate": 0
                    },
                {
                        "iso": "USD",
                        "symbol": "$",
                        "conversion_rate": 0
                    }
            ],
            "distance_to_uy": 1241.9409161263245,
        }

        request = factory.post(self.trace_url, {'ip': '181.238.72.59'})
        self.assertEqual(
            request.body,
            expected_result
        )

    def test_get_statistics(self):
        create_trace = factory.post(self.trace_url, {'ip': '181.238.72.59'})
        expected_result = {
            "longest_distance": {
                "country": "Argentina",
                "value": 839.5820890289746
            },
            "most_traced": {
                "country": "Argentina",
                "value": 1
            }
        }
        request = factory.get(self.statistics_url)
        self.assertEqual(
            request.body,
            expected_result
        )
