from app.observers.subject import Observer
from app.observers.singleton import SingletonMeta
from app.db.session import SessionLocal
from app.models.booking import Booking
from app.models.user import User
from app.services.mail_service import send_email

class ReminderObserver(Observer, metaclass=SingletonMeta):
    def update(self, event: str, data: dict):
        if event != "checkin_reminder":
            return

        booking_id = data.get("booking_id")
        if not booking_id:
            return

        db = SessionLocal()
        try:
            booking = db.query(Booking).filter(Booking.id == booking_id).first()
            user = db.query(User).filter(User.id == booking.user_id).first()
            subject = "Sắp đến giờ check-in"
            body = f"""
                <p>Chào {user.name},</p>
                <p>Bạn có booking <strong>#{booking.id}</strong> vào
                <strong>{booking.booking_date} lúc {booking.start_time.strftime('%H:%M')}</strong>.</p>
                <p>Vui lòng đến trước giờ để hoàn tất thủ tục check-in.</p>
            """
            send_email(user.email, subject, body)
        finally:
            db.close()
