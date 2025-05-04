from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api import auth_route, booking_route, checkin_route, room_route, admin_route, technician_route, it_route
from contextlib import asynccontextmanager
from app.observers.subject import event_subject
from app.observers.checkin_observer import CheckinObserver
from app.observers.timeout_observer import TimeoutObserver
from app.observers.reminder_observer import ReminderObserver
from app.observers.auto_checkout_observer import AutoCheckoutObserver

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    iot_observer = CheckinObserver()
    timeout_observer = TimeoutObserver()
    reminder_observer = ReminderObserver()
    auto_checkout_observer = AutoCheckoutObserver()

    event_subject.attach(iot_observer)
    event_subject.attach(timeout_observer)
    event_subject.attach(reminder_observer)
    event_subject.attach(auto_checkout_observer)
    print("Observers attached.")

    try:
        yield
    finally:
        event_subject.detach(iot_observer)
        event_subject.detach(timeout_observer)
        event_subject.detach(reminder_observer)
        event_subject.detach(auto_checkout_observer)
        print("Observers detached.")

app = FastAPI(
    title="S3-MRS",
    description="Smart Study Space Management and Reservation System at HCMUT.",
    docs_url="/docs",
    lifespan=lifespan
)

app.include_router(auth_route.router, tags=["auth"])
app.include_router(booking_route.router, tags=["booking"])
app.include_router(checkin_route.router, tags=["checkin"])
app.include_router(room_route.router, tags=["room"])
app.include_router(admin_route.router, tags=["admin"])
app.include_router(technician_route.router, tags=["technicians"])
app.include_router(it_route.router, tags=["it"])

# for r in app.router.routes:
#     print(r.path, r.methods, getattr(r, "endpoint", r))
