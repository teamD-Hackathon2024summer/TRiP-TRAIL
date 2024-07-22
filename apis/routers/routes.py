# routers/routes.py
from fastapi import APIRouter, HTTPException
from schemas import RouteRequest
import googlemaps
import os

router = APIRouter()

gmaps = googlemaps.Client(key=os.getenv("GMAPS_API_KEY"))

@router.post("/route")
async def get_route(request: RouteRequest):
    try:
        directions = gmaps.directions(request.origin, request.destination)
        return directions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def read_root():
    return {"Hello": "World"}
