import sys  # Importa o módulo sys para manipulação de caminhos do sistema
import os  # Importa o módulo os para interação com o sistema operacional
import pytest  # Importa o módulo pytest para executar os testes
from app import (
    create_app,
    db,
)  # Importa a função create_app e o objeto db do módulo app

# Adicione o diretório do seu projeto ao path do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Configuração para o banco de dados em memória virtual temporário
class TestConfig:
    TESTING = True  # Ativa o modo de teste do aplicativo Flask
    os.environ["DATABASE_URL"] = (
        "mysql+pymysql://root:@localhost/mamaco_test"  # Configura a URL do banco de dados para os testes
    )
    os.environ["SECRET_KEY"] = (
        "test_secret_key"  # Configura a chave secreta para os testes
    )


# Fixture para criar uma instância do aplicativo Flask para os testes
@pytest.fixture
def app():
    app = create_app()  # Cria uma instância do aplicativo Flask
    app.config.from_object(
        TestConfig
    )  # Carrega as configurações de teste para o aplicativo
    with app.app_context():
        db.create_all()  # Cria todas as tabelas no banco de dados de teste
        yield app  # Retorna a instância do aplicativo para os testes


# Fixture para obter um cliente de teste para interagir com o aplicativo Flask durante os testes
@pytest.fixture
def client(app):
    return (
        app.test_client()
    )  # Retorna um cliente de teste para interagir com o aplicativo durante os testes
