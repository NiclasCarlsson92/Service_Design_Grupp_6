from flask_login import login_user
from passlib.hash import argon2
from models import User
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import logout_user, login_required, current_user

bp_open = Blueprint('bp_open', __name__)


@bp_open.get('/')
def login_get():
    return render_template('login.html')


@bp_open.post('/login')
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('Wrong email or password')
        return redirect(url_for('bp_open.login_get'))

    if not argon2.verify(password, user.password):
        flash('Wrong email or password')
        return redirect(url_for('bp_open.login_get'))

    login_user(user)
    user.online = True

    from app import db
    db.session.commit()
    return render_template('index.html')


@bp_open.get('/logout')
def logout_get():
    user = current_user
    user.online = False
    from app import db
    db.session.commit()
    logout_user()
    return redirect(url_for('bp_open.index_get'))


@bp_open.get('/signup')
def signup_get():
    return render_template('signup.html')


@bp_open.post('/signup')
def signup_post():
    name = request.form['name']
    email = request.form.get('email')
    password = request.form['password']
    hashed_password = argon2.using(rounds=10).hash(password)
    user = User.query.filter_by(email=email).first()
    if user:
        flash("Email address is already in use")
        return redirect(url_for('bp_open.signup_get'))

    if not email:
        flash("Please enter an email")
        return redirect(url_for('bp_open.signup_get'))

    if not password:
        flash("Please enter a password")
        return redirect(url_for('bp_open.signup_get'))

    new_user = User(name=name, email=email, password=hashed_password)
    from models import Wallet
    wallet = Wallet(user_id=new_user.get_id())
    new_user.wallet_id = wallet.id

    from app import db
    db.session.add(new_user, wallet)
    db.session.commit()
    login_user(new_user)

    return redirect(url_for('bp_open.login_get'))
