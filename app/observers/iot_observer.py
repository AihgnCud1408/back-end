from app.db.session import SessionLocal
from app.observers.subject import Observer
from app.observers.singleton import SingletonMeta
from app.models.room import Room
from app.models.device import Device, DeviceStatus

class IotObserver(Observer, metaclass=SingletonMeta):
    def update(self, event: str, data: dict):
        if event != "checked_in":
            return

        room_id = data.get("room_id")
        if not room_id:
            return

        db = SessionLocal()
        try:
            room = db.query(Room).filter(Room.id == room_id).first()
            if room:
                light = db.query(Device).filter(
                    Device.room_id == room.id,
                    Device.type == "light"
                ).first()
                if light:
                    light.status = DeviceStatus.on
                    db.commit()
        finally:
            db.close()
