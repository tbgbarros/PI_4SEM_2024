import pytest
from flask import Flask
from flask import url_for
from app import create_app, db
from app.models.user import User


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://root:@localhost/mamaco_test"
    )
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="module")
def client(test_app):
    return test_app.test_client()


@pytest.fixture(scope="module")
def init_database(test_app):
    with test_app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


def test_signup_page(client):
    with client:
        response = client.get("/auth/signup")  # Corrija o caminho da rota
        assert response.status_code == 200
        assert b"Criar conta!" in response.data


def test_signup_success(client, init_database):
    with client:
        response = client.post(
            "/auth/signup",  # Corrija o caminho da rota
            data={
                "username": "newuser",
                "password": "Password123",
                "confirm_password": "Password123",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200


def test_signup_failure(client, init_database):
    with client:
        response = client.post(
            "/auth/signup",  # Corrija o caminho da rota
            data={
                "username": "newuser",
                "password": "Password123",
                "confirm_password": "WrongPassword",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200


@pytest.fixture(scope="function")
def new_user():
    user = User(username="testuser", password="Password123")
    return user


def test_set_password(new_user):
    assert new_user.password_encrypted is not None
    assert new_user.hash is not None


def test_check_password(new_user):
    assert new_user.check_password("Password123") is True
    assert new_user.check_password("WrongPassword") is False


def test_user_creation(test_app, init_database, new_user):
    with test_app.app_context():
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(username="testuser").first()
        assert user is not None
        assert user.username == "testuser"
