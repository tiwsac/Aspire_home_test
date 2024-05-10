from app import db
from models.user import User


def create_new_user(username, password, is_admin):
    """ Create new user. """
    if User.query.filter_by(username=username).first() is not None:
        return "Existing User", 400  # existing user
    user = User(username=username, is_admin=is_admin)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    response = 'User Created'
    return response
