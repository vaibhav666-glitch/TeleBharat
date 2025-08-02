```

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
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=sqlite:///./medical_system.db
SECRET_KEY=your-super-secret-jwt-key-here-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🏗️ Project Structure

```
TELEBHARAT/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── database.py                # Database configuration
│   ├── config.py                  # Configuration settings
│   ├── auth/
│   │   ├── __init__.py
│   │   └── auth_service.py        # JWT authentication service
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py               # User model
│   │   ├── patient.py            # Patient model
│   │   ├── doctor.py             # Doctor model
│   │   └── appointment.py        # Appointment model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user_schema.py        # User Pydantic schemas
│   │   ├── patient_schema.py     # Patient Pydantic schemas
│   │   ├── doctor_schema.py      # Doctor Pydantic schemas
│   │   └── appointment_schema.py # Appointment Pydantic schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── user_routes.py        # User & Auth endpoints
│   │   ├── patient_routes.py     # Patient endpoints (Protected)
│   │   ├── doctor_routes.py      # Doctor endpoints (Protected)
│   │   └── appointment_routes.py # Appointment endpoints (Protected)
│   └── websocket/
│       ├── __init__.py
│       └── manager.py            # WebSocket connection manager
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 🔌 API Endpoints

### 👤 Users & Authentication
- `POST /users/register` - Register new user (returns JWT token)
- `POST /users/login` - User login (returns JWT token)
- `GET /users/` - Get all users (🔒 Protected)
- `GET /users/{user_id}` - Get user by ID (🔒 Protected)
- `PUT /users/{user_id}` - Update user (🔒 Protected)
- `DELETE /users/{user_id}` - Delete user (🔒 Protected)

### 🏥 Patients
- `POST /patients/` - Register patient (🔒 Protected)
- `GET /patients/` - Get all patients with pagination (🔒 Protected)
- `GET /patients/{patient_id}` - Get patient by ID (🔒 Protected)
- `GET /patients/user/{user_id}` - Get patient by user ID (🔒 Protected)
- `PUT /patients/{patient_id}` - Update patient (🔒 Protected)
- `DELETE /patients/{patient_id}` - Delete patient (🔒 Protected)
- `GET /patients/search/` - Search patients (🔒 Protected)

### 👨‍⚕️ Doctors
- `POST /doctors/` - Register doctor (🔒 Protected)
- `GET /doctors/` - Get all doctors with pagination (🔒 Protected)
- `GET /doctors/{doctor_id}` - Get doctor by ID (🔒 Protected)
- `GET /doctors/user/{user_id}` - Get doctor by user ID (🔒 Protected)
- `GET /doctors/license/{license_number}` - Get doctor by license (🔒 Protected)
- `PUT /doctors/{doctor_id}` - Update doctor (🔒 Protected)
- `DELETE /doctors/{doctor_id}` - Delete doctor (🔒 Protected)
- `GET /doctors/search/` - Search doctors (🔒 Protected)
- `GET /doctors/specializations/` - Get all specializations (🔒 Protected)

### 📅 Appointments
- `POST /appointments/` - Create appointment (🔒 Protected)
- `GET /appointments/` - Get all appointments with filtering (🔒 Protected)
- `GET /appointments/{appointment_id}` - Get appointment by ID (🔒 Protected)
- `GET /appointments/patient/{patient_id}` - Get patient appointments (🔒 Protected)
- `GET /appointments/doctor/{doctor_id}` - Get doctor appointments (🔒 Protected)
- `PUT /appointments/{appointment_id}` - Update appointment (🔒 Protected)
- `DELETE /appointments/{appointment_id}` - Cancel appointment (🔒 Protected)

### 🔔 WebSocket & Status (Real-time)
- `WS /appointments/ws/{user_type}/{user_id}` - User-specific connection (🔒 Token Required)
- `WS /appointments/ws/general` - General notifications
- `GET /appointments/doctor/{doctor_id}/status` - Get doctor status (🔒 Protected)
- `POST /appointments/doctor/{doctor_id}/status` - Update doctor status (🔒 Protected)

## 💡 Usage Examples

### User Registration (Gets Token Automatically)
```python
import requests

# Register new user - automatically returns JWT token
user_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "gender": "Male",
    "contact_number": "+1234567890",
    "role": "patient",
    "password": "securepassword123"
}

response = requests.post("http://localhost:8000/users/register", json=user_data)
result = response.json()
token = result["access_token"]  # JWT token automatically generated
print(f"Token: {token}")
```

### User Login (Get Token)
```python
# Login existing user to get token
login_data = {
    "email": "john.doe@example.com",
    "password": "securepassword123"
}

response = requests.post("http://localhost:8000/users/login", json=login_data)
result = response.json()
token = result["access_token"]
print(f"Login Token: {token}")
```

### Using Token for Protected Routes
```python
# Use token in headers for protected routes
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Create patient (protected route)
patient_data = {
    "user_id": 1,
    "medical_record": "Patient has history of diabetes",
    "diagnosis": "Type 2 Diabetes"
}

response = requests.post(
    "http://localhost:8000/patients/", 
    json=patient_data, 
    headers=headers
)
print(response.json())

### Creating an Appointment (Protected)
```python
# Must include JWT token in headers
headers = {
    "Authorization": f"Bearer {your_jwt_token}",
    "Content-Type": "application/json"
}

