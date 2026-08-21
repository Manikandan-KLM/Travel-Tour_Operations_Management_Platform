from fastapi import FastAPI, Request

from database import Base, engine


from fastapi.exceptions import (
    RequestValidationError
)

from sqlalchemy.exc import (
    IntegrityError
)

from utils.exceptions import (

    validation_exception_handler,

    integrity_exception_handler
)

app = FastAPI()

app.add_exception_handler(

    RequestValidationError,

    validation_exception_handler
)


app.add_exception_handler(

    IntegrityError,

    integrity_exception_handler
)

from slowapi import (
    _rate_limit_exceeded_handler
)

from slowapi.errors import (
    RateLimitExceeded
)

from utils.rate_limit import (
    limiter
)

app.state.limiter = limiter

app.add_exception_handler(

    RateLimitExceeded,

    _rate_limit_exceeded_handler
)

# CROS configuration -------------------------------------

from fastapi.middleware.cors import (
    CORSMiddleware
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:3000",

        "http://127.0.0.1:3000"
    ],

    allow_credentials=True,

    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE"
    ],

    allow_headers=[
        "Authorization",
        "Content-Type"
    ]
)

from models.user_model import User
from models.destination_model import Destination
from models.package_model import TourPackage
from models.itinerary_model import Itinerary
from models.customer_model import Customer
from models.booking_model import Booking
from models.traveler_model import Traveler
from models.hotel_model import Hotel
from models.room_model import Room
from models.hotel_reservation_model import HotelReservation
from models.activity_model import Activity
from models.guide_model import Guide
from models.payment_model import Payment
from models.cancellation_model import Cancellation
from models.review_model import Review
from models.notification_model import Notification


from routes import auth
from routes import destination
from routes import package
from routes import itinerary
from routes import customer
from routes import travelers
from routes import bookings
from routes import hotels
from routes import rooms
from routes import hotel_reservations
from routes import activities
from routes import guides
from routes import payments
from routes import cancellations
from routes import reviews
from routes import notifications
from routes import dashboard
from routes import reports


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Travel & Tour Operations Management Platform",
    version="1.0.0"
)


app.include_router(auth.router)
app.include_router(destination.router)
app.include_router(package.router)
app.include_router(itinerary.router)
app.include_router(customer.router)
app.include_router(travelers.router)
app.include_router(bookings.router)
app.include_router(hotels.router)
app.include_router(rooms.router)
app.include_router(hotel_reservations.router)
app.include_router(activities.router)
app.include_router(guides.router)
app.include_router(payments.router)
app.include_router(cancellations.router)
app.include_router(reviews.router)
app.include_router(notifications.router)
app.include_router(dashboard.router)
app.include_router(reports.router)
# app.include_router(package_router,prefix="/api/v1")
# app.include_router(booking_router,prefix="/api/v1")



@app.get("/")
def root():
    return {
        "message": "Travel & Tour API is running"
    }


