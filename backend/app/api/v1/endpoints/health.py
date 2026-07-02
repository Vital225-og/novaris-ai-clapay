"""Health endpoint."""

from fastapi import APIRouter

from app.core.constants import APP_NAME, APP_VERSION

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": APP_NAME,
        "version": APP_VERSION,
    }

