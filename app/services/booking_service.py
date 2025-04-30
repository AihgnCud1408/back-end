from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks
from datetime import datetime, timedelta
from app.models.booking import Booking, BookingStatus
from app.models.room import Room
from threading import Timer
from app.observers.subject import event_subject
from app.services.notification_service import get_notification_service

class BookingService:
    @staticmethod
    def create_booking(db: Session, user_code: int, room_id: int, start_time: datetime, end_time: datetime):
        # now = datetime.now()
        # if start_time <= now:
        #     raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cannot booking at this time")
        if start_time >= end_time:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Start time must be before end time")

        conflict = db.query(Booking).filter(
            Booking.room_id == room_id,
            Booking.status == BookingStatus.active,
            Booking.start_time < end_time,
            Booking.end_time > start_time
        ).first()
        if conflict:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Room is already booked")

        booking = Booking(
            user_code=user_code,
            room_id=room_id,
            start_time=start_time,
            end_time=end_time
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)

        Timer(30*60, lambda: event_subject.notify(db, "checkin_timeout", {"booking_id": booking.id})).start()

        return booking

    @staticmethod
    def get_user_bookings(db: Session, user_code: int):
        return db.query(Booking).filter(Booking.user_code == user_code).all()

    @staticmethod
    def cancel_booking(db: Session, booking_id: int, user_code: int):
        booking = db.query(Booking).filter(
            Booking.id == booking_id,
            Booking.user_code == user_code
        ).first()
        if not booking:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Booking not found")
        if booking.status != BookingStatus.active:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cannot cancel this booking")
        booking.status = BookingStatus.cancelled
        db.commit()
        db.refresh(booking)
        return booking

    @staticmethod
    def schedule_reminder(db: Session, booking: Booking, background_tasks: BackgroundTasks):
        remind_at = booking.start_time - timedelta(minutes=20)
        delay = (remind_at - datetime.now()).total_seconds()
        if delay > 0:
            background_tasks.add_task(
                BookingService._send_reminder,
                db,
                booking.user_code,
                booking.id,
                booking.room_id,
                delay
            )

    @staticmethod
    def _send_reminder(db: Session, user_code: int, booking_id: int, room_id: int, delay: float):
        import time
        time.sleep(delay)
        room = db.query(Room).filter(Room.id == room_id).first()
        get_notification_service().send_message(
            queue_name=f"reminder_queue_{user_code}",
            payload={
                "booking_id": booking_id,
                "room_code": room.room_code
            }
        )
