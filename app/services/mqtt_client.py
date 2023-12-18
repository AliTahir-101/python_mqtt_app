import paho.mqtt.client as mqtt
import time
import json
import threading
import datetime
from typing import Any, Dict


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
        print(f"Connected with result code {rc}")
        client.subscribe(self.topic)

    def on_message(self, client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage) -> None:
        """
        Callback for when a PUBLISH message is received from the broker.

        Args:
            client (mqtt.Client): The client instance for this callback.
            userdata (Any): The private user data as set in Client() or user_data_set().
            message (mqtt.MQTTMessage): An instance of MQTTMessage. This is a class with members topic, payload, qos, retain.
        """
        timestamp: datetime.datetime = datetime.datetime.now()
        payload: str = message.payload.decode("utf-8")
        payload_data: Dict = json.loads(payload)

        log_entry: Dict[str, Any] = {
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "topic": message.topic,
            "payload": payload_data
        }

        print(f"Received message: {json.dumps(log_entry)}")

    def start(self) -> None:
        """
        Starts the MQTT client and connects it to the broker. Also starts a thread for publishing messages periodically.
        """
        self.running = True
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()
        threading.Thread(target=self.publish_message_periodically).start()

    def publish_message_periodically(self) -> None:
        """
        Publishes messages to the MQTT topic periodically every 60 seconds.
        """
        while self.running:
            message: Dict[str, Any] = {
                "session_id": 1,
                "energy_delivered_in_kWh": 30,
                "duration_in_seconds": 45,
                "session_cost_in_cents": 70
            }
            self.client.publish(self.topic, json.dumps(message))
            time.sleep(60)

    def stop(self) -> None:
        """
        Stops the MQTT client and disconnects it from the broker.
        """
        self.running = False
        self.client.loop_stop()
        self.client.disconnect()
