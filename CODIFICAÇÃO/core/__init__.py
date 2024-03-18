from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from core.models import creat_db

app = Flask(__name__)


app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flask_example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'echo': True, 'pool_pre_ping': True}  # Adicionando opções do SQLAlchemy
db = creat_db(app)

