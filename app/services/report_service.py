import calendar
from datetime import date
from sqlalchemy.orm import Session
from app.models.booking import Booking, BookingStatus
from app.schemas.report_schema import ReportReadSchema

class ReportService:
    @staticmethod
    def count_bookings(db: Session, year: int, month: int):
        first_day = date(year, month, 1)
        last_day = date(year, month, calendar.monthrange(year, month)[1])
        total_bookings = db.query(Booking).filter(
            Booking.booking_date >= first_day,
            Booking.booking_date <= last_day
        ).count()

        total_completed = db.query(Booking).filter(
            Booking.booking_date >= first_day,
            Booking.booking_date <= last_day,
            Booking.status == BookingStatus.checked_out
        ).count()

        total_cancelled = db.query(Booking).filter(
            Booking.booking_date >= first_day,
            Booking.booking_date <= last_day,
            Booking.status == BookingStatus.cancelled
        ).count()

        return ReportReadSchema(
            year=year,
            month=month,
            total_bookings=total_bookings,
            total_completed=total_completed,
            total_cancelled=total_cancelled
        )
