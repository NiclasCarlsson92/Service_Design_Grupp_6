import datetime
from app import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(100))
    admin = db.Column(db.BOOLEAN, default=False)
    online = db.Column(db.BOOLEAN, default=False)
    current_balance = db.Column(db.Integer, default=1000)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Wallet(db.Model):
    __tablename__ = "wallet"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    btc = db.Column(db.Float)
    eth = db.Column(db.Float)
    usdt = db.Column(db.Float)
    bnb = db.Column(db.Float)
    usdc = db.Column(db.Float)


class TransactionHistory(db.Model):
    __tablename__ = "transaction_history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=False)
    amount_usd = db.Column(db.Integer)
    token_name = db.Column(db.String(150))
    token_amount = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.datetime.now())


class APILogs(db.Model):
    __tablename__ = "api_logs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity = db.Column(db.String(150))
    time = db.Column(db.DateTime, default=datetime.datetime.now())
