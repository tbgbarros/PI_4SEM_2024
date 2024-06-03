# Importações necessárias para os testes
import pytest  # Importa o módulo pytest para executar os testes
from flask import (
    url_for,
    session,
)  # Importa a função url_for e o objeto session do módulo flask
from app import (
    create_app,
    db,
)  # Importa a função create_app e o objeto db do módulo app
from app.models.user import User  # Importa a classe User do módulo app.models.user
from app.forms import (
    SignupForm,
    LoginForm,
)  # Importa as classes SignupForm e LoginForm do módulo app.forms


# Fixture para configurar o ambiente de teste
@pytest.fixture(scope="module")
def test_app():
    app = create_app()  # Cria uma instância do aplicativo Flask para os testes
    app.config["TESTING"] = True  # Define o modo de teste para True
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://root:@localhost/mamaco_test"  # Define a URI do banco de dados de teste
    )
    with app.app_context():
        db.create_all()  # Cria todas as tabelas no banco de dados
        yield app  # Retorna o aplicativo configurado para os testes


# Fixture para obter um cliente de teste para interagir com o aplicativo Flask durante os testes
@pytest.fixture(scope="module")
def client(test_app):
    return (
        test_app.test_client()
    )  # Retorna um cliente de teste para interagir com o aplicativo Flask


# Teste para verificar o cadastro de um novo usuário com dados válidos
def test_signup(client, test_app):
    response = client.post(
        "/auth/signup",
        data={
            "username": "testuser",
            "password": "Password123",
            "confirm_password": "Password123",
        },
        follow_redirects=True,  # Seguir redirecionamento após o cadastro
    )
    assert response.status_code == 200  # Verifica se o cadastro foi bem-sucedido


# Teste para verificar o login de um usuário com dados válidos
def test_login(client, test_app):
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "Password123"},
        follow_redirects=True,  # Seguir redirecionamento após o login
    )
    assert response.status_code == 200  # Verifica se o login foi bem-sucedido


# Teste para verificar o logout de um usuário
def test_logout(client):
    # Realiza o login para poder testar o logout
    client.post(
        "/auth/login",
        data={"username": "testuser", "password": "Password123"},
        follow_redirects=True,
    )

    # Testa o logout
    response = client.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200  # Verifica se o logout foi bem-sucedido

    # Verifica se a sessão do usuário foi limpa após o logout
    with client.session_transaction() as session:
        assert (
            "username" not in session
        )  # Verifica se o nome de usuário não está mais na sessão
