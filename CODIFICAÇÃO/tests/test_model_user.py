# Importações necessárias para os testes
import pytest  # Importa o módulo pytest para executar os testes
from app import (
    create_app,
    db,
)  # Importa a função create_app e o objeto db do módulo app
from app.models.user import User  # Importa a classe User do módulo app.models.user


# Fixture para configurar o ambiente de teste
@pytest.fixture(scope="module")
def teste_rodando():
    # Cria uma instância do aplicativo Flask para os testes
    app = create_app()
    app.config["TESTING"] = True  # Define o modo de teste para True
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://root:@localhost/mamaco_test"  # Define a URI do banco de dados de teste
    )
    with app.app_context():
        db.create_all()  # Cria todas as tabelas no banco de dados
        yield app  # Retorna o aplicativo configurado para os testes
        db.drop_all()  # Remove todas as tabelas do banco de dados após os testes


# Fixture para obter um cliente de teste para interagir com o aplicativo Flask durante os testes
@pytest.fixture(scope="module")
def testar_cliente(teste_rodando):
    return teste_rodando.test_client()


# Fixture para inicializar o banco de dados
@pytest.fixture(scope="module")
def inicializarDatabase(teste_rodando):
    with teste_rodando.app_context():
        yield db  # Retorna o objeto do banco de dados para os testes
        db.session.remove()  # Remove a sessão do banco de dados após os testes


# Fixture para criar um novo usuário para os testes
@pytest.fixture(scope="function")
def novo_usuario():
    return User.create(username="testuser", password="Password123")


# Teste para verificar a criação de um novo usuário
def teste_usuario_criacao(teste_rodando, inicializarDatabase, novo_usuario):
    with teste_rodando.app_context():
        db.session.add(
            novo_usuario
        )  # Adiciona o novo usuário à sessão do banco de dados
        db.session.commit()  # Comita as alterações no banco de dados
        user = User.query.filter_by(
            username="testuser"
        ).first()  # Obtém o usuário recém-criado do banco de dados
        assert user is not None  # Verifica se o usuário foi criado com sucesso
        assert user.username == "testuser"  # Verifica se o nome de usuário é correto
        assert user.check_password(
            "Password123"
        )  # Verifica se a senha foi criptografada corretamente


# Teste para verificar a configuração da senha do novo usuário
def teste_setar_novo_usuario(novo_usuario):
    assert (
        novo_usuario.password_encrypted is not None
    )  # Verifica se a senha criptografada foi definida
    assert novo_usuario.hash is not None  # Verifica se o hash da senha foi definido


# Teste para verificar a função de verificação de senha do novo usuário
def teste_checar_senha(novo_usuario):
    assert (
        novo_usuario.check_password("Password123") is True
    )  # Verifica se a senha correta é aceita
    assert (
        novo_usuario.check_password("WrongPassword") is False
    )  # Verifica se uma senha incorreta é rejeitada
