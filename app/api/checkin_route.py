from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.checkin_schema import CheckinReadSchema
from app.services.checkin_service import CheckinService
from app.db.session import get_db
from app.services.auth_service import get_current_user
from app.models.user import User

router = APIRouter(prefix="/check", tags=["checkin"])

@router.post("/in/{booking_id}", response_model=CheckinReadSchema)
def check_in(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CheckinService().check_in(db, current_user.user_code, booking_id)

@router.post("/out/{booking_id}", response_model=CheckinReadSchema)
def check_out(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CheckinService().check_out(db, current_user.user_code, booking_id)
