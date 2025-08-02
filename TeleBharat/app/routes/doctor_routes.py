from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.doctor import Doctor
from app.models.user import User
from app.schemas.doctor_schema import DoctorCreate, DoctorOut, DoctorUpdate, DoctorBasicOut
from typing import List, Optional

router = APIRouter(prefix="/doctors", tags=["Doctors"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=DoctorOut)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == doctor.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user is already a doctor
    existing_doctor = db.query(Doctor).filter(Doctor.id == doctor.user_id).first()
    if existing_doctor:
        raise HTTPException(status_code=400, detail="User is already registered as a doctor")
    
    # Verify user role (optional - you might want to ensure only certain roles can be doctors)
    if user.role not in ["doctor", "physician", "medical_professional"]:  # Adjust based on your role system
        raise HTTPException(status_code=400, detail="User role is not eligible to be a doctor")
    
    # Check if license number is already taken (if provided)
    if doctor.license_number:
        existing_license = db.query(Doctor).filter(Doctor.license_number == doctor.license_number).first()
        if existing_license:
            raise HTTPException(status_code=400, detail="License number already registered")
    
    db_doctor = Doctor(
        id=doctor.user_id,
        specialization=doctor.specialization,
        license_number=doctor.license_number
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@router.get("/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.get("/", response_model=List[DoctorOut])
def get_doctors(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    specialization: Optional[str] = Query(None, description="Filter by specialization"),
    db: Session = Depends(get_db)
):
    query = db.query(Doctor)
    
    if specialization:
        query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))
    
    doctors = query.offset(skip).limit(limit).all()
    return doctors

@router.get("/user/{user_id}", response_model=DoctorOut)
def get_doctor_by_user_id(user_id: int, db: Session = Depends(get_db)):
    """Get doctor record by user ID"""
    doctor = db.query(Doctor).filter(Doctor.id == user_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor record not found for this user")
    return doctor

@router.get("/license/{license_number}", response_model=DoctorOut)
def get_doctor_by_license(license_number: str, db: Session = Depends(get_db)):
    """Get doctor by license number"""
    doctor = db.query(Doctor).filter(Doctor.license_number == license_number).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found with this license number")
    return doctor

@router.put("/{doctor_id}", response_model=DoctorOut)
def update_doctor(doctor_id: int, doctor_update: DoctorUpdate, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Check license number uniqueness if being updated
    if doctor_update.license_number and doctor_update.license_number != doctor.license_number:
        existing_license = db.query(Doctor).filter(Doctor.license_number == doctor_update.license_number).first()
        if existing_license:
            raise HTTPException(status_code=400, detail="License number already registered")
    
    for key, value in doctor_update.dict(exclude_unset=True).items():
        setattr(doctor, key, value)
    
    db.commit()
    db.refresh(doctor)
    return doctor

@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db.delete(doctor)
    db.commit()
    return {"detail": "Doctor record deleted successfully"}

@router.get("/search/", response_model=List[DoctorOut])
def search_doctors(
    name: Optional[str] = Query(None, description="Search by doctor name"),
    email: Optional[str] = Query(None, description="Search by doctor email"),
    specialization: Optional[str] = Query(None, description="Search by specialization"),
    license_number: Optional[str] = Query(None, description="Search by license number"),
    db: Session = Depends(get_db)
):
    """Search doctors by various criteria"""
    query = db.query(Doctor).join(User)
    
    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    if specialization:
        query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))
    if license_number:
        query = query.filter(Doctor.license_number.ilike(f"%{license_number}%"))
    
    doctors = query.all()
    return doctors

@router.get("/specializations/", response_model=List[str])
def get_specializations(db: Session = Depends(get_db)):
    """Get all unique specializations"""
    specializations = db.query(Doctor.specialization).distinct().all()
    return [spec[0] for spec in specializations if spec[0]]

@router.get("/{doctor_id}/basic", response_model=DoctorBasicOut)
def get_doctor_basic(doctor_id: int, db: Session = Depends(get_db)):
    """Get doctor record without user details (for privacy-sensitive contexts)"""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor