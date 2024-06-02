import pytest
from flask import url_for, session
from app import create_app, db
from app.models.user import User
from app.forms import SignupForm, LoginForm


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


@pytest.fixture(scope="module")
def client(test_app):
    return test_app.test_client()


def test_signup(client, test_app):
    # Testa o cadastro com dados válidos
    response = client.post(
        "/auth/signup",
        data={
            "username": "testuser",
            "password": "Password123",
            "confirm_password": "Password123",
        },
        follow_redirects=True,  # Seguir redirecionamento
    )
    assert response.status_code == 200


def test_login(client, test_app):
    # Testa o login com dados válidos
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "Password123"},
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_logout(client):
    # Realiza o login para poder testar o logout
    client.post(
        "/auth/login",
        data={"username": "testuser", "password": "Password123"},
        follow_redirects=True,
    )

    # Testa o logout
    response = client.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200

    # Verifica se a sessão do usuário foi limpa
    with client.session_transaction() as session:
        assert "username" not in session
