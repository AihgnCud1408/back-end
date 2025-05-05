from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import Role
from app.schemas.booking_schema import BookingReadSchema
from app.schemas.room_schema import RoomReadSchema, RoomCreateSchema
from app.schemas.report_schema import ReportReadSchema
from app.services.booking_service import BookingService
from app.services.room_service import RoomService
from app.services.report_service import ReportService
from app.utils.rbac import require_roles
from typing import List

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[require_roles([Role.admin])])

@router.get("/room", response_model=List[RoomReadSchema])
def get_all_rooms(db: Session = Depends(get_db)):
    return RoomService.get_all_rooms(db)

@router.post("/room/create", response_model=RoomReadSchema)
def create_room(payload: RoomCreateSchema, db: Session = Depends(get_db)):
    return RoomService.create_room(
        db,
        payload.room_code,
        payload.room_type,
        payload.location
    )

@router.delete("/room/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    return RoomService.delete_room(db, room_id)

@router.get("/booking", response_model=List[BookingReadSchema])
def get_all_bookings(db: Session = Depends(get_db)):
    return BookingService.get_all_bookings(db)

@router.get("/export", response_model=ReportReadSchema)
def export_report(year: int, month: int, db: Session = Depends(get_db)):
    return ReportService.count_bookings(db, year, month)
