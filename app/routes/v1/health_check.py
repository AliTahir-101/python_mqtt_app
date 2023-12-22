from fastapi import APIRouter
from app.models.health_check_model import HealthCheckResponse

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
def health_check():
    """
    Health Check Endpoint

    Returns:
        HealthCheckResponse: A response model indicating the health of the service.
    """
    return {"status": "ok"}
