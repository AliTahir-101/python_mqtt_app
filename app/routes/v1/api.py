from typing import List
from fastapi import APIRouter
from ...services.database_client import DatabaseClient
from ...models.mqtt_model import LogEntry

router = APIRouter()
db_client = DatabaseClient()


@router.get("/messages", response_model=List[LogEntry])
def get_all_messages():
    messages = db_client.get_all_messages()
    return [LogEntry(**message).model_dump(by_alias=True) for message in messages]
