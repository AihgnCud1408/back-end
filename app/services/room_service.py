from sqlalchemy.orm import Session
from app.models.room import Room

class RoomService:
    def get_all_rooms(self, db: Session):
        return db.query(Room).all()