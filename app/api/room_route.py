from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.room_schema import RoomReadSchema
from app.services.room_service import RoomService
from typing import List
from datetime import date, time

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.get("/", response_model=List[RoomReadSchema])
def get_all_rooms(
    booking_date: date,
    start_time: time,
    end_time: time,
    db: Session = Depends(get_db)
):
    return RoomService.get_available_rooms(db, booking_date, start_time, end_time)
    