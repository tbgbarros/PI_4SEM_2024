
from flask_sqlalchemy import SQLAlchemy

db = None

def creat_db(app=None):
    global db
    db = SQLAlchemy(app)

    return db