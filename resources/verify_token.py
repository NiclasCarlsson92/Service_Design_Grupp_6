from models import User


def verify_token(token):
    token_verified = User.query.filter_by(api_token=token).first()
    if token_verified is None:
        return False
    return True
