import json
import os
import math
import requests
from dotenv import load_dotenv
from flask import Blueprint, Response, request
from flask_login import login_required, current_user
from controllers.user_controller import get_user_by_id
from controllers.wallet_controller import get_user_wallet
load_dotenv()


bp_api = Blueprint('bp_api', __name__)

API_KEY = os.getenv('API_KEY')

@bp_api.get("/api/v.1/cryptousd")
@login_required
def api_get(**kwargs):
    # This example uses Python 2.7 and the python-request library.

    headers = {
        'Accepts': 'application/json',
        # API Key is linked to an account created by estani

        'X-CMC_PRO_API_KEY': '12c385ec-6a53-458e-b418-d4a987d2e3a5'


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


@bp_api.get("/api/v.1/get_user_crypto")
@login_required
def get_all_cryptos():
    from models import Wallet
    # data = request.get_json(force=True)
    user_id = request.args.get("id")
    user = get_user_by_id(user_id)
    print(user_id)
    wallet = get_user_wallet(user_id)
    crypto = wallet.get_cryptos()
    crypto["userBalance"] = user.current_balance
    return Response(json.dumps(crypto), 200, content_type="application/json")
