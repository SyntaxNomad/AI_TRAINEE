from sqlalchemy.orm import Session
from app.models import HISPatient
from app.schemas import PatientCreate, PatientUpdate
from datetime import datetime
from fastapi import HTTPException
import app.models



def create_patient(db: Session, patient: PatientCreate):
    
    now = datetime.now()
    db_patient = HISPatient(
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
        MobileNumber= patient.MobileNumber if patient.MobileNumber else None,
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

    # Check if patient has appointments
    appointments = db.query(app.models.t_HIS_Appointment).filter(
        app.models.t_HIS_Appointment.c.PatientID == patient_id
    ).first()

    if appointments:
        raise HTTPException(status_code=400, detail="Cannot delete: patient has appointments.")

    # If no appointments, delete
    db.delete(patient)
    db.commit()
    return patient
