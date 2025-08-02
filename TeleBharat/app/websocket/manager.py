from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
from datetime import datetime
import asyncio

class ConnectionManager:
    def __init__(self):
        # Store active connections by user type and ID
        self.active_connections: Dict[str, List[WebSocket]] = {
            "doctors": [],
            "patients": [],
            "general": []
        }
        # Store user-specific connections
        self.user_connections: Dict[int, WebSocket] = {}
        # Store doctor status
        self.doctor_status: Dict[int, Dict] = {}
    
    async def connect(self, websocket: WebSocket, user_type: str = "general", user_id: int = None):
        await websocket.accept()
        
        # Add to general connections
        if user_type in self.active_connections:
            self.active_connections[user_type].append(websocket)
        
        # Store user-specific connection
        if user_id:
            self.user_connections[user_id] = websocket
            
        print(f"New {user_type} connection established. User ID: {user_id}")
    
    def disconnect(self, websocket: WebSocket, user_type: str = "general", user_id: int = None):
        # Remove from general connections
        if user_type in self.active_connections:
            if websocket in self.active_connections[user_type]:
                self.active_connections[user_type].remove(websocket)
        
        # Remove user-specific connection
        if user_id and user_id in self.user_connections:
            del self.user_connections[user_id]
            
        print(f"{user_type} connection closed. User ID: {user_id}")
    
    async def send_personal_message(self, message: str, user_id: int):
        """Send message to specific user"""
        if user_id in self.user_connections:
            websocket = self.user_connections[user_id]
            try:
                await websocket.send_text(message)
            except:
                # Connection might be closed, remove it
                del self.user_connections[user_id]
    
    async def broadcast_to_type(self, message: str, user_type: str):
        """Broadcast message to all users of a specific type"""
        if user_type in self.active_connections:
            disconnected = []
            for connection in self.active_connections[user_type]:
                try:
                    await connection.send_text(message)
                except:
                    disconnected.append(connection)
            
            # Remove disconnected connections
            for conn in disconnected:
                self.active_connections[user_type].remove(conn)
    
    async def broadcast_to_all(self, message: str):
        """Broadcast message to all connected users"""
        for user_type in self.active_connections:
            await self.broadcast_to_type(message, user_type)
    
    async def update_doctor_status(self, doctor_id: int, status: str):
        """Update doctor status and notify all connected users"""
        self.doctor_status[doctor_id] = {
            "status": status,
            "last_updated": datetime.utcnow().isoformat()
        }
        
        # Broadcast status update
        status_message = {
            "type": "doctor_status_update",
            "doctor_id": doctor_id,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.broadcast_to_all(json.dumps(status_message))
    
    def get_doctor_status(self, doctor_id: int) -> Dict:
        """Get current status of a doctor"""
        return self.doctor_status.get(doctor_id, {"status": "offline", "last_updated": None})
    
    async def notify_appointment_update(self, appointment_data: Dict, action: str):
        """Notify relevant users about appointment updates"""
        message = {
            "type": f"appointment_{action}",
            "data": appointment_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Notify the patient
        if "patient_id" in appointment_data:
            await self.send_personal_message(
                json.dumps({**message, "message": f"Your appointment has been {action}"}),
                appointment_data["patient_id"]
            )
        
        # Notify the doctor
        if "doctor_id" in appointment_data:
            await self.send_personal_message(
                json.dumps({**message, "message": f"Appointment has been {action}"}),
                appointment_data["doctor_id"]
            )

# Global connection manager instance
manager = ConnectionManager()