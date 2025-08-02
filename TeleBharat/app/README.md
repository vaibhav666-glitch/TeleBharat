
A comprehensive FastAPI-based medical appointment booking system with real-time notifications, WebSocket support, and complete CRUD operations for users, patients, doctors, and appointments.

## ✨ Features

### 🔐 User Management & Authentication
- JWT-based user registration with automatic token generation
- Secure login API with token-based authentication
- Bcrypt password hashing for maximum security
- Role-based access control (Patient, Doctor)
- Protected routes requiring valid JWT tokens
- Token-based authorization for all API endpoints
- Email validation and unique constraints

### 👥 Patient & Doctor Management
- Patient medical records and diagnosis tracking
- Doctor specialization and license management
- Relationship mapping between users and their roles
- Advanced search and filtering capabilities

### 📅 Appointment System
- Real-time appointment booking with conflict detection
- Multiple appointment statuses (Pending, Confirmed, Cancelled, Completed, In Progress)
- Duration-based scheduling with automatic conflict prevention
- Patient and doctor-specific appointment views

### 🔔 Real-time Notifications
- WebSocket-based real-time notifications
- Doctor online/offline status tracking
- Instant appointment updates for all parties
- User-specific and broadcast messaging

### 🚀 Advanced Features
- RESTful API with comprehensive documentation
- Database relationships with SQLAlchemy ORM
- Pydantic data validation and serialization
- Pagination and advanced filtering
- Error handling and validation

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.8+)
- **Database**: SQLAlchemy ORM (SQLite/PostgreSQL/MySQL)
- **Validation**: Pydantic v2
- **Authentication**: JWT tokens + Bcrypt password hashing
- **WebSocket**: Real-time notifications and status updates
- **Authentication**: JWT (optional integration)
- **Documentation**: Automatic OpenAPI/Swagger

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/medical-appointment-system.git
cd medical-appointment-system
