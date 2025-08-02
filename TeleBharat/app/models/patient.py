# Updated Patient Model
from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    medical_record = Column(String)
    diagnosis = Column(String)
    
    # Relationships
    user = relationship("User", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")
    
    def __repr__(self):
        return f"<Patient(id={self.id}, diagnosis='{self.diagnosis}')>"

