from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text, JSON, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    sessions = relationship("FocusSession", back_populates="user")


class FocusSession(Base):
    __tablename__ = "focus_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    start_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    end_time = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="sessions")
    reflections = relationship("Reflection", back_populates="session", cascade="all, delete-orphan")


class Reflection(Base):
    __tablename__ = "reflections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("focus_sessions.id", ondelete="CASCADE"), nullable=False)
    phase = Column(String, nullable=False)  # "before" or "after"

    goal = Column(Text, nullable=True)
    levers = Column(ARRAY(Text), nullable=True)   # Postgres array type
    state = Column(JSON, default={})  # { "score": 5, "text": "Feeling distracted" }
    model = Column(Text, nullable=True)

    state_metadata = Column(JSON, default={})  # embeddings, sentiment, etc.
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    session = relationship("FocusSession", back_populates="reflections")
