from fastapi import Request

from fastapi.responses import JSONResponse

from fastapi.exceptions import (
    RequestValidationError
)

from sqlalchemy.exc import (
    IntegrityError
)

# VALIDATION ERROR ---------------------------------------------------------

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    return JSONResponse(

        status_code=422,

        content={

            "success": False,

            "message":
                "Validation error",

            "errors":
                exc.errors()
        }
    )


# INTEGRITY ERROR --------------------------------------------------------------

async def integrity_exception_handler(
    request: Request,
    exc: IntegrityError
):

    return JSONResponse(

        status_code=400,

        content={

            "success": False,

            "message":
                "Database integrity error"
        }
    )

