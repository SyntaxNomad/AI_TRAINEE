from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Dict
from app.routers import patient
from app.database import engine, Base
from app import models




app = FastAPI()

# Create all tables
Base.metadata.create_all(bind=engine)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail or "An error occurred"},
    )

@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    # Special handling for malformed JSON (e.g., number starting with 0)
    if any("JSON decode error" in str(e) for e in exc.errors()):
        return JSONResponse(
            status_code=422,
            content={
                "detail": "The data sent is not in the correct format. Check all fields are filled and in the right format and check for commas."
                          
            },
        )

    user_friendly_errors = []

    # Mapping known technical messages to readable ones
    def to_user_message(field: str, message: str) -> str:
        known: Dict[str, str] = {
            "Field contains a default placeholder value": f"{field} cannot be a placeholder like 'string'. Please enter real information.",
            "Field cannot be empty": f"{field} cannot be empty.",
        }
        return known.get(message, f"There is an issue with the field '{field}': {message}")

    for err in exc.errors():
        field = ".".join(str(loc) for loc in err["loc"] if loc != "body").capitalize()
        message = err["msg"]
        readable = to_user_message(field, message)
        user_friendly_errors.append(readable)

    return JSONResponse(
        status_code=422,
        content={"errors": user_friendly_errors},
    )


# Register your routers last
app.include_router(patient.router, prefix="/patients", tags=["Patients"])


