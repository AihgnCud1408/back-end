from sqlalchemy.orm import Session
from datetime import datetime, time, date
from app.models.room import Room
from app.models.booking import Booking, BookingStatus

class RoomService:
    @staticmethod
    def get_all_rooms(db: Session):
        return db.query(Room).all()

    @staticmethod
    def get_available_rooms(db: Session, booking_date: date, start_time: time, end_time: time):
        conflict = db.query(Booking.room_id).filter(
            Booking.booking_date == booking_date,
            Booking.start_time < end_time,
            Booking.end_time > start_time,
            Booking.status.in_([BookingStatus.active, BookingStatus.checked_in])
        ).subquery()
        available_rooms = db.query(Room).filter(Room.id.notin_(conflict)).all()
        return available_rooms
