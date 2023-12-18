import paho.mqtt.client as mqtt
import time
import json
import threading
import datetime
from typing import Any, Dict
from .database_client import DatabaseClient
from ..models.mqtt_model import LogEntry


class MQTTClient:
    """
    A client class for connecting to an MQTT broker and handling messages.

    Attributes:
        broker (str): The address of the MQTT broker.
        port (int): The port number of the MQTT broker.
        topic (str): The MQTT topic to subscribe to and publish messages.
    """

    def __init__(self, broker: str, port: int, topic: str) -> None:
        """
        Initialize the MQTT client with broker details and topic.

        Args:
            broker (str): The address of the MQTT broker.
            port (int): The port number of the MQTT broker.
            topic (str): The MQTT topic to subscribe to.
        """
        self.client = mqtt.Client()
        self.broker: str = broker
        self.port: int = port
        self.topic: str = topic
        self.running: bool = False
        self.db_client = DatabaseClient()

        # Set up callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client: mqtt.Client, userdata: Any, flags: Dict, rc: int) -> None:
        """
        Callback for when the client receives a CONNACK response from the server.

        Args:
            client (mqtt.Client): The client instance for this callback.
            userdata (Any): The private user data as set in Client() or user_data_set().
            flags (Dict): Response flags sent by the broker.
            rc (int): The connection result.
        """
        if rc == 0:
            print(f"Connected with result code {rc}")
            client.subscribe(self.topic)
        else:
            print(f"Connection failed with result code {rc}")

    def on_message(self, client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage) -> None:
        """
        Callback for when a PUBLISH message is received from the broker.

        Args:
            client (mqtt.Client): The client instance for this callback.
            userdata (Any): The private user data as set in Client() or user_data_set().
            message (mqtt.MQTTMessage): An instance of MQTTMessage. This is a class with members topic, payload, qos, retain.
        """
        try:
            timestamp: datetime.datetime = datetime.datetime.now()
            payload: str = message.payload.decode("utf-8")
            payload_data: Dict = json.loads(payload)

            # Create a LogEntry instance
            log_entry = LogEntry(
                timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                topic=message.topic,
                payload=payload_data
            )

            # Save the log entry to the database
            self.db_client.save_message(log_entry.model_dump())
            print(f"Received message: {log_entry.model_dump_json()}")
        except Exception as e:
            # Handle any exceptions that might occur during message processing
            print(f"Error processing message: {str(e)}")

    def start(self) -> None:
        """
        Starts the MQTT client and connects it to the broker. Also starts a thread for publishing messages periodically.
        """
        try:
            self.running = True
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            threading.Thread(target=self.publish_message_periodically).start()
        except Exception as e:
            # Handle connection-related exceptions and log the error
            print(f"MQTT Client Error: {str(e)}")

    def publish_message_periodically(self) -> None:
        """
        Publishes messages to the MQTT topic periodically every 60 seconds.
        """
        while self.running:
            try:
                message: Dict[str, Any] = {
                    "session_id": 1,
                    "energy_delivered_in_kWh": 30,
                    "duration_in_seconds": 45,
                    "session_cost_in_cents": 70
                }
                self.client.publish(self.topic, json.dumps(message))
                time.sleep(60)
            except Exception as e:
                # Handle publishing-related exceptions and log the error
                print(f"MQTT Publish Error: {str(e)}")

    def stop(self) -> None:
        """
        Stops the MQTT client and disconnects it from the broker.
        """
        try:
            self.running = False
            self.client.loop_stop()
            self.client.disconnect()
        except Exception as e:
            # Handle disconnection-related exceptions and log the error
            print(f"MQTT Disconnect Error: {str(e)}")
