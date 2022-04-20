from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import logout_user, login_required, current_user
from controllers.user_controller import get_all_but_current_users, get_user_by_id

bp_user = Blueprint('bp_user', __name__)


@bp_user.get('/logout')
def logout_get():
    user = current_user
    user.online = False
    from app import db
    db.session.commit()
    logout_user()
    return redirect(url_for('bp_open.index'))


@bp_user.get('/wallet')
@login_required
def user_get():
    users = get_all_but_current_users()
    return render_template('Wallet.html', users=users)