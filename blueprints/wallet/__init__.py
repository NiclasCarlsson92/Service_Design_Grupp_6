from blueprints.api import api_get
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, Response
from controllers.wallet_controller import get_user_wallet
from controllers.wallet_controller import wallet_buy as WB
from controllers.wallet_controller import wallet_sell as WS

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
    cryptos = api_get(dict=True)
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
    result = WB(crypto=crypto, amount=amount, user=current_user, wallet=wallet)
    return Response(result)


@bp_wallet.put('/api/v.1/sell')
def wallet_sell():
    data = request.get_json(force=True)
    crypto = data["crypto"]
    amount = data["amount"]
    amount = float(amount)
    wallet = get_user_wallet(current_user.id)
    result = WS(crypto=crypto, amount=amount, user=current_user, wallet=wallet)
    return Response(result)


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
