from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, time, date, timedelta
from app.models.booking import Booking, BookingStatus
from app.models.room import Room
from threading import Timer
from app.observers.subject import event_subject

class BookingService:
    @staticmethod
    def create_booking(db: Session, user_id: int, room_code: str, booking_date: date, start_time: time, end_time: time):
        room = db.query(Room).filter(Room.room_code == room_code).first()
        if not room:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Room not found.")

        conflict1 = db.query(Booking).filter(
            Booking.user_id == user_id,
            Booking.booking_date == booking_date,
            Booking.start_time < end_time,
            Booking.end_time > start_time,
            Booking.status.in_([BookingStatus.active, BookingStatus.checked_in])
        ).first()
        if conflict1:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "You have a booking at this time.")

        conflict2 = db.query(Booking).filter(
            Booking.room_code == room_code,
            Booking.booking_date == booking_date,
            Booking.start_time < end_time,
            Booking.end_time > start_time,
            Booking.status.in_([BookingStatus.active, BookingStatus.checked_in])
        ).first()
        if conflict2:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "This room has already booked this time.")

        if start_time > end_time:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid time.")

        now = datetime.now()
        start = datetime.combine(booking_date, start_time)
        if start <= now:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cannot book this time.")

        booking = Booking(
            user_id=user_id,
            room_code=room_code,
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)

        delay_reminder = (start - timedelta(minutes=20) - now).total_seconds()
        if delay_reminder > 0:
            Timer(delay_reminder, lambda: event_subject.notify("checkin_reminder", {"booking_id": booking.id})).start()
        else:
            event_subject.notify("checkin_reminder", {"booking_id": booking.id})

        delay_timeout = (start + timedelta(minutes=5) - now).total_seconds()
        if delay_timeout > 0:
            Timer(delay_timeout, lambda: event_subject.notify("checkin_timeout", {"booking_id": booking.id})).start()
        else:
            event_subject.notify("checkin_timeout", {"booking_id": booking.id})

        end = datetime.combine(booking_date, end_time)
        delay_checkout = (end - now).total_seconds()
        if delay_checkout > 0:
            Timer(delay_checkout, lambda: event_subject.notify("auto_checkout", {"booking_id": booking.id})).start()
        else:
            event_subject.notify("auto_checkout", {"booking_id": booking.id})

        return booking

    @staticmethod
    def get_user_bookings(db: Session, user_id: int):
        bookings = db.query(Booking).filter(Booking.user_id == user_id).all()
        if not bookings:
            return []

        return bookings

    @staticmethod
    def cancel_booking(db: Session, booking_id: int, user_id: int):
        booking = db.query(Booking).filter(
            Booking.id == booking_id,
            Booking.user_id == user_id
        ).first()
        if not booking:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Booking not found.")

        if booking.status != BookingStatus.active:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cannot cancel this booking.")

        booking.status = BookingStatus.cancelled
        db.commit()
        db.refresh(booking)

        return booking

    @staticmethod
    def get_all_bookings(db: Session):
        bookings = db.query(Booking).all()
        if not bookings:
            return []

        return bookings

    @staticmethod
    def get_active_bookings(db: Session, user_id: int):
        bookings = db.query(Booking).filter(
            Booking.user_id == user_id,
            Booking.status.in_([BookingStatus.active, BookingStatus.checked_in])
        ).all()
        if not bookings:
            return []

        return bookings
