
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import datetime

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
    MobileNumber: int

    @field_validator("FirstName", "MiddleName", "LastName")
    @classmethod
    def name_must_not_be_default_or_empty(cls, v):
        if not v.strip():
            raise ValueError("Field must not be empty")
        if v.strip().lower() in {"default", "string"}:
            raise ValueError("Field contains a default placeholder value")
        return v

    @field_validator("MobileNumber")
    @classmethod
    def mobile_validation(cls, v):
        v_str = str(v)
        if v_str.startswith("0"):
            raise ValueError("Mobile number must not start with 0")
        if not v_str.isdigit():
            raise ValueError("Mobile number must contain digits only")
        if len(v_str) != 9:
            raise ValueError("Mobile number must be 9 digits")
        return int(v_str)

  
    @field_validator("DateofBirth")
    @classmethod
    def date_not_in_future(cls, v):
        now = datetime.datetime.now()
        if v.replace(tzinfo=None) > now:
            raise ValueError("Date of birth cannot be in the future")
        return v



    @field_validator("NationalityID")
    @classmethod
    def validate_nationality_id(cls, v):
        if v.lower() == "string":
            raise ValueError("NationalityID contains a default placeholder value.")
        if len(v) > 3:
            raise ValueError("NationalityID must be at most 3 characters.")
        return v


from pydantic import BaseModel, field_validator
from typing import Optional

class PatientUpdate(BaseModel):
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    MobileNumber: Optional[int] = None

    @field_validator("FirstName", "LastName")
    @classmethod
    def name_validation(cls, v):
        if v is None:
            return v
        v_str = v.strip().lower()
        if v_str in {"default", "string", ""}:
            # Treat this like it was never provided (i.e. skip updating)
            return None
        return v

    @field_validator("MobileNumber")
    @classmethod
    def mobile_validation(cls, v):
        if v is None or v == 0:
            # Treat 0 as no update
            return None
        v_str = str(v)
        if not v_str.isdigit():
            raise ValueError("Mobile number must contain digits only")
        if v_str.startswith("0"):
            raise ValueError("Mobile number must not start with 0")
        if len(v_str) != 9:
            raise ValueError("Mobile number must be 9 digits")
        return int(v_str)


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
    MobileNumber: int
    EmailAddress: Optional[str]
    IsPregnant: Optional[int]
    BloodGroup: Optional[int]
    RHFactor: Optional[str]
    RegisteredDoctor: Optional[int]
    EmergencyContactName: Optional[str]
    EmergencyContactNo: Optional[int]

    class Config:
        from_attributes = True
