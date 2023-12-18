import pytest
from typing import Any, Dict
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from bson import ObjectId


@pytest.fixture
def client():
    return TestClient(app)


def test_get_all_messages_success(client):
    test_data = [{'_id': '658091a7a1f31226d48a5c08', 'timestamp': '2023-12-18 18:38:31', 'topic': 'charger/1/connector/1/session/1',
                  'payload': {'session_id': 1, 'energy_delivered_in_kWh': 30.0, 'duration_in_seconds': 45, 'session_cost_in_cents': 70}}]

    with patch('app.services.database_client.DatabaseClient.get_all_messages', return_value=test_data):
        response = client.get("/api/v1/messages")

        assert response.status_code == 200
        assert response.json() == test_data


def test_get_all_messages_failure(client):
    with patch('app.services.database_client.DatabaseClient.get_all_messages', side_effect=Exception("Database error")):
        response = client.get("/api/v1/messages")

        assert response.status_code == 500
        assert response.json() == {
            "detail": "Internal Server Error. Please try again later."}
