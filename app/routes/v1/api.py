from typing import List
from fastapi import APIRouter, HTTPException
from ...services.database_client import DatabaseClient
from ...models.mqtt_model import LogEntry

router = APIRouter()
db_client = DatabaseClient()


@router.get("/messages", response_model=List[LogEntry])
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
        raise HTTPException(
            status_code=500, detail="Internal Server Error. Please try again later.")
