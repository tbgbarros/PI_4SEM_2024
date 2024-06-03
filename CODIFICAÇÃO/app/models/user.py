import binascii  # Importa o módulo binascii para manipulação de dados binários
from app import db  # Importa a instância do banco de dados do Flask
from cryptography.fernet import Fernet  # Importa Fernet para criptografia simétrica
import base64  # Importa base64 para codificação e decodificação de dados
from app.utils.utils_user import (
    get_emblema_url,
)  # Importa uma função utilitária para obter a URL do emblema do usuário


# Define a classe User que representa a tabela 'user' no banco de dados
class User(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )  # Coluna 'id' é a chave primária
    username = db.Column(
        db.String(64), nullable=False, index=True, unique=True
    )  # Coluna 'username' deve ser única e indexada
    password_encrypted = db.Column(
        db.LargeBinary, nullable=False
    )  # Coluna 'password_encrypted' para armazenar a senha criptografada
    hash = db.Column(
        db.String(64), nullable=False
    )  # Coluna 'hash' para armazenar a chave criptografada em formato base64
    pontos = db.Column(
        db.Integer, default=0
    )  # Coluna 'pontos' para armazenar os pontos do usuário, com valor padrão 0

    def __init__(self, username):
        self.username = (
            username  # Inicializa a instância do usuário com o nome de usuário
        )

    @classmethod
    def create(cls, username, password):
        # Método de classe para criar um novo usuário com nome de usuário e senha
        user = cls(username=username)
        user.set_password(password)  # Define a senha criptografada
        return user

    def set_password(self, password):
        # Método para definir a senha criptografada
        key = Fernet.generate_key()  # Gera uma nova chave de criptografia
        cipher_suite = Fernet(key)  # Cria um objeto Fernet com a chave gerada
        self.password_encrypted = cipher_suite.encrypt(
            password.encode()
        )  # Criptografa a senha e armazena
        self.hash = base64.urlsafe_b64encode(
            key
        ).decode()  # Codifica a chave em base64 e armazena

    def check_password(self, password):
        # Método para verificar se a senha fornecida corresponde à senha criptografada
        try:
            key_bytes = base64.urlsafe_b64decode(
                self.hash.encode()
            )  # Decodifica a chave de base64 para bytes
            cipher_suite = Fernet(
                key_bytes
            )  # Cria um objeto Fernet com a chave decodificada
            decrypted_password = cipher_suite.decrypt(
                self.password_encrypted
            ).decode()  # Descriptografa a senha armazenada
            return (
                password == decrypted_password
            )  # Compara a senha fornecida com a senha armazenada
        except (binascii.Error, ValueError):
            return False  # Retorna False se houver erro na descriptografia

    def atualizar_pontos(self, pontos):
        # Método para atualizar os pontos do usuário
        self.pontos += (
            pontos  # Adiciona os pontos fornecidos aos pontos atuais do usuário
        )
        db.session.commit()  # Salva a alteração no banco de dados

    def emblema(self):
        # Método para obter a URL do emblema do usuário com base nos pontos
        return get_emblema_url(self.pontos)  # Retorna a URL do emblema
