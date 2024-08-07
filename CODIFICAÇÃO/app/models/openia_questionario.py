import os  # Importa o módulo os para interagir com o sistema operacional
import openai  # Importa a biblioteca openai para usar a API do OpenAI
import re  # Importa o módulo re para operações de expressões regulares
from app.models.user import User  # Importa o modelo User


class OpeniaQuestionario:
    def __init__(self, api_key):
        # Inicializa a classe com a chave de API e cria um cache para perguntas geradas
        openai.api_key = api_key
        self.gerar_perguntas_cache = {}

    def gerar_perguntas(self, tema):
        # Prepara as mensagens para enviar ao modelo OpenAI
        messages = [
            {
                "role": "system",
                "content": f"Você será um assistente que ira gerar  questões  cada uma com 4 alternativas, a,b,c e d, dependendo do {tema} . gerando sozinho apenas com o tema escolhido nada mais",
            },
            {"role": "user", "content": f"o {tema} escolhido , gere 5 perguntas"},
        ]
        perguntas_cache = {}
        if tema in perguntas_cache:
            # Retorna perguntas do cache se já foram geradas anteriormente
            return perguntas_cache[tema]
        else:
            while True:
                # Gera perguntas usando o modelo OpenAI
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=400,
                )
                # Extrai as perguntas do texto de resposta
                perguntas_text = response.choices[0].message.content

                # Remove os "** **" do texto
                perguntas_text = perguntas_text.replace("**", "")

                # Separa as perguntas em uma lista
                perguntas_separadas = []
                perguntas = perguntas_text.split("\n\n")
                for pergunta in perguntas[1:-1]:  # Remove a primeira e a última tupla
                    partes = pergunta.split("\n")
                    if len(partes) < 5:
                        continue
                    texto_pergunta = partes[0]
                    opcoes_resposta = partes[1:5]
                    perguntas_separadas.append((texto_pergunta, opcoes_resposta))

                # Verifica se exatamente 5 perguntas foram geradas
                if len(perguntas_separadas) == 5:
                    self.gerar_perguntas_cache[tema] = perguntas_separadas
                    return perguntas_separadas

    def obter_respostas_chat(self, tema):
        # Obtém perguntas originais do cache
        perguntas_originais = self.gerar_perguntas_cache.get(tema)
        print(f"Perguntas originais dentro da obter chat: {perguntas_originais}")

        if not perguntas_originais:
            return None

        # Prepara as mensagens para enviar ao modelo OpenAI
        messages = [
            {
                "role": "system",
                "content": f"Você será um assistente que responderá o questionário de {tema}. Forneça a resposta correta para cada pergunta.",
            },
            {
                "role": "user",
                "content": "\n\n".join(
                    [
                        f"{pergunta[0]}\n{', '.join(pergunta[1])}"
                        for pergunta in perguntas_originais
                    ]
                ),
            },
        ]

        # Obtém respostas do modelo OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages, max_tokens=400
        )

        # Processa as respostas do chat
        respostas_chat = (
            response.choices[0].message.content.replace("\n", " ").split("\n\n")
        )
        print(f"Respostas do chat: {respostas_chat}")

        return respostas_chat

    def verificar_respostas(self, respostas_submetidas, respostas_corretas, username):
        resultados = []  # Lista para armazenar os resultados das verificações
        acertos = 0  # Contador de acertos

        print(f"Respostas submetidas: {respostas_submetidas}")
        print(f"Respostas corretas: {respostas_corretas}")

        string_respostas = respostas_corretas[0]

        # Divide as questões usando expressões regulares
        questoes = re.split(r"\d+\.\s", string_respostas)

        # Remove entradas vazias
        questoes = [q for q in questoes if q.strip()]

        # Lista para armazenar as respostas corretas divididas
        respostas_corretas_divididas = []

        # Itera sobre as questões encontradas e adiciona à lista
        for questao in questoes:
            if "Resposta:" in questao:
                # Divide pela palavra "Resposta:" para pegar a parte correta
                partes = questao.split("Resposta:")
                pergunta = partes[0].strip()
                resposta = partes[1].strip()
            else:
                # Caso normal
                if " " in questao:
                    alternativa = questao.split(" ", 1)[0].strip()
                    resposta = questao.split(" ", 1)[1].strip()
                    resposta = f"{alternativa} {resposta}"

            respostas_corretas_divididas.append(resposta)

        print(f"Respostas corretas divididas: {respostas_corretas_divididas}")

        # Itera sobre as questões encontradas e adiciona à lista
        for resposta_correta, (pergunta_submetida, resposta_submetida) in zip(
            respostas_corretas_divididas, respostas_submetidas.items()
        ):
            print(f"Resposta correta: {resposta_correta}")
            print(f"Pergunta submetida: {pergunta_submetida}")
            print(f"Resposta submetida: {resposta_submetida}")

            # Extrai apenas o conteúdo da resposta correta e da resposta submetida
            try:
                # Remove pontuação das respostas para comparar corretamente
                resposta_correta_contenido = re.sub(
                    r"[^\w\s]",
                    "",
                    resposta_correta[resposta_correta.index(")") + 2 :].strip(),
                )
                resposta_submetida_contenido = re.sub(
                    r"[^\w\s]",
                    "",
                    resposta_submetida[resposta_submetida.index(")") + 2 :].strip(),
                )

                # Verifica se a resposta submetida é correta
                acertou = (
                    resposta_submetida_contenido.lower()
                    == resposta_correta_contenido.lower()
                )
            except ValueError as e:
                # Caso ocorra um erro na extração, marca como incorreta
                print(f"Erro ao extrair a resposta: {e}")
                acertou = False

            resultados.append(
                (pergunta_submetida, resposta_submetida, resposta_correta, acertou)
            )

            if acertou:
                acertos += 1

        print(f"Resultados: {resultados}")
        print(f"Acertos: {acertos}")

        # Busca o usuário pelo nome de usuário
        user = User.query.filter_by(username=username).first()

        # Calcula a pontuação total baseada nos acertos
        pontos = acertos

        # Atualiza os pontos do usuário no banco de dados
        user.atualizar_pontos(pontos)

        return resultados, acertos
