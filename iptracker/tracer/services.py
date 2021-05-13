import requests
import os

from django.core.cache import cache

GEOLOC_API_URL = os.getenv('IP_API_URL')
CURRENCY_API = os.getenv('CURRENCY_API_URL')
ACCESS_KEY = os.getenv('CURRENCY_ACCESS_KEY')


def get_geolocation(ip: str) -> dict:
    query_string = f'{ip}?fields=status,country,countryCode,lat,lon,currency,query'
    try:
        data = requests.get(
            f'{GEOLOC_API_URL}/{query_string}'
        )
    except requests.exceptions.RequestException as e:
        return e
    geolocation_data = data.json()
    return {
        'ip': geolocation_data.get('query'),
        'name': geolocation_data.get('country'),
        'code': geolocation_data.get('countryCode'),
        'lat': geolocation_data.get('lat'),
        'lon': geolocation_data.get('lon'),
        'currency_code': geolocation_data.get('currency'),
        'status': geolocation_data.get('status')
    }


def get_and_cache_lastest_currency():
    query_string = f'?access_key={ACCESS_KEY}'
    try:
        data = requests.get(
            f'{CURRENCY_API}/latest{query_string}'
        )
        new_rates = data.json()
        if cache.get('rates'):
            cache.delete('rates')
        cache.set('rates', new_rates.get('rates'))
    except requests.exceptions.RequestException as e:
        pass
