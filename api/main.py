import sys
import os
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import hashlib
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from database_manager_sqlite import DatabaseManager
from auth_manager import AuthManager
from vault_manager import VaultManager
from crypto_utils import CryptoUtils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_manager, auth_manager, vault_manager, crypto_utils
    try:
        logger.info("Initializing database and managers...")
        db_manager = DatabaseManager()
        crypto_utils = CryptoUtils()
        auth_manager = AuthManager(db_manager, crypto_utils)
        vault_manager = VaultManager(db_manager, crypto_utils)
        
        if not db_manager.initialize_db():
            raise Exception("Failed to initialize database")
        logger.info("Database and managers initialized successfully")
        yield
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise

app = FastAPI(
    title="Secure Vault API",
    version="1.0.0",
    description="A secure password vault API with encrypted storage",
    lifespan=lifespan
)
security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global managers - initialized in lifespan
db_manager = None
crypto_utils = None
auth_manager = None
vault_manager = None

active_sessions: Dict[str, Dict[str, Any]] = {}


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)


class VaultEntryCreate(BaseModel):
    service_name: str = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=200)
    notes: Optional[str] = Field(default="", max_length=500)


class VaultEntryUpdate(BaseModel):
    password: Optional[str] = Field(None, min_length=1, max_length=200)
    notes: Optional[str] = Field(None, max_length=500)


class UserResponse(BaseModel):
    id: int
    username: str


class VaultEntryResponse(BaseModel):
    id: int
    service_name: str
    username: str
    password: str
    notes: str
    created_at: str
    updated_at: str


def get_current_session(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    session = active_sessions.get(credentials.credentials)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")
    return session


def create_session_token(user_id: int, username: str, password: str) -> str:
    token_data = f"session_{user_id}_{hash(username + password)}"
    return hashlib.sha256(token_data.encode()).hexdigest()


@app.get("/")
async def root():
    return {"message": "Secure Vault API is running", "version": "1.0.0"}


@app.post("/api/register", response_model=Dict[str, str])
async def register(user: UserCreate):
    success = auth_manager.register_user(user.username, user.password)
    if not success:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    return {"message": "User registered successfully"}


@app.post("/api/login", response_model=Dict[str, Any])
async def login(user: UserLogin):
    result = auth_manager.login_user(user.username, user.password)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    session_token = create_session_token(result['user']['id'], user.username, user.password)
    active_sessions[session_token] = {
        'user': result['user'],
        'master_key': result['master_key']
    }
    
    return {
        "message": "Login successful",
        "token": session_token,
        "user": result['user']
    }


@app.get("/api/check-username/{username}")
async def check_username(username: str):
    existing_user = db_manager.fetch_one(
        "SELECT id FROM users WHERE username = ?", (username,)
    )
    return {"available": existing_user is None}


@app.post("/api/vault/entries", response_model=Dict[str, str])
async def create_vault_entry(entry: VaultEntryCreate, session: Dict[str, Any] = Depends(get_current_session)):
    success = vault_manager.add_entry(
        session['user']['id'],
        entry.service_name,
        entry.username,
        entry.password,
        entry.notes,
        session['master_key']
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create entry")
    
    return {"message": "Entry created successfully"}


@app.get("/api/vault/entries", response_model=List[VaultEntryResponse])
async def get_vault_entries(session: Dict[str, Any] = Depends(get_current_session)):
    entries = vault_manager.get_all_entries(session['user']['id'], session['master_key'])
    return [
        VaultEntryResponse(
            id=entry['id'],
            service_name=entry['service_name'],
            username=entry['username'],
            password=entry['password'],
            notes=entry['notes'],
            created_at=str(entry['created_at']),
            updated_at=str(entry['updated_at'])
        )
        for entry in entries
    ]


@app.get("/api/vault/entries/{service_name}")
async def get_vault_entry_by_service(service_name: str, session: Dict[str, Any] = Depends(get_current_session)):
    entry = vault_manager.get_entry_by_service(session['user']['id'], service_name, session['master_key'])
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    return VaultEntryResponse(
        id=entry['id'],
        service_name=entry['service_name'],
        username=entry['username'],
        password=entry['password'],
        notes=entry['notes'],
        created_at=str(entry['created_at']),
        updated_at=str(entry['updated_at'])
    )


@app.put("/api/vault/entries/{entry_id}")
async def update_vault_entry(entry_id: int, entry: VaultEntryUpdate, session: Dict[str, Any] = Depends(get_current_session)):
    success = vault_manager.update_entry(
        session['user']['id'],
        entry_id,
        entry.password,
        entry.notes,
        session['master_key']
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update entry")
    
    return {"message": "Entry updated successfully"}


@app.delete("/api/vault/entries/{entry_id}")
async def delete_vault_entry(entry_id: int, session: Dict[str, Any] = Depends(get_current_session)):
    success = vault_manager.delete_entry(session['user']['id'], entry_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete entry")
    
    return {"message": "Entry deleted successfully"}


@app.delete("/api/user/delete")
async def delete_user_account(user: UserLogin, session: Dict[str, Any] = Depends(get_current_session)):
    auth_result = auth_manager.login_user(user.username, user.password)
    if not auth_result or auth_result['user']['id'] != session['user']['id']:
        raise HTTPException(status_code=401, detail="Invalid password")
    
    db_manager.execute_query("DELETE FROM vault_entries WHERE user_id = ?", (session['user']['id'],))
    success = db_manager.execute_query("DELETE FROM users WHERE id = ?", (session['user']['id'],))
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete account")
    
    return {"message": "Account deleted successfully"}


@app.post("/api/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    active_sessions.pop(credentials.credentials, None)
    return {"message": "Logged out successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)