appointment_data = {
    "patient_id": 1,
    "doctor_id": 2,
    "appointment_date": "2025-08-15T10:00:00",
    "duration_minutes": 45,
    "reason": "Regular checkup"
}

response = requests.post(
    "http://localhost:8000/appointments/", 
    json=appointment_data,
    headers=headers
)
print(response.json())
```

### WebSocket Connection with JWT (JavaScript)
```javascript
// Connect with JWT token in URL parameters or send after connection
const token = 'your_jwt_token_here';
const ws = new WebSocket(`ws://localhost:8000/appointments/ws/patients/1?token=${token}`);

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received notification:', data);
    
    if (data.type === 'appointment_created') {
        showNotification(`New appointment: ${data.message}`);
    }
};

// Send status update (for doctors)
ws.send(JSON.stringify({
    type: "status_update",
    status: "online"
}));
```

## 🔍 Advanced Features

### Filtering and Search
- **Appointments**: Filter by status, date range, patient, or doctor
- **Patients**: Search by name, email, or diagnosis
- **Doctors**: Search by name, specialization, or license number
- **Pagination**: All list endpoints support `skip` and `limit` parameters

### Real-time Notifications
- Appointment creation/updates
- Doctor status changes (online/offline/busy)
- Automatic cleanup of disconnected WebSocket connections
- User-specific and broadcast messaging

### Authentication Flow
- **Registration**: Creates user account and automatically generates JWT token
- **Login**: Validates credentials and returns JWT token
- **Protected Routes**: All routes except registration/login require valid JWT token in Authorization header
- **Token Format**: `Authorization: Bearer <your_jwt_token>`
- **Token Expiry**: Configurable via `ACCESS_TOKEN_EXPIRE_MINUTES` in environment variables
### Data Validation & Security
- JWT token validation for all protected routes
- Bcrypt password hashing (never store plain text passwords)
- Email format validation
- Future date validation for appointments
- Unique constraints (email, license numbers)
- Duration limits (15-180 minutes)
- Conflict detection for appointments

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    gender VARCHAR,
    contact_number VARCHAR,
    password_hash VARCHAR NOT NULL,
    role VARCHAR NOT NULL
);
```

### Patients Table
```sql
CREATE TABLE patients (
    id INTEGER PRIMARY KEY,
    medical_record TEXT,
    diagnosis VARCHAR,
    FOREIGN KEY(id) REFERENCES users(id)
);
```

### Doctors Table
```sql
CREATE TABLE doctors (
    id INTEGER PRIMARY KEY,
    specialization VARCHAR NOT NULL,
    license_number VARCHAR UNIQUE,
    FOREIGN KEY(id) REFERENCES users(id)
);
```

### Appointments Table
```sql
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    appointment_date DATETIME NOT NULL,
    duration_minutes INTEGER DEFAULT 30,
    status VARCHAR DEFAULT 'pending',
    reason TEXT,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(patient_id) REFERENCES patients(id),
    FOREIGN KEY(doctor_id) REFERENCES doctors(id)
);
```

## 🧪 Testing

### Manual Testing
Use the interactive API documentation at `http://localhost:8000/docs` to test all endpoints.

### Example Test Workflow
1. Register a new user with role "patient" (receives JWT token)
2. Use token to create a patient record for that user
3. Register another user with role "doctor" (receives JWT token)  
4. Use token to create a doctor record for that user
5. Use either token to create an appointment between patient and doctor
6. Test WebSocket connection with JWT token for real-time updates
7. Test login endpoint to get fresh tokens

## 🚀 Deployment

### Production Setup
1. Set up a production database (PostgreSQL recommended)
2. Configure environment variables for production
3. Use a production WSGI server like Gunicorn
4. Set up reverse proxy with Nginx
5. Configure SSL certificates

### Example Production Command
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

**1. Email Validator Error**
```bash
pip install email-validator
# or
pip install pydantic[email]
```

**2. Database Connection Issues**
- Check your `DATABASE_URL` in `.env`
- Ensure database file permissions are correct
- For PostgreSQL/MySQL, verify connection credentials

**3. JWT Token Issues**
- Ensure `SECRET_KEY` is set in environment variables
- Check token expiry time in `ACCESS_TOKEN_EXPIRE_MINUTES`
- Verify token format: `Authorization: Bearer <token>`
- For protected routes, always include valid JWT token in headers
- Check if port 8000 is available
- Verify firewall settings
- Ensure WebSocket endpoint URLs are correct

**4. WebSocket Connection Failed**
- Verify all dependencies are installed
- Check Python path and virtual environment activation
- Ensure all `__init__.py` files are present

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

## 🔄 Version History

- **v1.0.0** - Initial release with full CRUD operations and WebSocket support
- **v1.1.0** - Added advanced search and filtering capabilities
- **v1.2.0** - Enhanced real-time notifications and doctor status tracking

---

**Made with ❤️ for better healthcare management**
