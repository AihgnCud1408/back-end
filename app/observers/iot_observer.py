from sqlalchemy.orm import Session
from app.observers.subject import Observer
from app.observers.singleton import SingletonMeta
from app.models.room import Room, SensorStatus
from app.models.device import Device, DeviceStatus


class IotObserver(Observer, metaclass=SingletonMeta):
    def update(self, db: Session, event: str, data: dict):
        if event != "checked_in":
            return

        room_id = data.get("room_id")
        if not room_id:
            return

        try:
            room = db.query(Room).get(room_id)
            if room and room.sensor == SensorStatus.active:
                light = db.query(Device).filter(
                    Device.room_id == room_id,
                    Device.type == "light"
                ).first()
                if light and light.status == DeviceStatus.off:
                    light.status = DeviceStatus.on
                    db.add(light)
                    db.commit()
        finally:
            return
