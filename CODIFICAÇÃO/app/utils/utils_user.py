from flask import url_for


# rank ate 24
def get_emblema_url(pontos):
    if pontos < 10:
        return url_for("static", filename="images/rank/1.png")
    elif pontos < 20:
        return url_for("static", filename="images/rank/2.png")
    elif pontos < 30:
        return url_for("static", filename="images/rank/3.png")
    elif pontos < 80:
        return url_for("static", filename="images/rank/4.png")
    elif pontos < 130:
        return url_for("static", filename="images/rank/5.png")
    elif pontos < 200:
        return url_for("static", filename="images/rank/6.png")
    elif pontos < 300:
        return url_for("static", filename="images/rank/7.png")
    elif pontos < 500:
        return url_for("static", filename="images/rank/8.png")
    elif pontos < 800:
        return url_for("static", filename="images/rank/9.png")
    elif pontos < 1100:
        return url_for("static", filename="images/rank/10.png")
    elif pontos < 2100:
        return url_for("static", filename="images/rank/11.png")
    elif pontos < 4100:
        return url_for("static", filename="images/rank/12.png")
    elif pontos < 8100:
        return url_for("static", filename="images/rank/13.png")
    elif pontos < 10100:
        return url_for("static", filename="images/rank/14.png")
    elif pontos < 13000:
        return url_for("static", filename="images/rank/15.png")
    elif pontos < 18100:
        return url_for("static", filename="images/rank/16.png")
    elif pontos < 25100:
        return url_for("static", filename="images/rank/17.png")
    elif pontos < 36100:
        return url_for("static", filename="images/rank/18.png")
    elif pontos < 51100:
        return url_for("static", filename="images/rank/19.png")
    elif pontos < 72100:
        return url_for("static", filename="images/rank/20.png")
    elif pontos < 101100:
        return url_for("static", filename="images/rank/21.png")
    elif pontos < 131100:
        return url_for("static", filename="images/rank/22.png")
    elif pontos < 161100:
        return url_for("static", filename="images/rank/23.png")
    elif pontos < 191100:
        return url_for("static", filename="images/rank/24.png")
    # Adicione mais condições conforme necessário para definir os emblemas com base nos pontos
    else:
        return "{{ url_for('static', filename='images/rank/default.png') }}"  # Emblema padrão para pontuações mais altas
