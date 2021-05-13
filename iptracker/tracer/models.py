import os
import json

from django.db import models
from django.core.cache import cache
from .utils import get_distance_in_km

URU_LAT, URU_LON = -34.8576, -56.1702  # env


class Country(models.Model):
    name = models.CharField(max_length=25)
    code = models.CharField(max_length=5)
    currency_code = models.CharField(max_length=6)
    times_looked = models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.name

    @property
    def currencies(self):
        rates = cache.get('rates', {})
        dir_path = os.path.dirname(os.path.abspath(__file__))
        relative_path = dir_path + '/currency_symbols.json'
        with open(relative_path, 'r') as file_obj:
            currencies_json = json.load(file_obj)
            country_info = currencies_json.get(self.currency_code, {})
            conversion_rate = rates.get(self.currency_code, 0)
            return [{
                "iso": self.currency_code,
                "symbol": country_info.get('symbol', '$'),
                "conversion_rate": conversion_rate
            }, {
                "iso": "USD",
                "symbol": "$",
                "conversion_rate": 1
            }]


class IpRecordManager(models.Manager):
    def create_with_country(
            self, country_data: dict, ip: str, lat: float, lon: float):
        try:
            # If the country already exists, increase its times_looked
            country = Country.objects.get(
                name=country_data.get('name'))
            country.times_looked += 1
            country.save()
        except Country.DoesNotExist:
            # If it doesnt exist create it
            country = Country.objects.create(
                **country_data
            )
            country.save()
        distance_to_uy = get_distance_in_km(
            lat, lon, URU_LAT, URU_LON
        )
        return self.create(
            ip=ip,
            country=country,
            lat=lat,
            lon=lon,
            distance_to_uy=distance_to_uy
        )

    def get_longest_distance(self):
        furthest_country = self.order_by('-distance_to_uy').first()
        if furthest_country:
            return {
                'country': furthest_country.country.name,
                'value': furthest_country.distance_to_uy
            }
        return {}

    def get_most_traced(self):
        most_traced = Country.objects.order_by('-times_looked').first()
        if most_traced:
            return {
                'country': most_traced.name,
                'value': most_traced.times_looked
            }
        return {}


class IpRecord(models.Model):
    ip = models.CharField(max_length=15, unique=True)
    country = models.ForeignKey(
        Country,
        related_name='ip_country',
        on_delete=models.CASCADE
    )
    distance_to_uy = models.FloatField(default=0)
    lat = models.FloatField()
    lon = models.FloatField()
    objects = IpRecordManager()

    def __str__(self) -> str:
        return f'{self.ip} - {self.country.name}'

    @property
    def name(self):
        return self.country.name

    @property
    def code(self):
        return self.country.code

    @property
    def currency_code(self):
        return self.country.currency_code
