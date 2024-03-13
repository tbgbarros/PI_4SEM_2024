# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config  # Importe a classe Config do arquivo config.py

app = Flask(__name__)
app.config.from_object(Config)  # Carregue as configurações do objeto Config

db = SQLAlchemy(app)

# Importe seus blueprints aqui
from app.controllers.user_controller import user_blueprint

# Registre os blueprints
app.register_blueprint(user_blueprint, url_prefix='/user')
