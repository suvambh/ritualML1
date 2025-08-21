from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
from datetime import datetime
import uuid


# ---------- USER ----------
class UserBase(BaseModel):
    name: Optional[str] = None
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        orm_mode = True


# ---------- FOCUS SESSION ----------
class FocusSessionCreate(BaseModel):
    user_id: uuid.UUID
    duration_minutes: int


class FocusSessionRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    start_time: datetime
    end_time: Optional[datetime]
    duration_minutes: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True


# ---------- REFLECTION ----------
class ReflectionBase(BaseModel):
    phase: str  # "before" or "after"
    goal: Optional[str] = None
    levers: Optional[List[str]] = None
    state: Optional[Dict] = None  # {"score": 5, "text": "Feeling distracted"}
    model: Optional[str] = None


class ReflectionCreate(ReflectionBase):
    session_id: uuid.UUID


class ReflectionRead(ReflectionBase):
    id: uuid.UUID
    session_id: uuid.UUID
    created_at: datetime

    class Config:
        orm_mode = True
