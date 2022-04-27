from flask_restful import Resource
from flask_login import current_user, login_required


class Wallet(Resource):

    @login_required
    def get(self, user_id):
        # Get current balance
        return current_user.current_balance

    @login_required
    def post(self):
        # Buy new token
        pass

    @login_required
    def put(self):
        # Sell token
        pass


