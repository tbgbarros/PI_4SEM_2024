import pytest  # Importa o módulo pytest para executar os testes
from flask import Flask  # Importa a classe Flask do módulo flask
from flask import url_for  # Importa a função url_for do módulo flask
from app import (
    create_app,
    db,
)  # Importa a função create_app e o objeto db do módulo app
from app.models.user import User  # Importa a classe User do módulo app.models.user


# Fixture para configurar e executar o aplicativo Flask para os testes
@pytest.fixture(scope="module")
def rodando_app():
    app = create_app()  # Cria uma instância do aplicativo Flask
    app.config["TESTING"] = True  # Ativa o modo de teste do aplicativo Flask
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://root:@localhost/mamaco_test"  # Configura a URI do banco de dados para os testes
    )
    with app.app_context():
        db.create_all()  # Cria todas as tabelas no banco de dados de teste
        yield app  # Retorna a instância do aplicativo para os testes
        db.drop_all()  # Remove todas as tabelas do banco de dados de teste


# Fixture para obter um cliente de teste para interagir com o aplicativo Flask durante os testes
@pytest.fixture(scope="module")
def client(rodando_app):
    return (
        rodando_app.test_client()
    )  # Retorna um cliente de teste para interagir com o aplicativo durante os testes


# Fixture para inicializar o banco de dados antes dos testes e limpar após os testes
@pytest.fixture(scope="module")
def init_database(rodando_app):
    with rodando_app.app_context():
        db.create_all()  # Cria todas as tabelas no banco de dados de teste
        yield db  # Retorna o banco de dados para os testes
        db.session.remove()  # Remove a sessão do banco de dados após os testes
        db.drop_all()  # Remove todas as tabelas do banco de dados de teste


# Teste para verificar se a página de criação de usuário é carregada corretamente
def teste_criar_usuario(client):
    with client:
        response = client.get(
            "/auth/signup"
        )  # Faz uma solicitação GET para a página de criação de usuário
        assert (
            response.status_code == 200
        )  # Verifica se a resposta é bem-sucedida (código 200)
        assert (
            b"Criar conta!" in response.data
        )  # Verifica se o texto esperado está presente na resposta


# Teste para verificar se um usuário é criado com sucesso
def teste_usuario_criado_sucesso(client, init_database):
    with client:
        response = client.post(
            "/auth/signup",  # Faz uma solicitação POST para criar um novo usuário
            data={
                "username": "newuser",
                "password": "Password123",
                "confirm_password": "Password123",
            },
            follow_redirects=True,  # Habilita redirecionamento após a solicitação
        )
        assert (
            response.status_code == 200
        )  # Verifica se a resposta é bem-sucedida (código 200)


# Teste para verificar se a criação de usuário falha devido à senha incorreta
def teste_criacao_usuario_falhou(client, init_database):
    with client:
        response = client.post(
            "/auth/signup",  # Faz uma solicitação POST para criar um novo usuário
            data={
                "username": "newuser",
                "password": "Password123",
                "confirm_password": "WrongPassword",  # Define uma senha incorreta
            },
            follow_redirects=True,  # Habilita redirecionamento após a solicitação
        )
        assert (
            response.status_code == 200
        )  # Verifica se a resposta é bem-sucedida (código 200)
