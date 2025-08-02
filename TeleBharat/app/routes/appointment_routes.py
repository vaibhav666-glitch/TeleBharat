from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.appointment import Appointment, AppointmentStatus
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.schemas.appointment_schema import (
    AppointmentCreate, AppointmentOut, AppointmentUpdate, 
    AppointmentBasicOut, DoctorStatusUpdate
)
from app.websocket.manager import manager
from typing import List, Optional
from datetime import datetime, timedelta
import json

router = APIRouter(prefix="/appointments", tags=["Appointments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# WebSocket endpoint for real-time notifications
@router.websocket("/ws/{user_type}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_type: str, user_id: int):
    await manager.connect(websocket, user_type, user_id)
    try:
        while True:
            # Keep connection alive and listen for client messages
            data = await websocket.receive_text()
            
            # Handle different types of messages from client
            try:
                message = json.loads(data)
                
                # Handle doctor status updates
                if message.get("type") == "status_update" and user_type == "doctors":
                    status = message.get("status", "online")
                    await manager.update_doctor_status(user_id, status)
                    
            except json.JSONDecodeError:
                # If not JSON, treat as simple message
                pass
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_type, user_id)
        
        # If doctor disconnects, mark as offline
        if user_type == "doctors":
            await manager.update_doctor_status(user_id, "offline")

# WebSocket endpoint for general notifications
@router.websocket("/ws/general")
async def general_websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "general")
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, "general")

@router.post("/", response_model=AppointmentOut)
async def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    # Verify patient exists
    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Verify doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Check for conflicting appointments
    conflicting_appointment = db.query(Appointment).filter(
        Appointment.doctor_id == appointment.doctor_id,
        Appointment.appointment_date <= appointment.appointment_date + timedelta(minutes=appointment.duration_minutes),
        Appointment.appointment_date + timedelta(minutes=30) > appointment.appointment_date,  # Assuming default 30 min
        Appointment.status.in_([AppointmentStatus.CONFIRMED, AppointmentStatus.PENDING])
    ).first()
    
    if conflicting_appointment:
        raise HTTPException(status_code=400, detail="Doctor already has an appointment at this time")
    
    # Create appointment
    db_appointment = Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    
    # Send real-time notification
    await manager.notify_appointment_update({
        "id": db_appointment.id,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "appointment_date": appointment.appointment_date.isoformat(),
        "status": db_appointment.status.value
    }, "created")
    
    return db_appointment

@router.get("/{appointment_id}", response_model=AppointmentOut)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.get("/", response_model=List[AppointmentOut])
def get_appointments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[AppointmentStatus] = Query(None),
    patient_id: Optional[int] = Query(None),
    doctor_id: Optional[int] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Appointment)
    
    if status:
        query = query.filter(Appointment.status == status)
    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)
    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)
    if date_from:
        query = query.filter(Appointment.appointment_date >= date_from)
    if date_to:
        query = query.filter(Appointment.appointment_date <= date_to)
    
    appointments = query.offset(skip).limit(limit).all()
    return appointments

@router.get("/patient/{patient_id}", response_model=List[AppointmentOut])
def get_patient_appointments(
    patient_id: int,
    status: Optional[AppointmentStatus] = Query(None),
    upcoming_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    """Get all appointments for a specific patient"""
    query = db.query(Appointment).filter(Appointment.patient_id == patient_id)
    
    if status:
        query = query.filter(Appointment.status == status)
    if upcoming_only:
        query = query.filter(Appointment.appointment_date >= datetime.utcnow())
    
    appointments = query.order_by(Appointment.appointment_date).all()
    return appointments

@router.get("/doctor/{doctor_id}", response_model=List[AppointmentOut])
def get_doctor_appointments(
    doctor_id: int,
    status: Optional[AppointmentStatus] = Query(None),
    date: Optional[datetime] = Query(None),
    upcoming_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    """Get all appointments for a specific doctor"""
    query = db.query(Appointment).filter(Appointment.doctor_id == doctor_id)
    
    if status:
        query = query.filter(Appointment.status == status)
    if date:
        # Get appointments for specific date
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        query = query.filter(
            Appointment.appointment_date >= start_of_day,
            Appointment.appointment_date < end_of_day
        )
    if upcoming_only:
        query = query.filter(Appointment.appointment_date >= datetime.utcnow())
    
    appointments = query.order_by(Appointment.appointment_date).all()
    return appointments

@router.put("/{appointment_id}", response_model=AppointmentOut)
async def update_appointment(
    appointment_id: int, 
    appointment_update: AppointmentUpdate, 
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # If updating appointment date, check for conflicts
    if appointment_update.appointment_date:
        conflicting_appointment = db.query(Appointment).filter(
            Appointment.doctor_id == appointment.doctor_id,
            Appointment.id != appointment_id,  # Exclude current appointment
            Appointment.appointment_date <= appointment_update.appointment_date + timedelta(minutes=appointment.duration_minutes),
            Appointment.appointment_date + timedelta(minutes=30) > appointment_update.appointment_date,
            Appointment.status.in_([AppointmentStatus.CONFIRMED, AppointmentStatus.PENDING])
        ).first()
        
        if conflicting_appointment:
            raise HTTPException(status_code=400, detail="Doctor already has an appointment at this time")
    
    # Update appointment
    for key, value in appointment_update.dict(exclude_unset=True).items():
        setattr(appointment, key, value)
    
    appointment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(appointment)
    
    # Send real-time notification
    await manager.notify_appointment_update({
        "id": appointment.id,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "appointment_date": appointment.appointment_date.isoformat(),
        "status": appointment.status.value
    }, "updated")
    
    return appointment

@router.delete("/{appointment_id}")
async def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Instead of deleting, mark as cancelled
    appointment.status = AppointmentStatus.CANCELLED
    appointment.updated_at = datetime.utcnow()
    db.commit()
    
    # Send real-time notification
    await manager.notify_appointment_update({
        "id": appointment.id,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "appointment_date": appointment.appointment_date.isoformat(),
        "status": appointment.status.value
    }, "cancelled")
    
    return {"detail": "Appointment cancelled successfully"}

# Doctor status endpoints
@router.get("/doctor/{doctor_id}/status")
def get_doctor_status(doctor_id: int):
    """Get current online status of a doctor"""
    status = manager.get_doctor_status(doctor_id)
    return status

@router.post("/doctor/{doctor_id}/status")
async def update_doctor_status(doctor_id: int, status_update: DoctorStatusUpdate):
    """Update doctor status manually"""
    await manager.update_doctor_status(doctor_id, status_update.status)
    return {"detail": f"Doctor status updated to {status_update.status}"}