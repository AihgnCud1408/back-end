from app.db.session import SessionLocal
from datetime import datetime, timedelta
from app.observers.subject import Observer
from app.observers.singleton import SingletonMeta
from app.models.booking import Booking, BookingStatus

class TimeoutObserver(Observer, metaclass=SingletonMeta):
    def update(self, event: str, data: dict):
        if event != "checkin_timeout":
            return

        booking_id = data.get("booking_id")
        if not booking_id:
            return

        db = SessionLocal()
        try:
            booking = db.query(Booking).get(booking_id)
            if (booking
                    and booking.status == BookingStatus.active
                    and datetime.now() >= booking.start_time + timedelta(minutes=30)):
                booking.status = BookingStatus.cancelled
                db.add(booking)
                db.commit()
        finally:
            db.close()
