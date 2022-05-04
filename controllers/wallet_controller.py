from flask_login import current_user


def get_user_balance():
    return current_user.current_balance

  
def get_user_wallet(user_id):
    from models import Wallet
    return Wallet.query.filter(Wallet.user_id == user_id).first()


def get_all_cryptos(wallet_id):
    from models import Wallet
    return Wallet.filter_by(id=wallet_id).query(Wallet.btc, Wallet.eth, Wallet.usdt, Wallet.bnb, Wallet.usdc)


def wallet_buy(crypto, amount, wallet, user):
    from app import db
    from models import APILogs, Wallet
    from blueprints.api import api_get
    from models import TransactionHistory

    token_usd = api_get(dict=True)
    token_usd = token_usd[crypto.upper()]
    user.current_balance = user.current_balance - amount
    bought_tokens = amount / token_usd
    token_name = f'${crypto.upper()}'

    if user.current_balance - amount < 0:
        user_activity = "Invalid balance"
        activity = APILogs(activity=user_activity, user_id=user.id)
        db.session.add(activity)
        db.session.commit()
        return "status=400"

    if crypto is not None:
        crypto = crypto.lower()
        wallet = get_user_wallet(user.id)
        wallet.add_currency(crypto, bought_tokens)
        db.session.commit()
        transaction = TransactionHistory(wallet_id=wallet.id, amount_usd=amount, token_name=token_name, token_amount=bought_tokens, action="Buy")
        user_activity = "Buying crypto"
        activity = APILogs(activity=user_activity, user_id=user.id)
        db.session.add(user)
        db.session.add(activity)
        db.session.add(transaction)
        db.session.commit()
        return "status=200"
    else:
        user_activity = "Error user could not buy crypto"
        activity = APILogs(activity=user_activity, user_id=user.id)
        db.session.add(activity)
        db.session.commit()
        return "status=400"


def wallet_sell(crypto, amount, wallet, user):
    from app import db
    from models import APILogs, Wallet
    from blueprints.api import api_get
    from models import TransactionHistory

    token_usd = api_get(dict=True)
    token_usd = token_usd[crypto.upper()]

    if wallet.__dict__[crypto] <= 0:
        user_activity = "Invalid balance"
        activity = APILogs(activity=user_activity, user_id=user.id)
        db.session.add(activity)
        db.session.commit()
        return "status=400"

    sell_usd = amount * token_usd
    user.current_balance = user.current_balance + sell_usd
    token_name = f'${crypto.upper()}'

    if crypto is not None:
        crypto = crypto.lower()
        wallet = Wallet.query.filter_by(id=wallet.id).first()
        wallet.remove_currency(crypto, amount)
        db.session.commit()
        transaction = TransactionHistory(wallet_id=wallet.id, amount_usd=sell_usd, token_name=token_name, token_amount=amount, action="Sell")
        user_activity = "Selling crypto"
        activity = APILogs(activity=user_activity, user_id=user.id)
        db.session.add(user)
        db.session.add(activity)
        db.session.add(transaction)
        db.session.commit()
        return "status=200"
    else:
        user_activity = "Error user could not sell crypto"
        activity = APILogs(activity=user_activity, user_id=user.id)
        db.session.add(activity)
        db.session.commit()
        return "status=400"
