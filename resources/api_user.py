import json
from flask import Response, request
from flask_restful import Resource
from resources.verify_token import verify_token


class Client(Resource):
    # Get current balance
    def get(self, token):
        verified_token = verify_token(token)
        if verified_token == "False":
            return Response('{"Unauthorized request"})', status=401, mimetype='application/json')
        else:
            from models import User
            user = User.query.filter_by(api_token=token).first()
            balance = user.current_balance
            return Response(json.dumps({"message": "Your current balance is: " + str(balance) + "$"}), status=200, mimetype='application/json')


    def put(self, token):
        if verify_token(token) == "False":
            return Response('{"Unauthorized request"}', status=401, mimetype='application/json')
        from models import User
        from passlib.hash import argon2
        admin = User.query.filter_by(api_token=token).first()
        if admin.admin == 1:
            data = request.get_json(force=True)
            email = data["email"]
            password = data["new password"]
            user = User.query.filter_by(email=email).first()
            ## TODO Include an if sats for right email and wrong email.
            hashed_password = argon2.using(rounds=10).hash(password)
            user.password = hashed_password
            from app import db
            db.session.add(user)
            db.session.commit()
            return Response('{"message": "Password updated"}', status=201, mimetype='application/json')


    def delete(self, token):
        verified_token = verify_token(token)
        if verified_token == "False":
            return Response('{"Unauthorized request"})', status=401, mimetype='application/json')
        from models import User
        admin = User.query.filter_by(api_token=token).first()
        if admin.admin == 1:
            data = request.get_json(force=True)
            email = data["email"]
            user_to_delete = User.query.filter_by(email=email).first()
            if user_to_delete is not None:
                from app import db
                db.session.delete(user_to_delete)
                db.session.commit()
                return Response('{"message": "User deleted"}', status=201, mimetype='application/json')
            else:
                return Response('{"message": "User not found"}', status=404, mimetype='application/json')
        else:
            return Response('{"message": "You need admin privilege to perform that request"}', status=400, mimetype='application/json')
