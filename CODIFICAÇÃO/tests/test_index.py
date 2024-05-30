# tests/test_index.py
import pytest
import unittest
from flask import Flask, render_template_string, url_for, session
from flask.blueprints import Blueprint
from flask_testing import TestCase
from app import create_app, db
from app.models import user
from app.forms import SignupForm

from unittest.mock import patch, MagicMock
from app.controllers.auth_controller import logout


# testes html
def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b'class="logoHome"' in response.data


def test_navbar_in_html_template(app):
    with app.app_context():
        rendered_html = render_template_string(
            """
            <!DOCTYPE html>
            <html lang="pt-br">
            <head>
            </head>
            <body>
                <nav class="navbar navbar-inverse">
                    <div class="container-fluid">
                        <div class="navbar-nav logotipo">
                            <a class="navbar-brand" href="#">Hackers School</a>
                        </div>
                    </div>
                </nav>
            </body>
            </html>
            """
        )
        assert "Hackers School" in rendered_html


# testes app/controllers auth
def test_auth_blueprint_url_prefix():
    bp = Blueprint("auth", __name__, url_prefix="/auth")
    assert bp.url_prefix == "/auth"


# test logout
class TestAuthController(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key = "test_secret_key"
        self.client = self.app.test_client()

    @patch("app.controllers.auth_controller.redirect")
    @patch("app.controllers.auth_controller.url_for")
    def test_logout(self, mock_url_for, mock_redirect):
        with self.app.test_request_context():
            # Simula a existência de um usuário na sessão
            session["username"] = "test_user"

            # Configuração do mock
            mock_url_for.return_value = "/"

            # Chamada da função de logout
            response = logout()

            # Verificações
            self.assertEqual(
                session.get("username"), None
            )  # Verifica se o usuário foi removido da sessão
            mock_redirect.assert_called_once_with("main.index")
            self.assertEqual(
                response.status_code, 302
            )  # Verifica se houve redirecionamento
