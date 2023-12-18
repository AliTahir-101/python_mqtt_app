from fastapi import FastAPI
from contextlib import asynccontextmanager
from .services.mqtt_client import MQTTClient
from .routes.health_check import router as health_check_router

# MQTT Client Setup
mqtt_client = MQTTClient(broker="127.0.0.1",
                         port=1883, topic="charger/1/connector/1/session/1")


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
