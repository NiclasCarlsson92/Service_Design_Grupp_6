import datetime
from app import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(100))
    api_token = db.Column(db.String(50))
    admin = db.Column(db.BOOLEAN, default=False)
    online = db.Column(db.BOOLEAN, default=False)
    current_balance = db.Column(db.Float, default=1000)

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
    btc = db.Column(db.Float, default=0)
    eth = db.Column(db.Float, default=0)
    usdt = db.Column(db.Float, default=0)
    bnb = db.Column(db.Float, default=0)
    usdc = db.Column(db.Float, default=0)

    def get_cryptos(self):
        return {"BTC": self.btc, "ETH": self.eth, "USDT": self.usdt, "BNB": self.bnb, "USDC": self.usdc}

    def add_currency(self, currency, amount):
        if currency == "btc":
            self.btc = self.btc + amount
        elif currency == "eth":
            self.eth = self.eth + amount
        elif currency == "usdt":
            self.usdt = self.usdt + amount
        elif currency == "bnb":
            self.bnb = self.bnb + amount
        else:
            self.usdc = self.usdc + amount

    def remove_currency(self, currency, amount):
        if currency == "btc":
            self.btc = self.btc - amount
        elif currency == "eth":
            self.eth = self.eth - amount
        elif currency == "usdt":
            self.usdt = self.usdt - amount
        elif currency == "bnb":
            self.bnb = self.bnb - amount
        else:
            self.usdc = self.usdc - amount


class TransactionHistory(db.Model):
    __tablename__ = "transaction_history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=False)
    amount_usd = db.Column(db.Float, default=0)
    token_name = db.Column(db.String(150))
    token_amount = db.Column(db.Float, default=0)
    time = db.Column(db.DateTime, default=datetime.datetime.now())
    action = db.Column(db.String(150))


class APILogs(db.Model):
    __tablename__ = "api_logs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity = db.Column(db.String(150))
    time = db.Column(db.DateTime, default=datetime.datetime.now())