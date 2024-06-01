import pytest
from flask import Flask
from flask import url_for
from app import create_app, db
from app.models.user import User


@pytest.fixture(scope="module")
def rodando_app():
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
def client(rodando_app):
    return rodando_app.test_client()


@pytest.fixture(scope="module")
def init_database(rodando_app):
    with rodando_app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


def teste_criar_usuario(client):
    with client:
        response = client.get("/auth/signup")  # Corrija o caminho da rota
        assert response.status_code == 200
        assert b"Criar conta!" in response.data


def teste_usuario_criado_sucesso(client, init_database):
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


def teste_criacao_usuario_falhou(client, init_database):
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
