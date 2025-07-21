import pytest
from pydantic import ValidationError
from app.schemas import PatientCreate
from datetime import datetime

def test_invalid_nationality():
    with pytest.raises(ValidationError) as exc_info:
        PatientCreate(
            RegistrationDate=datetime.now(),
            FirstName="F",
            MiddleName="M",
            LastName="L",
            Gender=1,
            DateofBirth=datetime.now(),
            NationalityID="Saudi",  # More than 3 characters, too long
            FirstVisit=datetime.now(),
            LastVisit=datetime.now(),
            NoOfVisit=0,
            MobileNumber="123456789"
        )
    assert "NationalityID must be at most 3 characters" in str(exc_info.value)

def test_mobile_starts_with_zero():
    with pytest.raises(ValidationError) as exc_info:
        PatientCreate(
            RegistrationDate=datetime.now(),
            FirstName="F",
            MiddleName="M",
            LastName="L",
            Gender=1,
            DateofBirth=datetime.now(),
            NationalityID="SAU",
            FirstVisit=datetime.now(),
            LastVisit=datetime.now(),
            NoOfVisit=0,
            MobileNumber="012345678"  # starts with zero
        )
    assert "Mobile number must not start with 0" in str(exc_info.value)

def test_mobile_starts_with_zero():
    with pytest.raises(ValidationError) as exc_info:
        PatientCreate(
            RegistrationDate=datetime.now(),
            FirstName="F",
            MiddleName="M",
            LastName="L",
            Gender=1,
            DateofBirth=datetime.now(),
            NationalityID="SAU",
            FirstVisit=datetime.now(),
            LastVisit=datetime.now(),
            NoOfVisit=0,
            MobileNumber=12345678  # Only 8 digits
        )
    assert "Mobile number must be 9 digits" in str(exc_info.value)
