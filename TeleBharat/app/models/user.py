# app/models/user.py
from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    gender = Column(String)
    contact_number = Column(String)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    
    # Relationship to Patient - this allows accessing patient data through user.patient
    patient = relationship("Patient", back_populates="user", uselist=False)
    
    # Relationship to Doctor - this allows accessing doctor data through user.doctor
    doctor = relationship("Doctor", back_populates="user", uselist=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}')>"
