# Importa o módulo pytest para executar os testes
import pytest

# Importa a função patch do módulo unittest.mock para realizar patching
from unittest.mock import patch

# Importa a função get_emblema_url do módulo app.utils.utils_user para teste
from app.utils.utils_user import get_emblema_url


# Define os parâmetros de teste para a função get_emblema_url
@pytest.mark.parametrize(
    "pontos, expected_filename",
    [
        # Define os pontos de entrada e os nomes de arquivo esperados
        (0, "images/rank/1.png"),
        (9, "images/rank/1.png"),
        (10, "images/rank/2.png"),
        (19, "images/rank/2.png"),
        (20, "images/rank/3.png"),
        (29, "images/rank/3.png"),
        (30, "images/rank/4.png"),
        (79, "images/rank/4.png"),
        (80, "images/rank/5.png"),
        (129, "images/rank/5.png"),
        (130, "images/rank/6.png"),
        (199, "images/rank/6.png"),
        (200, "images/rank/7.png"),
        (299, "images/rank/7.png"),
        (300, "images/rank/8.png"),
        (499, "images/rank/8.png"),
        (500, "images/rank/9.png"),
        (799, "images/rank/9.png"),
        (800, "images/rank/10.png"),
        (1099, "images/rank/10.png"),
        (1100, "images/rank/11.png"),
        (2099, "images/rank/11.png"),
        (2100, "images/rank/12.png"),
        (4099, "images/rank/12.png"),
        (4100, "images/rank/13.png"),
        (8099, "images/rank/13.png"),
        (8100, "images/rank/14.png"),
        (10099, "images/rank/14.png"),
        (10100, "images/rank/15.png"),
        (12999, "images/rank/15.png"),
        (13000, "images/rank/16.png"),
        (18099, "images/rank/16.png"),
        (18100, "images/rank/17.png"),
        (25099, "images/rank/17.png"),
        (25100, "images/rank/18.png"),
        (36099, "images/rank/18.png"),
        (36100, "images/rank/19.png"),
        (51099, "images/rank/19.png"),
        (51100, "images/rank/20.png"),
        (72099, "images/rank/20.png"),
        (72100, "images/rank/21.png"),
        (101099, "images/rank/21.png"),
        (101100, "images/rank/22.png"),
        (131099, "images/rank/22.png"),
        (131100, "images/rank/23.png"),
        (161099, "images/rank/23.png"),
        (161100, "images/rank/24.png"),
        (251099, "images/rank/24.png"),
    ],
)
# Testa a função get_emblema_url com os parâmetros fornecidos
@patch("app.utils.utils_user.url_for")
def test_get_emblema_url(mock_url_for, pontos, expected_filename):
    # Define o valor de retorno do mock_url_for para simular a rota estática
    mock_url_for.return_value = f"/static/{expected_filename}"
    # Chama a função get_emblema_url com os pontos fornecidos
    result = get_emblema_url(pontos)
    # Verifica se o url_for foi chamado com os parâmetros corretos
    mock_url_for.assert_called_with("static", filename=expected_filename)
    # Verifica se o resultado da função é o esperado
    assert result == f"/static/{expected_filename}"
