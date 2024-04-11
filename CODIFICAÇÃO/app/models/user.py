import binascii
from flask_login import LoginManager
from flask_login import LoginManager, UserMixin
from app import db
from cryptography.fernet import Fernet
import base64

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_encrypted = db.Column(db.LargeBinary)
    hash = db.Column(db.String(44))  # Store the key as a base64 encoded string

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        self.password_encrypted = cipher_suite.encrypt(password.encode())
        self.hash = base64.urlsafe_b64encode(key).decode()  # Store the key as a base64 encoded string

    def check_password(self, password):
        try:
            key_bytes = base64.urlsafe_b64decode(self.hash.encode())
            cipher_suite = Fernet(key_bytes)
            decrypted_password = cipher_suite.decrypt(self.password_encrypted).decode()
            return password == decrypted_password
        except (binascii.Error, ValueError):
            # Tratar exceções relacionadas à decodificação de base64 ou chave inválida
            return False
        
    
   