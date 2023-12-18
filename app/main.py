import os
import logging
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from .services.mqtt_client import MQTTClient
from .routes.v1.api import router as v1_router
from .routes.v1.health_check import router as health_router

# Configure the logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()  # Load environment variables from a .env file

# Retrieve MQTT broker configuration from environment variables
mqtt_broker_url = os.getenv("MQTT_BROKER_URL")
mqtt_broker_port = int(os.getenv("MQTT_BROKER_PORT"))
mqtt_topic = os.getenv("MQTT_TOPIC")

# Initialize and configure the MQTT client
mqtt_client = MQTTClient(broker=mqtt_broker_url,
                         port=mqtt_broker_port, topic=mqtt_topic)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI app.
    Manages the lifecycle of the MQTT client, starting it before the app starts and
    shutting it down after the app is finished.

    :param app: Instance of the FastAPI application.
    """
    try:
        logger.info("Starting MQTT client...")
        mqtt_client.start()

        yield

    except Exception as e:
        # Handle any unexpected exceptions and raise an HTTPException with a 500 status code
        logger.exception("Internal Server Error. Please try again later.")
        raise HTTPException(
            status_code=500, detail="Internal Server Error. Please try again later.")

    finally:
        # Clean up and release the resources on app shutdown
        logger.info("Shutting down MQTT client...")
        mqtt_client.stop()

app = FastAPI(lifespan=lifespan)

# Include routers for different endpoints
app.include_router(v1_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")
