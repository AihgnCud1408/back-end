from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
from app.schemas.device_schema import DeviceSchema
from app.models.device import Device
from app.observers.subject import event_subject

class DeviceServices:
    def create_device(self, db: Session, device_data: DeviceSchema):
        existing = db.query(Device).filter(Device.id == device_data.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Room name already exists")

        device = Device(**device_data.model_dump())
        db.add(device)
        db.commit()
        db.refresh(device)
        return device
    
    def delete_device(self, db: Session, device_id: int):
        device = db.query(Device).filter(Device.id == device_id).first()
        if not device:
            raise HTTPException(status_code=404, detail="Room not found")
        db.delete(device)
        db.commit()