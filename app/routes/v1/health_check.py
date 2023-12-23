from fastapi import APIRouter, status
from app.models.health_check_model import HealthCheckResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": HealthCheckResponse.Config.schema_extra["example"]
                }
            }
        }
    }
)
@router.get("/health", response_model=HealthCheckResponse)
def health_check():
    """
    Health Check Endpoint

    Returns:
        HealthCheckResponse: A response model indicating the health of the service.
    """
    return {"status": "ok"}
