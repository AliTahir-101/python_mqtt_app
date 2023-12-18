import os
from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from .services.mqtt_client import MQTTClient
from .routes.health_check import router as health_check_router

load_dotenv()  # Load environment variables

mqtt_broker_url = os.getenv("MQTT_BROKER_URL")
mqtt_broker_port = int(os.getenv("MQTT_BROKER_PORT"))
mqtt_topic = os.getenv("MQTT_TOPIC")

# MQTT Client Setup
mqtt_client = MQTTClient(broker=mqtt_broker_url,
                         port=mqtt_broker_port, topic=mqtt_topic)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting MQTT client...")
    mqtt_client.start()

    yield

    # Clean up and release the resources
    print("Shutting down MQTT client...")
    mqtt_client.stop()


app = FastAPI(lifespan=lifespan)

app.include_router(health_check_router)
