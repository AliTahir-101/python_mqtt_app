import os
from dotenv import load_dotenv


class Config:
    load_dotenv()  # Loading environment variables from our root .env file only once here

    MQTT_BROKER_URL = os.getenv("MQTT_BROKER_URL")
    MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT"))
    MQTT_TOPIC = os.getenv("MQTT_TOPIC")
    MONGODB_URI = os.getenv("MONGODB_URI")
