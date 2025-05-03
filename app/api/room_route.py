from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import Role
from app.schemas.room_schema import RoomReadSchema
from app.services.room_service import RoomService
from typing import List
from datetime import date, time
from app.utils.rbac import require_roles

router = APIRouter(prefix="/room", tags=["room"], dependencies=[require_roles([Role.student, Role.lecturer])])

@router.get("/", response_model=List[RoomReadSchema])
def search(
    booking_date: date,
    start_time: time,
    end_time: time,
    db: Session = Depends(get_db)
):
    return RoomService.get_available_rooms(db, booking_date, start_time, end_time)
    