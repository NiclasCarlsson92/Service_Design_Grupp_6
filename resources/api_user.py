import json
from flask import Response
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

    def put_log_out(self, token):
        if verify_token(token) == "False":
            return Response('{"Unauthorized request"}', status=401, mimetype='application/json')
        else:
            return Response('{"message": "You are logged out"}', status=201, mimetype='application/json')


    #def delete_user(self, token, user_id):

       #    from models import User
       #    user_to_delete = User.query.get_or_404(user_id)
       #     from app import db
       #     db.session.delete(user_to_delete)
       #     db.session.commit()
       #     return Response('{"message": "user deleted"}', status=201, mimetype='application/json')
       # else:
       #     return Response('{"message": "user not found"}', status=404, mimetype='application/json')
