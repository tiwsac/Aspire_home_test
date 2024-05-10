import pytest

from main import app, db
from models.loan import Loan
from models.emi import EMI
from models.user import User


@pytest.fixture()
def test_app():
    test_app = app
    test_app.config.update(
        TESTING=True,
        SECRET_KEY="test key",
    )
    return test_app


@pytest.fixture
def client(test_app):
    return app.test_client()


@pytest.mark.parametrize(
    ("username", "password", "is_admin", "message"),
    (
        ("test_user", "python", False, b"User Created"),
        ("test_admin", "python", True, b"User Created"),
    ),
)
def test_create_new_user(client, username, password, is_admin, message):
    """ Test for admin and non-admin user creation """
    response = client.post(
        "/api/create/user", json={"username": username, "password": password, "isAdmin": is_admin}
    )

    user_query = User.query.filter(User.username == username)
    user = user_query.first()
    user_is_admin = user.is_admin
    # removing test data
    user_query.delete()
    db.session.commit()

    assert message == response.data
    assert is_admin == user_is_admin


@pytest.mark.parametrize(
    ("username", "password", "is_admin", "message", "code"),
    (
        ("test_user", "python", False, b"Existing User", 400),
        ("test_admin", "python", True, b"Existing User", 400),
    ),
)
def test_create_new_user_failure(client, username, password, is_admin, message, code):
    """ Test for admin and non-admin existing user creation """
    response = client.post(
        "/api/create/user", json={"username": username, "password": password, "isAdmin": is_admin}
    )
    response = client.post(
        "/api/create/user", json={"username": username, "password": password, "isAdmin": is_admin}
    )

    user_query = User.query.filter(User.username == username)
    user = user_query.first()
    user_is_admin = user.is_admin
    # removing test data
    user_query.delete()
    db.session.commit()

    assert message == response.data
    assert code == response.status_code
    assert is_admin == user_is_admin


