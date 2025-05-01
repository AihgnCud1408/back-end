from sqlalchemy.orm import Session
from app.models.room import Room

class RoomService:
    @staticmethod
    def get_all_rooms(db: Session):
        return db.query(Room).all()