# import os
# import app


# class Config:
#     SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key"
#     SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/flask"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     STATIC_URL = "/static/"
#     STATICFILES_DIRS = [os.path.join(os.path.dirname("app/templates/static"))]

import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "mysql+pymysql://root:mamaco@localhost/mamaco"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_URL = "/static/"
    STATICFILES_DIRS = [os.path.abspath("app/static")]


class ProductionConfig(Config):
    # Configurações para ambiente de produção no GitHub
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


# Seleciona a configuração apropriada com base no ambiente
if os.environ.get("ENV") == "production":
    current_config = ProductionConfig
else:
    current_config = Config
