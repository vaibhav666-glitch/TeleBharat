from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from enum import Enum
from app.schemas.patient_schema import PatientBasicOut
from app.schemas.doctor_schema import DoctorBasicOut

class AppointmentStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"

class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    duration_minutes: Optional[int] = 30
    reason: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    @validator('appointment_date')
    def validate_future_date(cls, v):
        if v <= datetime.utcnow():
            raise ValueError('Appointment date must be in the future')
        return v
    
    @validator('duration_minutes')
    def validate_duration(cls, v):
        if v and (v < 15 or v > 180):
            raise ValueError('Duration must be between 15 and 180 minutes')
        return v

class AppointmentUpdate(BaseModel):
    appointment_date: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    status: Optional[AppointmentStatus] = None
    reason: Optional[str] = None
    notes: Optional[str] = None
    
    @validator('appointment_date')
    def validate_future_date(cls, v):
        if v and v <= datetime.utcnow():
            raise ValueError('Appointment date must be in the future')
        return v

class AppointmentOut(AppointmentBase):
    id: int
    status: AppointmentStatus
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    patient: PatientBasicOut
    doctor: DoctorBasicOut
    
    class Config:
        from_attributes = True

class AppointmentBasicOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    duration_minutes: int
    status: AppointmentStatus
    reason: Optional[str] = None
    
    class Config:
        from_attributes = True

# WebSocket message schemas
class NotificationMessage(BaseModel):
    type: str  # "appointment_created", "appointment_updated", "doctor_status"
    message: str
    data: dict
    timestamp: datetime = datetime.utcnow()

class DoctorStatusUpdate(BaseModel):
    doctor_id: int
    status: str  # "online", "offline", "busy"
    last_seen: datetime = datetime.utcnow()