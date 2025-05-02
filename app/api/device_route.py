from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.device_schema import DeviceSchema
from app.models.device import Device
from app.services.device_service import DeviceServices
from typing import List

router = APIRouter(prefix="/manage/devices", tags=["device"])

@router.get("/", response_model=List[DeviceSchema])
def get_all_devices(db: Session = Depends(get_db)):
    return db.query(Device).all()

@router.post("/create", response_model=DeviceSchema)
def create_room_api(device: DeviceSchema, db: Session = Depends(get_db)):
    return DeviceServices().create_device(db, device)

@router.delete("/rooms/delete/{device_id}")
def delete_room_api(device_id: int, db: Session = Depends(get_db)):
    return DeviceServices().delete_device(db, device_id)