from pydantic import BaseModel
from typing import Optional
from app.schemas.user_schema import UserOut

class DoctorBase(BaseModel):
    specialization: str
    license_number: Optional[str] = None

class DoctorCreate(DoctorBase):
    user_id: int  # Reference to existing user

class DoctorUpdate(BaseModel):
    specialization: Optional[str] = None
    license_number: Optional[str] = None

class DoctorOut(DoctorBase):
    id: int
    user: UserOut  # Include full user details
    
    class Config:
        from_attributes = True

class DoctorBasicOut(DoctorBase):
    id: int
    
    class Config:
        from_attributes = True