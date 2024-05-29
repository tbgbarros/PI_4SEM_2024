# tests/test_index.py
import pytest
from flask import Flask, render_template_string, url_for
from flask.blueprints import Blueprint
from flask_testing import TestCase
from app import create_app, db
from app.models import User
from app.forms import SignupForm


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


def test_css_link_in_html_template(app):
    with app.app_context():
        rendered_html = render_template_string(
            """
            <!DOCTYPE html>
            <html lang="pt-br">
            <head>
                <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/main.css') }}">
            </head>
            <body>
            </body>
            </html>
            """
        )
        assert (
            '<link rel="stylesheet" type="text/css" href="/static/css/main.css">'
            in rendered_html
        )


def test_js_link_in_html_template(app):
    with app.app_context():
        rendered_html = render_template_string(
            """
            <!DOCTYPE html>
            <html lang="pt-br">
            <head>
                <script src="{{ url_for('static', filename='js/main.js') }}"></script>
            </head>
            <body>
            </body>
            </html>
            """
        )
        assert '<script src="/static/js/main.js"></script>' in rendered_html


# testes app/controllers auth
def test_auth_blueprint_url_prefix():
    bp = Blueprint("auth", __name__, url_prefix="/auth")
    assert bp.url_prefix == "/auth"


class TestAuthBlueprint(TestCase):
    def create_app(self):
        app = create_app()
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False  # Desative CSRF para os testes
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # banco em memoria
        return app

    def setUp(self):
        # tabelas banco
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_signup_route_get(self):
        response = self.client.get(url_for("auth.signup"))
        self.assert200(
            response
        )  # Verifique se a rota retorna um código de status 200 OK
        self.assertTemplateUsed(
            "auth/signup.html"
        )  # Verifique se o template correto está sendo renderizado

    def test_signup_route_post(self):
        # Simule um POST request com dados de formulário válidos
        with self.client:
            response = self.client.post(
                url_for("auth.signup"),
                data=dict(username="testuser", password="testpassword"),
                follow_redirects=True,
            )
            self.assertIn(
                "Cadastrado, agora voce pode entrar para o Clã!".encode("utf-8"),
                response.data,
            )
            user = db.session.query(User).filter_by(username="testuser").first()
            self.assertIsNotNone(
                user
            )  # Verifique se o usuário foi adicionado ao banco de dados


if __name__ == "__main__":
    pytest.main()
