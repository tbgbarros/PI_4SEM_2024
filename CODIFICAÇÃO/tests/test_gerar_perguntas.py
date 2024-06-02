# import pytest
# from unittest.mock import Mock, patch
# from app.models.openia_questionario import OpeniaQuestionario
# from dotenv import load_dotenv
# import os

# load_dotenv()

# # api gpt
# api_key = os.getenv("CHATGPT_API_KEY")

# # mock
# mock_response = Mock()
# mock_response.choices = [Mock()]
# mock_response.choices[
#     0
# ].message.content = """
# Pergunta 1
# a) Resposta 1a
# b) Resposta 1b
# c) Resposta 1c
# d) Resposta 1d

# Pergunta 2
# a) Resposta 2a
# b) Resposta 2b
# c) Resposta 2c
# d) Resposta 2d

# Pergunta 3
# a) Resposta 3a
# b) Resposta 3b
# c) Resposta 3c
# d) Resposta 3d

# Pergunta 4
# a) Resposta 4a
# b) Resposta 4b
# c) Resposta 4c
# d) Resposta 4d

# Pergunta 5
# a) Resposta 5a
# b) Resposta 5b
# c) Resposta 5c
# d) Resposta 5d
# """


# @patch("app.models.openia_questionario.openai.ChatCompletion.create")
# def test_gerar_perguntas_retorna_5_perguntas(mock_create):
#     mock_create.return_value = mock_response

#     obj = OpeniaQuestionario(api_key)
#     tema = "ciência"
#     perguntas = obj.gerar_perguntas(tema)

#     assert len(perguntas) == 5


# @patch("app.models.openia_questionario.openai.ChatCompletion.create")
# def test_estrutura_das_perguntas(mock_create):
#     mock_create.return_value = mock_response

#     obj = OpeniaQuestionario(api_key)
#     tema = "ciência"
#     perguntas = obj.gerar_perguntas(tema)

#     for pergunta in perguntas:
#         assert len(pergunta) == 2
#         texto_pergunta, opcoes_resposta = pergunta
#         assert texto_pergunta.startswith("Pergunta")


# @patch("app.models.openia_questionario.openai.ChatCompletion.create")
# def test_numero_de_opcoes_de_resposta(mock_create):
#     mock_create.return_value = mock_response

#     obj = OpeniaQuestionario(api_key)
#     tema = "ciência"
#     perguntas = obj.gerar_perguntas(tema)

#     for pergunta in perguntas:
#         texto_pergunta, opcoes_resposta = pergunta
#         assert len(opcoes_resposta) == 4


# @patch("app.models.openia_questionario.openai.ChatCompletion.create")
# def test_formatacao_das_opcoes_de_resposta(mock_create):
#     mock_create.return_value = mock_response

#     obj = OpeniaQuestionario(api_key)
#     tema = "ciência"
#     perguntas = obj.gerar_perguntas(tema)

#     for pergunta in perguntas:
#         texto_pergunta, opcoes_resposta = pergunta
#         for opcao in opcoes_resposta:
#             assert (
#                 opcao.startswith("a)")
#                 or opcao.startswith("b)")
#                 or opcao.startswith("c)")
#                 or opcao.startswith("d)")
#             )
