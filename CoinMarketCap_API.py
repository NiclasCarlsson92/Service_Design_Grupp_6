import requests
import json
# from requests import Request, Session
# from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
# import json


def api():
    # This example uses Python 2.7 and the python-request library.

    headers = {
        'Accepts': 'application/json',
        # API Key is linked to an account created by estani
        'X-CMC_PRO_API_KEY': '12c385ec-6a53-458e-b418-d4a987d2e3a5',
    }
    params = {
        'start': '1',
        'limit': '5',
        'convert': 'USD'
    }

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    json_data = requests.get(url, params=params, headers=headers).json()

    coins = json_data['data']
    for x in coins:
        print(x['symbol'], x['quote']['USD']['price'])


if __name__ == '__main__':
    api()

