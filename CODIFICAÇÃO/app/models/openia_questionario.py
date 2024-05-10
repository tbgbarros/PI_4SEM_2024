import openai

class OpeniaQuestionario:
    def __init__(self, api_key):
        openai.api_key = api_key

    def gerar_perguntas(self, tema):
        messages = [
                    {"role": "system", "content": f"Voce será um assistente que ira gerar  questões  cada uma com 4 alternativas, a,b,c e d, dependendo do {tema} . gerando sozinho apenas com o tema escolhido nada mais"},
                    {"role": "user","content":f"o {tema} escolhido , gere 5 perguntas" }]
        perguntas_cache = {}
        if tema in perguntas_cache:
            return perguntas_cache[tema] 

        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages= messages,
                max_tokens=400, 
                 
            )
            # Extrair as perguntas do texto de resposta
        perguntas_text = response.choices[0].message.content

        # Separar as perguntas em uma lista
        perguntas_text = perguntas_text.split('\n\n', 1)[1]
        perguntas = perguntas_text.split("\n\n")
        perguntas.pop()

        perguntas_separadas = []
        for pergunta in perguntas:
            partes = pergunta.split('\n')
            texto_pergunta = partes[0]
            opcoes_resposta = partes[1:]
            perguntas_separadas.append((texto_pergunta, opcoes_resposta))

        return perguntas_separadas
  


    def verificar_respostas(self, resposta):
        messages = [
                    {"role": "system", "content": f"Voce ira receber um conjunto de 5 perguntas e {resposta} e ira verificar quais estão corretas ou não, caso estejam erradas voce dirá porque estão erradas. Por favor seja muito certo de sua respostas, leia bem a pergunta e as respostas antes de dizer se estão corretas ou não. Coloque a questão , a questão que o usuario selecionou, e se ela esta certa ou errada "},
                    {"role": "user","content":f"as {resposta} são essas." }]
        for pergunta, opcao in resposta.items():
            messages.append({"role": "system", "content": f"Pergunta: {pergunta}\nResposta: {opcao}\n"})
    

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=550,
        
        )
        respostas_text = response.choices[0].message.content

        respostas_text = respostas_text.split('\n\n', 1)[1]
        respostas_ia = respostas_text.split("\n\n")

        return respostas_ia
