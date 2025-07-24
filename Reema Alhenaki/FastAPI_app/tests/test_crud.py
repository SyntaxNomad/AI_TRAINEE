import pytest
from sqlalchemy.orm import Session
from app import crud, schemas
from datetime import datetime

def create_sample_patient(db_session: Session):
    return crud.create_patient(db_session, schemas.PatientCreate(
        RegistrationDate=datetime(2024, 1, 1),
        FirstName="Reema",
        MiddleName="User",
        LastName="Example",
        Gender=1,
        DateofBirth=datetime(1995, 3, 10),
        NationalityID="SAU",
        FirstVisit=datetime(2024, 1, 1),
        LastVisit=datetime(2024, 1, 1),
        NoOfVisit=1,
        MobileNumber='511222333'
    ))

def test_create_patient(db_session: Session):
    patient = create_sample_patient(db_session)

    assert patient.PatientID is not None
    assert patient.FirstName == "Reema"
    assert patient.LastName == "Example"
    assert patient.MobileNumber == '511222333'
    assert isinstance(patient.DateofBirth, datetime)

def test_get_patient(db_session: Session):
    patient = create_sample_patient(db_session)

    fetched = crud.get_patient(db_session, patient.PatientID)
    assert fetched is not None
    assert fetched.PatientID == patient.PatientID
    assert fetched.FirstName == "Reema"

def test_update_patient(db_session: Session):
    patient = create_sample_patient(db_session)

    updated = crud.update_patient(db_session, patient.PatientID, schemas.PatientUpdate(
        FirstName="Updated", LastName="Person", MobileNumber='523456789'
    ))
    assert updated is not None
    assert updated.FirstName == "Updated"
    assert updated.LastName == "Person"
    assert updated.MobileNumber == '523456789'

def test_delete_patient(db_session: Session):
    patient = create_sample_patient(db_session)

    deleted = crud.delete_patient(db_session, patient.PatientID)
    assert deleted is not None
    assert deleted.PatientID == patient.PatientID

    # Confirm it's deleted from DB
    fetched = crud.get_patient(db_session, patient.PatientID)
    assert fetched is None
