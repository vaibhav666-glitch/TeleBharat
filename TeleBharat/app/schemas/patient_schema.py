from pydantic import BaseModel
from typing import Optional
from app.schemas.user_schema import UserOut

class PatientBase(BaseModel):
    medical_record: Optional[str] = None
    diagnosis: Optional[str] = None

class PatientCreate(PatientBase):
    user_id: int  # Reference to existing user

class PatientUpdate(BaseModel):
    medical_record: Optional[str] = None
    diagnosis: Optional[str] = None

class PatientOut(PatientBase):
    id: int
    user: UserOut  # Include full user details
    
    class Config:
        from_attributes = True

class PatientBasicOut(PatientBase):
    id: int
    
    class Config:
        from_attributes = True