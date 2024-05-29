# tests/test_index.py


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b'class="logoHome"' in response.data
