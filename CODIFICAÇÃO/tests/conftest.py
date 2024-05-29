# tests/conftest.py
import sys
import os

import pytest

# erro de diretorio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def client(app):
    return app.test_client()
