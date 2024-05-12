from flask import render_template, request
from flask import Blueprint, redirect, url_for, flash
from app.models.openia_questionario import OpeniaQuestionario

openia_questionario = OpeniaQuestionario(api_key="")


bp = Blueprint("quest", __name__, url_prefix="/quest")


@bp.route("/gerar", methods=["POST"])
def gerar_questionario():
    tema = request.form["tema"]
    perguntas = openia_questionario.gerar_perguntas(tema)
    return render_template("quest/gerar.html", perguntas=perguntas)


@bp.route("/processar", methods=["POST"])
def processar_respostas():
    resposta = request.form
    respostas = openia_questionario.verificar_respostas(resposta)
    print(respostas)
    return render_template("quest/processar.html", respostas=respostas)
