import json
import pytest
import threading
from unittest.mock import Mock, patch, MagicMock, call
from app.services.mqtt_client import MQTTClient
from paho.mqtt.client import MQTTMessage


@pytest.fixture
def mock_thread():
    """
    A fixture to mock threading.Thread.
    """
    with patch.object(threading, 'Thread', MagicMock()) as MockThread:
        yield MockThread


@pytest.fixture
def mock_mqtt_client():
    """
    A fixture to mock the paho.mqtt.client.Client.
    """
    with patch('paho.mqtt.client.Client') as MockClient:
        yield MockClient()


@pytest.fixture
def mock_db_client():
    """
    A fixture to mock the DatabaseClient.
    """
    with patch('app.services.database_client.DatabaseClient') as MockDBClient:
        mock_db_client = MockDBClient()
        mock_db_client.save_message = Mock()  # Mock the save_message method
        yield mock_db_client


def test_mqtt_client_init(mock_mqtt_client, mock_db_client):
    """
    Test the initialization of MQTTClient.
    """
    mqtt_client = MQTTClient("broker.test", 1883, "test/topic")
    assert mqtt_client.broker == "broker.test"
    assert mqtt_client.port == 1883
    assert mqtt_client.topic == "test/topic"


def test_on_connect_success(mock_mqtt_client, mock_db_client):
    """
    Test successful connection handling in MQTTClient.
    """
    mqtt_client = MQTTClient("broker.test", 1883, "test/topic")
    mqtt_client.on_connect(mock_mqtt_client, None, {}, 0)
    mock_mqtt_client.subscribe.assert_called_with("test/topic")


def test_on_connect_failure(mock_mqtt_client, mock_db_client):
    """
    Test failed connection handling in MQTTClient.
    """
    mqtt_client = MQTTClient("broker.test", 1883, "test/topic")
    # Non-zero return code indicates failure
    mqtt_client.on_connect(mock_mqtt_client, None, {}, 1)
    mock_mqtt_client.subscribe.assert_not_called()


def test_on_message(mock_mqtt_client, mock_db_client):
    mqtt_client = MQTTClient("broker.test", 1883, "test/topic")
    mqtt_client.db_client = mock_db_client  # Use the mock database client

    message = MQTTMessage()
    message.payload = json.dumps({
        "session_id": 1,
        "energy_delivered_in_kWh": 30,
        "duration_in_seconds": 45,
        "session_cost_in_cents": 70
    }).encode()
    message.topic = b'test/topic'

    mqtt_client.on_message(mock_mqtt_client, None, message)

    if mock_db_client.save_message.called:
        args, _ = mock_db_client.save_message.call_args
        saved_data = args[0]
        assert 'timestamp' in saved_data
        assert saved_data['topic'] == 'test/topic'
        assert saved_data['payload']['session_id'] == 1
        assert saved_data['payload']['energy_delivered_in_kWh'] == 30
        assert saved_data['payload']['duration_in_seconds'] == 45
        assert saved_data['payload']['session_cost_in_cents'] == 70
    else:
        pytest.fail("save_message was not called")


def test_start_publish_thread(mock_mqtt_client, mock_db_client, mock_thread):
    """
    Test that the MQTTClient starts a thread for publishing messages.
    """
    mqtt_client = MQTTClient("broker.test", 1883, "test/topic")
    mqtt_client.start()

    mock_thread_calls = mock_thread.mock_calls
    expected_call = call(target=mqtt_client.publish_message_periodically)

    assert expected_call in mock_thread_calls, "Expected thread start call not found"


def test_stop_publish_thread(mock_mqtt_client, mock_db_client, mock_thread):
    """
    Test that the MQTTClient stops its publishing thread correctly.
    """
    mqtt_client = MQTTClient("broker.test", 1883, "test/topic")
    mqtt_client.start()
    mqtt_client.stop()

    assert not mqtt_client.running, "MQTT client running flag should be False"


def test_on_message_valid_payload(mock_mqtt_client, mock_db_client):
    """
    Test the handling of a valid MQTT message by the MQTTClient.
    This test simulates receiving a valid MQTT message and ensures it is processed correctly,
    including saving the message to the database.
    """
    mqtt_client = MQTTClient("broker.test", 1883, "test/topic")
    mqtt_client.db_client = mock_db_client

    valid_message = MQTTMessage()
    valid_message.payload = json.dumps({
        "session_id": 1,
        "energy_delivered_in_kWh": 30.0,
        "duration_in_seconds": 45,
        "session_cost_in_cents": 70
    }).encode()
    valid_message.topic = b'test/topic'

    mqtt_client.on_message(mock_mqtt_client, None, valid_message)

    assert mock_db_client.save_message.called, "Message should be saved for valid payload"


def test_on_message_invalid_payload(mock_mqtt_client, mock_db_client):
    """
    Test the handling of an invalid MQTT message by the MQTTClient.
    This test simulates receiving an MQTT message with invalid payload data,
    and checks that the message is not processed or saved to the database.
    """
    mqtt_client = MQTTClient("broker.test", 1883, "test/topic")
    mqtt_client.db_client = mock_db_client

    invalid_message = MQTTMessage()
    invalid_message.payload = json.dumps({
        "session_id": 1,
        "energy_delivered_in_kWh": "invalid",  # Invalid type
        "duration_in_seconds": 45,
        "session_cost_in_cents": 70
    }).encode()
    invalid_message.topic = b'test/topic'

    mqtt_client.on_message(mock_mqtt_client, None, invalid_message)

    assert not mock_db_client.save_message.called, "Message should not be saved for invalid payload"


def test_on_message_exception_handling(mock_mqtt_client, mock_db_client, caplog):
    """
    Test exception handling in the MQTTClient's on_message method.
    This test simulates an exception during the message processing to ensure
    that exceptions are handled gracefully and logged correctly.
    """
    mqtt_client = MQTTClient("broker.test", 1883, "test/topic")
    mqtt_client.db_client = mock_db_client

    # Let's Simulate an exception in message handling
    mock_db_client.save_message.side_effect = Exception("Test exception")

    message = MQTTMessage()
    message.payload = json.dumps({
        "session_id": 1,
        "energy_delivered_in_kWh": 30.0,
        "duration_in_seconds": 45,
        "session_cost_in_cents": 70
    }).encode()
    message.topic = b'test/topic'

    mqtt_client.on_message(mock_mqtt_client, None, message)

    assert "Error processing message" in caplog.text, "Exception should be logged"
