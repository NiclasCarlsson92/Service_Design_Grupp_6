import json

import requests
from flask import Blueprint, Response
from flask_login import login_required

bp_api = Blueprint('bp_api', __name__)


@bp_api.get("/api/v.1/cryptousd")
@login_required
def api_get(**kwargs):
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

    # Response
    json_data = requests.get(url, params=params, headers=headers).json()
    crypto = {}
    coins = json_data['data']
    for x in coins:
        # print(x['symbol'], x['quote']['USD']['price'])
        crypto[x['symbol']] = x['quote']['USD']['price']

    # kwargs return the dict whilst no kwargs returns a response with a json
    if kwargs is not None:
        return crypto

    return Response(json.dumps(crypto), 200, content_type="application/json")