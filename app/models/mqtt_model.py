from pydantic import BaseModel, Field
from bson import ObjectId, Optional


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
    id: PyObjectId representing the log entry DB ID.
    timestamp: String representing the timestamp of the log entry.
    topic: String representing the log topic.
    payload: Payload object representing the log payload.
    """
    id: Optional[PyObjectId] = Field(None, alias="_id")
    timestamp: str
    topic: str
    payload: Payload

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: lambda oid: str(oid),
            PyObjectId: lambda oid: str(oid)
        }
        schema_extra = {
            "example": {
                "id": "6585fdf275bc18953fe35770",
                "timestamp": "2023-12-18 18:38:31",
                "topic": "charger/1/connector/1/session/1",
                "payload": {
                    "session_id": 1,
                    "energy_delivered_in_kWh": 30.12,
                    "duration_in_seconds": 45,
                    "session_cost_in_cents": 70
                }
            }
        }
