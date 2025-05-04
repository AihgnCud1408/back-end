from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.device import Device, DeviceStatus
from app.models.user import User, Role
from app.schemas.device_schema import DeviceSchema
from app.services.auth_service import get_current_user
from app.services.iot_service import IotService
from typing import List
from app.utils.rbac import require_roles

router = APIRouter(prefix="/iot", tags=["iot"], dependencies=[require_roles([Role.student, Role.lecturer])])

@router.get("/", response_model=List[DeviceSchema])
def get_current_room_devices(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return IotService.get_current_room_devices(db, current_user.id)

@router.post("/{device_id}", response_model=DeviceSchema)
def control_device(device_id: int, db: Session = Depends(get_db)):
    return IotService.control_device(db, device_id)


