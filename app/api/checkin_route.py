from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.checkin_schema import CheckinReadSchema
from app.services.checkin_service import CheckinService
from app.db.session import get_db
from app.services.auth_service import get_current_user
from app.models.user import User, Role
from app.utils.rbac import require_roles

router = APIRouter(prefix="/check", tags=["checkin"], dependencies=[require_roles([Role.student, Role.lecturer])])

@router.post("/in", response_model=CheckinReadSchema)
def check_in(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CheckinService.check_in(db, current_user.id, booking_id)

@router.post("/in/qr/{room_code}", response_model=CheckinReadSchema)
def check_in_via_qr(
    room_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CheckinService.check_in_via_qr(db, current_user.id, room_code)

@router.post("/out", response_model=CheckinReadSchema)
def check_out(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CheckinService.check_out(db, current_user.id, booking_id)
