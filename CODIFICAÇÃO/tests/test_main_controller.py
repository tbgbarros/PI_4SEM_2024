# Importações necessárias para os testes
import pytest  # Importa o módulo pytest para executar os testes
from flask import (
    Flask,
    session,
    url_for,
    redirect,
    flash,
    make_response,
)  # Importa classes e funções do módulo flask
from app.controllers.main_controller import (
    verificar_autenticacao,
)  # Importa a função verificar_autenticacao do módulo app.controllers.main_controller
from flask import Blueprint  # Importa a classe Blueprint do módulo flask

# Cria um blueprint para autenticação
auth_bp = Blueprint("auth", __name__)


# Rota para login
@auth_bp.route("/login")
def login():
    return "Login"


# Configuração do aplicativo Flask para testes
@pytest.fixture
def app():
    app = Flask(__name__)  # Cria uma instância do aplicativo Flask
    app.secret_key = "secret"  # Define a chave secreta para o aplicativo
    app.config["TESTING"] = True  # Define o modo de teste para True
    app.register_blueprint(
        auth_bp
    )  # Registra o blueprint para autenticação no aplicativo

    # Rota protegida que requer autenticação
    @app.route("/protected")
    @verificar_autenticacao  # Aplica a função de verificação de autenticação
    def protected():
        return "Protected"

    return app  # Retorna o aplicativo configurado para os testes


# Fixture para obter um cliente de teste para interagir com o aplicativo Flask durante os testes
@pytest.fixture
def client(app):
    return app.test_client()


# Teste para verificar se o usuário não autenticado é redirecionado para a página de login
def test_verificar_autenticacao_usuario_nao_autenticado(client):
    with client.session_transaction() as sess:
        sess.clear()  # Limpa a sessão para garantir que o usuário não esteja autenticado
    response = client.get(
        "/protected", follow_redirects=False
    )  # Faz uma solicitação GET para a rota protegida

    assert (
        response.status_code == 302
    )  # Verifica se o código de status é 302 (redirecionamento)
    location = response.headers[
        "Location"
    ]  # Obtém o cabeçalho de localização do redirecionamento
    assert location.endswith(
        "/login"
    )  # Verifica se o redirecionamento é para a página de login


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
