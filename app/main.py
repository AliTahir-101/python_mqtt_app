from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html
import os
import logging
from fastapi import FastAPI, HTTPException
from app.config import Config
from contextlib import asynccontextmanager
from .services.mqtt_client import MQTTClient
from .routes.v1.api import router as v1_router
from .routes.v1.health_check import router as health_router

# Configure the logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve MQTT broker configuration
mqtt_broker_url = Config.MQTT_BROKER_URL
mqtt_broker_port = Config.MQTT_BROKER_PORT
mqtt_topic = Config.MQTT_TOPIC

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

app = FastAPI(
    lifespan=lifespan,
    title="IoT Energy Session Tracking API",
    description=(
        "This API interfaces with an MQTT broker to receive data from IoT devices about energy consumption sessions. "
        "It logs these messages, stores them in a MongoDB database, and provides an endpoint to retrieve the session data. "
        "The API simulates various devices in a household and their energy usage. Data is simulated and updated every minute."
    ),
    version="1.0.0",
    contact={
        "name": "Energy Tracker Support",
        "email": "support@enersense.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Apparently we don't need these but we can do more customization if we want, leaving these here just for an example.
# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(
#         openapi_url="/custom-openapi.json",
#         title="Customized Swagger UI",
#         swagger_js_url="/static/swagger-ui-bundle.js",
#         swagger_css_url="/static/swagger-ui.css"
#     )


# @app.get("/custom-openapi.json", include_in_schema=False)
# async def custom_openapi():
#     return get_openapi(
#         title="Custom API",
#         version="1.0.0",
#         description="This is a custom OpenAPI schema",
#         routes=app.routes
#     )

# Include routers for different endpoints
app.include_router(v1_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")
