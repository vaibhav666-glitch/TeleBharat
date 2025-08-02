from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user_routes, patient_routes, doctor_routes, appointment_routes
from app.database import engine, Base
from sqlalchemy import inspect

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Medical Appointment System",
    description="A comprehensive medical appointment booking system with real-time notifications",
    version="1.0.0"
)

def check_user_table_columns():
    inspector = inspect(engine)
    columns = inspector.get_columns("users")
    print("=== USERS TABLE COLUMNS SEEN BY SQLALCHEMY ===")
    for column in columns:
        print(column["name"])

if __name__ == "__main__":
    check_user_table_columns()

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_routes.router)
app.include_router(patient_routes.router)
app.include_router(doctor_routes.router)
app.include_router(appointment_routes.router)

@app.get("/")
def read_root():
    return {
        "message": "Medical Appointment System API",
        "version": "1.0.0",
        "endpoints": {
            "users": "/users",
            "patients": "/patients", 
            "doctors": "/doctors",
            "appointments": "/appointments",
            "websocket": "/appointments/ws"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "medical-appointment-system"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)