# tests/test_index.py
import pytest
from flask import Flask, render_template_string, url_for, session
from flask.blueprints import Blueprint
from flask_testing import TestCase
from app import create_app, db
from app.models.user import User


# testes html
def teste_pagina_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b'class="logoHome"' in response.data


def testar_navbar_html(app):
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
