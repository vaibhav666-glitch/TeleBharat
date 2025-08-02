from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.patient import Patient
from app.models.user import User
from app.schemas.patient_schema import PatientCreate, PatientOut, PatientUpdate, PatientBasicOut
from typing import List, Optional

router = APIRouter(prefix="/patients", tags=["Patients"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PatientOut)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == patient.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user is already a patient
    existing_patient = db.query(Patient).filter(Patient.id == patient.user_id).first()
    if existing_patient:
        raise HTTPException(status_code=400, detail="User is already registered as a patient")
    
    # Verify user role (optional - you might want to ensure only certain roles can be patients)
    if user.role not in ["patient", "user"]:  # Adjust based on your role system
        raise HTTPException(status_code=400, detail="User role is not eligible to be a patient")
    
    db_patient = Patient(
        id=patient.user_id,
        medical_record=patient.medical_record,
        diagnosis=patient.diagnosis
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.get("/", response_model=List[PatientOut])
def get_patients(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    diagnosis: Optional[str] = Query(None, description="Filter by diagnosis"),
    db: Session = Depends(get_db)
):
    query = db.query(Patient)
    
    if diagnosis:
        query = query.filter(Patient.diagnosis.ilike(f"%{diagnosis}%"))
    
    patients = query.offset(skip).limit(limit).all()
    return patients

@router.get("/user/{user_id}", response_model=PatientOut)
def get_patient_by_user_id(user_id: int, db: Session = Depends(get_db)):
    """Get patient record by user ID"""
    patient = db.query(Patient).filter(Patient.id == user_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient record not found for this user")
    return patient

@router.put("/{patient_id}", response_model=PatientOut)
def update_patient(patient_id: int, patient_update: PatientUpdate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    for key, value in patient_update.dict(exclude_unset=True).items():
        setattr(patient, key, value)
    
    db.commit()
    db.refresh(patient)
    return patient

@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.delete(patient)
    db.commit()
    return {"detail": "Patient record deleted successfully"}

@router.get("/search/", response_model=List[PatientOut])
def search_patients(
    name: Optional[str] = Query(None, description="Search by patient name"),
    email: Optional[str] = Query(None, description="Search by patient email"),
    diagnosis: Optional[str] = Query(None, description="Search by diagnosis"),
    db: Session = Depends(get_db)
):
    """Search patients by various criteria"""
    query = db.query(Patient).join(User)
    
    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    if diagnosis:
        query = query.filter(Patient.diagnosis.ilike(f"%{diagnosis}%"))
    
    patients = query.all()
    return patients

@router.get("/{patient_id}/basic", response_model=PatientBasicOut)
def get_patient_basic(patient_id: int, db: Session = Depends(get_db)):
    """Get patient record without user details (for privacy-sensitive contexts)"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient