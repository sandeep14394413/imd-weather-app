import requests

from app.config import settings
from app.schemas import ForecastRequest, ForecastResponse


def request_forecast(payload: ForecastRequest) -> ForecastResponse:
    response = requests.post(
        f"{settings.model_api_url}/predict",
        json=payload.model_dump(mode="json"),
        timeout=20,
    )
    response.raise_for_status()
    return ForecastResponse(**response.json())
