import pytest
from flask import Flask, session, url_for, redirect, flash, make_response
from app.controllers.main_controller import verificar_autenticacao
from flask import Blueprint

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login")
def login():
    return "Login"


# Configuração do aplicativo Flask para testes
@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "secret"
    app.config["TESTING"] = True
    app.register_blueprint(auth_bp)

    @app.route("/protected")
    @verificar_autenticacao
    def protected():
        return "Protected"

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_verificar_autenticacao_usuario_nao_autenticado(client):
    with client.session_transaction() as sess:
        sess.clear()  # Garantir que a sessão esteja limpa
    response = client.get("/protected", follow_redirects=False)

    assert response.status_code == 302  # Verifica se houve um redirecionamento
    location = response.headers["Location"]
    assert location.endswith("/login")


# def test_verificar_autenticacao_usuario_autenticado(client):
#     with client.session_transaction() as sess:
#         sess["username"] = "testuser"

#     response = client.get("/protected", follow_redirects=True)
#     print(response.data)
#     print(response.headers)
#     print(response.status_code)
#     print(response.location)
#     print(response.headers["Location"])
#     print(response.headers["Location"].endswith("/protected"))
#     print(response.headers["Location"].endswith("/login"))
#     print(sess)
#     # print(client.get("/login").data)

#     # assert response.status_code == 302
#     # assert "Location" in response.headers
#     # assert response.headers["Location"] == url_for("auth.login", _external=True)

#     location = response.headers["Location"]
#     assert location.endswith("auth.login")
