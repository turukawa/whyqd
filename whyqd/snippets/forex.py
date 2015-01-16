from django.conf import settings
from django.core.cache import cache

import urllib2                    # For downloading the currency data
import json                       # Allows the data to be decoded
# https://github.com/ashokfernandez/PyExchangeRates/blob/master/PyExchangeRates.py

CURRENCY_CHOICE = ("gbp", "usd", "eur")
BASE_CURRENCY = "gbp"

def get_forex():
    # https://openexchangerates.org/quick-start
    fx = cache.get('forex_key', 'has expired')
    if fx == 'has expired':
        # Get the latest currency rates from the API
        latest = urllib2.urlopen(settings.OPEXRATE_API_URL)
        full_fx = json.loads(latest.read())
        fx = {}
        for c in CURRENCY_CHOICE:
            fx[c] = full_fx['rates'][c.upper()]/full_fx['rates'][BASE_CURRENCY.upper()]
        cache.set('full_forex_key', full_fx)
        cache.set('forex_key', fx)
    return fx