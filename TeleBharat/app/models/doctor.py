from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

# Updated Doctor Model
class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    specialization = Column(String, nullable=False)
    license_number = Column(String, unique=True)
    
    # Relationships
    user = relationship("User", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
    
    def __repr__(self):
        return f"<Doctor(id={self.id}, specialization='{self.specialization}')>"