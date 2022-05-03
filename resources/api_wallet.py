import json
from flask import Response, request
from models import User
from flask_restful import Resource
from resources.verify_token import verify_token


class Wallet(Resource):
    # Get all cryptos balance
    def get(self, token):
        verified_token = verify_token(token)
        if verified_token == "False":
            return Response("{'Error':'Unauthorized request'})", status=401, mimetype='application/json')
        else:
            user = User.query.filter_by(api_token=token).first()
            from controllers.wallet_controller import get_all_cryptos, get_user_wallet
            wallet = get_user_wallet(user.id)
            all_cryptos = wallet.get_cryptos()
            return Response(json.dumps({"message": all_cryptos}), status=201, mimetype='application/json')

    # Buy new token
    def post(self, token):
        verified_token = verify_token(token)
        if verified_token == "False":
            return Response('{"Unauthorized request"})', status=401, mimetype='application/json')
        else:
            from controllers.wallet_controller import wallet_buy, get_user_wallet
            data = request.get_json(force=True)
            crypto = data["crypto"]
            amount = data["amount"]
            amount = float(amount)
            user = User.query.filter_by(api_token=token).first()
            wallet = get_user_wallet(user.id)
            result = wallet_buy(crypto=crypto, amount=amount, wallet=wallet, user=user)
            return Response('{"Success"})', status=201, mimetype='application/json')

    # Sell token
    def put(self, token):
        verified_token = verify_token(token)
        if verified_token == "False":
            return Response('{"Unauthorized request"})', status=401, mimetype='application/json')
        else:
            from controllers.wallet_controller import wallet_sell, get_user_wallet
            data = request.get_json(force=True)
            crypto = data["crypto"]
            amount = data["amount"]
            amount = float(amount)
            user = User.query.filter_by(api_token=token).first()
            wallet = get_user_wallet(user.id)
            result = wallet_sell(crypto=crypto, amount=amount, wallet=wallet, user=user)
            return Response('{"Success"})', status=201, mimetype='application/json')
