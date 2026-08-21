# Travel Platform Management System

A Travel Platform Management System built using FastAPI and SQLAlchemy.

This project helps manage travel packages, customers, bookings, travelers, hotels, rooms, payments, tour guides, reviews, cancellations, refunds, and reports.

## Features

- User Authentication
- JWT Authentication
- Role-Based Access Control
- Customer Management
- Destination Management
- Travel Package Management
- Booking Management
- Traveler Management
- Hotel and Room Management
- Activity Management
- Tour Guide Management
- Payment Management
- Cancellation and Refund Management
- Reviews and Ratings
- Search, Filtering and Pagination
- Notifications and Background Tasks
- Admin Dashboard and Reports
- Database Transactions
- Soft Delete
- Audit Logs
- Rate Limiting
- Redis Caching
- QR Code Generation
- PDF Booking Confirmation
- Excel Report Export
- API Versioning
- Unit and Integration Tests

## Technologies Used

- Python 3.10+
- FastAPI
- SQLAlchemy ORM
- PostgreSQL / SQLite
- JWT Authentication
- Alembic
- Redis
- Celery
- Docker
- Pytest
- Uvicorn

## Project Structure

```text
Travel & Tour_Operations_Management_Platform/
├── main.py
├── database.py
├── config.py
│
├── models/
│   ├── user.py
│   ├── customer.py
│   ├── destination.py
│   ├── package.py
│   ├── booking.py
│   ├── traveler.py
│   ├── hotel.py
│   ├── room.py
│   ├── payment.py
│   ├── guide.py
│   └── review.py
│
├── schemas/
├── routes/
├── services/
├── repositories/
│
├── auth/
│   ├── jwt.py
│   ├── dependencies.py
│   └── password.py
│
├── cache/
├── tasks/
├── reports/
├── websocket/
├── utils/
└── tests/

alembic/
.github/
requirements.txt
docker-compose.yml
Dockerfile
README.md