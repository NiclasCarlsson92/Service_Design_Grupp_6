import dotenv
from flask import Flask
from flask_restful import Api
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()

# Swagger
SWAGGER_URL = '/documentation'
SWAGGER_JSON = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    SWAGGER_JSON,
    config={
        'app_name': 'Crypto Exchange Api'
    }
)


def create_app():
    # Create a Flask application and configure SQLAlchemy
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123secret'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Create an API instance
    api = Api(app)
    from resources import api_user, api_wallet
    api.add_resource(api_wallet.Wallet, "/api/v1.0/wallets/<string:token>")
    api.add_resource(api_wallet.WalletBuy, "/api/v1.0/wallets/buy/<string:token>")
    api.add_resource(api_wallet.WalletSell, "/api/v1.0/wallets/sell/<string:token>")
    api.add_resource(api_user.User, "/api/v1.0/users/<string:token>")

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.filter_by(id=user_id).first()

    from blueprints.open import bp_open
    app.register_blueprint(bp_open)

    from blueprints.wallet import bp_wallet
    app.register_blueprint(bp_wallet)

    from blueprints.admin import bp_admin
    app.register_blueprint(bp_admin)

    from blueprints.api import bp_api
    app.register_blueprint(bp_api)
    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

    return app


if __name__ == '__main__':
    dotenv.load_dotenv()
    app = create_app()
    app.run()
