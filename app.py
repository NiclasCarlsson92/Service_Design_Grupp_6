import dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# We will use a factory function to avoid cyclic imports
def create_app():
    app = Flask(__name__)
    # Many parts of flask will require to use a secret key, so we need to create one
    app.config['SECRET_KEY'] = '123secret'
    # Turn off SQLAlchemy warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Will configure SQLAlchemy to use SQLite anthe file db.sqlite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Init the SQLAlchemy object with our app object
    db.init_app(app)

    # Handle flask-login stuff

    #Create login manager for flask-login
    login_manager = LoginManager()

    # Init the login manager with our app object
    login_manager.init_app(app)

    # Create user_loader function. Used by flask-login
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.filter_by(id=user_id).first()

    # Register the open blueprint with the app object
    # from blueprints.open import bp_open
    # app.register_blueprint(bp_open)

    # Register the user blueprint with the app object
    from blueprints.user import bp_user
    app.register_blueprint(bp_user)

    # Register the admin blueprint with the app object
    # from blueprints.admin import bp_admin
    # app.register_blueprint(bp_admin)


    return app


if __name__ == '__main__':
    dotenv.load_dotenv()
    app = create_app()
    app.run()