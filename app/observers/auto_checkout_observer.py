from app.observers.subject import Observer
from app.observers.singleton import SingletonMeta
from app.db.session import SessionLocal
from app.models.booking import Booking, BookingStatus
from app.models.room import Room, RoomStatus

class AutoCheckoutObserver(Observer, metaclass=SingletonMeta):
    def update(self, event: str, data: dict):
        if event != "auto_checkout":
            return

        booking_id = data.get("booking_id")
        if not booking_id:
            return

        db = SessionLocal()
        try:
            booking = db.query(Booking).filter(Booking.id == booking_id).first()
            if booking.status == BookingStatus.checked_in:
                booking.status = BookingStatus.checked_out
                room = db.query(Room).filter(Room.room_code == booking.room_code).first()
                room.status = RoomStatus.available
                db.commit()
        finally:
            db.close()
