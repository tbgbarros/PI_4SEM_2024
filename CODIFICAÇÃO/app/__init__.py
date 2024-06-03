import os  # Importa o módulo os para lidar com funcionalidades do sistema operacional
from sqlalchemy import (
    inspect,
)  # Importa o objeto 'inspect' do módulo sqlalchemy para inspecionar objetos SQLAlchemy
import bcrypt  # Importa o módulo bcrypt para realizar hash de senhas
from flask import Flask  # Importa a classe Flask do pacote flask
from flask_sqlalchemy import SQLAlchemy  # Importa a extensão SQLAlchemy para Flask
from flask_migrate import Migrate  # Importa a extensão Migrate para Flask
from config import Config  # Importa a classe Config do arquivo config.py
from flask_bcrypt import Bcrypt  # Importa a extensão Bcrypt para Flask
from sqlalchemy_utils import (
    database_exists,
    create_database,
)  # Importa funções auxiliares do SQLAlchemy
import logging  # Importa o módulo logging para lidar com logs

db = (
    SQLAlchemy()
)  # Cria uma instância da classe SQLAlchemy para interagir com o banco de dados
bcrypt = (
    Bcrypt()
)  # Cria uma instância da classe Bcrypt para lidar com hashing de senhas
migrate = (
    Migrate()
)  # Cria uma instância da classe Migrate para lidar com migrações de banco de dados


def create_app():
    app = Flask(__name__)  # Cria uma instância do aplicativo Flask
    app.config.from_object(Config)  # Carrega as configurações do objeto Config
    app.config["SECRET_KEY"] = "pedro"  # Define uma chave secreta para o aplicativo

    # Usa DATABASE_URL da variável de ambiente ou pega da configuração
    db_uri = os.getenv("DATABASE_URL", app.config["SQLALCHEMY_DATABASE_URI"])
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri  # Define a URI do banco de dados

    if not database_exists(db_uri):
        create_database(db_uri)  # Cria o banco de dados se não existir

    db.init_app(app)  # Inicializa o SQLAlchemy com o aplicativo
    bcrypt.init_app(app)  # Inicializa o Bcrypt com o aplicativo
    migrate.init_app(app, db)  # Inicializa o Migrate com o aplicativo e o SQLAlchemy

    with app.app_context():
        from .models.user import User  # Importa a classe User do módulo models.user

        db.create_all()  # Cria todas as tabelas definidas nos modelos

    # Importa os controladores e registra os blueprints no aplicativo
    from app.controllers import (
        auth_controller,
        main_controller,
        questionario_controller,
    )

    app.register_blueprint(auth_controller.bp)
    app.register_blueprint(main_controller.bp)
    app.register_blueprint(questionario_controller.bp)

    return app  # Retorna o aplicativo Flask


def init_db(app):
    with app.app_context():
        from .models.user import User  # Importa a classe User do módulo models.user

        db.create_all()  # Cria todas as tabelas definidas nos modelos


# Fora do create_app(), chame init_db() se o script for executado diretamente
if __name__ == "__main__":
    app = create_app()
    init_db(app)  # Inicializa o banco de dados
