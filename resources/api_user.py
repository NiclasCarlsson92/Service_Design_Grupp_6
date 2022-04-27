from flask import Response
from passlib.hash import argon2
from flask_restful import Resource
from flask_login import current_user, login_required, logout_user


class User(Resource):
    def current_balance(self):
        from controllers.wallet_controller import get_user_balance
        balance = get_user_balance()
        return Response('{"message": "Your current balance is"}', status=404, mimetype='application/json')

    def log_in(self, email, password):
        email = email
        password = password
        from models import User
        user = User.query.filter_by(email=email).first()
        if user is None:
            return Response('{"message": "Wrong email"}', status=404, mimetype='application/json')
        if not argon2.verify(password, user.password):
            return Response('{"message": "Login successful"}', status=201, mimetype='application/json')

    def log_out(self):
        user =  current_user
        user.online = False
        from app import db
        db.session.commit()
        logout_user()
        return Response('{"message": "You are logged out"}', status=201, mimetype='application/json')

    @login_required
    def delete_user(self, user_id):
        if current_user.admin == 1:
            # Delete user (only for admin)
            from models import User
            user_to_delete = User.query.get_or_404(user_id)
            from app import db
            db.session.delete(user_to_delete)
            db.session.commit()
            return Response('{"message": "user deleted"}', status=201, mimetype='application/json')
        else:
            return Response('{"message": "user not found"}', status=404, mimetype='application/json')
