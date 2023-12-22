from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """
    Health Check Response Model

    This model represents the response structure for the health check endpoint.
    It provides a simple way to convey the operational status of the service.

    Attributes:
        status (str): A string indicating the health of the service.
                      Typical values are 'ok' for a healthy service and
                      'unhealthy' or specific error messages for a service
                      experiencing issues.
    """
    status: str
