from fastapi import APIRouter, status
from app.models.health_check_model import HealthCheckResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="API Health Check",
    description=(
        "Checks the health of the API service. This endpoint is used for monitoring the status of the application, "
        "ensuring it is up and running. It returns a simple status message indicating the health of the service. "
        "A typical response includes a status field with a value of 'ok', signifying that the API is operational."
    ),
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
