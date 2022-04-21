from flask_login import current_user
from controllers.user_controller import get_user_by_id


def get_user_balance():
    return current_user.current_balance


def get_tokens_owned():
    # wallet = current_user

    # return every token name and amount owned by the wallet