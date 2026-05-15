import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    # Простая проверка, что документация доступна
    response = client.get("/docs")
    assert response.status_code == 200