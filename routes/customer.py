from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from auth.dependencies import (
    get_current_user,
    require_roles
)

from database import get_db

from schemas.customer_schema import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate
)

from services.customer_service import (
    CustomerService
)


router = APIRouter(prefix="/customers",tags=["Customers"])


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED
)
def create_customer(
    data: CustomerCreate,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            "Super Admin",
            "Tour Manager",
            "Booking Agent"
        )
    )
):

    return customer_service.create_customer(
        db,
        data
    )


@router.get(
    "",
    response_model=list[CustomerResponse]
)
def get_customers(
    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )
):

    return customer_service.get_customers(db)


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )
):

    return customer_service.get_customer(
        db,
        customer_id
    )


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: int,
    data: CustomerUpdate,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_roles(
            "Super Admin",
            "Tour Manager",
            "Booking Agent"
        )
    )
):

    return customer_service.update_customer(
        db,
        customer_id,
        data
    )

def search_customers(

    name: str | None = None,

    email: str | None = None,

    phone: str | None = None,

    page: int = 1,

    limit: int = 10,

    sort_by: str = "id",

    sort_order: str = "asc",

    db: Session = Depends(get_db)
):

    return customer_service.search_customers(

        db=db,

        name=name,

        email=email,

        phone=phone,

        page=page,

        limit=limit,

        sort_by=sort_by,

        sort_order=sort_order
    )


customer_service = CustomerService()