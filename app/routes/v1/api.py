import logging
from typing import List
from fastapi import APIRouter, HTTPException, status
from ...services.database_client import DatabaseClient
from ...models.mqtt_model import LogEntry

router = APIRouter()
db_client = DatabaseClient()
logger = logging.getLogger(__name__)


@router.get(
    "/messages",
    response_model=List[LogEntry],
    summary="Retrieve Energy Session Logs",
    description=(
        "Fetches a list of all energy session logs stored in the database. "
        "Each log entry contains details about energy consumption, session duration, and cost. "
        "Data is simulated and updated every minute, reflecting real-time energy usage by various devices."
    ),
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": [
                        LogEntry.Config.schema_extra["example"]
                    ]
                }
            }
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {"detail": "Internal Server Error. Please try again later."}
                }
            }
        }
    }
)
def get_all_messages():
    """
    Retrieve a list of all log messages.

    Returns:
        List[LogEntry]: A list of LogEntry objects containing log messages.

    Raises:
        HTTPException:
            - 500 Internal Server Error: If there is an issue with the database connection.
    """
    try:
        messages = db_client.get_all_messages()
        return [LogEntry(**message).model_dump(by_alias=True) for message in messages]
    except Exception as e:
        logger.exception(f"Internal Server Error. {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Please try again later.")
