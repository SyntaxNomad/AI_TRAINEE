from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

router = APIRouter()

#CREATE Method
@router.post("/", response_model=schemas.PatientRead)
def create(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient)


#READ Method
@router.get("/", response_model=list[schemas.PatientRead])
def read_all(db: Session = Depends(get_db)):
    return crud.get_patients(db)

@router.get("/{patient_id}", response_model=schemas.PatientRead)
def read_one(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient with this ID does not exist.")
    return patient


#UPDATE Method
@router.put("/{patient_id}", response_model=schemas.PatientRead)
def update(patient_id: int, updates: schemas.PatientUpdate, db: Session = Depends(get_db)):
    updated = crud.update_patient(db, patient_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Cannot update: patient not found.")
    return updated


@router.delete("/{patient_id}", response_model=schemas.PatientRead)
def delete_patient_route(patient_id: int, db: Session = Depends(get_db)):
    try:
        deleted = crud.delete_patient(db, patient_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Cannot delete: patient not found.")
        return deleted
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
