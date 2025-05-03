from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api import auth_route, booking_route, checkin_route, room_route, admin_route, technician_route
from contextlib import asynccontextmanager
from app.observers.subject import event_subject
from app.observers.iot_observer import IotObserver
from app.observers.timeout_observer import TimeoutObserver

Base.metadata.create_all(bind=engine)
event_subject.attach(IotObserver())
event_subject.attach(TimeoutObserver())

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     iot_observer = IotObserver()
#     timeout_observer = TimeoutObserver()
#     event_subject.attach(iot_observer)
#     event_subject.attach(timeout_observer)
#     try:
#         yield
#     finally:
#         event_subject.detach(iot_observer)
#         event_subject.detach(timeout_observer)

app = FastAPI(
    title="S3-MRS",
    description="Smart Study Space Management and Reservation System at HCMUT.",
    docs_url="/docs",
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

app.include_router(auth_route.router, tags=["auth"])
app.include_router(booking_route.router, tags=["booking"])
app.include_router(checkin_route.router, tags=["checkin"])
app.include_router(room_route.router, tags=["rooms"])
app.include_router(admin_route.router, tags=["admin"])
app.include_router(technician_route.router, tags=["technicians"])
