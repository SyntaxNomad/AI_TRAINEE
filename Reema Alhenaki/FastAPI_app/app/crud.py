from sqlalchemy.orm import Session
from app.models import HISPatient
from app.schemas import PatientCreate, PatientUpdate
import random
from datetime import datetime
from fastapi import HTTPException

def generate_unique_patient_id():
    return random.randint(100000, 999999)


def create_patient(db: Session, patient: PatientCreate):
    # Check for required fields 
    required_fields = {
        "FirstName": patient.FirstName,
        "LastName": patient.LastName,
        "Gender": patient.Gender,
        "DateofBirth": patient.DateofBirth,
        "NationalityID": patient.NationalityID,
    } 

    missing = [field for field, value in required_fields.items() if value is None]
    if missing:
        raise HTTPException(
            status_code=422,
            detail=f"The following required fields are missing or null: {', '.join(missing)}"
        )

    new_id = generate_unique_patient_id()
    while db.query(HISPatient).filter(HISPatient.PatientID == new_id).first():
        new_id = generate_unique_patient_id()

    now = datetime.now()

    db_patient = HISPatient(
        PatientID=new_id,
        FirstName=patient.FirstName,
        MiddleName=patient.MiddleName,
        LastName=patient.LastName,
        Gender=patient.Gender,
        DateofBirth=patient.DateofBirth,
        NationalityID=patient.NationalityID,
        RegistrationDate=now,
        FirstVisit=now,
        LastVisit=now,
        NoOfVisit=0,
        MobileNumber=int(patient.MobileNumber) if patient.MobileNumber else None,
    )

    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient





def get_patients(db: Session):
    return db.query(HISPatient).all()

def get_patient(db: Session, patient_id: int):
    return db.query(HISPatient).filter(HISPatient.PatientID == patient_id).first()

def update_patient(db: Session, patient_id: int, updates: PatientUpdate):
    patient = get_patient(db, patient_id)
    if not patient:
        return None
    update_data = updates.model_dump(exclude_unset=True)
    update_data = {k: v for k, v in update_data.items() if v is not None}


    for key, value in update_data.items():
        setattr(patient, key, value)
    db.commit()
    db.refresh(patient)
    return patient

def delete_patient(db: Session, patient_id: int):
    patient = get_patient(db, patient_id)
    if not patient:
        return None
    db.delete(patient)
    db.commit()
    return patient