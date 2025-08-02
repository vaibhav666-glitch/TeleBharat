from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr
    gender: str | None = None
    contact_number: str | None = None
    role: str

class UserCreate(UserBase):
    password_hash: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    gender: str | None = None
    contact_number: str | None = None
    role: str | None = None

class UserOut(UserBase):
    id: int
    
    class Config:
        from_attributes = True  # Updated for Pydantic v2