import json
from models import User
from flask_restful import Resource
from flask import Response, request
from resources.verify_token import verify_token


class Wallet(Resource):

    # Get all cryptos balance [/api/v1.0/wallet/{tokenId}]
    def get(self, token):
        verified_token = verify_token(token)
        if verified_token is False:
            return Response(json.dumps({'Error': 'Unauthorized request'}), status=401, mimetype='application/json')
        else:
            user = User.query.filter_by(api_token=token).first()
            from controllers.wallet_controller import get_user_wallet
            wallet = get_user_wallet(user.id)
            all_cryptos = wallet.get_cryptos()
            return Response(json.dumps({'Message': all_cryptos}), status=200, mimetype='application/json')


class WalletBuy(Resource):

    # Buy new token [/api/v1.0/wallet/buy/{tokenId}]
    def post(self, token):
        verified_token = verify_token(token)
        if verified_token is False:
            return Response(json.dumps({'Error': 'Unauthorized request'}), status=401, mimetype='application/json')
        else:
            from controllers.wallet_controller import wallet_buy, get_user_wallet
            data = request.get_json(force=True)
            crypto = data["crypto"]
            amount = data["amount"]
            amount = float(amount)
            user = User.query.filter_by(api_token=token).first()
            wallet = get_user_wallet(user.id)
            result = wallet_buy(crypto=crypto, amount=amount, wallet=wallet, user=user)
            if result == 405:
                return Response(json.dumps({'Message': 'Not enough balance.'}), status=405,
                                mimetype='application/json')
            elif result == 400:
                return Response(json.dumps({'Error' : 'User could not buy crypto.'}), status=400, mimetype='application/json')
            else:
                return Response(json.dumps(f'{f"You have purchased {amount}$ of {crypto}."}'), status=200,
                                mimetype='application/json')


class WalletSell(Resource):

    # Sell token [/api/v1.0/wallet/sell/{tokenId}]
    def post(self, token):
        verified_token = verify_token(token)
        if verified_token is False:
            return Response(json.dumps({'Error': 'Unauthorized request'}), status=401, mimetype='application/json')
        else:
            from controllers.wallet_controller import wallet_sell, get_user_wallet
            data = request.get_json(force=True)
            crypto = data["crypto"]
            amount = data["amount"]
            amount = float(amount)
            user = User.query.filter_by(api_token=token).first()
            wallet = get_user_wallet(user.id)
            result = wallet_sell(crypto=crypto, amount=amount, wallet=wallet, user=user)
            if result == 405:
                return Response(json.dumps({'Message': 'Not enough balance.'}), status=405,
                                mimetype='application/json')
            elif result == 400:
                return Response(json.dumps({'Error' : 'User could not buy crypto.'}),
                                status=400,
                                mimetype='application/json')
            else:
                return Response(json.dumps(f'{f"You have sold {amount}$ of {crypto}"}'),
                                status=200,
                                mimetype='application/json')
