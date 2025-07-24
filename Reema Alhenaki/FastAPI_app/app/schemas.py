from pydantic import BaseModel, Field, field_validator
from typing import Optional
import datetime


def validate_placeholder(value: str) -> str:
    """
    Ensures value is not empty, default, or placeholder string.
    """
    if not value.strip() or value.strip().lower() in {"default", "string"}:
        raise ValueError("Field contains an invalid placeholder value")
    return value


def validate_mobile(value: str) -> str:
    """
    Validates Saudi-style mobile numbers (must start with '5', not '0', 9 digits).
    """
    if value in {"default", "string", ""}:
        raise ValueError("Mobile number cannot be a placeholder")
    if value.startswith("0"):
        raise ValueError("Mobile number must not start with 0")
    if not value.startswith("5"):
        raise ValueError("Mobile number must start with 5")
    if not value.isdigit():
        raise ValueError("Mobile number must contain digits only")
    if len(value) != 9:
        raise ValueError("Mobile number must be 9 digits")
    return value


# ---------------------------
# Create Schema
# ---------------------------

class PatientCreate(BaseModel):
    RegistrationDate: datetime.datetime
    FirstName: str
    MiddleName: str
    LastName: str
    Gender: int
    DateofBirth: datetime.datetime
    NationalityID: str = Field(..., description="Nationality code, e.g., 'SAU'")
    FirstVisit: datetime.datetime
    LastVisit: datetime.datetime
    NoOfVisit: int
    MobileNumber: str

    # Name Validation
    @field_validator("FirstName", "MiddleName", "LastName")
    @classmethod
    def validate_names(cls, value: str):
        return validate_placeholder(value)

    # Mobile Validation
    @field_validator("MobileNumber")
    @classmethod
    def validate_mobile_number(cls, value: str):
        return validate_mobile(value)

    # DOB Validation
    @field_validator("DateofBirth")
    @classmethod
    def validate_date_of_birth(cls, value: datetime.datetime):
        now = datetime.datetime.now()
        if value.replace(tzinfo=None) > now:
            raise ValueError("Date of birth cannot be in the future")
        return value

    # Nationality Validation
    @field_validator("NationalityID")
    @classmethod
    def validate_nationality_id(cls, value: str):
        value = validate_placeholder(value)
        if any(char.isdigit() for char in value):
            raise ValueError("NationalityID can not contain digits, only letters.")
        if len(value) != 3:
            raise ValueError("NationalityID must be 3 characters.")
        return value



class PatientUpdate(BaseModel):
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    MobileNumber: Optional[str] = None

    @field_validator("FirstName", "LastName")
    @classmethod
    def validate_update_names(cls, value: Optional[str]):
        # Skip update if None, "string", or empty string
        if value is None or value.strip().lower() in {"string", "default", ""}:
            return None
        return validate_placeholder(value)

    @field_validator("MobileNumber")
    @classmethod
    def validate_update_mobile(cls, value: Optional[str]):
        # Skip update if None, "string", or empty string
        if value is None or value.strip().lower() in {"string", "default", ""}:
            return None
        return validate_mobile(value)



class PatientRead(BaseModel):
    PatientID: int
    FirstName: str
    MiddleName: str
    LastName: str
    Gender: int
    DateofBirth: datetime.datetime
    NationalityID: str
    RegistrationDate: datetime.datetime
    FirstVisit: datetime.datetime
    LastVisit: datetime.datetime
    NoOfVisit: int
    MobileNumber: str
    EmailAddress: Optional[str]
    IsPregnant: Optional[int]
    BloodGroup: Optional[int]
    RHFactor: Optional[str]
    RegisteredDoctor: Optional[int]
    EmergencyContactName: Optional[str]
    EmergencyContactNo: Optional[int]

    class Config:
        from_attributes = True
