from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import Role
from app.schemas.device_schema import DeviceSchema
from app.models.device import Device
from typing import List
from app.utils.rbac import require_roles

router = APIRouter(prefix="/technician/devices", tags=["device"], dependencies=[require_roles([Role.technician])])

@router.get("/", response_model=List[DeviceSchema])
def get_all_devices(db: Session = Depends(get_db)):
    return db.query(Device).all()
