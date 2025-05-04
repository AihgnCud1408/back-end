from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.room import Room, SensorStatus
from app.models.booking import Booking, BookingStatus
from app.models.device import Device, DeviceStatus
from threading import Timer
from datetime import datetime

class IotService:
    @staticmethod
    def get_current_room_devices(db: Session, user_id: int):
        now = datetime.now()
        today = now.date()
        current_time = now.time()
        booking = db.query(Booking).filter(
            Booking.user_id == user_id,
            Booking.booking_date == today,
            Booking.start_time <= current_time,
            Booking.end_time >= current_time,
            Booking.status == BookingStatus.checked_in
        ).first()
        if not booking:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "There is no room in_use.")

        return db.query(Device).filter(Device.room_id == booking.room_id).all()

    @staticmethod
    def control_device(db: Session, device_id: int):
        device = db.query(Device).filter(Device.id == device_id).first()
        if not device:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Device not found.")

        if device.status == DeviceStatus.on:
            device.status = DeviceStatus.off
        else:
            device.status = DeviceStatus.on
        db.commit()
        db.refresh(device)
        return device
