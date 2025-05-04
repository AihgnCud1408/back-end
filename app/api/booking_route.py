from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.booking_schema import BookingCreateSchema, BookingReadSchema
from app.services.booking_service import BookingService
from app.db.session import get_db
from app.services.auth_service import get_current_user
from app.models.user import User, Role
from app.utils.rbac import require_roles

router = APIRouter(prefix="/booking", tags=["booking"], dependencies=[require_roles([Role.student, Role.lecturer])])

@router.post("/", response_model=BookingReadSchema)
def book_room(
    payload: BookingCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = BookingService.create_booking(
        db,
        current_user.id,
        payload.room_id,
        payload.booking_date,
        payload.start_time,
        payload.end_time
    )
    return booking

@router.post("/cancel", response_model=BookingReadSchema)
def cancel_booking(booking_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return BookingService.cancel_booking(db, booking_id, current_user.id)

@router.get("/my_bookings", response_model=List[BookingReadSchema])
def get_user_bookings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return BookingService.get_active_bookings(db, current_user.id)

@router.get("/history", response_model=List[BookingReadSchema])
def get_user_bookings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return BookingService.get_user_bookings(db, current_user.id)

