# tests/test_index.py
import pytest
from flask import Flask, render_template_string, url_for
from flask.blueprints import Blueprint
from flask_testing import TestCase
from app import create_app, db
from app.models import user
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


# testes app/controllers auth
def test_auth_blueprint_url_prefix():
    bp = Blueprint("auth", __name__, url_prefix="/auth")
    assert bp.url_prefix == "/auth"
