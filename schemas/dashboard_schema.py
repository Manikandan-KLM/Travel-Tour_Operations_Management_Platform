from pydantic import BaseModel


class DashboardResponse(BaseModel):

    total_customers: int

    total_packages: int

    active_tours: int

    total_bookings: int

    confirmed_bookings: int

    cancelled_bookings: int

    total_revenue: float

    total_refunds: float