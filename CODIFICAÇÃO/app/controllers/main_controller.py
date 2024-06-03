from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.forms import (
    SignupForm,
    LoginForm,
)  # Importa os formulários de cadastro e login
from functools import (
    wraps,
)  # Importa wraps para decorar funções mantendo a metadata original

# Cria um Blueprint para o módulo principal com um template específico
bp = Blueprint("main", __name__, template_folder="templates/main")


# Função decoradora para verificar autenticação do usuário
def verificar_autenticacao(f):
    @wraps(f)  # Preserva a metadata da função original
    def decorated_function(*args, **kwargs):
        # Verifica se o usuário está logado
        if "username" not in session or session.get("username") is None:
            flash(
                "Você precisa fazer login para acessar esta página.", "warning"
            )  # Exibe mensagem de aviso
            return redirect(
                url_for("auth.login")
            )  # Redireciona para a página de login se não estiver logado
        return f(
            *args, **kwargs
        )  # Executa a função original se o usuário estiver logado

    return decorated_function


# Define a rota para a página inicial
@bp.route("/")
def index():
    return render_template("index.html")  # Renderiza o template da página inicial


# Define a rota para a página principal, protegida por autenticação
@bp.route("/principal")
@verificar_autenticacao  # Aplica a função decoradora para verificar autenticação
def principal():
    return render_template(
        "main/principal.html"
    )  # Renderiza o template da página principal


# Define a rota para a página do usuário, protegida por autenticação
@bp.route("/usuario")
@verificar_autenticacao  # Aplica a função decoradora para verificar autenticação
def usuario():
    return render_template(
        "main/usuario.html"
    )  # Renderiza o template da página do usuário


# Define a rota para a página de ranking, protegida por autenticação
@bp.route("/rank")
@verificar_autenticacao  # Aplica a função decoradora para verificar autenticação
def rank():
    return render_template(
        "main/rank.html"
    )  # Renderiza o template da página de ranking
