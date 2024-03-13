# run.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from app.controllers.user_controller import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')

if __name__ == "__main__":
    app.run(debug=True)
