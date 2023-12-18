# 🌐 Python MQTT Application with FastAPI and Docker 🐳

This Python application is a demonstration of integrating MQTT messaging with a FastAPI backend, all containerized using Docker. It subscribes to an MQTT topic, logs the messages, stores them in a MongoDB database, and exposes them via a REST API.

## Features

- 📡 Subscribes to MQTT topics.
- 📝 Logs MQTT messages with timestamps.
- 💾 Stores messages in MongoDB.
- 🚀 FastAPI for serving stored messages.
- 🐳 Fully containerized with Docker and Docker Compose.

## Prerequisites

Before running this project, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. **Clone the Repository:**

   ```bash
   git clone repo_url
   cd python_mqtt_app
   ```

2. **Environment Setup:**
   Create a `.env` file in the root directory and add any necessary environment variables e.g.

   ```bash
   MONGODB_URI=mongodb://mongo:27017/mqtt_data_store
   MQTT_BROKER_URL=mosquitto
   MQTT_BROKER_PORT=1883
   MQTT_TOPIC=charger/1/connector/1/session/1
   ```

3. **Build and Run with Docker Compose:**

   ```bash
   sudo docker-compose up --build
   ```

   This will start the MQTT broker (Mosquitto), MongoDB, and the Python application.

4. **Accessing the API Docs:**
   The FastAPI server runs on port 8000. Access the API Docs at `http://localhost:8000/docs`.

## Usage

- **MQTT Publishing:**

  The application publishes new MQTT sessions every minute with topics like `charger/1/connector/1/session/1`.

- **Viewing Stored Messages:**

  Use the FastAPI endpoint `/api/v1/messages` to retrieve all stored MQTT messages.

## Testing

To run tests, use the following command:

```bash
sudo docker-compose build --no-cache (optional if build already)
sudo docker-compose run test
```

## Structure

```bash
/python_mqtt_app
├── app/                  # Application source files
├── tests/                # Test cases
├── Dockerfile            # Dockerfile for Python app
├── docker-compose.yml    # Docker Compose configuration
├── mosquitto.conf        # Configuration for Mosquitto MQTT broker
├── README.md             # This file
└── requirements.txt      # Python dependencies

```

⭐️ From [Ali Tahir](https://github.com/AliTahir-101) with ❤️
