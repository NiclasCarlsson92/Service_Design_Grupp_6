from flask_login import current_user
from controllers.user_controller import get_user_by_id


def get_user_balance():
    return current_user.current_balance


#
# def get_tokens_owned():
#     # wallet = current_user
#
#     # return every token name and amount owned by the wallet
#
def get_user_wallet(user_id):
    from models import Wallet
    return Wallet.query.filter(Wallet.user_id == user_id).first()


def get_all_cryptos(wallet_id):
    from models import Wallet
    # cryptos = []
    return Wallet.filter_by(id=wallet_id).query(Wallet.btc, Wallet.eth, Wallet.usdt, Wallet.bnb, Wallet.usdc)
