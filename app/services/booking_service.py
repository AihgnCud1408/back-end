from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, time, date, timedelta
from app.models.booking import Booking, BookingStatus
from app.models.room import Room
from app.models.user import User
from app.schemas.booking_schema import BookingReadSchema
from threading import Timer
from app.observers.subject import event_subject

class BookingService:
    @staticmethod
    def create_booking(db: Session, user_id: int, room_id: int, booking_date: date, start_time: time, end_time: time):
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
            Booking.room_id == room_id,
            Booking.booking_date == booking_date,
            Booking.start_time < end_time,
            Booking.end_time > start_time,
            Booking.status.in_([BookingStatus.active, BookingStatus.checked_in])
        ).first()
        if conflict2:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "This room has already booked this time.")

        start = datetime.combine(booking_date, start_time)
        if start <= datetime.now():
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cannot book this time.")

        booking = Booking(
            user_id=user_id,
            room_id=room_id,
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)

        delay_reminder = (start - timedelta(minutes=20) - datetime.now()).total_seconds()
        if delay_reminder > 0:
            Timer(delay_reminder, lambda: event_subject.notify("checkin_reminder", {"booking_id": booking.id})).start()
        else:
            event_subject.notify("checkin_reminder", {"booking_id": booking.id})

        delay_timeout = (start + timedelta(minutes=5) - datetime.now()).total_seconds()
        if delay_timeout > 0:
            Timer(delay_timeout, lambda: event_subject.notify("checkin_timeout", {"booking_id": booking.id})).start()
        else:
            event_subject.notify("checkin_timeout", {"booking_id": booking.id})

        user_code = db.query(User.user_code).filter(User.id == user_id).scalar()
        room_code = db.query(Room.room_code).filter(Room.id == room_id).scalar()
        return BookingReadSchema(
            id=booking.id,
            user_code=user_code,
            room_code=room_code,
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time,
            status=booking.status,
            created_at=booking.created_at
        )

    @staticmethod
    def get_user_bookings(db: Session, user_id: int):
        bookings = db.query(Booking).filter(Booking.user_id == user_id).all()
        if not bookings:
            return []

        list_bookings = []
        user = db.query(User).filter(User.id == user_id).first()
        room_ids = {booking.room_id for booking in bookings}
        rooms = db.query(Room).filter(Room.id.in_(room_ids)).all()
        room_dict = {room.id: room for room in rooms}
        for booking in bookings:
            room = room_dict.get(booking.room_id)
            list_bookings.append(BookingReadSchema(
                id=booking.id,
                user_code=user.user_code,
                room_code=room.room_code,
                booking_date=booking.booking_date,
                start_time=booking.start_time,
                end_time=booking.end_time,
                status=booking.status,
                created_at=booking.created_at
            ))
        return list_bookings

    @staticmethod
    def cancel_booking(db: Session, booking_id: int, user_id: int):
        result = None
        try:
            booking = db.query(Booking).filter(
                Booking.id == booking_id,
                Booking.user_id == user_id
            ).first()
            if booking.status != BookingStatus.active:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cannot cancel this booking")

            booking.status = BookingStatus.cancelled
            db.commit()
            db.refresh(booking)

            user = db.query(User).filter(User.id == user_id).first()
            room = db.query(Room).filter(Room.id == booking.room_id).first()
            result = BookingReadSchema(
                id=booking.id,
                user_code=user.user_code,
                room_code=room.room_code,
                booking_date=booking.booking_date,
                start_time=booking.start_time,
                end_time=booking.end_time,
                status=booking.status,
                created_at=booking.created_at
            )
        finally:
            return result

    @staticmethod
    def get_all_bookings(db: Session):
        bookings = db.query(Booking).all()
        if not bookings:
            return []

        list_bookings = []
        room_ids = {booking.room_id for booking in bookings}
        rooms = db.query(Room).filter(Room.id.in_(room_ids)).all()
        room_dict = {room.id: room for room in rooms}
        user_ids = {booking.user_id for booking in bookings}
        users = db.query(User).filter(User.id.in_(user_ids)).all()
        user_dict = {user.id: user for user in users}
        for booking in bookings:
            room = room_dict.get(booking.room_id)
            user = user_dict.get(booking.user_id)
            list_bookings.append(BookingReadSchema(
                id=booking.id,
                user_code=user.user_code,
                room_code=room.room_code,
                booking_date=booking.booking_date,
                start_time=booking.start_time,
                end_time=booking.end_time,
                status=booking.status,
                created_at=booking.created_at
            ))
        return list_bookings

