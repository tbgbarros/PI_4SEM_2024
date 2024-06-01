import pytest
from app import create_app, db
from app.models.user import User


@pytest.fixture(scope="module")
def teste_rodando():
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
def testar_cliente(teste_rodando):
    return teste_rodando.test_client()


@pytest.fixture(scope="module")
def inicializarDatabase(teste_rodando):
    with teste_rodando.app_context():
        yield db
        db.session.remove()


@pytest.fixture(scope="function")
def novo_usuario():
    return User.create(username="testuser", password="Password123")


def teste_usuario_criacao(teste_rodando, inicializarDatabase, novo_usuario):
    with teste_rodando.app_context():
        db.session.add(novo_usuario)
        db.session.commit()
        user = User.query.filter_by(username="testuser").first()
        assert user is not None
        assert user.username == "testuser"
        assert user.check_password("Password123")


def teste_setar_novo_usuario(novo_usuario):
    assert novo_usuario.password_encrypted is not None
    assert novo_usuario.hash is not None


def teste_checar_senha(novo_usuario):
    assert novo_usuario.check_password("Password123") is True
    assert novo_usuario.check_password("WrongPassword") is False
