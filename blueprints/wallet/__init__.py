from blueprints.api import api_get
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, Response
from controllers.wallet_controller import get_user_wallet, wallet_buy, wallet_sell

bp_wallet = Blueprint('bp_wallet', __name__)


# @bp_wallet.get('/logout')
# def logout_get():
#     user = current_user
#     user.online = False
#     from app import db
#     db.session.commit()
#     logout_user()
#     return redirect(url_for('bp_open.index_get'))


@bp_wallet.get('/wallet')
@login_required
def wallet_get():
    from models import APILogs
    user = current_user
    user_activity = 'Visiting wallet'
    activity = APILogs(activity=user_activity)

    # We use the kwargs to get a dict instead of a response
    cryptos = api_get(dict=True)
    print(cryptos)
    from app import db
    db.session.add(user, activity)
    db.session.commit()

    return render_template('wallet.html', user=user, activity=activity, cryptos=cryptos)


# TODO add more activity and make transaction history real, and add ajax to the buy and sell html for the wallet
@bp_wallet.put('/api/v.1/buy')
@login_required
def wallet_buy():
    data = request.get_json(force=True)
    crypto = data["crypto"]
    amount = data["amount"]
    amount = float(amount)
    wallet = get_user_wallet(current_user.id)
    result = wallet_buy(crypto=crypto, amount=amount, wallet=wallet, user=current_user)
    return Response(result)

@bp_wallet.put('/api/v.1/sell')
def wallet_sell():
    from app import db
    from models import APILogs
    from models import TransactionHistory

    data = request.get_json(force=True)

    crypto = data["crypto"]
    amount = data["amount"]
    amount = float(amount)
    user = current_user
    wallet = get_user_wallet(user.id)
    # Do this bit for crypto
    held_crypto = wallet.get_cryptos()

    if held_crypto[crypto.upper()] < amount:
        user_activity = "Invalid crypto balance"
        activity = APILogs(activity=user_activity, user_id=user.id)
        db.session.add(activity)
        db.session.commit()
        return Response(status=400)

    token_usd = api_get(dict=True)
    token_usd = token_usd[crypto.upper()]
    token_name = f'${crypto.upper()}'
    sell_tokens = amount * token_usd

    if crypto is not None:
        wallet = getattr(wallet, crypto.lower()) - amount
        user.current_balance = user.current_balance + sell_tokens
        user_activity = "Selling crypto"
        activity = APILogs(activity=user_activity, user_id=user.id)
        transaction = TransactionHistory(wallet_id=wallet.id, amount_usd=sell_tokens, token_name=token_name,
                                         token_amount=amount, action="Sell")
        db.session.add(user)
        db.session.add(wallet)
        db.session.add(activity)
        db.session.add(transaction)
        db.session.commit()
        return Response()
    else:
        user_activity = "Error user could not sell crypto"
        activity = APILogs(activity=user_activity, user_id=user.id)
        db.session.add(activity)
        db.session.commit()
        return Response(status=400)


@bp_wallet.get("/buy")
@login_required
def wallet_get_buy():
    user = current_user
    wallet = get_user_wallet(user.id)
    wallet = wallet.get_cryptos()
    cryptos = api_get(dict=True)
    return render_template("buy_crypto.html", user=user, wallet=wallet, cryptos=cryptos)


@bp_wallet.get("/sell")
@login_required
def wallet_get_sell():
    user = current_user
    wallet = get_user_wallet(user.id)
    wallet = wallet.get_cryptos()
    cryptos = api_get(dict=True)
    return render_template("sell_crypto.html", user=user, wallet=wallet, cryptos=cryptos)
