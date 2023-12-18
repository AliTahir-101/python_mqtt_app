import pytest
from unittest.mock import patch, MagicMock
from app.services.database_client import DatabaseClient, DatabaseError


def test_init_success():
    """
    Test the successful initialization of the DatabaseClient.
    Ensures that the MongoClient is called once during initialization.
    """
    with patch('app.services.database_client.MongoClient') as mock_mongo:
        DatabaseClient()
        mock_mongo.assert_called_once()


def test_init_failure():
    """
    Test the initialization of the DatabaseClient with a failure scenario.
    Simulates a failure in the MongoClient connection and checks if a ConnectionError is raised.
    """
    with patch('app.services.database_client.MongoClient') as mock_mongo, \
            pytest.raises(ConnectionError):
        mock_mongo.side_effect = Exception("Connection failed")
        DatabaseClient()


def test_save_message_success():
    """
    Test the success of the save_message method in DatabaseClient.
    Checks if the message is correctly passed to the MongoClient's insert_one method.
    """
    with patch('app.services.database_client.MongoClient') as mock_mongo:
        client = DatabaseClient()
        mock_mongo.return_value.get_default_database.return_value.messages.insert_one = MagicMock()
        client.save_message({
            "session_id": 1,
            "energy_delivered_in_kWh": 30,
            "duration_in_seconds": 45,
            "session_cost_in_cents": 70
        })
        mock_mongo.return_value.get_default_database.return_value.messages.insert_one.assert_called_with({
            "session_id": 1,
            "energy_delivered_in_kWh": 30,
            "duration_in_seconds": 45,
            "session_cost_in_cents": 70
        })


def test_save_message_failure():
    """
    Test the failure of the save_message method in DatabaseClient.
    Simulates a failure in message insertion and checks if a DatabaseError is raised.
    """
    with patch('app.services.database_client.MongoClient') as mock_mongo:
        mock_mongo.return_value.get_default_database.return_value.messages.insert_one.side_effect = Exception(
            "Insertion failed")
        client = DatabaseClient()
        with pytest.raises(DatabaseError):
            client.save_message({
                "session_id": 1,
                "energy_delivered_in_kWh": 30,
                "duration_in_seconds": 45,
                "session_cost_in_cents": 70
            })


def test_get_all_messages_success():
    """
    Test the successful retrieval of all messages from the database.
    Validates that the returned value matches the expected mock data.
    """
    with patch('app.services.database_client.MongoClient') as mock_mongo:
        mock_mongo.return_value.get_default_database.return_value.messages.find.return_value = [{
            "session_id": 1,
            "energy_delivered_in_kWh": 30,
            "duration_in_seconds": 45,
            "session_cost_in_cents": 70
        }, {
            "session_id": 1,
            "energy_delivered_in_kWh": 30,
            "duration_in_seconds": 45,
            "session_cost_in_cents": 70
        }]
        client = DatabaseClient()
        result = client.get_all_messages()
        assert result == [{
            "session_id": 1,
            "energy_delivered_in_kWh": 30,
            "duration_in_seconds": 45,
            "session_cost_in_cents": 70
        }, {
            "session_id": 1,
            "energy_delivered_in_kWh": 30,
            "duration_in_seconds": 45,
            "session_cost_in_cents": 70
        }]


def test_get_all_messages_failure():
    """
    Test the failure of retrieving messages from the database.
    Simulates a query failure and checks if a DatabaseError is raised.
    """
    with patch('app.services.database_client.MongoClient') as mock_mongo:
        mock_mongo.return_value.get_default_database.return_value.messages.find.side_effect = Exception(
            "Query failed")
        client = DatabaseClient()
        with pytest.raises(DatabaseError):
            client.get_all_messages()


def test_close_connection():
    """
    Test the closing of the database connection.
    Ensures that the close method on the MongoClient instance is called once.
    """
    with patch('app.services.database_client.MongoClient') as mock_mongo:
        client = DatabaseClient()
        client.close_connection()
        mock_mongo.return_value.close.assert_called_once()
