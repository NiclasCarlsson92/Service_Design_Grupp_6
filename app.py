import dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


db = SQLAlchemy()


def create_app():

    # Create a Flask application
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123secret'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Create an API instance
    api = Api(app)
    from resources import api_user, api_wallet
    api.add_resource(api_wallet.Wallet, "/api/v1.0/wallet/<string:token>")
    api.add_resource(api_user.Client, "/api/v1.0/user/<string:token>")

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

    return app


if __name__ == '__main__':
    dotenv.load_dotenv()
    app = create_app()
    app.run()
