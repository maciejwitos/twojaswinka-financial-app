from app.models import Currency
from scraper.currency_scraper import *
import json


def read_values():

    try:
        GetCurrencies.scrap_currencies()
    except:
        pass

    try:
        values = json.load(open('scraper/currencies.json', 'r'))

        eur = Currency.objects.get(name='EUR')
        eur.in_pln = values['EUR']
        eur.save()

        usd = Currency.objects.get(name='USD')
        usd.in_pln = values['USD']
        usd.save()

        gbp = Currency.objects.get(name='GBP')
        gbp.in_pln = values['GBP']
        gbp.save()

        nok = Currency.objects.get(name='NOK')
        nok.in_pln = values['NOK']
        nok.save()

        chf = Currency.objects.get(name='CHF')
        chf.in_pln = values['CHF']
        chf.save()

        btc = Currency.objects.get(name='BTC')
        btc.in_pln = values['BTC']
        btc.save()

    except:
        pass
