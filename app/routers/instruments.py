from fastapi import APIRouter
from app.services.instrument_service import fetch_instruments

router = APIRouter(prefix="/instruments", tags=["Instruments"])

@router.get("/")
def get_instruments():
    return fetch_instruments()
