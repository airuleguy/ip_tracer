from tracer.utils import deg2rad, get_distance_in_km
from django.test import TestCase


class TestUtils(TestCase):
    def test_deg2rad(self):
        expected_result = 0.017453292519943295
        self.assertEqual(
            expected_result,
            deg2rad(1),
        )

    def test_get_distance_in_km(self):
        lat_arg, lon_arg = -38.416097, -63.616672
        lat_uru, lon_uru = -32.522779, -55.765835
        expected_result = 966.2
        distance = round(get_distance_in_km(
            lat_arg, lon_arg, lat_uru, lon_uru
        ), 1)
        self.assertEqual(
            expected_result,
            distance
        )
