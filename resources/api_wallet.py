import json
from flask import Response, request
from models import User, Wallet
from flask_restful import Resource
from resources.verify_token import verify_token


class Wallet(Resource):
    # Get all cryptos balance
    def get(self, token):
        verified_token = verify_token(token)
        if verified_token == "False":
            return Response('{"Unauthorized request"})', status=401, mimetype='application/json')
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
            data = request.get_json(force=True)
            print(data)


    def put(self, token):
        verified_token = verify_token(token)
        if verified_token == "False":
            return Response('{"Unauthorized request"})', status=401, mimetype='application/json')
        #else:
        # Sell token
        pass


