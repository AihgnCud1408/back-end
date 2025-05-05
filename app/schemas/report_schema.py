from pydantic import BaseModel

class ReportReadSchema(BaseModel):
    year: int
    month: int
    total_bookings: int
    total_completed: int
    total_cancelled: int
    total_rooms: int