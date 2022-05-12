"""imported json"""
import json
from flask import Response, request
from flask_restful import Resource
from resources.verify_token import verify_token


class User(Resource):
    # Get current balance [/api/v1.0/user/{token}]
    def get(self, token):
        verified_token = verify_token(token)
        if verified_token is False:
            return Response(json.dumps({"Error": "Unauthorized request"}), status=401, mimetype='application/json')
        else:
            from models import User
            user = User.query.filter_by(api_token=token).first()
            balance = user.current_balance
            message = {"id": user.id, "name": user.name, "balance": str(user.current_balance) + "$", "email": user.email,
                       "admin": user.admin, 'links': {
                        'Crypto market(GET)': f'/api/v1.0/wallets/{user.api_token}',
                        "Change password(PUT)": f'/api/v1.0/users/{user.api_token}',
                        'Delete user(DEL)': f'/api/v1.0/users/{user.api_token}'
                        }}

            return Response(json.dumps({"Message": message}), status=200,
                            mimetype='application/json')

    # Update password [/api/v1.0/user/{token}]
    def put(self, token):
        verified_token = verify_token(token)
        if verified_token is False:
            return Response(json.dumps({"Error": "Unauthorized request"}), status=401, mimetype='application/json')
        from models import User
        from passlib.hash import argon2
        admin = User.query.filter_by(api_token=token).first()
        if admin.admin == 1 or admin.api_token == token:
            data = request.get_json(force=True)
            email = data["email"]
            password = data["new password"]
            user = User.query.filter_by(email=email).first()
            if user is None:
                return Response(json.dumps({"Message": "Bad request"}), status=400, mimetype='application/json')
            else:
                hashed_password = argon2.using(rounds=10).hash(password)
                user.password = hashed_password
                from app import db
                db.session.add(user)
                db.session.commit()
                return Response(json.dumps({"Message": "Password updated"}), status=202, mimetype='application/json')

    # Delete user [/api/v1.0/user/{token}]
    def delete(self, token):
        verified_token = verify_token(token)
        if verified_token is False:
            return Response(json.dumps({"Error": "Unauthorized request"}), status=401, mimetype='application/json')
        from models import User
        admin = User.query.filter_by(api_token=token).first()
        if admin.admin == 1 or admin.api_token == token:
            data = request.get_json(force=True)
            email = data["email"]
            user_to_delete = User.query.filter_by(email=email).first()
            if user_to_delete is not None:
                from app import db
                db.session.delete(user_to_delete)
                db.session.commit()
                return Response(json.dumps({"Message": "User deleted"}), status=200, mimetype='application/json')
            else:
                return Response(json.dumps({"message": "User not found"}), status=404, mimetype='application/json')
        else:
            return Response(json.dumps({"Error": "You need admin privilege to perform that request"}), status=401,
                            mimetype='application/json')
