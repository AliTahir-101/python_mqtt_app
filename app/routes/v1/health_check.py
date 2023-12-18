from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Health Check Endpoint

    Returns:
        dict: A dictionary with a status indicating the health of the service.
    """
    return {"status": "ok"}
