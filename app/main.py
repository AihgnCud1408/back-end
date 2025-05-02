from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
<<<<<<< HEAD
from app.api import auth_route, booking_route, checkin_route, room_route, admin_route
=======
from app.api import auth_route, booking_route, checkin_route, room_route, manage_room_route,device_route
>>>>>>> 002a571b72a84d3fa1537a12958d3347c5cea181
from contextlib import asynccontextmanager
from app.observers.subject import event_subject
from app.observers.iot_observer import IotObserver
from app.observers.timeout_observer import TimeoutObserver

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    event_subject.attach(IotObserver())
    event_subject.attach(TimeoutObserver())
    try:
        yield
    finally:
        event_subject.detach(IotObserver())
        event_subject.detach(TimeoutObserver())

app = FastAPI(
    title="S3-MRS",
    description="Smart Study Space Management and Reservation System at HCMUT.",
    docs_url="/docs",
    lifespan=lifespan
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
<<<<<<< HEAD
app.include_router(admin_route.router, tags=["admin"])
=======
app.include_router(manage_room_route.router, tags=["manage"])
app.include_router(device_route.router, tags=["device"])
>>>>>>> 002a571b72a84d3fa1537a12958d3347c5cea181
