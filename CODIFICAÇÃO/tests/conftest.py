import sys
import os
import pytest
from app import create_app, db

# Adicione o diretório do seu projeto ao path do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Configuração para o banco de dados em memória virtual temporário
class TestConfig:
    TESTING = True
    os.environ["DATABASE_URL"] = "mysql+pymysql://root:@localhost/mamaco_test"
    os.environ["SECRET_KEY"] = "test_secret_key"


# Fixture para criar uma instância do aplicativo Flask para os testes
@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(TestConfig)
    with app.app_context():
        db.create_all()
        yield app


# Fixture para obter um cliente de teste para interagir com o aplicativo Flask durante os testes
@pytest.fixture
def client(app):
    return app.test_client()
