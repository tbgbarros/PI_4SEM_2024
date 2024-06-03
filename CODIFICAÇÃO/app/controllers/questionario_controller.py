import os  # Importa o módulo os para interagir com o sistema operacional
from flask import (
    render_template,
    request,
    session,
    Blueprint,
    redirect,
    url_for,
    flash,
)  # Importa funções e classes do Flask
from dotenv import (
    load_dotenv,
)  # Importa a função load_dotenv para carregar variáveis de ambiente de um arquivo .env
from app.models.openia_questionario import (
    OpeniaQuestionario,
)  # Importa a classe OpeniaQuestionario do módulo models

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave de API da variável de ambiente
api_key = os.getenv("CHATGPT_API_KEY")

# Cria uma instância da classe OpeniaQuestionario com a chave de API
openia_questionario = OpeniaQuestionario(api_key=api_key)

# Cria um Blueprint para o módulo de questionários com um prefixo de URL
bp = Blueprint("quest", __name__, url_prefix="/quest")


# Define uma rota para gerar questionários, que aceita apenas o método POST
@bp.route("/gerar", methods=["POST"])
def gerar_questionario():
    # Obtém o tema do formulário enviado pelo cliente
    tema = request.form["tema"]
    # Gera perguntas baseadas no tema usando a instância de OpeniaQuestionario
    perguntas = openia_questionario.gerar_perguntas(tema)
    print(f"Perguntas geradas: {perguntas}")

    # Obtém as respostas do chat com base no tema
    respostas = openia_questionario.obter_respostas_chat(tema)
    print(f"Respostas do chat na rota gerar_questionario: {respostas}")

    # Armazena as respostas na sessão do usuário
    session["respostas"] = respostas
    # Renderiza o template com as perguntas geradas
    return render_template("quest/gerar.html", perguntas=perguntas)


# Define uma rota para processar respostas, que aceita apenas o método POST
@bp.route("/processar", methods=["POST"])
def processar_respostas():
    # Obtém as respostas submetidas pelo formulário
    respostas_submetidas = request.form
    # Obtém as respostas corretas armazenadas na sessão
    respostas_corretas = session.get("respostas")
    # Obtém o nome de usuário armazenado na sessão
    username = session.get("username")

    print(f"Respostas submetidas dentro do processar_respostas: {respostas_submetidas}")
    print(
        f"Respostas corretas fornecidas pela API dentro do processar respostas: {respostas_corretas}"
    )

    if respostas_corretas:
        # Verifica as respostas submetidas com as respostas corretas
        resultados, acertos = openia_questionario.verificar_respostas(
            respostas_submetidas, respostas_corretas, username
        )
        print(f"Resultados: {resultados}, Acertos: {acertos}")
    else:
        resultados = None
        acertos = 0

    # Renderiza o template com os resultados e o número de acertos
    return render_template(
        "quest/processar.html", resultados=resultados, acertos=acertos
    )
