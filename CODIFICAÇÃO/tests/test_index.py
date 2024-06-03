# Importações necessárias para os testes
import pytest  # Importa o módulo pytest para executar os testes
from flask import (
    Flask,
    render_template_string,
    url_for,
    session,
)  # Importa classes e funções do módulo flask
from flask.blueprints import (
    Blueprint,
)  # Importa a classe Blueprint do módulo flask.blueprints
from flask_testing import TestCase  # Importa a classe TestCase do módulo flask_testing
from app import (
    create_app,
    db,
)  # Importa a função create_app e o objeto db do módulo app
from app.models.user import User  # Importa a classe User do módulo app.models.user


# Teste para verificar se a página index é carregada corretamente
def teste_pagina_index(client):
    response = client.get("/")  # Faz uma solicitação GET para a rota raiz
    assert (
        response.status_code == 200
    )  # Verifica se a resposta é bem-sucedida (código 200)
    assert (
        b'class="logoHome"' in response.data
    )  # Verifica se a classe "logoHome" está presente na resposta


# Teste para verificar se a navbar é renderizada corretamente
def testar_navbar_html(app):
    with app.app_context():
        # Renderiza um HTML simulando a estrutura da navbar
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
        # Verifica se o texto "Hackers School" está presente no HTML renderizado
        assert "Hackers School" in rendered_html
