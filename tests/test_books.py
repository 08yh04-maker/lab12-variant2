import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)


def test_get_books_empty():
    response = client.get("/books/")
    assert response.status_code == 200
    assert "books" in response.json()


def test_get_book_not_found():
    response = client.get("/books/99999")
    assert response.status_code == 404