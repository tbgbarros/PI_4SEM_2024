from flask import (
    Blueprint,  # Blueprint é usado para organizar um grupo de rotas e outros elementos relacionados
    render_template,  # render_template renderiza um template HTML
    redirect,  # redirect redireciona o usuário para uma rota diferente
    url_for,  # url_for gera URLs para as rotas
    flash,  # flash exibe mensagens temporárias ao usuário
    session,  # session armazena dados entre solicitações do usuário
    current_app,  # current_app fornece acesso ao contexto da aplicação
)
from app.forms import (
    SignupForm,
    LoginForm,
)  # Importa os formulários de cadastro e login
from app.models.user import User  # Importa o modelo de usuário
from app import db  # Importa a instância do banco de dados
from app.utils.utils_user import (
    get_emblema_url,
)  # Importa a função para obter a URL do emblema

# Cria um Blueprint para o módulo de autenticação com prefixo de URL '/auth'
bp = Blueprint("auth", __name__, url_prefix="/auth")


# Define a rota para a página de cadastro, que aceita métodos GET e POST
@bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()  # Instancia o formulário de cadastro
    if form.validate_on_submit():  # Verifica se o formulário foi validado e enviado
        # Cria um novo usuário com os dados do formulário
        user = User.create(username=form.username.data, password=form.password.data)
        db.session.add(user)  # Adiciona o usuário ao banco de dados
        db.session.commit()  # Confirma a transação no banco de dados
        flash("Cadastro realizado com sucesso!", "success")  # Exibe mensagem de sucesso
        return redirect(url_for("auth.login"))  # Redireciona para a página de login
    return render_template(
        "auth/signup.html", form=form
    )  # Renderiza o template de cadastro com o formulário


# Define a rota para a página de login, que aceita métodos GET e POST
@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()  # Instancia o formulário de login
    if form.validate_on_submit():  # Verifica se o formulário foi validado e enviado
        # Consulta o usuário no banco de dados pelo nome de usuário
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(
            form.password.data
        ):  # Verifica se o usuário existe e se a senha está correta
            flash("Invalid username or password")  # Exibe mensagem de erro
            return render_template(
                "auth/login.html",
                title="Sign In",
                form=form,
                error="Invalid username or password",
            )

        # Obtém a URL do emblema do usuário com base nos pontos
        emblema_url = get_emblema_url(user.pontos)
        session["username"] = form.username.data  # Armazena o nome de usuário na sessão
        session["emblema_url"] = emblema_url  # Armazena a URL do emblema na sessão
        return redirect(
            url_for("main.principal")
        )  # Redireciona para a rota principal após o login
    return render_template(
        "auth/login.html", title="Sign In", form=form
    )  # Renderiza o template de login com o formulário


# Define a rota para logout
@bp.route("/logout")
def logout():
    session.pop("username", None)  # Remove o nome de usuário da sessão
    return redirect(
        url_for("main.index")
    )  # Redireciona para a rota principal após o logout
