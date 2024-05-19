from flask import render_template, request, session
from flask import Blueprint, redirect, url_for, flash
from app.models.openia_questionario import OpeniaQuestionario

openia_questionario = OpeniaQuestionario(api_key="")

bp = Blueprint("quest", __name__, url_prefix="/quest")

@bp.route("/gerar", methods=["POST"])
def gerar_questionario():
    tema = request.form["tema"]
    perguntas = openia_questionario.gerar_perguntas(tema)
    print(f"Perguntas geradas: {perguntas}")

    respostas = openia_questionario.obter_respostas_chat(tema)
    print(f"Respostas do chat na rota gerar_questionario: {respostas}")

    session['respostas'] = respostas
    return render_template("quest/gerar.html", perguntas=perguntas)



@bp.route("/processar", methods=["POST"])
def processar_respostas():
    respostas_submetidas = request.form
    respostas_corretas = session.get('respostas')

    print(f"Respostas submetidas dentro do processar_respostas: {respostas_submetidas}")
    print(f"Respostas corretas fornecidas pela API dentro do processar respostas: {respostas_corretas}")

    if respostas_corretas:
        resultados, acertos = openia_questionario.verificar_respostas(respostas_submetidas, respostas_corretas)
        print(f"Resultados: {resultados}, Acertos: {acertos}")
    else:
        resultados = None
        acertos = 0

    return render_template("quest/processar.html", resultados=resultados, acertos=acertos)

