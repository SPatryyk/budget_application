import requests
from datetime import date
from .models import ExchangeRate
from decimal import Decimal

CURRENCY_API_KEY = 'cur_live_m2OtohlWOiEJrKtA454yxrb9MVAAfdVMEbL00bWX'
CURRENCY_API_URL = 'https://api.currencyapi.com/v3/latest'
CURRENCIES = ['PLN', 'USD', 'EUR']


def get_exchange_rate(base_currency: str, target_currency: str):
    today = date.today()

    try:
        record = ExchangeRate.objects.get(
            base_currency=base_currency, target_currency=target_currency)
        if record.updated_at == today:
            return record.rate
        else:
            record.delete()
    except ExchangeRate.DoesNotExist:
        pass

    response = requests.get(CURRENCY_API_URL, params={
        'apikey': CURRENCY_API_KEY,
        'base_currency': 'PLN',
        'currencies': ','.join(CURRENCIES)
    })

    if response.status_code != 200:
        print(f"Błąd API: {response.status_code} {response.text}")
        return None

    data = response.json().get('data', {})

    for target in CURRENCIES:
        if target == 'PLN':
            continue
        rate = data.get(target, {}).get('value')
        if rate:
            ExchangeRate.objects.update_or_create(
                base_currency='PLN', target_currency=target,
                defaults={'rate': Decimal(rate), 'updated_at': today}
            )
            if rate != 0:
                inverse_rate = 1 / Decimal(rate)
                ExchangeRate.objects.update_or_create(
                    base_currency=target, target_currency='PLN',
                    defaults={'rate': inverse_rate, 'updated_at': today}
                )

    for base in ['USD', 'EUR']:
        response = requests.get(CURRENCY_API_URL, params={
            'apikey': CURRENCY_API_KEY,
            'base_currency': base,
            'currencies': 'USD,EUR'
        })
        data = response.json().get('data', {})
        for target in ['USD', 'EUR']:
            if base == target:
                continue
            rate = data.get(target, {}).get('value')
            if rate:
                ExchangeRate.objects.update_or_create(
                    base_currency=base, target_currency=target,
                    defaults={'rate': Decimal(rate), 'updated_at': today}
                )

    try:
        record = ExchangeRate.objects.get(
            base_currency=base_currency, target_currency=target_currency)
        return record.rate
    except ExchangeRate.DoesNotExist:
        return None
