from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import logout_user, login_required, current_user
from passlib.hash import argon2
from controllers.user_controller import get_all_but_current_users, get_user_by_id

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

    from app import db
    db.session.add(user, activity)
    db.session.commit()

    return render_template('Wallet.html', user=user, activity=activity)
