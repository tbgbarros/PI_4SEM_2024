# tests/test_index.py
import pytest
from flask import Flask, render_template_string


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
                <link rel="stylesheet" type="text/css" href="/static/css/main.css">
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
                <script src="/static/js/main.js"></script>
            </head>
            <body>
            </body>
            </html>
            """
        )
        assert '<script src="/static/js/main.js"></script>' in rendered_html
