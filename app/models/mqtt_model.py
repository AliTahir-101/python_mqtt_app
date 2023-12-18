from pydantic import BaseModel, Field, TypeAdapter, ValidationError
from typing import Any
from bson import ObjectId


class Payload(BaseModel):
    """
    A model representing the payload data with the following attributes:
    session_id: Integer representing the session ID.
    energy_delivered_in_kWh: Float representing the energy delivered in kWh.
    duration_in_seconds: Integer representing the session duration in seconds.
    session_cost_in_cents: Integer representing the session cost in cents.
    """
    session_id: int
    energy_delivered_in_kWh: float
    duration_in_seconds: int
    session_cost_in_cents: int


class PyObjectId(ObjectId):
    """
    Custom type for handling BSON ObjectId for Pydantic models.
    This uses TypeAdapter for type conversion and custom validation.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, values):
        if isinstance(v, ObjectId):
            return str(v)
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema, source_type):
        """
        Custom schema method for Pydantic core to handle BSON ObjectId.
        """
        return {'type': 'string'}


class LogEntry(BaseModel):
    """
    Model representing a log entry with the following attributes:
    id: PyObjectId representing the log entry ID.
    timestamp: String representing the timestamp of the log entry.
    topic: String representing the log topic.
    payload: Payload object representing the log payload.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    timestamp: str
    topic: str
    payload: Payload

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: lambda oid: str(oid),
            PyObjectId: lambda oid: str(oid)
        }
